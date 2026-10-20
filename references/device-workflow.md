# Device connection, evidence, and transactions

## Choose a target and transport

Use only the TV the user identifies and is authorized to administer. Ask for the IP/port shown on that TV rather than scanning a network. `adb devices -l` inventories already connected targets; it is not permission to select one automatically. Explain the TV authorization prompt and let the user accept it physically.

Prefer maintained Android SDK Platform Tools. On supported firmware, use `adb pair HOST:PAIRING_PORT`, entering the code interactively rather than putting it in command history, then `adb connect HOST:CONNECTION_PORT`. The two ports can differ. Do not assume port 5555, enable legacy TCP mode, open firewall ports, or downgrade an encrypted connection merely for convenience. A TV already offering authorized legacy ADB can be used on the user's trusted local network after explaining the exposure; disconnect and disable debugging afterward.

If the host blocks ADB, resolve the stated permission issue with the user. A Python client is not a permission bypass. `tools/tv.py` at the reviewed upstream revision uses legacy TCP ADB and can reuse `~/.android/adbkey` if present, otherwise using `tools/adbkey/`; it is not a replacement for TLS pairing. Do not silently switch transports. If specifically authorized and reviewed, isolate its dependencies in a venv and bind both `TV_HOST` and `TV_PORT` explicitly for every invocation. Never copy host keys into this project or publish either key location. This release's generated command arrays use stock ADB only.

`SERIAL`, `PACKAGE`, and paths in the commands below are placeholders. Substitute validated values using the host's argument handling. Every device command needs `-s SERIAL`. Never concatenate untrusted strings into a shell. Use one remote operation per call, capture stdout/stderr, and bound runtime. Read-only queries normally have a 30-second timeout; an APK install can use a reviewed longer timeout. Investigate a failed read once; do not retry mutations automatically.

## Save a private baseline

Create a new session folder outside this repository, with owner-only access where the host supports it. Preserve timestamp, tool version, upstream commit, target endpoint, stable hardware serial and its property source, and build fingerprint. Check free local space first. Save raw outputs without modifying them. Read only the minimum needed, rather than dumping all properties or logs by default.

```text
adb version
adb devices -l
adb -s SERIAL get-state
adb -s SERIAL shell getprop ro.product.manufacturer
adb -s SERIAL shell getprop ro.product.model
adb -s SERIAL shell getprop ro.product.device
adb -s SERIAL shell getprop ro.serialno
adb -s SERIAL shell getprop ro.boot.serialno
adb -s SERIAL shell getprop ro.build.fingerprint
adb -s SERIAL shell getprop ro.build.version.sdk
adb -s SERIAL shell pm list features
adb -s SERIAL shell am get-current-user
adb -s SERIAL shell pm list users
adb -s SERIAL shell dumpsys device_policy
adb -s SERIAL shell pm list packages --user 0
adb -s SERIAL shell pm list packages -e --user 0
adb -s SERIAL shell pm list packages -d --user 0
adb -s SERIAL shell cmd package resolve-activity --brief --user 0 -a android.intent.action.MAIN -c android.intent.category.HOME
adb -s SERIAL shell cmd package query-activities --brief --user 0 -a android.intent.action.MAIN -c android.intent.category.HOME
adb -s SERIAL shell settings --user 0 get secure default_input_method
adb -s SERIAL shell ime list -s
adb -s SERIAL shell dumpsys package PACKAGE
```

Use a non-placeholder `ro.serialno`, or `ro.boot.serialno` when the former is unavailable. Record the selected property as `device.identity_property` and its exact value as `device.hardware_serial`; re-query that same property before every write and after every reconnect. Ask the user to confirm the physical target during setup. If the identifier is missing, generic, known to be duplicated, or untrustworthy, stop at audit/plan; do not substitute model, IP, Android ID, or fingerprint as proof of physical identity. These checks reduce accidental targeting errors, not malicious device impersonation.

Confirm TV/leanback characteristics and firmware identity, not just the brand. These commands are version-sensitive: check `pm help` / `cmd package help` if syntax is unsupported. If HOME enumeration or package state cannot be obtained unambiguously, stop mutations. A resolver/chooser (`android/...`) is not a proven default Home. Managed/device-owner/work-profile evidence or a current user other than 0 means audit only. Protect every keyboard and HOME package, not only the selected one.

For any APK install/update, require a confirmed single-user device (only owner user 0) as well as the common mutation gate. Updating an APK can affect the shared package code used by other users even when install is requested for user 0. On a multi-user device, keep launcher builds local and report installation unsupported by this release.

For a candidate, inspect the `User 0:` stanza in `dumpsys package` and record its exact integer `enabled=` value. It must be installed, visible/not hidden, not suspended, and effectively enabled (present in the `-e` list). State 0 means manifest default; 1 means explicitly enabled; 2/3/4 are disabled variants. Do not infer state 0 from absence in the disabled list. Keep the raw evidence behind every normalized field. This release only disables baseline states 0 or 1 and restores those exact settings. Component-level changes are outside the guard.

Inspect shared UID, providers, receivers/services, required libraries, permissions, and observed device role. Package names alone do not prove function. Add discovered critical and user-required packages to `protected_packages`. Unresolved dependencies remain untouched. In particular, Setup Wizard may own saved Wi-Fi configuration; disabling it can remove the connection even after setup is complete. Compare upstream examples only for the same model, OS, and firmware, and still validate each package locally.

Before optional settings changes, capture exact namespace, user, key presence, and value. `settings get` returning `null` can be ambiguous: use a targeted review of `settings --user 0 list NAMESPACE` to distinguish an absent key from a literal string. Store outputs locally; they can contain identifiers or secrets. Do not export full settings to an issue.

## Functional evidence

Record whether baseline Home, Settings, D-pad/Back, physical input button, HDMI/tuner, keyboard, Bluetooth remote, network, and required streaming/DRM/casting/voice functions work. Some checks need the user's eyes or remote. A screenshot does not prove audio, DRM playback, physical buttons, or network stability.

For a local screenshot use the host's binary-safe subprocess capture of:

```text
adb -s SERIAL exec-out screencap -p
```

Write stdout directly as bytes to a private PNG and inspect it. Do not use text-mode PowerShell redirection for binary images. If no image tool is available, ask for user verification and mark visual inspection unperformed. A blank frame on protected content or an input source is not evidence that Home works; navigate to Home only when within the authorized interaction scope. Screenshots can expose accounts and viewing history.

## Journal and interrupted sessions

Before a mutation, append a JSON line with sequence, timestamp, target identity, plan digest, package, original enabled setting, forward argv, inverse argv, and `pending` status. Append later outcome lines rather than rewriting history. Record actual observations, not expected success. Save and flush the pending record before issuing the command; if that fails, do not execute.

After a timeout, crash, or disconnect, reconnect only to the same confirmed device. Re-read hardware serial from its recorded property, fingerprint, current user, state, and health before deciding whether an operation completed. Do not replay the plan. If the state is already 3 and the journal proves a pending disable from 0/1, verify or recover; if state conflicts with the journal, stop and investigate. Rollback only session changes in reverse order, with a readback after each. Do not overwrite a later user change.
