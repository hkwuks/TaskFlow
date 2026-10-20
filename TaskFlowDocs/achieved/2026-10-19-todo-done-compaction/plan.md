# Plan — Compact a closed Todo entry to the fields triage still needs

> Task version: v1
> Status: completed

No `spec.md` — small task: one hook changes behaviour, one file is migrated, two documents state the shape. No new interface, no new data format on disk that another component parses, and the reader side is unchanged by construction.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — routing for `CONTRIBUTING.md` (design, code, commit, pr, release) and `CODE_STYLE.md` (code, review).
- `hooks/archive:1-19` — the transaction's preconditions and the promise that Git is never invoked.
- `hooks/archive:41-95` — the `mv`, the in-place Todo rewrite through `awk`, and the three-field edit (`Status`, `Next action`, `Task:` path).
- `hooks/archive:20-38` — `rollback`, which restores both the directory and the Todo file.
- `hooks/task:94-96` (`isfield`) and `:147-158` (`notes_end`) — the existing definition of where a Notes block ends. The compaction must agree with it, not invent a second rule.
- `hooks/task:545-555` (`entry`) — `task get` already prints "every non-blank line", so it must keep working on a compacted entry and on a backfilled one.
- `hooks/merge-todo:92-109` (`key_of`) — the ID key. Compaction and backfill both change which key an entry produces.
- `hooks/reopen:104-116` — the reader that rewrites three fields, one of which compaction removes.
- `skills/taskflow/SKILL.md:299-311` (§7) and `skills/taskflow/references/artifacts.md` (Todo field list) — where the documented shape belongs.
- `CONTRIBUTING.md` — branch prefixes (`chore/`), one task one worktree, and that a task's documents land in its own pull request.

## Related Tasks

- Parent: None.
- Children: None.
- Depends on: None.
- Blocks: None.
- Related:
  - `2026-09-22-todo-intake-insert` (done) — fixed `intake`'s insertion point relative to `## Removed`; this task does not touch insertion.
  - `2026-09-22-merge-todo-removed` (done) — the tombstone/live-entry keying this migration makes consistent.
  - `2026-09-22-task-get-notes` (done) — `task get` printing indented continuations; the ID backfill relies on `findsec` matching by ID, which this task makes reachable for the 10 heading-derived IDs it backfills.
  - `TF-20261011-e27329` (inbox) — single history owner across prd/plan/spec. Adjacent: this task creates one new record section in `plan.md`, and that entry would decide who owns records like it.

## Skills / Tools Used

