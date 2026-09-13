# Model optional repository documents and consume SessionStart event input
> Task version: v1
> Status: in_progress

## Goal

Model optional repository documents and consume SessionStart event input

## Background / Confirmed Facts

- SessionStart receives structured JSON on stdin, but the current hook ignores it.
- The repository index currently labels every absent recognized document as `missing`, including optional governance files.

## Requirements

- Consume `hook_event_name`, `cwd`, and `session_id` from stdin JSON.
- Process only `SessionStart`; ignore unrelated events safely.
- Prefer event `cwd` for repository resolution.
- Classify absent documents as `optional` where appropriate and reserve `missing` for required sources.
- Inject only derived paths/status, never source policy text.

## Acceptance Criteria

- Valid SessionStart JSON routes to the event cwd and includes session metadata safely.
- Non-SessionStart input exits without mutating or emitting TaskFlow context.
- Optional absent documents do not appear as blocking errors.
- Existing smoke tests remain green.

## In Scope

- `hooks/session-start`, `hooks/repository-docs-context`, and focused smoke coverage/documentation.

## Out of Scope

- Changing task selection semantics or adding new repository policy documents.

## Risks / Deferred Items

- Malformed event JSON should fail closed with an actionable diagnostic rather than guess a directory.

## Open Questions

## Version History

- v1 — approved and in progress.
