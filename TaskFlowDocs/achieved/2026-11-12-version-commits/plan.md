# Plan — 仓库代码版本提交与回退点
> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md`

## Reference Pointers

- `skills/taskflow/references/versioning-and-recovery.md`：逻辑版本与 Git 历史的关系。
- `hooks/task`、`hooks/version`、`hooks/archive`：版本起点与全部结束入口。
- `CONTRIBUTING.md`、`CODE_STYLE.md` 和 `TaskFlowDocs/repository-docs/index.md`：独立工作树、提交及项目规则。

## Related Tasks

- `TF-20261112-21a0ce`：能力选择与真实效果调查，独立实现与验收。
- `TF-20261008-ca2fce`：长程任务兼容性待办，本任务不更改其状态。

## Skills / Tools Used

- [PRD] Unaided — 根据用户决定界定仓库级需求；considered: requirements elicitation
- [Spec] Unaided — 对照现有生命周期入口和 Git 状态设计；considered: architecture and design
- [Plan] Unaided — 首次制定时自行拆解；considered: work breakdown
- [Test] Unaided — 设计真实 Git 场景；considered: testing strategy
- 复审时读取 `agent-skills:planning-and-task-breakdown`，按依赖和可验证性修订方案；首次阶段已登记 unaided，不将本次读取伪称宿主观察。

## Preconditions

- 工作区：`D:/WorkSpace/Agent/TaskFlow/.worktrees/task-version-commits`，分支 `feature/task-version-commits`。
- 用户明确批准本版本计划后才开始产品实现。

## Plan Review

- Verdict: sound
- Coverage: PRD 关于仓库提交、纯任务记录及保守路径边界由 Step 1 覆盖；阶段性提交指导和恢复边界由 Step 2 覆盖；自动验证和不破坏用户文件由两步的真实 Git 验证覆盖。
- Verifiability: 测试以实际 Git 提交、工作区与退出状态检查条件；包含提交前拒绝和提交后成功的对照，以及直接 archive 和失败后文档不变，避免仅凭字符串或标记通过。忽略文件与人为归属不可验证，作为限制而非保证。
- Layer ownership: 版本基线与检查由生命周期脚本负责；现有 fixture 若因新基线契约改变，只在真正代表合法任务时补真实 Git 初始状态，绝不通过放宽检查让测试绿。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-12 16:05 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 建立版本起点与 Git 检查

- Goal: 为各任务版本建立 Git 起点，并在升版、完成和直接归档前检查整个仓库。
- Dependencies: 本计划获得用户批准。
- Files: `hooks/task`、`hooks/version`、`hooks/archive`、共享 Git 检查脚本和现有 smoke tests。
- Implementation checklist:
  - [x] 实现独立 worktree 的任务版本基线、出错回滚与仓库状态检查。
  - [x] 将检查接入三个结束入口并保留纯任务记录免提交行为。
  - [x] 以真实 Git 仓库覆盖提交、有未提交内容、版本切换、缺失基线、路径边界和并行 worktree。
- Acceptance: 当前任务记录以外的改动须在版本结束前提交；未提交、不可验证或已改写历史时不执行版本切换及归档，不更改用户文件。
- Verification: 对真实 Git 场景运行定向自动测试，断言实际提交范围、文件内容与失败前后的状态；运行相关 smoke。
- Rollback: 在任务分支回退本步骤提交。
- Status: done

### Step 2 — 规则和端到端复核

- Goal: 解释版本回退点和按影响增加提交的做法，明确用户数据、忽略文件和历史改写边界。
- Dependencies: Step 1。
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/versioning-and-recovery.md`、相关测试。
- Implementation checklist:
  - [x] 更新版本、提交、恢复和失败处理指导。
  - [x] 核对各入口及真实 Git 测试，运行适用项目检查并记录限制。
- Acceptance: 工作流规则与实际检查一致；Git 未能证明的归属和远端留存不被表述为已保证。
- Verification: 用户场景复核、针对性测试、项目规定的适用检查与差异审查。
- Rollback: 回退本步骤提交。
- Status: done

