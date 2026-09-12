# Harden the Windows hook launcher argument forwarding and failure reporting
> Task version: v1
> Status: in_progress

## Goal

Harden the Windows hook launcher argument forwarding and failure reporting

## Background / Confirmed Facts

- `hooks/run-hook.cmd` currently expands only `%2` through `%9`, so arguments after the ninth are lost.
- Re-expanding individual batch parameters also makes quoting behavior harder to preserve.
- Git Bash is the repository's single Windows execution path; a separate PowerShell implementation is out of scope.

## Requirements

- Forward every argument after the script name through Git Bash.
- Preserve spaces, Unicode text, multiple arguments, and quoted values.
- Keep a visible non-zero diagnostic when no acceptable Git Bash is available.
- Preserve the Unix polyglot path.

## Acceptance Criteria

- More than eight post-script arguments arrive intact and in order.
- Spaces, Chinese text, and embedded quote cases are covered by an executable Windows check.
- Missing Git Bash produces a clear non-zero failure.
- Linux smoke tests and shell syntax checks remain green.

## In Scope

- `hooks/run-hook.cmd` and the smallest relevant launcher test/documentation updates.

## Out of Scope

- Replacing Git Bash, installing it automatically, or implementing another lifecycle runtime.
- Other optimization Todo items.

## Risks / Deferred Items

- Batch parsing has platform-specific quoting rules; native Windows execution is required before claiming those cases passed.

## Open Questions

- None.

## Version History

- v1 — approved and in progress.
