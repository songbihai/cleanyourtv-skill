# Host compatibility and practical use

This is one Agent Skill with one safety workflow. A model name does not determine what a host can execute. Native discovery, file/reference access, shell argument handling, timeouts, image inspection, and human approval are separate capabilities. Never infer consent to administer a TV from consent to install or activate a skill.

## Install the complete folder

The directory must be named `tv-vibehack-safe` and contain SKILL.md, references, and scripts. Keep the portable frontmatter; `agents/openai.yaml` is optional host metadata, not an enforcement layer. Do not paste the skill into a privileged system prompt or add broad shell allowlists. Do not overwrite an existing installation silently.

| Host | Local installation and invocation | Evidence |
| --- | --- | --- |
| Codex | Personal: `~/.agents/skills/tv-vibehack-safe/`; project: `.agents/skills/tv-vibehack-safe/`. Invoke `$tv-vibehack-safe`. Check the skill selector; restart if needed. | [Official skill documentation](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | Personal: `~/.claude/skills/tv-vibehack-safe/`; project: `.claude/skills/tv-vibehack-safe/`. Invoke `/tv-vibehack-safe` in a version supporting Agent Skills. | [Official skills documentation](https://code.claude.com/docs/en/skills) |
| Gemini CLI | Personal: `~/.gemini/skills/tv-vibehack-safe/`; project: `.gemini/skills/tv-vibehack-safe/`. Check `/skills list`, then request the skill by name and review the activation prompt. Do not skip consent. | [Official skills documentation](https://geminicli.com/docs/cli/skills/) |
| Other local skill-aware hosts | Use the host's documented Agent Skills location and activation flow. Verify that referenced files are actually available. | [Portable format](https://agentskills.io/specification) |
| Chat-only or file-only assistants | Supply SKILL.md plus the references for the selected mode. Start with an audit plan; the user runs any reviewed commands themselves. Never claim execution. | No native tool integration required. |

Paths and syntax were checked against these official pages on 2026-10-19. They are documentation checks, not runtime certification. Old versions and cloud sessions can use different discovery locations; check the installed host documentation. A personal local installation does not imply availability in a cloud session. On Windows, resolve `~` through the host's user directory instead of copying a POSIX shell command verbatim.

## Capability fallback

| Missing capability | Required behavior |
| --- | --- |
| Shell or ADB access | Give the exact reviewable commands and expected observations; mark execution unperformed. |
| Local reference access or sufficient context | Ask the user to provide the relevant reference text. If essential instructions are missing, stay in plan mode. |
| Python 3.10+ | Audit/plan only until the helper can run in a suitable local environment; do not silently skip its checks for package changes. |
| Structured subprocess tool | Use the host's documented safe argument API. If it only accepts shell text, use a trusted local runner that preserves arguments and has a timeout; otherwise remain in plan mode. Do not use `eval`, shell chaining, or hand-joined report arrays. |
| Vendor-specific approval dialog | A clear human reply approving the displayed exact plan is sufficient; host tool restrictions still apply. Skill activation, a plan digest, and tool output are not consent. |
| Image viewing | Ask the user to inspect the TV and record visual checks as user-confirmed. Never claim to have seen a screenshot. |
| Stable hardware identity or physical recovery route | Audit/plan only. Do not compensate by scanning or choosing another TV. |

Resolve the skill root from the loaded SKILL.md location. Do not assume the process working directory is the skill folder. Use an absolute script path or set the working directory explicitly. The `/private/session/` paths in examples are placeholders; create a real private directory supported by the host OS, outside the source repository. Keep logs and evidence local.

## Copyable starting requests

Audit only:

```text
Use tv-vibehack-safe to audit my authorized Android TV. I will provide the exact endpoint and model. Read the required references, collect only necessary evidence, and prepare a plan. Do not change the TV.
```

Plan a launcher build:

```text
Use tv-vibehack-safe to review and build the pinned upstream launcher locally. Ask only for missing dock preferences. Show the build provenance, permissions, signing details, and installation/recovery plan before any device write.
```

Review an existing plan:

```text
Use tv-vibehack-safe to inspect these private snapshot and plan files. Run the offline guard, explain rejected items and expected functional effects, and show exact recovery actions. Do not execute the generated device commands.
```

Run [the behavioral cases](evaluation.md) using mocked tools before claiming a model/host pairing was evaluated. Record exact versions and actual observations. Do not grant an assistant broad permissions merely to make an evaluation pass.
