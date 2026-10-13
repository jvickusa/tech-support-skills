# Manual installation

Use this option if you do not have Node.js/npx or prefer to copy the skill yourself.

Download the repository with GitHub's **Code → Download ZIP**, then extract it.
Or, if Git is installed:

```sh
git clone https://github.com/jvickusa/tech-support-skills.git
```

Choose `internet-diagnostics`, `game-diagnostic`, or `game-optimizer`. Copy the **whole** corresponding folder
under `skills/`, including references, assets, license and any scripts. Each skill installs independently.
Review any existing installation before replacing it.

| Agent | Personal destination | Project destination |
| --- | --- | --- |
| Codex | `~/.agents/skills/internet-diagnostics/` | `.agents/skills/internet-diagnostics/` |
| Claude Code | `~/.claude/skills/internet-diagnostics/` | `.claude/skills/internet-diagnostics/` |
| Other compatible agents | Agent's documented skills directory | Agent's documented skills directory |

`~` means your home folder. Personal installations work across projects; project installations work in that folder.
Replace `internet-diagnostics` in destination paths and examples with the chosen skill name.

From the extracted repository, macOS/Linux personal Codex installation:

```sh
mkdir -p ~/.agents/skills
cp -R skills/internet-diagnostics ~/.agents/skills/
```

Windows PowerShell personal Codex installation:

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills" | Out-Null
Copy-Item -Recurse skills/internet-diagnostics "$HOME/.agents/skills/"
```

For Claude Code replace `.agents` with `.claude`. You can also copy folders using your file manager.
Refresh/restart the agent if needed, then follow [the usage example](../README.md#use).

See [Codex discovery documentation](https://developers.openai.com/codex/skills) and
[Claude Code skills documentation](https://code.claude.com/docs/en/skills) for agent-specific details.
