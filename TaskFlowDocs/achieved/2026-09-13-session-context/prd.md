# Reduce SessionStart context output to the active task by default
> Task version: v1
> Status: completed

## Goal

Reduce SessionStart context output to the active task by default

## Background / Confirmed Facts

- SessionStart currently injects every unfinished Todo and every active task before repository-document routes.
- `TASKFLOW_TASK_ID` already scopes repository phase inference to one task.

## Requirements

- Default output selects one current task and its next unfinished Plan step.
- `TASKFLOW_TASK_ID` takes precedence when it identifies an active task.
- `TASKFLOW_VERBOSE=1` preserves the full Todo and active-task inventory.
- Ambiguous multi-task state stays concise and does not guess.

## Acceptance Criteria

- Default output omits unrelated Todo and active tasks when a current task is selected.
- Verbose output retains the complete inventory.
- Explicit task selection and ambiguous selection have regression coverage.
- Repository-document routes remain present.

## In Scope

- `hooks/summarize-state`, related SessionStart documentation, and smoke tests.

## Out of Scope

- Parsing SessionStart stdin JSON or changing optional-document statuses; tracked by TF-20260911-08.

## Risks / Deferred Items

- No current task can be inferred when multiple active tasks exist without an explicit ID; output must ask for classification compactly.

## Open Questions

## Version History

- v1 — approved and in progress.
