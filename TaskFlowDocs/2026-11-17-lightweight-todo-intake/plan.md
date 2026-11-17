# Plan — 轻量 Todo 录入
> Task version: v1
> Status: in_progress

## Spec Pointers
- spec.md

## Reference Pointers
- hooks/task、hooks/smoke-test、skills/taskflow/SKILL.md：近似扫描与重叠义务。

## Related Tasks
- 2026-11-10-token-review v3：此前实现中文候选提示；用户选择独立修复，保留历史与其工作树。

## Skills / Tools Used
- [PRD] Unaided — 根据代码和用户选择确定范围；considered: root cause investigation
- [Spec] Unaided — 确定现有接口边界；considered: architecture and design specification
- [Plan] Unaided — 按依赖及验收划分；considered: work breakdown and task decomposition
- [Test] Unaided — 使用现有回归；considered: testing strategy

## Preconditions
- 工作树 .worktrees/capability-outcomes，分支 fix/todo-intake-lightweight，基于本地 origin/main 5bf7551，远端新鲜度未核实。
- 已读 TaskFlowDocs/repository-docs/index.md、LICENSE、CONTRIBUTING.md、README.md；遵循工作树隔离、计划审批和 AGPL 许可。变更属于插件自身行为，影响所有使用者。

## Plan Review
- Verdict: sound
- Coverage: Step 1 覆盖录入与任务选择边界以及扫描移除；Step 2 覆盖中英文、精确重复、ID 和相关检查。
- Verifiability: 隔离 Todo 夹具检查输出、文件和回归。
- Layer ownership: Agent 流程属 Skill，候选扫描属 intake；精确重复保护不变。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-17 16:04 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 简化录入
- Goal: 只录入后停止，移除近似候选扫描。
- Dependencies: 用户批准 v1。
- Files: skills/taskflow/SKILL.md、hooks/task、必要引用文档。
- Implementation checklist:
  - [x] 明确本地和远程的只录入边界，保留开始工作前的重叠检查。
  - [x] 删除近似扫描，保留精确重复、ID 与错误处理。
- Acceptance: 满足 PRD 行为要求。
- Verification: 隔离夹具和 Skill 检查。
- Rollback: 回退本任务改动。
- Status: done

### Step 2 — 验证
- Goal: 验证录入和既有保护。
- Dependencies: Step 1。
- Files: hooks/smoke-test 等相关测试。
- Implementation checklist:
  - [x] 覆盖中英文近似录入无提示、精确重复及确定性 ID。
  - [x] 运行适用测试并记录结果。
- Acceptance: 所有验收标准通过，限制明确。
- Verification: 针对性测试、脚本语法和 diff 检查，适用时运行 smoke。
- Rollback: 回退本任务改动。
- Status: done

## Checkpoints
实施完成后记录 Git 检查点。

## Verification / Review
Windows Git Bash：中英文相似目标成功且 stderr 为空，精确重复拒绝且文件不变，相同目标跨夹具 ID 一致；Skill 两阶段边界检查通过。bash -n 与 git diff --check 通过。完整 smoke 首次因默认临时目录权限失败；套件会删除测试文件，按用户禁止删除文件的要求未重试。夹具保留在 .worktrees/todo-intake-verification-20261117。

## Change Log
- 2026-11-17：用户选择独立修复、移除相似检查并保留精确重复拒绝；已实现并完成针对性验证。

## Follow-ups
Issue 计划存储不在本次范围。

## Version History
- v1 — planning.
