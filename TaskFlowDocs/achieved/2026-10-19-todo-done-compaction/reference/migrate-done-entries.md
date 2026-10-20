# The one-time migration that compacts the 85 done entries

Run once, from the repository root, with `todo.md` at the revision the numbers
below were measured at. It applies the same three rules `hooks/archive` now
applies to a live archive, in the same order:

1. **Backfill `- ID:`** from the heading, for a done entry whose heading starts
   with `TF-yyyymmdd-…` or `T-yyyymmdd-…` and that has no `- ID:` line.
2. **Move the prose** — every non-blank line inside the entry that is not a field
   line, plus the value on a `- Notes:` line — into
   `TaskFlowDocs/achieved/<task>/plan.md` under `## Todo Record`.
3. **Compact the entry** to its heading plus `ID`, `Status`, `Goal`, `Task`,
   `Next action`.

An entry whose `- Task:` is not a backticked `TaskFlowDocs/achieved/...` path has
no destination and keeps its prose; only its triage fields go. Measured: one
entry is in that shape (`TF-20260929-3fc4b8`).

## What it asserts before writing anything

- Every done entry still exists after migration, by ID set: nothing removed.
- Every `- Task:` path that the migration touched still resolves to a directory.
- The Plan it appends to exists, and already ends without a `## Todo Record`
  section (a second run is refused rather than duplicating).
- `wc -c` before and after, printed, so the reduction is a measurement rather
  than a claim.

It writes the Plan changes first and the Todo file last, each through a temp file
and a rename, so a failure cannot leave a Todo entry that has lost prose which
never landed anywhere.
