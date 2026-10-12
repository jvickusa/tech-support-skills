# TURN and WebRTC investigation

Use for calls/media or game features using WebRTC, relay establishment errors, or app reports of blocked UDP.
Ordinary ping, TCP 443, and speed tests do not validate ICE negotiation or TURN media delivery.
Start with the application's own connection statistics and error timestamps. Avoid participant names/meeting URLs.

## Distinguish stages

| Observation | What it establishes | What remains unknown |
| --- | --- | --- |
| Host or server-reflexive ICE candidate | Local/STUN candidate gathering | TURN allocation or relay delivery |
| Relay candidate gathered | TURN allocation succeeded for that configured URL/browser/path | Selected relay pair, peer connectivity, media quality |
| Selected candidate pair includes relay and is connected | That session uses a relay path | Sustained media delivery and other relay transports |
| Media statistics from a connected relay session | Actual observed media counters for that session | Cause/location of degradation |
| Credential/authentication, allocation, ICE, TLS or relay failure | That stage is unavailable/failed | Never evidence of 100% packet loss |

Inspect the selected candidate pair through app diagnostics or browser WebRTC internals.
Candidate gathering alone does not prove the relay was selected. Browser dumps expose addresses, SDP,
session IDs and possibly sensitive server information; inspect locally and summarize allowlisted fields.

## Optional local allocation probe

`scripts/turn-probe.html` uses native browser ICE with `iceTransportPolicy: relay` and one user-selected TURN URL.
It performs allocation only; no microphone, camera, packet-loss estimate, speed test or custom measurement engine.
It closes its peer connection on success, failure, timeout (15 seconds), cancellation and page exit.
Output contains only stage/status, elapsed time, relay-candidate count, and numeric ICE error codes.
No credentials, addresses, SDP, or raw browser error messages are rendered or exported.

Serve only the script directory on localhost:

```sh
python -m http.server 8765 --bind 127.0.0.1 --directory skills/internet-diagnostics/scripts
```

Open `http://127.0.0.1:8765/turn-probe.html` in the user's browser on Windows, macOS or Linux.
Explain that Start sends a bounded allocation request to the entered server. User enters short-lived credentials
directly in the local form after approving the test. Never request secrets in chat, CLI args, URLs, committed files
or browser automation calls. The server receives the normal TURN authentication exchange.
Fields clear immediately when the probe starts. No persistence, external assets, uploads, logs or analytics.
Close the local server after use. Do not serve a directory containing other private files on a network interface.

Use an authorized, currently supported relay and current temporary credentials from its operator.
No default or deprecated public relay. Long-term provider/API signing keys belong server-side, never in this form.
Test one configured URL/transport at a time (`turn:host:port?transport=udp`, `turn:host:port?transport=tcp`,
or provider-supported `turns:`). Unsupported transport/browser configurations remain unavailable.
Do not assume the relay transport equals the candidate's protocol or that TCP/UDP routes are identical.

## Application delivery and loss

After allocation succeeds, reproduce an actual call with consent and inspect its selected pair.
Record whether relay is selected, configured transport, session/window and in-app RTT/jitter/loss method.
For RTP counters, compare matching stream IDs across a bounded window; counter resets/stream switches invalidate deltas.
Do not subtract unrelated snapshots or equate retransmissions/data-channel reliability with RTP loss.
If counters or selected relay are absent, report media/relay loss unavailable. Preserve valid partial observations.
No fixed media thresholds; verify current app requirements.

Compare existing Wi-Fi/wired or approved VPN on/off paths using the same app/relay configuration.
A transport-specific failure supports a policy/path possibility, not proof of an ISP or firewall fault.
Expired credentials, browser restrictions, DNS/TLS, server policy/quota, captive portals and NAT are alternatives.
Do not open broad ports, disable filtering or change VPN policy automatically.
Report the exact stage, browser/OS, timestamps, redacted error codes, observations and requested provider/IT check.
