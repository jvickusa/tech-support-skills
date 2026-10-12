# Report contract

Raw collector Markdown is an evidence appendix, not a diagnosis. Keep private evidence separate from redacted summary.

## Human template

```text
Problem/impact: [symptom/app, onset, device/service scope]
Window: [start/end with time zone; reproduced or not]
Environment: [OS, connection, VPN/proxy; unknowns explicit]
Conclusion: [supported boundary/mechanism or undetermined; confidence/reason]
Observed: [IDs, methods/target roles, windows, actual results, limitations]
Comparisons: [workload/target, changed variable, before/after, repeated or not]
Possible causes: [hypothesis/confidence, supporting IDs, alternatives, next test]
Unavailable/untested: [reason; no substituted zeros]
Changes: [approval, saved state, identical retest, result, rollback status; or none]
Next/escalation: [who acts, concrete evidence-backed request, reviewed attachments]
```

Redact usernames/device names, addresses, SSIDs/BSSIDs/MACs/GUIDs, private domains, identifying VPN names,
meeting links, accounts, locations, and neighboring networks unless essential for private support.
Review archives manually; automatic redaction cannot guarantee privacy. Sharing requires separate authorization.

## Local collector JSON, version 1

Envelope: `schema_version`, `captured_at`, `os`, `os_release`, `observations`.
Observation: `id`, `started_at`, `duration_seconds`, `command` (argument array), `status`
(`ok`, `error`, `timeout`, `unavailable`), `exit_code` (integer/null), `output`, `truncated` (boolean).
Stdout/stderr merged; output capped per command. `ok` means successful process exit, not healthy networking.
Errors/timeouts may retain useful partial evidence. Cancellation emits completed observations plus
`cancelled: true`, exits 130, skips remaining tests. Command targets/raw output are sensitive;
never place this envelope in public share links.
The TCP probe tests only the first resolved address on port 443. Failure does not establish failure of every
address, port, application, or protocol. The collector intentionally creates no bandwidth load.
`system-dns` uses the OS name service (including caches/hosts files). A literal-IP target performs no hostname
lookup; its success cannot establish DNS health. Use a relevant hostname to investigate name resolution.

Optional `--wifi`/`--vpn` observations follow the same envelope and remain sensitive local evidence.
TURN allocation output is a separate version-1 `kind: turn-allocation` record containing only
`captured_at`, `status` (`observed`, `unavailable`, `cancelled`), `reason`, `relay_candidates`,
`ice_error_codes` and `duration_seconds`, plus `schema_version`/`kind`.
This is allocation evidence, not relay media loss or proof of a selected connection.
Reference it in the human report as method `turn-allocation`, distinct from application/WebRTC statistics.

## Optional agent-authored summary JSON, version 1

```json
{
  "schema_version": 1,
  "kind": "internet-diagnostics-summary",
  "captured_at": "2026-10-11T19:40:00-05:00",
  "conclusion": "Loaded latency needs a controlled comparison.",
  "confidence": "undetermined",
  "observations": [{"id": "target-ping", "method": "icmp-echo", "target_role": "internet", "status": "unavailable", "summary": "No interpretable reply series."}],
  "hypotheses": [],
  "comparisons": [],
  "changes": [],
  "next_steps": ["Repeat gateway and Internet tests during the affected workload."]
}
```

Top-level keys above only. Confidence enum: `high`, `moderate`, `low`, `undetermined`.
Observation fields above; role enum: `gateway`, `internet`, `service`, `local`;
status enum: `observed`, `unavailable`, `skipped`.
Hypothesis fields: `cause`, `confidence`, `evidence_ids`, `alternatives`, `next_test`.
Comparison fields: `variable`, `before`, `after`, `evidence_ids`.
Change fields: `action`, `approved`, `result`, `rollback_status`.
Text fields are strings; evidence_ids/alternatives/next_steps are string arrays; approved is boolean.
No numeric metrics initially: retain measurement methods in observations without inventing values.
No raw output, addresses/hostnames, context, SSIDs, samples or credentials. Review free text for identifiers too.

Future website imports must validate enums/types/version/kind, reject unknown fields, bound arrays to 50
and strings to 2000 characters, and render as text. Evidence IDs must refer to existing observations.
This defines a future integration contract; no website importer or share schema modification is included.
