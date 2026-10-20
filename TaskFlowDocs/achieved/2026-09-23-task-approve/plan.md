# Plan — Record Approval from a hook instead of hand-editing the five fixed fields

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/task` — command dispatch, `promote` Approval template (~651–657),
  `require_approval` (~503–515), `today` (~18).
- `hooks/version` — five-field reset shape (post-#52) — read-only mirror.
- `hooks/smoke-test` — lifecycle / approval-gates sections.
- `skills/taskflow/SKILL.md` — “Record approval as” snippet (~225–233).
- Predecessor: `TF-20260919-b7821b` / PR #52 (shape alignment).

## Related Tasks

- `TF-20260918-454ac4` — this task’s ID.
- `TF-20260919-b7821b` — done; five-field shape.

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell text
  processing and the repository's own hook conventions, all read directly.`

## Preconditions

- [x] Docs/rules inspected; worktree `.worktrees/feat-task-approve` on
  `feat/task-approve` from `main` = `7f531a2`.
- [x] Housekeeping archive commit for b7821b is on local main (`7f531a2`).
- [x] Field sources and `require_approval` inputs recorded in PRD.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-23
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — task approve

- Goal: R1–R5.
- Files: `hooks/task`.
- Checklist:
  - [x] `approve <task-id> [approver] [--root]` usage; default `user`.
  - [x] Preflight: plan + `## Approval` + `> Task version:`; no write on fail.
  - [x] Rewrite/insert five fields in promote order with R3 values;
        `Approved at` from `date '+%Y-%m-%d %H:%M %z'`; scope from R4.
  - [x] Do not touch `> Status:`, Todo, or Git; not gated by
        `require_approval`.
  - [x] `bash -n hooks/task`.
- Acceptance: A, B, C.
- Status: done

### Step 2 — skill sentence

- Goal: R6.
- Files: `skills/taskflow/SKILL.md`.
- Checklist:
  - [x] After the five-line snippet: record via `task approve [approver]`
        once the user has approved; hand-edit only as fallback.
  - [x] No second field template.
- Acceptance: D (snippet unchanged shape).
- Status: done

### Step 3 — smoke

- Goal: R7/R8.
- Files: `hooks/smoke-test`.
- Checklist:
  - [x] Promoted pending plan → `approve` → five lines exact → gated
        command passes.
  - [x] Custom approver; missing section/version leaves file unchanged.
  - [x] Scope `PRD / Plan` vs `PRD / Spec / Plan`.
  - [x] Existing approval-gates section still green.
- Acceptance: E.
- Status: done

## Checkpoints

- After Step 1: `bash -n` + A/B/C fixtures.
- After Step 3: one full suite; no chained mutations; pkill if killed.

## Verification / Review

| Check | Result |
|---|---|
| `bash -n hooks/task` | pass |
| `bash -n hooks/smoke-test` | pass |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` |
| `git diff --check` | clean |
| Approve + gate (A/B) | pass (suite) |
| Refuse no-write (C) | pass (suite) |
| Scope subsets (D) | pass (suite) |

## Change Log

- v1 — planning; Q1 optional approver default `user`, Q2 `date` with
  timezone no fallback, Q3 fixed `PRD / Spec / Plan` subset order.
- v1 — approved (user, 2026-09-23); Steps 1–3 done; suite green.

## Follow-ups

- Push local main housekeeping `7f531a2` when convenient (currently
  ahead of origin by 1 on base only — actually local main has it; push
  with next main push or separately).

## Version History

- v1 — planning.
- v1 — approved (user, 2026-09-23); Steps 1–3 done; suite green.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-09-18 用户提出**：手改 Approval 块能否自动化。判定——`## Approval` 的字段里只有 `Approved by` 是语义的（必须由人表态），其余都可推导：`Status` 是该子命令的动词，`Approved at` 是当天日期（hook 已有 `today`），`Approved version` 直接读 plan 自己的 `> Task version:` 行，`Approved scope` 由存在的核心文档推出。`skills/taskflow/SKILL.md` 已把模板钉成「`- Approved by:` 起的四行」，格式无需 Agent 判断。
  **先修一个现成的自相矛盾**：`hooks/version` 的重置只写 `- Approved by/at/version/scope: pending` 四条，**不写 `- Status:`**；而 `hooks/task` 的模板是**五**行、带 `- Status: requested`。于是经 `version` 迁移过的任务，Approval 块是 version 的字段集加上一条滞留在旧值的 `- Status:` 行——两个 hook 对同一块内容的形状意见不一致。**本任务就是实例**：v1→v2 后 `- Status:` 留在 `checking` 一路没人管，直到 `complete` 读它才发现对不上（`require_approval` 用的是 `grep -qx -- "- Status: approved"`）。
  **时间格式也打架**：模板写 `YYYY-MM-DD HH:mm +08:00`，`version` 复位只写 `pending`。若自动化，`today` 目前只有 `+%Y-%m-%d`，要扩出分钟与时区。
  **门禁必须在写入之前**：合法顺序是「人先批准 → hook 记录」，不是「hook 写入 → 门禁通过」，否则 `require_approval` 变成自我认证。自动化只应删掉**转录**（把已表态的事实落成固定格式），不能生成或推断批准本身。
  **与 `TF-20260918-88e04c`、`TF-20260918-e7c041` 同族**：本次归档时 `complete` 在 base 检出上失败，正是因为 main 落后导致合并把 `Approval` 块覆盖回 `pending`，手工补批准后重跑才过。真正的修法在 `complete` 的**事务原子性**上（`e7c041`），不在让批准好写。
