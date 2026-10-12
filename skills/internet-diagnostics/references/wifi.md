# Wi-Fi investigation

Use when wireless connections lag, buffer, disconnect, or differ from wired clients.
Start with symptom scope, location/distance, affected clients, band if known, mesh/repeater use,
and whether the problem correlates with movement or household load. Do not request Wi-Fi passwords.

## Read-only evidence

Preview `scripts/collect.py --wifi --dry-run`, explain sensitive identifiers, then collect locally.
Windows reads current association and adapter counters. macOS reads AirPort inventory.
Linux reads cached NetworkManager scan data and wireless interface inventory; no active rescan.
Each inspection has a 15-second deadline. Missing tools, location restrictions, denied access,
and timeout remain unavailable; do not grant location permissions or elevate automatically.

For Linux current association use `iw dev <selected-interface> link` after identifying the route/interface.
On macOS use Wireless Diagnostics for disconnect/radio evidence when inventory is insufficient.
On Windows `netsh wlan show interfaces` may need OS location permission; offer manual Wi-Fi settings
instead of silently changing permissions. WLAN reports are optional sensitive generated files.
Read only the user's OS reference for exact commands.

Record association state, band/channel, signal, negotiated link rate, disconnect events, and counter deltas
where available. Signal percentage is tool-specific; never convert it to dBm with a universal formula.
Lifetime error counters, neighbor counts, and a busy channel alone do not establish the current problem.
Link rate does not equal application throughput. Cached scan output may be stale.

## Isolate

1. Probe the selected gateway and relevant Internet target during a reproduced symptom.
2. With approval, compare the same device/workload on Ethernet; confirm the route changed.
3. If wired is clean, compare a second Wi-Fi device at the same location and the same device near the AP.
4. Repeat the affected window; capture current association again if the client roamed between mesh nodes.

Do not run active scans while judging latency. Mesh backhaul, client radio/driver, interference,
AP load, power saving, and placement remain alternatives. A clean gateway test alone does not prove Wi-Fi healthy.
Do not diagnose a faulty AP from one intermediate response or a single signal reading.

## Recommend and report

Placement or Ethernet can be useful evidence-backed options. Channel/band, driver, power-saving,
mesh/router, or roaming changes require an exact approved proposal and rollback.
Never disable security or prescribe a universal channel/width. Ask vendor guidance for that hardware/region.
Report the controlled difference, observed association, unavailable fields, confidence, and next comparison.
Redact SSIDs/BSSIDs/MACs, neighboring networks, and location clues before sharing.
