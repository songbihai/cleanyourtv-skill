"""Synthetic publication regressions; no GitHub API, ADB, or device access."""

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_repository as checker
import build_release as builder


class ReleaseToolTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.parent = Path(self.temporary.name)
        self.root = self.parent / 'source'
        for name in checker.DISTRIBUTION_FILES:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)

    def assertRejected(self):
        errors = checker.check(self.root)
        self.assertTrue(errors)
        with self.assertRaises(ValueError):
            builder.archive_bytes(self.root)
        return errors

    def test_clean_declared_source_passes(self):
        self.assertEqual(checker.check(self.root), [])

    def test_env_file_is_rejected(self):
        (self.root / '.env').write_text('SYNTHETIC_SETTING=not-a-real-secret\n')
        self.assertTrue(any('.env' in e for e in self.assertRejected()))

    def test_undeclared_private_json_is_rejected(self):
        (self.root / 'snapshot.json').write_text('{}')
        self.assertRejected()

    def test_private_session_directory_is_rejected(self):
        (self.root / 'sessions').mkdir()
        (self.root / 'sessions' / 'state.json').write_text('{}')
        self.assertRejected()

    def test_binary_file_is_rejected(self):
        (self.root / 'device.png').write_bytes(b'not-an-image')
        self.assertRejected()

    def test_changed_promotional_asset_is_rejected(self):
        asset = self.root / next(iter(checker.PINNED_ASSETS))
        asset.write_bytes(asset.read_bytes() + b'undisclosed-content')
        self.assertTrue(any('asset differs' in e for e in self.assertRejected()))

    def test_missing_promotional_asset_is_rejected(self):
        (self.root / next(iter(checker.PINNED_ASSETS))).unlink()
        self.assertRejected()

    def test_undeclared_asset_is_rejected(self):
        (self.root / 'assets/tvremotex/private.png').write_bytes(b'private-evidence')
        self.assertRejected()

    def test_oversize_promotional_asset_is_rejected(self):
        (self.root / next(iter(checker.PINNED_ASSETS))).write_bytes(b'x' * (checker.MAX_ASSET_BYTES + 1))
        self.assertRejected()

    def test_broken_html_image_reference_is_rejected(self):
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n<img src="assets/tvremotex/missing.png" alt="Missing">\n')
        self.assertRejected()

    def test_external_local_html_image_reference_is_rejected(self):
        (self.parent / 'private.png').write_bytes(b'private-evidence')
        with (self.root / 'README.md').open('a') as stream:
            stream.write("\n<img src='../private.png' alt='Private'>\n")
        self.assertRejected()

    def test_missing_entrypoint_fails_without_traceback(self):
        (self.root / 'SKILL.md').unlink()
        self.assertTrue(any('SKILL.md' in e for e in self.assertRejected()))

    def test_incomplete_frontmatter_is_rejected(self):
        (self.root / 'SKILL.md').write_text('---\nname: cleanyourtv-skill\n')
        self.assertRejected()

    def test_bad_json_and_syntax_are_rejected(self):
        (self.root / 'examples' / 'plan.synthetic.json').write_text('not JSON')
        (self.root / 'scripts' / 'plan_guard.py').write_text('def invalid syntax')
        self.assertRejected()

    def test_non_utf8_is_rejected(self):
        (self.root / 'NOTICE').write_bytes(b'\xff\xfe')
        self.assertRejected()

    def test_oversize_source_is_rejected(self):
        (self.root / 'NOTICE').write_bytes(b'x' * (checker.MAX_FILE_BYTES + 1))
        self.assertRejected()

    def test_obvious_private_key_in_declared_file_is_rejected(self):
        # Construct at runtime so the source file is not itself a credential fixture.
        header = '-----BEGIN ' + 'OPENSSH PRIVATE KEY-----'
        (self.root / 'NOTICE').write_text(header + '\nSYNTHETIC\n')
        errors = self.assertRejected()
        self.assertTrue(any('credential' in e for e in errors))
        self.assertFalse(any(header in e for e in errors))

    def test_obvious_token_in_declared_file_is_rejected(self):
        (self.root / 'NOTICE').write_text('ghp_' + 'A' * 36)
        self.assertRejected()

    def test_source_symlink_is_rejected(self):
        outside = self.parent / 'outside.md'
        outside.write_text('Not distributable.')
        (self.root / 'NOTICE').unlink()
        try:
            (self.root / 'NOTICE').symlink_to(outside)
        except OSError:
            self.skipTest('Host does not permit symlink creation')
        self.assertRejected()

    def test_broken_relative_reference_is_rejected(self):
        with (self.root / 'README.md').open('a') as out:
            out.write('\n[Missing](missing.md)\n')
        self.assertRejected()

    def test_reference_outside_tree_is_rejected(self):
        (self.parent / 'outside.md').write_text('External private file.')
        with (self.root / 'README.md').open('a') as out:
            out.write('\n[External](../outside.md)\n')
        self.assertRejected()

    def test_version_drift_is_rejected(self):
        (self.root / 'VERSION').write_text('0.99.0\n')
        self.assertRejected()

    def test_skill_cannot_silently_select_another_upstream_revision(self):
        path = self.root / 'SKILL.md'
        path.write_text(path.read_text(encoding='utf-8').replace(checker.UPSTREAM_REVISION, '0' * 40), encoding='utf-8')
        self.assertTrue(any('upstream identity' in e for e in self.assertRejected()))

    def test_release_provenance_cannot_drift_from_reviewed_source(self):
        for name in ('NOTICE', 'references/upstream-review.md'):
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_text(encoding='utf-8')
                path.write_text(original.replace(checker.UPSTREAM_REVISION, '1' * 40), encoding='utf-8')
                self.assertTrue(any('provenance differs' in e for e in self.assertRejected()))
                path.write_text(original, encoding='utf-8')

    def test_real_evidence_cannot_replace_synthetic_example(self):
        path = self.root / 'examples/snapshot.synthetic.json'
        data = json.loads(path.read_text())
        data['synthetic'] = False
        path.write_text(json.dumps(data))
        self.assertRejected()

    def test_guard_cannot_add_a_process_dependency_unnoticed(self):
        path = self.root / 'scripts/plan_guard.py'
        with path.open('a') as stream:
            stream.write('\nimport subprocess\n')
        self.assertRejected()

    def test_guard_cannot_add_os_system_call_unnoticed(self):
        path = self.root / 'scripts/plan_guard.py'
        with path.open('a') as stream:
            stream.write('\nos.system("synthetic-only")\n')
        # This parses but never imports or executes the mutated source.
        self.assertRejected()

    def test_git_and_runtime_caches_do_not_enter_archive(self):
        for directory in ('.git', '__pycache__', '.venv'):
            path = self.root / directory
            path.mkdir()
            (path / 'local.txt').write_text('Must not enter the source archive.')
        self.assertEqual(checker.check(self.root), [])
        with zipfile.ZipFile(io.BytesIO(builder.archive_bytes(self.root))) as archive:
            self.assertEqual(set(archive.namelist()), {'cleanyourtv-skill/' + name for name in checker.DISTRIBUTION_FILES})

    def test_archive_is_deterministic_despite_source_mtime_and_mode(self):
        first = builder.archive_bytes(self.root)
        for name in checker.DISTRIBUTION_FILES:
            path = self.root / name
            os.utime(path, (1_000_000_000, 1_000_000_000))
            path.chmod(0o600)
        self.assertEqual(first, builder.archive_bytes(self.root))

    def test_archive_metadata_and_crc(self):
        with zipfile.ZipFile(io.BytesIO(builder.archive_bytes(self.root))) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(archive.namelist(), sorted(archive.namelist()))
            for info in archive.infolist():
                self.assertEqual(info.date_time, (2026, 1, 1, 0, 0, 0))
                self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                self.assertEqual((info.external_attr >> 16) & 0o777, 0o644)
                self.assertNotIn('..', info.filename.split('/'))

    def test_builder_writes_matching_checksum(self):
        output = self.parent / 'release.zip'
        digest = builder.build_release(output, self.root)
        self.assertEqual(digest, hashlib.sha256(output.read_bytes()).hexdigest())
        self.assertEqual(output.with_name('release.zip.sha256').read_text(), digest + '  release.zip\n')

    def test_existing_archive_is_not_overwritten(self):
        output = self.parent / 'release.zip'
        output.write_bytes(b'Existing user file')
        with self.assertRaises(ValueError):
            builder.build_release(output, self.root)
        self.assertEqual(output.read_bytes(), b'Existing user file')
        self.assertFalse(output.with_name('release.zip.sha256').exists())

    def test_existing_checksum_is_not_overwritten(self):
        output = self.parent / 'release.zip'
        checksum = self.parent / 'release.zip.sha256'
        checksum.write_text('Existing user file')
        with self.assertRaises(ValueError):
            builder.build_release(output, self.root)
        self.assertEqual(checksum.read_text(), 'Existing user file')
        self.assertFalse(output.exists())

    def test_output_inside_source_is_rejected(self):
        with self.assertRaises(ValueError):
            builder.build_release(self.root / 'release.zip', self.root)
        self.assertFalse((self.root / 'release.zip').exists())

    def test_unsafe_archive_names_are_rejected(self):
        for name in ('release\nother.zip', 'release.txt', 'archive space.zip'):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    builder.build_release(self.parent / name, self.root)
                self.assertFalse((self.parent / name).exists())

    def test_build_cli_failure_has_no_success_report(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = builder.main(['--output', str(ROOT / 'forbidden.zip')])
        self.assertEqual(code, 2)
        self.assertEqual(out.getvalue(), '')
        self.assertIn('outside', err.getvalue())


if __name__ == '__main__':
    unittest.main()
