# Validation record

Date: 2026-10-20 (America/Los_Angeles).

Package: CleanYourTV Skill 0.4.0 public prerelease.

## 0.4.0 LG webOS extension

- Reviewed aiowebostv v0.10.0 (`36fbc433147dd17032f63e40ada57c439625e6ed`), webOS Dev Manager v1.99.20 (`5445d114d6167df38624edfea8b05b9f652657d7`), its ares-cli-rs v0.6.0 dependency (`ef1247bc5b2fc4cdc625b663eb7721e8242d80b6`) and SlopBro (`21023d56ca424607bb03d2939609cc658c655fc7`) as source, alongside Home Assistant and LG official documentation. See [source review](references/lg-source-review.md) for inspected files and boundaries.
- Added platform routing, LG normal control and official developer-app procedures. Documented SSAP's plaintext/unverified-TLS behavior, SSH server-trust limits, physical confirmation, pairing/access effects, bounded single actions, developer expiry and existing-root conflicts. Added explicitly requested SlopBro static research; no payload or root execution is supported.
- Kept `scripts/plan_guard.py` byte-identical to 0.3.0. Its existing unsupported-platform regression rejects webOS; the LG Markdown plan does not claim automated guard coverage. No network client or third-party implementation was added.
- Expanded the declared manifest to **44 files** with three English references, corresponding bilingual README/tutorial changes, and pinned-source provenance regressions. All four promotional PNG hashes and localization restrictions remain unchanged.
- Ran all **100 offline tests** with Python 3.12.14 on macOS: passed. The repository checker, synthetic demo, skill frontmatter validator and whitespace check passed. Deterministic archive construction was checked by the suite, including byte preservation of translated documents and rejection of changed assets, undeclared files and source-pin drift.
- Added 20 LG/research cases to the manual behavioral protocol. These are test scenarios, not completed independent model runs. Source review and offline tests do not exercise a TV, pairing, firmware dependencies or every third-party binary/dependency.
- No TV was connected or changed; no LG client was installed or run, no upstream executable was imported, and no exploit server or payload was executed. Hosted matrix outcomes belong to the release pull request and Actions tab once completed; historical records below retain their original scope.

## Bilingual documentation included in 0.4.0

- Added a complete Chinese README with reciprocal language navigation, plus the optional Chinese tutorial (41 files in the current source manifest). Core instructions and execution boundaries remain English and unchanged.
- Restricted localized documents to `README.zh-CN.md` and `docs/guide.zh-CN.md`, with only a standalone language-navigation line allowed in the English README. Regressions check UTF-8 archive preservation, reference validation in both translations, and continued rejection of Chinese body prose in English core files.
- Ran all **98 offline tests** with Python 3.12.14 on macOS: passed. Repository integrity and whitespace checks also passed. Hosted results are linked in the pull request; historical release records below retain their original test counts and source scope.

## 0.3.0 upstream synchronization

- Reviewed upstream main revision `7c61d3c57e561323b85d7096ee2b686685b9b499` against the previous pin. Upstream has no version tags at this revision; the launcher declares version 2.3 (code 4).
- Updated the skill/repository name and pinned source metadata, keeping independent skill versioning and historical records.
- Added bounded module-card, local settings/theme recovery, physical remote-key, Private DNS, and existing-private-route procedures. Preserved every existing mutation gate, protected package rule, and stock Home / Setup Wizard restriction.
- Kept the package command generator byte-identical. Optional feature writes are reviewed separately; the package guard does not validate those operations.
- Expanded the publication manifest to 39 files and added regressions that reject upstream pin/provenance drift. The four promotional PNG hashes remain unchanged.
- Ran all **95 offline tests** with Python 3.12.14 on macOS: passed. The repository checker, synthetic demo, skill frontmatter validator, and whitespace check also passed. No TV was connected or changed.
- Hosted CI results are linked in the release and Actions tab. Historical completed checks below retain their original scope.


## 0.2.1 naming and README update

