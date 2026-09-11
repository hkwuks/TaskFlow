# Plan — Todo intake and promotion workflow
> Task version: v1
> Status: completed

## Spec Pointers
- `spec.md` — Todo item model, promotion contract, and checklist semantics.

## Related Tasks
- Depends on: None
- Blocks: None
- Related: `TaskFlowDocs/2026-09-07-repository-standards-and-doc-root/`

## Skills / Tools Used
- `taskflow` — routes this new workflow-design task through PRD, Spec, and Plan.
- `spec-driven-development` — defines the Todo promotion contract before implementation.

## Preconditions
- Existing TaskFlow root is `TaskFlowDocs/`.
- Existing rule against duplicate generic task fact sources must be reconciled with the proposed Todo inbox.

## Approval
- Approved by: user
- Approved at: 2026-09-07 22:33 +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps
### Step 1 — Confirm Todo inbox contract
- Goal: Resolve inbox path, fields, statuses, and promotion ownership.
- Dependencies: User decisions.
- Files: `prd.md`, `spec.md`, `plan.md`.
- Implementation checklist:
  - [x] Confirm inbox path and whether one repository-level `todo.md` is allowed.
  - [x] Confirm status transitions and required fields.
  - [x] Confirm promotion trigger and split/cancel behavior.
- Acceptance: No blocking open questions remain in PRD/Spec.
- Verification: User approval recorded in `plan.md`.
- Rollback: Retain planning state; do not create a Todo inbox until approved.
- Status: done

### Step 2 — Update TaskFlow documentation
- Goal: Document Todo→PRD→Spec→Plan and Plan checklists.
- Dependencies: Step 1 approval.
- Files: `taskflow/SKILL.md`, `taskflow/references/artifacts.md`, `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md`, `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [x] Add Todo intake and promotion phase.
  - [x] Add checklist block to Plan templates and completion gate.
  - [x] Synchronize paths, statuses, and links across documents.
- Acceptance: All documents describe the same promotion and checklist contract.
- Verification: Repository-wide search and `git diff --check`.
- Rollback: Revert documentation-only changes.
- Status: done

### Step 3 — Verify lifecycle examples
- Goal: Confirm examples cover capture, promotion, implementation, completion, and cancellation.
- Dependencies: Step 2.
- Files: changed documentation only.
- Implementation checklist:
  - [x] Validate one Todo item can be traced to one task directory.
  - [x] Validate a Plan Step cannot be done with unchecked required items.
  - [x] Validate no duplicate fact source is introduced.
- Acceptance: Acceptance criteria pass and follow-ups are recorded.
- Verification: `rg` checks plus manual document review.
- Rollback: Reopen the affected step.
- Status: done

## Checkpoints
- After Step 1: contract approved before repository-wide documentation edits.
- After Step 2: all references agree before final verification.

## Verification / Review
- User approved inbox path, status flow, item schema, and mandatory checklists on 2026-09-07.
- `rg -n 'Todo|todo|checklist|清单' taskflow taskflow/references README.md README.zh-CN.md TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md TaskFlowDocs/todo.md` — passed; intake and checklist rules are present.
- `git diff --check` — passed.

## Follow-ups
- Consider a separate CLI only if manual promotion becomes a measured bottleneck.

## Version History
- v1 — initial plan, implemented and verified.
