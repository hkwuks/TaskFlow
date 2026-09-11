# Plan — Task selection, maintenance, and repository documents
> Task version: v4
> Status: in_progress

## Approval
- Approved by: user
- Approved at: 2026-09-08 11:02 +08:00
- Approved version: v4
- Approved scope: PRD / Spec / Plan

## Steps
### Step 1 — Approve Todo-first and achieved-retrieval contract
- Goal: Confirm Todo is mandatory intake and achieved tasks are retrieved before material maintenance.
- Dependencies: User approval of v4.
- Files: `prd.md`, `spec.md`, `plan.md`.
- Implementation checklist:
  - [x] Confirm all direct and imported requests are Todo-first.
  - [x] Confirm batch imports retain one Todo item per source requirement.
  - [x] Confirm achieved-task retrieval, versioning, and re-approval.
- Acceptance: No intake or achieved-task maintenance ambiguity remains.
- Verification: User approval recorded.
- Rollback: Retain v3 archive and do not change the shared Skill.
- Status: done

### Step 2 — Implement Todo-first and achieved-task behavior
- Goal: Encode mandatory Todo intake, batch import handling, achieved archival, and retrieval.
- Dependencies: Step 1 approval.
- Files: Skill first, then artifacts, catalog, workflow draft, READMEs.
- Implementation checklist:
  - [x] Add Todo-first gate before task selection and import handling.
  - [x] Add one-item-per-requirement batch import rules.
  - [x] Add achieved move, retrieval, versioning, and re-approval rules.
- Acceptance: The Skill controls the behavior without relying on explanatory documents.
- Verification: Scenario review, Todo template check, and stale-rule search.
- Rollback: Revert this step only.
- Status: done

### Step 3 — Synchronize and verify the design
- Goal: Align public references and validate Todo-first and achieved retrieval.
- Dependencies: Step 2 implementation.
- Files: `taskflow/references/artifacts.md`, `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md`, `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [x] Synchronize active documentation with the Skill.
  - [x] Verify Todo template supports imported requirements.
  - [x] Run focused consistency and diff checks.
- Acceptance: Public guidance and the Skill describe the same model.
- Verification: `rg` stale-path search and `git diff --check`.
- Rollback: Revert this step only.
- Status: done

## Verification / Review

- 2026-09-08 — v3 was completed, moved to `achieved/`, then retrieved for the user's new material requirements; its documents are preserved in `old/v3/`.
- 2026-09-08 — Confirmed Todo-first, batch one-item-per-requirement, and achieved retrieval rules across Skill, references, workflow draft, READMEs, and Todo template.
- 2026-09-08 — Focused rule search and `git diff --check` passed.

## Completion

- Status: completed
- Acceptance: passed; every request is Todo-first, batch imports preserve one Todo item per source requirement, and achieved tasks are retrieved/versioned/re-approved before maintenance.

## Version History
- v1 — superseded directory-only approach.
- v2 — superseded due to incomplete task selection and separate standards layer.
- v3 — existing-task-first and unified document model.
- v4 — Todo-first intake and achieved-task retrieval; completed.
