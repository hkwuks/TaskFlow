# Compact a closed Todo entry to the fields triage still needs

> Task version: v1
> Status: checking

## Goal

Stop `TaskFlowDocs/todo.md` from growing without bound. A done entry keeps every
field it ever had — the triage fields nobody reads once it is closed, and the
free-form Notes an Agent accumulated while working it. `hooks/archive` is the
one moment the entry is known to be finished, and it is the right place to
reduce it.

Measured on `01a067a` (1.1.6), 1402 lines / 114,226 bytes:

| Part | Bytes | Share |
| --- | --- | --- |
| `done` — 85 entries | 89,554 | 78% |
| `inbox` — 10 entries | 21,538 | 19% |
| `## Removed` tombstones | 8,277 | — |
| preamble, template, template-example headings | 2,857 | — |

Growth is not theoretical: `v1.1.1` carried 55,061 bytes, `v1.1.6` carries
114,186 — roughly a doubling in five weeks, about 12 KB per release.

The cost is no longer "every task reads the whole file": `task intake`,
`task next` and `task get` are all awk-addressed and `summarize-state` skips done
entries outright. What remains is three real costs — an Agent opening the list to
see what is there pays for the archive; every `todo.md` diff and pull-request
review is against 1400 lines; and `merge-todo` materialises one temporary file
per entry per side on every merge.

## Background / Confirmed Facts

All measured in this worktree at `01a067a` on 2026-10-19. Every claim below was
produced by a command, not by reading the hooks and inferring.

**What the readers actually consume.** Each one was read in full:

| Reader | What it reads from a done entry | Survives compaction? |
| --- | --- | --- |
| `hooks/summarize-state:129` | `- Status:` — and `continue`s on `done` | n/a, skips |
| `hooks/todo-check:52` | `- ID:` only, compared as a set across a merge | keeps `ID` |
| `hooks/merge-todo:92` | entry key = `- ID:` first token, else heading | keeps both |
| `hooks/repository-check:101` | `- Task:` path | keeps `Task` |
| `hooks/reopen:108-113` | rewrites `Status`, `Next action`, `Updated` | see Risks |
| `hooks/archive:61-93` | rewrites `Status`, `Next action`, `Task:` | the change lands here |
| `hooks/task:285` (`intake`) | `- Goal:` byte-exact duplicate check | keeps `Goal` |

**The fields being removed are read by nothing.** `grep -rn '"Priority"\|"Owner"\|"Source"\|"Added"\|"Updated"' hooks/` returns two hits, neither of which parses a Todo entry: `hooks/repository-docs-context:165` reads a different file's `Source` field, and `hooks/task:470` *writes* `Updated`. `Priority` is read by no hook at all.

**Notes are not already in `achieved/`.** An earlier reading of this task said
the prose could simply go because the achieved task directory holds it. Measured
against the 16 done entries whose prose survives a sentence split: of **195
sentences, 2 appear verbatim** in the corresponding achieved documents. The Notes
hold the analysis that produced the task — why a mechanism fails, what was
reproduced, what was ruled out — and the Plan records the decision, not the
reasoning. So Notes are **moved** to the achieved Plan before the entry is
compacted, never dropped.

**Capacity check for that move.** 23 done entries carry prose. 22 of them link an
achieved directory that exists. The one that does not is `TF-20260929-3fc4b8`
(`- Task: Not promoted.`), whose Notes are a live verification recipe, and two
more whose `- Task:` is prose about where the work went rather than a path. They
are left byte-identical.

**The legacy entries cannot be addressed.** 19 entries carry their ID only in
the heading (`## TF-20260913-03 — …`) with no `- ID:` line, so `task get
TF-20260913-03` answers `Todo entry not found`, and `merge-todo` keys them by
heading rather than by ID. All 19 headings match
`^(TF|T)-[0-9]{8}-[0-9A-Za-z-]+` cleanly, so the ID is recoverable from the
heading with no guesswork. They are distinct from the three non-entry headings
(`## Item template`, `## Status flow`, `## Items`), which must stay ID-less.

**But seven of those IDs are already in use.** Measured: `TF-20260911-02`
through `TF-20260911-08` identify a *different* live entry each
(`achieved/2026-09-12-current-task-routing/` and siblings) — the old numbering
ran per day-of-work and was reused. Backfilling a heading blindly would make
`task get` answer with the wrong entry, silently. So the backfill declines an ID
that any `- ID:` line in the file already carries, and the affected headings keep
no ID line: 10 of the 19 are backfilled, 7 are left as they are.

**Two structures carry the same title.** The preamble's indented sample entry
opens with `## <goal, cut to 80 bytes>`, and three real done entries open with
`## TF-20260913-03 — <its own title>`. That is why the compaction must be driven
by `- Status: done` inside an entry block and never by shape.

## Requirements

1. **`hooks/archive` compacts the entry it closes.** At the same moment it sets
   `- Status: done`, it reduces the entry to its heading plus `ID`, `Status`,
   `Goal`, `Task`, `Next action` — and appends any Notes to the achieved
   `plan.md` first, under a `## Todo Record` section.
2. **A Notes block is appended once and never duplicated.** Re-running archive,
   or archiving an entry that already carries a `## Todo Record`, must not append
   a second copy.
3. **An entry with no achieved Plan is left untouched.** `- Task: Not promoted.`
   and a `- Task:` that is prose rather than a path give the prose nowhere to go,
   and it cannot stay where it is: a `## Todo Record` heading at column 0 inside
   an entry is a section boundary to every hook that splits on `## `. Measured:
   3 of the 85 done entries are in this shape, and they keep every field.
