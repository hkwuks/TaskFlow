# Plan — 共享缓存与安全复用 worktree
> Task version: v1
> Status: completed

## Spec Pointers
- `spec.md`

## Reference Pointers
- `TaskFlowDocs/repository-docs/index.md`、`LICENSE`、`CONTRIBUTING.md`、`CODE_STYLE.md`：本任务改变 TaskFlow 插件行为，并需同步本仓库直接冲突的工作树规则；不将仓库私有规则放入插件模板。
- `hooks/task`、`hooks/archive`、`hooks/repository-check`、`hooks/prompt-reminder`、`hooks/capability-evidence`、`hooks/capability-gate`、`hooks/external-evidence`、`hooks/version-baseline`、`skills/taskflow/SKILL.md` 和 `skills/taskflow/references/runtime.md`：当前工作区及证据依赖一个工作树的整个生命周期。
- 官方 Git、npm、pip 文档及结论记录在 `prd.md` External Facts。

## Related Tasks
- TF-20261119-bf0c36（已有 Todo）；主工作区中保留原始未提交条目，本任务仅在独立工作树中使用它。
- TF-20261119-d31806：已归档的多 Todo 任务，本任务不改其文档。

## Skills / Tools Used
- [PRD] Unaided — none applied; considered: requirements elicitation and framing.
- [Spec] Unaided — none applied; considered: architecture and design specification.
- [Plan] Declared `agent-skills:planning-and-task-breakdown` — 依赖排序、按验收拆分；只将适用内容写入本 Plan，未创建第二套任务文件。
- [Test] Unaided — none applied; considered: testing strategy.
- [Research] 官方 Git / npm / pip 文档；具体来源见 PRD；记录区分宿主观察与声明。

## Preconditions
- 用户确认 TaskFlow 通用规则、优先共享安全缓存；复用前原任务必须归档且归档已提交。复用时先切到已核实 main 提交，再基于该提交创建新分支，不从旧分支起步；保留工作树时已合并本地分支仍按安全规则清理。
- 当前路径 `.worktrees/2026-11-19-shared-cache`，分支 `feature/shared-cache-reuse`。工作树复用操作仅触及明确选定的空闲目录；不更改项目外内容。
- 计划待用户审批后实施；不自动删除 worktree、缓存或未合并分支，已合并本地分支的清理仍需核验及用户授权。

