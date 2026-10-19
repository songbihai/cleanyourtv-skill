# Release checklist

This is a publication checklist. It does not imply the checks below have already happened. See VALIDATION.md for actual results.

## Local preparation

- Run the documented tests, repository checker, and demo on a clean checkout. Ensure no network or device is used by the helper or tests.
- Review the complete diff for targeting, unknown outcomes, protected roles, exact inverses, prompt injection, and private data. Check staged files **and history**; ignore rules do not remove tracked secrets.
- Verify every relative reference resolves and the skill loads in at least one intended host. Use the behavioral protocol before claiming a model/host pairing has been evaluated.
- Retain the upstream notice and full reviewed commit. Re-review any upstream update before changing that pin.
- Update CHANGELOG.md, skill metadata version, and VALIDATION.md together. Publish the reviewed candidate as 0.2.0; do not label it universally safe or hardware-certified.

## GitHub configuration (repository owner)

Creating/uploading the review repository and publishing a tagged release are separate steps. A local package cannot enable repository settings, prove hosted CI, or invent a maintainer identity.

- Create the public repository under the intended owner after reviewing the local package. Do not commit device sessions or the upstream working tree.
- Enable private vulnerability reporting and confirm that SECURITY.md matches the actual channel. If unavailable, establish and document a private channel before publishing a tagged release.
- Enable branch protection/rules requiring the Validate workflow and pull request review where available. Grant collaborators minimum permissions. The workflow needs only read access to repository contents.
- Run the configured Linux/macOS/Windows Python matrix successfully on GitHub. Those results are pending until the workflow actually runs.
- Verify action commit pins against their official repositories before release; review updates rather than replacing pins with floating tags. Use GitHub-hosted runners for public pull requests, not a personal machine with credentials or LAN access. Keep fork workflow approval restrictions enabled. No publishing job, persistent cache, or repository secret is needed for this CI. Dependabot proposes action updates for human review; it does not auto-merge them.
- Create an annotated `v0.2.0` tag on the reviewed commit and a release with actual scope, validation, limitations, and links to source. Use a prerelease label while model/host behavior is still under evaluation.
- Prefer the declared-source archive builder (`scripts/build_release.py`) for a custom artifact; it rejects unexpected files and writes a SHA-256 sidecar. Inspect `git ls-files` and history before using GitHub source archives, because source archives include every tracked file, even when ignored. Do not bundle a dirty working directory, ADB keys, APKs, or cached dependencies.

The user should supply the GitHub owner/name and authorize publication when ready. This package does not create a remote repository, push code, or publish a release by itself.

## Local artifact build

After the checks pass, use an output directory outside this repository:

```text
python3 scripts/build_release.py --output /local/output/tv-vibehack-safe-0.2.0.zip
```

The builder packages only its declared source manifest in sorted order, uses fixed ZIP metadata and uncompressed entries for reproducibility across supported Python implementations, and refuses existing archive/checksum files. It does not read `.git` history, publish, sign, or prove source authenticity. Confirm the archive checksum after transfer. Do not upload a zip of an arbitrary working folder.

## After publication

Triage safety reports promptly, withdraw an affected release if necessary, and document known limitations. Re-evaluate safety-affecting changes with synthetic cases. Device reports are evidence for a specific firmware only; do not turn them into a global safe-package list. No external telemetry is collected by the offline helper.
