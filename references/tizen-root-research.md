# Samsung Tizen Root research: separate experimental route

Only an explicit Samsung Root research request selects this module. Root permission from the user permits assessment; it does not identify a TV or approve every future system change. SlopBro targets LG webOS and must never be tried on Samsung. Normal Jellyfin/Moonlight app installation remains available through [tizen.md](tizen.md) without Root.

Baseline: [chris-ritsen/samsung-tv-root at 4ad2c4d3b0d0e0da4b5b7ebe4a787e94596f416b](https://github.com/chris-ritsen/samsung-tv-root/tree/4ad2c4d3b0d0e0da4b5b7ebe4a787e94596f416b). This is a promising research project with narrow device evidence, not a generally mature root package for all retail Samsung TVs. This skill supports static source/eligibility and customization planning for this route; it does not execute its exploits, start its controller or certify payloads.

The inspected README reports these exact targets:

| Model | Firmware / internal build |
| --- | --- |
| QN55QN90BAFXZA | T-PTMAKUC-1602.3 / T-PTMAKUC-REL-202310071804 |
| QN75QN90FAFXZA | 1203.0 / T-RSMFAKUC-0090-REL-202512092052 |
| QA55QN90FAUXEG | 1301.0 / T-RSMFUABC-0090-REL-202607141954 |

These are upstream reports, not tests performed by this skill. “Compatible-untested” and “model-independent” labels do not establish equivalence for a new panel, region, SoC, kernel, driver or build. Compare full hardware/firmware evidence; unknown or mismatched identity remains a research report, not an execution recommendation. Do not downgrade firmware or change security/update policy to make a target fit.

The project combines an SDB package-name injection foothold with device-specific memory/GPU or archive-launcher escalation, then a root agent. Optional UEP changes allow unsigned native execution. Root is volatile; a host controller can reacquire it after boot or agent loss. That controller is repeated exploitation with ongoing access, not a harmless persistent connection. Source names like `preflight` do not mean read-only: inspect the call path before any future live probe.

Produce a private report with: explicit goal and authority; physical identity, region/full firmware and exact source match; desired benefit such as remote-key remapping or temporary UI customization; normal-app alternatives; all source/payload/dependency provenance; foothold/escalation writes and privilege changes; listener authentication/secrets; agent/controller lifecycle and retry behavior; update effects; and model-specific recovery/data-loss limits. Mark unreviewed payloads/dependencies honestly. Do not import/run the CLI even for capability discovery during static research.

Avoid universal system debloat lists, stock Smart Hub removal, system-partition writes, firmware keys/DRM extraction, automatic UEP disable, hidden observation, screenshots or remote-input capture. Root access does not approve any of those effects. Any future execution support requires a complete route-specific payload and recovery review plus a concrete owned-device plan; this release supplies no root command recipe for Samsung. Retain source data outside the project and never publish real TV tokens, DUIDs or network identities.
