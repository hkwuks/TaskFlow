# Spec — Token-saving lifecycle scripts
> Task version: v1

## Command Interface

- `hooks/task intake <goal> [source] [--root <path>]`
- `hooks/task promote <todo-id> <task-id> <small|large> [--root <path>]`
- `hooks/task state <task-id> <planning|ready|in_progress|checking|blocked> [--root <path>]`
- `hooks/task progress <task-id> <step-number> <pending|in_progress|done|blocked> [verification] [--root <path>]`
- `hooks/task complete <task-id> --user-accepted [--root <path>]`

On Windows the same calls use `hooks\\run-hook.cmd task ...`.

## Responsibilities

- One implementation owns Markdown parsing and atomic file replacement.
- The Agent owns goals supplied to intake, semantic artifact content, state-transition decisions, verification conclusions, and confirmation that the user accepted completion.
- `complete` sets PRD/Plan to `completed`, then delegates the existing archive transaction.

## Invariants

- Operate only below the resolved repository's `TaskFlowDocs`.
- Reject duplicate Todo goals and IDs, existing promotion destinations, unknown states, missing approval for `in_progress`, incomplete checklists for a `done` Step, and completion without the exact flag.
- Do not overwrite semantic sections during metadata updates.
- Write files atomically before invoking the existing archive command.

## Testing

- Extend `hooks/smoke-test` with one isolated end-to-end lifecycle fixture plus focused failure assertions.
- Validate Windows launcher reachability, Bash syntax, JSON, links, and diff whitespace.

## Design Decision

- Use one `hooks/task` dispatcher instead of five scripts so parsing, validation, and atomic-write behavior exist once.
