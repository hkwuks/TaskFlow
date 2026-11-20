# Plan — 复用工作树时同步目录名称
> Task version: v1
> Status: completed

## Reference Pointers
- `TaskFlowDocs/repository-docs/index.md`、`LICENSE`、`CONTRIBUTING.md`、`CODE_STYLE.md`：沿用项目命名、隔离和测试规则；遵守许可。
- `hooks/reuse-worktree`、`hooks/test-reuse-worktree`：既有交接和恢复边界。

## Related Tasks
- TF-20261120-f1d4ab：已完成候选发现；本任务增加复用后的命名。

## Skills / Tools Used
- [PRD] Unaided — 已检查现有交接和用户决策；considered: requirements elicitation
- [Spec] Unaided — 已检查交接边界；considered: architecture and design
- [Plan] Unaided — 按验收逐项检查；considered: work breakdown
- [Test] Unaided — 使用现有故障注入夹具；considered: testing strategy

## Preconditions
工作树 `D:/WorkSpace/Agent/TaskFlow/.worktrees/worktree-rename`；分支 `feature/worktree-rename`。范围属于插件行为，影响安装 TaskFlow 的仓库。

## Plan Review
- Verdict: sound
- Coverage: Step 1 覆盖命名、冲突、Git 登记及恢复；Step 2 覆盖说明与测试。
- Verifiability: 成功、冲突、故障注入和恢复夹具逐项核验验收标准及文件完整性。
- Layer ownership: 测试夹具验证用户可见行为，修改文档和测试不会代替交接实现。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-20 22:27 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps
### Step 1 — 实现交接改名与恢复
- Goal: 安全移动目录并保持恢复能力。
- Dependencies: 用户批准方案。
- Files: `hooks/reuse-worktree`。
- Implementation checklist:
  - [x] 在状态修改前验证目标路径，交接中记录并移动工作树。
  - [x] 更新恢复流程以处理移动前后故障。
- Acceptance: 同名不覆盖；成功后路径与分支描述一致；故障可恢复。
- Verification: 扩展交接夹具覆盖路径、Git 登记、证据及故障恢复。
- Rollback: 恢复脚本文件至变更前版本；保留测试产生的恢复证据。
- Status: done

### Step 2 — 验证与说明
- Goal: 覆盖真实调用和说明。
- Dependencies: Step 1。
- Files: `hooks/test-reuse-worktree`、`skills/taskflow/SKILL.md`、`skills/taskflow/references/runtime.md`。
- Implementation checklist:
  - [x] 增加成功、冲突与移动前后故障测试。
  - [x] 更新调用位置、命名和恢复说明。
  - [x] 运行聚焦测试并审查变更。
- Acceptance: 测试通过，文档与实现一致。
- Verification: Git Bash 运行 `bash hooks/test-reuse-worktree`，检查 diff。
- Rollback: 回退本任务对测试和文档的修改。
- Status: done

## Checkpoints
完成 Step 1 后核对任务证据与 Git 登记。

## Verification / Review

- 2026-11-20 Step 2: Windows Git Bash focused test and diff check passed

- 2026-11-20 Step 1: Windows Git Bash focused handoff and recovery test passed
Windows Git Bash：`bash -n hooks/reuse-worktree hooks/test-reuse-worktree` 通过；`hooks/test-reuse-worktree` 通过，覆盖开始、恢复、目的地冲突、恢复冲突、移动前后故障、旧格式日志、Git 登记和忽略文件。首次复测运行中修改了测试脚本导致意外 EOF；之后停止修改并完整重跑通过。`git diff --check` 通过。

测试夹具由交接测试层维护：成功后的路径断言按新目录合同更新，新增冲突和故障注入断言；没有通过修改中间值绕过检查。未发现与本任务无关的代码改动。

## Change Log
- v1：记录用户确认的命名、时机及冲突行为。
- v1：用户另行允许兼容旧格式未完成交接日志，以维持恢复能力。

## Follow-ups
无。

## Version History
- v1 — planning.
