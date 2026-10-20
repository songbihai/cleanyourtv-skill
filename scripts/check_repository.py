#!/usr/bin/env python3
"""Validate declared source files. Not an exhaustive secret scan or a sandbox."""

import ast
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_URL = 'https://github.com/Gathin23/cleanyourtv'
UPSTREAM_REVISION = '7c61d3c57e561323b85d7096ee2b686685b9b499'
# Only explicitly declared localized documentation may contain non-English prose.
LOCALIZED_DOCUMENTS = frozenset({'README.zh-CN.md', 'docs/guide.zh-CN.md'})
# The English README permits only this standalone native-language navigation line.
ENGLISH_LANGUAGE_NAVIGATION = '**English** | [\u7b80\u4f53\u4e2d\u6587](README.zh-CN.md)'
# Only these reviewed promotional bytes may bypass UTF-8 source checks.
PINNED_ASSETS = {
    'assets/tvremotex/logo.png': 'edbcc77cc85d68ce09781c0b863321b96409ebf39726513afc14ad041541ecee',
    'assets/tvremotex/01-brands-en-US.png': '05284cef80431bc1c897bcdd4c3577ad11811b5f901696a18e8a105530a89a41',
    'assets/tvremotex/02-power-and-apps-en-US.png': 'fb870e5c3b43cf52bc336f83fec2cb14943c5effb67715f5b13c7c595b4789ef',
    'assets/tvremotex/03-keyboard-and-touchpad-en-US.png': '2c55b7aa56b44d8e2e990f7048ebe61970ea9c8638ff22efb81f534cae6bad6f',
}
# The release builder uses this exact manifest, never an arbitrary directory zip.
DISTRIBUTION_FILES = tuple(sorted((
    'SKILL.md', 'README.md', 'README.zh-CN.md', 'LICENSE', 'NOTICE', 'SECURITY.md', 'CONTRIBUTING.md',
    'CHANGELOG.md', 'VALIDATION.md', 'VERSION', '.editorconfig', '.gitignore', '.gitattributes',
    'agents/openai.yaml', '.github/workflows/validate.yml', '.github/dependabot.yml',
    '.github/ISSUE_TEMPLATE/bug_report.md', '.github/pull_request_template.md',
    'references/device-workflow.md', 'references/launcher.md', 'references/recovery.md',
    'references/plan-format.md', 'references/upstream-review.md', 'references/network-extras.md', 'docs/evaluation.md',
    'docs/release.md', 'docs/compatibility.md', 'docs/guide.zh-CN.md', 'docs/audit.md', 'scripts/plan_guard.py',
    'scripts/check_repository.py', 'scripts/build_release.py', 'tests/test_plan_guard.py',
    'tests/test_release_tools.py', 'examples/snapshot.synthetic.json', 'examples/plan.synthetic.json',
    'assets/tvremotex/NOTICE.md',
) + tuple(PINNED_ASSETS)))
IGNORED_LOCAL_DIRS = {'.git', '__pycache__', '.venv', 'venv', '.pytest_cache'}
MAX_FILE_BYTES = 1_048_576
MAX_ASSET_BYTES = 2_097_152
SECRET_RE = re.compile(
    r'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----|'
    r'\bgh[pousr]_[A-Za-z0-9]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}\b'
)


def _bad_constant(value):
    raise ValueError('non-finite JSON constant')


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON object key')
        result[key] = value
    return result


class _HTMLReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if (tag, name) in (('img', 'src'), ('a', 'href')) and value:
                self.targets.append(value)


