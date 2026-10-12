# Tech Support Skills

Portable, evidence-based troubleshooting skills. MIT licensed. First skill:
**internet-diagnostics** for gaming lag, streaming buffering, broken calls, and poor browsing despite good speeds.

Uses the [Agent Skills specification](https://agentskills.io/specification). Each folder under `skills/`
is independently installable. No agent-specific APIs, accounts, telemetry, or automatic system changes.

## Installation

```sh
git clone https://github.com/jvickusa/tech-support-skills.git
cd tech-support-skills
```

Copy the whole `skills/internet-diagnostics` directory, including scripts and references.
Review existing installations before replacing them.

| Agent | Personal directory | Project directory | Invoke |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` | `$internet-diagnostics` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | `/internet-diagnostics` |
| Other compatible agents | Agent's documented skill directory | Agent's documented skill directory | Natural-language request or agent command |

macOS/Linux, personal Codex installation:

```sh
mkdir -p ~/.agents/skills
cp -R skills/internet-diagnostics ~/.agents/skills/
```

Windows PowerShell, personal Codex installation:

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills" | Out-Null
Copy-Item -Recurse skills/internet-diagnostics "$HOME/.agents/skills/"
```

For Claude Code replace `.agents` with `.claude`. Refresh/restart the agent if needed.
See [Codex docs](https://developers.openai.com/codex/skills) and
[Claude Code docs](https://code.claude.com/docs/en/skills) for discovery details.
Native command references work without Python. Optional collector requires Python 3.10+.
Windows can use `py -3`; macOS/Linux can use `python3`.

## Use

Ask: “Use internet-diagnostics. My game lags when someone uploads, but my speed test looks good.”
The agent scopes symptoms, detects the OS, explains commands, compares evidence, and produces a report.
Beginners receive one short test at a time. Advanced users can request command batches and JSON.

```sh
python skills/internet-diagnostics/scripts/collect.py --dry-run
python skills/internet-diagnostics/scripts/collect.py --wifi --vpn --dry-run
python skills/internet-diagnostics/scripts/collect.py --format markdown > baseline.md
python skills/internet-diagnostics/scripts/collect.py --gateway 192.168.1.1 --target example.com --count 20 > evidence.json
```

Baseline sends no deliberate probes. Target/gateway options add bounded network probes.
Select the gateway for the target route, not an assumed address. `example.com` illustrates syntax;
choose a relevant authorized destination. No scanning or bandwidth saturation.
`--trace` adds a bounded trace; `--family 6` selects IPv6 probes.
`--dry-run` prints commands without executing them.
Shell redirection creates files: choose private storage and avoid overwriting evidence.
**Output is sensitive and unredacted.** Review names, addresses, routes, and Wi-Fi details before sharing.
Nothing uploads. Collector JSON is local evidence, not a confirmed diagnosis or public share payload.

Wi-Fi and VPN have dedicated workflows and optional `--wifi`/`--vpn` inspection profiles.
These use current/cached state without active scans, secret collection, or VPN disconnection.
The [TURN guide](skills/internet-diagnostics/references/turn.md) includes a local browser allocation probe,
using temporary credentials entered locally and relay-only ICE. It closes after at most 15 seconds.
It tests allocation only; call quality/loss needs actual connected application statistics.
No default/deprecated public relay, long-term keys, or new bandwidth/packet-loss engine.

## Development

```sh
python -m unittest discover -s tests -v
node --test tests/turn-probe.test.mjs
python skills/internet-diagnostics/scripts/collect.py --dry-run --target example.com
```

CI tests Windows, macOS, and Linux. Tests simulate missing tools, failures, partial output, invalid inputs,
platform plans, allocation results, cancellation and timeout. Node 22+ is only needed for JS development tests;
users need an ordinary WebRTC browser for the optional TURN probe.
See [validation](docs/validation.md) for actual-host limits and manual scenarios.
Optionally install upstream [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref)
and run `skills-ref validate skills/internet-diagnostics`.

See [design](docs/design.md) for architecture and provenance. Add skills only for distinct demonstrated needs.
Keep helpers beside their skill; avoid a framework until shared behavior exists.
