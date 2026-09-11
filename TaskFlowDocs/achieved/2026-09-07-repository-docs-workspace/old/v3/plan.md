# Plan — Task selection, maintenance, and repository documents
> Task version: v3
> Status: completed

## Approval
- Approved by: user
- Approved at: 2026-09-08 00:06 +08:00
- Approved version: v3
- Approved scope: PRD / Spec / Plan

## Steps
### Step 1 — Confirm task boundaries and supplement scope
- Goal: Resolve the higher new-task threshold, mixed-request behavior, and supplement applicability.
- Dependencies: User decisions.
- Files: `prd.md`, `spec.md`, `plan.md`.
- Implementation checklist:
  - [x] Confirm independent acceptance plus releasability threshold.
  - [x] Confirm mixed-request split behavior.
  - [x] Confirm scope-matched personal supplements.
- Acceptance: No task-selection or precedence ambiguity remains.
- Verification: User approval recorded.
- Rollback: Keep v3 planning state; do not change shared Skill.
- Status: done

### Step 2 — Implement behavior in TaskFlow
- Goal: Encode task selection, mandatory maintenance, unified repository docs, and supplement precedence.
- Dependencies: Step 1 approval.
- Files: Skill first, then artifacts, catalog, workflow draft, READMEs.
- Implementation checklist:
  - [x] Add existing-task-first decision and maintenance checks.
  - [x] Remove active standards-layer paths.
  - [x] Add personal supplement contract and conflict stop.
- Acceptance: The Skill controls behavior without relying on explanatory documents.
- Verification: Scenario review and stale-path search.
- Rollback: Revert this step only.
- Status: done

### Step 3 — Synchronize and verify the design
- Goal: Align public references and prove the active model has no standards layer.
- Dependencies: Step 2 implementation.
- Files: `taskflow/references/artifacts.md`, `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md`, `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [x] Synchronize active documentation with the Skill.
  - [x] Check active paths for the removed standards layer.
  - [x] Run focused diff and consistency checks.
- Acceptance: Public guidance and the Skill describe the same model.
- Verification: `rg` stale-path search and `git diff --check`.
- Rollback: Revert this step only.
- Status: done

## Verification / Review

- 2026-09-08 — User approval recorded for all three v3 decisions.
- 2026-09-08 — `quick_validate.py` could not run because the environment lacks Python `yaml`; equivalent frontmatter and invariant checks passed.
- 2026-09-08 — Stale active `standards/` paths absent; `git diff --check` passed.

## Completion

- Status: completed
- Acceptance: passed; TaskFlow now enforces existing-task-first selection, mandatory maintenance, unified `repository-docs`, and scoped non-conflicting personal supplements.

## Version History
- v1 — superseded directory-only approach.
- v2 — superseded due to incomplete task selection and separate standards layer.
- v3 — existing-task-first and unified document model.
