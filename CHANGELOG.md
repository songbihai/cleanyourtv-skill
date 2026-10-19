# Changelog

## 0.2.1 — 2026-10-19 (prerelease)

- Name the repository, skill entrypoint, host metadata, and archive root `tv-vibehack-skill`.
- Add the maintainer’s optional TVRemoteX app, its icon, the first three current English screenshots from the App Store Connect workflow, and the U.S. App Store link to the README.
- Keep promotional images under separate terms and pin their exact bytes in the publication manifest. Reject changed or undeclared assets and broken local HTML image references.
- Preserve the existing device safety gates and offline plan behavior.

## 0.2.0 — 2026-10-19 (prerelease)

- Require schema 2 with a stable hardware serial and property source; schema 1 is rejected.
- Apply the same identity, user, policy, approval, journal, and recovery checks to all device writes. Restrict launcher APK installation to confirmed single-user devices.
- Reject special-file JSON inputs, numeric overflow, bidi/format controls, and unpaired surrogates; add read-only preflight arguments.
- Replace permissive packaging checks with a declared-source manifest, credential-pattern screening, and deterministic archive builder.
- Correct current host installation guidance, add capability fallbacks, refresh pinned GitHub Actions to Node 24 releases, and add reviewed Dependabot updates.
- Add regression tests and a review report. The nine-environment GitHub CI matrix passed. Hardware and independent model behavior remain unverified.

## 0.1.0 — Initial local draft (not publicly released)

- Added portable audit, plan, execution, launcher, and recovery guidance.
- Added the initial offline helper, 49 tests, CI configuration, attribution, and release/security documentation.
