# Fix `hooks/merge-todo` so a `## Removed` record matches its live entry by ID token and deletion wins

> Task version: v1
> Status: completed

## Goal

`hooks/merge-todo` treats a `## Removed` tombstone as an unrelated entry (its
key is the whole `… (removed …)` string), so a live entry the other side still
holds is classified “only they have it” and is **resurrected**. Fix the key,
make deletion win when one side has a tombstone and the other has the live
entry, and clear the duplicate IDs that resurrection left in `todo.md`.

## Background / Confirmed Facts

All measured on `main` = `9887dc3`, 2026-09-22, in worktree
`.worktrees/fix-merge-todo-removed` unless noted. Nothing here is inferred.

**Original report (entry Notes, v1.0.7 era).** Live entry deleted → tombstone
written → merge `944d833` restored the live entry → same ID twice. Notes name
two roots: (1) `task remove` gate bypassed by rewriting `Task:` to
`Not promoted.` first; (2) `merge-todo` `key_of` using `substr($0, 7)` so the
tombstone key is `id:TF-… (removed …)` ≠ live `id:TF-…`. Directed fix: token
key + “Removed on one side, live on the other → delete”; **do not only tighten
the remove gate**.

**Live reproduction — our own rebase of the housekeeping commit.**

Commit `b9fd49e` correctly deleted three stale live entries and wrote three
tombstones (`todo.md` −74 lines). `git rebase origin/main` onto PR #49
(`86a6a24`) invoked `merge=taskflow-todo`. Result `9887dc3` (pushed) has
`tombstones + live bodies` for the same IDs:

| ID | Live line | Tombstone line |
|---|---|---|
| `TF-20260921-4d8ae2` | 15 | 990 |
| `TF-20260919-76e7fb` | 801 | 991 |
| `TF-20260919-2877ca` | 821 | 992 |
| `TF-20260918-985164` | 783 | 989 (pre-existing) |

`grep -o '^- ID: TF-…' | sort | uniq -d` returns all four.

**Why key_of alone is not enough.** `split_todo` cuts on `## `, so **all
tombstones live in one section** headed `## Removed`. `key_of` then reads only
the **first** `- ID:` inside that section. The Removed blob never carries keys
for IDs 2..n, and never equals a live entry’s `id:TF-…` unless the first
tombstone happens to be that ID and the suffix matches (it does not).

**Why the live entry survives.** Driver rule (merge-todo:167–170): “Only we
have it: either we added it, or they removed it. **Keep it**.” During rebase,
theirs still had live `4d8ae2`; ours had no live section (only a line inside
`## Removed`). No match → emit theirs → resurrection. The comment assumes a
deleted entry simply disappears; `remove` moves it into `## Removed`, which
this driver does not join to the live key space.

**`remove` itself works** on a clean fixture (live section gone, one tombstone
under `## Removed`). The gate bypass is historical; the merge bug is what
**undoes** a correct remove.

**Structural facts the fix must respect:**

- `## Removed` must remain **one** heading with tombstone lines under it
  (todo-check: `sed -n '/^## Removed$/,/^## /p'`).
- Live sections stay separate `## title` blocks keyed by `- ID:` token.
- Existing smoke: disjoint adds, one-sided edit, double-edit conflict,
  install idempotence — all must stay green.

## Requirements

- **R1.** `key_of`: ID key is the **first whitespace-delimited token** after
  `- ID:` (tombstone `TF-x (removed …)` → `id:TF-x`).
- **R2.** A section whose heading is `Removed` is always keyed
  `head:Removed` (never by the first tombstone’s ID), so both sides’ Removed
  blobs match each other regardless of which tombstone is first.
- **R3.** Deletion wins on one-sided presence: if side A has a **live** entry
  with ID `X` and side B’s Removed set contains `X`, do **not** emit A’s live
  `X`. Symmetric for the other side. Removed-set membership uses R1’s token.
- **R4.** When both sides have `## Removed` and only one changed it relative to
  base, the existing one-sided rule takes that side (already true if R2 holds).
  When **both** added different tombstones, **union** tombstone lines by ID
  token (order: ours first, then theirs-only), exit 0 — not a conflict.
- **R5.** Data cleanup in this PR’s `todo.md`: exactly one `- ID:` record per
  duplicated ID. `4d8ae2` / `76e7fb` / `2877ca` keep **tombstone only**;
  `985164` keeps the **live** promoted entry for this task and drops the false
  v1.0.7 tombstone. `uniq -d` empty.
- **R6.** Smoke: (a) ours deletes live X→tombstone, theirs leaves X alone →
  merge has tombstone, no live X; (b) symmetric; (c) both add tombstones →
  union, no conflict; (d) existing merge sections green.
- **R7.** `bash hooks/smoke-test` → `ALL SMOKE PASSED`.

## Acceptance Criteria

- **A.** Reproduction of the rebase case (ours=deleted+tombstone, theirs=live
  unchanged) yields tombstone only.
- **B.** `grep -o '^- ID: TF-…' TaskFlowDocs/todo.md | sort | uniq -d` empty
  after R5.
- **C.** todo-check still reads all tombstones from one `## Removed` range.
- **D.** Suite green; `bash -n hooks/merge-todo`.

## In Scope

- `hooks/merge-todo` (key_of, Removed key, deletion-wins, Removed union).
- `hooks/smoke-test` — R6 assertions.
- `TaskFlowDocs/todo.md` — R5 cleanup + this task’s status.
- Task documents.

## Out of Scope

- Tightening `task remove`’s `Task:` gate (Notes: necessary but not
  sufficient; gate-only leaves merge resurrection).
- `hooks/todo-check` (already extracts tombstone IDs correctly).
- Re-attempting the historical v1.0.7 archive (dir already gone).

## Risks / Deferred Items

- Delete/modify where theirs **also** edited the live body: R3 skips the live
  entry (deletion wins) and may drop their edit. Preferable to resurrection;
  a future rule could conflict instead — not observed, not required now.
- Gate bypass (rewrite `Task:` first) remains possible until a separate fix.

## Open Questions

1. Union tombstones when both sides add (R4) vs conflict — **Recommend:
   union** (parallel removes are ordinary; conflict on two tombstone lines is
   noise).
2. Fix `remove` gate in this PR? — **Recommend: no** (Notes explicitly says
   gate-only is the wrong fix; keep this PR on the merge path + data).

## Version History

- v1 — planning.
- v1 — ready; approved by user 2026-09-22 (R1–R7; Q1 union, Q2 no gate fix;
  R5 wording corrected: live `985164` kept).
