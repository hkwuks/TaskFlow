# Record the host SessionStart session_id in the active task's sessions.md
> Task version: v1
> Status: completed

## Goal

Make the platform session identifier that `hooks/session-start` already reads reach the active task's `sessions.md`, so a cross-session or cross-agent resume points at a real, platform-specific session instead of a placeholder.

## Background / Confirmed Facts

- `hooks/session-start` parses the host event JSON and already extracts `session_id` (hooks/session-start:30,35), exporting it as `TASKFLOW_SESSION_ID` (hooks/session-start:43).
- `TASKFLOW_SESSION_ID` has no reader anywhere in the repository (verified by grep over the whole tree): the value is currently discarded.
- Claude Code SessionStart stdin provides `session_id`, `cwd`, `hook_event_name`, and `source` with source values `startup|resume|clear|compact|fork`. The matcher `startup|resume|clear|compact|fork` in `hooks/hooks.json` is an exact-value list, so all of these fire the hook.
- `skills/taskflow/SKILL.md:246` and `skills/taskflow/references/artifacts.md` define an optional `sessions.md` resume index; `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` §9 defines the same index as the design source. No hook currently creates or maintains it.
- The `sessions.md` template (`artifacts.md` Session outline) requires fields a hook cannot derive: `Last completed` and `Next step` are semantic progress that belongs to `plan.md`.
- Claude Code sessions resume with `claude --resume <session_id>`; Codex sessions resume with `codex resume <session_id> -C <dir>`. Agent identity is detectable from the environment (`AI_AGENT=claude-code_<version>_agent`, `CLAUDECODE=1`; Codex equivalents).
- Repository rule `skills/taskflow/references/runtime.md:44` allows a hook to "inject a derived, clearly non-authoritative context summary"; it does not yet authorize hook writes to task documents. This task is the explicit authorization for one narrow write.

## Requirements

- R1. A new extensionless bash script `hooks/session-record` writes/updates `sessions.md` only in the single selected active task, then exits without printing to stdout.
- R2. `hooks/session-start` invokes it after the existing summary/index steps, passing the event cwd and `session_id` it already parsed. A failure of the new step must not change SessionStart's exit code or context output.
- R3. The script selects a task exactly like `hooks/summarize-state`: explicit `TASKFLOW_TASK_ID` when it names an active task, otherwise the unique active task; zero or multiple active tasks means no write.
- R4. It skips silently when there is no `session_id`, no task, no `TaskFlowDocs`, or the selected task has no `plan.md`.
- R5. Behavior by target state:
  - no `sessions.md` → create the file with the `artifacts.md` Session outline header, one `## Active / Resumable` section, and one entry;
  - `sessions.md` with a hand-written but parseable template → fill the empty entry fields in place;
  - `sessions.md` with an existing entry whose `Session ID` equals the current one → update that entry's hook-owned fields in place;
  - `sessions.md` with entries for other sessions only → append a new entry using the next free `S<n>` id.
- R6. Hook-owned fields are exactly: `Status` (`resumable`), `Primary` (`yes` only when `sessions.md` has no other `resumable` entry, else `no`), `Session availability` (`local-only`), `Session ID`, `Started` (preserved when already present), `Last active`, `Code working directory` (event cwd), `Task artifact directory` (task-relative path), `Task version / phase` (from `plan.md`), `Resume` (platform-appropriate command when the platform and id are known, an explicit unknown-platform note otherwise).
- R7. Fields the hook does not own — `Last completed`, `Next step`, `Notes`, and any prose — must survive an upsert byte-for-byte.
- R8. The script never writes outside the selected task directory, never touches `TaskFlowDocs/achieved/`, never marks an entry `closed`, and never rewrites content it cannot parse.
- R9. Documentation states this write in `skills/taskflow/references/runtime.md` and `skills/taskflow/references/artifacts.md`, and the hook inventory in `hooks/README.md` lists the new script.
- R10. `hooks/smoke-test` covers creation, same-session update, new-session append, and the no-session / no-task / multi-task no-op paths.

## Acceptance Criteria

- A1. With one active task and a SessionStart event carrying `session_id=S`, `sessions.md` exists with exactly one `### S1 — <Agent>` entry whose `Session ID` is `S` and `Status` is `resumable`.
- A2. A second SessionStart with the same `S` updates that entry in place: still one entry with `Session ID: S`, refreshed `Last active`, no duplicated entry.
- A3. A SessionStart with a different `session_id` appends a second entry and leaves the first entry's bytes unchanged.
- A4. Given a hand-written `sessions.md` entry with `Last completed`/`Next step` filled in, the matching-session upsert leaves those lines unchanged.
- A5. With no `session_id`, no active task, or two active tasks and no `TASKFLOW_TASK_ID`, no `sessions.md` is created or modified, and SessionStart's stdout JSON and exit code are unchanged.
- A6. An unparseable `sessions.md` produces a stderr warning, leaves the file untouched, and keeps SessionStart at exit 0 with its normal context.
- A7. `bash hooks/smoke-test` passes and `git diff --check` is clean.

## In Scope

- `hooks/session-record` (new), `hooks/session-start` (one added invocation), `hooks/smoke-test`, `hooks/README.md`, `skills/taskflow/references/runtime.md`, `skills/taskflow/references/artifacts.md`.
- Aligning the `sessions.md` template's hook-owned vs Agent-owned fields where the current template is ambiguous.

## Out of Scope

- Recording `Last completed` / `Next step` from `plan.md` (Agent-owned semantic progress).
- Marking sessions `closed`/`expired`, rotating old entries, or archiving `sessions.md`.
- Writing session records for tasks under `TaskFlowDocs/achieved/`.
- Any new host event binding (`UserPromptSubmit`, `Stop`, `SessionEnd`) or any other hook write.
- Changes to `skills/taskflow/SKILL.md` session guidance beyond the field-ownership clarification the template alignment requires.

## Risks / Deferred Items

- The hook writes into a task document; a wrong task selection would create `sessions.md` in the wrong task directory. Mitigated by reusing the existing selection rule and by the no-op-by-default behavior on ambiguity.
- Idempotence is limited to template lines; a heavily restructured `sessions.md` degrades to an append, not an overwrite. Appending never loses user content.
- `hooks/smoke-test` runs SessionStart through `run-hook.cmd` on Windows; the new step must stay crash-free when `TASKFLOW_SESSION_ID` is absent.

## Open Questions

None — task shape, field set, and write strategy were decided by the user on 2026-09-14.

## Version History

- v1 — planning.
