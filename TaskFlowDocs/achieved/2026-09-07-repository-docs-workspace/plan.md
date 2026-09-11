# Plan — Task selection, maintenance, and repository documents
> Task version: v6
> Status: completed

## Approval
- Approved by: user
- Approved at: 2026-09-08 15:52 +08:00
- Approved version: v6
- Approved scope: PRD / Spec / Plan

## Steps
### Step 1 — Record historical archive repair
- Goal: Create Todo traceability for completed active tasks before archive.
- Dependencies: User approval.
- Files: `prd.md`, `spec.md`, `plan.md`.
- Implementation checklist:
  - [x] Identify completed active task directories.
  - [x] Add one Todo item per historical task.
  - [x] Record user approval for archive repair.
- Acceptance: Each completed active task has a linked in-progress Todo item.
- Verification: Todo review.
- Rollback: Leave directories active and Todo items in progress.
- Status: done

### Step 2 — Archive completed historical tasks
- Goal: Apply the archive transaction separately to each completed historical task.
- Dependencies: Step 1 approval.
- Files: Skill first, then artifacts, catalog, workflow draft, READMEs.
- Implementation checklist:
  - [x] Archive `2026-09-07-repository-standards-and-doc-root` and update its Todo item.
  - [x] Archive `2026-09-07-todo-intake-and-promotion` and update its Todo item.
  - [x] Verify no completed task remains at the active root.
- Acceptance: Both task directories, Todo records, and root statuses agree.
- Verification: Explicit path/status checks.
- Rollback: Record blocker; do not claim complete archive.
- Status: done

### Step 3 — Verify global archive consistency
- Goal: Prove the rule and filesystem now agree.
- Dependencies: Step 2 implementation.
- Files: `taskflow/references/artifacts.md`, `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md`, `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [x] Verify each Todo completed task points into `achieved/`.
  - [x] Verify achieved root PRD/Plan statuses are `completed`.
  - [x] Run focused consistency and diff checks.
- Acceptance: No completed active root task remains.
- Verification: status inventory and `git diff --check`.
- Rollback: Revert this step only.
- Status: done

## Verification / Review

- 2026-09-08 — v5 retrieved from achieved for the user-approved v6 historical archive repair; `old/v5/` preserves its documents and archive record.
- 2026-09-08 — Archived both remaining completed active tasks and synchronized their Todo paths/statuses.
- 2026-09-08 — Verified no completed task remains at active root; all repaired achieved root PRD/Plan files say `completed`; `git diff --check` passed.

## Completion

- Status: completed
- Acceptance: passed; completed-task storage and Todo traceability now match the Skill policy.

## Version History
- v1 — superseded directory-only approach.
- v2 — superseded due to incomplete task selection and separate standards layer.
- v3 — existing-task-first and unified document model.
- v4 — Todo-first intake and achieved-task retrieval; completed.
- v5 — universal TaskFlow activation and archive-consistency repair; completed.
- v6 — archive remaining completed historical tasks and restore Todo traceability; completed.