- [PRD] `general-purpose` — purpose: adversarially verify that no reader depends on a field the compaction removes, and locate every smoke assertion that would break; outcome: succeeded; incorporated: confirmed-risks folded into `## Risks / Deferred Items` R1 (reopen's `Updated`), and the smoke-assertion inventory folded into Step 2's checklist.
- [Plan] Unaided — no capability applied to this phase; considered: work breakdown and task decomposition.

## Preconditions

- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded. `repository-docs/index.md` routes `CONTRIBUTING.md` (design, code, commit, pr, release) and `CODE_STYLE.md` (code, review). No repository document specifies the Todo entry's field set; `artifacts.md` lists the fields to maintain, which this task narrows for a closed entry. No `personal.md` in this clone.
- [x] For remote/fork/PR work: `origin` = `hkwuks/TaskFlow`, base = `main`. This branch `chore/todo-done-compaction` starts from `01a067a` (= `origin/main` at branch time). Re-checked before any push.
- [x] For PR creation/update: `.github/pull_request_template.md` read and mapped field by field in Step 4.
- [x] Missing governance drafts and explicit approvals: not applicable — no governance document is created.
- [x] Single writer for core documents: Primary Agent (Claude). Worktree `.worktrees/todo-done-compaction`, branch `chore/todo-done-compaction`.
- [x] Isolation before the first document: the worktree and branch existed before any `TaskFlowDocs/2026-10-19-todo-done-compaction/` file; `promote` ran inside it.
- [x] Existing user rulings recorded: 2026-10-19 — (a) compact to a fixed field set rather than a separate file or year shards; (b) move the Notes into the achieved `plan.md` before removing them; (c) fold the missing-ID backfill into this task. See PRD `## Open Questions`.
- [x] The measured premise re-verified in this worktree, not carried over: `wc -l -c TaskFlowDocs/todo.md` → `1402 114226`; `awk` over entry blocks → `done` 85 entries / 89,554 bytes; `v1.1.1`…`v1.1.6` blob sizes 55,061 → 114,186.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-19 23:34 +0800
- Approved version: v1
- Approved scope: PRD / Plan

> 2026-10-19: this block was approved by `hooks/task approve` at 23:18 before the
> user had read the Plan. It is reset to `requested` because the approval was a
> side effect of checking the gate, not a decision — the Plan has not been read
> by the user yet. Re-approval is requested above.

## Steps

### Step 1 — `hooks/archive` compacts, moves Notes, and backfills the ID

- Goal: the one place an entry is known to be finished reduces it, in the same transaction that moves the directory, and nothing is lost that has no other home.
- Dependencies: none.
- Files: `hooks/archive`, `hooks/reopen`.
- Implementation checklist:
  - [x] **The print loop covers the whole file.** `hooks/archive:88-91` prints every line; the field filter must be scoped to `start+1 … finish-1` or it strips unrelated entries.
  - [x] **Synthesise, do not reuse the insertion fallback.** `status_i` / `next_i` and the `if (!next_i && status_i)` block at `:83-87` insert into an array the new emitter will no longer print line-for-line. The new emitter writes `- Status: done` and `- Next action: None — completed and archived.` itself, so an entry that never had either still ends up with both.
  - [x] **The `Task:` path rewrite still has to happen.** `gsub` at `:89` currently applies to every line; the retained `Task:` line must carry it.
  - [x] The entry's block is located the way the script already locates it (the last `## ` heading at or before the line carrying the task's path link), not by shape.
  - [x] Prose collection follows `hooks/task`'s own rule: a field line is `^- [A-Za-z][A-Za-z ]*:`; every non-blank line that is not a field line belongs to the field above it. Prose is collected for **every** field block, not only `Notes` — measured: 3 done entries carry prose under `- Next action:`. Two of those three sit in the **same entry** as a `- Notes:` block, so one entry can contribute two records and the migration has to keep them apart rather than merge them.
  - [x] Before rewriting, if the entry has prose and its `- Task:` is not `Not promoted.`, append `## Todo Record` + the prose verbatim to the achieved `plan.md`. Append, never edit: if the file already ends with a `## Todo Record` section, append nothing (idempotent re-run).
  - [x] Rewrite the entry to its heading plus `- ID:`, `- Status: done`, `- Goal:`, `- Task:`, `- Next action:`, in that order. Keep the heading untouched.
  - [x] Prose is removed only after it was written to the achieved Plan. There is no "keep it in the entry" shape: a `## Todo Record` at column 0 inside an entry would be read as a new section by every hook that splits on `## `. An entry with no destination is therefore left exactly as it is — measured during the migration, 3 of the 85 done entries are in that shape (`Not promoted.`, and two whose `- Task:` is prose about where the work went).
  - [x] Backfill `- ID:` immediately after the heading when the entry has no ID line and the heading is `## TF-yyyymmdd-…` or `## T-yyyymmdd-…`. A heading that does not match gets no ID line and is otherwise handled as today.
  - [x] Order of operations inside the existing transaction: `mv` directory, append Notes to the achieved Plan, then rewrite `todo.md`. A failure in any of them calls the existing `rollback`, which today restores the directory and the Todo file. Extend it to also restore the achieved `plan.md` from a backup taken before the append — one more file in the same rollback, not a second mechanism.
  - [x] Verification block extended: after the rewrite, assert the compacted entry has exactly the five fields, that the achieved Plan holds the record when prose existed, and that the ID line is present.
  - [x] The script still invokes no Git and prints the same stage lines.
  - [x] `hooks/reopen` gets the same fallback `archive` already has for `- Next action:` — when the entry carries no `- Updated:` line, insert one instead of skipping the refresh. This is not cosmetic: `reopen`'s own verification passes without it, and the next `task state` then dies at `hooks/task:167` with `missing Todo field: Updated`. An entry that still has the line is untouched.
  - [x] The migration and the ID backfill land in **one commit**. `merge-todo` keys an ID-less entry by heading; the backfill flips 19 entries from `head:` to `id:`. Split across commits, a merge spanning the boundary conflicts on all 19. Checked for collisions: the 19 heading-derived IDs collide with neither the 86 existing IDs nor the 15 tombstones.
