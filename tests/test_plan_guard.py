"""Offline behavior tests. Never discover, connect to, or mutate a device."""

from contextlib import redirect_stderr, redirect_stdout
import copy
from datetime import datetime, timedelta, timezone
import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('plan_guard', ROOT / 'scripts' / 'plan_guard.py')
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)
NOW = datetime(2026, 10, 19, 12, 0, tzinfo=timezone.utc)
CANDIDATE = 'com.example.promotions'


class PlanGuardTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = json.loads((ROOT / 'examples/snapshot.synthetic.json').read_text(encoding='utf-8'))
        self.plan = json.loads((ROOT / 'examples/plan.synthetic.json').read_text(encoding='utf-8'))
        self.snapshot['synthetic'] = False
        self.snapshot['captured_at'] = NOW.isoformat()

    def report(self):
        return guard.build_report(self.snapshot, self.plan, now=NOW)

    def rejected(self):
        with self.assertRaises(guard.PlanError):
            self.report()

    def rename_candidate(self, name):
        self.snapshot['packages'][name] = self.snapshot['packages'].pop(CANDIDATE)
        self.plan['actions'][0]['package'] = name

    def test_default_state_is_restored_exactly(self):
        action = self.report()['actions'][0]
        self.assertEqual(action['forward_argv'], ['adb', '-s', 'SYNTHETIC-TV-ONLY', 'shell', 'pm', 'disable-user', '--user', '0', CANDIDATE])
        self.assertEqual(action['rollback_argv'][-5:], ['pm', 'default-state', '--user', '0', CANDIDATE])
        self.assertEqual(action['readback_argv'][-3:], ['dumpsys', 'package', CANDIDATE])
        self.assertEqual(self.report()['authorization'], 'required')

    def test_explicit_enable_is_restored_exactly(self):
        self.snapshot['packages'][CANDIDATE]['enabled_setting'] = 1
        self.assertEqual(self.report()['actions'][0]['rollback_argv'][-4:], ['enable', '--user', '0', CANDIDATE])

    def test_preexisting_disabled_states_are_not_touched(self):
        for state in (2, 3, 4):
            with self.subTest(state=state):
                self.snapshot['packages'][CANDIDATE]['enabled_setting'] = state
                self.rejected()

    def test_target_mismatch(self):
        for key, value in [('serial', 'OTHER-TV'), ('fingerprint', 'another/build'), ('platform', 'android-tv'), ('android_sdk', 33)]:
            with self.subTest(key=key):
                old = self.plan['device'][key]
                self.plan['device'][key] = value
                self.rejected()
                self.plan['device'][key] = old

    def test_reject_non_owner_users(self):
        for key in ('current_user',):
            self.snapshot[key] = 10
            self.rejected()
        self.snapshot['current_user'] = 0
        self.snapshot['device']['user_id'] = 10
        self.plan['device']['user_id'] = 10
        self.rejected()

    def test_boolean_is_not_an_integer(self):
        self.snapshot['device']['user_id'] = False
        self.plan['device']['user_id'] = False
        self.rejected()

    def test_unsupported_platforms(self):
        for platform in ('fire-os', 'tizen', 'webos', 'android', None):
            with self.subTest(platform=platform):
                self.snapshot['device']['platform'] = platform
                self.plan['device']['platform'] = platform
                self.rejected()

    def test_managed_device(self):
        self.snapshot['managed'] = True
        self.rejected()

    def test_stale_snapshot(self):
        self.snapshot['captured_at'] = (NOW - timedelta(hours=24, seconds=1)).isoformat()
        self.rejected()

    def test_future_snapshot(self):
        self.snapshot['captured_at'] = (NOW + timedelta(minutes=5, seconds=1)).isoformat()
        self.rejected()

    def test_recent_snapshot_and_clock_skew(self):
        self.snapshot['captured_at'] = (NOW + timedelta(minutes=4)).isoformat()
        self.report()

    def test_naive_or_invalid_timestamp(self):
        for timestamp in ('2026-10-19T12:00:00', 'not-a-date', ''):
            with self.subTest(timestamp=timestamp):
                self.snapshot['captured_at'] = timestamp
                self.rejected()

    def test_shell_injection_package_identifiers(self):
        for name in ('com.example.a;reboot', 'com.example.a && id', 'com.example.$(id)', 'com.example.`id`', 'com.example.a/.Main', '-s', 'com.example.a\nreboot', 'com.exämple.a'):
            with self.subTest(name=name):
                self.plan['actions'][0]['package'] = name
                self.rejected()

    def test_shell_injection_serials(self):
        for serial in ('-s', 'tv;reboot', 'tv $(id)', 'tv\nother', 'tv`id`'):
            with self.subTest(serial=serial):
                self.snapshot['device']['serial'] = serial
                self.plan['device']['serial'] = serial
                self.rejected()

    def test_ip_and_port_are_preserved_as_one_argument(self):
        for serial in ('192.0.2.10:5555', 'test-tv.local:39001'):
            with self.subTest(serial=serial):
                self.snapshot['device']['serial'] = serial
                self.plan['device']['serial'] = serial
                self.assertEqual(self.report()['actions'][0]['forward_argv'][2], serial)

    def test_protected_names(self):
        for name in ('com.google.android.tungsten.setupwraith', 'com.google.android.apps.tv.launcherx', 'com.android.systemui', 'com.vendor.updater', 'com.vendor.fota', 'com.vendor.bluetooth', 'com.vendor.remotecontrol', 'com.vendor.hdmiinput', 'com.vendor.widevine', 'com.vendor.contentprovider', 'com.vendor.assistant', 'com.vendor.keyboard', 'com.vendor.network', 'com.vendor.accessibility', 'com.netflix.ninja'):
            with self.subTest(name=name):
                self.snapshot['packages'][name] = copy.deepcopy(self.snapshot['packages'][CANDIDATE])
                self.plan['actions'][0]['package'] = name
                self.rejected()

    def test_dynamic_protected_package(self):
        self.snapshot['protected_packages'].append(CANDIDATE)
        self.rejected()

    def test_all_home_candidates_are_protected(self):
        self.snapshot['home_candidates'].append(CANDIDATE + '/.MainActivity')
        self.rejected()

    def test_all_imes_are_protected(self):
        self.snapshot['ime_packages'].append(CANDIDATE)
        self.rejected()

    def test_opaque_unknown_dependency_is_not_inferred(self):
        # The guard has no semantic oracle: a real reviewer must supply protection.
        self.rename_candidate('com.vendor.opaque')
        self.snapshot['protected_packages'].append('com.vendor.opaque')
        self.rejected()

    def test_missing_critical_inventory(self):
        del self.snapshot['packages']['com.vendor.input']
        self.rejected()

    def test_missing_candidate(self):
        del self.snapshot['packages'][CANDIDATE]
        self.rejected()

    def test_missing_evidence(self):
        self.snapshot['packages'][CANDIDATE]['evidence'] = ''
        self.rejected()

    def test_missing_dependency_review(self):
        self.snapshot['critical_review'] = '  '
        self.rejected()

    def test_missing_plan_reason_evidence_or_checks(self):
        for key in ('rationale', 'evidence', 'verify'):
            with self.subTest(key=key):
                old = self.plan['actions'][0][key]
                self.plan['actions'][0][key] = ''
                self.rejected()
                self.plan['actions'][0][key] = old

    def test_hidden_suspended_uninstalled_or_ineffective(self):
        for key, value in [('hidden', True), ('suspended', True), ('installed', False), ('effectively_enabled', False)]:
            with self.subTest(key=key):
                old = self.snapshot['packages'][CANDIDATE][key]
                self.snapshot['packages'][CANDIDATE][key] = value
                self.rejected()
                self.snapshot['packages'][CANDIDATE][key] = old

    def test_invalid_baseline_state_type(self):
        for value in (True, '0', 0.0, -1, 5):
            with self.subTest(value=value):
                self.snapshot['packages'][CANDIDATE]['enabled_setting'] = value
                self.rejected()

    def test_non_boolean_flag(self):
        self.snapshot['packages'][CANDIDATE]['installed'] = 1
        self.rejected()

    def test_duplicate_action(self):
        self.plan['actions'].append(copy.deepcopy(self.plan['actions'][0]))
        self.rejected()

    def test_batch_limit_and_empty_plan(self):
        self.plan['actions'] = []
        self.rejected()
        self.plan['actions'] = [{} for _ in range(6)]
        self.rejected()

    def test_up_to_five_distinct_actions(self):
        base = copy.deepcopy(self.plan['actions'][0])
        self.plan['actions'] = []
        for index in range(5):
            name = f'com.example.promotion{index}'
            self.snapshot['packages'][name] = copy.deepcopy(self.snapshot['packages'][CANDIDATE])
            self.plan['actions'].append(dict(base, package=name))
        self.assertEqual(len(self.report()['actions']), 5)

    def test_unknown_command_or_approval_field(self):
        for field in ('command', 'shell', 'approved', 'operation'):
            with self.subTest(field=field):
                self.plan['actions'][0][field] = 'anything'
                self.rejected()
                del self.plan['actions'][0][field]

    def test_unknown_top_level_field(self):
        self.plan['approved'] = True
        self.rejected()

    def test_duplicate_home_candidate(self):
        self.snapshot['home_candidates'] *= 2
        self.rejected()

    def test_home_chooser(self):
        self.snapshot['home_component'] = 'android/.ResolverActivity'
        self.snapshot['home_candidates'].append('android/.ResolverActivity')
        self.rejected()

    def test_unknown_home_or_malformed_home(self):
        for home in ('com.other.home/.Main', None, [], {}, 'com.vendor.home/.Main;id'):
            with self.subTest(home=home):
                self.snapshot['home_component'] = home
                self.rejected()

    def test_inactive_home(self):
        self.snapshot['packages']['com.vendor.home']['effectively_enabled'] = False
        self.rejected()

    def test_text_control_characters(self):
        self.plan['actions'][0]['rationale'] = 'fake\x1b[31mreason'
        self.rejected()

    def test_demo_has_no_executable_arrays(self):
        self.snapshot['synthetic'] = True
        self.snapshot['captured_at'] = '2020-01-01T00:00:00Z'
        report = guard.build_report(self.snapshot, self.plan, demo=True, now=NOW)
        self.assertEqual(report['mode'], 'synthetic-demo-no-execution')
        self.assertFalse(any(key.endswith('_argv') for item in report['actions'] for key in item))

    def test_synthetic_cannot_enter_real_mode(self):
        self.snapshot['synthetic'] = True
        self.rejected()

    def test_real_cannot_enter_demo_mode(self):
        with self.assertRaises(guard.PlanError):
            guard.build_report(self.snapshot, self.plan, demo=True, now=NOW)

    def test_json_loader_rejects_duplicate_keys_and_nonfinite_numbers(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.json'
            for content in ('{"x":1,"x":2}', '{"x": NaN}', '{"x": Infinity}', '{"x": -Infinity}', 'not JSON', '{"x": {"a": 1, "a": 2}}'):
                with self.subTest(content=content):
                    path.write_text(content, encoding='utf-8')
                    with self.assertRaises(guard.PlanError):
                        guard.load_json(path)

    def test_json_loader_rejects_oversize_and_invalid_encoding(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.json'
            for content in (b' ' * (guard.MAX_BYTES + 1), b'\xff\xfe'):
                path.write_bytes(content)
                with self.assertRaises(guard.PlanError):
                    guard.load_json(path)

    def test_cli_demo_output_and_digests(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = guard.main(['--snapshot', str(ROOT/'examples/snapshot.synthetic.json'), '--plan', str(ROOT/'examples/plan.synthetic.json'), '--demo'])
        self.assertEqual(code, 0, err.getvalue())
        report = json.loads(out.getvalue())
        self.assertEqual(len(report['input_sha256']['snapshot']), 64)
        self.assertEqual(report['authorization'], 'not-applicable')

    def test_malformed_json_shapes_fail_closed(self):
        values = [None, True, 0, 0.5, "", [], {}]
        for field in self.snapshot:
            for value in values:
                snapshot = copy.deepcopy(self.snapshot)
                snapshot[field] = value
                with self.subTest(field=field, value=value):
                    try:
                        guard.build_report(snapshot, self.plan, now=NOW)
                    except guard.PlanError:
                        pass
                    else:
                        # False is correct for managed/synthetic; zero is current_user.
                        self.assertEqual(type(value), type(self.snapshot[field]))
                        self.assertEqual(value, self.snapshot[field])

    def test_missing_snapshot_field(self):
        for field in self.snapshot:
            snapshot = copy.deepcopy(self.snapshot)
            del snapshot[field]
            with self.subTest(field=field):
                with self.assertRaises(guard.PlanError):
                    guard.build_report(snapshot, self.plan, now=NOW)

    def test_cli_fresh_real_report_is_still_review_only(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot['captured_at'] = datetime.now(timezone.utc).isoformat()
        out, err = io.StringIO(), io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / 'snapshot.json'
            plan_path = Path(directory) / 'plan.json'
            snapshot_path.write_text(json.dumps(snapshot), encoding='utf-8')
            plan_path.write_text(json.dumps(self.plan), encoding='utf-8')
            with redirect_stdout(out), redirect_stderr(err):
                code = guard.main(['--snapshot', str(snapshot_path), '--plan', str(plan_path)])
        self.assertEqual(code, 0, err.getvalue())
        report = json.loads(out.getvalue())
        self.assertEqual(report['mode'], 'review-only-no-execution')
        self.assertEqual(report['authorization'], 'required')
        self.assertIn('rollback_argv', report['actions'][0])

    def test_hardware_identity_and_source_are_bound(self):
        for key, value in [('hardware_serial', 'OTHER-HARDWARE-002'), ('identity_property', 'ro.boot.serialno')]:
            with self.subTest(key=key):
                old = self.plan['device'][key]
                self.plan['device'][key] = value
                self.rejected()
                self.plan['device'][key] = old
        preflight = self.report()['preflight']
        self.assertEqual(preflight[0]['argv'][-2:], ['getprop', 'ro.serialno'])
        self.assertEqual(preflight[0]['expected'], 'SYNTHETIC-HARDWARE-001')

    def test_missing_or_placeholder_hardware_identity(self):
        for value in ('unknown', 'UNKNOWN', '', 'null', 'none', '00000000', 'serialno', 'bad;id'):
            with self.subTest(value=value):
                self.snapshot['device']['hardware_serial'] = value
                self.plan['device']['hardware_serial'] = value
                self.rejected()

    def test_unsupported_identity_source(self):
        self.snapshot['device']['identity_property'] = 'user-controlled;id'
        self.plan['device']['identity_property'] = 'user-controlled;id'
        self.rejected()

    def test_schema_one_is_not_upgraded_silently(self):
        self.snapshot['schema_version'] = 1
        self.plan['schema_version'] = 1
        self.rejected()

    def test_unicode_bidi_format_controls_and_surrogates(self):
        for codepoint in (0x202E, 0x202D, 0x2066, 0x2069, 0x200B, 0xD800, 0xDFFF):
            with self.subTest(codepoint=codepoint):
                self.plan['actions'][0]['evidence'] = 'Untrusted' + chr(codepoint) + 'text'
                self.rejected()

    def test_numeric_overflow_in_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.json'
            for value in ('1e9999', '-1e9999'):
                path.write_text('{"number":' + value + '}', encoding='utf-8')
                with self.assertRaises(guard.PlanError):
                    guard.load_json(path)

    def test_json_directory_is_not_an_input(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(guard.PlanError):
                guard.load_json(directory)

    def test_json_symlink_is_not_an_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'input.json'
            source.write_text('{}', encoding='utf-8')
            link = Path(directory) / 'link.json'
            try:
                link.symlink_to(source)
            except OSError:
                self.skipTest('Host does not permit symlink creation')
            with self.assertRaises(guard.PlanError):
                guard.load_json(link)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'POSIX named-pipe regression')
    def test_named_pipe_cli_fails_without_hanging(self):
        with tempfile.TemporaryDirectory() as directory:
            pipe = Path(directory) / 'input.fifo'
            os.mkfifo(pipe)
            result = subprocess.run([sys.executable, str(ROOT/'scripts/plan_guard.py'),
                '--snapshot', str(pipe), '--plan', str(ROOT/'examples/plan.synthetic.json'), '--demo'],
                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn('regular local file', result.stderr)

    def test_demo_has_no_preflight_commands(self):
        self.snapshot['synthetic'] = True
        report = guard.build_report(self.snapshot, self.plan, demo=True, now=NOW)
        self.assertNotIn('preflight', report)
        self.assertNotIn('argv', json.dumps(report))

    def test_cli_failure_has_no_partial_report(self):
        out, err = io.StringIO(), io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / 'missing.json')
            with redirect_stdout(out), redirect_stderr(err):
                code = guard.main(['--snapshot', missing, '--plan', missing])
        self.assertEqual(code, 2)
        self.assertEqual(out.getvalue(), '')
        self.assertIn('Validation failed', err.getvalue())

    def test_cli_real_mode_reports_invalid_input_without_commands(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = guard.main(['--snapshot', str(ROOT/'examples/snapshot.synthetic.json'), '--plan', str(ROOT/'examples/plan.synthetic.json')])
        self.assertEqual(code, 2)
        self.assertEqual(out.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
