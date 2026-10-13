# Game network comparisons

Record game region, in-game RTT/loss, symptom times, wired/Wi-Fi, VPN and relevant load. Choose authorized targets: destination-selected gateway, neutral external endpoint with stated rationale, documented game/service endpoint when available. Multiple interfaces/VPNs need the route selected for the target; do not pick the first default route blindly. No scanning for game servers/ports.

Use bounded installed ping probes (Windows `ping -n 20`, macOS/Linux `ping -c 20`) in comparable symptom/healthy windows; validate target and bound execution time. Compare gateway and external windows, ideally alongside in-game stats. ICMP reply loss is ICMP evidence, not game UDP loss. No replies/errors are unavailable for application loss inference. TCP reachability does not prove UDP session health.

Record sent/replies, RTT sample count, median/p95/max and method when samples exist. A jitter proxy from consecutive successful RTT differences must state its definition; do not bridge missing probes or claim RFC RTP jitter. Summary-only ping output cannot establish sample percentiles.

Routes (`tracert -d`, installed `traceroute -n`/`tracepath`) provide context. Silent/slow intermediate hops can filter/deprioritize ICMP; even downstream degradation does not identify a defective named router. Changing routes/asymmetric paths complicate inference. Compare wired/Wi-Fi, VPN/no-VPN and idle/load only with authorization for disruption and a recovery path for remote sessions.

Gateway degradation raises local-path possibilities; clean gateway plus repeated destination impairment raises wider path/service possibilities. Proxy targets cannot establish game server quality. Clean general checks with one-game failure warrant official service status, region and game-specific investigation. Do not apply DNS/MTU/TCP tweaks to unexplained lag. A site speed test is optional context, not a game-path or synchronized frame capture.

Use `internet-diagnostics` if available for deeper Wi-Fi/DNS/VPN analysis; this guide remains usable independently. Never replace the website's measurement engine or infer TURN packet loss from allocation failure.
