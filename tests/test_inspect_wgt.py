"""Synthetic WGT inspection cases: no SDK, network, extracted files or device."""

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import inspect_wgt as wgt

MANIFEST = '''<?xml version="1.0" encoding="UTF-8"?>
<widget xmlns="http://www.w3.org/ns/widgets" xmlns:tizen="http://tizen.org/ns/widgets"
 id="https://example.invalid/synthetic" version="1.2.3">
 <tizen:application id="Example123.Demo" package="Example123" required_version="5.5"/>
 <tizen:profile name="tv"/><content src="index.html"/>
 <tizen:privilege name="http://tizen.org/privilege/internet"/>
 <access origin="*"/>
</widget>'''


class WgtTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / 'synthetic.wgt'

    def make(self, manifest=MANIFEST, extras=()):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(self.path, 'w') as archive:
                archive.writestr('config.xml', manifest)
                archive.writestr('index.html', '<p>Synthetic</p>')
                for name, content in extras:
                    archive.writestr(name, content)
        return self.path

    def reject(self):
        with self.assertRaises((wgt.InspectionError, OSError)):
            wgt.inspect(self.path)

    def test_report_has_exact_identity_hash_and_no_execution(self):
        self.make()
        report = wgt.inspect(self.path)
        self.assertEqual(report['application_id'], 'Example123.Demo')
        self.assertEqual(report['package_id'], 'Example123')
        self.assertEqual(report['required_tizen_version'], '5.5')
        self.assertEqual(report['archive_sha256'], hashlib.sha256(self.path.read_bytes()).hexdigest())
        self.assertEqual(report['signature_verification'], 'not-performed')
        self.assertEqual(report['mode'], 'offline-wgt-review-only')
        self.assertEqual(set(p.name for p in self.root.iterdir()), {'synthetic.wgt'})
        self.assertFalse(any('argv' in k or k == 'approved' for k in report))

    def test_signature_filenames_are_not_signature_verification(self):
        self.make(extras=[('author-signature.xml', '<not-a-signature/>'), ('signature1.xml', 'fake')])
        report = wgt.inspect(self.path)
        self.assertEqual(len(report['signature_files']), 2)
        self.assertEqual(report['signature_verification'], 'not-performed')

    def test_remote_entry_point_is_reported_without_fetching(self):
        self.make(MANIFEST.replace('src="index.html"', 'src="https://example.invalid/app"'))
        report = wgt.inspect(self.path)
        self.assertTrue(any('Remote entry point' in x for x in report['warnings']))

    def test_metadata_duplicates_and_services_are_preserved_for_review(self):
        extra = '<tizen:metadata key="same" value="a"/><tizen:metadata key="same" value="b"/>'
        extra += '<tizen:service id="Example123.Service"><tizen:content src="service.js"/></tizen:service>'
        self.make(MANIFEST.replace('</widget>', extra + '</widget>'))
        report = wgt.inspect(self.path)
        self.assertEqual([e['value'] for e in report['metadata']], ['a', 'b'])
        self.assertTrue(any('Background service' in x for x in report['warnings']))

    def test_traversal_and_absolute_paths_are_rejected(self):
        for name in ('../outside', '/absolute', 'a/../b', 'a\\b', 'C:drive', 'a//b', './config.xml'):
            with self.subTest(name=name):
                self.make(extras=[(name, 'synthetic')]); self.reject()

    def test_duplicate_case_and_unicode_collisions_are_rejected(self):
        for names in [('config.xml',), ('CONFIG.XML',), ('caf\u00e9', 'cafe\u0301')]:
            with self.subTest(names=names):
                self.make(extras=[(name, 'synthetic') for name in names]); self.reject()

    def test_file_directory_conflict_is_rejected(self):
        self.make(extras=[('a', 'file'), ('a/b', 'other')]); self.reject()

    def test_symlink_archive_member_is_rejected(self):
        entry = zipfile.ZipInfo('link')
        entry.create_system = 3
        entry.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.make(extras=[(entry, '../outside')]); self.reject()

    def test_encrypted_entry_metadata_is_rejected(self):
        self.make()
        data = bytearray(self.path.read_bytes())
        central = data.index(b'PK\x01\x02')
        struct.pack_into('<H', data, central + 8, 1)
        self.path.write_bytes(data); self.reject()

    def test_archive_and_manifest_size_bounds(self):
        self.make()
        with patch.object(wgt, 'MAX_ARCHIVE', 100): self.reject()
        with patch.object(wgt, 'MAX_TOTAL', 100): self.reject()
        with patch.object(wgt, 'MAX_MANIFEST', 100): self.reject()
        with patch.object(wgt, 'MAX_ENTRIES', 1): self.reject()

    def test_excessive_declared_member_size_is_rejected(self):
        self.make()
        data = bytearray(self.path.read_bytes())
        central = data.index(b'PK\x01\x02')
        struct.pack_into('<L', data, central + 24, wgt.MAX_ARCHIVE + 1)
        self.path.write_bytes(data); self.reject()

    def test_zip64_or_oversize_directory_rejected_before_zipfile_parse(self):
        self.make()
        data = bytearray(self.path.read_bytes()); end = data.rfind(b'PK\x05\x06')
        struct.pack_into('<L', data, end + 12, 5 * 1024 * 1024)
        self.path.write_bytes(data)
        with patch.object(wgt.zipfile, 'ZipFile', side_effect=AssertionError('must reject first')):
            self.reject()

    def test_dtd_entities_and_alternate_encoding_are_rejected(self):
        variants = [MANIFEST.replace('<widget', '<!DOCTYPE widget [<!ENTITY x "synthetic">]><widget', 1),
                    MANIFEST.encode('utf-16'), MANIFEST.replace('UTF-8', 'ISO-8859-1')]
        for text in variants:
            with self.subTest(text=type(text).__name__): self.make(text); self.reject()

    def test_malformed_namespace_or_ambiguous_manifest_is_rejected(self):
        for text in ('<bad', MANIFEST.replace('http://www.w3.org/ns/widgets', 'urn:wrong'),
                     MANIFEST.replace('</widget>', '<content src="index.html"/></widget>'),
                     MANIFEST.replace('Example123.Demo', 'Another.Demo'),
                     MANIFEST.replace('name="tv"', 'name="mobile"')):
            with self.subTest(text=text[:35]): self.make(text); self.reject()

    def test_missing_manifest_or_entry_is_rejected(self):
        self.make(MANIFEST.replace('index.html', 'missing.html')); self.reject()
        with zipfile.ZipFile(self.path, 'w') as archive: archive.writestr('nested/config.xml', MANIFEST)
        self.reject()

    def test_direction_controls_in_identifiers_and_paths_are_rejected(self):
        self.make(MANIFEST.replace('Example123.Demo', 'Example123.\u202eDemo')); self.reject()
        self.make(extras=[('a\u202eb', 'synthetic')]); self.reject()

    def test_non_zip_and_unsupported_extension_are_rejected(self):
        self.path.write_bytes(b'not a zip'); self.reject()
        other = self.root / 'not-wgt.zip'; other.write_bytes(b'not wgt')
        with self.assertRaises(wgt.InspectionError): wgt.inspect(other)

    def test_input_symlink_is_rejected(self):
        self.make(); link = self.root / 'link.wgt'
        try: link.symlink_to(self.path)
        except OSError: self.skipTest('Host does not permit symlink creation')
        with self.assertRaises(wgt.InspectionError): wgt.inspect(link)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'POSIX special input')
    def test_fifo_input_is_rejected_without_waiting(self):
        os.mkfifo(self.path); self.reject()

    def test_malformed_deflate_is_reported_without_traceback(self):
        with zipfile.ZipFile(self.path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('config.xml', MANIFEST)
            archive.writestr('index.html', '<p>Synthetic</p>')
        data = bytearray(self.path.read_bytes())
        offset = 30 + len('config.xml')
        data[offset:offset+4] = b'\xff\xff\xff\xff'
        self.path.write_bytes(data)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err): code = wgt.main(['--wgt', str(self.path)])
        self.assertEqual(code, 2); self.assertEqual(out.getvalue(), '')
        self.assertIn('error', json.loads(err.getvalue()))

    def test_excessive_compression_ratio_is_rejected_without_expansion(self):
        with zipfile.ZipFile(self.path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('config.xml', MANIFEST)
            archive.writestr('index.html', 'x' * (2 * 1024 * 1024))
        self.reject()

    def test_cli_rejection_has_no_partial_report(self):
        self.path.write_bytes(b'bad')
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err): code = wgt.main(['--wgt', str(self.path)])
        self.assertEqual(code, 2); self.assertEqual(out.getvalue(), '')
        self.assertIn('error', json.loads(err.getvalue()))

    def test_cli_outputs_machine_readable_review(self):
        self.make(); out = io.StringIO()
        with redirect_stdout(out): self.assertEqual(wgt.main(['--wgt', str(self.path)]), 0)
        self.assertEqual(json.loads(out.getvalue())['application_id'], 'Example123.Demo')


if __name__ == '__main__':
    unittest.main()
