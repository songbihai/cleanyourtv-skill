#!/usr/bin/env python3
"""Offline review aid. Reads JSON; prints arguments; never executes commands."""

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import stat
import unicodedata

SCHEMA_VERSION = 2
MAX_BYTES = 1_048_576
MAX_PACKAGES = 5000
PACKAGE_RE = re.compile(r'(?:android|[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)+)\Z')
SERIAL_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.:\[\]-]{0,127}\Z')
TIMESTAMP_RE = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})\Z')
ACTIVITY_RE = re.compile(r'\.?[A-Za-z_][A-Za-z0-9_.$]*\Z')
# A conservative screen, not a complete dependency map or an allowlist.
PROTECTED_RE = re.compile(
    r'launcher|setup|wraith|systemui|settings|provider|permission|packageinstaller|'
    r'input|keyboard|bluetooth|remote|network|wifi|wlan|ethernet|connectivity|'
    r'widevine|drm|keychain|keystore|certinstaller|update|updater|'
    r'accessibility|devicepolicy|devicemanagement|tuner|tvservice|tvinput|'
    r'cast|miracast|assistant|katniss|vending|google.*services|'
    r'netflix|youtube|primevideo|disney|hulu|'
    r'(?:^|[._])(?:ota|fota|gms|gsf|vpn|ime)(?:[._]|$)', re.IGNORECASE,
)
SNAPSHOT_KEYS = {
    'schema_version', 'synthetic', 'captured_at', 'device', 'current_user', 'managed',
    'home_component', 'home_candidates', 'ime_packages', 'protected_packages',
    'critical_review', 'packages',
}
DEVICE_KEYS = {'serial', 'hardware_serial', 'identity_property', 'fingerprint', 'platform', 'android_sdk', 'user_id'}
PACKAGE_KEYS = {'enabled_setting', 'effectively_enabled', 'installed', 'hidden', 'suspended', 'evidence'}
ACTION_KEYS = {'package', 'rationale', 'evidence', 'verify'}


class PlanError(ValueError):
    """Invalid or unsupported review input."""


def require(condition, message):
    if not condition:
        raise PlanError(message)


def exact_keys(value, expected, label):
    require(type(value) is dict, f'{label} must be an object')
    require(set(value) == expected, f'{label} has missing or unknown fields')


def integer(value, low, high, label):
    require(type(value) is int and low <= value <= high, f'{label} must be an integer in {low}..{high}')


def text_field(value, label, maximum=4096):
    require(type(value) is str and 0 < len(value) <= maximum and bool(value.strip()), f'{label} must be nonempty text')
    require(not any(unicodedata.category(c) in ('Cc', 'Cf', 'Cs') for c in value), f'{label} contains control, formatting, or surrogate characters')
    return value


def package_name(value):
    text_field(value, 'package name', 255)
    require(PACKAGE_RE.fullmatch(value) is not None, 'invalid package identifier')
    return value


def component(value):
    text_field(value, 'component', 512)
    parts = value.split('/')
    require(len(parts) == 2, 'component must be package/activity')
    package_name(parts[0])
    require(ACTIVITY_RE.fullmatch(parts[1]) is not None, 'invalid component activity')
    return parts[0]


def unique_list(value, label, validator):
    require(type(value) is list and 0 < len(value) <= MAX_PACKAGES, f'{label} must be a nonempty bounded list')
    result = set()
    for item in value:
        validator(item)
        require(item not in result, f'{label} contains duplicates')
        result.add(item)
    return result


def reject_constant(value):
    raise PlanError('non-finite JSON numbers are not accepted')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON object key')
        result[key] = value
    return result


def finite_float(value):
    number = float(value)
    require(math.isfinite(number), 'non-finite JSON numbers are not accepted')
    return number


