# Plan — Detect a task directory that no Todo entry references

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/repository-check` — uncommitted artifact loop (~69–90); add orphan
  pass beside it.
- `hooks/smoke-test` — `== repository-check … ==` sections (~1078+).
- `TaskFlowDocs/todo.md` — `- Task:` backticked paths.
- Predecessor: `TF-20260916-ab381b` (isolation + uncommitted report).

## Related Tasks

- `TF-20260916-a357ee` — this task’s ID.
- `TF-20260916-ab381b` — done; different direction (misplaced/uncommitted).

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell text
  processing and the repository's own check conventions, all read directly.`

## Preconditions

- [x] Docs/rules inspected; worktree `.worktrees/feat-orphan-task-dirs` on
  `feat/orphan-task-dirs` from `main` = `5eba691`.
- [x] Incident, direction, and ab381b boundary recorded in PRD Background.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-23
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — repository-check orphan report

- Goal: R1–R5.
- Files: `hooks/repository-check`.
- Checklist:
  - [x] Collect `- Task:` backticked paths from `todo.md`.
  - [x] Scan `TaskFlowDocs/*/` and `TaskFlowDocs/achieved/*/` with prd or
        plan; report dirs not referenced (trailing-slash tolerant).
  - [x] Orphans set `needs=1`; uncommitted artifacts unchanged.
  - [x] `bash -n hooks/repository-check`.
- Acceptance: A, B, C.
- Status: done

### Step 2 — smoke

- Goal: R6/R7.
- Files: `hooks/smoke-test`.
- Checklist:
  - [x] Unreferenced active + achieved → listed, exit 2.
  - [x] After adding matching `Task:` → not listed.
  - [x] Existing repository-check sections still green.
- Acceptance: D, E.
- Status: done

## Checkpoints

- After Step 1: `bash -n` + A/B/C fixtures.
- After Step 2: one full suite; no chained mutations; pkill if killed.

## Verification / Review

| Check | Result |
|---|---|
| `bash -n hooks/repository-check` | pass |
| `bash -n hooks/smoke-test` | pass |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` |
| `git diff --check` | clean |
| Active orphan listed / ref clears (A/B) | pass (suite) |
| Achieved orphan (C) | pass (suite) |
| Existing check sections (D) | pass (suite) |

## Change Log

- v1 — planning; Q1 orphan sets needs, Q2 no reverse hard-fail, Q3 no
  special-case names.
- v1 — approved (user, 2026-09-23); Steps 1–2 done; suite green.

## Follow-ups

- Housekeeping commit `5eba691` is on local main only until next push.
- If live tree reports the known historical achieved orphan after merge:
  human decides tombstone vs extra Todo line (data, not code).

## Version History

- v1 — planning.
- v1 — approved (user, 2026-09-23); Steps 1–2 done; suite green.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- 发现于 2026-09-16 —— 提交 PR #28 时为让提交只含任务 A 而摘掉 B/C/D 的 Todo 条目，随后一次 `git checkout -- TaskFlowDocs/todo.md` 把工作区文件整体回退，三条条目一度丢失（同日已按原样补回），而三个任务目录始终在 `TaskFlowDocs/` 下，形成「目录存在、无 Todo 指向」的孤儿态（仅工作区，未进入任何提交）。同一形态在历史里也有一例：`TaskFlowDocs/achieved/2026-09-10-repository-document-placement/`，全部历史中从未有过对应的 Todo 条目。目前该缺口无自动检查兜住。注意：只查「任务目录 → Todo」这一个方向；反方向（Todo 条目指向不存在的目录）本轮已实测为空。2026-09-16 追问：本条与 `TF-20260916-ab381b` 是同一根因的两个方向——孤儿目录是「文档先于隔离产生」的结果，`ab381b` 修根因并在 `hooks/repository-check` 里报告错位产物；本条仍是更广的历史审计（含已提交、已归档的目录），是否仍要独立成检查待定。
