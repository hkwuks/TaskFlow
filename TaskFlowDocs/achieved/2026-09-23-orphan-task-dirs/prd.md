# Detect a task directory that no Todo entry references

> Task version: v1
> Status: completed

## Goal

`hooks/repository-check` reports every task directory (active and
`achieved/`) whose path no `- Task:` line in `todo.md` names — a lost Todo
record must not leave orphaned documents invisible. Report only; the hook
never moves or deletes files.

## Background / Confirmed Facts

Measured on `main` = `5eba691`, 2026-09-23, worktree
`.worktrees/feat-orphan-task-dirs`. Nothing inferred.

**Incident (Notes, 2026-09-16):** while staging PR #28 for one task, Todo
entries for B/C/D were stripped; `git checkout -- TaskFlowDocs/todo.md`
then restored the file, but for a window the three directories had **no
Todo reference** (workspace only; restored same day). Historical example
still true on this tree: `TaskFlowDocs/achieved/2026-09-10-repository-document-placement/`
— never had a Todo entry in any commit.

**Direction (Notes):** only **directory → Todo**. Reverse (Todo → missing
directory) was measured empty on 2026-09-16; not part of this check unless
it costs nothing extra (see Open Questions).

**`ab381b` (done)** fixed isolation-before-documents and taught
`repository-check` to list **uncommitted** task artifacts. Those lines never
set `needs`. They do **not** answer “directory exists, Todo forgot it” —
committed and archived orphans are invisible to that loop today
(`TaskFlowDocs/*/` only, and only when not in `HEAD`).

**`repository-check` shape (hooks/repository-check):** read-only; artifact
section prints and leaves `needs` alone; final `STATUS: pass` (0) or
`needs-user-input` (2). Existing smoke sections: general status + uncommitted
artifacts without changing verdict.

**Todo `Task:` values that *do* reference a directory** (backticked):

- `TaskFlowDocs/<task>/`
- `TaskFlowDocs/achieved/<task>/`

Non-references: `Not promoted.`, `None — …`, template placeholders.

**Task directory =** has `prd.md` or `plan.md`. That already skips
`repository-docs/`, `todo.md`, and `achieved/` itself. Must also scan
`TaskFlowDocs/achieved/*/` — current loop does not.

**Survey on `5eba691`:** with that rule, **0 active + 0 achieved orphans**
among dirs that have core docs *except* the known historical achieved dir
if its Task: is still missing — counted in implementation smoke fixtures,
not by mutating real history here. (Fixture-driven; live tree may report
the known achieved orphan until a human adds a tombstone or accepts the
line.)

## Requirements

- **R1.** In `hooks/repository-check`, after the uncommitted-artifacts
  section (or adjacent), report **orphan task directories**: every
  `TaskFlowDocs/<id>/` and `TaskFlowDocs/achieved/<id>/` that has `prd.md`
  or `plan.md`, for which no `- Task:` line in `TaskFlowDocs/todo.md` equals
  that path with or without a trailing backtick slash.
- **R2.** Read-only. Never delete, move, or rewrite Todo/dirs.
- **R3.** Orphan findings **set `needs=1`** (STATUS `needs-user-input`,
  exit 2) — a lost Todo record is actionable integrity, unlike the
  informational uncommitted-artifact lines which stay `needs`-neutral.
- **R4.** Empty orphan set → no behavior change vs today for that condition
  (does not by itself fail a clean repo that already passes).
- **R5.** Output names each path once under a clear heading (e.g.
  `Orphan task directories:`) with one path per line.
- **R6.** Smoke: (a) fixture with an unreferenced active dir → report lists
  it, status 2; (b) same dir referenced by `- Task:` → not listed; (c)
  achieved/ orphan listed; (d) clean fixture with only referenced dirs →
  no orphan section / still pass when nothing else is wrong; (e) existing
  repository-check sections still green.
- **R7.** `bash hooks/smoke-test` → `ALL SMOKE PASSED`.

## Acceptance Criteria

- **A.** Fixture `TaskFlowDocs/2026-01-01-lost/{prd,plan}.md` + Todo with no
  matching `Task:` → line contains that path; exit 2.
- **B.** Add `- Task: \`TaskFlowDocs/2026-01-01-lost/\`` → path gone from
  orphan list.
- **C.** `TaskFlowDocs/achieved/2026-01-01-gone/` with core docs, no Task:
  → listed.
- **D.** Uncommitted-artifact fixture still reports staged/untracked and
  does not require an orphan to exercise that path.
- **E.** Suite green; `bash -n hooks/repository-check`.

## In Scope

- `hooks/repository-check` orphan report.
- `hooks/smoke-test`.

## Out of Scope

- Auto-delete or auto-repair orphans.
- Reverse check (Todo → missing dir) as a hard requirement (optional
  freebie only if free; see Q2).
- New hook binary.
- Changing uncommitted-artifact `needs` neutrality.
- Rewriting historical achieved records to invent Todo entries.

## Risks / Deferred Items

- Known historical achieved orphan may turn real repos to exit 2 until a
  human records a tombstone/entry — **mitigate:** report is accurate;
  fix is data, not code. Note in Change Log if live survey trips.
- `Task:` written without backticks would be missed — current repo uses
  backticks for real paths; match backticked form only (R1) unless a
  non-backticked path appears (survey: none for real dirs).

## Open Questions

1. Orphan sets `needs` — **Recommend: yes (R3)**; distinct from uncommitted
   artifacts.
2. Also assert Todo → dir exists — **Recommend: no hard fail this PR**;
   Notes said measured empty; add only if a free one-liner in the same
   loop, still report-only. Default: skip to keep the diff small.
3. Live known achieved orphan — **Recommend: report it**; do not special-
   case names.

## Version History

- v1 — planning.
