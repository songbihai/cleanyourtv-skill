# Validation record

Date: 2026-10-19 (America/Los_Angeles).

Package: TV Vibehack Safe 0.2.0 public prerelease.

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

- Created the public [songbihai/tv-vibehack-safe repository](https://github.com/songbihai/tv-vibehack-safe). Read back all 33 source paths and file bytes: identical to the reviewed local source at commit `529c20300ee58d955a1ac35269ed0a3070c5a67a`.
- [Validate run 39234904676](https://github.com/songbihai/tv-vibehack-safe/actions/runs/39234904676) completed successfully in all nine jobs: Python 3.10, 3.12, and 3.14 on ubuntu-latest, macos-latest, and windows-latest. These are runner labels; they do not certify every OS version.
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
