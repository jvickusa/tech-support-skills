# Evidence and confidence

Each observation needs ID, window, method, target role, and availability. Preserve partial replies from timeouts.
Missing samples never become zero. Unreachable errors are not echo replies. If localized output cannot be
interpreted, keep raw text and mark derived metrics unavailable. Process status cannot establish packet loss.

| Pattern | Supported possibility | Next discrimination / limitation |
| --- | --- | --- |
| Wi-Fi gateway bad, same device wired clean repeatedly | Local wireless path; high confidence after reproduction | Compare client/location; AP/driver/interference not identified |
| Gateway stable, external RTT rises under wired upload and recovers repeatedly | Queueing beyond LAN; high confidence in mechanism | Exact bottleneck unknown; inspect load/router support |
| Multiple wired devices lose Internet, gateway reachable | WAN/access/path issue; moderate confidence | Request WAN/line/ISP telemetry |
| One service fails, comparable services/devices healthy | Service/path/app issue; moderate confidence | Official status, actual service route/app stats |
| Known-IP works, repeated lookup failure | DNS branch; moderate confidence | Resolver reachability, split DNS/policy, explicit query |
| One trace hop silent, later hops healthy | No forwarding failure established | ICMP treatment; no change justified by that hop |
| No ping replies, HTTPS/app works | ICMP unavailable/filtered | Not 100% application loss |
| Large probes fail, small succeed on same path | Possible size/PMTU behavior | Filtering still possible; correlate application |

High confidence needs repeated controlled comparison excluding credible alternatives for the claimed mechanism.
Moderate supports a boundary but lacks comparison/telemetry. Low is weak/confounded evidence.
Undetermined means insufficient evidence. No confidence level proves a particular faulty device.

Report ICMP sent/reply counts, target/family/window separately from unreachable errors.
ICMP nonresponse is not media/game loss; actual app/TURN results are required.
Ping spread is not standardized RTP jitter. Link rate is not throughput; speed estimates depend on method/path/time.
No hop-level diagnosis or maximum-speed claims. Website edge RTT cannot locate browser overhead.

Escalate ISP cases with repeatable multi-device wired degradation beyond a healthy gateway; request timestamped
WAN/line/modem/ONT errors, provisioning/congestion checks. Service-only problems go to that provider with app stats.
Wired-clean/multi-client wireless problems go to AP/router support. One-device/tunnel/policy cases go to endpoint,
VPN vendor, or managed IT. Explain unknowns, request a ticket, and attach only reviewed evidence.
