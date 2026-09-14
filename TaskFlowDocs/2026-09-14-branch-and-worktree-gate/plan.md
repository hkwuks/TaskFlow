# Plan — Require a working branch or dedicated worktree before implementation starts
> Task version: v1
> Status: planning

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `CONTRIBUTING.md`
- `CODE_STYLE.md`
- `hooks/repository-docs-context`
- `hooks/repository-check`

## Related Tasks

- Depends on: None
- Related: `TaskFlowDocs/2026-09-14-macos-hook-portability/` (also touches routing/CI, no shared files)
- Blocks: None

## Skills / Tools Used (Optional)

## Preconditions

- [x] Applicable repository documents and personal supplements inspected; precedence/conflicts recorded.
- [x] For remote/fork/PR work: not applicable.
- [x] For PR creation/update: not applicable — no PR is created by this task.
- [x] Missing governance drafts and explicit approvals recorded before they become binding.
- [x] Work isolation: this task runs in `fix/repo-doc-housekeeping`-style short-lived branch inside its own worktree, per the rule being added.

## Approval

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

## Steps

### Step 1 — Implement and verify

- Goal: State the contributor branch rule in repository guidance, the worktree rule in the Skill, and route contribution rules to the design phase.
- Dependencies: None.
- Files: `CONTRIBUTING.md`, `skills/taskflow/SKILL.md`, `TaskFlowDocs/repository-docs/index.md`, `hooks/repository-docs-context`, `hooks/smoke-test`, `README.md`, `README.zh-CN.md`, `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [x] Add the contributor branch rule with one command to `CONTRIBUTING.md` (R1–R3).
  - [x] Add the worktree rule to `skills/taskflow/SKILL.md` Phase 5 (R4).
  - [x] Add `design` to `CONTRIBUTING.md`'s phase list in `hooks/repository-docs-context` and regenerate `index.md` (R5, R6).
  - [x] Extend the `hooks/smoke-test` routing regression for the design phase (R6).
  - [x] State the rule in `README.md` and `README.zh-CN.md` (R8).
- Acceptance: PRD acceptance criteria A1–A7 pass.
- Verification: `TASKFLOW_PHASE=design bash hooks/repository-docs-context`; `bash hooks/smoke-test`; `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow`; `git diff --check`.
- Rollback: Revert the Step 1 commit.
- Status: done

## Checkpoints

## Verification / Review

## Change Log

## Follow-ups

## Version History

- v1 — planning.
