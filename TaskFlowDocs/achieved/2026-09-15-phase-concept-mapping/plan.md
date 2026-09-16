# Plan — Map TaskFlow phases to the concept class each phase corresponds to
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `CONTRIBUTING.md`
- `CODE_STYLE.md`
- `skills/taskflow/SKILL.md` (capability section, `## Phase routing`)

## Related Tasks

- Depends on: None
- Related: `TaskFlowDocs/2026-09-14-branch-and-worktree-gate/` (also edits `SKILL.md` phase text; different phase and hunk)
- Blocks: None

## Skills / Tools Used (Optional)

## Preconditions

- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded.
- [x] For remote/fork/PR work: not applicable.
- [x] For PR creation/update: not applicable — no PR is created by this task.
- [x] Missing governance drafts and explicit approvals recorded before they become binding.
- [x] Work isolation: this task runs on `docs/concept-mapping` inside its own worktree.

## Approval

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

## Steps

### Step 1 — Implement and verify

- Goal: Add one concept-correspondence table so each phase recognizes the class of capability that belongs to it.
- Dependencies: None.
- Files: `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, `README.md`, `README.zh-CN.md`, `hooks/smoke-test`, `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [x] Add the phase → concept-class table to the capability section of `SKILL.md` (R1–R4).
  - [x] State the unaided signal per phase so a skipped capability is visible (R2).
  - [x] Keep the accounting rule in `artifacts.md` and stop there (R5).
  - [x] Add one sentence to each README (R7).
  - [x] Pin the table's presence, phase coverage, and tool-neutrality in `hooks/smoke-test` (R6).
- Acceptance: PRD acceptance criteria A1–A7 pass.
- Verification: `grep` for phase coverage and for tool names inside the table; `bash hooks/smoke-test`; `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow`; `git diff --check`.
- Rollback: Revert the Step 1 commit.
- Status: done

## Checkpoints

## Verification / Review

## Change Log

- 2026-09-15 work revision — Closed out: the work shipped as PR #21 (merged) and is on `main`; the phase → concept-class table is in `skills/taskflow/SKILL.md`. Archived with `## Approval` left at `Status: requested`: no commit in this repository's history records an approval for this task, so no approver is named. Recorded as a work revision because implementation is complete and no approved contract is being changed.

## Follow-ups

- The Todo entry was absent from `main` when this task was closed out: a6d8fdd (PR #21) wrote it, and the merge in 77c25dd (PR #17, "Merge branch 'main' into chore/untrack-workflow-draft") dropped the whole section without a conflict marker because one side of the merge did not carry it. Reconstructed from a6d8fdd.

## Version History

- v1 — planning.
