# Plan — Fix `hooks/merge-todo` so a `## Removed` record matches its live entry by ID token and deletion wins

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/merge-todo` — `key_of`, `Removed` key, deletion-wins, Removed union.
- `hooks/todo-check` `removed_at` — single `## Removed` range (C).
- `hooks/smoke-test` — new section `== todo merge driver treats ## Removed … ==`.
- `TaskFlowDocs/todo.md` — R5 data cleanup.

## Related Tasks

- `TF-20260918-985164` — this task's Todo item.
- `task remove` gate bypass — deferred (PRD Q2).

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell/awk text
  processing, POSIX-portability references, and the repository's own merge
  driver conventions, all read directly.`

## Preconditions

- [x] Docs/rules inspected; worktree `.worktrees/fix-merge-todo-removed` on
  `fix/merge-todo-removed` from `main` = `9887dc3`.
- [x] Bug reproduced (four duplicated IDs after rebase) and root-caused.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-22
- Approved version: v1
- Approved scope: R1–R7; union on dual tombstone edits (Q1); gate fix out
  (Q2).

## Steps

### Step 1 — merge-todo: token key, Removed key, deletion wins, union

- Goal: R1–R4.
- Files: `hooks/merge-todo`.
- Implementation checklist:
  - [x] `key_of`: first whitespace token; `Removed` heading → `head:Removed`.
  - [x] Per-side removed-ID sets; skip lone live copy when the other side
        names the ID (both only-we-have and theirs-only paths).
  - [x] Dual-changed `## Removed` → union tombstones by ID, exit 0.
  - [x] Header Rules comment updated (deletion is `## Removed` and wins).
  - [x] `bash -n hooks/merge-todo`.
- Acceptance: A.
- Verification: smoke delete/keep fixtures (both directions) + union.
- Status: done

### Step 2 — smoke assertions

- Goal: R6/R7.
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] Ours deletes / theirs keeps live → tombstone only, no conflict.
  - [x] Symmetric reverse.
  - [x] Both add tombstones → union, one `## Removed`.
  - [x] Existing merge driver sections still pass.
- Acceptance: D.
- Verification: one full `bash hooks/smoke-test` → `ALL SMOKE PASSED`.
- Status: done

### Step 3 — clear duplicate IDs in todo.md

- Goal: R5/B/C.
- Files: `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [x] `4d8ae2` / `76e7fb` / `2877ca`: live sections removed; tombstones kept.
  - [x] `985164`: **live kept** (this task, promoted); false v1.0.7 tombstone
        dropped — PRD R5 corrected: one record per ID, not “always drop live”.
  - [x] `uniq -d` empty; single `## Removed` with three tombstones.
- Acceptance: B, C.
- Status: done

## Checkpoints

- After Step 1: `bash -n` + fixtures — done.
- After Step 2: one full suite (after killing a stuck run per memory);
  `ALL SMOKE PASSED`; process count 0.
- After Step 3: `uniq -d` empty.

## Verification / Review

| Check | Result |
|---|---|
| `bash -n hooks/merge-todo` | pass |
| `bash -n hooks/smoke-test` | pass |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` |
| `git diff --check` | clean |
| `uniq -d` on todo IDs | empty |
| Delete/keep + union fixtures | suite section green |

## Change Log

- v1 — approved and implemented; R5 data rule clarified: keep live `985164`
  (active task), drop its obsolete tombstone; three stale IDs keep tombstones
  only.
- follow-up on PR #50 CI: `todo-check` `ids_at` now takes the first ID token
  (same identity as `removed_at`), so dropping a stale tombstone while keeping
  the live ID is not reported as a drop.

## Follow-ups

- `task remove` gate vs pre-rewritten `Task:` — separate if desired.
- Archive family `172455` / `88e04c` / `e7c041`.
- `b7821b` Approval shape.

## Version History

- v1 — planning.
- v1 — approved (user, 2026-09-22); Steps 1–3 done; suite green.
