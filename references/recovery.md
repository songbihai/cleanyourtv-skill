# Recover from an interrupted or unhealthy session

For LG webOS, use the recovery section in [webos.md](webos.md); the ADB/package steps below are Android-only. SlopBro research performs no device changes and supplies no root rollback.

Stop forward work at the first failed health check. Use the saved local journal and confirmed identity, not a remembered upstream example list. Never broadcast a restore to all ADB devices. If the original plan explicitly included automatic rollback on a failed check, its scoped inverse is authorized; otherwise obtain authorization for the concrete recovery action. Host permissions still apply.

A failed or unresolved Home check can be the damage recovery is intended to repair. It blocks new forward changes, but does not block a specifically authorized inverse of a matching journaled change when hardware identity, user/policy, and actual changed state are confirmed. Do not require Home to be healthy before restoring it. If identity or actual state cannot be established, stop device writes and use the physical/vendor path.

## Reachable device

1. Apply the common mutation gate. Reconfirm the target endpoint, stable hardware serial from its recorded property, fingerprint, current user, management state, and current state. Distinguish an unknown command outcome from a confirmed change.
2. For a package this session changed from state 0 to state 3, restore with `pm default-state --user 0 PACKAGE`. For a change from 1 to 3, use `pm enable --user 0 PACKAGE`. Check local `pm help` beforehand and read back the per-user state afterward. A generic `enable` does not reproduce state 0. Run it only for the confirmed matching journal entry, using `adb -s SERIAL shell` and one remote operation per call. If current state no longer matches this session's expected state, investigate drift before overwriting it.
3. Restore only attempted/confirmed session changes in reverse order. Never re-enable every package that was already disabled before the session. Do not apply a complete report if only one action ran.
4. If Home selection changed, restore the exact previously recorded component and verify actual HOME resolution and the physical button. This skill never disables stock Home, so the stock candidate should remain available. If it is unexpectedly disabled, treat that as drift; inspect and review a concrete repair rather than guessing a package.
5. Restore changed settings to their recorded values or delete a key only when the baseline proves it was absent. Restore prior theme files or their documented absence. Do not run upstream `restore.sh`/`.ps1` as an exact-state rollback: they also select a stock launcher and reset animation values, and do not reverse every optional change.
6. Repeat the affected functional checks and record what recovered and what remains unverified. App data, running processes, firmware, and every side effect are not restored by an enabled-state inverse.

## Unreachable device

Do not continue issuing commands or change the host firewall. Ask the user to use the physical remote and Settings to re-enable the last changed app or select the original Home if accessible. Use a previously prepared, model-specific vendor recovery guide if necessary. Avoid repeated forced power cycles. Do not recommend or initiate a factory reset as a routine rollback; it destroys data and is outside this skill. Escalate to the device manufacturer's support when the documented recovery path is unavailable.

Recovery is complete only when device health has been observed again. Record `recovery pending` if the TV remains unreachable. Keep debugging enabled only as long as needed for recovery, on a trusted local network; afterward let the user disable it and revoke temporary trust. Do not delete the private session evidence before the user has retained a usable recovery record.