4. **`hooks/archive` backfills `- ID:` from the heading** when the entry has no
   ID line and the heading starts with `TF-yyyymmdd-…` or `T-yyyymmdd-…`, and
   **only when no other entry in the file already carries that ID**. A heading
   that does not match, or whose ID is taken, keeps no ID line and is otherwise
   untouched.
5. **The backfill and the compaction are one transaction with the directory
   move.** Any failure restores the Todo file from the backup that already
   exists in the script, and the achieved `plan.md` from the backup taken before
   the append; no intermediate state is left on disk.
6. **The migration of the 85 existing done entries is a one-time, verified
   run.** Same five fields, same Notes destinations, same ID backfill — done
   with a reviewed script in this task, not by hand.
7. **Documentation states the shape.** `SKILL.md` §7 and
   `references/artifacts.md` say what a closed entry keeps and where its Notes
   go, so an Agent does not re-add the removed fields.

## Acceptance Criteria

- `task get <id>` works on every entry after the migration, including the 19
  that previously could not be found.
- `todo-check` passes across the migration commit: no `- ID:` is lost, and 19
  are gained.
- `merge-todo` keys every entry by ID, not by heading — verified by building a
  two-branch fixture that edits the same entry on both sides.
- A fresh archive of a fixture task produces exactly the five fields, appends
  its Notes to the achieved `plan.md` once, and leaves every destination-less entry
  with its Notes intact.
- `bash hooks/smoke-test` passes, including the new assertions and the updated
  ones. `bash hooks/repository-check .` and `bash hooks/todo-check .` pass.
- `todo.md` ends under 70 KB, down from 114,226.

## In Scope

- `hooks/archive` — compaction, Notes append, ID backfill, transaction.
- `hooks/reopen` — insert `- Updated:` when the entry no longer carries it, the
  same fallback `archive` already applies to `- Next action:`.
- `hooks/smoke-test` — assertions for each of the three behaviours, plus the
  updated expectations for any existing assertion that greps a dropped field.
- `TaskFlowDocs/todo.md` — the one-time migration of 85 done entries.
- `skills/taskflow/SKILL.md` §7 and `skills/taskflow/references/artifacts.md`
  — the documented shape of a closed entry.
- `TaskFlowDocs/achieved/*/plan.md` — a `## Todo Record` section appended to the
  15 achieved Plans that receive migrated Notes.

## Out of Scope

- Moving `done` to a separate file, or sharding by year. Both were considered
  and rejected: a separate file makes `todo-check`'s lost-entry invariant unable
  to distinguish "moved" from "lost", and every entry is from 2026, so sharding
  buys nothing today.
- Compacting `inbox` entries. They are live; the 10 of them are 21,538 bytes and
  will be worked or closed.
- Changing what `hooks/task intake`, `next`, `get` or `remove` do.
- Rewriting the content of any Notes. They move verbatim.
- `TF-20260929-3fc4b8`'s Notes — it links no achieved directory.

## Risks / Deferred Items

**R1 — `reopen` loses `- Updated:`, and that is a hard break, not a refresh.** `hooks/reopen:113` rewrites the line **only when it is present**; a compacted entry has none. The chain that follows is not cosmetic: `hooks/reopen:182-186` verifies only `Task:`/`Status:`/`Next action:`, so it reports success, and then the documented next step `task state <task> planning` writes a `Status`/`Updated` pair unconditionally (`hooks/task:892-895`) and `loadpairs` dies on the absent field (`hooks/task:167`, `missing Todo field: Updated`). Reproduced by the verification agent on a five-field fixture: `reopen OK`, then exit 1. `hooks/smoke-test:849-852` runs exactly that pair of commands.

Fixed in this task rather than documented: `hooks/archive:83-87` already carries the fallback pattern (`if (!next_i && status_i)` inserts the canonical line when an older entry lacks it), so `reopen` gets the same treatment for `Updated` — one insertion, no new mechanism. An entry that still has the line is untouched, so every existing reopen behaviour is preserved, and `task state` regains the field it requires.

The sibling asymmetry — `task next` inserts a missing `Updated` (`hooks/task:470-472`) while `task state` dies on it — predates this task and is recorded as a follow-up rather than widened into this change.

**R2 — a done entry can be reopened, and reopening now yields a five-field
entry.** That is intended: `reopen`'s own rewrite is what restores `Status`,
`Next action` and `Task:`, `updated` is inserted per R1, and `promote`/`state`
restore the rest as the task moves. Notes do not come back on reopen; they stay
in the achieved Plan's `## Todo Record`, which is where the reopened task's
history already lives.

**R3 — the one-time migration touches 85 entries in one commit.** A mistake
there is a large diff to review. Mitigation: the migration is a script committed
with the task, its output is verified by re-reading every entry with
`task get`, `todo-check` compares the ID set across the commit, and the diff is
reviewed before push.

**R4 — Notes append to Plans that are read-only by policy.** `SKILL.md:110` and
`:305` say a completed task is read-only in `achieved/`. This task appends to 15
of them. That is authorized by the user's decision on 2026-10-19 and is stated
here as an explicit exception: the section is appended, nothing existing is
edited, and no re-approval is implied.

**R5 — a future entry could carry prose that is neither a field nor a Notes
block.** Measured: 15 done entries do. Those paragraphs are part of the Notes
migration: the compaction must treat every continuation line of an entry as
"prose to move", not only lines under `- Notes:`.

## Open Questions

None. The two decisions this task needed were made by the user on 2026-10-19:
compact to the fixed field set (not a separate file, not by year), and move the
Notes into the achieved Plan before removing them from the Todo entry.
