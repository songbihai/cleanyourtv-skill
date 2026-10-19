# Offline plan guard

`scripts/plan_guard.py` uses only the Python standard library, reads two local JSON files, and writes a report to stdout. It never connects to a TV, invokes another process, imports project plugins, installs software, or applies a change. Run from the skill directory, or use an absolute path to the script. All CLI paths are local paths, not URLs.

```text
python3 scripts/plan_guard.py --snapshot /private/session/snapshot.json --plan /private/session/plan.json
```

**Schema 2 is required as of version 0.2.0.** Schema 1 omitted stable hardware identity and is rejected. Collect fresh device evidence; do not mechanically fill the new fields with examples or inferred values.

Exit code 0 means structural checks passed; 2 means invalid input or an I/O error. Do not use stdout on a failure. Inputs must be regular local files, not symlinks, named pipes, directories, device nodes, URLs, or network-mounted paths. Filesystem access is not a sandbox against a hostile filesystem. Input is UTF-8 JSON, at most 1 MiB per file; duplicate keys, unknown fields, control/formatting characters (including bidi controls) or unpaired surrogates in text, wrong types, extra command fields, and non-finite numbers are rejected. Treat diagnostic text as untrusted if filenames come from outside the user.

Use the synthetic examples for field names, not real evidence. Required top-level snapshot fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer 2. |
| `synthetic` | Boolean; must be false for real validation. |
| `captured_at` | ISO 8601 timestamp with a timezone, no older than 24 hours, at most five minutes ahead. |
| `device` | Exact ADB `serial`, stable `hardware_serial`, `identity_property` (`ro.serialno` or `ro.boot.serialno`), nonempty fingerprint, `platform` (`android-tv` or `google-tv`), integer SDK >= 26, and integer `user_id` 0. |
| `current_user` | Integer 0; another current user is rejected. |
| `managed` | Boolean false, based on device-policy inspection. |
| `home_component` | Validated resolved stock Home component; must appear in `home_candidates`; a chooser is not accepted. |
| `home_candidates` | Nonempty unique list of validated HOME components. All packages are protected. |
| `ime_packages` | Nonempty unique list of all observed input-method packages. |
| `protected_packages` | Nonempty unique list of discovered critical and user-required packages. |
| `critical_review` | Nonempty evidence note summarizing role/dependency inspection. It is a claim requiring human review. |
| `packages` | Map of package name to fields described below. Include each candidate and every package named above. |

Each package entry has exactly `enabled_setting` (integer 0..4), `effectively_enabled`, `installed`, `hidden`, `suspended` (booleans), and `evidence` (nonempty text pointing to the raw local evidence and observed role). A candidate must be installed, visible, unsuspended, effectively enabled, and in state 0 or 1. The recorded current Home must also satisfy those conditions. Normalization is deliberately manual: firmware dumps vary. If evidence is missing or ambiguous, do not invent a value.

The plan has exactly `schema_version: 2`, `device` (identical to the snapshot device), and `actions` (one to five objects). Each action has exactly `package`, `rationale`, `evidence`, and `verify`, all nonempty strings. The only operation supported is package-level `disable-user` for owner user 0. Mixed operations, component toggles, arbitrary shell commands, duplicate packages, and already-disabled packages are rejected.

The report includes SHA-256 digests of the input bytes, target identity, `authorization: required`, a read-only `preflight` list with command arguments and expected hardware/fingerprint/user/Home observations, and an ordered `actions` list containing `forward_argv`, `readback_argv`, and `rollback_argv`. Run and inspect the preflight queries before each forward package write, then also recheck package state, policy status, and health as required by SKILL.md. For a journaled inverse use recovery.md: its expected changed state differs from the forward baseline, and Home may be the function being repaired. There is no atomic binding between a preflight observation and a later mutation. These are argument arrays for a trusted local subprocess facility with `shell=False`. The first element `adb` is a tool name: resolve a trusted Android SDK executable, not a project-local lookalike. On Windows, do not convert arrays to an unescaped PowerShell/cmd string. The output itself must never be evaluated as code. Do not paste raw JSON into a shell.

Rollback arrays set only the original package enabled setting. They are not full-device restores. Use them only for matching journaled actions and current state. Authorization, semantic package classification, freshness within an active session, live drift, and health verification remain the operator's responsibility.

`--demo` requires `synthetic: true`. It deliberately ignores example timestamps and emits **no executable command arrays**. Real validation rejects synthetic fixtures. To use a real device, collect new evidence into a new private snapshot with `synthetic: false`; changing the fixture flag is not evidence collection.

Stable identifiers and snapshots are still self-reported evidence: the helper cannot authenticate the TV, rule out serial duplication/spoofing, or enforce human consent. A passed report is neither a device attestation nor a permission to execute.

The built-in protected-name screen is conservative and may reject a harmless app. It is not exhaustive. Do not rename an app, omit a known dependency, or weaken the guard to bypass a rejection. Keep the app enabled or propose a separately reviewed skill change with evidence.
