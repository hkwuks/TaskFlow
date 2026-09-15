# Plan — Map TaskFlow phases to the concept class each phase corresponds to
> Task version: v1
> Status: planning

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
  - [ ] Add the phase → concept-class table to the capability section of `SKILL.md` (R1–R4).
  - [ ] State the unaided signal per phase so a skipped capability is visible (R2).
  - [ ] Keep the accounting rule in `artifacts.md` and stop there (R5).
  - [ ] Add one sentence to each README (R7).
  - [ ] Pin the table's presence, phase coverage, and tool-neutrality in `hooks/smoke-test` (R6).
- Acceptance: PRD acceptance criteria A1–A7 pass.
- Verification: `grep` for phase coverage and for tool names inside the table; `bash hooks/smoke-test`; `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow`; `git diff --check`.
- Rollback: Revert the Step 1 commit.
- Status: pending

## Checkpoints

## Verification / Review

## Change Log

## Follow-ups

## Version History

- v1 — planning.
