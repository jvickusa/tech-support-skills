# Evidence-backed actions

| Finding | Candidate experiment | Tradeoff / rollback |
| --- | --- | --- |
| GPU throughput constraint | One render-scale, ray-tracing or GPU-heavy setting reduction | Image quality; restore exact original value |
| CPU/game-thread constraint | One supported crowd/simulation/view-distance setting | World detail; restore value; lowering resolution may not help |
| Unstable pacing above sustainable rate | Supported game FPS cap | Peak FPS/latency; save original cap; check VRR/display range |
| VRAM pressure with correlated stalls | One texture-quality reduction | Detail; confirm actual pressure and repeat scene |
| Competing workload correlates with stalls | User saves work, then pauses/closes identified app through its supported UI | Lost work/session risk; restarting may not restore session, disclose first |
| Demonstrated power-policy limitation | Supported available power mode A/B | Heat/battery; save exact prior mode, monitor throttling |
| Known version regression | Official game/OEM/vendor-supported rollback/update | Restart/compatibility; verify release notes, recovery and rollback availability |
| Storage contention or game file errors | Pause known workload or supported launcher move/verification | Time/I/O, file replacement; back up relevant saves/config; verification is a mutation |
| Local wireless/path impairment | Ethernet/location or authorized VPN comparison | Connectivity/remote access; preserve recovery path and prior connection |
| External/game-region impairment | Documented region selection or evidence handoff | Matchmaking/ping tradeoff; no local tweak fixes an ISP route |

Frame generation/upscaling may change visual quality, latency and displayed FPS; report these separately. No universal “best” VSync/VRR/driver settings. Do not disable all overlays: test only an identified compatible candidate. Cooling/power evidence supports practical supported cooling/AC checks, not undocumented fan/clock controls or automatic hardware disassembly.

Windows power plan: read `powercfg /getactivescheme` and `/list`; if evidence justifies and approval covers it, use `/setactive` with an existing selected GUID. Rollback uses saved original GUID. Never assume High Performance helps a thermally constrained laptop.

Linux: if installed, read `powerprofilesctl get` and `list`. Test only an available supported profile, then restore the saved profile. Do not write governor/sysfs/kernel settings. macOS: use supported System Settings energy mode when available; no undocumented `pmset` recipe. Check platform/OEM support rather than installing tools automatically.

Network changes require a specific diagnosed mechanism. DNS flush/change cannot lower established-session RTT or raise FPS. Avoid generic IPv6/MTU/TCP tuning, port forwarding, interface resets and firewall changes. Official documented game port requirements do not authorize exposing arbitrary ports. Physical connection/VPN comparisons need approval when they disconnect a remote session.

Outside this skill: registry/timer packs, HPET/`bcdedit` tricks, security/anti-cheat disabling, service/Update debloating, realtime priorities, raw disk repair, BIOS/firmware flashing, overclock/undervolt and driver-cleaner utilities. Do not delete shader caches/config/save directories as routine optimization. A game-specific repair needs evidence, backup and explicit scope; hand off risky recovery work.
