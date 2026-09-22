# Plan — Make the task complete / archive transaction fail-safe, print the stage commands, and keep todo.md rewrites byte-tight

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/task` `complete` branch — preflight, docstatus, archive, rollback.
- `hooks/archive` — mv + todo rewrite + verify; add stage/branch print.
- `hooks/smoke-test` `== archive preflight ==` / `== archive happy path ==` /
  lifecycle complete.
- Sibling todos: `TF-20260918-88e04c`, `TF-20260918-172455` (Next action
  already points here).

## Related Tasks

- `TF-20260918-e7c041` — umbrella / this task’s ID.
- `TF-20260918-88e04c`, `TF-20260918-172455` — family.
- `TF-20260919-b7821b` / `454ac4` — Approval shape; out of scope.

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell text
  processing and the repository's own hook conventions, all read directly.`

## Preconditions

- [x] Docs/rules inspected; worktree `.worktrees/fix-archive-transaction` on
  `fix/archive-transaction` from `main` = `e9d4c3c`.
- [x] Failure modes and two historical incidents recorded in PRD Background.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-22
- Approved version: v1
- Approved scope: R1–R6; Q1 print stage, Q2 current branch, Q3 lock R4 only.

## Steps

### Step 1 — complete: preflight first, rollback on archive failure

- Goal: R1/R2.
- Files: `hooks/task`.
- Checklist:
  - [x] Expand preflight before any `docstatus`: todo link, achieved absent,
        both core docs present (same checks archive will re-do).
  - [x] Record `> Status:` of plan and prd; write `completed`; call archive.
  - [x] On archive non-zero: restore both statuses; `fail` with archive output.
  - [x] `bash -n hooks/task`.
- Acceptance: A.
- Status: done

### Step 2 — archive: reverse-move on verify fail; print stage + branch

- Goal: R2 tail, R3, R4.
- Files: `hooks/archive`.
- Checklist:
  - [x] After successful `mv`, if todo rewrite or verify fails: `mv` achieved
        path back to active (best effort), then exit 1.
  - [x] On success, print exact `git add` lines for active-remove and
        achieved-add paths, and: commit on the **current branch**.
  - [x] Keep todo rewrite to Status/Task/Next action only (R4).
  - [x] `bash -n hooks/archive`.
- Acceptance: B, C.
- Status: done

### Step 3 — smoke

- Goal: R5/R6.
- Files: `hooks/smoke-test`.
- Checklist:
  - [x] Stub-archive fixture: complete marks docs then archive exits 1 → both
        statuses restored, active dir still present, complete non-zero.
  - [x] Happy path: stage print contains both paths + current-branch phrase.
  - [x] Happy path: todo diff only expected fields; `git diff --check` clean
        on fixture.
  - [x] Existing archive/lifecycle sections green.
- Acceptance: D.
- Status: done

## Checkpoints

- After Step 1–2: `bash -n` + targeted fixtures.
- After Step 3: one full suite; no chained mutations; pkill if killed.

## Verification / Review

| Check | Result |
|---|---|
| `bash -n hooks/task` | pass |
| `bash -n hooks/archive` | pass |
| `bash -n hooks/smoke-test` | pass |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` |
| `git diff --check` | clean |
| Rollback fixture (A) | pass (suite) |
| Stage print (B) | pass (suite) |
| R4 three-field rewrite | pass (suite) |

## Change Log

- v1 — planning; scope from e7c041+88e04c+172455. Q1 print, Q2 current
  branch, Q3 no blank-line hunt.
- v1 — approved and implemented; suite green.

## Follow-ups

- Complete/archive `985164` and `9acf57` (done work still promoted).
- `b7821b` Approval shape next after this lands.

## Version History

- v1 — planning.
- v1 — approved (user, 2026-09-22); Steps 1–3 done; suite green.
