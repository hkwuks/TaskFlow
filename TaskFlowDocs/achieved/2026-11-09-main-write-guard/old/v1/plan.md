# Plan — 防止开发任务修改基础工作区
> Task version: v1
> Status: in_progress

## Spec Pointers
- `spec.md`

## Reference Pointers
- `TaskFlowDocs/repository-docs/index.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`：工作树隔离、跨宿主覆盖、审批和测试规则。
- `hooks/capability-gate`、各 `hooks/hooks*.json`、`skills/taskflow/references/runtime.md`：现有事件适配与限制。
- https://learn.chatgpt.com/docs/hooks：Codex 事件覆盖、信任和限制。

## Related Tasks
- Todo: TF-20261109-e2df6d；后续关联 TF-20261109-293987（能力对齐）和 TF-20261109-3c1409（用户可见性）。
- Follows: `TaskFlowDocs/achieved/2026-09-16-capability-selection-enforcement/`（提升门禁与隔离规则）；本任务增加写入保护。

## Skills / Tools Used
- [PRD] Unaided — no capability applied to this phase; considered: requirements elicitation and framing.
- [Spec] Unaided — no capability applied to this phase; considered: architecture and design specification.
- [Plan] `agent-skills:planning-and-task-breakdown`：形成可验证步骤；任务文件按 TaskFlow 作为唯一事实源。
- [Research] `openai-docs`：核对 Codex 官方 hook 事件与限制。

## Preconditions
- worktree `.worktrees/2026-11-09-main-write-guard`，分支 `fix/2026-11-09-main-write-guard`。
- 不修改或清理基础工作区的其他 Todo 与未跟踪文件。

## Plan Review
- Verdict: 用户已同意 v1。
- Coverage: 文件编辑门、跨宿主、例外和限制。
- Verifiability: 独立 Git 仓库夹具与条件允许时的真实宿主测试。
- Layer ownership: hook 拒绝可识别的编辑事件；权限沙箱不由 TaskFlow hook 伪造。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-09
- Approved version: v1
- Approved scope: PRD、Spec 与 Plan v1；用户在对话中明确同意。

## Steps
### Step 1 — 核实事件及例外
- Goal: 对五宿主确认文件编辑事件、拒绝格式、路径与发布/Todo 例外，识别无法判断的场景。
- Dependencies: 无。
- Files: 各宿主接线、`runtime.md`、官方文档。
- Implementation checklist:
  - [ ] 记录事件契约和证据等级，确定可验证例外。
- Acceptance: 每个宿主有可实现的行为或具体不支持依据。
- Verification: 核对官方文档及实际事件；记录不可测情况。
- Rollback: 无生产代码改动。
- Status: pending

### Step 2 — 写前守卫与各宿主接线
- Goal: 在支持的编辑路径拒绝写基础工作区，允许合法例外。
- Dependencies: Step 1。
- Files: `hooks/` 守卫和宿主接线；必要时 Skill 与 runtime 文档。
- Implementation checklist:
  - [ ] 实现目标路径判断与可解释拒绝，保持每个 patch 原子。
  - [ ] 对可支持宿主接线，记录无法支持的具体机制。
- Acceptance: PRD 1、2、4。
- Verification: 回归夹具覆盖基础/任务树、绝对路径、Windows、非项目及例外。
- Rollback: 回退本步骤改动。
- Status: pending

### Step 3 — 验证与文档
- Goal: 验证行为、宿主覆盖和用户可见限制。
- Dependencies: Step 2。
- Files: `hooks/smoke-test`、Windows 测试、runtime 和相关 README。
- Implementation checklist:
  - [ ] 增加并运行相关自动测试；可能时运行真实 Codex 事件测试。
  - [ ] 审查 diff、更新文档，记录证据等级与不能覆盖的路径。
- Acceptance: PRD 全部验收条件；真实宿主不可测时明确标注。
- Verification: 定向测试、适用的 Windows suite、`git diff --check`、项目规定的技能校验。
- Rollback: 回退本任务变更。
- Status: pending

## Checkpoints
Step 1 若发现不能安全区分例外，先报告并调整方案，不擅自放宽保护。

## Verification / Review
待实施。

## Change Log
- 2026-11-09 用户明确同意 v1，随后明确要求手动记入；`task approve` 因 Codex 未自动记录 Plan 技能调用而拒绝，批准字段据用户指示手动记录，未伪造证据，待 TF-20261109-293987 修复该缺口。
- 2026-11-09 建立计划；源 Todo 从基础工作区复制至任务 worktree，原条目保留。

## Follow-ups
- 其他宿主能力对齐由关联 Todo 跟踪。

## Version History
- v1 — planning。
