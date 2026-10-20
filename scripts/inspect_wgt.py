#!/usr/bin/env python3
"""Inspect a bounded local WGT as data; never extract, install, sign or execute it."""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import struct
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
import zlib

MAX_ARCHIVE = 128 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_ENTRIES = 6000
MAX_MANIFEST = 256 * 1024
WIDGET = '{http://www.w3.org/ns/widgets}'
TIZEN = '{http://tizen.org/ns/widgets}'


class InspectionError(ValueError):
    """Input cannot be inspected within the supported format and bounds."""


def require(condition, message):
    if not condition:
        raise InspectionError(message)


def safe_text(value):
    require(isinstance(value, str) and len(value) <= 8192, 'oversized manifest text')
    require(not any(unicodedata.category(c) in ('Cc', 'Cf', 'Cs') for c in value),
            'control or direction characters in metadata')
    return value


def member_name(value):
    safe_text(value)
    require(value and len(value) <= 512 and '\\' not in value and ':' not in value,
            'unsafe archive member name')
    parts = value.rstrip('/').split('/')
    require(all(p not in ('', '.', '..') for p in parts), 'unsafe archive member path')
    return value


def local_bytes(path):
    source = Path(path)
    require(source.suffix.lower() == '.wgt', 'expected a local .wgt file')
    require(not source.is_symlink(), 'symlink input is not supported')
    flags = os.O_RDONLY | getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(source, flags)
    try:
        require(stat.S_ISREG(os.fstat(descriptor).st_mode), 'input must be a regular local file')
        require(os.fstat(descriptor).st_size <= MAX_ARCHIVE, 'archive exceeds size limit')
        with os.fdopen(descriptor, 'rb') as stream:
            descriptor = None
            data = stream.read(MAX_ARCHIVE + 1)
        require(len(data) <= MAX_ARCHIVE, 'archive exceeds size limit')
        return data
    finally:
        if descriptor is not None:
            os.close(descriptor)


