# Plan — Detect a task directory that no Todo entry references

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/repository-check` — uncommitted artifact loop (~69–90); add orphan
  pass beside it.
- `hooks/smoke-test` — `== repository-check … ==` sections (~1078+).
- `TaskFlowDocs/todo.md` — `- Task:` backticked paths.
- Predecessor: `TF-20260916-ab381b` (isolation + uncommitted report).

## Related Tasks

- `TF-20260916-a357ee` — this task’s ID.
- `TF-20260916-ab381b` — done; different direction (misplaced/uncommitted).

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell text
  processing and the repository's own check conventions, all read directly.`

## Preconditions

- [x] Docs/rules inspected; worktree `.worktrees/feat-orphan-task-dirs` on
  `feat/orphan-task-dirs` from `main` = `5eba691`.
- [x] Incident, direction, and ab381b boundary recorded in PRD Background.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-23
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — repository-check orphan report

- Goal: R1–R5.
- Files: `hooks/repository-check`.
- Checklist:
  - [x] Collect `- Task:` backticked paths from `todo.md`.
  - [x] Scan `TaskFlowDocs/*/` and `TaskFlowDocs/achieved/*/` with prd or
        plan; report dirs not referenced (trailing-slash tolerant).
  - [x] Orphans set `needs=1`; uncommitted artifacts unchanged.
  - [x] `bash -n hooks/repository-check`.
- Acceptance: A, B, C.
- Status: done

### Step 2 — smoke

- Goal: R6/R7.
- Files: `hooks/smoke-test`.
- Checklist:
  - [x] Unreferenced active + achieved → listed, exit 2.
  - [x] After adding matching `Task:` → not listed.
  - [x] Existing repository-check sections still green.
- Acceptance: D, E.
- Status: done

## Checkpoints

- After Step 1: `bash -n` + A/B/C fixtures.
- After Step 2: one full suite; no chained mutations; pkill if killed.

## Verification / Review

| Check | Result |
|---|---|
| `bash -n hooks/repository-check` | pass |
| `bash -n hooks/smoke-test` | pass |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` |
| `git diff --check` | clean |
| Active orphan listed / ref clears (A/B) | pass (suite) |
| Achieved orphan (C) | pass (suite) |
| Existing check sections (D) | pass (suite) |

## Change Log

- v1 — planning; Q1 orphan sets needs, Q2 no reverse hard-fail, Q3 no
  special-case names.
- v1 — approved (user, 2026-09-23); Steps 1–2 done; suite green.

## Follow-ups

- Housekeeping commit `5eba691` is on local main only until next push.
- If live tree reports the known historical achieved orphan after merge:
  human decides tombstone vs extra Todo line (data, not code).

## Version History

- v1 — planning.
- v1 — approved (user, 2026-09-23); Steps 1–2 done; suite green.
