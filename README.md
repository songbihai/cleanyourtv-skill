# TV Vibehack Skill

A model-independent Agent Skill for cautious Android TV and Google TV customization, based on [Gathin23/tv-vibehack](https://github.com/Gathin23/tv-vibehack). It adds evidence-based package review, hardware identity checks, explicit target selection, small transactions, and recovery instructions. All project text is in English.

**Version 0.2.1: public prerelease.** Offline tests do not establish hardware compatibility. No TV was changed during development. This project does not promise that disabling a package is safe on every firmware.

## What is included

- A portable [SKILL.md](SKILL.md) with progressively loaded references.
- An offline Python plan guard that rejects malformed plans, protected package names, missing baseline state, device mismatch, and stale snapshots. It emits command arguments but cannot execute them.
- Launcher, connection, recovery, and privacy procedures tied to a reviewed upstream revision.
- Standard-library tests, cross-platform CI configuration, behavioral evaluation cases, licensing, and contribution/security guidance.

## Quick start

1. Download the source or checked ZIP from the [v0.2.1 prerelease](https://github.com/songbihai/tv-vibehack-skill/releases/tag/v0.2.1). For the custom ZIP, verify the adjacent SHA-256 file before extraction. Do not run device commands from an unreviewed branch.
2. Open [SKILL.md](SKILL.md) in your assistant, or install this entire folder as a skill using your host's documented method. Preserve `references/` and `scripts/` beside it.
3. Ask: `Use tv-vibehack-skill to audit my Android TV. Start in plan mode. Do not change the device. I will provide its exact ADB endpoint.`
4. For a real operation, follow the snapshot and plan procedure in [plan-format.md](references/plan-format.md), review its output, and approve the exact change before execution.

To inspect the synthetic example without a TV, from the repository root:

```text
python3 scripts/plan_guard.py --snapshot examples/snapshot.synthetic.json --plan examples/plan.synthetic.json --demo
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

`--demo` accepts only fixtures marked synthetic and labels output non-executable. It does not allow stale real snapshots. Never use fixture evidence to administer a device. Python 3.10 or newer is required for the helpers; they have no third-party dependencies.

## Model and host compatibility

The core is ordinary Markdown using the [Agent Skills format](https://agentskills.io/specification). Any model can read it; correct behavior depends on the model, context limits, tools, and host safeguards. This is a design target, not a claim of live testing on every model.

| Host capability | Use |
| --- | --- |
| Native Agent Skills loader | Install the whole folder; invoke `tv-vibehack-skill` using the host's syntax. |
| Codex | Copy the folder to `~/.agents/skills/tv-vibehack-skill/`; invoke `$tv-vibehack-skill`. Optional `agents/openai.yaml` supplies UI text. |
| Claude Code | Use the personal or project skill location and invocation described in [compatibility.md](docs/compatibility.md). |
| Gemini CLI | Use its documented skill discovery and consent flow; see [compatibility.md](docs/compatibility.md). |
| Chat assistant with file access, no shell | Read the skill and relevant references; produce plans and ask the user for command output. |
| No file/reference access | Provide the skill and the required reference text in context; stop if required instructions do not fit or are missing. |
| No reliable target selection, timeout, or approval mechanism | Audit/plan only; no device mutations. |

See [compatibility.md](docs/compatibility.md) for official host sources, copyable audit requests, argument handling, and capability fallbacks. Installation compatibility is documented; model behavior is not certified.

No API, vendor SDK, MCP server, model-specific system prompt, or paid service is required by the skill. Actual execution requires Android SDK Platform Tools and authorization on the TV. Building the upstream launcher additionally requires its JDK/Android SDK/Gradle toolchain and dependency downloads.

## Supported scope

Audit and carefully reviewed per-user disabling on Android TV/Google TV; build/install/configure the upstream launcher while keeping stock Home available. Samsung Tizen, LG webOS, Fire OS, managed devices, secondary-user mutations, rooting, flashing, and stock-launcher/setup-wizard disabling are outside this release. These limits are intentional even where upstream offers broader workflows.

The guard checks structured claims; it cannot discover hidden OEM dependencies or validate facts invented by a model. The operator must inspect real evidence and recheck the device before each change. Instructions are not a security boundary. See [SECURITY.md](SECURITY.md).

## From the maintainer: TVRemoteX

<img src="assets/tvremotex/logo.png" alt="TVRemoteX app icon" width="72" height="72">

TVRemoteX brings everyday TV controls to your iPhone and iPad: navigate with a touchpad, type with your phone’s keyboard, adjust volume, and launch apps on compatible TVs.

[View TVRemoteX on the U.S. App Store](https://apps.apple.com/us/app/tvremotex-universal-tv-remote/id6755671893)

<p>
  <img src="assets/tvremotex/01-brands-en-US.png" alt="TVRemoteX English screenshot 1: TV brands" width="31%">
  <img src="assets/tvremotex/02-power-and-apps-en-US.png" alt="TVRemoteX English screenshot 2: power, channels, and app control" width="31%">
  <img src="assets/tvremotex/03-keyboard-and-touchpad-en-US.png" alt="TVRemoteX English screenshot 3: keyboard, volume, and touchpad" width="31%">
</p>

Made by the maintainer of this skill. TVRemoteX is optional; the skill works independently. Features vary by TV model and platform. Some features require in-app purchases.

## Project status and publishing

See [upstream-review.md](references/upstream-review.md) for provenance, [evaluation.md](docs/evaluation.md) for behavioral cases, [release.md](docs/release.md) for release gates, and [VALIDATION.md](VALIDATION.md) for the actual validation record. The [historical nine-environment validation run](https://github.com/songbihai/tv-vibehack-skill/actions/runs/39234904676) passed for 0.2.0; the [Actions tab](https://github.com/songbihai/tv-vibehack-skill/actions) and [validation record](VALIDATION.md) track the current update. Hardware behavior and independent model/host behavior remain unverified; see the validation record for exact scope. Future releases must satisfy the release checklist. Do not describe this as hardware-certified or universally safe.

To build a review archive containing only declared source and reviewed assets, run `python3 scripts/build_release.py --output /path/outside/repository/tv-vibehack-skill-0.2.1.zip`. It refuses existing output and writes a `.sha256` sidecar. The [audit report](docs/audit.md) records this review and its limits.

Instructions and helpers are MIT licensed; promotional images have [separate terms](assets/tvremotex/NOTICE.md). Upstream attribution is preserved in [NOTICE](NOTICE) and [LICENSE](LICENSE). This is an independent project, not an official upstream or Android project.
