# Token-saving lifecycle scripts
> Task version: v1
> Status: completed

## Goal

Replace repetitive Agent reads and whole-document edits with deterministic, concise lifecycle commands.

## Requirements

- Provide explicit `intake`, `promote`, `state`, `progress`, and `complete` operations.
- Keep write operations Agent-invoked; do not bind them to `PostToolUse`, `Stop`, or `UserPromptSubmit`.
- `promote` reads the Todo and accepts Todo ID, task ID, and `small|large`; the Agent supplies semantic content afterward.
- `complete` requires an explicit user-accepted flag before marking core documents completed and invoking archive.
- Successful commands emit one short line; failures emit actionable errors.
- Enhance SessionStart summary only when doing so avoids full document reads without adding noisy content.
- Preserve approval, semantic classification, and development-request applicability boundaries.

## Acceptance Criteria

- One shared command exposes all five operations through the existing Windows/Unix launcher.
- Todo allocation/update, promotion scaffolding, state synchronization, Plan progress updates, and accepted completion work in an isolated fixture.
- Invalid or unauthorized transitions fail before mutation.
- Existing smoke checks continue to pass.

## Scope

- `hooks/task`, `hooks/summarize-state`, smoke tests, Skill/runtime/artifact guidance, and public command documentation.
- No automatic write Hook, user config/cache edit, commit, push, or archive of existing tasks.

## Version History

- v1 — approved mixed explicit-write/automatic-summary design.
