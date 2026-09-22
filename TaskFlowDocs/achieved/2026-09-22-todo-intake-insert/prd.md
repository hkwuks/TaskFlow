# `task intake` inserts a new entry into the previous section instead of `## Items`

> Task version: v1
> Status: completed

## Goal

`hooks/task intake` writes the new entry at the top of `## Items` — after the
section heading and its comment, before any other `## ` heading — so an intake
can never land in `## Removed` or under another entry's title.

## Background / Confirmed Facts

All measured on `main` = `895e102` (PR #47 merged), 2026-09-22, in worktree
`.worktrees/fix-todo-intake-insert`. Nothing here is inferred.

**Root cause (`hooks/task` `intake`, lines 193–216).** The branch:

1. rejects duplicate Goal / ID against every section;
2. derives `title` from Goal (`rstrip "."` then truncate 80);
3. strips trailing blank lines from the whole file;
4. reprints the file;
5. appends `"\n\n## <title>\n\n- ID: …"` at EOF.

There is no scan for `## Items`, no insertion index, and no awareness of
`## Removed`. The insertion point is always end-of-file.

**Live reproduction** (fixture: preamble + `## Items` + one seed entry +
`## Removed` as last section), `bash hooks/task intake "New goal…" --root $tmp`:

| Line | Content |
|---|---|
| 7 | `## Items` |
| 10 | `## Seed entry` |
| 23 | `## Removed` |
| 25 | tombstone `- ID: TF-20260101-bb (removed …)` |
| **27** | **`## New goal lands in the wrong section`** |
| **29** | **new live `- ID: TF-20260922-5fd629`** |

The new live entry is the last section of the file, **after** `## Removed`.
`todo-check`'s `removed_at` is `sed -n '/^## Removed$/,/^## /p'`, so the range
ends at line 27; the live ID is not currently swallowed as a tombstone when the
new heading is present — but the entry is outside `## Items`'s intended top,
and any future writer that appends fields *without* a fresh `## ` heading (or a
reader that treats “after `## Removed`” as removed territory) sees a live entry
in the deleted region. The todo item also recorded a promote that derived its
task directory from the **previous** entry's heading when the new heading was
not a clean section break.

**Documented convention the code contradicts** — `TaskFlowDocs/todo.md` line 11:

```text
<!-- Add new items at the top using the template below. -->
```

**What is *not* broken:**

- `task get` / `task next` / `task edit` locate by `- ID:` via `findsec`, not by
  “am I under `## Items`”.
- `task remove` already places `## Removed` deliberately: above the first entry
  that has an `- ID:` (lines 321–338), or appends the section when no entry is
  left.
- Duplicate Goal/ID refusal works (smoke: `duplicate goal accepted`).
- Parallel-intake merge driver smoke passes; this fix does not touch merge.

**Same-root secondary issue (out of scope, recorded in the todo Notes):**
`promote` derives the task directory name from the section heading returned by
`get`, and ~23 extra `## ` template headings plus ~30 hand-written titles do
not match Goal. Only `promote` errors when the heading is wrong; `get`/`findsec`
do not care. Deferred as an open question below.

## Requirements

- **R1.** `intake` inserts the new `## <title>` block immediately after the
  `## Items` heading, its blank lines, and an optional leading `<!-- … -->`
  comment — i.e. before the next `## ` line (or EOF if Items has no children).
- **R2.** The new entry never appears after a `## Removed` heading. If
  `## Items` is absent but `## Removed` exists, insert immediately before
  `## Removed` (still not at EOF).
- **R3.** If neither `## Items` nor `## Removed` exists (bare `# Todo inbox`
  fixtures), keep the current append-at-EOF behaviour so existing smoke
  fixtures do not need structural rewrites.
- **R4.** Duplicate Goal/ID refusal, title derivation, and the field template
  stay byte-identical — only the insertion index changes.
- **R5.** `bash hooks/smoke-test` gains at least: (a) with Items+Removed
  fixture, new entry's heading line number is `< Removed`'s and the entry sits
  before the first existing entry heading; (b) `removed_at` range does not
  contain the new ID; (c) bare fixture still accepts intake.

## Acceptance Criteria

- **A.** On the reproduction fixture above, after intake the line order is
  `## Items` → **new `## <title>` + new `- ID:`** → `## Seed entry` →
  `## Removed`; new ID not inside `sed -n '/^## Removed$/,/^## /p'`.
- **B.** `hooks/task get <new-id>` returns the Goal-derived title (section
  heading intake wrote), not the previous entry's title.
- **C.** `bash hooks/smoke-test` → `ALL SMOKE PASSED`.
- **D.** `bash -n hooks/task` clean; no change to `hooks/task` outside the
  `intake` branch's emission (plus any shared helper it needs).

## In Scope

- `hooks/task` — `intake` insertion index only.
- `hooks/smoke-test` — assertions in R5.
- `TaskFlowDocs/todo.md` — promote/status bookkeeping for this task.

## Out of Scope

- `promote` title / Goal alignment (open question in the todo Notes).
- `## Item template` and historical heading cleanup.
- `hooks/todo-check`, `hooks/merge-todo`, remove's tombstone placement.
- The other open todos (`985164` duplicate ID, `4d8ae2` stale close, `b7821b`
  Approval shape).

## Risks / Deferred Items

- Fixtures that intentionally placed an entry at EOF after a non-Items
  structure will keep working via R3; if a fixture has `## Items` *and*
  expected EOF placement, the smoke run will surface it.
- R2's “before `## Removed`” when Items is missing is a narrower rule than
  R1; a file with Removed but no Items is already malformed relative to the
  documented layout.

## Open Questions

1. Should `promote` re-derive or rewrite the section title from Goal so
   directory names stop depending on hand-written headings? — **Recommend: no
   in this PR** (separate todo already covers the title mismatch; changing
   promote here widens blast radius for no intake benefit).
2. Should `intake` refuse a todo.md that has `## Removed` but no `## Items`?
   — **Recommend: no**; R2 inserts before Removed and moves on (ponytail: one
   insertion rule, no new refusal path).

## Version History

- v1 — planning.
- v1 — ready; approved by user 2026-09-22 (R1–R5; Q1/Q2 recommendations
  accepted: no promote-title change, no new refusal when Items is missing).