def load_json(path):
    # Reject special files before opening. O_NONBLOCK and fstat also cover a
    # POSIX race replacing an inspected file with a FIFO. This is not a sandbox
    # against a hostile filesystem or network-mounted paths.
    source = Path(path)
    require(stat.S_ISREG(source.lstat().st_mode), 'input must be a regular local file, not a symlink or special file')
    flags = os.O_RDONLY | getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(source, flags)
    try:
        require(stat.S_ISREG(os.fstat(descriptor).st_mode), 'input must be a regular local file')
        with os.fdopen(descriptor, 'rb') as stream:
            descriptor = None
            raw = stream.read(MAX_BYTES + 1)
    finally:
        if descriptor is not None:
            os.close(descriptor)
    require(len(raw) <= MAX_BYTES, 'input exceeds the 1 MiB limit')
    try:
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_object,
                          parse_constant=reject_constant, parse_float=finite_float)
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        if isinstance(exc, PlanError):
            raise
        raise PlanError('input must be valid UTF-8 JSON with bounded nesting') from exc
    return data, hashlib.sha256(raw).hexdigest()


def validate_device(device):
    exact_keys(device, DEVICE_KEYS, 'device')
    text_field(device['serial'], 'serial', 128)
    require(SERIAL_RE.fullmatch(device['serial']) is not None, 'invalid target serial')
    hardware = text_field(device['hardware_serial'], 'hardware_serial', 128)
    require(SERIAL_RE.fullmatch(hardware) is not None, 'invalid hardware serial')
    require(hardware.lower() not in ('unknown', 'null', 'none', 'unset', 'default', 'serial', 'serialno')
            and bool(hardware.strip('0')), 'hardware identity is unavailable or a placeholder')
    require(device['identity_property'] in ('ro.serialno', 'ro.boot.serialno'), 'unsupported identity property')
    text_field(device['fingerprint'], 'fingerprint', 512)
    require(device['platform'] in ('android-tv', 'google-tv'), 'unsupported platform')
    integer(device['android_sdk'], 26, 100, 'android_sdk')
    integer(device['user_id'], 0, 0, 'user_id')


def validate_snapshot(snapshot, demo=False, now=None):
    exact_keys(snapshot, SNAPSHOT_KEYS, 'snapshot')
    integer(snapshot['schema_version'], SCHEMA_VERSION, SCHEMA_VERSION, 'snapshot schema_version')
    require(type(snapshot['synthetic']) is bool, 'synthetic must be a boolean')
    require(snapshot['synthetic'] == demo, 'demo requires synthetic evidence; real validation rejects synthetic evidence')
    text_field(snapshot['captured_at'], 'captured_at', 64)
    require(TIMESTAMP_RE.fullmatch(snapshot['captured_at']) is not None, 'captured_at must use a full ISO 8601 timestamp with timezone')
    try:
        captured = datetime.fromisoformat(snapshot['captured_at'].replace('Z', '+00:00'))
    except ValueError as exc:
        raise PlanError('invalid captured_at timestamp') from exc
    require(captured.tzinfo is not None and captured.utcoffset() is not None, 'captured_at needs a timezone')
    if not demo:
        current = now or datetime.now(timezone.utc)
        require(current - timedelta(hours=24) <= captured <= current + timedelta(minutes=5), 'snapshot is stale or in the future')
    validate_device(snapshot['device'])
    integer(snapshot['current_user'], 0, 0, 'current_user')
    require(type(snapshot['managed']) is bool and not snapshot['managed'], 'managed sessions are unsupported')
    text_field(snapshot['critical_review'], 'critical_review')
    homes = unique_list(snapshot['home_candidates'], 'home_candidates', component)
    home_package = component(snapshot['home_component'])
    require(snapshot['home_component'] in homes, 'resolved Home must be one of the HOME candidates')
    require(home_package != 'android', 'a chooser is not a resolved stock Home')
    imes = unique_list(snapshot['ime_packages'], 'ime_packages', package_name)
    protected = unique_list(snapshot['protected_packages'], 'protected_packages', package_name)
    protected.update(imes)
    protected.update(component(item) for item in homes)
    packages = snapshot['packages']
    require(type(packages) is dict and 0 < len(packages) <= MAX_PACKAGES, 'packages must be a nonempty bounded object')
    for name, state in packages.items():
        package_name(name)
        exact_keys(state, PACKAGE_KEYS, f'package {name}')
        integer(state['enabled_setting'], 0, 4, 'enabled_setting')
        for key in ('effectively_enabled', 'installed', 'hidden', 'suspended'):
            require(type(state[key]) is bool, f'{key} must be a boolean')
        text_field(state['evidence'], 'package evidence')
    require(protected <= set(packages), 'protected, HOME, or IME package is missing from the inventory')
    require(is_active(packages[home_package]), 'recorded stock Home is not active')
    return protected


