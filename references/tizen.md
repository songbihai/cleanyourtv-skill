# Samsung Tizen: install useful apps, build and review WGTs

Read this before any Samsung TV connection. Identify retail Samsung **Tizen TV**, exact model/region, OS and firmware. Samsung Orsay, Android, LG webOS and managed hospitality/signage devices use different workflows. This mode adds apps and their configuration; it is not a generic system debloater, launcher replacement or remote-control-only integration.

## Choose an outcome

| User outcome | Reviewed source / route | What success means |
| --- | --- | --- |
| Play the user's own media library | Jellyfin for Tizen + a matching Jellyfin Web release and existing authorized server | Reviewed signed WGT installed, user logs in privately, a representative video/audio/subtitle plays and Home/Back work. |
| Stream the user's PC games | Moonlight for Tizen + an existing authorized Sunshine/GameStream host | Reviewed signed WGT installed, explicit host paired by the user, conservative video settings and a real controller test. |
| Build/test a personal web app | Samsung Tizen Studio, TV extension and Certificate Manager | Offline package review, valid TV signing/profile and one approved install/launch. |
| Custom web apps or modules | TizenBrew, optional separate module review | Requires its own localhost developer-host change and dynamic-code/service assessment; do not auto-run its installer. |
| Root-dependent customization | [Tizen Root research](tizen-root-research.md) | Exact-firmware comparison and a concrete plan. Samsung Root is experimental and is not the LG SlopBro flow. |

Read [tizen-source-review.md](tizen-source-review.md) for fixed revisions and why convenience installers are not the default. Prefer an existing official store app if it meets the goal; otherwise review the exact upstream source/artifact. Source pins are inspection baselines, not a command to downgrade a supported working install. Do not invent codec, HDR, gamepad or firmware compatibility from a model year or manifest minimum version.

## Platform identity, tools and credentials

- Confirm ownership/administrative authority, physical remote access and one TV's displayed address. Record model/region, complete firmware/build and Tizen release, developer-mode status and its **Host PC IP** baseline. The Host PC IP is the allowed development computer's address, not the TV's address.
- Use Samsung/Tizen Studio from the official publisher with TV and certificate extensions. Review host downloads, dependencies, signing and affected files before installation. Follow host-specific instructions; never silently accept SDK terms, use `sudo`, install obsolete host runtimes globally or weaken OS/firewall protections. Build in a private isolated workspace outside this skill.
- Create/import a **TV** certificate profile through Samsung's supported Certificate Manager. The user signs in privately. Author keys, `.p12` files, passwords, account tokens and distributor certificates/DUID lists stay outside the repository and public logs. Preserve the existing author certificate for updates. Do not borrow a publisher's private key, forge privileges, or use a third-party login/token capture flow.
- Bind the exact SDB serial and target name to the physical TV and its displayed DUID/unique identity where available. `sdb devices` lists local connections, not unique hardware proof. Never select the first device, a duplicate friendly name, every device or an emulator. Recheck after reconnect, firmware change and before every write. If stable identity is unavailable, stay in device-plan mode rather than inventing an Android serial.
- Developer-mode activation, Host PC IP changes, application-install permission, signing and activation reboot are separate effects. List the needed ones together in the concrete plan and reuse already supplied authorization. Only use the TV's normal Apps developer dialog, not the service/factory menu. Do not toggle developer mode or update/downgrade firmware as a diagnostic shortcut.
- Use a trusted private network with physical TV confirmation. SDB is development access; do not claim an authenticated/encrypted channel simply because it connects, scan the LAN, expose ports, or use another transport to bypass a denial. Host policy still applies. Keep the desktop's existing protections intact.

Local `--help` and source inspection do not need a TV. Before any live command, record the actual installed CLI version and its TV-specific syntax. `sdb -s SERIAL` selects a device; Samsung's TV CLI accepts `-s SERIAL` or `-t TARGET`. Prefer the explicit serial; if using a name, resolve it to one confirmed serial first. The same flag can mean something different in packaging: `tizen package -s PROFILE` selects a signing profile, not a TV.

## Inspect the package offline

Run from the skill root, substituting a private regular file:

```text
python3 scripts/inspect_wgt.py --wgt /private/session/reviewed.wgt
```

