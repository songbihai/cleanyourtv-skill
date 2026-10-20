# CleanYourTV Skill

**English** | [简体中文](README.zh-CN.md)

**Make TV customization easier and safer — Android cleanup, LG webOS and useful Samsung Tizen apps.**

Use your AI assistant to clean up Android TV, customize LG webOS, or install Jellyfin and Moonlight on a Samsung Tizen TV for your media library and PC games. CleanYourTV Skill combines the Android workflow from [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) with reviewed LG and Samsung app workflows: identify your TV, review the source and plan, then apply the changes you approve.

## Why use this skill?

- **Easier to use.** Install one reusable skill and describe what you want. Your assistant follows the relevant audit, cleanup, launcher, or recovery procedure, with copyable requests and references available when needed.
- **Safer execution by design.** The skill adds explicit device identity checks, a plan you approve before changes, protected-package rules, one-package Android transactions, LG pairing/transport checks, and recorded recovery steps. Uncertain outcomes stop further changes instead of triggering blind retries.
- **Portable across assistants.** Plain Markdown and standard-library helpers keep the workflow independent of any model provider. It adapts to the tools and permissions available in your assistant, including plan-only use without device access.

These guardrails are designed to reduce wrong-device changes, unintended loss of TV functions, and mistakes from copying commands or package lists without checking the target TV. Android keeps the original launcher and Setup Wizard enabled; LG keeps its stock Home and system services intact. LG uses its own identity, pairing and recovery procedure rather than Android commands.

## What you can do

