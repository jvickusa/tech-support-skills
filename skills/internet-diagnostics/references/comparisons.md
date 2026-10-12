# Comparisons and workloads

Record target, protocol/family, connection, VPN, count, timestamp/time zone, workload, and symptom reproduction.
Change one variable. Twenty probes screen a short window, not long-term stability.

## Wi-Fi / Ethernet

Same device, application, destination, and comparable window; get approval before interface switching.
Confirm selected route uses Ethernet. Repeatable Wi-Fi gateway degradation removed by Ethernet supports
a local wireless path issue, not a named AP/driver fault. Compare another device/location, association events,
and counter deltas. PHY rate is not Internet throughput. Suggest placement/cable checks based on evidence.

## Idle / load

First observe the existing troublesome workload. Measure gateway/Internet before, during, and after
separately identified upload/download. Collector commands are sequential, not synchronized time series.
For simultaneous monitoring, use two bounded native ping processes and record their actual windows.
Do not create saturation without agreement on duration, data cost, and household/call disruption.
Prefer the existing workload or an approved service speed test; no unlimited downloads/custom measurement engine.
Record direction, method/provider, and app behavior. Repeat idle after stopping load.

Stable gateway plus repeatable external RTT inflation under load supports queueing beyond the LAN observation
point; exact queue unknown. Gateway ICMP deprioritization can also affect replies.
Reduce competing load first. Router SQM/AQM may help when supported; configuration needs approval.
No fixed bandwidth percentage or endpoint DSCP tweak without device-specific evidence.

## Gaming

Distinguish render/frame stalls from ping spikes, rubber-banding, disconnects, or matchmaking failure.
Record game region and in-app network stats without account IDs. Use authorized actual endpoints when known;
public targets cannot measure the game's exact route. Compare region where practical.
Hosting/matchmaking may involve NAT/firewall. No broad forwarding, DMZ, or unsolicited UPnP enablement.

## Streaming

Record startup, buffering, resolution, service/device/time. Compare same stream wired/wireless and another
service/device. Service-side sustained delivery tests can reveal instability hidden by short speed bursts.
If one provider fails, check official status, DNS/CDN/app behavior. Verify current vendor Mbps requirements.

## Calls

Record who sees/hears degradation and in-app statistics. Broken outgoing audio suggests investigating
upstream; incoming problems suggest downstream, but either may be app/device related.
Compare unloaded and wired calls. Protect meeting links/participant identities; no recordings as baseline.
TCP 443 success cannot validate media UDP, TURN, or WebRTC. Actual relay/media stats are required for media loss;
failed relay establishment means unavailable, never 100% loss.

## Browsing / intermittent

Separate lookup, known-IP reachability, and HTTPS/application behavior. HTTPS by literal IP can fail certificate
validation; do not mistake that for a network fault. Repeat bounded good/bad windows and one reproduction.
Universal latency thresholds do not replace controlled comparison and workload context.
