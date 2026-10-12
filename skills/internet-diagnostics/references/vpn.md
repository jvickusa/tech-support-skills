# VPN investigation

Use when performance changes with a tunnel, private resources fail, or only some destinations stall.
Ask whether VPN is required by policy, full/split tunnel, provider/client if relevant, failing resource scope,
and whether the support connection itself depends on it. Do not request configuration files or credentials.

## Inspect before changing

Preview `scripts/collect.py --vpn --dry-run`, explain profile names/private route sensitivity, then collect locally.
Windows reads user/system built-in profiles. macOS reads system connections and proxy state.
Linux reads active NetworkManager connection types and policy rules. Baseline already records routes/DNS/MTU.
Commands time out after 15 seconds. Missing/denied commands remain unavailable.
None of these lists is a complete third-party VPN detector. Empty output does not prove VPN is off.
Use vendor connection status and selected-route evidence; never dump keys, `wg showconf`, or nmcli secrets.

Resolve the actual affected destination and inspect selected route/source/interface using the OS reference.
Compare public and authorized private resources separately. Split DNS and private routes may be intentional.
Check client-reported connection/region/protocol, resolver selection, family, interface MTU, and proxy policy.
Do not conclude “DNS leak” or “kill switch broken” from a public IP change or one failed probe.

## Controlled comparison

Save the connected baseline and exact reconnection procedure first.
Propose one brief public-workload test with VPN disconnected, its duration/security impact, and recovery.
Require explicit approval. If policy forbids this or no local recovery console exists, keep the tunnel on
and escalate with read-only evidence. Never defeat kill switches or organization security controls.

After approval, compare identical destination/family/workload before, off, and reconnected.
Verify route/DNS/private access after reconnection. Record whether failure follows the tunnel repeatedly.
Different public exit routes/regions confound comparisons; improvement does not identify VPN software as faulty.
If only large responses fail, follow PMTU investigation rather than applying a guessed MTU.

## Fix and escalation

Evidence may justify a provider-region comparison, vendor update, or targeted DNS/MTU/policy investigation.
Client/protocol/route/DNS changes need separate approval, exact saved state, and rollback.
Managed split-tunnel, firewall, and resolver changes belong to IT.
Report connected/off/reconnected results, relevant private-resource behavior, uncertainty and restoration status.
Redact employer names, profile names, private domains, routes and addresses from public summaries.