- Renamed the skill identifier, host metadata, repository references, and deterministic archive root to `tv-vibehack-skill`.
- Added the maintainer-approved TVRemoteX icon and first three English screenshots in their App Store Connect workflow order (original slides 01, 03, 04), with a U.S. App Store link, optional-app disclosure, and separate image terms.
- Pinned the four reviewed PNG files by SHA-256. The publication checker still rejects undeclared files and changed assets, and now checks local HTML image references as well as Markdown links.
- Ran all **93 offline tests** with Python 3.12.14 on macOS: passed. Ran the repository checker, synthetic demo, and skill frontmatter validator: passed.
- Compared `scripts/plan_guard.py` and the device workflow references with the previous release: byte-identical. No device command or execution approval boundary changed.
- [Validate run 39237849227](https://github.com/songbihai/cleanyourtv-skill/actions/runs/39237849227) passed all nine jobs for the reviewed update at `bccbc5d0cb6ddaf0cea921fa95279314fff2e3bc`. The suite contains 93 tests; the POSIX named-pipe case is intentionally skipped on Windows.
- Read back all 38 uploaded paths and file bytes from the update branch: identical to the reviewed package. Verified GitHub renders all four images at the correct proportions and the download link points to the U.S. App Store.
- This validation-record-only commit is checked by subsequent PR/main runs. The historical runs below cover 0.2.0.

## Historical 0.2.0 validation


Reviewed upstream commit: `b01bb945a0fc64e6dfbb544d8d2163a490c82c50`.

## Completed locally

- Reviewed the entire prior 0.1.0 local draft and recorded findings, reproductions, fixes, and remaining limits in [docs/audit.md](docs/audit.md). Reproductions used only synthetic local data.
- Ran `python -B -m unittest discover -s tests` with Python 3.12.14 on macOS: **87 tests passed**. This includes strict plan validation, exact enabled-state inverses, hardware identity binding, special-file rejection with a finite subprocess timeout, Unicode control/surrogate rejection, numeric overflow, private-file detection, missing/malformed source, archive contents/metadata, deterministic archive bytes, overwrite refusal, and checksum matching.
- Ran `python -B scripts/check_repository.py`: passed declared-source, relative-reference, version, recognizable credential-pattern, and helper-constraint checks. This is not an exhaustive secret scanner or a security audit.
- Ran the skill-creator `quick_validate.py` with temporary validation-only PyYAML 6.0.3: passed (`Skill is valid!`). PyYAML is not a project runtime dependency.
- Parsed host metadata, workflow, and Dependabot YAML; checked read-only token permission, no privileged fork trigger, no referenced repository secrets, non-persistent checkout credentials, full action commit pins, five-minute job timeout, and the configured nine-cell matrix (Python 3.10/3.12/3.14 on Linux/macOS/Windows).
- Checked host installation/capability guidance against official Codex, Claude Code, Gemini CLI, and Agent Skills documentation. This is a documentation check, not a runtime model evaluation.
- Verified checkout v7.0.1 and setup-python v7.0.0 full commit pins against their official release pages and inspected action input/runtime metadata (Node 24). This is not a full audit of their bundled JavaScript or transitive dependencies.
- Reviewed cross-reference consistency, common mutation gates, recovery exceptions, optional feature effects, and absence of unsupported compatibility/safety claims.

The synthetic demo and final archive checks are part of the local artifact pass. Archive/checksum results are supplied beside the final artifact rather than embedded as a self-referential hash in this file.

Development validation was offline except retrieving source, consulting primary documentation/release metadata, and installing temporary validation tooling. No device network was accessed.

## Completed on GitHub

- Created the public [songbihai/tv-vibehack-safe repository](https://github.com/songbihai/cleanyourtv-skill). Read back all 33 source paths and file bytes: identical to the reviewed local source at commit `529c20300ee58d955a1ac35269ed0a3070c5a67a`.
- [Validate run 39234904676](https://github.com/songbihai/cleanyourtv-skill/actions/runs/39234904676) completed successfully in all nine jobs: Python 3.10, 3.12, and 3.14 on ubuntu-latest, macos-latest, and windows-latest. These are runner labels; they do not certify every OS version.
- The Windows Python 3.14 job reported 87 tests, OK with one expected skip for the POSIX named-pipe regression. Do not interpret a platform-specific skip as an executed test.
- Verified that private vulnerability reporting is enabled. GitHub secret scanning and push protection were enabled in the repository settings. No persistent credentials or repository secrets are used by the validation workflow.
- Publication metadata changes are checked by subsequent Validate runs linked from the repository Actions tab. The source commit/run above identifies the tested code; it does not claim an exact later commit was tested before that run exists.

## Not performed / remaining limits

- No ADB connection, device discovery, package disabling, launcher install, settings change, reboot, or recovery on a real TV. No hardware/firmware compatibility certification or boot-persistence test.
- No independent behavioral runs across Codex, Claude, Gemini, or other model/provider combinations. [docs/evaluation.md](docs/evaluation.md) is a protocol, not results.
- No production APK build/signing validation, model API calls, or paid evaluation.
- No native skill installation or independent runtime behavioral evaluation in each assistant host. File/reference readability and format checks do not prove that a model will follow the workflow.
- Repository protection settings and release assets are external state; inspect them on GitHub and follow [docs/release.md](docs/release.md) for future releases.

Offline tests establish the helpers' tested behavior only. They do not establish semantic package safety, authenticity of supplied evidence, host enforcement, resistance to a hostile filesystem/device, or future model compliance. This is a scoped public prerelease; it is not hardware-certified stable software.
