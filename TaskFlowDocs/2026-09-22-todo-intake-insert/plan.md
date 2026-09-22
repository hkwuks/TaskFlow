# Plan — `task intake` inserts a new entry into the previous section instead of `## Items`

> Task version: v1
> Status: ready

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/task` `intake` branch — the only production edit.
- `hooks/task` `remove` — how `## Removed` is placed; must stay compatible.
- `hooks/todo-check` `removed_at` (`sed -n '/^## Removed$/,/^## /p'`) — the
  reader the insertion must not poison.
- `TaskFlowDocs/todo.md` — `<!-- Add new items at the top … -->`.
- `hooks/smoke-test` — new section after the parallel-intake block.

## Related Tasks

- `TF-20260921-337ab8` — this task's Todo item.
- `TF-20260918-985164` — duplicate ID + false Removed record; **not fixed here**
  (data cleanup, separate).
- Promote title mismatch / Goal alignment — deferred per PRD Q1.

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell/awk text
  processing, POSIX-portability references, and the repository's own hook
  conventions, all read directly.`

## Preconditions

- [x] Applicable repository documents and personal rules inspected;
  precedence/conflicts recorded. — `CONTRIBUTING.md`, `CODE_STYLE.md`,
  `TaskFlowDocs/todo.md`, `hooks/task`, `hooks/todo-check`, `hooks/smoke-test`
  read in this worktree.
- [x] Worktree isolation: `.worktrees/fix-todo-intake-insert` on
  `fix/todo-intake-insert` from `main` = `895e102`.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-22
- Approved version: v1
- Approved scope: R1–R5; intake insertion only — no promote/title alignment
  (PRD Open Question 1), no new refusal path when Items is missing (Q2).

## Steps

### Step 1 — `intake` insertion index

- Goal: new block lands at top of `## Items` (R1), or just before
  `## Removed` when Items is missing (R2), or EOF only when neither exists
  (R3).
- Dependencies: none.
- Files: `hooks/task`.
- Implementation checklist:
  - [x] In the `intake` branch, compute an insertion line index instead of
        always emitting after `line[n]`.
  - [x] Scan for `^## Items` then skip blanks / one leading HTML comment;
        insert there. Else scan for `^## Removed`; insert there. Else keep
        current EOF path (rstrip + append).
  - [x] Keep Goal/ID duplicate checks, title derivation, and field template
        unchanged (R4) — fields now go through the shared `emit()` path.
  - [x] `bash -n hooks/task`.
- Acceptance: A, B, D.
- Verification: four manual fixtures (Items+trailing Removed; bare `# Todo`;
  no Items + Removed; Removed-above-first-entry). Order
  `Items < new < seed < Removed`; new ID absent from the `removed_at` range;
  Goal-derived `## <title>` written.
- Rollback: revert this commit; no other file depends on the index.
- Status: done

### Step 2 — smoke assertions

- Goal: a regression of the insertion point fails the suite (R5).
- Dependencies: Step 1.
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] Fixture with `## Items` + seed entry + trailing `## Removed`; intake;
        assert new heading is after `## Items` and before both the seed
        heading and `## Removed`.
  - [x] Assert new ID absent from the `removed_at` sed range.
  - [x] Bare `# Todo` still intakes (R3); no-Items+Removed lands before
        Removed (R2).
- Acceptance: C.
- Verification: one full `bash hooks/smoke-test` → `ALL SMOKE PASSED`.
- Rollback: drop the block; Step 1 still stands alone.
- Status: done

## Checkpoints

- After Step 1: manual fixtures + `bash -n` before touching smoke — done.
- After Step 2: one full `bash hooks/smoke-test` — done; no chained mutation
  runs; `pkill` confirmed 0 leftover processes.

## Verification / Review

| Check | Result |
|---|---|
| `bash -n hooks/task` | pass |
| `bash -n hooks/smoke-test` | pass |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` (rc=0) |
| `git diff --check` | clean |
| PRD reproduction fixture | order + removed-range + Goal title OK |
| No interpreter / bash 3.2 parse section | pass (suite) |

## Change Log

- v1 — approved and implemented; scope from `TF-20260921-337ab8` Notes
  (insertion point + Removed pollution + smoke acceptance). Title/promote
  alignment explicitly out of scope.

## Follow-ups

- `TF-20260918-985164` — remove the false tombstone / restore or cancel the
  live duplicate.
- `TF-20260921-4d8ae2` — close the stale inbox entry (fix already on
  `fix/repository-docs-reader`, merged via #46).
- Promote-title vs Goal — decide in the todo Notes' open question when that
  item is picked up.

## Version History

- v1 — planning.
- v1 — approved (user, 2026-09-22); Steps 1–2 done; suite green.
