# Plan — 多 Todo 共同处理
> Task version: v2
> Status: completed

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
- 用户确认 v2 主关联和 Plan 清单的折中方案。
- 工作区 `.worktrees/2026-11-19-multi-todo`，分支 `feature/multi-todo`。

## Plan Review
- Verdict: sound
- Coverage: 步骤 1 设计关联与单项生命周期覆盖身份及部分完成；步骤 2 实施本地及远程和流程；步骤 3 覆盖失败恢复、单项与回归。
- Verifiability: 回归须核对每个条目的身份、状态、路径和正文，并模拟远程失败；绿色测试不能代替逐项验收。
- Layer ownership: 状态由生命周期和远程同步层负责，测试只断言经批准的行为；不修改中间数据掩盖缺陷。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-19 10:32 +0800
- Approved version: v2
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 完善关联与生命周期设计
- Goal: 逐一梳理全部读取、更新、归档和重开路径，确定共享任务关联和部分完成的接口与恢复语义。
- Dependencies: 用户批准。
- Files: `spec.md`、相关 hooks 和测试。
- Implementation checklist:
  - [x] 盘点调用方和远程关联约束，写明实际接口与迁移边界。
  - [x] 检查部分完成时共享文档、未完成项和重开的路径。
- Acceptance: 设计覆盖本地、远程及混合场景，且不会误关闭或丢失未完成项。
- Verification: 逐条审查调用路径和状态转换。
- Rollback: 恢复本步骤文档。
- Status: done

### Step 2 — 实现流程和关联
- Goal: 支持用户指定多个已有条目共享工作，并各自更新结果。
- Dependencies: 步骤 1。
- Files: `skills/taskflow/`、生命周期与远程 hooks。
- Implementation checklist:
  - [x] 添加按 ID 更新未提升本地 Todo 的操作，增加主关联验收保护，更新流程指导。
  - [x] 复用远程逐项 stage 与现有失败恢复，不扩展远程关联模型。
- Acceptance: 各项状态和归档只反映已确认的结果。
- Verification: 聚焦测试覆盖混合状态及远程失败。
- Rollback: 回退本任务变更。
- Status: done

### Step 3 — 验证和审查
- Goal: 核验全部验收条件和已有单项路径。
- Dependencies: 步骤 2。
- Files: 测试、计划和必要文档。
- Implementation checklist:
  - [x] 运行针对性与项目要求的检查，记录结果。
  - [x] 审查影响范围、正文保留、失败和恢复。
- Acceptance: 逐项验收通过，限制与未验证项明确。
- Verification: 聚焦回归、项目校验和 diff 检查。
- Rollback: 回退本任务变更。
- Status: done

## Checkpoints
- v2 基线 `40e0565`；实现与测试检查点 `5a56b5f`。

## Verification / Review
- 用户于 2026-11-19 确认验收并同意归档；测试范围与未验证项如下。
- `hooks/test-multi-todo`：通过，验证单项状态、正文保留、远程关联拒绝、主项验收和重复关联的重开保护。
- `hooks/test-remote-todo-task-state`：通过（使用模拟远程服务）；不代表真实宿主 Issue 写入。
- `quick_validate.py skills/taskflow`：使用已安装 torch 环境的 Python 及 `PYTHONUTF8=1` 通过。
- `git diff --check`：通过。Windows 本地 Bash smoke 第三轮通过全部远程用例后，在模拟无解释器环境的 `session-record` 启动时因 Git Bash 链接程序缺少动态库而停止；此项属于 Windows 运行 Unix smoke 的环境限制，后续用例未运行。CI 的 Windows 入口是 `hooks/smoke-test-windows.ps1`，已接入新增测试，使用 Windows launcher 单独执行新增测试通过；完整 Windows 套件及跨平台 CI 未运行。
- 第一次完整 smoke 中并发创建测试失败，独立复测当前代码两次通过、一次失败；基线两次通过，测试依赖两秒并发窗口，原因未确定。第二次在嵌套工作区夹具的 Git 恢复目录检查停止；使用 `GIT_CEILING_DIRECTORIES` 后该用例单独通过，第三次全部远程用例通过。
- 本地单项状态命令仅支持未提升且非远程关联记录；已提升项按自身任务处理，远程项使用原有远程操作。

## Change Log
- v2：用户选择一个主关联及 Plan 中的其他条目，按 ID 独立更新，避免多对多关联改造。
- v2：落实主项验收门、重复关联拒绝和独立本地副本处理；Windows 及 Unix CI 入口覆盖新测试。
- v1：记录用户对共享文档、逐项状态及本地和远程范围的确认。

## Follow-ups
- 不包含下载内容共享 Todo。
- Unix 和 macOS CI 及完整 Windows CI 尚未运行；保留 Unix smoke 的 Windows Bash 动态库限制与并发用例偶发失败。

## Version History
- v1 — planning.

- 2026-11-19：用户批准 v1；检查发现状态、归档、重开和远程去重/迁移/解除关联均依赖单条关联，直接复用任务路径会误更新或遗留失效引用；继续完成端到端接口设计后再修改实现。