- Acceptance: a fixture task archived by the hook ends with a five-field entry, a `## Todo Record` in its achieved Plan, and — for a fixture with no ID — a backfilled ID line. Re-running the archive on the same fixture is refused by the existing `achieved/$task already exists` guard before anything is appended. Reopening a compacted fixture restores `Status`, `Next action`, `Task:`, writes `- Updated:`, and `task state` then succeeds.
- Verification: new smoke sections (Step 2) plus a manual fixture run.
- Rollback: revert the file; the change is additive inside one script.
- Status: done

### Step 2 — smoke-test pins every direction

- Goal: each new behaviour reddens on its own when removed, and no existing assertion silently stops meaning anything.
- Dependencies: Step 1.
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] New section: archiving a fixture task compacts the entry to exactly the five fields — assert the presence of each and the **absence** of `- Priority:`, `- Owner:`, `- Source:`, `- Added:`, `- Updated:`, `- External:` and `- Notes:` in that entry.
  - [x] New section: the prose arrives in the achieved `plan.md` under `## Todo Record`, byte-identical to the entry's prose; and the entry no longer carries it.
  - [x] New section: an entry whose `- Task:` is not an achieved path is left byte-identical, then `archive` refuses it (it cannot reach a destination), and the suite says so rather than aborting.
  - [x] New section: an entry with no `- ID:` and a matching heading gains one, and `task get` then finds it; a heading that does not match gains none.
  - [x] Rewrite every existing assertion the compaction invalidates. Two are known and both encode today's three-line rewrite rather than the new shape:
    - `== archive todo rewrite only touches Status/Task/Next action ==` (`hooks/smoke-test:731`) — its diff filter allows only those three lines and its fixture carries `- Updated:`, which the compaction removes.
    - `== archive happy path ==` (`:637`) — `:647` asserts the line **after** `- Status: done` is `- Next action:`, so any field order with `Goal:` between them reddens it.
  - [x] Leave the live-entry assertions alone: `== task next writes the deterministic Todo fields … ==` (`:2939`) and `== a Todo entry names the host that created it as its owner ==` (`:1103`) grep fields the compaction removes, but they exercise live entries via `task next` / `intake`, which are unchanged. They must keep passing untouched — that is the evidence the change is scoped to `archive`.
  - [x] `hooks/reopen` gains one assertion of its own: reopening a compacted entry (no `- Updated:` line) produces an entry with `- Status: promoted`, the restored `Next action`, the active `Task:` path, and a fresh `- Updated:` line. The existing reopen section keeps passing unchanged, which is what proves the fallback did not alter the branch that already had the line.
- Acceptance: `bash hooks/smoke-test` passes; each new section fails when its behaviour is removed (mutation-checked one at a time).
- Verification: the full suite, then each mutation.
- Rollback: revert the file.
- Status: done

### Step 3 — migrate the 85 existing done entries once

