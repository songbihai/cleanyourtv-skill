# Reviewed upstream source

Upstream: https://github.com/Gathin23/cleanyourtv (formerly tv-vibehack).
Reviewed revision: `ec811adadbf093f63a388551741dc9fc7d33c960`.
Review date: 2026-11-23 (America/Los_Angeles).

The retrieved main snapshot declares launcher **3.6**, version code **15**, default package `com.gathin.tvhome`, minimum SDK 26, compile/target SDK 34, Java source/target 17 and Gradle 8.9. Use a full JDK 17 through 22 with `jlink` and Android platform 34/build-tools 34.x. A newer SDK platform alone does not replace platform 34. This baseline replaces `7c61d3c57e561323b85d7096ee2b686685b9b499` (launcher 2.3) in skill 0.6.0. LG and Tizen pins are unchanged.

Scope: static review of the README, Gradle/wrapper, manifest, configuration, module contract, themes/add-on documentation, installer/disable surfaces, native-ADB documentation, and ServiceRepair/GuardRevival/GuardKeep/ThemeProvider implementations. This is not a complete audit of the expanded repository, every add-on or dependency. No upstream code was run or built. Its Git commit date may use a timezone one day ahead of this local review date; the exact SHA identifies the retrieved bytes.

Review the [pinned source tree](https://github.com/Gathin23/cleanyourtv/tree/ec811adadbf093f63a388551741dc9fc7d33c960), not a moving branch, before building or executing anything. No upstream source, APK, fonts, images, ADB keys, device lists, or dependency binaries are bundled here. This package supplies independent instructions and offline helpers, with upstream attribution in NOTICE and LICENSE.

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

- [Module card specification](https://github.com/Gathin23/cleanyourtv/blob/ec811adadbf093f63a388551741dc9fc7d33c960/docs/specs/card.md)
- [Module card owner workflow](https://github.com/Gathin23/cleanyourtv/blob/ec811adadbf093f63a388551741dc9fc7d33c960/docs/modules.md)
- [Theme configuration](https://github.com/Gathin23/cleanyourtv/blob/ec811adadbf093f63a388551741dc9fc7d33c960/themes/README.md)
- [Private remote routes](https://github.com/Gathin23/cleanyourtv/blob/ec811adadbf093f63a388551741dc9fc7d33c960/docs/REMOTE.md)
- [Android ADB documentation](https://developer.android.com/tools/adb) and [apksigner documentation](https://developer.android.com/tools/apksigner)

The review describes source behavior and the skill's boundaries. Upstream device reports apply to their reported hardware and firmware; they do not replace target identification or the current user's approval.

## 3.6 changes and adoption decisions

- App library and tile management, richer themes/wallpaper collections, local stats, Game Day and add-ons are optional. Use the local UI/configuration reference; a theme or module does not authorize installing another app, contacting its server or granting permissions. Hiding a tile is not package disabling.
- `launcherApplicationId` can change the APK identity for OEM allowlists. This skill keeps the default identity: do not impersonate a stock launcher, overwrite an OEM package or select a package-name workaround automatically. Stop at an OEM restriction.
- The manifest now requests `WRITE_SECURE_SETTINGS`. `restore_key_services` defaults to false, but an existing grant can survive an APK update. Capture the grant and effective configuration before updating. ServiceRepair can rewrite the accessibility list and switch; GuardRevival uses notification-listener access and GuardKeep can restore a helper. These are distinct optional access/lifecycle changes, not ordinary launcher installation. Do not silently grant, revoke or activate them.
- The current install wrapper can grant or revoke secure-settings access, set OEM autostart app-ops, cycle the accessibility list, install/start Home and alter the Home candidate set. The wrapper remains excluded even if stock disabling is suppressed.
- The theme content provider provides an app-supported path when direct `Android/data` access is refused. Review its allowlisted paths and back up all replaced files before using it; do not root or grant the launcher secure-settings access merely to write a theme. Wallpaper collections and UI overrides require complete recovery, not a single config-file copy.
- The optional Google ADB backend selects a previously paired endpoint through `TV_ADB_BINARY`/`TV_HOST`. It can retain encrypted Wireless debugging without opening port 5555. Review dependencies and host authorization before use; no relay or alternate client may bypass a denied Local Network/tool permission.
- Upstream examples and device reports have grown. They remain model/firmware evidence, never a package allowlist. This skill still preserves all HOME candidates, Setup Wizard, updates and unknown dependencies; it does not adopt Fire OS or generalized bulk restore.

Additional pinned references: [add-ons](https://github.com/Gathin23/cleanyourtv/blob/ec811adadbf093f63a388551741dc9fc7d33c960/addons/README.md), [native ADB](https://github.com/Gathin23/cleanyourtv/blob/ec811adadbf093f63a388551741dc9fc7d33c960/tools/native-adb.md), [launcher build](https://github.com/Gathin23/cleanyourtv/blob/ec811adadbf093f63a388551741dc9fc7d33c960/launcher/app/build.gradle).