## Plan Review
- Verdict: sound
- Coverage: 缓存验收由步骤 1 覆盖；归档前置、复用、文件保护及证据隔离由步骤 2 覆盖；保留工作树同时清理合并分支、生命周期提示和完整测试由步骤 3、4 覆盖。
- Verifiability: 实仓夹具直接检查原文件、原分支、账本归属、拒绝和恢复；缓存规则验证实际授权路径与工具行为，不将文件逻辑大小或下载量冒充 SSD 写入实测。
- Layer ownership: 独立工作区选择由复用流程负责，任务证据由证据存储和门禁负责；更改旧测试只在契约确有改变时逐项说明，不改中间值掩盖失败。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-19 13:12 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 缓存与复用规则
- Goal: 设计并实现可适用于各仓库的安全缓存指导，区分授权、原生下载缓存和不可直接共享的产物。
- Dependencies: 用户批准。
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/runtime.md`，以及必要的项目约定。
- Implementation checklist:
  - [x] 按工具检查现有 pip/npm/uv 等原生下载缓存及允许的读写路径；仅在项目内或已有授权的位置按需复用，不改全局配置、不清空缓存；环境与构建产物不默认共享。
  - [x] 同步与 worktree 复用冲突的现有规则，保留每个并发任务的隔离。
- Acceptance: 新任务能够按规则复用合适的已有资源，禁止将可变安装/构建目录无条件共用。
- Verification: 与已查阅官方文档逐条核对，检查插件与仓库规则一致及授权边界。
- Rollback: 回退本步骤文档变更。
- Status: done

### Step 2 — 安全复用与账本隔离
- Goal: 在原任务已归档、归档记录已提交且确认空闲的工作树里，从目标 base 创建新任务分支；原分支未合并时保留，旧证据可恢复。
- Dependencies: 步骤 1 的契约。
- Files: 复用命令、`hooks/task`、能力和外部证据相关代码；按实际调用关系修改。
- Implementation checklist:
  - [x] 校验原任务已归档且归档记录已提交，工作树无活动写入者、索引未隐藏变化、无未提交或未跟踪数据、子模块安全；核实并固定 main SHA，先使用 `git checkout --no-overwrite-ignore --detach <main-sha>`，再使用 `git switch --no-track -c <new> <main-sha>`；不覆盖忽略文件、不重置或追踪旧分支；固定并核对 main 引用、旧分支引用及新分支起点，不改写任何既有提交。
  - [x] 按旧任务 ID 原样保存 `evidence`、`released`、`declarations`、`external` 及恢复记录，新任务使用独立账本；`version-baselines` 原位保留。恢复旧任务时恢复对应快照，不从旧任务为新任务提供证据。
  - [x] 对交接与所有账本读写、门禁和审批使用同一互斥协议；证据 hook 遇锁立即返回，不等待日志写入；门禁遇锁或未完成 journal 失败关闭。
  - [x] 使用 journal 记录原任务、旧 HEAD、main SHA、目标、快照和交接阶段；在保存、切到分离 HEAD、创建分支、建账各边界中断时可检查并恢复，冲突不覆盖、不自动删除或 reset；原分支未合并时保留。
- Acceptance: 未归档任务不能复用；已归档且已提交但未合并的分支可保留并从 base 切换新任务；异常不得丢用户文件或让新任务复用旧证据。
- Verification: 隔离 Git 实仓测试旧任务未归档、独立任务、旧任务恢复、脏工作树、忽略冲突、共同锁竞争以及保存前后/分离 HEAD 后/创建分支后/建账后的故障注入；校验两次切换不创建提交或改写原有引用、新分支从 main SHA 创建且不追踪旧分支、未合并的旧提交不被带入，分离 HEAD 中途失败不得继续提交，main 和旧分支引用不变，旧文件、账本和基线不丢；覆盖 main 随后变化产生普通合并冲突以及旧分支未合并的情形，journal 未完成时审批不通过。
- Rollback: 回退实现；测试用临时夹具的旧证据不删除，验证失败保留恢复记录。
- Status: done

### Step 3 — 提示与跨平台测试
- Goal: 归档后保留可复用工作树，同时在原分支已合并、用户授权并核实安全后继续清理本地分支；用户选择时仍可移除工作树。
- Dependencies: 步骤 2。
- Files: `hooks/archive`、`hooks/repository-check`、`hooks/prompt-reminder`、`CONTRIBUTING.md`、相关 smoke/Windows 测试及 hook 清单。
- Implementation checklist:
  - [x] 同步创建、复用、归档后的引导和本仓库约定；先安全切到已核实 base 的分离 HEAD 或复用到新分支，核对旧分支与最新远端 base 的祖先关系并确认已有授权，再使用 `git branch -d`；不得仅凭该命令的 upstream 判定，拒绝或 squash/rebase 不满足条件时保留并报告。
  - [x] 加入各宿主平台适用的测试与 CI 入口；核对变更旧测试的真实契约。
- Acceptance: 保留工作树不阻碍已合并本地分支清理；未合并分支不删，`-d` 因 squash/rebase 拒绝时保留并说明；测试覆盖真实行为。
- Verification: 针对性测试、Windows launcher、Unix smoke/CI；核对帮助信息与仓库清单。
- Rollback: 回退本步骤改动。
- Status: done

### Step 4 — 全量核验与审查
- Goal: 审查所有验收、回滚点、隐私/权限与现有工作区状态，记录局限。
- Dependencies: 步骤 1–3。
- Files: 任务计划和必要测试。
- Implementation checklist:
  - [x] 运行适用的项目测试、技能格式验证、`git diff --check`；区分环境与产品失败。
  - [x] 核对每条验收、外部事实、并发和恢复风险；审查旧文件、夹具和期望变更。
- Acceptance: 用户可审查所有结果，未验证项与遗留风险明确。
- Verification: 命令与结果记录于下方，用户验收后才归档。
- Rollback: 使用本任务 Git 检查点和文档版本恢复。
- Status: done

## Checkpoints
- v1 从 `8d6c477` 开始；按工作包建立回滚点，归档前依规则提交代码。

## Verification / Review
- 2026-11-19 提交前审查：复核归档条件、忽略文件保护、引用校验、证据互斥与恢复、授权范围和未合并分支保留；`git diff --check` 通过，WSL Python 运行 `quick_validate.py skills/taskflow` 通过。目标 `hkwuks/TaskFlow` 的 `main` 与任务起点 `8d6c477` 一致。主工作区已有未提交 Todo 不纳入本任务提交。
- 2026-11-19 重测：WSL Ubuntu 2 的 Unix 全套 `hooks/smoke-test` 返回 0，输出 `ALL SMOKE PASSED`。最小工具集加入锁释放所需的 `rmdir`；归档复制失败夹具改为目标路径冲突，以便在 Windows 盘的 WSL 挂载上可靠验证同一错误处理。
- Windows 全套 `hooks/smoke-test-windows.ps1` 返回 0；open-stdin 自检 138 秒通过。单独计时为 131 秒，原 90 秒上限会在本机误报；现异步读取子进程输出和错误流，并将上限调整为 240 秒以继续检测无限等待。
- 证据互斥聚焦夹具 `hooks/test-ledger-lock` 在 Windows Git Bash 通过：锁被占用时能力/外部记录不等待并不写入，审批和文档门禁拒绝，释放后恢复正常记录；journal 和异常恢复集成验证已通过。
- 缓存指导、worktree 显式交接/恢复、归档及清理提示已实现；保留子模块和非标准 Git 元数据布局为拒绝复用的边界。
- Windows Git Bash 真实 Git 夹具通过：未归档和脏目录拒绝、忽略文件冲突后恢复、分离 HEAD 与创建新分支后的故障恢复、多 Todo 已归档、旧任务证据恢复、未合并旧分支保留、已合并分支删除后 worktree 保留，以及后续 base 变动产生正常合并冲突。main 和旧分支在交接期间未移动。
- 证据保存前、保存后、分离 HEAD 后、创建分支后及恢复旧账本过程中断的故障注入均通过。
- 先前 Git for Windows 上的 Unix 测试及 Windows open-stdin 失败已分别用 WSL 完整回归和修正后 Windows 完整回归重新验证，均通过。


## Change Log
- 2026-11-19：用户选择通用规则与安全缓存；进一步明确切换前原任务必须归档，保留 worktree 不影响已合并本地分支按安全条件清理。
- 调研发现复用需保护 Git ignored 文件以及每 worktree 的证据队列和外部来源账本；加入失败关闭与恢复验收。
- 2026-11-19：用户批准 v1；初步实现非阻塞证据锁并通过聚焦测试，交接事务仍在实现。
- 用户指出此前只写目标未写选型；补全逐任务账本快照、共同互斥协议、journal 故障边界、旧账本恢复及独立本地分支清理的具体方案，并明确共享缓存的权限边界。
- 用户要求先切到 main 再创建新分支；固定已核实 main SHA，先以分离 HEAD 切到该提交，再从该 SHA 创建不自动追踪旧分支的新分支；增加分离状态的恢复测试；临时分离 HEAD 不应创建提交或改写历史，失败时禁止继续提交。用户进一步要求核验 main 引用、旧分支引用及提交图，明确后续并行修改仍可能引起普通冲突、未合并旧提交不会被自动带入。

## Follow-ups
- 不更改主工作区独立 Todo 原记录；后续按合并流程妥善对齐。

## Version History
- v1 — planning.
