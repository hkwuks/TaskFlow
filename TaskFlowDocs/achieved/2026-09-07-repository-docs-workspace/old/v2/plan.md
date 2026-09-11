# Plan — Repository document environment behavior
> Task version: v2
> Status: completed

## Approval
- Approved by: user
- Approved at: 2026-09-07 23:29 +08:00
- Approved version: v2
- Approved scope: PRD / Spec / Plan

## Steps
### Step 1 — Confirm refresh and discovery policy
- Goal: Resolve the behavior decisions that control when and how the Agent maintains the catalog.
- Dependencies: User decisions.
- Files: `prd.md`, `spec.md`, `plan.md`.
- Implementation checklist:
  - [x] Confirm refresh trigger.
  - [x] Confirm handling of unrecognized candidate documents.
  - [x] Confirm handling of missing expected classes.
- Acceptance: No behavior-level ambiguity remains.
- Verification: User approval recorded.
- Rollback: Keep task in planning; do not modify common workflow instructions.
- Status: done

### Step 2 — Encode Agent workflow
- Goal: Add discovery, catalog refresh, selection, and source-authority rules to TaskFlow.
- Dependencies: Step 1 approval.
- Files: Skill, artifact reference, workspace index, workflow draft, READMEs.
- Implementation checklist:
  - [x] Add phase-specific selection rules.
  - [x] Add refresh/change behavior.
  - [x] Add catalog metadata and link fallback contract.
- Acceptance: Agent behavior is executable from the Skill, not implied by docs.
- Verification: Scenario review and path checks.
- Rollback: Revert Step 2 documents.
- Status: done

### Step 3 — Verify document catalog
- Goal: Confirm sources, fallback, and no fake links.
- Dependencies: Step 2.
- Files: none expected.
- Implementation checklist:
  - [x] Confirm index paths resolve to existing source documents.
  - [x] Confirm unavailable classes are listed as not found.
  - [x] Confirm no symlink is created with `core.symlinks=false`.
- Acceptance: All PRD acceptance criteria pass.
- Verification: `test`, `find`, `rg`, and `git diff --check`.
- Rollback: Reopen the affected step.
- Status: done

## Verification / Review
- `test -f ../../README.md && test -f ../../README.zh-CN.md` from `repository-docs/` — passed.
- `find TaskFlowDocs/repository-docs -type l` — no links created while `core.symlinks=false`.
- Active workflow references use `TaskFlowDocs/repository-docs/`; old standards paths remain only in historical task records.
- `git diff --check` — passed.

## Version History
- v1 — superseded directory-only approach.
- v2 — behavior-first design.
