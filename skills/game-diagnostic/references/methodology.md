# Reproducible evidence

Record scene, duration, configuration, tool/version, metric definitions, timestamps/time zone, warm-up, AC/battery and relevant background workload. Preserve normal user conditions; do not reboot or clear caches just to manufacture a clean baseline.

Built-in benchmarks take precedence. Otherwise use roughly 60–120 seconds warm-up and 60–120 seconds capture as starting defaults, not validity thresholds. Investigate first-run/shader compilation separately from warm steady-state behavior. For degradation after several minutes, capture until the usual onset within an agreed bounded window; 10–30 minutes is an optional thermal investigation, not a routine stress test. Stop on instability or unsafe thermal behavior.

Repeat matched runs to estimate normal variability. Change one variable for A/B; repeat or use A/B/A when practical. Keep resolution, route, cap, scene, power, cache/warm-up state and instrumentation constant unless that is the tested variable. Live multiplayer results have uncontrolled server/player variance: qualify comparisons.

Prefer per-frame times: count, duration, p50/p95/p99/max milliseconds, average FPS and count over selected budget (`1000 / target FPS` ms). State percentile method (for example nearest-rank) and source column/units. Average FPS from frame intervals is `1000 / mean(interval_ms)`, not mean of per-frame FPS. Do not silently remove hitches, menus or loading frames; document window selection. Sampled overlay logs are not necessarily one row per frame; do not derive per-frame percentiles from interval averages. Define any “1% low” calculation explicitly.

Keep resource samples with their original timing and cadence. Correlation needs repeated co-occurrence and a plausible mechanism; coincidence alone is not causation. CPU aggregate load can hide one busy thread. GPU saturation can be expected. High temperature without clock/throttle evidence does not prove thermal limitation. Memory allocation alone does not prove pressure; disk activity alone does not prove an I/O stall.

Confidence bands describe evidence strength, not probabilities: low (matching pattern, substantial alternatives); moderate (repeated correlation, not isolated); high (independent corroboration plus discriminating A/B); undetermined (insufficient/conflicting evidence). Reserve confirmed mechanism language for repeated controlled removal/reintroduction, never a guessed component. Avoid numeric confidence scores without calibration.

Ledger per observation: ID, exact command/UI action, tool/version, start/end with zone, workload, status, exit code when applicable, artifact path and limitation. Errors/timeouts/cancellation preserve completed observations; stop remaining captures and restore only instrumentation owned by this run. Raw captures stay private; include checksums when preparing a support bundle.
