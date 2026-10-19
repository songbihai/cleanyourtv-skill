#!/usr/bin/env python3
"""Build an offline, declared-source ZIP. Does not sign, publish, or use ADB."""

import argparse
import hashlib
import io
import json
import re
from pathlib import Path
import sys
import zipfile

from check_repository import DISTRIBUTION_FILES, ROOT, check


def archive_bytes(root=ROOT):
    root = Path(root).resolve()
    failures = check(root)
    if failures:
        raise ValueError('Source validation failed: ' + '; '.join(failures))
    result = io.BytesIO()
    with zipfile.ZipFile(result, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name in DISTRIBUTION_FILES:
            # No filesystem modes, creation times, or local paths enter the ZIP.
            info = zipfile.ZipInfo('tv-vibehack-skill/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, (root / name).read_bytes())
    return result.getvalue()


def build_release(output, root=ROOT):
    root = Path(root).resolve()
    output = Path(output).absolute()
    # Output must be outside the source tree, including through a parent symlink.
    if output.resolve().is_relative_to(root):
        raise ValueError('Archive output must be outside the source repository')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,123}\.zip', output.name):
        raise ValueError('Archive filename must be a simple ASCII name ending in .zip')
    checksum = output.with_name(output.name + '.sha256')
    if output.exists() or output.is_symlink() or checksum.exists() or checksum.is_symlink():
        raise ValueError('Refusing to overwrite an existing archive or checksum')
    data = archive_bytes(root)
    digest = hashlib.sha256(data).hexdigest()
    # Exclusive creation also fails closed if another writer races the check.
    # On an I/O failure a partial artifact can remain: never publish it.
    with checksum.open('x', encoding='ascii', newline='\n') as stream:
        with output.open('xb') as archive:
            archive.write(data)
        stream.write(digest + '  ' + output.name + '\n')
    return digest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='New ZIP path outside the source repository')
    args = parser.parse_args(argv)
    try:
        digest = build_release(args.output)
        print(json.dumps({'archive': str(Path(args.output).absolute()), 'sha256': digest}, ensure_ascii=True))
        return 0
    except (OSError, ValueError) as exc:
        print('Build failed: ' + json.dumps(str(exc), ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
