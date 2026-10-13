# Windows observations

Use PowerShell with native read-only queries; choose relevant fields, not a full machine dump:

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber,TotalVisibleMemorySize,FreePhysicalMemory
Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors
Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion,DriverDate
Get-Volume | Select-Object DriveLetter,SizeRemaining,Size,HealthStatus
powercfg /getactivescheme
```

`Win32_VideoController.AdapterRAM` is not reliable modern VRAM capacity. Task Manager/Resource Monitor and supported vendor telemetry can provide live observations. `Get-Process.CPU` is cumulative CPU seconds, not current utilization; compare deltas over a measured interval or use live counters. Counter names can be localized.

Prefer built-in game benchmarks. If PresentMon is already installed, inspect its executable/version and `--help`; console and capture GUI releases differ. Select the actual game PID/process and a bounded capture. Confirm frame-time column meaning and units from that version's docs; don't combine multiple processes/swap chains or treat CPU/GPU duration as display interval. Captures may require elevated tracing access: ask only when authorization is missing.

For NVIDIA, feature-detect `nvidia-smi`; `--help-query-gpu` lists supported query fields. Read temperature, clocks, utilization, power and clock-event reasons where supported; unavailable fields stay unavailable. Never use reset, power-limit or clock modification options.

Crashes: query Application/System with `Get-WinEvent -FilterHashtable` using narrow StartTime/EndTime around the incident and bounded output. Display reset events corroborate a reset, not defective hardware. Avoid unrelated logs and dumps.

Escalate to WPR/WPA only when ordinary capture leaves scheduler/I/O/driver contention unresolved. Inspect installed profiles and existing recording status first; do not stop another recording. Agree on privilege, duration and potentially large sensitive ETL file before start. Stop/save only this session's capture; preserve partial evidence on cancellation. Do not run boot tracing or deep tracing by default.

Sources: [PresentMon console](https://github.com/GameTechDev/PresentMon/tree/main/PresentMon), [Microsoft WPR](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder), [NVIDIA SMI](https://docs.nvidia.com/deploy/nvidia-smi/index.html). Read installed help/current sources before selecting capture flags.
