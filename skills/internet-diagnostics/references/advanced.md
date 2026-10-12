# Advanced investigations

Load only the relevant branch after simpler comparisons.

## DNS / families

Inspect configured system resolvers and actual service lookup. Known-IP reachability plus repeated lookup
failure supports a DNS branch, not a proven faulty resolver. Compare an approved explicit alternate query
without changing system DNS; split/private DNS may be intentional.
Record A/AAAA selection. Compare the same dual-stack service over IPv4/IPv6 via native probes or curl family flags.
Unavailable subscription support differs from broken configured IPv6. Never routinely disable IPv6.

## VPN / routing

Inspect selected route/source, tunnel, DNS and MTU for the same target.
VPN off/on requires approval: explain public traffic exposure, private access loss, and remote-session impact.
Skip when policy requires VPN; do not bypass employer controls. Restore and verify connection after the test.
Improvement narrows the tunnel/path branch, not its root cause.
Bound numeric route traces. Intermediate nonresponse/isolated loss is not forwarding-loss proof.
Even persistent destination degradation cannot identify a faulty hop: return paths/ICMP treatment differ.
Corroborate with repeated destination/application evidence and provider telemetry.

## PMTU

Size-dependent stalls/tunnels/large-transfer anomalies justify OS-specific MTU and bounded DF/tracepath tests.
Vary payload against the same responsive destination/path/family. Success establishes only that probe's success;
failure may be filtering. IPv4 ICMP usually adds 28 bytes without options; IPv6/tunnels differ.
No universal optimum MTU. Changes need exact saved interface/family/value and approved recovery plan.

## Policy / NAT

Inspect relevant firewall rules, security client status, and QoS. Empty native VPN lists do not exclude tunnels;
native firewall settings do not describe all filters. NAT labels are vendor-specific. Correlate actual app error
and vendor docs. No scans, DMZ, filter disabling, or blanket port forwarding.
Narrow exceptions need evidence, approval, saved state, and exact removal instructions.

## Capture

Prefer in-app statistics. Necessary captures require consent covering interface/filter, duration, sensitivity,
local storage, cleanup and elevation. Use narrow bounded capture; avoid payloads where possible.
No automatic upload. Encrypted behavior remains unknown; never invent decrypted evidence.