Use Python 3.10+ (`python` where that starts Python 3). This standard-library helper reads the ZIP manifest as data; it never extracts, executes, downloads, signs, connects or installs. It reports SHA-256, widget/application/package IDs, version, minimum Tizen, declared privileges, services, network access, settings, metadata and signature **filenames**. It rejects unsafe/duplicate paths, symlinks, encrypted/oversized/unsupported archives, excessive expansion, unsafe XML declarations, ambiguous application entries and missing local entry points. ZIP64, split archives and non-UTF-8 manifests are intentionally unsupported: review such a package separately without disabling the checks.

A successful report is **not approval**. It does not cryptographically verify signatures, audit payload code, determine privilege levels, inspect every ZIP member's CRC or prove compatibility. Keep the report private. Verify the actual author/distributor identity and valid DUID/privilege coverage with Samsung tooling, and compare the exact artifact/source with upstream. A signature filename or a checksum obtained from the same untrusted download is not independent authenticity evidence.

Review source, build scripts and lockfiles, every background service, network URL, privilege and native component. Follow the original license when building; this skill does not redistribute app code or WGTs. Reject unknown app-ID conflicts, system IDs, privileged/native TPK bundles and downloads that silently change between review and installation. Do not use the Android JSON plan guard; it deliberately rejects Tizen.

## Jellyfin: build and connect a media library