- **Clean up Android apps.** Review preinstalled apps and promotional services, understand what they do, and disable approved packages one at a time.
- **Personalize Android Home.** Build and configure the upstream lightweight, Apple TV-style launcher with a favorites dock, app grid, and themes. Switching the default Home depends on your firmware; the original launcher stays enabled.
- **Use the latest launcher features.** Review module cards individually, adjust launcher layout and motion, and configure remote-key helpers when requested. Optional Private DNS and existing private remote connections have [separate procedures](references/network-extras.md).
- **Control LG webOS without root.** Use an existing [Home Assistant LG integration](https://www.home-assistant.io/integrations/webostv/) or [aiowebostv](https://github.com/home-assistant-libs/aiowebostv) for volume, navigation, playback, installed apps and HDMI inputs. Test your own webOS apps through official Developer Mode with [webOS Dev Manager](https://github.com/webosbrew/dev-manager-desktop) or LG CLI. See the [LG workflow](references/webos.md).
- **Add useful Samsung Tizen apps.** Build/review/install [Jellyfin](https://github.com/jellyfin/jellyfin-tizen) for your own media library or [Moonlight](https://github.com/OneLiberty/moonlight-chrome-tizen) for PC game streaming, with final WGT inspection, private TV signing and one-app recovery. This goes beyond remote control. [TizenBrew](https://github.com/reisxd/TizenBrew) is a separate optional module route; see the [Samsung workflow](references/tizen.md).
- **Enable LG Root explicitly.** The [SlopBro module](references/slopbro-research.md) now covers a reviewed, gated Root attempt on an authorized LG TV, including Homebrew/persistence effects, isolated networking and recovery limits. A research request stays source-only. SlopBro does not apply to Samsung; [Samsung Root](references/tizen-root-research.md) remains experimental source research.
- **Keep track of every change.** Review expected effects and recovery steps before approving a change, then check that your essential TV functions still work.

Start with a request like:

```text
Use cleanyourtv-skill to help me clean up my Android TV
and set up a simpler home screen. Keep my streaming apps,
casting, and voice controls. Show me a plan before changing anything.
```

For Samsung apps, start with:

```text
Use cleanyourtv-skill to prepare Jellyfin for my media server
or Moonlight for my own PC on my Samsung Tizen TV. Review my
exact firmware, source, signed WGT and recovery limits.
Build/review locally first; show the install plan before TV changes.
```

For LG, start with:

```text
Use cleanyourtv-skill for my LG webOS TV. Review my existing
Home Assistant LG entity and available apps/HDMI inputs.
I will confirm the exact TV. Start with a plan; do not pair,
install, change settings or issue controls yet.
```

Android device access uses ADB and TV debugging authorization. LG uses its own paired controller or developer tools; it does not use ADB or install the Android launcher. A chat-only assistant can review either plan from the required private evidence. Everyday control and official developer-app testing need no root.

## What is included

- A portable [SKILL.md](SKILL.md) with progressively loaded references.
- An original offline WGT inspector reporting package IDs, hash, permissions, services and signing filenames without extraction or execution; it does not verify signatures or approve installation.
- An offline Python plan guard that rejects malformed plans, protected package names, missing baseline state, device mismatch, and stale snapshots. It emits command arguments but cannot execute them.
- Launcher, connection, recovery, and privacy procedures tied to a reviewed upstream revision.
- Standard-library tests, cross-platform CI configuration, behavioral evaluation cases, licensing, and contribution/security guidance.

## Quick start

1. Download the source or checked ZIP from the [v0.5.0 prerelease](https://github.com/songbihai/cleanyourtv-skill/releases/tag/v0.5.0). For the custom ZIP, verify the adjacent SHA-256 file before extraction. Do not run device commands from an unreviewed branch.
2. Open [SKILL.md](SKILL.md) in your assistant, or install this entire folder as a skill using your host's documented method. Preserve `references/` and `scripts/` beside it.
3. Ask: `Use cleanyourtv-skill to audit my Android TV. Start in plan mode. Do not change the device. I will provide its exact ADB endpoint.`
4. For Android package cleanup, use the snapshot and offline guard in [plan-format.md](references/plan-format.md). For LG, use [webos.md](references/webos.md); for Samsung apps, use [tizen.md](references/tizen.md) and its offline WGT inspector. Explicit LG Root has its own gate in [slopbro-research.md](references/slopbro-research.md). Review and authorize the exact effects before execution; the Android guard does not validate LG/Tizen/Root actions, and the WGT inspector is a review aid rather than an executor.

For step-by-step setup and copyable Chinese requests, see the [Chinese usage guide](docs/guide.zh-CN.md).

To inspect the synthetic example without a TV, from the repository root:

```text
python3 scripts/plan_guard.py --snapshot examples/snapshot.synthetic.json --plan examples/plan.synthetic.json --demo
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

`--demo` accepts only fixtures marked synthetic and labels output non-executable. It does not allow stale real snapshots. Never use fixture evidence to administer a device. Python 3.10 or newer is required for the helpers; they have no third-party dependencies.

## Model and host compatibility

The skill uses ordinary Markdown and the [Agent Skills format](https://agentskills.io/specification). Load it in an assistant that can read the skill and its references. The workflows below adapt to the tools, permissions, and context available in each host.

| Host capability | Use |
| --- | --- |
| Native Agent Skills loader | Install the whole folder; invoke `cleanyourtv-skill` using the host's syntax. |
| Codex | Copy the folder to `~/.agents/skills/cleanyourtv-skill/`; invoke `$cleanyourtv-skill`. Optional `agents/openai.yaml` supplies UI text. |
| Claude Code | Use the personal or project skill location and invocation described in [compatibility.md](docs/compatibility.md). |
| Gemini CLI | Use its documented skill discovery and consent flow; see [compatibility.md](docs/compatibility.md). |
| Chat assistant with file access, no shell | Read the skill and relevant references; produce plans and ask the user for command output. |
| No file/reference access | Provide the skill and the required reference text in context; stop if required instructions do not fit or are missing. |
| No reliable target selection, timeout, or approval mechanism | Audit/plan only; no device mutations. |

See [compatibility.md](docs/compatibility.md) for official host sources, copyable audit requests, argument handling, and capability fallbacks.

No API, vendor SDK, MCP server, model-specific system prompt, or paid service is required by the skill. Android execution uses Platform Tools; launcher builds also require the upstream JDK/Android SDK/Gradle toolchain. LG can reuse an existing Home Assistant integration or Dev Manager GUI; a separate aiowebostv client requires Python 3.11+ and its dependencies. Samsung WGT builds/installs use Tizen Studio with TV/certificate tools, plus the selected app's build toolchain. Optional tools, pairing, signing and downloads have their own approval and trust requirements.

## Supported scope

| Platform / mode | Supported work |
| --- | --- |
| Android TV / Google TV | Audit, reviewed per-user package disabling, and upstream launcher build/install/configuration with stock Home retained. |
| LG webOS, non-root | Targeted normal controls, state/app/input review, and testing the user's own app through official Developer Mode. No system debloat or Android launcher replacement. |
| Samsung Tizen apps | Jellyfin media libraries, Moonlight PC streaming, personal WGT build/review/sign/install/test and scoped recovery; optional TizenBrew module review. |
| Explicit LG SlopBro Root | Source/firmware assessment and a separately approved, bounded Root attempt with dependency/startup/access/recovery review. Research-only requests stay source-only. |
| Explicit Samsung Root research | Exact upstream model/build comparison and customization planning; experimental exploit execution is not included. |

Samsung Orsay, LG NetCast, Fire OS, managed devices, Android secondary-user mutations, flashing, system-app removal and stock-launcher/setup-wizard disabling remain outside scope. Reviewed LG clients have [transport and developer-session limits](references/webos.md); use a trusted private network and confirm the physical TV.

Review real device output and confirm the target TV before each change. The offline guard checks plan structure, protected packages, device identity fields, and recovery data; firmware dependencies still require a review of the specific device. See [SECURITY.md](SECURITY.md).

## From the maintainer: TVRemoteX

<img src="assets/tvremotex/logo.png" alt="TVRemoteX app icon" width="72" height="72">

TVRemoteX brings everyday TV controls to your iPhone and iPad: navigate with a touchpad, type with your phone’s keyboard, adjust volume, and launch apps on compatible TVs.

[View TVRemoteX on the App Store](https://apps.apple.com/us/app/tvremotex-universal-tv-remote/id6755671893)

<p>
  <img src="assets/tvremotex/01-brands-en-US.png" alt="TVRemoteX English screenshot 1: TV brands" width="31%">
  <img src="assets/tvremotex/02-power-and-apps-en-US.png" alt="TVRemoteX English screenshot 2: power, channels, and app control" width="31%">
  <img src="assets/tvremotex/03-keyboard-and-touchpad-en-US.png" alt="TVRemoteX English screenshot 3: keyboard, volume, and touchpad" width="31%">
</p>

Made by the maintainer of this skill. TVRemoteX is optional; the skill works independently. Features vary by TV model and platform. Some features require in-app purchases.

## Project status and publishing

**Version 0.5.0.** Synced to the reviewed [cleanyourtv source revision](https://github.com/Gathin23/cleanyourtv/tree/7c61d3c57e561323b85d7096ee2b686685b9b499), whose launcher is version 2.3. The offline helpers and packaging tools have a **126-test suite**. See [VALIDATION.md](VALIDATION.md) for completed checks and the [Actions tab](https://github.com/songbihai/cleanyourtv-skill/actions) for cross-platform CI results.

The skill builds on the upstream TV customization workflow. Consult upstream’s [device examples](https://github.com/Gathin23/cleanyourtv/tree/main/examples) for model-specific reports, then match the model, OS, and firmware to your TV. Keep device changes within the supported scope above and review each plan before execution.

See [upstream-review.md](references/upstream-review.md) for Android provenance and [lg-source-review.md](references/lg-source-review.md) for LG tool versions and findings, [tizen-source-review.md](references/tizen-source-review.md) for Samsung application/installer choices, [evaluation.md](docs/evaluation.md) for assistant behavior scenarios, [release.md](docs/release.md) for publishing procedures, and the [Actions tab](https://github.com/songbihai/cleanyourtv-skill/actions) for current CI results.

To build a review archive containing only declared source and reviewed assets, run `python3 scripts/build_release.py --output /path/outside/repository/cleanyourtv-skill-0.5.0.zip`. It refuses existing output and writes a `.sha256` sidecar. The [audit report](docs/audit.md) records this review and its limits.

Instructions and helpers are MIT licensed; promotional images have [separate terms](assets/tvremotex/NOTICE.md). Upstream attribution is preserved in [NOTICE](NOTICE) and [LICENSE](LICENSE). This is an independent project, not an official upstream, Samsung, LG, Home Assistant or Android project. Optional third-party tools retain their own licenses; no client, IPK or exploit code is bundled.
