# Explicit approval before changes

Diagnostic access does not authorize resets, installs, DNS/MTU/QoS/firewall changes, VPN disconnection,
interface switching, router restart, or captures. Make each proposal concrete before requesting approval:

1. Supporting observation, hypothesis, and one comparison to test.
2. Exact action/command, interface/family/service, and privilege.
3. Security/connectivity impact, including household and remote support channel.
4. Exact saved original state, rollback, verification and stopping condition.

Managed policy changes belong to IT. Before remote-session disruption require acknowledgment and local console
access. If recovery cannot be assured, remain read-only and provide local instructions.

| Evidence | Candidate after approval | Recovery |
| --- | --- | --- |
| Local link instability | Cable/placement/Ethernet comparison | Restore connection; verify route |
| Upload-correlated latency | Pause competing load; supported SQM investigation | Restore workload/settings; repeat before/during/after |
| Stale resolution | Targeted cache clear | Cache repopulates; not a delivery fix |
| Resolver failure | Temporary resolver comparison/change | Restore exact DHCP/static/split-DNS policy |
| VPN-only issue | Short tunnel-off comparison | Reconnect; verify private access/route |
| Size-dependent app/PMTU evidence | Temporary MTU on one interface/family | Save exact MTU, restore, verify |
| App blocked by identified rule | Narrow temporary exception | Save state; remove exactly that exception |

No boilerplate Winsock/network resets, route/filter flushing, IPv6 disabling or optimizers.
Broad resets are last-resort separately approved work with backup/recovery.
`finally`/shell traps cannot guarantee recovery after termination/power loss/lost session.
Save state outside the process and give local recovery instructions.
Failed restoration must be reported explicitly; stop further experiments.
