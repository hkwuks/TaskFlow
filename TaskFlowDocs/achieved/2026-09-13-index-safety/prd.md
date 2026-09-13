# Validate repository-document index paths and protect concurrent writes
> Task version: v1
> Status: completed

## Goal

Validate repository-document index paths and protect concurrent writes

## Background / Confirmed Facts

- `hooks/repository-docs-context` derives index rows from repository-relative source paths and writes the index atomically through a temporary file.
- Existing path handling accepts preserved index rows and needs an explicit repository-boundary check before routing or writing.

## Requirements

- Reject absolute and traversal paths in repository-document index records.
- Never route or write a source path outside the repository root.
- Preserve the existing index if parsing or validation fails.
- Keep writes atomic and add a minimal concurrency safeguard.

## Acceptance Criteria

- Malicious absolute/`..` records fail safely without replacing the existing index.
- Concurrent invocations do not leave partial index files.
- Existing smoke checks remain green.

## In Scope

- `hooks/repository-docs-context` and focused smoke coverage.

## Out of Scope

- Redesigning the repository-document catalog format or changing source policy.

## Risks / Deferred Items

- A single repository-local lock serializes index refreshes; higher throughput is not needed for SessionStart.

## Open Questions

## Version History

- v1 — approved and in progress.
