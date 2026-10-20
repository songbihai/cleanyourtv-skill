# Optional network features

Read this only for an explicit request to change the TV's Private DNS or use an already configured private remote route. Apply every common mutation gate, stable hardware identity check, exact-target rule, and journal requirement in SKILL.md. The offline package guard does not validate these operations. Keep networking unchanged for an ordinary cleanup or launcher task.

## Private DNS

1. Confirm Android 9 / SDK 28 or later and inspect support on this firmware. Explain that the resolver receives DNS queries; DNS filtering does not remove every ad or block ads embedded in streaming content. The user must choose the exact provider and resolver hostname. Do not choose a public provider silently.
2. Capture exact global `private_dns_mode` and `private_dns_specifier` values **and key presence** using the procedure in device-workflow.md. A printed `null` is ambiguous. Record current Wi-Fi, existing VPN, ADB route, and a working path to the TV's network settings. Require a person at the TV who can restore settings if the connection fails; otherwise remain in plan mode.
3. Review a plan containing only the required hostname and mode writes, their order, and exact inverses. Validate the hostname as a DNS hostname, with no URI scheme, path, port, credentials, whitespace, or shell syntax. Use argument arrays, never shell interpolation. Android's strict mode value is `hostname`; its resolver key is `private_dns_specifier`. Inspect device help before choosing command syntax.
4. After approval, journal and apply one write at a time. Set the approved resolver before enabling strict mode; read back each exact value before proceeding. On timeout or connection loss, mark the outcome unknown and stop. A separate successful host DNS lookup does not establish the TV's resolver state.
5. Verify TV connectivity, required streaming/DRM, casting, and any existing VPN with the user. If an inverse is needed, restore the recorded mode and specifier, deleting only keys that were absent. Never assume `opportunistic` or another factory default. If the baseline was non-strict, restore that mode before changing the resolver. If it was already strict, explicitly plan a recovery order that avoids an unintended resolver. Do not invent baseline values after a failure.
6. Preserve the journal and report unresolved recovery accurately. Do not modify the host's DNS, router, firewall, VPN, or unrelated TV settings to rescue this feature.

## Existing private remote route

- Use only an existing route that the owner explicitly identifies and authorizes, such as a private Tailscale connection. Creating or sharing a tailnet, changing ACLs, advertising subnet routes, firewall changes, or unattended access is a separate administration task with separate authorization. Never expose or forward ADB on the public Internet.
- Obtain the exact private endpoint and, where applicable, distinct wireless pairing and connection ports from the owner. Do not scan subnets, infer routes, or treat an IP address as hardware identity. mDNS discovery may not cross a private route. Do not downgrade a TLS connection by enabling legacy `adb tcpip 5555`.
- Confirm stable hardware identity, firmware, current user, and session freshness through that exact target. If identity is unavailable, remain read-only. Require an available person at the TV and a physical recovery path before any mutation over a remote route.
- Preserve the Wi-Fi, VPN, Setup Wizard, and network services carrying the connection. A launcher VPN badge is not evidence that traffic uses the expected route. Do not reboot by default or change networking just because a command times out.
- At completion, revoke only temporary access that the user agreed to remove. Do not tear down pre-existing VPNs, routes, or ADB authorizations indiscriminately. Protect endpoints, key material, logs, and device identifiers from issues and release archives.
