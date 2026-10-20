# Reviewed upstream source

Upstream: https://github.com/Gathin23/cleanyourtv (formerly tv-vibehack).
Reviewed revision: `7c61d3c57e561323b85d7096ee2b686685b9b499`.
Review date: 2026-10-19 (America/Los_Angeles).

This is the upstream main-branch revision retrieved for this release; upstream has no version tags at this revision. Its launcher declares version 2.3, version code 4, package `com.gathin.tvhome`, minimum SDK 26, compile/target SDK 34, and Java 17. This Android baseline was adopted in skill 0.3.0 and remains pinned in 0.5.0; LG and Tizen source reviews are separate. The previous review used `b01bb945a0fc64e6dfbb544d8d2163a490c82c50`.

Review the [pinned source tree](https://github.com/Gathin23/cleanyourtv/tree/7c61d3c57e561323b85d7096ee2b686685b9b499), not a moving branch, before building or executing anything. No upstream source, APK, fonts, images, ADB keys, device lists, or dependency binaries are bundled here. This package supplies independent instructions and offline helpers, with upstream attribution in NOTICE and LICENSE.

| Upstream area reviewed | Skill treatment |
| --- | --- |
| PROMPT, device examples, Private DNS and remote-access documentation | Model/firmware evidence is contextual. Do not copy package lists. Optional networking has a separate plan and recovery gate. |
| `tools/tv.py` and transport helpers | Platform Tools first. The Python helper can reuse the host's Android ADB key; review key exposure and dependencies before any authorized use. It is not a host-permission bypass or TLS replacement. |
| Disable/restore scripts and package-input guards | Improved validation and line-ending handling do not make bulk changes appropriate. Keep single-package transactions and exact prior enabled states. Never use the Setup Wizard override; the wizard can own saved Wi-Fi configuration. |
| Launcher build/install wrappers | Their install, permission, Home, and stock-launcher effects remain separate operations. Do not execute the combined wrappers. |
| Gradle and manifest | Build requirements above apply even when an example describes an older Android device. Release builds use debug signing; inspect the artifact and certificate. |
| Module cards and card XML parser | Inspect the declaring package, signing certificate, folded label, and launch component. Keep unfamiliar cards hidden; approve each independently. Bounded parsing does not sandbox an installed app or prove publisher trust. |
| Launcher settings and theme loader | Local layout/motion choices can be cleared by a theme file's length/mtime or revision change. Record and restore UI choices as well as overlay bytes. |
| Theme shell/PowerShell wrappers | They delete overlays, restart Home, and rewrite accessibility state. Use separately reviewed file operations and user-controlled accessibility settings instead. |
| Home/Settings/Input key services | Optional accessibility grants and physical-button checks remain separate. Preserve every existing service. |
| Sky, clock, motion, VPN badge, and input configuration | Expose requested local options; do not infer performance benefits or VPN routing from a badge. Inspect explicit components and approved installed apps. |
| OEM installation and Home restrictions | Stop at vendor verification/signature restrictions. No verifier bypass, stock-Home disabling, root, or bootloader changes. |

The package-plan guard is unchanged from the prior release. It validates only its documented package-plan format; it does not authorize or validate launcher UI actions, APK installation, theme changes, accessibility, DNS, or remote networking. All such writes use the entrypoint's common mutation gate and durable per-step journal.

Primary references at the reviewed revision:

- [Module card specification](https://github.com/Gathin23/cleanyourtv/blob/7c61d3c57e561323b85d7096ee2b686685b9b499/docs/specs/card.md)
- [Module card owner workflow](https://github.com/Gathin23/cleanyourtv/blob/7c61d3c57e561323b85d7096ee2b686685b9b499/docs/modules.md)
- [Theme configuration](https://github.com/Gathin23/cleanyourtv/blob/7c61d3c57e561323b85d7096ee2b686685b9b499/themes/README.md)
- [Private remote routes](https://github.com/Gathin23/cleanyourtv/blob/7c61d3c57e561323b85d7096ee2b686685b9b499/docs/REMOTE.md)
- [Android ADB documentation](https://developer.android.com/tools/adb) and [apksigner documentation](https://developer.android.com/tools/apksigner)

The review describes source behavior and the skill's boundaries. Upstream device reports apply to their reported hardware and firmware; they do not replace target identification or the current user's approval.
