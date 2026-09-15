# Stop tracking the workflow draft in TaskFlowDocs
> Task version: v1
> Status: planning

## Goal

Remove `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` from Git tracking, leaving the local file in place, so the task-document root contains only the TaskFlowDocs artifact system.

## Background / Confirmed Facts

- `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` (814 lines) was committed in `660679a` ("feat: release TaskFlow 1.0.2") and is therefore present at `main`, `v1.0.2`, `v1.0.3`, and `v1.0.4`.
- No Skill file, reference, hook, README, or CI workflow reads it: `grep -rln TASKFLOW_WORKFLOW_DRAFT skills hooks README.md README.zh-CN.md CONTRIBUTING.md` returns nothing.
- Its content is duplicated as durable rules in `skills/taskflow/SKILL.md` and `skills/taskflow/references/*.md`; the draft was the design source for v1 and is now historical.
- `TaskFlowDocs/` is defined by the Skill as the task-artifact root: `todo.md`, `repository-docs/`, `<task-id>/`, and `achieved/`. The draft is not any of those.
- The local copy must survive: it is the only full design narrative and is not recoverable from the current Skill text alone.

## Requirements

- R1. `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` is untracked in the change set (`git rm --cached`, no content change, local file preserved).
- R2. The file's bytes are unchanged by this task.
- R3. No other tracked file is modified except the Todo entry for this task.
- R4. The local leftover copy is excluded from `git status` in this clone through `.git/info/exclude`, not through a tracked ignore rule: the file is being removed from the repository, so a repo-wide `.gitignore` entry would document a path that no longer exists in it.
- R5. The untrack path and the reason are recorded in `plan.md`, including where the surviving narrative now lives.

## Acceptance Criteria

- A1. `git ls-files TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` returns nothing after the change.
- A2. The local file exists with the same SHA-256 as before the change.
- A3. `git status --short` shows exactly the deletion entry and the Todo change; no content modification to the draft.
- A4. `git check-ignore -v TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` matches the local exclude rule in `.git/info/exclude`.
- A5. No source change to `skills/`, `hooks/`, or `README*`: this task only changes tracking state plus the ignore rule.
- A6. `bash hooks/smoke-test` passes and `git diff --check` is clean.

## In Scope

- The tracked status of `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md`, its ignore entry, and the `TaskFlowDocs/todo.md` entry for this task.

## Out of Scope

- Rewriting history or removing the file from `660679a`, `main`, or any released tag (`v1.0.2`–`v1.0.4`).
- Deleting or relocating the local file, or promoting its content anywhere.
- Changing `hooks/summarize-state`, `hooks/repository-docs-context`, or any task discovery logic: the draft is not a task directory and already does not match their patterns.
- Any other file in `TaskFlowDocs/`.

## Risks / Deferred Items

- The file stays in published tags; anyone cloning `main` after this change loses it, and existing clones that keep the hard copy will show it as untracked until the ignore rule is present. Reported, not fixed here.
- If the draft is later wanted as durable documentation, it belongs at a documented repository path outside `TaskFlowDocs/` under the normal document rules — deferred, needs its own approved task.
- History rewrite was considered and rejected: it would rewrite shared, already-released tags.

## Open Questions

None — scope (untrack only, history untouched) was decided by the user on 2026-09-14.

## Version History

- v1 — planning.
