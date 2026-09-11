# TaskFlow Hook opportunity audit

> Reviewed: 2026-09-10
> Scope: Claude Code and Codex plugin Hooks

## Outcome

Implement one shared read-only `hooks/check` first. Reuse it from `PostToolUse` for immediate feedback and `Stop` for an end-of-turn gate. Keep all semantic or destructive transitions as explicit Agent-invoked scripts.

## Priority 1 — shared structural checker

### `hooks/check [task-id | --all-active]`

- Mode: explicit command and shared implementation for automatic Hooks.
- Reads: Todo and active task PRD/Spec/Plan files.
- Writes: nothing.
- Checks:
  - Todo task links resolve and Todo/task lifecycle states agree.
  - Existing core documents use one Task version.
  - `ready` has no active approval; `in_progress` has approval for the current version.
  - Required PRD/Plan exist and large tasks with a declared Spec pointer have `spec.md`.
  - A `done` Plan step has no unchecked required checklist item.
  - `completed` tasks meet archive preconditions but are not moved automatically.
- Value: consolidates rules currently re-evaluated by the Agent and gives both hosts one deterministic result.
- Output: empty on success; short actionable diagnostics with task ID, invariant, and file path on failure.

## Priority 2 — automatic feedback using the checker

### `PostToolUse` / Claude `PostToolBatch`

- Trigger: successful file mutation tools (`apply_patch`, `Edit`, `Write`); shell mutation coverage is checked at `Stop` because parsing arbitrary commands is brittle.
- Action: run `hooks/check --changed` only when `TaskFlowDocs/` changed.
- Writes: nothing.
- Response: inject a diagnostic only on failure; otherwise print nothing.
- Value: catches mixed versions, stale Todo links, and invalid approval/state combinations before the next model action.
- Constraint: multiple matching Hooks run concurrently, so this must not depend on another Hook's output or mutate shared state.

### `Stop` / `SubagentStop`

- Trigger: Agent attempts to finish a turn.
- Action: run `hooks/check --all-active`.
- Block only for deterministic, actionable inconsistencies introduced or left unresolved in the current task. Respect the host's repeated-stop guard to avoid loops.
- Writes: nothing.
- Value: prevents a false completion claim while keeping ordinary conversational turns quiet.
- Do not require every active task to be completed; unfinished work is valid.

## Priority 3 — explicit scripts, not automatic Hooks

### `hooks/intake`

- Inputs supplied by Agent: ID, source, one-sentence goal, owner/priority when known.
- Action: append or update one Todo item, allocate the next same-day numeric ID, and reject duplicates.
- Value: removes repetitive Markdown writing and ID bookkeeping.
- Boundary: never infer the goal from the raw user prompt and never promote automatically.

### `hooks/state <task-id> <state>`

- Action: atomically update PRD/Plan/Todo lifecycle metadata after the Agent has established the transition is allowed.
- Value: prevents three-file status drift and saves mechanical edits.
- Boundary: never grant approval, decide completion, or archive; reject transitions whose deterministic prerequisites fail.

### `hooks/promote <todo-id> <task-id> [--large]`

- Action: create compact PRD/Plan shells, optional Spec shell, and update the Todo link/status.
- Value: avoids rewriting standard headings.
- Boundary: only explicit invocation after clarification; Agent still writes goals, requirements, acceptance criteria, design, and plan content.
- Priority below `intake` and `state`: placeholder shells can create churn if the task is simple.

## Already covered

- `SessionStart` already matches startup, resume, clear, and compact, so a separate `PostCompact` summary adds no value.
- `archive`, `reopen`, and copy-first `version` are already deterministic explicit commands.

## Do not Hook automatically

- PRD/Spec/Plan generation: semantic authorship cannot be derived safely from an event payload.
- Tool or Skill selection: preserve Agent autonomy; Hooks cannot observe private selection intent.
- Approval: always belongs to the user.
- Task-version classification: deciding whether a user change is material is semantic.
- Archive/reopen/version execution: moves or copies durable history and must remain explicit.
- Todo creation from every `UserPromptSubmit`: many prompts are questions or follow-ups, and Codex/Claude matchers cannot reliably classify them without adding another model.
- Repository-document catalog refresh: discovery can be scripted, but document classification and whether an unknown file is authoritative require review.
- Automatic tests after every edit: expensive and noisy; use focused Plan verification, with the structural checker as the cheap Hook.
- Capability-use ledger from `PostToolUse`: the event proves a call happened but cannot determine its purpose or which conclusion was incorporated.
- Session file writes on start/end: creates concurrency and stale-resume problems for an optional artifact.

## Recommended implementation order

1. `hooks/check` with direct smoke fixtures.
2. Wire it read-only to `PostToolUse`/`PostToolBatch` and `Stop`/`SubagentStop` for both hosts.
3. Add `hooks/intake` only after observing repeated manual Todo edits.
4. Add `hooks/state` only after the checker has stabilized the lifecycle invariants.
5. Add `hooks/promote` only if measured token savings justify placeholder management.

## Sources

- OpenAI Codex Hooks: https://developers.openai.com/codex/hooks
- Claude Code Hooks reference: https://docs.anthropic.com/en/docs/claude-code/hooks
- Local runtime contract: `skills/taskflow/references/runtime.md`
