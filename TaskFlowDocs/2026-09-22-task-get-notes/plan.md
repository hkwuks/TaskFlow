# Plan — Fix `task get` silently dropping indented Notes continuation lines

> Task version: v1
> Status: ready

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/task` `entry` branch (`cmd == "entry"`) — the only production edit.
- `hooks/smoke-test` `== task get prints one entry and not the Todo file ==`
  — contract the fix must keep; Notes assertions added in the same section.
- `hooks/task` `notes_end` / `next` — related write path, **not** edited here.
- `TaskFlowDocs/todo.md` `TF-20260918-9acf57` — this task's Todo item.

## Related Tasks

- `TF-20260918-9acf57` — this task's Todo item.
- `TF-20260918-454ac4` — Approval automation; depends on a trustworthy `get`
  for Notes, but is not implemented here.
- `notes_end` / `task next` indent — deferred (PRD Q2).

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell/awk text
  processing, POSIX-portability references, and the repository's own hook
  conventions, all read directly.`

## Preconditions

- [x] Applicable repository documents and personal rules inspected;
  precedence/conflicts recorded. — `CONTRIBUTING.md`, `CODE_STYLE.md`,
  `hooks/task`, `hooks/smoke-test`, `TaskFlowDocs/todo.md` read.
- [x] Worktree isolation: `.worktrees/fix-task-get-notes` on
  `fix/task-get-notes` from `main` = `2dfffe3`.
- [x] Bug reproduced on this tree: indented Notes lines absent from `get`.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-22
- Approved version: v1
- Approved scope: R1–R4; print non-blank body (PRD Q1=a); `notes_end` left
  out (Q2).

## Steps

### Step 1 — `entry` prints the full non-blank body

- Goal: R1/R2 — no prefix filter beyond blankness.
- Dependencies: none.
- Files: `hooks/task`.
- Implementation checklist:
  - [x] Replace `if (at(line[i], "- ")) print line[i]` with a non-blank
        filter over `[a, b]`.
  - [x] Leave internal `TASKFLOW_CMD=get` untouched (R2) — still 3 call sites.
  - [x] `bash -n hooks/task`.
- Acceptance: A, B, C.
- Verification: reproduction fixture prints all three Notes lines; existing
  get smoke section green (verbatim slice, no sibling/heading/blank,
  positional ID, read-only, unknown ID, round-trip with `next`).
- Rollback: one-line revert of the filter.
- Status: done

### Step 2 — smoke assertions for Notes continuations

- Goal: R3/R4 — a dropped continuation fails the suite.
- Dependencies: Step 1.
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] Fixture with indented `- ` line and indented no-dash line under Notes.
  - [x] Assert both appear; no blank/heading; body verbatim via `diff`.
- Acceptance: D.
- Verification: one full `bash hooks/smoke-test` → `ALL SMOKE PASSED`.
- Rollback: drop the assertions; Step 1 stands alone.
- Status: done

## Checkpoints

- After Step 1: manual fixture + `bash -n` — done.
- After Step 2: one full suite; no chained mutation runs; process count 0.

## Verification / Review

| Check | Result |
|---|---|
| `bash -n hooks/task` | pass |
| `bash -n hooks/smoke-test` | pass |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` (rc=0) |
| `git diff --check` | clean |
| Reproduction fixture (A) | all three Notes lines present |
| Existing get contract (B) | suite section green |
| `TASKFLOW_CMD=get` call sites (R2) | still 3 |

## Change Log

- v1 — approved and implemented; scope from `TF-20260918-9acf57` (option (a):
  print the body). `notes_end` indent left out per PRD Q2.

## Follow-ups

- `notes_end` / `task next` when Notes continuations are indented.
- Housekeeping still uncommitted on `main` (archive `337ab8`, three stale
  removes) — separate commit when authorized.
- `985164` duplicate ID + merge-todo `key_of` — next candidate after this.

## Version History

- v1 — planning.
- v1 — approved (user, 2026-09-22); Steps 1–2 done; suite green.
