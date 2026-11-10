# Plan — 宿主能力对齐
> Task version: v1
> Status: completed

## Reference Pointers
- `TaskFlowDocs/repository-docs/index.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`
- `skills/taskflow/references/runtime.md`、各 `hooks/hooks*.json`
- `hooks/capability-evidence`、`hooks/capability-gate`、`hooks/external-evidence`、`hooks/task`
- https://learn.chatgpt.com/docs/hooks
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/tool-skill/README.md

## Related Tasks
- Todo: TF-20261109-293987；接续已合并守卫 TF-20261109-e2df6d。
- Codex 工具引用引导 TF-20261110-a56e72 在本任务完成后独立处理；不能假定两者根因相同。

## Skills / Tools Used
- [PRD] Declared `agent-skills:debugging-and-error-recovery` — purpose: 复核宿主接线差异和现有失败；outcome: 已读取并按复现、定位、修复顺序调查，宿主未自动观测；incorporated: 区分可观察事件与记录缺口。
- [Plan] Unaided — none applied; considered: work breakdown and task decomposition.
- [Test] Unaided — none applied; considered: testing strategy.
- [Spec] Unaided — none applied; considered: architecture and design specification.
- [Research] `openai-docs` — purpose: 核实 Codex hook 事件；outcome: 官方文档确认 MCP 工具的前后事件；incorporated: 宿主矩阵与可观测性边界。

## Preconditions
- worktree `.worktrees/2026-11-10-host-capability-parity`；不修改用户基础工作区或全局宿主配置。
- Todo 已先于调查记录；初步调查在提升任务前进行，如实记录此顺序。

## Plan Review
- Verdict: sound
- Coverage: 矩阵对应验收 1；事件接线、阶段门和隔离测试对应验收 2；显式声明及审批对账对应验收 3；自动化、真实宿主探针和限制报告对应验收 4。Codex 工具引用引导保留为下一独立任务。
- Verifiability: 自动测试覆盖合成事件及声明、审批、拒绝、旧证据、任务和工作树隔离；可运行宿主另行实测。无法运行的宿主及任何未观察到的交互明确待验证，不以合成测试替代。
- Layer ownership: 宿主配置负责接线，共享 hook 负责识别事件，task 命令负责声明与审批，测试和文档分别验证和说明；不读取任意文件来推断调用，不修改用户全局配置。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-10 11:28 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan
- Recording exception: 用户明确批准 v1 后，`task approve` 因本任务自身要修复的 Codex 能力观测缺口而拒绝 PRD 阶段；已登记实际查询的外部资料，未将真实技能调用伪记为 unaided，也未伪造观测。此处如实记录用户批准，待声明路径修复后重新通过命令核对。

## Steps
### Step 1 — 核实宿主差异
- Goal: 形成五宿主逐能力矩阵，定位可观测事件与证据缺口。
- Acceptance: 区分已接线、未接线、确实不支持和未验证，并提供依据。
- Verification: 官方宿主契约、当前源文件、实际可用环境与针对性事件。
- Rollback: 不更改宿主安装；调查结论在任务文档中更正。
- Status: done

### Step 2 — 修复可观察路径与证据语义
- Goal: 接入 Codex 可观察 MCP 事件；依据已核实的 dsh 契约适配小写 skill、参数和可用事件，核对阶段写门和外部证据。新增最小明确声明命令，为不可观察使用记录 `declared` 来源，更新审批与相关队列读取路径。
- Acceptance: 宿主观测、声明、unaided 三种来源各自可辨；声明只针对当前工作树、任务、版本、阶段和能力，不能伪称由宿主观测，也不能改变用户审批要求。未确认的事件不猜测接线。
- Verification: 针对成功、失败、缺失来源、已有 invoke/unaided、重复事件、Test 特例、多工作树及并发/异常存储的必要回归；可行时真实宿主实测。
- Rollback: 回退本任务提交恢复原有接线和记录方式；不清理用户数据或配置。
- Status: done

### Step 3 — 审核各宿主覆盖
- Goal: 处理其余可支持差异，记录无法可靠承载和无法验证的项目。
- Acceptance: 逐项标明依据、静态接线、合成测试和真实宿主测试；不把未实现称为不支持或已验证。非阻断提醒保持非阻断，不强制重启会话。
- Verification: 对照宿主事件文档与配置逐项复核。
- Rollback: 更正文档和接线，不改用户全局配置。
- Status: done

### Step 4 — 验证与交付
- Goal: 运行相应 CI 与安全审查，更新用户可见文档。
- Acceptance: CI、宿主实测和限制分别报告，保留用户文件与配置。
- Verification: 三系统 CI、相关真实宿主探针及 `git diff --check`。
- Rollback: 若最终复核未通过则保留草稿 PR，不合并。
- Status: done