def check(root=ROOT):
    root = Path(root).resolve()
    if not root.is_dir():
        return ['Source root is missing or not a directory']
    errors, content_by_name, readable = [], {}, set()
    allowed = set(DISTRIBUTION_FILES)
    directories = {str(parent).replace(os.sep, '/') for name in allowed
                   for parent in Path(name).parents if str(parent) != '.'}
    for directory, dirs, files in os.walk(root, followlinks=False):
        parent = Path(directory)
        for name in list(dirs):
            path = parent / name
            rel = path.relative_to(root).as_posix()
            if name in IGNORED_LOCAL_DIRS:
                dirs.remove(name)
            elif path.is_symlink():
                errors.append(f'Unexpected directory symlink: {rel}')
                dirs.remove(name)
            elif rel not in directories:
                errors.append(f'Unexpected source directory: {rel}')
                dirs.remove(name)
        for name in files:
            path = parent / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                errors.append(f'Unexpected file symlink: {rel}')
                continue
            if rel not in allowed:
                errors.append(f'Unexpected source file: {rel}')
                continue
            try:
                bound = MAX_ASSET_BYTES if rel in PINNED_ASSETS else MAX_FILE_BYTES
                if not path.is_file() or path.stat().st_size > bound:
                    errors.append(f'Not a bounded regular source file: {rel}')
                    continue
                if rel in PINNED_ASSETS:
                    data = path.read_bytes()
                    if hashlib.sha256(data).hexdigest() != PINNED_ASSETS[rel]:
                        errors.append(f'Reviewed promotional asset differs: {rel}')
                        continue
                    readable.add(rel)
                    continue
                content = path.read_text(encoding='utf-8')
                content_by_name[rel] = content
                readable.add(rel)
                if SECRET_RE.search(content):
                    # Do not print matching bytes or private data.
                    errors.append(f'Recognizable credential pattern in: {rel}')
                language_content = content
                if rel == 'README.md':
                    language_content = content.replace('\n' + ENGLISH_LANGUAGE_NAVIGATION + '\n', '\n', 1)
                if rel not in LOCALIZED_DOCUMENTS and re.search(r'[\u3400-\u9fff]', language_content):
                    errors.append(f'Unexpected CJK prose in English-only source: {rel}')
                if path.suffix == '.json':
                    json.loads(content, object_pairs_hook=_unique_object, parse_constant=_bad_constant)
                if path.suffix == '.py':
                    ast.parse(content)
                if path.suffix == '.md':
                    html = _HTMLReferences()
                    html.feed(content)
                    targets = re.findall(r'\[[^\]]*\]\(([^)]+)\)', content) + html.targets
                    for target in targets:
                        if target.startswith(('https://', 'http://', '#')):
                            continue
                        dest = (path.parent / target.split('#')[0]).resolve()
                        if not dest.is_relative_to(root) or not dest.is_file():
                            errors.append(f'Broken or external local reference in: {rel}')
            except (OSError, UnicodeError, ValueError, RecursionError, SyntaxError):
                errors.append(f'Cannot parse source file: {rel}')
    for missing in sorted(allowed - readable):
        errors.append(f'Missing readable declared file: {missing}')
    skill = content_by_name.get('SKILL.md', '')
    parts = skill.split('---', 2)
    if not skill.startswith('---\n') or len(parts) != 3:
        errors.append('SKILL.md needs complete YAML frontmatter')
    else:
        front = parts[1]
        if not re.search(r'^name: cleanyourtv-skill$', front, re.MULTILINE):
            errors.append('Invalid skill name')
        if not re.search(r'^description: .+', front, re.MULTILINE):
            errors.append('Skill description is missing')
        if (f'  upstream: "{UPSTREAM_URL}"' not in front or
                f'  upstream_revision: "{UPSTREAM_REVISION}"' not in front):
            errors.append('Skill upstream identity differs from the reviewed source pin')
        version = content_by_name.get('VERSION', '').strip()
        if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', version):
            errors.append('VERSION must contain a semantic release version')
        elif f'  version: "{version}"' not in front or f'## {version} ' not in content_by_name.get('CHANGELOG.md', ''):
            errors.append('Version differs between VERSION, skill metadata, and changelog')
    for name in ('NOTICE', 'references/upstream-review.md'):
        if UPSTREAM_REVISION not in content_by_name.get(name, '') or UPSTREAM_URL not in content_by_name.get(name, ''):
            errors.append(f'Upstream provenance differs from the reviewed source pin: {name}')
    if len(skill.splitlines()) > 250:
        errors.append('Entrypoint exceeds the project context budget of 250 lines')
    source = content_by_name.get('scripts/plan_guard.py')
    if source:
        try:
            tree = ast.parse(source)
            permitted = {'argparse', 'datetime', 'hashlib', 'json', 'math', 'os', 'pathlib', 're', 'sys', 'stat', 'unicodedata'}
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [item.name.split('.')[0] for item in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [(node.module or '').split('.')[0]]
                else:
                    names = []
                if any(name not in permitted for name in names):
                    errors.append('Plan guard added an unreviewed runtime dependency')
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in ('eval', 'exec', '__import__'):
                        errors.append('Plan guard must not evaluate dynamic code')
                    if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                        if node.func.value.id == 'os' and node.func.attr not in ('open', 'fstat', 'fdopen', 'close'):
                            errors.append('Plan guard added an unreviewed OS operation')
        except SyntaxError:
            errors.append('Plan guard is not valid Python')
    for name in ('examples/snapshot.synthetic.json', 'examples/plan.synthetic.json'):
        try:
            example = json.loads(content_by_name.get(name, '{}'))
            if example.get('schema_version') != 2:
                errors.append(f'Example schema is not current: {name}')
            if not example.get('device', {}).get('serial', '').startswith('SYNTHETIC-'):
                errors.append(f'Example target is not clearly synthetic: {name}')
            if name.endswith('snapshot.synthetic.json') and example.get('synthetic') is not True:
                errors.append('Snapshot example must remain synthetic')
        except (AttributeError, ValueError, TypeError):
            errors.append(f'Invalid example: {name}')
    return sorted(set(errors))


if __name__ == '__main__':
    failures = check()
    if failures:
        for failure in failures:
            # Filenames may come from untrusted local files; escape controls.
            print(json.dumps(failure, ensure_ascii=True), file=sys.stderr)
        sys.exit(1)
    print('Repository checks passed: declared source, references, version, credential patterns, and helper constraints.')
