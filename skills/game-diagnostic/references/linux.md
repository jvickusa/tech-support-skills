# Linux observations

Use installed `cat /etc/os-release`, `uname -rmo`, `lscpu`, `free -h`, `df -hT`, and `lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS` as relevant. Read GPU driver with `lspci -nnk` if installed; record Proton/Wine/runtime version and launch options for translated games. Paths and hardware identifiers stay local.

Use bounded `vmstat 1 10` and installed `iostat -xz 1 30` for pressure/I/O around reproduction. First rows may summarize since boot; do not treat them as the current window. Process `%CPU` may describe lifetime averages; use interval sampling. Read only relevant `hwmon` sensors, their labels and units. `temp*_input` usually uses millidegrees Celsius; sensor identity is driver-specific. CPU policy frequency may differ from instantaneous hardware clock.

If MangoHud is installed and compatible with the game/anti-cheat, inspect that version's help/config. Prefer a temporary per-launch configuration and a user-owned output directory with bounded `log_duration`; record configuration and remove only this run's launch wrapper after capture. Persistent Steam launch-option edits need change authorization and saved originals. Never trigger upload hotkeys/options. Do not assume `upload_logs=0` is supported: verify actual installed upload controls. MangoHud interval logs may aggregate frames; do not label their percentiles per-frame p99 without confirming granularity.

Use NVIDIA read queries only when supported; installed `sensors` is optional. Do not write CPU governors, GPU clocks/power limits or kernel parameters. Read bounded `journalctl --since ... --until ...` for the game or relevant kernel reset; journal permission failures mean unavailable. No package installs or sudo fallback without authorization.

Sources: [MangoHud configuration/logging](https://github.com/flightlessmango/MangoHud), [CPU frequency](https://docs.kernel.org/admin-guide/pm/cpufreq.html), [hwmon units](https://docs.kernel.org/hwmon/sysfs-interface.html). Consult installed tool docs for model/version differences.
