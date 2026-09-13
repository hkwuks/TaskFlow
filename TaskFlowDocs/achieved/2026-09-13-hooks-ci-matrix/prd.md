# Add Linux and Windows CI coverage for TaskFlow hooks
> Task version: v1
> Status: completed

## Goal

Add Linux and Windows CI coverage for TaskFlow hooks

## Background / Confirmed Facts

- Hook smoke tests exist for Bash and native Windows PowerShell/Git Bash.
- The repository currently has no GitHub Actions workflow enforcing them.

## Requirements

- Run the Bash smoke suite on Ubuntu.
- Run the native Windows smoke suite with Git Bash and Python 3 on Windows.
- Trigger for pull requests and pushes to `main`.
- Avoid new project dependencies and deployment/release behavior.

## Acceptance Criteria

- Workflow syntax is valid and uses pinned major GitHub-maintained actions.
- Both OS jobs execute the repository's existing smoke entrypoints.
- Required repository validation remains represented without duplicating test logic.

## In Scope

- One minimal GitHub Actions workflow and directly related documentation/tests if necessary.

## Out of Scope

- Release automation, deployment, coverage services, and unrelated linters.

## Risks / Deferred Items

- Hosted-runner behavior is ultimately verified by GitHub after push.

## Open Questions

## Version History

- v1 — approved and in progress.
