# Windows

Use PowerShell; feature-detect with `Get-Command <name> -ErrorAction SilentlyContinue`.
Managed hosts may deny reads; record unavailable. Native output can be localized.

## Baseline

```powershell
Get-NetAdapter
Get-NetIPConfiguration
Get-DnsClientServerAddress
Get-NetIPInterface
Get-NetRoute -DestinationPrefix '0.0.0.0/0'
Get-NetRoute -DestinationPrefix '::/0'
```

Inspects link, addresses, DNS, MTU, and defaults; exposes network identifiers.
`Resolve-DnsName example.com` sends DNS queries. Use `Find-NetRoute -RemoteIPAddress <resolved-IP>`
and `Get-NetRoute -InterfaceIndex <index>` for the actual selected source/next hop.
VPN/policy routing may override defaults; never assume the first adapter is active for this destination.

## Bounded probes

```powershell
ping.exe -4 -n 20 -w 1000 <gateway-IP>
ping.exe -4 -n 20 -w 1000 <target-IP>
Test-NetConnection example.com -Port 443 -InformationLevel Detailed
tracert.exe -4 -d -h 12 -w 1000 <target-IP>
```

Replace placeholders; no literal angle brackets. Ping sends 20 ICMP probes, roughly 20–40 seconds.
TCP connects to one specified port; no scan/application validation. Bound TCP/trace processes externally.
Use `-6` for IPv6. Link-local gateways need the interface scope (for example `%12`).
A 12-hop trace may end before the destination; mark incomplete. `pathping -n` is a later, longer bounded test.

## Conditional inspection

`netsh wlan show interfaces`: signal/channel/rates; redact SSID/BSSID.
`Get-NetAdapterStatistics`: counter deltas, not lifetime totals.
`Get-VpnConnection`: Windows profiles only; third-party tunnels need client/route inspection.
`Get-NetFirewallProfile`, targeted `Get-NetFirewallRule`, `Get-NetQosPolicy`: relevant policy inspection.
Endpoint QoS does not expose router bottleneck queues.
`netsh wlan show wlanreport` writes sensitive files and may require approved elevation; review locally.
Never dump saved Wi-Fi credentials with `key=clear`.

For selective size-dependent hangs: inspect MTU, then bounded IPv4
`ping.exe -4 -n 3 -f -l 1472 <target-IP>` and smaller payloads against the same responsive target.
1472 + 20-byte IPv4 + 8-byte ICMP = 1500 without IP options. Not IPv6/tunnel arithmetic.
Nonresponse alone establishes no MTU ceiling and warrants no arbitrary MTU change.
