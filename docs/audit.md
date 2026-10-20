# Safety, portability, and publication review

## 0.4.0 platform-extension review — 2026-10-20

- Separated Android gates from LG identity, pairing, transport and app-lifecycle gates; Android user/serial requirements and offline guard are unchanged. Existing regression cases still reject webOS in Android JSON plans.
- Reviewed aiowebostv and Dev Manager release sources, Dev Manager's SSH dependency and SlopBro. Documented plaintext/unverified-TLS and unauthenticated-server SSH behavior instead of implying secure defaults from project maturity.
- Reused maintained clients rather than adding a network executor. Restricted LG to normal single-target control and reviewed user-owned developer apps; SlopBro is explicit static research only.
- Corrected SECURITY.md's stale supported-version line. Extended the declared manifest and provenance checks without broadening the approved PNG or localization exceptions.
- Added mocked LG cases for pairing grants, target drift, permission errors, action context, developer expiry/root conflict, timeout reconciliation, and no payload-test execution. These are a manual protocol, not fabricated cross-model results.

## Historical 0.2.0 review

Review date: 2026-10-19. Reviewed the complete 0.1.0 local draft; fixes are in the 0.2.0 candidate. All reproductions used local synthetic files. No TV, ADB transport, or model-provider API was used. This is an author review with regression tests, not an independent security certification.

| Finding | Reproduction or inspection | Fix |
| --- | --- | --- |
| Target identity could collide | ADB endpoint plus fingerprint could describe a different TV of the same build. The old helper required no stable identifier. | Schema 2 binds a non-placeholder hardware serial and property source; the workflow rechecks it before every write. Unknown or duplicate IDs mean audit only. |
| Mutation gates differed by mode | Package disabling had explicit checks; launcher/settings instructions did not inherit all of them. | One entrypoint gate covers every device write, including recovery. APK install additionally requires a single-user device. |
| Input could block | A named pipe with no writer kept the old CLI waiting until its test process was terminated. | Reject special files and symlinks before opening; POSIX nonblocking open and descriptor checks mitigate file replacement races. |
| JSON overflow was accepted by loader | `1e9999` parsed as infinity. | Reject numeric overflow as well as explicit non-finite constants. |
| Text direction controls were accepted | A rationale containing a bidi override passed the old guard. | Reject Unicode control, format, and surrogate categories. |
| Publication checker missed private files | Adding a synthetic `.env` file did not fail the old checker. | Reject undeclared source files and recognizable credential patterns; archive only a declared source manifest. |
| Missing files could crash the checker | Mandatory content was read after a missing-file check instead of being handled safely. | Return actionable failures for missing/malformed source; test failure paths. |
| Host documentation was incomplete | Current official Codex discovery paths differ from the draft's example; host activation consent and device approval were conflated. | Correct host paths, keep one portable skill, and document explicit capability fallbacks and approval semantics. |
| CI pins were old runtime releases | Previous pins used older action major versions. | Verify and pin official Node 24 checkout/setup-python releases, keep read-only tokens and ephemeral GitHub-hosted jobs, and add reviewed dependency updates. |
| Uniform gates could deadlock recovery | A damaged Home can fail the very gate required for a repair. | Forward changes stop; a documented exception allows only an authorized exact journaled inverse after identity/user/policy/state checks. |
| Recovery scope was not explicit enough | Package inverse approval was optional in prose but absent from the plan presentation checklist. | Present automatic rollback scope before approval; journal every write and never overwrite intervening changes. |

## Validation boundaries

See [VALIDATION.md](../VALIDATION.md) for actual test commands and results. [Behavioral cases](evaluation.md) remain a protocol until run against a specific model/host. An adversarial or mistaken model can ignore instructions; the helper cannot authenticate a device, verify raw evidence, guarantee OEM dependency safety, or enforce consent. Hardware serial checks reduce accidental misidentification but do not defeat impersonation or make separate ADB calls atomic.

The package is suitable for source publication and a clearly scoped prerelease once the owner completes GitHub settings and hosted CI. Do not describe it as a universally safe or hardware-tested stable release. Use a trusted, unchanged local source tree when building an artifact; these tools are not a sandbox for malicious repository code or hostile filesystems.

## Primary sources checked

- [Agent Skills specification](https://agentskills.io/specification)
- [Official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Gemini CLI skills](https://geminicli.com/docs/cli/skills/)
- [GitHub Actions security guidance](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- [GitHub private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)
- [Official checkout v7.0.1 commit](https://github.com/actions/checkout/commit/3d3c42e5aac5ba805825da76410c181273ba90b1)
- [Official setup-python v7.0.0 commit](https://github.com/actions/setup-python/commit/5fda3b95a4ea91299a34e894583c3862153e4b97)
