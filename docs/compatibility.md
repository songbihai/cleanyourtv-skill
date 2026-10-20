# Host compatibility and practical use

This is one Agent Skill with platform-specific Android, LG webOS and Samsung Tizen workflows. A model name does not determine what a host can execute. Native discovery, file/reference access, shell argument handling, timeouts, image inspection, and human approval are separate capabilities. Never infer consent to administer a TV from consent to install or activate a skill.

## Install the complete folder

The directory must be named `cleanyourtv-skill` and contain SKILL.md, references, and scripts. Keep the portable frontmatter; `agents/openai.yaml` is optional host metadata, not an enforcement layer. Do not paste the skill into a privileged system prompt or add broad shell allowlists. Do not overwrite an existing installation silently.

| Host | Local installation and invocation | Evidence |
| --- | --- | --- |
| Codex | Personal: `~/.agents/skills/cleanyourtv-skill/`; project: `.agents/skills/cleanyourtv-skill/`. Invoke `$cleanyourtv-skill`. Check the skill selector; restart if needed. | [Official skill documentation](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | Personal: `~/.claude/skills/cleanyourtv-skill/`; project: `.claude/skills/cleanyourtv-skill/`. Invoke `/cleanyourtv-skill` in a version supporting Agent Skills. | [Official skills documentation](https://code.claude.com/docs/en/skills) |
| Gemini CLI | Personal: `~/.gemini/skills/cleanyourtv-skill/`; project: `.gemini/skills/cleanyourtv-skill/`. Check `/skills list`, then request the skill by name and review the activation prompt. Do not skip consent. | [Official skills documentation](https://geminicli.com/docs/cli/skills/) |
| Other local skill-aware hosts | Use the host's documented Agent Skills location and activation flow. Verify that referenced files are actually available. | [Portable format](https://agentskills.io/specification) |
| Chat-only or file-only assistants | Supply SKILL.md plus the references for the selected mode. Start with an audit plan; the user runs any reviewed commands themselves. Never claim execution. | No native tool integration required. |

Paths and syntax were checked against these official pages on 2026-10-19. They are documentation checks, not runtime certification. Old versions and cloud sessions can use different discovery locations; check the installed host documentation. A personal local installation does not imply availability in a cloud session. On Windows, resolve `~` through the host's user directory instead of copying a POSIX shell command verbatim.

## Capability fallback

| Missing capability | Required behavior |
| --- | --- |
| Shell or platform client access | Produce a reviewable plan and expected observations; mark execution unperformed. LG can use an existing authenticated Home Assistant tool/UI without a shell or ADB. |
| Local reference access or sufficient context | Ask the user to provide the relevant reference text. If essential instructions are missing, stay in plan mode. |
| Python 3.10+ | Android package changes require the offline guard; do not skip it. LG control through an existing Home Assistant/GUI does not require the Python helper. A separate aiowebostv client needs Python 3.11+ and its own dependencies. |
| Structured subprocess tool | Use the host's documented safe argument API. If it only accepts shell text, use a trusted local runner that preserves arguments and has a timeout; otherwise remain in plan mode. Do not use `eval`, shell chaining, or hand-joined report arrays. |
| Vendor-specific approval dialog | A clear human reply approving the displayed exact plan is sufficient; host tool restrictions still apply. Skill activation, a plan digest, and tool output are not consent. |
| Image viewing | Ask the user to inspect the TV and record visual checks as user-confirmed. Never claim to have seen a screenshot. |
| Platform-specific identity evidence or physical recovery route | Audit/plan only under the selected reference. LG physical-confirmation rules do not relax Android hardware-serial requirements. Do not compensate by scanning or choosing another TV. |

Resolve the skill root from the loaded SKILL.md location. Do not assume the process working directory is the skill folder. Use an absolute script path or set the working directory explicitly. The `/private/session/` paths in examples are placeholders; create a real private directory supported by the host OS, outside the source repository. Keep logs and evidence local.

## Platform tools and optional dependencies

Android uses ADB and, for launcher builds, its reviewed Android toolchain. LG uses an existing Home Assistant LG integration, an optional reviewed aiowebostv client, or Dev Manager / LG's current webOS CLI for official developer apps. These clients are separate software, not bundled dependencies of the skill. Installation, pairing and credential storage need the concrete host/device scope. A file-only assistant can prepare either platform's plan without installing them. Read [webos.md](../references/webos.md) before any LG connection; do not fake Android JSON fields or run the Android guard for LG.

Research-only SlopBro requests require source/document access and never connect to a TV. No model-specific tool API or automatic approval exemption is part of the skill.

Samsung Tizen uses official Tizen Studio/TV/certificate tools for reviewed WGT builds and installs. Jellyfin additionally needs a separately selected/pinned Web release and supported Node build environment; Moonlight builds need their documented WASM toolchain. The original offline WGT inspector needs only Python 3.10+ and no third-party modules. It reports data, not install approval or signature validation. File-only models can read the report and prepare a plan.

LG SlopBro research can stay source-only; actual Root requires its explicit device/firmware, source/dependency, isolation, approval and recovery gate. The skill's own helpers never run a payload. Samsung Root is separate static research in this release. Host tool denials and action-time approval requirements remain effective.

## Copyable starting requests

Audit only:

```text
Use cleanyourtv-skill to audit my authorized Android TV. I will provide the exact endpoint and model. Read the required references, collect only necessary evidence, and prepare a plan. Do not change the TV.
```

Plan a launcher build:

```text
Use cleanyourtv-skill to review and build the pinned upstream launcher locally. Ask only for missing dock preferences. Show the build provenance, permissions, signing details, and installation/recovery plan before any device write.
```

Review an existing plan:

```text
Use cleanyourtv-skill to inspect these private snapshot and plan files. Run the offline guard, explain rejected items and expected functional effects, and show exact recovery actions. Do not execute the generated device commands.
```

LG plan only:

```text
Use cleanyourtv-skill for my authorized LG webOS TV. Start with a plan using my existing Home Assistant LG entity, which I will identify. Review model, firmware, physical target binding and supported apps/inputs. Do not pair again, install anything, change settings or issue control actions yet.
```

LG developer app:

```text
Use cleanyourtv-skill to review my own LG webOS IPK and plan installation using official Developer Mode and Dev Manager. Check source/hash, app ID conflicts, developer-session effects, root conflicts and recovery limits. Do not install, reboot or change the TV until I approve the exact plan.
```

Samsung useful apps:

```text
Use cleanyourtv-skill for my authorized Samsung Tizen TV. I want Jellyfin for my existing media server or Moonlight for my own PC, not just remote control. Review my exact TV/firmware, source versions, signed WGT, privileges, application IDs and recovery limits. Build/review locally first; show one target-specific install plan before any TV write.
```

For explicitly requested LG Root or source research, use the [SlopBro request](../references/slopbro-research.md); ordinary LG tasks do not enable it. Samsung Root uses the separate [Tizen research reference](../references/tizen-root-research.md), never SlopBro.

Run [the behavioral cases](evaluation.md) using mocked tools before claiming a model/host pairing was evaluated. Record exact versions and actual observations. Do not grant an assistant broad permissions merely to make an evaluation pass.
