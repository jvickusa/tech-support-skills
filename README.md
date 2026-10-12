# Tech Support Skills

Troubleshooting skills for AI agents, from [whyismyinternetcrap.com](https://whyismyinternetcrap.com).
Use them to investigate why games lag, streams buffer, or calls freeze—even when a speed test looks good.

The website checks your connection from the browser. These skills help a compatible agent investigate
your device and network, explain the evidence, and recommend the next step. You can use them independently
or give your agent a result from the site. Results are not imported or uploaded automatically.

## Installation

With [Node.js](https://nodejs.org/) (including npm/npx) and [Git](https://git-scm.com/) installed, run:

```sh
npx skills add jvickusa/tech-support-skills
```

The [Skills CLI](https://github.com/vercel-labs/skills) discovers `internet-diagnostics` and installs it
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

## What internet-diagnostics covers

The first skill investigates local connections, Wi-Fi, name resolution (DNS), delay under load,
VPNs, routing, and problems affecting one application. It supports Windows, macOS, and Linux.

For video calls, it also guides WebRTC/TURN relay troubleshooting. Its optional local browser probe
checks whether a relay can be allocated; call quality and loss require actual application statistics.
See the [skill workflow](skills/internet-diagnostics/SKILL.md) or [optional diagnostic tools](docs/tools.md)
for details. Additional skills will be added when they address a distinct support need.

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
