# macOS observations

Start with `sw_vers`, `uname -m`, relevant `system_profiler SPDisplaysDataType` fields, `vm_stat`, and `df -h` for the game's volume. `system_profiler SPHardwareDataType` can expose serial numbers/UUIDs; select model/chip/memory fields locally rather than copying full output into a shareable report.

Prefer the game's built-in benchmark/counter. For supported Metal apps, Apple's Metal Performance HUD and Instruments Metal System Trace provide more detail. Check macOS/game/launcher support first. A direct temporary launch with `MTL_HUD_ENABLED=1` is an instrumentation change: explain/authorize it and avoid persistent global environment settings. Inspect current HUD logging/report support rather than assuming all OS versions export identical fields. Translation layers and non-Metal games need explicit compatibility checks.

Use Activity Monitor or bounded `top -l 2 -o cpu` observations for competing load. `vm_stat` cumulative paging counters require time deltas, not a single total. Confirm timestamp alignment with frame captures; live overlay readings alone do not provide per-frame distributions.

For power/thermal escalation, read local `man powermetrics`, select supported samplers, and obtain missing elevation approval before a bounded `sudo powermetrics -i 1000 -n 30`. Telemetry varies by hardware. High thermal pressure plus declining performance is stronger evidence than an isolated temperature.

Crashes: known game logs and Console, or a narrow `log show` interval with the verified game process predicate. Bound output and keep raw reports/dumps local. No global log collection or `pmset` modification during diagnosis.

Sources: [Metal performance monitoring](https://developer.apple.com/documentation/xcode/monitoring-your-metal-apps-graphics-performance), [Metal HUD](https://developer.apple.com/videos/play/tech-talks/110339/). Verify installed support; no mandatory developer tools installation.
