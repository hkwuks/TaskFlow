# Plan — Record Approval from a hook instead of hand-editing the five fixed fields

> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/task` — command dispatch, `promote` Approval template (~651–657),
  `require_approval` (~503–515), `today` (~18).
- `hooks/version` — five-field reset shape (post-#52) — read-only mirror.
- `hooks/smoke-test` — lifecycle / approval-gates sections.
- `skills/taskflow/SKILL.md` — “Record approval as” snippet (~225–233).
- Predecessor: `TF-20260919-b7821b` / PR #52 (shape alignment).

## Related Tasks

- `TF-20260918-454ac4` — this task’s ID.
- `TF-20260919-b7821b` — done; five-field shape.

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell text
  processing and the repository's own hook conventions, all read directly.`

## Preconditions

- [x] Docs/rules inspected; worktree `.worktrees/feat-task-approve` on
  `feat/task-approve` from `main` = `7f531a2`.
- [x] Housekeeping archive commit for b7821b is on local main (`7f531a2`).
- [x] Field sources and `require_approval` inputs recorded in PRD.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-23
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — task approve

- Goal: R1–R5.
- Files: `hooks/task`.
- Checklist:
  - [x] `approve <task-id> [approver] [--root]` usage; default `user`.
  - [x] Preflight: plan + `## Approval` + `> Task version:`; no write on fail.
  - [x] Rewrite/insert five fields in promote order with R3 values;
        `Approved at` from `date '+%Y-%m-%d %H:%M %z'`; scope from R4.
  - [x] Do not touch `> Status:`, Todo, or Git; not gated by
        `require_approval`.
  - [x] `bash -n hooks/task`.
- Acceptance: A, B, C.
- Status: done

### Step 2 — skill sentence

- Goal: R6.
- Files: `skills/taskflow/SKILL.md`.
- Checklist:
  - [x] After the five-line snippet: record via `task approve [approver]`
        once the user has approved; hand-edit only as fallback.
  - [x] No second field template.
- Acceptance: D (snippet unchanged shape).
- Status: done

### Step 3 — smoke

- Goal: R7/R8.
- Files: `hooks/smoke-test`.
- Checklist:
  - [x] Promoted pending plan → `approve` → five lines exact → gated
        command passes.
  - [x] Custom approver; missing section/version leaves file unchanged.
  - [x] Scope `PRD / Plan` vs `PRD / Spec / Plan`.
  - [x] Existing approval-gates section still green.
- Acceptance: E.
- Status: done

## Checkpoints

- After Step 1: `bash -n` + A/B/C fixtures.
- After Step 3: one full suite; no chained mutations; pkill if killed.

## Verification / Review

| Check | Result |
|---|---|
| `bash -n hooks/task` | pass |
| `bash -n hooks/smoke-test` | pass |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` |
| `git diff --check` | clean |
| Approve + gate (A/B) | pass (suite) |
| Refuse no-write (C) | pass (suite) |
| Scope subsets (D) | pass (suite) |

## Change Log

- v1 — planning; Q1 optional approver default `user`, Q2 `date` with
  timezone no fallback, Q3 fixed `PRD / Spec / Plan` subset order.
- v1 — approved (user, 2026-09-23); Steps 1–3 done; suite green.

## Follow-ups

- Push local main housekeeping `7f531a2` when convenient (currently
  ahead of origin by 1 on base only — actually local main has it; push
  with next main push or separately).

## Version History

- v1 — planning.
- v1 — approved (user, 2026-09-23); Steps 1–3 done; suite green.
