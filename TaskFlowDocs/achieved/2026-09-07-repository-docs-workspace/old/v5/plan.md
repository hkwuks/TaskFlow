# Plan — Task selection, maintenance, and repository documents
> Task version: v5
> Status: completed

## Approval
- Approved by: user
- Approved at: 2026-09-08 15:01 +08:00
- Approved version: v5
- Approved scope: PRD / Spec / Plan

## Steps
### Step 1 — Approve universal activation and archive transaction
- Goal: Confirm TaskFlow applies before every repository work path and archival is a verified transaction.
- Dependencies: User approval of v5.
- Files: `prd.md`, `spec.md`, `plan.md`.
- Implementation checklist:
  - [x] Confirm universal TaskFlow activation for small and non-trivial requests.
  - [x] Confirm Todo path/status update is mandatory during archive.
  - [x] Confirm no lower-threshold new-task wording remains in active guidance.
- Acceptance: No activation, archive, or task-selection ambiguity remains.
- Verification: User approval recorded.
- Rollback: Retain v4 archive and do not change the shared Skill.
- Status: done

### Step 2 — Implement activation and archive consistency
- Goal: Encode universal activation, atomic archive checks, and corrected task-selection wording.
- Dependencies: Step 1 approval.
- Files: Skill first, then artifacts, catalog, workflow draft, READMEs.
- Implementation checklist:
  - [x] Expand the Skill description to all repository work requests.
  - [x] Add archive transaction and Todo path/status verification.
  - [x] Remove the obsolete lower-threshold new-task wording.
- Acceptance: The Skill controls the behavior without relying on explanatory documents.
- Verification: Scenario review, Todo template check, and stale-rule search.
- Rollback: Revert this step only.
- Status: done

### Step 3 — Synchronize and prove consistency
- Goal: Align public references and verify the archive invariant.
- Dependencies: Step 2 implementation.
- Files: `taskflow/references/artifacts.md`, `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md`, `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [x] Synchronize active documentation with the Skill.
  - [x] Verify an achieved task's root statuses and Todo path.
  - [x] Run focused consistency and diff checks.
- Acceptance: Public guidance and the Skill describe the same model.
- Verification: `rg` stale-path search and `git diff --check`.
- Rollback: Revert this step only.
- Status: done

## Verification / Review

- 2026-09-08 — v4 retrieved from achieved for a v5 repair; `old/v4/` preserves its documents and archive record.
- 2026-09-08 — Skill description now covers every repository work request; the detailed workflow retains the lightest-path decision after Todo intake.
- 2026-09-08 — Archive transaction now verifies the moved directory, Todo `Task:` path/status, absent active path, and achieved root PRD/Plan status.
- 2026-09-08 — Focused obsolete-wording search and `git diff --check` passed.

## Completion

- Status: completed
- Acceptance: passed; all identified activation, archive, and task-selection inconsistencies are repaired.

## Version History
- v1 — superseded directory-only approach.
- v2 — superseded due to incomplete task selection and separate standards layer.
- v3 — existing-task-first and unified document model.
- v4 — Todo-first intake and achieved-task retrieval; completed.
- v5 — universal TaskFlow activation and archive-consistency repair; completed.
