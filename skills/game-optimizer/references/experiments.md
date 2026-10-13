# Controlled experiment

Scope game/version, OS/driver/hardware, target FPS/quality/latency, AC/battery, scene/save, resolution/render scale, refresh/cap/VSync/VRR, ray tracing/upscaling/frame generation, power state and relevant background work. If no findings exist, begin read-only: reproduce and identify plausible CPU/GPU, memory/I/O, thermal/power or network mechanism. Do not tweak every category.

Use a built-in benchmark or identical route/replay. Optional starting window: 60–120 seconds warm-up and 60–120 seconds capture; cold-start/shader or degradation symptoms require separate matched windows. Agree on extended tests. Preserve normal conditions. Repeat baseline to estimate noise, test one variable, and repeat/A/B/A when useful. Multiplayer variance, changed patches, caches, background load or different capture tools can invalidate comparison.

Compare the same metric definitions: frame-time p50/p95/p99/max, average FPS, over-budget count, sample count/duration, plus relevant quality/latency/power signals. Define percentiles and units. Per-frame intervals and overlay interval averages are different; generated/displayed frames are different from rendered frames. FPS is not input latency. Align timestamps before claiming coincidence; otherwise compare windows. Unavailable sensors remain unavailable.

Before action, record: finding/evidence IDs, current state, exact command/UI action, backup path if needed, expected signal, acceptable tradeoff, risk, approval scope (including rollback), test, rollback, after state, measured effect and final state. No automatic change executor or generic snapshot can safely restore arbitrary OS/game state.

Prefer temporary game-local tests. Do not bundle preset, cap and power changes. If a setting requires restart, keep restart/warm-up conditions comparable and obtain any missing disruption approval. On failure/cancellation, stop capture, retain useful evidence and restore this experiment's changes if authorized. Do not terminate unrelated recording sessions or delete unrelated files. A driver/OS update may not have reliable rollback: disclose that and use a recovery plan, never promise reversibility.

Stop once objective is met, available evidence is exhausted or recovery is unresolved. Report neutral/uncertain outcomes plainly; normal variation is not an improvement.