def inspect(path):
    data = local_bytes(path)
    # Bound the central directory before ZipFile allocates one object per member.
    # This inspector deliberately excludes ZIP64 and split archives.
    end = data.rfind(b'PK\x05\x06', max(0, len(data) - 65557))
    require(end >= 0 and end + 22 <= len(data), 'missing ZIP end record')
    record = struct.unpack_from('<4s4H2LH', data, end)
    _, disk, directory_disk, disk_count, count, directory_size, offset, comment_size = record
    require(disk == directory_disk == 0 and disk_count == count and count <= MAX_ENTRIES,
            'split, ZIP64 or excessive-entry archive is not supported')
    require(directory_size <= 4 * 1024 * 1024 and offset <= end and
            end + 22 + comment_size == len(data), 'invalid or oversized ZIP directory')
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            require(0 < len(entries) == count <= MAX_ENTRIES, 'archive entry count differs or exceeds limit')
            names, total, files = set(), 0, set()
            for item in entries:
                name = member_name(item.orig_filename)
                require(name == item.filename, 'ambiguous archive member name')
                folded = unicodedata.normalize('NFC', name.rstrip('/')).casefold()
                require(folded not in names, 'duplicate or colliding archive members')
                names.add(folded)
                mode = stat.S_IFMT(item.external_attr >> 16)
                require(mode in (0, stat.S_IFREG, stat.S_IFDIR), 'non-regular archive member')
                require(not item.flag_bits & 1, 'encrypted archive is not supported')
                require(item.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED),
                        'unsupported archive compression')
                require(item.file_size <= MAX_ARCHIVE, 'archive member exceeds size limit')
                total += item.file_size
                require(total <= MAX_TOTAL, 'expanded archive exceeds size limit')
                require(item.file_size <= max(1_048_576, item.compress_size * 1000),
                        'excessive archive compression ratio')
                if not item.is_dir():
                    files.add(name)
            for name in files:
                parts = name.split('/')
                require(not any('/'.join(parts[:i]) in files for i in range(1, len(parts))),
                        'archive file conflicts with a directory')
            require('config.xml' in files, 'one root config.xml is required')
            info = archive.getinfo('config.xml')
            require(info.file_size <= MAX_MANIFEST, 'manifest exceeds size limit')
            with archive.open(info) as stream:
                manifest = stream.read(MAX_MANIFEST + 1)
            require(len(manifest) <= MAX_MANIFEST, 'manifest exceeds size limit')
        # Strict UTF-8 prevents alternate-encoding declarations hiding a DTD.
        text = manifest.decode('utf-8-sig')
        require('\x00' not in text and '<!DOCTYPE' not in text.upper() and '<!ENTITY' not in text.upper(),
                'DTD and entity declarations are not supported')
        declaration = re.search(r'<\?xml\b[^?]*\bencoding\s*=\s*[\'"]([^\'"]+)', text, re.IGNORECASE)
        require(not declaration or declaration.group(1).lower() in ('utf-8', 'utf8'),
                'manifest must declare UTF-8')
        root = ET.fromstring(text)
        require(root.tag == WIDGET + 'widget', 'expected a widget manifest namespace')
        require(sum(1 for _ in root.iter()) <= 3000, 'manifest element count exceeds limit')
        for element in root.iter():
            for value in element.attrib.values():
                safe_text(value)
        apps = root.findall(TIZEN + 'application')
        contents = root.findall(WIDGET + 'content')
        require(len(apps) == 1 and len(contents) == 1, 'one application and one content entry required')
        app = apps[0]
        app_id, package_id = app.get('id', ''), app.get('package', '')
        require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{1,127}', app_id) is not None,
                'invalid application ID')
        require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{1,63}', package_id) is not None,
                'invalid package ID')
        require(app_id.startswith(package_id + '.'), 'application and package IDs disagree')
        profiles = [e.get('name', '') for e in root.findall(TIZEN + 'profile')]
        require(all(p in ('tv', 'tv-samsung') for p in profiles), 'non-TV profile')
        entry = contents[0].get('src', '')
        require(entry, 'missing entry point')
        remote = bool(re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', entry) or entry.startswith('//'))
        if not remote:
            normalized = entry[2:] if entry.startswith('./') else entry
            member_name(normalized)
            require(normalized in files, 'local entry point is missing from archive')
        def attributes(tag):
            return [dict(e.attrib) for e in root.findall(tag)]
        signatures = sorted(n for n in files if n == 'author-signature.xml' or
                            re.fullmatch(r'signature[0-9]+\.xml', n))
        warnings = ['Review data only: no install approval, code audit, signature verification or firmware compatibility decision.']
        if not signatures:
            warnings.append('No conventional signature filenames found; signing must be reviewed separately.')
        if remote:
            warnings.append('Remote entry point: delivered executable content can change after package review.')
        if root.findall(TIZEN + 'service'):
            warnings.append('Background service declarations require separate source and privilege review.')
        if any(e.get('origin') == '*' for e in root.findall(WIDGET + 'access')):
            warnings.append('Wildcard network access is declared.')
        if not profiles:
            warnings.append('No explicit TV profile; confirm target support with Samsung tooling.')
        return {
            'mode': 'offline-wgt-review-only', 'archive_sha256': hashlib.sha256(data).hexdigest(),
            'archive_bytes': len(data), 'entry_count': len(entries), 'declared_expanded_bytes': total,
            'widget_id': root.get('id', ''), 'version': root.get('version', ''),
            'application_id': app_id, 'package_id': package_id,
            'required_tizen_version': app.get('required_version', ''), 'profiles': profiles,
            'entry_point': entry, 'privileges': attributes(TIZEN + 'privilege'),
            'network_access': attributes(WIDGET + 'access'), 'services': attributes(TIZEN + 'service'),
            'metadata': attributes(TIZEN + 'metadata'), 'settings': attributes(TIZEN + 'setting'),
            'signature_files': signatures, 'signature_verification': 'not-performed',
            'payload_code_review': 'not-performed', 'warnings': warnings,
        }
    except (zipfile.BadZipFile, ET.ParseError, UnicodeError, RuntimeError, NotImplementedError, RecursionError, EOFError, zlib.error) as exc:
        raise InspectionError('invalid or unsupported WGT archive/manifest') from exc


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wgt', required=True, help='local regular .wgt file; no URL or extraction')
    args = parser.parse_args(argv)
    try:
        report = inspect(args.wgt)
    except (OSError, ValueError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
