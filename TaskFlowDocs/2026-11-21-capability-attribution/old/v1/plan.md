# Plan — 能力调用证据归属
> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md` — 身份、阶段上下文、旧账本保留和失败语义。

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — 仓库文档路由；`LICENSE` — 项目许可。
- `CONTRIBUTING.md` — 插件行为放在 `hooks/` 或 `skills/`，隔离工作区和实施前批准；`CODE_STYLE.md` — Shell、语言及验证约束。
- `README.md`、`README.zh-CN.md`、`skills/taskflow/references/runtime.md` — 现有宿主和证据机制说明，随行为变更核对。
- `hooks/capability-evidence`、`hooks/capability-gate`、`hooks/task`、`hooks/reuse-worktree` — 记录、消费、审批与交接的实现。

## Related Tasks

- `TF-20261012-c79e31` / `TaskFlowDocs/achieved/2026-10-17-stage-capability-pairing/`：之前有意接受阶段队列错配；本任务调整上游归属及该决定。

## Skills / Tools Used

- [PRD] Declared `agent-skills:debugging-and-error-recovery` — purpose: 分析缺陷根因；outcome: 已读取调查流程；incorporated: 从生产证据处定位归属缺失，并要求回归验证。
- [Spec] Unaided — 使用模型自身能力分析设计；considered: architecture and design
- [Plan] Unaided — 使用模型自身能力拆分工作；considered: work breakdown
- [Test] Unaided — 使用模型自身能力设计回归；considered: testing strategy

## Preconditions

- 独立工作区 `D:/WorkSpace/Agent/TaskFlow/.worktrees/2026-11-21-capability-attribution`，分支 `fix/capability-attribution`；本变更属于插件自身行为。
- 用户选择同时修复跨任务和跨阶段、保留无法归属的旧账本、保留显式 unaided。
- 本仓库偏好 CI 覆盖可自动化验证；真实 Claude 宿主验证与合成测试分开报告。

## Plan Review

- Verdict: sound
- Coverage: 覆盖记录、门禁、审批、交接、旧账本、文档及测试。
- Verifiability: 以跨任务、跨阶段和匹配证据的失败/通过矩阵验证，并回归恢复及并发。
- Layer ownership: 在证据生产时绑定身份，消费和审批验证，不通过修改下游文案掩盖。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-21 10:03 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 复现并确定上下文协议

- Goal: 审计调用者、存储格式、宿主事件及交接；写最小失败回归并明确阶段身份生命周期。
- Dependencies: 用户批准。
- Files: 相关 hooks、测试和运行时说明。
- Implementation checklist:
  - [x] 回归跨任务和跨阶段消费，核对版本、声明和未观察调用。
  - [x] 确定上下文命令、数据格式、状态切换、锁和旧账本保留规则。
- Acceptance: 复现问题且协议覆盖任务、版本、阶段和歧义。
- Verification: 对应回归在修复前失败。
- Rollback: 不修改产品行为时撤销测试与方案改动。
- Status: done

### Step 2 — 实施归属和隔离

- Goal: 在证据生产、门禁消费、审批和交接处实施身份约束。
- Dependencies: Step 1。
- Files: hooks、相关宿主接线及测试。
- Implementation checklist:
  - [x] 实施阶段上下文、身份记录和严格核对；保留 unaided / declared。
  - [x] 保留历史账本；覆盖交接、恢复和竞争条件。
- Acceptance: spec 的归属和保留约束均满足。
- Verification: 运行聚焦测试及适用 CI 检查。
- Rollback: 撤销本次代码与文档变更，保留用户账本。
- Status: in_progress

### Step 3 — 文档和审核

- Goal: 更新跨宿主实际行为、用户操作、限制及验收记录。
- Dependencies: Step 2。
- Files: Skill、runtime、README、测试和本任务计划。
- Implementation checklist:
  - [x] 更新文档并审核真实宿主与合成证据的区别。
  - [ ] 审查变更、运行适用检查并记录结果及风险。
- Acceptance: 文档与实现一致，结果可复核。
- Verification: 记录测试和未覆盖宿主。
- Rollback: 随产品变更一起撤销。
- Status: pending

## Checkpoints

- 仅在用户批准当前 Plan 后实施。

## Verification / Review

- 2026-11-21 Step 1: 回归已复现；阶段、会话和调用快照协议已确定

- 协议：`capability-context stage` 显式绑定任务、版本、阶段、会话；调用开始时按 session ID 和 tool-use ID 保存快照，成功结束时写带身份证据；Test 使用 `release-test`。无法匹配时拒绝归属。
- 已通过：跨任务/阶段与乱序、会话隔离、失败调用、中断重试、Test 释放、账本锁、宿主合成对齐、交接/恢复，以及审批和 Test 阶段的独立 smoke 片段。
- 已通过：归属/异步快照/失败回调/幂等聚焦测试，非阻塞锁、工作区交接和宿主合成对齐测试，审批、Test 阶段、能力记录及宿主接线 smoke 片段；Shell 语法、hook JSON、技能结构与 `git diff --check`。
- 待完成：完整 smoke 和三平台 CI 尚未运行；该 CI 仅由面向 main 的 PR 或 main 推送触发。真实 Claude Code 会话及其他宿主字段未验证；当前改动未提交、未发布、未安装。
- 限制：非阻塞锁竞争时可能漏记；子代理内部事件不自动归属，真实但不可观察的调用使用 declared。
- 回归：`hooks/test-capability-attribution` 在现有代码上输出 `FAIL unbound old invocation released a new task`，证实旧的无归属证据会释放新任务。同时复现 `FAIL PRD invocation released Plan`；临时夹具已删除。
- 设计约束：宿主事件的会话 ID 必须与阶段上下文绑定，避免同一工作区并发会话调用错归属；无会话身份时不推断。Claude Code 官方 hook 文档确认事件包含 session_id；其他宿主字段和可靠上下文建立方式尚需验证。异步调用还需要在启动时捕获阶段而不是仅在返回时读取当前阶段。

## Change Log

- v1：确认范围和归属设计。
- 工作修订：核对 Claude Code 官方 hook 字段，修正 External Facts 为 yes；不改变已批准的身份绑定契约。

## Follow-ups

- 真实 Claude Code 宿主首写事件需要在目标机器验证。

## Version History

- v1 — planning.