def is_active(state):
    return (state['enabled_setting'] in (0, 1) and state['effectively_enabled']
            and state['installed'] and not state['hidden'] and not state['suspended'])


def name_is_protected(name):
    return (name == 'android' or name.startswith(('com.android.', 'com.google.', 'com.amazon.'))
            or PROTECTED_RE.search(name) is not None)


def build_report(snapshot, plan, demo=False, now=None):
    protected = validate_snapshot(snapshot, demo=demo, now=now)
    exact_keys(plan, {'schema_version', 'device', 'actions'}, 'plan')
    integer(plan['schema_version'], SCHEMA_VERSION, SCHEMA_VERSION, 'plan schema_version')
    validate_device(plan['device'])
    require(plan['device'] == snapshot['device'], 'plan target differs from snapshot target')
    actions = plan['actions']
    require(type(actions) is list and 1 <= len(actions) <= 5, 'a plan needs one to five actions')
    report = {
        'schema_version': SCHEMA_VERSION,
        'mode': 'synthetic-demo-no-execution' if demo else 'review-only-no-execution',
        'authorization': 'not-applicable' if demo else 'required',
        'device': dict(snapshot['device']),
        'warning': 'Synthetic evidence. No executable commands emitted.' if demo else
                   'Structural review only. Verify evidence, authorization, live identity/state, and health before each change.',
        'actions': [],
    }
    if not demo:
        prefix = ['adb', '-s', snapshot['device']['serial'], 'shell']
        report['preflight'] = [
            {'check': 'hardware_serial', 'argv': prefix + ['getprop', snapshot['device']['identity_property']],
             'expected': snapshot['device']['hardware_serial']},
            {'check': 'fingerprint', 'argv': prefix + ['getprop', 'ro.build.fingerprint'],
             'expected': snapshot['device']['fingerprint']},
            {'check': 'current_user', 'argv': prefix + ['am', 'get-current-user'], 'expected': '0'},
            {'check': 'home_component', 'argv': prefix + ['cmd', 'package', 'resolve-activity', '--brief', '--user', '0',
             '-a', 'android.intent.action.MAIN', '-c', 'android.intent.category.HOME'],
             'expected': snapshot['home_component']},
        ]
    seen = set()
    for action in actions:
        exact_keys(action, ACTION_KEYS, 'action')
        name = package_name(action['package'])
        require(name not in seen, 'duplicate package action')
        seen.add(name)
        require(name not in protected and not name_is_protected(name), f'protected package rejected: {name}')
        for key in ('rationale', 'evidence', 'verify'):
            text_field(action[key], key)
        require(name in snapshot['packages'], f'candidate is absent from inventory: {name}')
        state = snapshot['packages'][name]
        require(is_active(state), f'candidate is not installed, visible, unsuspended, and active: {name}')
        item = dict(action)
        item['original_enabled_setting'] = state['enabled_setting']
        item['expected_enabled_setting_after_disable'] = 3
        if not demo:
            prefix = ['adb', '-s', snapshot['device']['serial'], 'shell']
            item['forward_argv'] = prefix + ['pm', 'disable-user', '--user', '0', name]
            item['readback_argv'] = prefix + ['dumpsys', 'package', name]
            inverse = 'default-state' if state['enabled_setting'] == 0 else 'enable'
            item['rollback_argv'] = prefix + ['pm', inverse, '--user', '0', name]
        report['actions'].append(item)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', required=True, help='Local snapshot JSON path')
    parser.add_argument('--plan', required=True, help='Local plan JSON path')
    parser.add_argument('--demo', action='store_true', help='Synthetic fixtures only; emit no commands')
    args = parser.parse_args(argv)
    try:
        snapshot, snapshot_digest = load_json(args.snapshot)
        plan, plan_digest = load_json(args.plan)
        report = build_report(snapshot, plan, demo=args.demo)
        report['input_sha256'] = {'snapshot': snapshot_digest, 'plan': plan_digest}
        print(json.dumps(report, indent=2, ensure_ascii=True))
        return 0
    except (PlanError, OSError, RecursionError, OverflowError) as exc:
        # Escape diagnostic control characters supplied by an external path.
        print('Validation failed: ' + json.dumps(str(exc), ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
