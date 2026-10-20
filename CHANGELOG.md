# Changelog

## 0.5.0 — 2026-10-20 (prerelease)

- Add useful Samsung Tizen app workflows: Jellyfin media libraries, Moonlight PC streaming, personal WGT builds, signing, single-target installation, testing and scoped removal/recovery. Keep Android and LG tooling separate.
- Add an original offline standard-library WGT inspector with bounded ZIP/XML parsing, exact IDs/hash/privilege reporting and no extraction, signing, execution or network access.
- Review TizenBrew dynamic modules and exclude the unmodified TizenBrew Installer from execution because of its TLS, account/listener and certificate-storage behavior. Keep experimental Samsung Root as explicit static research with exact upstream model/build evidence.
- Expand the explicitly enabled LG SlopBro module from research-only to a gated owned-device Root workflow. Research requests remain source-only; actual execution requires a concrete target/firmware plan, dependency review, isolated network, approvals and bounded attempt with honest recovery limits.
- Review Homebrew Channel v0.7.3 startup/elevation effects, including unauthenticated/default remote access, startup hooks, failsafe behavior and telemetry changes. Make pre-reboot access handling and persistence verification explicit.
- Update English/Chinese documentation, manual behavioral cases, security scope, source pins and deterministic publication manifest; preserve Android command generation and approved promotional assets.

## 0.4.0 — 2026-10-20 (prerelease)

- Add LG webOS normal control through an existing Home Assistant integration or reviewed aiowebostv client, and official non-root developer-app testing through Dev Manager / LG CLI.
- Route by actual platform, with LG pairing/access approval, private credential storage, physical target binding, transport limits, bounded single actions and honest recovery limits. Keep Android package gates and the offline command generator unchanged.
- Add an explicitly requested SlopBro / Root source-research module with pinned provenance and persistent-change/recovery assessment; it never executes a payload or roots a TV.
- Review and pin aiowebostv v0.10.0, Dev Manager v1.99.20, its ares-cli-rs v0.6.0 dependency and SlopBro. Document SSAP/SSH server-authentication limits and official developer-session app-removal effects; do not vendor code or binaries.
- Extend bilingual usage guidance, mocked behavioral cases and release provenance checks; fix the security policy's stale supported-version reference.

- Add an optional Simplified Chinese tutorial covering setup, copyable requests, reviewed execution, launcher features, and recovery.
- Provide complete English and Simplified Chinese READMEs with reciprocal native-language navigation and corresponding content; link the tutorial from Quick start.
- Allow localized prose only in the declared Chinese documents and a single navigation line in the English README, keeping the core skill English and all existing publication checks active.

## 0.3.0 — 2026-10-19 (prerelease)

- Rename the repository, skill, host metadata, and archive root to `cleanyourtv-skill`, following the upstream project rename.
- Review and pin cleanyourtv commit `7c61d3c57e561323b85d7096ee2b686685b9b499` (launcher 2.3, versionCode 4), replacing the original upstream baseline.
- Add procedures for module-card identity and consent, launcher settings and motion, theme preference restoration, and Home/Input/Settings key helpers.
- Add scoped, optional Private DNS changes and use of an existing private remote route; preserve exact settings and require recovery before network writes.
- Document new setup-wizard Wi-Fi dependencies, sideload restrictions, theme-script accessibility effects, and upstream key reuse. Preserve the existing protected-package and device-mutation gates.
- Check upstream pin consistency during publication and keep the TVRemoteX showcase and its approved assets unchanged.

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
