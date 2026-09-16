# Plan — Repair the duplicate Todo ID
> Task version: v1
> Status: ready

No spec required — one data repair in `TaskFlowDocs/todo.md`.

## Reference Pointers

- `hooks/task` 的 `intake` 分支 — ID 派生算法的唯一实现（`cksum` 摘要 6 位十六进制），本任务按同一算法重算，并**不修改**它。
- `hooks/task` 的 `findsec()` — 「按 ID 查取首个命中」的行为，是本任务的风险依据。
- `TaskFlowDocs/achieved/2026-09-15-todo-merge-driver/prd.md`（第 46 行附近）与 `plan.md` 的 Follow-ups — 撞车成因与「只对新 intake 生效、不回改历史」的既有决定。

## Related Tasks

- Depends on: None
- Related: `TaskFlowDocs/2026-09-16-todo-entry-loss-detection/`、`TaskFlowDocs/2026-09-16-web-ui-merge-loss-guard/`（同一条问题线；本任务不与其共享文件，可独立提交）

## Skills / Tools Used (Optional)

## Preconditions

- [x] 适用仓库文档已读：`CONTRIBUTING.md`、`CODE_STYLE.md`。
- [x] 分支：`fix/duplicate-todo-id`，基于 `main`。
- [x] 远程基线：`origin` 即 `hkwuks/TaskFlow`，目标 `main`；非 fork。
- [x] 本任务不新建治理文档、不新增检查。

## Approval

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

## Steps

### Step 1 — 重算并改写重复 ID

- Goal: 让「ID → 任务」重新是单值映射，且不触碰历史与 hook 行为。
- Dependencies: 无。
- Files: `TaskFlowDocs/todo.md`。
- Implementation checklist:
  - [ ] 用 `hooks/task intake` 的同一算法（`printf '%s' "<Goal>" | cksum`，取 `%06x` 低 24 位）算出 `no-python-hooks` 条目的新 ID；先确认该值在当前 `todo.md` 中未被占用。
  - [ ] 把 452 行附近那条的 `- ID:` 改为新值，`- Updated:` 改为改动日期。
  - [ ] `phase-concept-mapping` 那条（413 行附近）保持 `TF-20260915-01` 与其余字段不变。
  - [ ] 改完 grep 复核无重复，并逐字段 diff 确认只有两行变化。
- Acceptance: 见 PRD 的 Acceptance Criteria。
- Verification: `grep -o '^- ID: .*' TaskFlowDocs/todo.md | sort | uniq -d` 为空；`git diff -- TaskFlowDocs/todo.md` 只有预期的两行；重算脚本再跑一次得到同一 ID；`bash hooks/smoke-test` 全绿。
- Rollback: `git checkout -- TaskFlowDocs/todo.md`。
- Status: pending

## Checkpoints

- 本任务不改任何可执行逻辑，因此不新增 smoke 断言；验收靠 grep 与逐行 diff。

## Verification / Review

## Change Log

## Follow-ups

## Version History

- v1 — planning.
