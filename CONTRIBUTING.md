# Contributing

Use English for core instructions, documentation, code comments, CLI output, and synthetic examples. Localized prose belongs in `README.zh-CN.md` and `docs/guide.zh-CN.md`; the English README also includes a native-language navigation label. Keep both READMEs aligned in features, installation, scope, release information, and asset disclosures when any of those change. Keep tutorial steps consistent with the English skill and references. Keep the skill model-independent and references small enough to load only when needed.

For a change, explain the user-visible behavior, evidence, risks, recovery impact, and actual validation. New package evidence must identify model/firmware privately; public reports use redacted or synthetic data. A model match alone never justifies globally allowing a package. Do not add automatic disabling of stock Home, Setup Wizard, update services, or unknown dependencies.

Run from the repository root with Python 3.10+:

```text
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

Tests must cover meaningful acceptance/rejection behavior, command-injection inputs, target drift, and rollback semantics when affected. Never use a real TV or network access in automated tests. Document a plan-format change and update examples together. Keep the runtime standard-library-only unless a demonstrated need justifies a reviewed dependency.

For live evaluation, first obtain device-specific authorization, read `SKILL.md`, save a private baseline, and apply only a concrete approved plan. No live device test is required for routine documentation fixes. Do not copy real evidence into fixtures.

Submit focused pull requests. Maintainers should review safety-affecting changes and the release checklist before merging. Disclose vulnerabilities through `SECURITY.md`, not a public reproduction. Contributions are provided under the project's MIT license; retain attribution for borrowed material.
