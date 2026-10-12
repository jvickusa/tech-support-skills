# macOS

Detect with `command -v <name>`; verify release-sensitive flags in local man pages.
`sw_vers` identifies version. No deprecated private `airport` binary dependency.

## Baseline

```sh
ifconfig
networksetup -listallhardwareports
scutil --dns
netstat -rn
route -n get default
scutil --nc list
```

Inspects link/MTU, hardware mappings, resolvers, routes, system VPNs. Output exposes network identifiers.
Third-party VPNs may be absent from `scutil --nc list`.
Resolve with `dscacheutil -q host -a name example.com`, then `route -n get <resolved-IP>` for selected path.
Check local `route` family flags for IPv6. Do not assume `en0` or a service named `Wi-Fi`.

## Bounded probes

```sh
ping -c 20 -W 1000 <gateway-IPv4>
ping -c 20 -W 1000 <target-IPv4>
curl -I --connect-timeout 5 --max-time 10 https://example.com/
traceroute -n -m 12 -w 1 <target-IPv4>
```

Ping sends 20 probes; macOS `-W` uses milliseconds, unlike Linux.
IPv6 uses `ping6 -c 20` and optional `traceroute6`; bound processes externally.
Link-local IPv6 needs interface scope (`%en0`, for example). Traces may need privileges; no automatic elevation.
Curl sends HTTPS HEAD; 405 may mean unsupported HEAD, not failed connectivity.
Separate certificate/HTTP errors from transport errors; never disable TLS verification as a fix.

## Conditional branches

For Wi-Fi, guide Apple Wireless Diagnostics (Option-click Wi-Fi menu). Analysis does not change settings;
its archive is sensitive. Review locally. PHY rate is not Internet throughput.
`networkQuality -h` describes Apple's capacity/responsiveness tool if installed.
Running it can saturate the connection and use substantial data; require approval and bounded duration.
Its responsiveness metric is not ICMP RTT or interchangeable with website metrics.

Inspect selected MTU with `ifconfig <interface>`. For size-dependent hangs consult local `man ping`
before DF/payload experiments; no universal flag recipe or IPv6 shortcut.
Inspect application-firewall settings first; PF reads may require approved elevation.
Never disable firewall/flush rules. Router settings require a separate approved change.
