# Design

Foundation: supplied `docs/tech-support-research.md` in sibling
[crap-internet](https://github.com/jvickusa/crap-internet), reviewed 2026-10-11.
Research is not a runtime dependency. Generated citation markers are not portable URLs;
primary links live in `skills/internet-diagnostics/references/sources.md`.
Research scripts were reviewed and adapted rather than copied wholesale.

One independently installable skill follows the [open specification](https://agentskills.io/specification).
Short entrypoint routes to OS commands, comparisons, advanced branches, interpretation, and reporting.
No proprietary frontmatter, tool grants, or premature skill framework.

One Python standard-library collector avoids three collectors and localized parsers.
Fixed argument arrays, process timeouts, bounded retained output, and explicit statuses preserve evidence.
No shell execution, installs, elevation, configuration changes, bandwidth loads, or root-cause engine.
Gateway selection stays explicit because first-default-route selection misleads on VPN/multihomed systems.
Localized ping stays raw; process exit codes cannot establish loss. Partial observations remain marked.

Collector JSON is a versioned local evidence envelope. A separate summary contract excludes raw topology,
context and identifiers. Future website imports require validation and safe text rendering.
No uploader, website engine change, backend, or share-link schema is included.
Native tools differ by OS release, privilege and Linux distribution; feature detection and manual fallbacks
preserve unavailable states. Additional skills should address distinct demonstrated workflows.
