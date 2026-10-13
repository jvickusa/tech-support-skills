# Symptom decisions

| Symptom/evidence | Candidate | Smallest useful distinction |
| --- | --- | --- |
| Low FPS, GPU near saturation with healthy clocks | GPU throughput limit | Approved lower render-scale A/B; CPU and power context unchanged |
| Low FPS, busy game thread, GPU headroom | CPU/game-thread constraint | Approved CPU-heavy view-distance/crowd/simulation option A/B; total CPU alone is weak evidence |
| Exact stable FPS ceiling | Limiter/VSync/refresh policy | Read game, driver and display cap settings before changes |
| Hitch at first encounter, improves on repeats | Shader compilation/cache or streaming | Compare first and repeated traversal; preserve cache and correlate I/O/CPU |
| Hitch with memory pressure/paging or VRAM eviction | Memory/asset pressure | Correlate pressure and frame spikes; allocation totals alone are insufficient |
| Repeated traversal hitch with elevated I/O latency | Storage/streaming/decompression | Same-route capture; independent CPU/memory evidence; synthetic throughput is not proof |
| Degrades after minutes with falling clocks/throttle flags | Thermal/power limit | Capture through onset; compare same load before/after cooling under comparable power state |
| Rubber-banding with stable local frame timing | Network/server simulation | Gateway/external/service and in-game stats during symptom |
| Crash/black screen | Game, driver, OS or hardware instability | Exact timestamp, game error, bounded OS events, recent version changes; error code does not prove root cause |
| Input delay with stable FPS | Queue, display/input settings or game behavior | Record cap/VSync/VRR/frame generation and supported latency metrics; FPS/RTT cannot establish input-to-photon latency |

For crashes distinguish application exit, GPU/display reset, OS freeze and whole-machine restart. Read relevant game logs first, then OS events near the timestamp. Dumps are sensitive and collection is optional. Known issue/release-note matches need current official sources. No automatic driver reinstall, file verification, repair or cache/config deletion: each changes state and belongs to an approved experiment.
