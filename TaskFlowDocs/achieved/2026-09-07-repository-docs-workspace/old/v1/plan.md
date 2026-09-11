# Plan — Repository documentation workspace
> Task version: v1
> Status: in_progress

## Approval
- Approved by: user
- Approved at: 2026-09-07 23:29 +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps
### Step 1 — Create portable workspace
- Goal: Move standards and create the workspace index.
- Dependencies: User approval.
- Files: `TaskFlowDocs/repository-docs/`, moved standards.
- Implementation checklist:
  - [x] Move `standards/` into `repository-docs/`.
  - [ ] Index existing repository documentation and missing classes.
  - [ ] Record link fallback because `core.symlinks=false`.
- Acceptance: Workspace is readable without symbolic links.
- Verification: Inspect index and moved standards path.
- Rollback: Move standards back and remove the new workspace.
- Status: in_progress

### Step 2 — Synchronize workflow documentation
- Goal: Replace standards paths and document link behavior.
- Dependencies: Step 1.
- Files: `taskflow/SKILL.md`, `taskflow/references/artifacts.md`, `README.md`, `README.zh-CN.md`, `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md`.
- Implementation checklist:
  - [ ] Replace active standards paths.
  - [ ] Document relative-link and index fallback rules.
  - [ ] Keep task-specific references separate.
- Acceptance: All documents use the new workspace contract.
- Verification: Repository-wide path search and diff check.
- Rollback: Revert documentation changes.
- Status: pending

### Step 3 — Verify document catalog
- Goal: Confirm sources, fallbacks, and no fake links.
- Dependencies: Steps 1–2.
- Files: none expected.
- Implementation checklist:
  - [ ] Confirm index paths resolve to existing source documents.
  - [ ] Confirm unavailable classes are listed as not found.
  - [ ] Confirm no symlink is created with `core.symlinks=false`.
- Acceptance: All PRD acceptance criteria pass.
- Verification: `test`, `find`, `rg`, and `git diff --check`.
- Rollback: Reopen the affected step.
- Status: pending

## Verification / Review
- Pending Steps 1–3.

## Version History
- v1 — initial plan.