Use the [official Jellyfin Tizen project](https://github.com/jellyfin/jellyfin-tizen), not a look-alike download site. First identify the user's existing Jellyfin server version and choose the matching supported Jellyfin Web release. Pin both full commits and their dependencies for the actual build; the wrapper's placeholder `0.1.0` is not the web-client or server version. Do not create/expose a server or import a media library as part of TV installation.

1. Review `package.json`, lockfiles, `gulpfile.babel.js`, `config.xml` and the selected Web release. `npm ci` runs lifecycle code; in the wrapper its postinstall prepares the interface and deletes/rebuilds local `www`. Confirm that this is a disposable build directory, not a user's existing work. Approve required downloads first; never copy shell chains from an unreviewed installer.
2. Build the selected Web release in isolation with its supported Node/runtime and `USE_SYSTEM_FONTS=1` as appropriate; supply that `dist` through `JELLYFIN_WEB_DIR` when preparing the Tizen wrapper. Use the source release's documented build requirements; do not transplant a floating sample branch. On Windows, pass environment variables through the process environment instead of pasting POSIX assignment syntax.
3. Build the Web project with Tizen Studio, package with the selected private TV signing profile, and run the WGT inspector on the **final signed artifact**. Record unsigned-source provenance, signing identity and final hash separately; re-signing changes the bytes.
4. Apply the installation transaction below. The user enters their own server URL/account in the TV app. Use their existing trusted/private HTTPS route; do not disable certificate checks, create public forwarding or publish credentials. A server/login change is not authorization to change other TVs or the server configuration.
5. Check a small representative media sample, audio, subtitles, resume, D-pad/Back/Home and stock apps. Note direct play vs transcoding and codec limitations accurately. Do not promise 4K/HDR/Dolby support from installation success or bypass DRM to fix playback.

If a compatible official store version is available, explain that option before doing build work. Third-party prebuilt Jellyfin WGTs require a separate provenance/build/signature review; they do not become official merely because the wrapper is official.

## Moonlight: turn the TV into a PC streaming client

Use the reviewed [Moonlight Tizen port](https://github.com/OneLiberty/moonlight-chrome-tizen) for a TV/firmware supporting its Samsung WebAssembly/socket APIs. Upstream declares Tizen 5.5+; that minimum alone does not validate every codec, firmware or controller. Confirm the existing host is owned/authorized and running a supported Sunshine/GameStream setup; prefer the user's explicit host address rather than discovering other computers.

- Choose an exact reviewed release/build and inspect `res/config.xml`, source, toolchain and dependencies. If building, record Samsung Emscripten, CMake/Ninja and component revisions. If using a container, pin its digest and review its contents; no privileged container, host root filesystem/keys mount, floating `latest`/nightly or bundled signing identity. Upstream's Dockerfile contains a shared weak signing setup and old build runtimes: do not reuse that key/password or install those runtimes into the host system.
- Sign the reviewed widget through the user's supported TV profile, inspect the final WGT and use the same install transaction. Never apply the README's delete-old-app update recipe automatically; removal and pairing/settings loss require separate informed approval, and an unknown signer mismatch stops the update.
- Pair only the explicit host. The user confirms the PIN on that computer privately; do not expose Sunshine administration, open router ports or enable unattended desktop access. Start with conservative supported resolution/FPS/codec and test one change at a time. Do not toggle TV Game Mode, picture settings or audio output just because the app supports them.
- Test picture/audio, controller latency, exit/Home/Back and return to stock apps. HDR, unsupported codecs, network throughput and TV firmware can affect results; a black screen means stop/recover the last app setting, not reboot/root/patch the TV automatically. Revoke only this session's temporary host pairing if requested.

## One reviewed installation transaction

Prepare a private plan: model/full firmware/physical identity; SDB serial and alias; current developer/Host PC IP baseline; source and final WGT hash; widget ID, application ID and package ID; signer/profile/DUID and privileges; installed-app/version/data baseline; exact effects; finite deadlines; health checks; recovery and data-loss limits; authorization. Show the plan before writes unless that exact scope is already approved. No application install, profile export, reboot, run or uninstall is implied by loading the skill.

1. Establish live identity and inspect existing Apps/Device Manager state. If installed identity/version/signer cannot be established, stop at the update plan. Record any new developer access/install permission before granting it through the supported tool UI. Do not push certificate wildcards to guessed device paths.
2. Journal `pending` before **one** approved install. Use argument arrays and an absolute approved package directory. A TV CLI example is `["tizen", "install", "-s", "SERIAL", "--name", "reviewed.wgt", "--", "/private/session"]`, after checking local help. Never omit target selection or join user labels into shell text. Use an explicit finite host timeout, normally 120 seconds for install and 30 for control/readback; do not change global CLI timeout settings to force it through.
3. Timeout means an unknown outcome. Inspect the exact app state before deciding; no repeated install, alternate installer, uninstall or root workaround. Installer exit success alone is insufficient: verify app ID/version and actual launch on the confirmed TV, then test required functions.
4. Launch separately with `tizen run -s SERIAL -p APPLICATION_ID` where documented. **For Samsung TV, run/uninstall use the application ID, not the package ID**, despite the `--pkgid` name. Use the ID from the inspected final config and the TV, not a marketing label.
5. If the newly added app fails, an approved removal may use `tizen uninstall -s SERIAL -p APPLICATION_ID`, only while identity/version still match the session. Warn that app data/pairing can be lost. Updates can replace/remove the prior version; reinstalling an old WGT does not guarantee data recovery. Never remove stock/pre-existing apps as an error workaround or call uninstall an exact inverse of an update.
6. Reconcile the journal and restore only approved session configuration without overwriting later user changes. A development-mode/Host PC IP restoration can affect other developer tools/apps; inspect and explain before doing it. Retain the author certificate for future updates. Keep unresolved recovery pending; no factory reset, system-package purge, repeated power cycle or firmware flashing.

## Optional TizenBrew route

TizenBrew is a web-app/module host with background service and localhost SDB/debug behavior, not Root or a drop-in replacement for stock Smart Hub. Its reviewed default configuration references a floating TizenTube module, and modules/services can download and run code after package installation. A WGT hash alone therefore does not fix the full execution content.

Only an explicit TizenBrew/module request selects this route. Review the exact module source/version, dynamic resources, services, network origins, auto-launch settings and login effects **before first launch**. Use a reviewed local build/configuration with no unapproved default or auto-launch module; retain the original notices and record the diff. If the host cannot prevent unreviewed dynamic code from starting, prepare a plan rather than run it. Do not silently change the developer Host PC IP to loopback; that is a separate access/configuration change that can stop desktop development access and needs a restoration plan.

The reviewed TizenBrew Installer disables TLS verification process-wide, hosts account-related listeners, stores reusable certificate material and selects latest assets. Do not execute that unmodified installer, enter Samsung credentials into it, or “fix” a denial by switching to it. Use Samsung's official signing/install workflow for reviewed WGTs. USB demo installation is deprecated upstream; do not fall back to random USB packages, native TPKs or exploit installation. New module revisions require new source/effect review; no bulk catalog or arbitrary URL installs.
