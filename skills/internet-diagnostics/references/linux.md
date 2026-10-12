# Linux

Detect with `command -v <name>`. Linux does not imply NetworkManager/systemd-resolved.
No automatic package installs or elevation. Record unavailable tools; offer existing alternatives.

## Baseline

```sh
ip -brief address
ip -s link
ip route show
ip -6 route show
resolvectl status
nmcli device status
nmcli connection show --active
```

Inspects links, counters, routes, resolvers, connections. Run only installed tools.
If `ip` is absent, `ifconfig`/`netstat -rn` may exist. If `resolvectl` is absent, inspect `/etc/resolv.conf`
locally; it can identify only a stub. `getent ahosts example.com` uses system name service;
`resolvectl query example.com` is an alternative. Use `ip route get <IPv4>` or `ip -6 route get <IPv6>`
for selected path. Policy routing/VPNs may override defaults; direct paths may lack a pingable gateway.

## Bounded probes

```sh
ping -4 -c 20 -W 1 <gateway-IP>
ping -4 -c 20 -W 1 <target-IP>
curl -I --connect-timeout 5 --max-time 10 https://example.com/
tracepath -n <target-IP>
```

Linux iputils `-W` uses seconds; BusyBox/other implementations may differ. Check local help.
Use `ping -6` for IPv6; link-local gateways need interface scope (`%wlan0`).
Bound tracepath externally; it discovers PMTU without root. Alternative:
`traceroute -n -m 12 -w 1 <target-IP>` (`-6` if supported).
Container/capability policy may deny ICMP. TCP success does not validate UDP.
Separate curl certificate/HTTP status from transport failures.

## Conditional inspection

`iw dev <interface> link`: current association. `nmcli device wifi list --rescan no`: cached scan;
includes neighboring identifiers. No active scans in baseline; never `nmcli --show-secrets`.
`tc qdisc show dev <interface>`: endpoint queues, not necessarily WAN queues.
Approved elevated `nft list ruleset`: inspect filters; never flush rules.
No VPN configuration/private-key dumps; status and routes often suffice.

Selective hangs only: `tracepath -n` then bounded IPv4 `ping -4 -c 3 -M do -s 1472 <target-IP>`
and smaller payloads. 1472 represents 1500-byte IPv4 ICMP without options, not IPv6/tunnels.
Filtered/nonresponding probes alone prove no PMTU fault.
