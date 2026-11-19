# Plan — 多 Todo 共同处理
> Task version: v1
> Status: in_progress

## Spec Pointers
- `spec.md`

## Reference Pointers
- `TaskFlowDocs/repository-docs/index.md`、`LICENSE`、`CONTRIBUTING.md`、`CODE_STYLE.md`：插件规则放在 `skills/taskflow/` 与 `hooks/`；任务分支隔离，计划批准后实施；遵循 shell 错误处理。
- `hooks/task`、`hooks/archive`、`hooks/remote-todo`：当前只查找或归档首项，远程关联只有一条。

## Related Tasks
- 独立 Todo TF-20261119-bf0c36：共享下载内容，不纳入本任务。

## Skills / Tools Used
- [PRD] Unaided — none applied; considered: requirements elicitation and framing.
- [Spec] Unaided — none applied; considered: architecture and design specification.
- [Plan] Unaided — none applied; considered: work breakdown and task decomposition.
- [Test] Unaided — none applied; considered: testing strategy.

## Preconditions
- 用户已确认共享文档、逐项结果和本地/远程范围；具体计划等待批准。
- 工作区 `.worktrees/2026-11-19-multi-todo`，分支 `feature/multi-todo`。

## Plan Review
- Verdict: sound
- Coverage: 步骤 1 设计关联与单项生命周期覆盖身份及部分完成；步骤 2 实施本地及远程和流程；步骤 3 覆盖失败恢复、单项与回归。
- Verifiability: 回归须核对每个条目的身份、状态、路径和正文，并模拟远程失败；绿色测试不能代替逐项验收。
- Layer ownership: 状态由生命周期和远程同步层负责，测试只断言经批准的行为；不修改中间数据掩盖缺陷。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-19 10:17 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 完善关联与生命周期设计
- Goal: 逐一梳理全部读取、更新、归档和重开路径，确定共享任务关联和部分完成的接口与恢复语义。
- Dependencies: 用户批准。
- Files: `spec.md`、相关 hooks 和测试。
- Implementation checklist:
  - [ ] 盘点调用方和远程关联约束，写明实际接口与迁移边界。
  - [ ] 检查部分完成时共享文档、未完成项和重开的路径。
- Acceptance: 设计覆盖本地、远程及混合场景，且不会误关闭或丢失未完成项。
- Verification: 逐条审查调用路径和状态转换。
- Rollback: 恢复本步骤文档。
- Status: pending

### Step 2 — 实现流程和关联
- Goal: 支持用户指定多个已有条目共享工作，并各自更新结果。
- Dependencies: 步骤 1。
- Files: `skills/taskflow/`、生命周期与远程 hooks。
- Implementation checklist:
  - [ ] 更新关联、状态及归档逻辑与流程指导。
  - [ ] 保留远程部分失败可检查信息。
- Acceptance: 各项状态和归档只反映已确认的结果。
- Verification: 聚焦测试覆盖混合状态及远程失败。
- Rollback: 回退本任务变更。
- Status: pending

### Step 3 — 验证和审查
- Goal: 核验全部验收条件和已有单项路径。
- Dependencies: 步骤 2。
- Files: 测试、计划和必要文档。
- Implementation checklist:
  - [ ] 运行针对性与项目要求的检查，记录结果。
  - [ ] 审查影响范围、正文保留、失败和恢复。
- Acceptance: 逐项验收通过，限制与未验证项明确。
- Verification: 聚焦回归、项目校验和 diff 检查。
- Rollback: 回退本任务变更。
- Status: pending

## Checkpoints
- 实现前记录 Git 基线；按变更影响建立回滚点。

## Verification / Review
- 待执行。

## Change Log
- v1：记录用户对共享文档、逐项状态及本地和远程范围的确认。

## Follow-ups
- 不包含下载内容共享 Todo。

## Version History
- v1 — planning.

- 2026-11-19：用户批准 v1；检查发现状态、归档、重开和远程去重/迁移/解除关联均依赖单条关联，直接复用任务路径会误更新或遗留失效引用；继续完成端到端接口设计后再修改实现。
