# Optional diagnostic tools

Guided troubleshooting works without Python. These helpers are for agents or users who want repeatable
collection or more detailed WebRTC evidence. Missing tools should not block native OS checks.

## Python collector

Requires Python 3.10+. From a repository checkout:

```sh
python skills/internet-diagnostics/scripts/collect.py --dry-run
python skills/internet-diagnostics/scripts/collect.py --wifi --vpn --dry-run
python skills/internet-diagnostics/scripts/collect.py --format markdown > baseline.md
python skills/internet-diagnostics/scripts/collect.py --gateway 192.168.1.1 --target example.com --count 20 > evidence.json
```

For an installed skill, ask your agent to locate `scripts/collect.py` in that installation.
Windows can use `py -3`; macOS/Linux can use `python3`.
`--dry-run` previews commands. Baseline sends no deliberate probes; target/gateway options add bounded probes.
Select the gateway for the actual destination route, not an assumed address.
`example.com` illustrates syntax; choose a relevant authorized destination.
`--trace` adds a bounded trace; `--family 6` selects IPv6.
Wi-Fi/VPN profiles read current or cached state without active scans or tunnel changes.

Output is sensitive and unredacted. Choose private storage and avoid overwriting evidence.
Nothing uploads automatically. Raw JSON is an evidence record, not a confirmed diagnosis or public share payload.

## Local TURN allocation probe

The [TURN guide](../skills/internet-diagnostics/references/turn.md) explains the optional browser probe,
temporary credentials, and interpreting allocation versus actual media delivery.
Its documented local-server command uses Python; an existing localhost static server can serve the same files.
If neither is available, use the application's own WebRTC diagnostics instead of installing a runtime just for this test.
No camera/microphone is requested. Failure means allocation unavailable, never 100% packet loss.