- Goal: the same shape applied to the archive that already exists, with the same Notes destinations, verified rather than trusted.
- Dependencies: Steps 1 and 2 (the migration reuses the hook's rules; the assertions in Step 2 are what make the shared code trustworthy).
- Files: `TaskFlowDocs/todo.md`, `TaskFlowDocs/achieved/*/plan.md` (15 distinct Plans).
- Implementation checklist:
  - [x] Write the migration as a small script under the task's `reference/` directory, committed with the task so the transformation is reviewable — not run once from a shell history.
  - [x] Before: record `wc -l -c`, the count of `- ID:` lines (85 + live), and the sorted ID set. After: assert the ID set is the old set ∪ the 19 backfilled, with nothing removed.
  - [x] Apply the same three rules as Step 1 in the same order: backfill ID, append prose to the achieved Plan, compact.
  - [x] Leave every entry with no achieved Plan untouched — measured, 3 of the 85 (`TF-20260929-3fc4b8` with `- Task: Not promoted.`, and `T-20260909-001`/`T-20260909-002` whose `- Task:` is prose). The exclusion is by destination, not by ID.
  - [x] Exclude the three non-entry headings (`## Item template`, `## Status flow`, `## Items`) and the indented sample entry: none is followed by a `- Status: done`.
  - [x] After: `bash hooks/task get` on all 19 backfilled IDs, and a byte-level look at three migrated entries of different shapes (prose with `Notes`, prose under `Next action`, prose-free).
  - [x] After: `bash hooks/todo-check .` and `bash hooks/repository-check .` both report pass.
- Acceptance: `todo.md` under 70 KB; every ID addressable; prose present in the achieved Plans and absent from the Todo entries that were migrated.
- Verification: the before/after ID-set diff, `todo-check`, `repository-check`, `task get` on the backfilled IDs, and the suite from Step 2 run again on the migrated tree.
- Rollback: the migration commit is one commit; `git revert` restores both the Todo file and the appended Plan sections together.
- Status: done

### Step 4 — state the shape, then open the pull request

- Goal: the document that defines the Todo entry says what a closed one looks like, so the removed fields are not re-added by the next Agent; and the work lands through the repository's own PR path.
- Dependencies: Steps 1–3.
- Files: `skills/taskflow/SKILL.md` (§7 and the Todo paragraph at `:148`),
  `skills/taskflow/references/artifacts.md`,
  `TaskFlowDocs/2026-10-19-todo-done-compaction/*`,
  `TaskFlowDocs/todo.md` (this task's own entry, archived at the end).
- Implementation checklist:
  - [x] `SKILL.md` §7 states, as part of the archive transaction, that the linked entry is compacted to five fields, that its Notes move to the achieved Plan's `## Todo Record`, and that an entry with no achieved directory keeps its Notes.
  - [x] `artifacts.md`'s Todo field list distinguishes a live entry's fields from a closed one's.
  - [x] The `## Todo Record` section name is added to `artifacts.md`'s list of headings a hook matches — it is not hook-matched, so it belongs to the prose side; state which it is rather than leaving it ambiguous.
  - [x] Archive this task; the archive commit lands on this branch, in this pull request, per `CONTRIBUTING.md`.
  - [x] PR body follows `.github/pull_request_template.md`: Summary, TaskFlow traceability with the file table, Verification with the run and its result, Review boundaries, and a Landing claim naming the commits.
  - [x] Record the merge topology as a check, not a promise: "after merge, `repository-check` reports `Stale task worktrees: none`" — a fact that only exists after the merge and therefore is checked, not written back.
- Acceptance: the documents match the shipped behaviour; CI green on all six jobs; the PR body's fields all filled.
- Verification: `quick_validate.py skills/taskflow`, `bash hooks/release-check`,
  `git diff --check`, and the CI run.
- Rollback: revert the commits; the documents and the hook move together.
- Status: done

## Checkpoints

- After Step 1: a fixture archive run inspected by hand before any test is written — the shape is decided by looking at real output, not by asserting the shape the code happens to produce.
- After Step 3: the before/after ID set diff reviewed before the migrated tree is committed.
- Before the PR: the whole suite run on the migrated tree, not on a fixture.

## Verification / Review

- 2026-10-20 Step 4: SKILL.md 7 + artifacts.md updated; quick_validate Skill is valid

- 2026-10-20 Step 3: todo.md 114226 -> 64938 bytes; 0 IDs lost, 10 backfilled; todo-check pass

Work done in this worktree at `01a067a`, on branch `chore/todo-done-compaction`.
Every number below is a command output, not an estimate.

### The suite, and the two assertions that had to change

`bash hooks/smoke-test` — exit `0`, **80 `ok` sections** (76 before; four new).
The two existing assertions the compaction invalidated were both encoding the
old three-field rewrite, and each was rewritten to assert the new invariant
rather than relaxed:

| Section | Was | Now |
| --- | --- | --- |
| `archive happy path` | the line after `- Status: done` must be `- Next action:` | the compacted entry must contain it — adjacency was asserting field order |
| `archive todo rewrite only touches Status/Task/Next action` | every changed line is one of three fields | everything outside the entry is byte-identical, and every line removed inside it must appear on the achieved Plan |

Both bare `archive` calls in fixture sections were also guarded. Under
`set -e` an unguarded failing hook aborts the whole suite with no message: the
log simply stops mid-section. That is how the first M2 mutation looked —
green through `membership…` and then nothing — so the guard is part of the fix,
not a tidiness pass.

### Nine mutations, nine distinct assertions

Applied one at a time to a copy of the tree under `/tmp`, each restored before
the next.

| # | Mutation | Red at |
| --- | --- | --- |
| 1 | never write the prose to the Plan | `FAIL archive changed a line inside the entry that it neither kept nor moved` |
| 2 | keep the old fields alongside the new | `FAIL archive failed on the happy-path fixture` (its own verification refuses) |
| 3 | disable the ID backfill | `FAIL archive did not backfill the ID from the heading` |
| 4 | remove `reopen`'s `Updated` insert | `FAIL reopen did not write Updated into a compacted entry` |
| 5 | always insert, even when the line exists | `FAIL reopen left two Updated lines` |
| 6 | emit the whole original body after the five fields | `FAIL archive failed on the happy-path fixture` |
| 7 | leak one triage field, verify relaxed | `FAIL the compacted entry is not the five fields in order` |
| 8 | drop the `- Notes:` value, keep the continuations | `FAIL the Notes value did not reach the achieved Plan` |
| 9 | drop the blank line after the heading | `FAIL archive changed a line inside the entry that it neither kept nor moved: <blank line>` |

Two of these found holes in the *tests*, and the tests were fixed before the
mutation was rerun:

- **M2 first read as a bare `exit 1` with no line.** The failing archive never
  printed which assertion it broke, because the fixture call was unguarded. The
  guard now names the fixture.
- **M9 passed on the first attempt.** The moved-line check skipped blank lines,
  so a dropped separator was indistinguishable from prose that moved. Blank
  lines are now reported by name.

### The migration

`reference/migrate-done-entries . --apply`, dry-run first on a copy:

| | Before | After |
| --- | --- | --- |
| `todo.md` | 1402 lines / 114,226 bytes | 924 lines / 64,938 bytes (**−43%**) |
| `done` entries compacted | 85 | 82 — 3 left untouched |
| Plans given a `## Todo Record` | 0 | 22 |
| IDs | 86 | 96 — 10 backfilled, **0 lost** |

Verified across the migration:

- `comm` on the sorted ID set before and after: nothing lost, the 10 gained are
  exactly the heading-derived ones.
- `bash hooks/todo-check .` → `STATUS: pass` over both parent commits.
- `bash hooks/task get T-20260908-001` → the entry, which was unreachable before.
- All 79 `- Task:` paths still resolve to a directory.
- `bash hooks/smoke-test` → exit 0, 80 `ok`, **on the migrated tree**.
- `git diff --check` → clean.

The three untouched entries are excluded by destination, not by ID:
`TF-20260929-3fc4b8` (`- Task: Not promoted.`) and `T-20260909-001` /
`T-20260909-002`, whose `- Task:` is prose about where the work went.

### What the migration found that the Plan did not predict

**Seven heading IDs collide with a real ID on a different entry.** The old
numbering ran per day-of-work and was reused, so `## TF-20260911-02 — Allow
appropriate tools…` sits beside `- ID: TF-20260911-02` on an unrelated entry
(`achieved/2026-09-12-current-task-routing/`). Backfilling those would have made
`task get` address the wrong entry, silently. The backfill therefore checks the
whole file and declines a taken ID; the affected headings keep no ID line, which
is exactly their state today.

**Three more `- Task:` values are not paths** — two are prose. The destination
rule is "a backticked achieved path whose `plan.md` exists", not "matches
`Not promoted.`", and the dry run is what showed the difference.

**A `(vN)` suffix sits beside the path, not inside it**
(`…/2026-09-15-hook-integrity/` (v2)`), so the path itself still resolves. The
first pattern required a closing backtick at end-of-line and silently skipped
that entry; the dry-run count caught it.

### Document state

PRD and Plan were restored after the migration rewrote them: `todo.md` is the
file being compacted, and this task's own entry lives in it. The migration
touched its entry in the working tree and `git checkout` reverted that together,
so the documents were reinstated from a copy and `promote` re-ran. The Plan's
`## Approval` block is the user's real approval from 23:34, not a re-approval.

- 2026-10-20 Step 2: 80 ok sections; suite green before and after the migration

- 2026-10-20 Step 1: fixture runs; 9 mutations each red on a distinct assertion

Filled in as the work is done, per `CONTRIBUTING.md`: the commands run, their
exit codes, the mutation table, and the CI run that verified the final commit.

## Change Log

- 2026-10-19 v1 — Plan written for a small task; no spec.
- 2026-10-19 v1 — `reopen`'s missing `- Updated:` moved from a documented risk to in-scope after it was reproduced as a hard failure (`reopen OK`, then `task state` → `missing Todo field: Updated`).
- 2026-10-19 v1 — destination-less entries changed from "compacted, prose kept" to "left untouched": an in-entry `## Todo Record` is a section boundary to every hook, so that shape does not exist. Measured 3 of 85.
- 2026-10-19 v1 — ID backfill gained a collision check; 7 heading IDs are already taken by another entry.

## Follow-ups

- **`task state` dies where `task next` inserts.** `hooks/task:167` (`loadpairs`) fails an entry with no `- Updated:` line, while `task next` inserts one (`hooks/task:470-472`). Reopen's fallback (Step 1) closes the path this task creates, but the asymmetry predates it and any hand-written entry can still hit it. Its own entry rather than a silent widening here.
- **`task get` output shrinks for a done entry** from the full body to five fields (`hooks/task:550-555` prints every non-blank line). Nothing asserts a dropped field on a done entry, so no test reddens — an unasserted contract change, recorded so the shrink is deliberate rather than discovered.
- **`intake`'s duplicate-Goal check is load-bearing on done entries.** `hooks/task:285` is byte-exact across every entry with no status filter; the `ID` fallback at `:289` is date-scoped and cannot replace it. This is the reason `Goal` is one of the five retained fields; removing it later would silently weaken dedup for archived work.
- `TF-20261009-8abbd6` and `TF-20261012-c66ad3` are untouched here: this task changes the Todo file's shape, not the capability ledger.
- Whether `reopen` should restore the other removed triage fields (`Priority`, `Owner`, `Source`, `Added`) is a separate question, and it is not the same as `Updated`: `Updated` is a mechanical field the lifecycle maintains, while those four are intake facts whose value after a reopen is not obvious. They stay removed until a reopened task actually needs one.

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-09-19 用户提出，明确排除在本次修复范围外**（「先立一个 todo，我后面研究修复」）。
- 2026-10-19 用户裁定，方案 C（done 收成固定字段），并把无 ID 老条目并入本任务。实测 main 01a067a：1402 行 / 114226 字节，done 85 条 89554 字节（78%）。保留字段取标题+ID+Status+Task+Next+Goal 一档，迁移后约 66323 字节（原 114226，降 42%）。三个后续裁定：Notes 不丢弃而是搬到 achieved plan.md 的 ## Todo Record；reopen 缺失 - Updated: 是硬故障（reopen 自检通过，随后 task state 在 hooks/task:167 上 missing Todo field: Updated），一并修掉；无 achieved 目录的条目整条不动，因为列 0 的 ## Todo Record 会被所有 hook 当成新 section。读侧 hook 全部零改动。已否决：搬去单独文件（todo-check 的丢条目不变式无法区分移动与丢失）、按年份拆分（85 条全在 2026 年）。
  **实测分布**（HEAD `c1147ab`，877 行 / 50,427 字节，按条目正文统计）：`done` 47 条 / 22,661 字节（45%）；`inbox` 12 条 / 14,194 字节；`in_progress` 4 条 / 3,422 字节；`promoted` 2 条 / 991 字节；模板与无法解析的 4 段 / 384 字节。**待每天打交道的 live 条目只有 18 条、不到三分之一。**
  **两个已观测到的结构损伤**（不只是「长」）：(1) `## Item template` 模板块停在第 251 行，**在条目中间**，其下还有条目，随后第 267 行是一句被截断的半句 `Every direct request or imported requireme`；(2) 条目顺序是三个时代的堆叠，不是严格新在前——`TF-20260919-*` 的若干条排在 `TF-20260918-*` 之下。
  **已排除的选项**：本文件的定义是 intake 清单（`SKILL.md:30`、`references/artifacts.md:9` 都写 triage metadata only），历史事实在 `TaskFlowDocs/achieved/`，且 `SKILL.md:44` 禁止第二份事实源——所以往 todo.md 里做归档是反方向的。按日期分片/换后端会把整套 hook（`hooks/archive`、`hooks/summarize-state`、`hooks/todo-check`、`hooks/merge-todo`、`hooks/task`）都改一遍。
  **读取代价已被 v1.0.7 砍掉一半**：`hooks/task get <todo-id>` 只回一条条目，`task next` / `task intake` 只写一条，所以「查/改」不再需要读全文；剩下的整读场景只有「新增条目」。（本条由 `hooks/task next` 写入，未手改。）
