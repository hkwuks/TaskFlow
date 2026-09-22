# Fix `task get` silently dropping indented Notes continuation lines

> Task version: v1
> Status: ready

## Goal

`hooks/task get` prints every non-blank line of the entry body, so Notes
continuations and other non-column-0 content are no longer omitted without a
warning.

## Background / Confirmed Facts

All measured on `main` = `2dfffe3` (PR #48 merged), 2026-09-22, in worktree
`.worktrees/fix-task-get-notes`. Nothing here is inferred.

**Root cause (`hooks/task` `entry` branch, the CLI `get`):**

```awk
for (i = a; i <= b; i++) if (at(line[i], "- ")) print line[i]
```

`at(s, p)` is `index(s, p) == 1`, so only lines whose **first two characters**
are `- ` are printed. Everything else in the entry body is dropped.

**Live reproduction** (fixture with a three-line Notes block):

| In file | In `get` output |
|---|---|
| `- Notes: first line` | yes |
| `␣␣- second line indented` | **no** |
| `␣␣- third line indented` | **no** |

Real entries also carry Notes continuations that are indented prose with **no**
dash at all (e.g. `TF-20260918-454ac4` Notes bullets after the first line are
`  **…**` / `  …`). Those are dropped by the same filter.

**Why it matters:** `get` exists so a caller reads one entry instead of the
whole file. A silent short read looks complete; the caller then decides on a
truncated Notes block. The todo item records the same finding: hazard is the
absence of any warning, not an error.

**What `get` must keep (existing smoke, `== task get prints one entry… ==`):**

- field lines verbatim, in file order;
- no sibling entry, no `## ` heading, no blank line, no file header;
- positional parse (`awk '{print $NF}'` on `- ID:`) still works;
- read-only.

Printing every non-blank line in the section body `[a, b]` satisfies all of
those: headings sit outside `[a, b]` (`bend` is the next `## ` minus one), and
blanks are filtered.

**Related but out of scope:** `notes_end` (used by `task next` when appending
a bullet) only continues on column-0 `- ` lines, so an indented Notes line ends
the block early and the next bullet can land mid-block. Same family, write
path; not required to fix `get`.

## Requirements

- **R1.** `entry` (CLI `get`) prints every line in the entry body that is not
  blank, in file order, verbatim — fields, Notes header, Notes continuations
  (indented or not), no other filtering by prefix.
- **R2.** No change to internal `TASKFLOW_CMD=get` (title + selected keys);
  three internal callers keep that shape.
- **R3.** Smoke: fixture Notes block with an indented `- ` continuation **and**
  an indented no-dash line; `get` output contains both; still no blank/heading;
  existing get section stays green.
- **R4.** `bash hooks/smoke-test` → `ALL SMOKE PASSED`.

## Acceptance Criteria

- **A.** Reproduction fixture: `get` prints all three Notes lines.
- **B.** Existing get assertions (verbatim slice ID→Updated, no sibling, no
  heading, no blank, positional ID, read-only, unknown ID fails) pass.
- **C.** `bash -n hooks/task` clean; only the `entry` branch changes.
- **D.** `bash hooks/smoke-test` → `ALL SMOKE PASSED`.

## In Scope

- `hooks/task` — `entry` branch only.
- `hooks/smoke-test` — R3 assertions beside the existing get section.
- Task documents for this item.

## Out of Scope

- `notes_end` / `task next` indent handling (related write-path note above).
- `TASKFLOW_CMD=get` internal shape.
- Title/heading alignment, archive family, Approval shape.

## Risks / Deferred Items

- Printing all non-blank body lines will also print a future non-field line a
  hand edit puts inside an entry (e.g. a stray `foo`). That is still better
  than dropping it: `get` is a raw body read, not a schema printer.

## Open Questions

1. Alternative (b) in the todo — stderr warn instead of print — **Recommend:
   no.** A warning still leaves the caller without the data; printing the body
   is the smaller correct contract.
2. Fold `notes_end` indent fix into this PR? — **Recommend: no** (separate
   write path; keep the diff to `entry` + one smoke block).

## Version History

- v1 — planning.
- v1 — ready; approved by user 2026-09-22 (R1–R4; Q1=a print body, Q2 no
  notes_end change).
