# Index-driven repository document routing
> Task version: v3
> Status: completed

## Goal

Make `repository-docs/index.md` the primary routing record, maintain its deterministic metadata at SessionStart, and inject concise document routes into Agent context.

## Background / Confirmed Facts

- Repository source documents remain authoritative for their actual rules.
- The current index calls itself derived navigation and lacks phase metadata.
- `hooks/session-start` already injects derived context from `hooks/summarize-state`.
- The user approved deterministic automatic index maintenance and compact route injection.
- Windows uses the existing `run-hook.cmd` launcher and Git for Windows Bash; a second PowerShell implementation is not required.

## Requirements

1. Treat the index as the authoritative routing and check record without copying policy text into it or the Skill.
2. Automatically synchronize deterministic metadata for recognized repository documents at SessionStart.
3. Record class, source path, applicable phases, existence, last check, and routing status.
4. Inject applicable paths and status, not full document contents.
5. Mark uncertain candidates for review rather than guessing policy or classification.
6. Never let the hook edit source policies, task core documents, approvals, Git state, PRs, or releases.
7. Support Linux Bash and Windows through `run-hook.cmd` plus Git for Windows Bash.
8. Exercise the complete Windows call chain in a path containing spaces and Chinese characters: launcher, SessionStart, index synchronization, and JSON context injection.
9. After all acceptance checks pass, archive the completed task under `TaskFlowDocs/achieved/` and update its Todo record atomically.
10. Merge the verified branch into `main` and publish patch release `v1.0.3` with Claude `1.0.3` and Codex `1.0.3+codex.20260911` manifests.

## Acceptance Criteria

- A fixture gains or refreshes an index deterministically.
- SessionStart output names routed authoritative documents and missing/review states.
- Re-running synchronization on the same day is idempotent.
- The Skill reads the index first, then routed sources, and records conclusions in Plan.
- Smoke tests and whitespace validation pass.
- Linux smoke passes and the Windows PowerShell/cmd test proves the complete SessionStart chain with Unicode/path-space handling and idempotent index writes.
- The active task path is absent after completion; the achieved task path exists with completed PRD/Plan status and Todo points to it as `done`.

## In Scope

- Index schema and current catalog.
- One synchronization/routing helper and SessionStart integration.
- Skill, artifact reference, hook documentation, and focused smoke checks.
- Windows regression coverage and TaskFlow completion/archive transaction.

## Out of Scope

- Copying source rules into TaskFlow documentation.
- Automatically creating missing governance documents.
- Automatic commits, pushes, pull requests, approvals, tags, or releases.
- Unrelated product changes or user-owned task files.
- Heuristic classification of arbitrary documents.
- A separate PowerShell implementation of the hook logic.

## Risks / Deferred Items

- SessionStart may create a tracked index diff when repository documents changed; this is intentional and reviewable.
- Phase inference from task state is coarse; explicit `TASKFLOW_PHASE` may narrow routing when supplied.
- Windows requires Git for Windows Bash, consistent with the existing plugin launcher contract.

## Open Questions

None.

## Version History

- v1 — Approved index-first routing and bounded SessionStart maintenance.
- v2 — Added Linux/Windows compatibility, full Windows SessionStart-chain verification, and mandatory achieved archival after acceptance.
