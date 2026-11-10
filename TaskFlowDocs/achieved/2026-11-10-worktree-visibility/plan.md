# Plan — 让插件和桌面应用中的用户能够清楚获知 Agent 创建的 worktree
> Task version: v2
> Status: completed

## Spec Pointers

- `spec.md`

## Reference Pointers
- `hooks/task`、`skills/taskflow/SKILL.md`、`hooks/smoke-test`、仓库 `CONTRIBUTING.md`。

## Related Tasks
- Todo TF-20261109-3c1409；与基础工作区防护任务相关，但验收独立。
- 接续已归档 TF-20261104-d535ae 的合并后 cleanup 提示和报告；按用户要求与本任务一起加强，不另建流程。

## Skills / Tools Used
- [PRD] Unaided — none applied; considered: requirements elicitation and framing.
- [Spec] Unaided — none applied; considered: architecture and design specification.
- [Plan] Unaided — none applied; considered: work breakdown and task decomposition.
- [Test] Unaided — none applied; considered: testing strategy.

## Preconditions
- 插件自身能力，非仓库专用规则；不修改用户全局配置。

## Plan Review

- Verdict: sound
- Coverage: 一次性位置输出、用户可见转达和合并后的完整清理分别覆盖；脏或无法确认合并的工作区不强制删除。
- Verifiability: 命令输出与 Git 状态用夹具验证；宿主用户可见效果另行观察，不把模拟输出算作真实显示。
- Layer ownership: Git 提供事实，TaskFlow 指导合并后的检查和清理；宿主负责展示，删除须符合用户授权。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-10 16:43 +0800
- Approved version: v2
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 显示工作区位置

- Goal: 提升任务成功时提供真实路径及分支，并指导 Agent 清楚告知用户。
- Dependencies: 方案获用户批准。
- Files: `hooks/task`、`skills/taskflow/SKILL.md`、必要测试。
- Implementation checklist:
  - [x] 实现一次性、非阻断的路径与分支提示。
  - [x] 验证 linked worktree、detached 和非 Git 情况。
- Acceptance: 准确报告路径与分支，未知状态不伪造；常规开发不反复提示。
- Verification: 隔离 Git 夹具及实际宿主可见性记录。
- Rollback: 回退本任务提交。
- Status: done

### Step 2 — 合并后工作区和分支收尾
- Goal: 在合并后而非归档时重新检查并处理当前任务的 worktree 与本地分支，同时报告无法安全清理的情况。
- Dependencies: 实际合并可验证、所需删除授权明确。
- Files: `skills/taskflow/SKILL.md`、`hooks/repository-check` 或可复用的既有流程及必要测试。
- Implementation checklist:
  - [x] 检查已合并、未合并、dirty、detached、无基线和被占用 worktree；明确待处理的数据。
  - [x] 在清理获授权且条件满足时，按顺序处理 worktree 和本地分支并核实结果。
  - [x] 不增加阻断任务开发的后台守卫或强制清理。
- Acceptance: 合并完成后不静默遗漏；不可证明安全时保留并报告，禁止强制删除。
- Verification: 通过隔离 Git 夹具验证状态和清理顺序；真实宿主可见性分开记录。
- Rollback: 回退本任务代码与指导；不删除用户原有数据。
- Status: done

## Checkpoints

## Verification / Review
- 已核实现有流程仅要求 Agent 用 `pwd` 和 `git branch --show-current` 自查，不要求将结果清楚展示给用户；候选入口为已存在的 `task promote` 成功输出。
- 现有 `archive` 只在合并前提示后续清理；`repository-check` 必须显式再次运行，并跳过 dirty worktree、自身工作区及无法按祖先关系证明合并的分支，因而不能保证合并后实际清理。
- 2026-11-10：已在 Windows Git Bash 隔离仓库验证普通 linked worktree 与 detached HEAD 的提升输出，路径及状态正确；已合并但有未跟踪内容的 worktree 由 repository-check 标识为 dirty 且保留，检查退出 0。脚本语法及 `git diff --check` 通过；其余场景、完整 CI 和真实宿主用户可见性待验证。
- 非 Git 验证第一次因测试目录仍被上层 Git 仓库识别而失败；将 Git 搜索边界设置在测试目录父级后复测，通过并报告 unknown。该测试不代表独立宿主 UI 已显示结果。
- 合并分支对应的 worktree 在隔离夹具中不可访问时，`repository-check` 报告 unknown 并保留，整体治理状态仍为 pass；不同于之前静默跳过。
- Skill quick validation 在 Windows 默认 GBK 下首次因 UTF-8 文件解码失败；启用 `PYTHONUTF8=1` 后验证通过。
- [CI](https://github.com/hkwuks/TaskFlow/actions/runs/42791155777) 的 Ubuntu、macOS、Windows smoke 和 evals 通过；release 按路径分类跳过。用户于 2026-11-10 按已验证范围验收并同意归档；清理仍依赖 Agent 在合并后执行，非自动后台删除。

## Change Log
- 2026-11-10：基于既有 Todo 建立 v1 草案，待计划批准。
- 2026-11-10：用户要求同一任务覆盖合并后工作区和本地分支收尾；v1 已获批准但尚未实施，v2 新增清理范围并重新审核。

## Follow-ups
- 真实桌面或插件中用户是否看到路径和分支，由未完成的 TF-20261110-0c7346 宿主验证继续跟踪。

## Version History

- v1 — planning.