## Verification / Review
- Repository change layer: `skills/taskflow/` and `hooks/` change the plugin for every installing repository; they are not repository-only rules or templates.
- PR template `.github/pull_request_template.md`: Summary → observed gaps and fixes; TaskFlow traceability → task path, scope, target `hkwuks/TaskFlow` / `main`; Verification → CI run, `git diff --check`, Skill validation and Plan results; Review boundaries → secrets, unrelated files, remote assumptions and explicit host limitations. Open draft first and fill CI results before marking ready.
- 2026-11-10 初步事实：Codex 配置未把 `PostToolUse` 的 MCP 调用接入现有能力记录器，尽管官方 hook 文档描述了该事件；Skill 不应仅因普通文件读取而被当成已调用。
- dsh 官方文档确认模型可调用小写 `skill`，但用户显式调用可能通过注入而非工具事件发生。具体桥接版本和事件字段须进一步核对。
- 隔离夹具 `.diagnostic-20261110/` 实测：直接向现有 `capability-evidence` 投递 Codex 形状的 MCP `PostToolUse` 事件，得到 `invoke|mcp__example__search`；同一工作树的 `hooks-codex.json` 没有连接该记录器。Git Bash 曾报告 fork 资源重试，最终命令退出 0；该实验是合成事件，不代表真实 Codex 已投递。
- dsh 官方当前源码定义 `skill` 的输入字段为 `name`；当前记录器读取 `tool_input.skill` 且只接受大写 `Skill`。这是源码契约差异，仍需对应实际安装版本和真实事件验证：https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/skill/tool-skill/src/index.ts 。
- 本地环境版本：Codex CLI 0.167.0、Claude Code 2.1.311；当前 PATH 未发现 dsh 或 CodeBuddy，不能将其标为已真实实测。
- `external-evidence` 对 `PostToolUse` 只检查事件名和 cwd，再从输入和输出扫描 URL，不依赖 tool_name。现有 runtime 中以 dsh 小写名字论证该记录器不支持的说法与实现的判据不一致；桥接是否传递完整事件需要按当前版本核实，不能只改文档或仅按工具名否定。
- 2026-11-10 合成 dsh 形状事件：`PostToolUse` + `tool_name: skill` + `tool_input.name` 没有新增能力证据；使用小写 `search` 和响应 URL 的 `PostToolUse` 直接喂给 `external-evidence` 则成功记录 URL。配置尚未接线，此结果不代表真实 dsh 测试。
- README 已合并任务按用户要求归档；基础守卫任务的已合并部分与未验证部分需按事实区分，不能把未执行测试记为通过。
- 2026-11-10 Windows Git Bash 隔离夹具：声明不进入观测队列；dsh `skill`、`write`、`apply_patch` 和 Codex MCP 形状分别通过记录、释放及缺失证据拒绝测试；均为合成事件。
- 独立审批夹具分别通过 v1 声明审批及 v2 继承审批，输出明确区分 `declared (not host-observed)`；这些是假数据夹具，不代表实际宿主事件。
- dsh 当前官方桥接源码展示 PreToolUse/PostToolUse 按原始工具名和参数转发，PostToolUse 包含响应文本；本机未安装 dsh，版本与真实显示待验证：https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/hooks/hooks-claude-code/src/index.ts 。
- dsh 官方 MCP 客户端文档确认工具名形如 `mcp__<server>__<tool>`，与接线的 matcher 一致；这不代替真实 dsh 会话验证：https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/mcp/mcp-client/README.md 。
- Codex 官方文档将子代理启动单列为 `SubagentStart`，携带 `agent_type`；按该事件记录实际启动，不把普通文件读取视为 Skill 调用。新接线仍需真实宿主验证：https://learn.chatgpt.com/docs/hooks 。
- 初轮 CI 的 Windows smoke 通过；Ubuntu/macOS 先后暴露宿主状态措辞和新增测试脚本清单遗漏，已分别修复并发起后续 CI。目标平台结果以最后一次运行的实际状态为准。
- 代码提交 `3d4bc37` 的 [Hooks CI](https://github.com/hkwuks/TaskFlow/actions/runs/42752923550)：Ubuntu、macOS、Windows smoke、evals、Todo merge audit 和 changes 均通过；release 按变更路径跳过。`git diff --check` 和 bundled Python 的 Skill quick validation 通过。
- 用户验收前最终提交 `f4aeafc` 的 [Hooks CI](https://github.com/hkwuks/TaskFlow/actions/runs/42753684086)：三系统 smoke、evals、Todo merge audit 和 changes 均通过；release 按变更路径跳过。用户于 2026-11-10 验收可验证范围，真实宿主未测项继续跟踪。
- 审查：原测试对 dsh 未接线和 Codex 不记录 MCP 的断言随实际事件契约变更，现由配置与合成事件验证替代；新增声明来源、冲突、名称及版本继承检查。真实 Codex / Claude 异步提醒显示及 dsh、CodeBuddy、Trae 真实宿主端到端仍待验证，不能由合成事件或 CI 代替。

## Change Log
- 2026-11-10 建立任务草稿；实施方案和不可观测证据语义尚待确认。
- 2026-11-10 用户同意按来源区分声明，并先交付可验证的宿主部分；完成方案审查，等待当前版本实施审批。已合并守卫按批准范围归档，未验证项由本任务跟踪。
- 2026-11-10 用户批准 v1；审批命令因既有 Codex 能力证据缺口拒绝，记录真实审批并把重新核对作为本任务验证项。
- 2026-11-10 实现细化：声明使用独立的工作树内账本，而非进入自动事件队列，避免并发追加导致证据序号错配；批准范围和来源语义不变。

## Follow-ups
- TF-20261110-0c7346：真实宿主会话中的事件和异步提醒验证；现有能力对齐任务验收后保留此待办，避免未测项目丢失。
- 完成后开始 TF-20261110-a56e72。

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- 2026-11-09 实例：Codex 未接入 capability-evidence，Plan 阶段实际读取并使用 planning-and-task-breakdown 后，task approve 报 stage [Plan] was never released。不得将实际使用的能力伪记为 unaided；需支持可审计的真实调用记录与审批恢复，并验证真实宿主。关联任务 TF-20261109-e2df6d。
