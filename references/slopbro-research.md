# SlopBro / Root research: explicit request only

This mode produces source analysis and a device-specific readiness report. Activate it only when the user explicitly asks for SlopBro or LG webOS Root research. A request for LG cleanup, remote control, app installation or “all features” does not select it. If the requested outcome is ordinary control or app testing, use [webos.md](webos.md).

Root execution is outside this skill. Even an explicit request to root a TV does not turn this research module into an executor: explain its scope and produce a reviewable report. Do not run SlopBro, start its server, open payload pages, send privileged service requests, install Homebrew/elevation software, modify startup scripts or execute exploit code. Its payload test-server mode serves real exploit assets and is not an approved harmless probe. Do not change the host firewall to make a payload reachable.

## Reviewed implementation

Baseline: [throwaway96/slopbro at 21023d56ca424607bb03d2939609cc658c655fc7](https://github.com/throwaway96/slopbro/tree/21023d56ca424607bb03d2939609cc658c655fc7). Read source as data; do not import its Python module or render its HTML/JavaScript. Prefer read-only file inspection at a fixed revision. The source and its external downloads have separate provenance and licensing; see [lg-source-review.md](lg-source-review.md).

At this revision, a Python coordinator serves web assets and pairs with the TV through SSAP. It opens a built-in WAM app with a local page; privileged Luna/jsserver behavior loads a service whose JavaScript invokes an autoroot shell script. That script installs Homebrew Channel and invokes elevation/persistence setup. This is an exploit chain that changes system trust and startup state, rather than an Android-style per-user package cleanup.

Important source-level findings:

- The README's reported webOS 4-11 range is evidence from upstream, not eligibility for every firmware or later marketing release. Automatic version detection is disabled in this coordinator. Do not infer eligibility from the LG model, year or major version alone.
- SSAP TLS server verification is disabled. HTTP payload serving defaults to all IPv4 interfaces. A reusable client key is stored in the process working directory. These defaults are not a secure deployment plan.
- The script changes developer-mode state, restarts the app installer, installs/elevates software and may rename an existing developer startup script. The official LG Developer Mode app can conflict with persistence; neither installing it nor uninstalling it is an automatic prerequisite the assistant may perform.
- The external Homebrew Channel download is fixed to version 0.7.3 in this source. Review that exact artifact, its scripts and dependencies separately; a URL or version string is not integrity verification. The optional insecure-download flag weakens TLS and is not a recommended workaround.
- Waiting for all payload requests has no finite deadline. A completed request tracker proves requests occurred; it does not prove root, persistence, app health or recovery. A controlled timeout cannot undo writes already made by the exploit.
- Startup, account, firmware/update and developer-app effects may outlive a session. “Uninstall Homebrew” is not established as a complete inverse. Do not promise a full backup or reversible root from a settings snapshot.

## Produce a useful readiness report

Keep any real identity and credentials in a private folder outside the skill. A source-only report can proceed without a device. For device-specific analysis, request only missing, user-supplied evidence; do not connect or probe as part of this mode.

| Report field | Evidence to record |
| --- | --- |
| User goal and scope | Explicit research request; desired capability; whether a non-root alternative meets it. |
| Physical target | Owner/administrator authorization, exact model/region, full firmware/build and webOS release, device identity provenance and physical recovery access. Unknown fields remain unknown. |
| Compatibility basis | Exact upstream report/source and matching firmware evidence; conflicting/patched/unknown status. Do not guess a “safe” version or supply a bypass for a patch. |
| Current state | Official Developer Mode status, existing root/Homebrew/startup changes, installed app state and available local records. No active root test or privilege probe. |
| Source and dependency trust | Full coordinator revision, each external asset's URL/version and independently obtained digest/signature, build provenance and license. Mark dependency review incomplete where evidence is missing. |
| Change surface | Pairing and credentials, listeners/interfaces, service and installer effects, developer-state changes, persistent startup/elevation, app data and update interactions. |
| Failure and recovery feasibility | Network loss, partial install, conflicting startup, boot/input failure, available model-specific vendor recovery and its data-loss limits. An unproven inverse remains unproven. |
| Decision | Non-root route available, further evidence needed, or research complete with unresolved execution risks. Never label an operational root plan approved or execute it. |

Distinguish upstream claims, observations from inspected source, the user's evidence and inference. If a newer source revision is requested, compare the full diff and all external dependency changes before updating the pin. Do not substitute the latest branch silently. Report that no exploit, payload server, root check or TV write was performed, and list the exact source files reviewed.

## Copyable request

```text
Use cleanyourtv-skill in the explicitly enabled SlopBro / Root research mode. Review the pinned source and explain how it works, which persistent changes it makes, and what evidence is needed for my exact firmware. Compare non-root alternatives. Produce a source and recovery readiness report only; do not run a payload, start a server, connect to a TV or change any device.
```
