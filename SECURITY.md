# Security policy

## Scope and supported version

Security fixes are intended for the latest 0.2.x prerelease. There is no guaranteed response time or commercial support. This candidate has offline validation only; no firmware or hardware certification is implied.

This skill is advisory text plus an offline validator. It cannot constrain a malicious or mistaken model, verify fabricated evidence, detect every OEM dependency, or replace tool permissions. Review plans and keep physical access to the TV. Package disabling can break Home, inputs, networking, or boot behavior even without root. Recovery may require vendor assistance.

## Report a vulnerability

Do not post ADB keys, pairing codes, serials, fingerprints, IP addresses, account data, screenshots, or private logs in a public issue. Check this repository's Security tab for private vulnerability reporting; use it if enabled. If unavailable, open a minimal issue requesting a private reporting channel without exploit details or personal data. Before a public tagged release, maintainers must enable private reporting or establish and document an alternative private channel. GitHub private reporting can be configured after creating the public repository; do not publish a release before verifying the channel. No unconfigured email address or reporting service is advertised here.

Include the affected release, host/tool versions, a synthetic reproduction, expected behavior, and impact through the private channel. Never test a report on a device you do not own or administer. Do not scan networks or publish a real device endpoint.

## Credentials and evidence

Keep ADB keys and private sessions outside this repository. Use the declared-source archive builder; it excludes all undeclared files, including local caches and device evidence. The repository checker also rejects unexpected source files and recognizable credential patterns. These checks are not an exhaustive secret scanner. `.gitignore` is only a secondary safeguard: inspect staged files and commit history before publishing. Device settings, package dumps, screenshots, and logs can reveal identity or usage; use minimal synthetic examples for issues. Revoke any accidentally exposed ADB trust/key, remove sensitive content from history before release, and follow the hosting provider's secret-removal procedure if already published.

Use Platform Tools from Android's official distribution. Review downloaded source and build scripts, isolate dependencies, and verify artifact identity/signatures. Do not publish upstream debug-signed APKs as production releases. Never weaken a sandbox, network policy, TLS pairing, or device permission to work around a denial.
