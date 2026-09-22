# Make the task complete / archive transaction fail-safe, print the stage commands, and keep todo.md rewrites byte-tight

> Task version: v1
> Status: ready

## Goal

`task complete` must not leave a half-archived task when `hooks/archive` fails;
`hooks/archive` must tell the Agent exactly what to stage (and on which branch)
without touching Git itself; and the Todo rewrite must not invent blank lines.

Umbrella for the three filed siblings: `e7c041` (fail-safe), `88e04c`
(stage/branch), `172455` (blank lines — not reproduced; lock the good shape).

## Background / Confirmed Facts

Measured on `main` = `e9d4c3c`, 2026-09-22, worktree
`.worktrees/fix-archive-transaction`. Nothing inferred.

**Current `complete` order (`hooks/task` ~816–838):**

1. `require_approval`, unchecked boxes, unfinished steps, achieved-absent, todo
   lookup — all read-only.
2. `docstatus completed` on **plan**, then **prd** — mutations.
3. `hooks/archive` — move dir + rewrite todo.

`hooks/archive` itself requires both docs already `> Status: completed` before
it moves anything. So step 2 is irreversible if step 3 fails: docs say
completed, directory may or may not have moved, todo may or may not have been
rewritten. **Observed twice** (e7c041 Notes): complete failed after mutation;
a later merge overwrote the completed plan back to `pending` and the second
complete refused.

**Stage gap (88e04c Notes, measured):** `hooks/archive` uses `mv`, never
`git add`. After complete, the worktree is delete + untracked add. Agent must
stage both sides; a too-narrow or too-wide `git add` caused dual-directory
commits (`04e808e` redo `ebd6b4f`). Hook-not-touching-Git is a stated design
boundary — printing the exact commands keeps that boundary.

**Branch gap:** no rule for which branch carries the archive commit. Observed
cost: stash → switch → ff → pop on a stale base because complete ran with
`--root` pointing at the base checkout.

**Blank lines (172455):** original report said archive inserts a blank after
the Item template fence and leaves one at EOF. **Not reproduced** on
`2026-09-18-todo-field-writes` (`git diff --check` clean; only Status/Task/Next
action changed). Do not “fix” a guessed bug; lock the three-line-only rewrite
in smoke.

## Requirements

- **R1 (e7c041).** `complete` runs **all** preflight (existing gates plus the
  archive preconditions archive would apply: todo file, `Task:` link, achieved
  absent, both docs exist) **before** any `docstatus` write.
- **R2.** If `hooks/archive` fails after docs were marked completed, `complete`
  **rolls both docs back** to their previous `> Status:` values and exits
  non-zero with the archive message. No half state: either both docs completed
  **and** archived, or docs at the prior status and active dir still present
  (archive’s own failure modes already refuse before `mv` when preflight fails).
- **R3 (88e04c).** On success, `hooks/archive` prints the exact stage lines the
  Agent must run — paths for the removed active dir and the added achieved dir
  — and states: **commit on the current branch** (the task worktree branch);
  do not switch to `main` for the archive commit. Hook still does not invoke
  Git.
- **R4 (172455).** Archive’s todo rewrite changes only `- Status:`, `- Task:`,
  `- Next action:` (plus inserting Next action when absent). No other byte
  changes; no blank line before `## Item template` or at EOF beyond what the
  source already had.
- **R5.** Smoke: (a) force archive failure after docs would be completed →
  both docs restored, active dir intact, non-zero exit; (b) happy path prints
  stage commands containing both paths and the current-branch rule;
  (c) happy path todo diff is only the expected field lines (`git diff --check`
  / structural assert).
- **R6.** `bash hooks/smoke-test` → `ALL SMOKE PASSED`.

## Acceptance Criteria

- **A.** Fixture: make archive fail (e.g. achieved already exists is caught in
  preflight — use a failure after preflight: make `mv` fail via a read-only
  achieved parent or inject archive error by making todo rewrite fail) → docs
  not left `completed` if archive did not finish.
- Simpler reliable fail point: preflight in complete rejects before any write
  when archive would refuse (achieved exists, missing todo link). For
  post-write failure: archive verify step after `mv` — if we cannot inject
  easily, unit-test rollback by stubbing… **ponytail:** make archive fail after
  `mv` by pre-creating achieved as a **file** (not dir) after preflight check
  `[ ! -e achieved ]` passes… ` -e` catches files. Use: create achieved as
  directory with same name after complete’s old preflight but before mv — hard.
  **Practical:** complete’s new code path: if archive returns non-zero, restore.
  Force non-zero by temporarily replacing `hooks/archive` in fixture with a
  script that exits 1 after complete has written docs (fixture-only), OR
  break archive’s verify by making todo unlink… Simplest smoke: run complete
  with `ARCHIVE_FAIL=1` only if we add a test hook — **do not add prod test
  hooks.** Fixture: copy tree, `chmod` achieved parent ro so `mv` fails after
  docs completed — on Linux works; Windows CI may not. **Portable:** archive
  checks achieved-absent first; to fail after docstatus, complete must call
  archive and archive fails on todo missing mid-flight — not available.
  **Chosen:** extract “mark completed + archive + rollback” so smoke can call
  complete against a fixture where `hooks/archive` is a stub `exit 1` on PATH
 … complete uses `$SCRIPT_DIR/archive` absolute path, not PATH.
  **Final approach for A:** put a **failing archive** beside task by running
  complete with a copied `hooks/` tree where `archive` is `#!/bin/sh\nexit 1`
  after a newline comment; SCRIPT_DIR is the copy’s dir. That is fixture-only,
  no production test flag.
- **B.** Stage output names both `TaskFlowDocs/<task>` and
  `TaskFlowDocs/achieved/<task>` and the current-branch sentence.
- **C.** Todo after happy archive: only expected field lines change.
- **D.** Suite green; `bash -n` on changed hooks.

## In Scope

- `hooks/task` `complete` (preflight + rollback).
- `hooks/archive` (stage/branch print; rewrite stays tight).
- `hooks/smoke-test`.
- Sibling todo Next actions already pointed at this task.

## Out of Scope

- Actually running `git add` / `git commit` from hooks.
- Switching branches from hooks.
- Approval automation (`454ac4`), version Approval shape (`b7821b`).
- Guaranteeing 172455’s original blank-line repro (unknown trigger).

## Risks / Deferred Items

- Rollback restores `> Status:` only — if archive partially moved the directory
  before failing verify, rollback of docs alone leaves moved dir. Archive’s
  verify failure after successful `mv` + todo rewrite is the rare half case:
  **mitigate:** archive does todo rewrite only after `mv` succeeds, and verify
  failures attempt `mv` back (best-effort reverse). Include reverse-move on
  archive verify fail (R2 extension).
- Windows `chmod` not available — fixture uses stub archive script, not
  permissions.

## Open Questions

1. Stage: **print exact commands** vs `--stage` flag — **Recommend: print**
   (keeps “hook never touches Git”).
2. Branch: **current worktree branch** — **Recommend: current** (archive
   belongs to the task branch being merged; switching is how the stale-base
   incident happened).
3. 172455 blank-line hunt — **Recommend: no hunt**; only lock R4 (Notes
   already said don’t fix a guess).

## Version History

- v1 — planning.
- v1 — ready; approved by user 2026-09-22 (R1–R6; Q1 print, Q2 current
  branch, Q3 lock R4 only).
