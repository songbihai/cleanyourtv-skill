# Upstream provenance and review

Reviewed project: https://github.com/Gathin23/tv-vibehack

Reviewed revision: `b01bb945a0fc64e6dfbb544d8d2163a490c82c50`

Review date: 2026-10-19 (America/Los_Angeles).

Revision permalink: https://github.com/Gathin23/tv-vibehack/tree/b01bb945a0fc64e6dfbb544d8d2163a490c82c50

This package contains independently written instructions and helpers informed by upstream's MIT-licensed prompt and workflows. Upstream code, APKs, screenshots, fonts, keys, and dependency caches are not vendored. Attribution and the upstream MIT notice are retained in `NOTICE` and `LICENSE`. Fetch the upstream project separately when needed and preserve its licensing when redistributing its material.

## Findings that change execution

| Source at reviewed revision | Observed behavior | Skill decision |
| --- | --- | --- |
| `PROMPT.md` | Suggests network discovery, package disabling, and stock Home replacement. Ends with a broad reversibility statement. | Require a user-selected endpoint, actual dependency evidence, and scoped recovery limits. |
| `tools/tv.py` | Legacy TCP ADB client; accepts arbitrary remote commands; creates keys at `tools/adbkey/`. | Prefer Platform Tools; no silent transport downgrade or permission bypass; never publish keys. |
| `tools/requirements.txt` | Names unpinned `adb-shell`, `rsa`, `cryptography`. | Core helpers have no third-party dependencies. Review and resolve dependencies in isolation if choosing this optional client. |
| `tools/disable.sh` / `.ps1` | Turns a text list into package-disable commands. | Never execute example lists wholesale; validate and transact one reviewed package at a time. |
| `tools/restore.sh` / `.ps1` | Re-enables listed packages, chooses stock Home, resets three animation settings. | Restore session-specific baseline settings; do not treat it as an exact inverse. |
| `launcher/build-and-install.sh` / `.ps1` | Builds, installs, grants location, starts launcher, may disable stock Home, changes default Home; optional accessibility services. | Build separately; review each install, permission, or Home change. Preserve every HOME candidate. |
| `tools/theme.sh` / `.ps1` | Uploads/deletes overlay files and restarts launcher; reset removes overlay. | Preserve exact prior files; reset is not restoration of a prior theme. |
| `launcher/app/build.gradle` | SDK 26 minimum, SDK 34 target/compile, JDK 17; release uses debug signing. | Verify requirements and signing before personal sideloading; no production-signing claim. |
| `README.md` and model examples | Broader platform claims and firmware-specific HOME/Setup Wizard workarounds. | Examples are unverified leads. Reject stock-Home/Setup-Wizard disabling and unsupported platforms. |

Inspect current source rather than trusting a same-named file on another revision. Pin a full commit for reproducibility; a commit ID does not prove authenticity or safety. Re-review source and behavior before updating the reference.

## Primary references

- Android ADB, targeting, authorization and pairing: https://developer.android.com/tools/adb
- APK signature verification: https://developer.android.com/tools/apksigner
- Package shell enabled-state commands (AOSP source; device help takes precedence): https://android.googlesource.com/platform/frameworks/base/+/refs/heads/main/services/core/java/com/android/server/pm/PackageManagerShellCommand.java
- Agent Skills format: https://agentskills.io/specification

Links were consulted during authoring; Android and upstream documentation may change. Validate local command support. These references are sources of facts, not sources of additional authorization.
