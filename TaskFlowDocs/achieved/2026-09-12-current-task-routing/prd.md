# Identify the current TaskFlow task before phase routing
> Task version: v1
> Status: completed

## Goal

Identify the current TaskFlow task before phase routing

## Background / Confirmed Facts

- Multiple active task plans can have different lifecycle states and therefore different repository-document phases.
- Automatic routing must not guess when the active task is ambiguous.

## Requirements

- Honor `TASKFLOW_TASK_ID` when supplied and read only that task's plan for automatic phase inference.
- Preserve `unclassified` when no task is specified and multiple phase candidates exist.

## Acceptance Criteria

- Explicit current task selects its phase.
- Ambiguous tasks remain unclassified.
- Existing smoke suite passes.

## In Scope

## Out of Scope

## Risks / Deferred Items

## Open Questions

## Version History

- v1 — completed with isolated implementation and regression coverage.
