# Plan — 改善 TaskFlow 能力选择与问题解决效果
> Task version: v1
> Status: planning

## Spec Pointers

- `spec.md`：已记录证据边界、三个候选方向及受控验证要求；尚未选定实施方案。

## Reference Pointers

- `TaskFlowDocs/achieved/2026-11-07-repro-requirement/`：原修复的机制和机械验收。
- `TaskFlowDocs/achieved/2026-11-10-codex-tool-guidance/`：真实失败案例与非阻断提示的验证边界。
- `hooks/hooks-codex.json`、`hooks/capability-gate`、`hooks/prompt-reminder`、`evals/README.md`。
- `TaskFlowDocs/repository-docs/index.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`。

## Related Tasks

- `TF-20261112-8dd98e`：仓库代码版本提交回退点，用户确认分开、关联并独立验收。
- `TF-20261110-0c7346`：既有真实宿主验证任务；报告交叉范围，不擅自修改。
- `TF-20261110-84d1a9`：流程与 Token 审视；不擅自修改。
- `TF-20261107-5c5ee2` 和 `TF-20261110-a56e72`：已完成的历史调查，需复核其交付有效性。

## Skills / Tools Used

- [PRD] Declared `agent-skills:debugging-and-error-recovery` — purpose: 重建真实失败、定位所属层；outcome: 区分记录、提示和模型行为；incorporated: 背景与验收。声明不表示宿主自动观测。
- [Plan] Declared `agent-skills:planning-and-task-breakdown` — purpose: 按依赖拆分调查、验证和改进；outcome: 区分可观测机制与行为验证；incorporated: 调查步骤。声明不表示宿主自动观测。
- [Spec] Unaided — 根据已读取源码和已调用技能的调查结果整理候选和边界；considered: architecture and design。阶段记录在首稿之后补录，不能声称写作前已通过门禁。
- [Test] Unaided — 制定真实行为与隔离验证口径；considered: testing strategy。

## Preconditions

- 工作区 `C:/Users/hk/.codex/worktrees/task-version-commits/TaskFlow`；分支 `fix/taskflow-capability-outcomes`。
- 计划及具体方案须经用户批准后实施。

## Plan Review

- Verdict: needs revision
- Coverage: 待真实行为基线和候选机制确定后审核。
- Verifiability: 自动审批拒绝真实模型基线，不能假设真实行为已经验证。
- Layer ownership: 须区分宿主事件、模型选择及最终问题解决，避免只做标记。

## Approval

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

## Steps

### Step 1 — 复核既有案例与真实行为基线

- Goal: 用历史记录和合适的实际宿主试验定位问题，记录能力选择、调查和产物。
- Dependencies: 用户批准了必要真实模型验证；实际测试的发送范围和目的地仍受自动审批约束。
- Files: 当前任务文档和必要的脱敏样本。
- Implementation checklist:
  - [x] 对照本次失败、digdig 历史案例与旧任务测试范围。
  - [ ] 明确真实测试的数据边界并获得必要授权，执行可复核基线。
  - [ ] 归纳已证实原因与待验证假设。
- Acceptance: 每条结论有证据来源和限制；不把离线字符串测试描述为模型测试。
- Verification: 复核事件、工具调用和实际产物。
- Rollback: 更正任务记录，不改写历史会话。
- Status: in_progress

### Step 2 — 形成候选设计与评估计划

- Goal: 对比提醒、工具接口、宿主覆盖与必要的门禁，选择真正改善结果的方案。
- Dependencies: Step 1 基线或明确的证据限制。
- Files: `spec.md`、`plan.md`。
- Implementation checklist:
  - [ ] 比较改动位置与副作用，列出明确可证伪的测试。
  - [ ] 计划审查后提交用户批准，再实施产品改动。
- Acceptance: 能覆盖实际问题而非仅生成标记；不擅自增加阻断。
- Verification: 回看原始需求并对照真实案例。
- Rollback: 修改设计记录。
- Status: pending

## Checkpoints

方案批准前不修改产品实现。

## Verification / Review

- 已读取调试和规划技能。规划技能默认要求 `tasks/plan.md` 与 `tasks/todo.md`；TaskFlow 将现有任务目录的 `plan.md` 和 `TaskFlowDocs/todo.md` 定为唯一事实源。因此采用规划技能的拆解方法、将内容写回 TaskFlow 文件，不额外创建第二套计划。该整合方式是依据两份指令作出的处理，尚未通过真实宿主端到端验证。
- `hooks/task approve` 源码明确说只验证 Plan Review 字段是否有答案，不能判断答案质量；真实缺陷调查和计划质量不能等同于字段齐全。
- 真实模型测试原先遭自动审批拒绝；用户随后同意向 Codex 模型服务发送测试提示、TaskFlow 规则和测试读取的仓库内容。
- 首次启动显示 provider=custom，立即中断；测试提示可能已发送，提供方的实际地址未知，未确认模型读取仓库内容。
- 显式使用 provider=openai 的只读试验中，模型实际读取调试与规划技能；提示明确要求检查这些技能，因此不能验证 TaskFlow 本身是否促成调用。启动时部分 hook 失败，模型列表刷新超时。
- 该模型还检索了授权范围之外的本机记忆文件；发现后立即中断，检索结果可能已发送给 OpenAI 模型服务。未进一步重复，真实测试数据边界需要可执行的隔离保障。
- `python evals/runner.py`：PASS (6 evals)；逐读 runner 确认这些是关键字和静态 fixture 检查，不能证明模型行为。
- `hooks/capability-evidence` 将 `mcp__*` 均记为调用，`hooks/capability-gate` 按先进先出把记录释放给写入的阶段；代码注释明确承认阶段归属不能从队列还原。由此只能判断事件被记录，不能判断能力相关性或实际结果。
- 查询了本机 CLI 功能开关：存在 shell_tool、unified_exec 等开关，但尚未证明禁用后能完全阻止通过其他工具读取本机数据；未再次启动模型。
- WSL Ubuntu 的用户/挂载命名空间可用于隔离 Linux 进程，但现有 pnpm 安装仅发现 `codex-win32-x64`，未发现 Linux 原生运行时；不能把 WSL 中启动 Windows 进程当作受 Linux 文件系统隔离。凭据必须同时与模型可调用工具隔离。

## Change Log

- 2026-11-12：用户确认分成两个关联任务，允许必要真实模型验证，先实测再决定机制；明确允许上述仓库数据发送，试验发生范围外读取并已中断。

## Follow-ups

真实宿主验证与既有 TF-20261110-0c7346 的边界待后续确认。

## Version History

- v1 — planning；需先形成可验证隔离和行为对照，再选择方案。
