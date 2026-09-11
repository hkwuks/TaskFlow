# Index-driven repository document routing
> Task version: v1
> Status: in_progress

## Goal

Make `repository-docs/index.md` the primary routing record, maintain its deterministic metadata at SessionStart, and inject concise document routes into Agent context.

## Background / Confirmed Facts

- Repository source documents remain authoritative for their actual rules.
- The current index calls itself derived navigation and lacks phase metadata.
- `hooks/session-start` already injects derived context from `hooks/summarize-state`.
- The user approved deterministic automatic index maintenance and compact route injection.

## Requirements

1. Treat the index as the authoritative routing and check record without copying policy text into it or the Skill.
2. Automatically synchronize deterministic metadata for recognized repository documents at SessionStart.
3. Record class, source path, applicable phases, existence, last check, and routing status.
4. Inject applicable paths and status, not full document contents.
5. Mark uncertain candidates for review rather than guessing policy or classification.
6. Never let the hook edit source policies, task core documents, approvals, Git state, PRs, or releases.

## Acceptance Criteria

- A fixture gains or refreshes an index deterministically.
- SessionStart output names routed authoritative documents and missing/review states.
- Re-running synchronization on the same day is idempotent.
- The Skill reads the index first, then routed sources, and records conclusions in Plan.
- Smoke tests and whitespace validation pass.

## In Scope

- Index schema and current catalog.
- One synchronization/routing helper and SessionStart integration.
- Skill, artifact reference, hook documentation, and focused smoke checks.

## Out of Scope

- Copying source rules into TaskFlow documentation.
- Automatically creating missing governance documents.
- Automatic commits, pushes, pull requests, approvals, tags, or releases.
- Heuristic classification of arbitrary documents.

## Risks / Deferred Items

- SessionStart may create a tracked index diff when repository documents changed; this is intentional and reviewable.
- Phase inference from task state is coarse; explicit `TASKFLOW_PHASE` may narrow routing when supplied.

## Open Questions

None.

## Version History

- v1 — Approved index-first routing and bounded SessionStart maintenance.