## Checkpoints

完成 Step 1 后核对失败不改用户文件；按变更影响创建聚焦提交。

## Verification / Review

- 已在 `hooks/version-baseline` 实现任务版本 Git 起点与工作区检查，接入 `promote`、`version`、`complete` 和 `archive`；当前任务在首次改代码前记录 v1 起点 `b502679ef2b517376336891a5524824c106e2c64`。
- 在 Git 元数据下保留真实仓库夹具：暂存、未暂存、未跟踪、其他任务文档、空格和中文路径、暂存删除、重命名、版本切换、直接归档、complete、worktree 隔离和非祖先历史均验证通过；每项拒绝均检查工作区或文档未被归档/升版。
- `bash -n` 覆盖六个修改或新增的 shell 脚本；`python evals/runner.py` 通过 6 项离线检查；`git diff --check` 通过。使用已有 torch Python 环境并设置 `PYTHONUTF8=1` 后，Skill 校验通过；默认 Python 缺少 PyYAML，未安装依赖。
- 用户同意清理测试自己新建的文件；在 WSL 私有内存挂载内移除 DAC 权限绕过能力后运行完整 `bash hooks/smoke-test`，结果 `ALL SMOKE PASSED`。该方式具备真实 Linux 不可写目录语义，Windows 专项子测试在前一轮单独通过；未运行 macOS CI。
- 采用 `agent-skills:code-review-and-quality` 自审 Git 入口、基线失败和数据保护；尚未有独立审查或三平台 CI。
- 审查中用真实 Git 夹具复现 `assume-unchanged` 会让已修改文件被普通状态检查漏掉；修复后拒绝隐藏索引路径，Windows 定向测试同时覆盖 `assume-unchanged` 与 `skip-worktree`，完整 Linux smoke 重跑 `ALL SMOKE PASSED`。
- 代码提交 `7fa00ab` 与 `1ddea08`；实际任务运行 `hooks/version-baseline check . 2026-11-12-version-commits v1` 通过，报告从 `b502679` 到 `1ddea08` 的提交范围。

- GitHub [Hooks CI](https://github.com/hkwuks/TaskFlow/actions/runs/43190832429) 在提交 `b3a90b7` 上通过 Ubuntu、macOS、Windows smoke、evals、Todo merge audit 和 CI 复用测试；release 按路径跳过。
- PR 模板 `.github/pull_request_template.md`：Summary 说明版本回退点及未提交变更拒绝；TaskFlow traceability 对应本任务、hooks/skill 范围、`hkwuks/TaskFlow:main`；Verification 对应 Hooks CI、`git diff --check`、Skill 校验及本 Plan；Review boundaries 对应秘密、文件范围、远端/基线和已知限制。
- 2026-11-12 只读核对 `origin` 为 `https://github.com/hkwuks/TaskFlow.git`，GitHub 默认分支 `main`，非 fork；`git ls-remote` 的 main 为 `b502679ef2b517376336891a5524824c106e2c64`，是当前任务分支祖先；远端状态会随时间变化。
- 已审查工作树变更只涉及本任务记录及已提交的 hooks / skill 文件；测试使用虚构 Git 夹具，不纳入凭据或用户文件。忽略文件、旧任务基线缺失和本地基线丢失的限制已写入 `spec.md`。

## Change Log

- 2026-11-12：用户明确检查整个仓库；复审补入可独立调用的 archive。
- 2026-11-12：用户确认 TaskFlow 任务记录以外的仓库路径采用保守提交规则；明确工作树起点、不可恢复历史与忽略文件边界。
- 2026-11-12：用户批准 v1；完成实现、定向 Git 验证和完整 Linux smoke，Windows 专项子测试通过；发现并修复 Git 隐藏索引标记绕过后重跑 smoke。

## Follow-ups

无。

## Version History

- v1 — ready，等待用户批准。
