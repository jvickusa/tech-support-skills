# Tech Support Skills

Troubleshooting skills for AI agents, from [whyismyinternetcrap.com](https://whyismyinternetcrap.com).
Use them to investigate connection problems, diagnose game performance, and test evidence-backed optimizations.

The website checks your connection from the browser. These skills help a compatible agent investigate
your device, game and network, explain the evidence, and recommend the next step. You can use them independently
or give your agent a result from the site. Results are not imported or uploaded automatically.

## Installation

With [Node.js](https://nodejs.org/) (including npm/npx) and [Git](https://git-scm.com/) installed, run:

```sh
npx skills add jvickusa/tech-support-skills
```

The [Skills CLI](https://github.com/vercel-labs/skills) discovers all three skills and installs your selection
for your selected agent. Follow any selection and confirmation prompts. Supported agents include Codex
and Claude Code. By default, installation is scoped to the current project folder.

To make it available across your projects:

```sh
npx skills add jvickusa/tech-support-skills --global
```

To select this skill and specific agents explicitly:

```sh
npx skills add jvickusa/tech-support-skills --skill internet-diagnostics --agent codex claude-code
```

Replace `internet-diagnostics` with `game-diagnostic` or `game-optimizer` to select a gaming skill.

No Node.js or Git? Use [manual installation](docs/installation.md).
**Python is not required for guided troubleshooting.** The agent can use commands already available
on Windows, macOS, or Linux. The optional Python collector batches those checks into a report.

## Use

Open your agent in the folder where you installed the skill and ask:

> Use internet-diagnostics. My game lags when someone uploads, but my speed test looks good.
> I'm not technical—explain each test and guide me one step at a time.

You can also invoke `$internet-diagnostics` in Codex or `/internet-diagnostics` in Claude Code.
Refresh or restart your agent if the skill does not appear.

The agent asks about your symptoms, selects checks for your operating system, compares results,
and writes a troubleshooting report. It distinguishes observed problems from possible causes,
including what remains unknown. You do not need coding experience to follow its guidance.

Ask for **Markdown**, **HTML**, or **both**. Reports use adaptable templates; the agent chooses content
based on your investigation. The HTML report matches the site's visual style and opens offline directly
in a browser, without Python, Node.js or a server. Use the browser's Print / Save as PDF if needed.
See [fictional Markdown preview](skills/internet-diagnostics/assets/report-example.md) or download and open
the [standalone HTML preview](skills/internet-diagnostics/assets/report-example.html).

## Available skills

| Skill | Use it for |
| --- | --- |
| [internet-diagnostics](skills/internet-diagnostics/SKILL.md) | Wi-Fi, DNS, VPN, congestion, buffering, calls and connection problems |
| [game-diagnostic](skills/game-diagnostic/SKILL.md) | Low FPS, stutter, input delay, rubber-banding, crashes and loading stalls; read-only evidence first |
| [game-optimizer](skills/game-optimizer/SKILL.md) | One authorized, reversible, evidence-backed experiment at a time; matched benchmarks and rollback decisions |

Gaming skills support Windows, macOS and Linux, require no Python for guided use, and include their own
workflow references and offline report templates. Optional capture tools are not installed automatically.

> Use game-diagnostic. My game starts stuttering after ten minutes. Start read-only, help me reproduce it,
> and compare frame timing with relevant CPU, GPU, memory, storage and power evidence.

> Use game-optimizer with my diagnostic findings. Help me improve frame pacing while preserving image quality.
> Prepare one experiment with its baseline, side effects and rollback, then ask before changing settings.

Invoke `$game-diagnostic` or `$game-optimizer` in Codex, or the corresponding slash command in Claude Code.
The optimizer establishes a baseline when no diagnostic report exists; it does not require another installed skill.

## What internet-diagnostics covers

The first skill investigates local connections, Wi-Fi, name resolution (DNS), delay under load,
VPNs, routing, and problems affecting one application. It supports Windows, macOS, and Linux.

For video calls, it also guides WebRTC/TURN relay troubleshooting. Its optional local browser probe
checks whether a relay can be allocated; call quality and loss require actual application statistics.
See the [skill workflow](skills/internet-diagnostics/SKILL.md) or [optional diagnostic tools](docs/tools.md)
for details. Gaming skills distinguish game rendering/resource constraints from network symptoms.

## Safety and privacy

Checks are read-only by default. The agent explains commands and requires explicit approval before
changing network settings, disconnecting a VPN, or taking other disruptive actions.

Diagnostic logs stay local unless you choose to share them. They can contain network names and addresses;
review and redact them first. Never provide passwords, long-term API keys, or VPN credentials.
The optional TURN probe uses temporary credentials entered directly in its local form.
The skill adds no telemetry or automatic diagnostic uploads. Your agent and the third-party installer
have their own data policies.

## Development

To work on the repository, clone it and run the existing tests:

```sh
git clone https://github.com/jvickusa/tech-support-skills.git
cd tech-support-skills
python -m unittest discover -s tests -v
node --test tests/turn-probe.test.mjs
```

Development tests require Python 3.10+ and Node.js 22+. CI runs on Windows, macOS, and Linux.
See [validation and live-test limits](docs/validation.md).
Skills follow the open [Agent Skills specification](https://agentskills.io/specification), with references
and scripts bundled inside each skill. The installer downloads these skill folders directly from GitHub.

## License

[MIT](LICENSE). Each installable skill includes its license.
Report fonts use the SIL Open Font License; notices are bundled and embedded in the standalone HTML.
