# Plan — Hold Todo protection on the web-UI merge path
> Task version: v1
> Status: ready

No spec required — one range argument added to an existing read-only hook plus one CI job.

## Reference Pointers

- `TaskFlowDocs/2026-09-16-todo-entry-loss-detection/` — 本任务的前置任务，交付 `hooks/todo-check` 单提交模式。
- `.github/workflows/hooks.yml` — 既有 `smoke` / `release` / `evals` job；`release` job 的 `fetch-depth: 0` 是范围审计需要的同款 checkout。
- `skills/taskflow/references/runtime.md` 的「Only local merges」段落 — 本任务要改写的限制说明。
- `TaskFlowDocs/achieved/2026-09-15-todo-merge-driver/prd.md` — 「插件不能改托管设置」的实测依据。

## Related Tasks

- Depends on: `TaskFlowDocs/2026-09-16-todo-entry-loss-detection/`（`hooks/todo-check` 必须已合入 `main`，本任务才有文件可扩展）
- Related: `TaskFlowDocs/2026-09-16-duplicate-todo-id/`（同一条问题线的第三个任务，与本任务无文件重叠）

## Skills / Tools Used (Optional)

## Preconditions

- [x] 适用仓库文档已读：`CONTRIBUTING.md`、`CODE_STYLE.md`、`.github/pull_request_template.md`。
- [x] 分支：本任务在 `2026-09-16-todo-entry-loss-detection` 合并后，从新的 `main` 切 `fix/web-ui-merge-loss-guard`。
- [x] 远程基线：`origin` 即 `hkwuks/TaskFlow`，目标 `main`；非 fork。
- [x] 本任务不新建治理文档；CI 改动在既有 workflow 内。

## Approval

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

## Steps

### Step 1 — 范围模式与 CI 接线

- Goal: 让 `hooks/todo-check` 能审计一次推送引入的合并提交，并让 `push: main` 跑它。
- Dependencies: `TaskFlowDocs/2026-09-16-todo-entry-loss-detection/` 已合入 `main`。
- Files: `hooks/todo-check`、`.github/workflows/hooks.yml`、`hooks/smoke-test`、`hooks/README.md`、`skills/taskflow/references/runtime.md`。
- Implementation checklist:
  - [ ] `hooks/todo-check` 第二参数含 `..` 时进入范围模式：`git rev-list --merges <range>` 取该范围的合并提交，逐个按单提交模式的逻辑审计，输出里带上提交哈希。
  - [ ] 范围为空 → `STATUS: pass` 退出 `0`；范围不可解析 → `STATUS: blocked` 退出 `3`；任一合并丢条目 → 退出 `2`。
  - [ ] 单提交模式（不含 `..`）行为与上一任务一致，回归不变。
  - [ ] `.github/workflows/hooks.yml` 新 job：`fetch-depth: 0`；`push` 事件用 `github.event.before..github.event.after`，`before` 缺失或全零时退化为审计 `HEAD`；`pull_request` 事件用 `HEAD`。
  - [ ] smoke 覆盖范围模式四例（含丢条目 → `2`、只有非合并提交 → `0`、坏范围 → `3`、退化路径与单提交一致）。
  - [ ] `runtime.md` 的 web-UI 段落改写为「本地合并用 driver + 推送后在 CI 审计」，并给出取回丢失条目的命令；两个 hook 清单更新 `todo-check` 的范围参数说明。
- Acceptance: 见 PRD 的 Acceptance Criteria。
- Verification: `bash hooks/smoke-test`；本地对构造范围跑 `todo-check`；推送后 CI 新 job 成功；`bash:3.2` 容器 `bash -n`。
- Rollback: 还原 `hooks/todo-check` 的范围分支、删掉 CI job、还原两处文档。
- Status: pending

## Checkpoints

- 新增断言逐条 mutation 验证。
- 这是本任务线里唯一改动 CI 的任务；`smoke` / `release` / `evals` 三个既有 job 的行为不得改变。

## Verification / Review

## Change Log

## Follow-ups

## Version History

- v1 — planning.
