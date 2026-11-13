# Plan — 改善 TaskFlow 能力选择与问题解决效果
> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md`：建议通过既有提示和阶段概念改善能力发现，保留 unaided 与现有门禁，七阶段分别验证能力选择和实际产物。

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
- 后续调查读取 `agent-skills:idea-refine`，比较实际能力选择、机制真实性和结果验证；与任务事实的决策均写入现有任务文件。
- 后续读取 `agent-skills:spec-driven-development` 重审规格：保留 TaskFlow 的 Spec 位置与标题，检查目标、命令、项目结构、代码约束、测试策略和边界；现稿仍缺选定的实施契约、各阶段可执行验收和完整测试命令，暂不视为可审批规格。该技能是在首稿后才读取，不能追称参与首稿。

## Preconditions

- 工作区 `D:/WorkSpace/Agent/TaskFlow/.worktrees/capability-outcomes`；分支 `fix/taskflow-capability-outcomes`。
- 计划及具体方案须经用户批准后实施。

## Plan Review

- Verdict: sound
- Coverage: Step 1 对应失败重建，Step 2 对应七阶段提示及兼容，Step 3 对应静态检查，Step 4 对应真实行为与产物验收，Step 5 对应交付和残留风险。七阶段中未达标的场景必须在 Step 4 保持未完成并回到 Step 2，不能以文字断言替代。
- Verifiability: 可运行现有脚本与有监督的真实宿主对照；规格、审查、构思各有一次候选提示对照，但其提示来自测试用户而非真实 hook，尚不证明新 hook 有效。对照须同时检查提示到达、能力选择与产物；不可运行或出现越界时记录失败，不能标记验收通过。
- Layer ownership: 能力发现提示属于 TaskFlow；方法与产物质量属于实际能力及验收。既有事件队列只证明记录，模型语义无法由字段证明；本方案不伪称修复事件错配或覆盖所有写入路径。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-12 19:29 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 复核既有案例与真实行为基线

- Goal: 用历史记录和合适的实际宿主试验定位问题，记录能力选择、调查和产物。
- Dependencies: 用户已知悉隔离限制并同意本机测试，指示仅读取测试仓库和必要技能、监控并在发现越界时中断。
- Files: 当前任务文档和必要的脱敏样本。
- Implementation checklist:
  - [x] 对照本次失败、digdig 历史案例与旧任务测试范围。
  - [x] 明确真实测试的数据边界并获得用户授权。
  - [ ] 依照用户批准的监控方式执行可复核的普通开发任务基线。
  - [ ] 归纳已证实原因与待验证假设。
- Acceptance: 每条结论有证据来源和限制；不把离线字符串测试描述为模型测试。
- Verification: 复核事件、工具调用和实际产物。
- Rollback: 更正任务记录，不改写历史会话。
- Status: in_progress

### Step 2 — 实现阶段能力引导

- Goal: 让既有提示要求按当前工作内容匹配实际能力，并让阶段表覆盖可用规格、探索和审查能力的概念。
- Dependencies: 本版本 PRD、Spec、Plan 经用户批准；Step 1 的可复核基线及其限制已记录。
- Files: `hooks/prompt-reminder`、`skills/taskflow/SKILL.md`；若验证发现需要，调整已有宿主连线和 `skills/taskflow/references/runtime.md`。
- Implementation checklist:
  - [ ] 为 planning、in_progress、checking 和无活动任务的开发入口审查提示时机与内容，保持只读任务、无适用能力和同阶段继续工作的合理路径；不得虚构具体阶段。
  - [ ] 在阶段概念中补充 Spec 编写等能匹配实际技能描述的用途；保留 TaskFlow 固定标题及任务文件作为唯一事实源。
  - [ ] 不新增调用记录字段、技能名称白名单或硬门禁；如需超出规格的机制，先修订规格并重新取得批准。
- Acceptance: 七阶段各有明确入口；提示要求检查描述、适用时先调用并审核结果；无合适能力可自行完成。既有状态、无任务及非开发请求语义不退化。
- Verification: 对照 Spec 七阶段矩阵、现有宿主 hook 表和现有 prompt-reminder 输出。
- Rollback: 恢复本 Step 相关文件至版本基线，保留用户文件及任务记录。
- Status: in_progress

### Step 3 — 验证提示契约与宿主覆盖

- Goal: 确认提示按状态输出、不产生副作用且不会损坏既有生命周期。
- Dependencies: Step 2。
- Files: `hooks/smoke-test`、必要的现有宿主测试与配置。
- Implementation checklist:
  - [ ] 覆盖 planning、in_progress、checking、无任务、多任务及非开发场景，验证状态输出、能力引导、unaided 和既有提示兼容；检验 hook 不修改工作区或 Git 状态。
  - [ ] 运行 `bash hooks/smoke-test <项目内测试夹具目录>`、`python evals/runner.py`、`git diff --check` 和仓库要求的 skill 校验；记录环境失败及回归。
  - [ ] 对照五个已声明宿主的提示入口，缺失或宿主不支持时核实并记录，不能仅按配置推断真实运行。
- Acceptance: 定向测试和适用本地检查通过；静态断言只证明提示契约。
- Verification: 记录命令、结果与保留的测试证据；PR CI 覆盖三平台。
- Rollback: 回滚本 Step 的测试与连线变更，不改变基线断言以掩盖失败。
- Status: in_progress

### Step 4 — 真实阶段和产物验收

- Goal: 确认真实模型收到产品提示后，适当地使用能力并产出满足任务的结果。
- Dependencies: Step 3；遵守用户已允许的测试范围、实时监控及官方缓存保留规则。
- Files: 当前任务 `plan.md` 与必要的项目内测试夹具；不写产品外配置。
- Implementation checklist:
  - [ ] 按 Spec 矩阵对定义／头脑风暴、研究、Spec、Plan、实现、测试审查、完成归档分别运行或复用有证据的正反场景；记录任务、能力、hook 提示、调用和结果，区分真实阶段与只读模拟。
  - [ ] 重放 Spec 遗漏、审查及构思场景，比较现有基线与实际产品提示；检查规格边界、根因／验证及方案取舍，使用无适用能力和无需发散的负对照。
  - [ ] 任何缺口重现、产物不可靠或提示不可达时，记录原因并回到 Step 2；缺少真实宿主结果的阶段不得称作通过。
- Acceptance: 逐阶段结果满足需求并可复核；不凭调用或声明数量宣布有效。
- Verification: 保存最小必要调用与产物证据，标明模型不确定性、失败、使用量和未覆盖宿主。
- Rollback: 清理本任务测试创建的夹具，保留官方插件更新及用户文件。
- Status: pending

### Step 5 — 交付审查与收尾

- Goal: 完成交付、提交回退点并如实记录限制。
- Dependencies: Step 4 全部验收通过及用户验收。
- Files: 任务记录、修改的产品和测试文件。
- Implementation checklist:
  - [ ] 复核差异与七阶段验收；提交至少一次本版本代码变更，必要时增加有意义的阶段提交。
  - [ ] 按 TaskFlow 完成归档与仓库 PR 流程；合并、推送及清理仅按用户已有授权执行。
- Acceptance: 用户问题得到实际解决、回退点和验证可追溯；所有未覆盖事项明确，不虚报完成。
- Verification: `git diff --check`、提交状态和用户验收。
- Rollback: 按提交回退本任务变更，保留无关工作。
- Status: pending

## Checkpoints

方案批准前不修改产品实现。

## Verification / Review

- 已按用户授权重新安装项目内测试插件并使用交互式 Codex `/hooks` 检查：启动时有 7 条 hook 待审查，其中 `UserPromptSubmit` 的一条来源为 `taskflow@taskflow-eval-local`；只对该条选择 trust，界面显示 Trusted，其余未全部信任。正常配置、禁用正式同名插件的非交互 Codex 会话未收到夹具任务状态；相同条件的交互会话显示 `Hook failed` 且模型答复无法取得任务状态，失败消息未识别具体 hook，因此不能断言失败一定由测试插件造成。事后只读核对本次测试会话记录，发现模型违背“不调用工具”提示，调用了工具目录查询，但没有读取任务文件；记录中未发现夹具任务编号或新增能力提示，故该轮不应描述为完全无工具。
- 测试会话可能受宿主配置／其他 hook 影响；没有识别确切的失败来源前不得宣称插件自动加载或引导有效。测试前配置与信任状态已按 SHA-256 还原，临时插件、快照和项目内夹具已删除。交互式 CLI 产生的测试会话记录尚保留；来源未明的 marketplace staging 未删除。

- Codex 真实宿主正对照：在项目内独立 Git 夹具，用仅本次生效的 `hooks.UserPromptSubmit` 配置和已审阅 hook 信任选项注入无副作用标识，模型在不读文件、不调用工具时准确返回 `HOOK_CONTROL_R7X42`，证明该配置路径可注入上下文。随后改为直接调用本工作树 `hooks/run-hook.cmd prompt-reminder`：planning、in_progress、checking 三个状态中，模型均在不读文件时返回夹具任务编号、版本、对应状态，并概括能力选择要求。此结果验证同一真实 Codex CLI 的临时 inline hook 送达，不证明通过安装插件的 hook 已加载，也不证明七阶段实际选择与产物质量。忽略用户配置时 shell 工具被现有策略拒绝，因而此对照不包含真实技能读取；夹具已清理。

- OpenAI [plugin documentation](https://developers.openai.com/plugins/build/plugins) 与 [hook trust documentation](https://developers.openai.com/codex/hooks) 说明插件安装或启用不会自动信任 hook；需在 `/hooks` 审查，或在已经审核所有启用 hook 的一次性自动化中使用临时信任选项。首次安装不触发探针与此一致，但不能单凭文档断言本机根因。
- 对已审核的临时插件，在市场源与安装副本均插入项目内调用探针；使用忽略用户配置和一次性 hook 信任选项时探针仍未出现，且 shell 执行被宿主策略拒绝。直接用同一 Windows launcher 执行该安装副本时探针出现并输出预期提示，说明脚本本身可在该夹具下运行；仍不能确定运行时是否加载了该插件。真实 hook 送达和七阶段验收未通过。
- 本轮插件测试结束后，先检查配置未被并发修改，再恢复测试前配置并以 SHA-256 核验；测试插件、配置备份和项目内夹具均已删除。

- 用户授权临时安装待测本地 TaskFlow 插件。安装后 CLI 显示启用，安装副本中的 `prompt-reminder` 起初与工作树 SHA-256 一致；真实规格场景无 hook 事件证据，模型未读取规格技能。随后仅在安装副本加入项目内文件调用探针，用默认配置和 `--ignore-user-config` 各试一次，探针均未生成；后者还阻止了 README 的 shell 读取。由于尚未证明运行时确实从被插桩副本加载 hook，不能据此断言 hook 一定未运行，但提示送达和效果均未验证。
- 已确认测试后配置未被并发修改，恢复前后 SHA-256 与测试前备份一致；临时插件缓存、配置快照和项目内测试夹具已删除。期间出现一个来源未确认的 marketplace staging 目录，依用户要求保留不擅自删除，官方插件更新未回滚。

- 2026-11-12 Step 3: 提示定向测试、eval 与技能校验通过；完整测试存在主分支同样的失败

- 2026-11-12 Step 2: 实现已提交，七阶段真实效果尚待验证

- 实现提交 `0dfe57b` 和布局修正提交 `4e03912`：共享提醒覆盖无活动任务的开发入口、planning、in_progress、checking；现有阶段表补充规格编写和可验证验收的匹配描述。无新增硬门禁、能力名称白名单或证据字段。
- 提醒相关原有 smoke 段落（包含 in_progress、checking、planning、无任务、ready、多任务、目录外静默以及强化资料顺序）定向运行通过；`python evals/runner.py` PASS (6 evals)，`git diff --check` 和 Bash 语法检查通过。skill 校验用 `PYTHONUTF8=1`、已有 torch 环境的 PyYAML 通过；基础 Python 缺少 PyYAML，未安装依赖。
- 全量 `hooks/smoke-test` 在 Windows 的无解释器夹具因 bash 共享库加载失败，未运行到提示段落；Windows 生命周期 smoke 在 complete 查找测试根目录时报 no active task。用主分支原始 Windows smoke 和相同类型的项目内夹具重跑，出现相同错误，故不能归因本次改动。两次失败均未证明全量 CI 通过；夹具已清理。
- 实际产品 hook 被真实宿主加载、七阶段行为及产物仍需验证；此前针对用户提示附加候选文字的对照不能冒充产品 hook 验证。
- 真实宿主加载尝试：在任务目录内建立独立 Git 仓库和本地市场，复制待测插件。CLI 能发现 `taskflow@taskflow-eval-local`，但临时 enabled 参数启动 Codex 后，该插件未出现在已安装列表，事件流没有待测 hook 调用证据；规格场景未见规格技能调用。此次不能作为产品 hook 成效验证。未通过写用户配置强行安装；测试夹具已清理。报告 usage input 158832（cached 126464）、output 1684。

- 七阶段静态核对（仅说明指引存在，不证明被模型执行）：定义阶段列出需求澄清、发散及缺陷调查；研究阶段列出检索与证据评估；设计阶段列出架构与接口；规划阶段列出拆解和依赖；实现阶段列出增量及代码规范；验证阶段列出测试与审查；完成阶段列出文档与决策记录。目录中分别可见 `idea-refine`、`spec-driven-development`、`planning-and-task-breakdown`、`incremental-implementation`、`test-driven-development`、`code-review-and-quality`、`documentation-and-adrs` 等候选，是否适用取决于具体任务。
- `capability-gate` 的阶段提示覆盖 PRD、Spec、Plan；`task declared` / `unaided` 接受 PRD、Spec、Plan、Test。研究、实现和归档虽然在技能表中有引导，但不是这些命令的独立阶段；这不是单凭覆盖差异就应增加标记的证据。任务后续须检查各阶段实际行为，尤其 Spec 遗漏与头脑风暴触发边界。
- 每轮提示覆盖差异：`hooks/prompt-reminder` 的 `planning` 分支提示考虑能力；`in_progress`/`checking` 的输出包含当前任务、可选强化资料、外部检索和变更分类，但没有对应的能力选择提示。技能总规则仍要求每一阶段实质工作前检查能力；两者说明提示时机不一致，不能单凭静态代码认定这造成了某次遗漏。研究、实现、验证与归档的真实调用和产物仍待验证。
- 已读取调试和规划技能。规划技能默认要求 `tasks/plan.md` 与 `tasks/todo.md`；TaskFlow 将现有任务目录的 `plan.md` 和 `TaskFlowDocs/todo.md` 定为唯一事实源。因此采用规划技能的拆解方法、将内容写回 TaskFlow 文件，不额外创建第二套计划。该整合方式是依据两份指令作出的处理，尚未通过真实宿主端到端验证。
- `hooks/task approve` 源码明确说只验证 Plan Review 字段是否有答案，不能判断答案质量；真实缺陷调查和计划质量不能等同于字段齐全。
- 真实模型测试原先遭自动审批拒绝；用户随后同意向 Codex 模型服务发送测试提示、TaskFlow 规则和测试读取的仓库内容。
- 首次启动显示 provider=custom，立即中断；测试提示可能已发送，提供方的实际地址未知，未确认模型读取仓库内容。
- 显式使用 provider=openai 的只读试验中，模型实际读取调试与规划技能；提示明确要求检查这些技能，因此不能验证 TaskFlow 本身是否促成调用。启动时部分 hook 失败，模型列表刷新超时。
- 该模型还检索了授权范围之外的本机记忆文件；发现后立即中断，检索结果可能已发送给 OpenAI 模型服务。未进一步重复，真实测试数据边界需要可执行的隔离保障。
- `python evals/runner.py`：PASS (6 evals)；逐读 runner 确认这些是关键字和静态 fixture 检查，不能证明模型行为。
- 合成真实 hook 事件：无能力记录的 Plan 写入被拒绝；单次 `mcp__unrelated__calendar` 事件后相同写入放行，`released` 记为 `Plan|1|invoke|mcp__unrelated__calendar`。夹具仅在当前 worktree 的 Git 元数据内创建并保留；这不是一次真实模型对照。 进一步在合成 `tool_response.isError=true` 后测试，Spec 写入仍放行；这证明脚本不检查该字段，不证明真实宿主失败事件一定使用此字段。
- `hooks/capability-evidence` 将 `mcp__*` 均记为调用，`hooks/capability-gate` 按先进先出把记录释放给写入的阶段；代码注释明确承认阶段归属不能从队列还原。由此只能判断事件被记录，不能判断能力相关性或实际结果。
- 查询了本机 CLI 功能开关：存在 shell_tool、unified_exec 等开关，但尚未证明禁用后能完全阻止通过其他工具读取本机数据；未再次启动模型。
- WSL Ubuntu 的用户/挂载命名空间可用于隔离 Linux 进程，但现有 pnpm 安装仅发现 `codex-win32-x64`，未发现 Linux 原生运行时；不能把 WSL 中启动 Windows 进程当作受 Linux 文件系统隔离。凭据必须同时与模型可调用工具隔离。
- OpenAI 的 [Sandbox security](https://developers.openai.com/api/docs/guides/agents-api/environments/security) 说明执行环境中的代码能够读取其可访问的文件和凭据，建议将应用凭据留在环境外；该文描述 Agents API，不能据此认定本机 Codex CLI 的具体配置已经安全。
- npm 元数据中的匹配 Linux 运行时解压约 459 MB；下载尝试未完成。尚无证据证明安装它即可同时隔离宿主文件及凭据，因此未继续下载或启动模型。
- 2026-11-12：对本机 `codex sandbox` 使用限制读取的临时权限配置执行无模型探针，命令报 `Restricted read-only access requires the elevated Windows sandbox backend`，未启动探针。该结果只说明当前后端未接受此配置，不证明其他后端已安装或可安全启用；未更改系统配置。
- 用户于 2026-11-12 明确同意在无法完全隔离时使用本机 Codex 测试，限定模型仅读取测试仓库和必要技能，并监控越界中断；知悉其他本机文件读取结果可能发送给 OpenAI。
- 使用 `debug prompt-input` 在当前目录检查新会话初始输入：可见项目指令和技能目录；没有发现记忆正文，唯一 memory 提及是通用指令中的例子。这是该调试命令在当前配置下的观察，不保证不同启动参数或宿主一致。`shell_tool` 和 `unified_exec` 当前启用，模型仍可通过工具读取可访问文件；此前试验已实际读取记忆。当前任务文档包含调查结论，也需要从盲测材料中排除。`codex mcp list` 返回没有配置 MCP 服务器，但不能由此推断所有插件或宿主工具均不可用。
- 普通规格场景：以用户此前的任务版本 Git 回退需求为提示，要求只读调查、输出规格草案，不指定专家技能，不读取现有任务文档、历史或个人文件。主动读取已安装 TaskFlow 技能、调查源码和测试并输出草案；可见调用中未见读取 `spec-driven-development`。草案识别了当前已有实现，但提出持久提交映射等额外需求，需与原授权边界对照，不能直接视为正确需求。此场景针对已实现的功能且只输出草案，不能代替原始任务或验证实际写文件阶段；工具输出有截断，不能断言调用清单完整。模型列表刷新超时但最终答复完成；报告 usage input 221905（cached 167808）、output 3088，不等同费用。
- 未定方向的头脑风暴场景：要求只读探索长程开发任务交接的方向与取舍，不指定技能。读取仓库中的 TaskFlow 规则及交接相关源码，提出四个方向、适用条件、风险和推荐；可见调用未见读取 `idea-refine`。这说明本次有产出备选方案，不证明已完成充分探索或适用能力引导成功；提示本身要求多个方向、是只读讨论而非真实 TaskFlow 定义阶段，且输出截断，不能作为完整调用审计。需补充已定方向的负对照、真实开发阶段与改进前后比较。报告 usage input 154397（cached 104960）、output 1444，不等同费用。
- 头脑风暴候选提示对照：同一交接需求，增加按发散构思、选项比较与假设检验检查适用能力、并读取指引的提示，不指定技能名称。模型读取 `idea-refine` 和 `doubt-driven-development`，提出五个方向、适用情况、成本风险及关键假设，建议先做交接演练；基线提出四个方向并建议就绪检查。候选输出更明确地区分了假设与证据，但一次开放式只读对照不能证明长期改进，且两次均未实际执行宿主开发阶段。模型遇到一次 context-mode 大文件读取拦截，随后改用局部搜索并完成；本次事件流输出保留命令与最终回复。报告 usage input 324175（cached 276992）、output 2721。
- 简单任务负对照：只读核查 README 中指定拼写错误并建议最小修改；模型未发现该错误，报告无需修改，未发散或读取专家技能。该场景是只读且指定错误不存在，说明一次简单核查没有机械触发发散，不代表真实修改阶段的普遍行为。报告 usage input 92071（cached 73472）、output 452，不等同费用。
- 规格候选提示对照：同样的 Git 版本需求与只读边界，额外要求按规格设计内容检查可用能力并读取适用指引，未指定技能名称。模型识别并读取 `spec-driven-development`，按 TaskFlow Spec 标题输出规格草案；基线轮次可见调用未见该技能。两次草案都提出持久映射及超出原需求的历史保留选择；因此这次提示改变了可见的能力选择与格式，但不能证明范围控制或问题解决质量得到改善，也不能证明因果或跨阶段有效。两轮输出均有截断、没有完整可审计日志；该对照不是完整宿主生命周期。报告 usage input 217016（cached 184448）、output 3497，不等同费用。
- `debug codex prompt-input` 默认与 `--disable plugin_discovery_prefetch` 的输出都未出现目标技能名称，不能证明该开关既保留技能目录又能阻止刷新。[官方配置参考](https://developers.openai.com/codex/config-reference/) 指出禁用插件不保证市场刷新不会更新文件；尚未验证无项目外写入且保留同等宿主能力的启动方式。后续真实实验不能假定只读模型工具也约束宿主后台行为。
- 用户更正授权：允许测试期间宿主自动更新插件缓存和临时目录，并要求测试后恢复。本轮前将 marketplace 与 plugin cache 复制到任务目录，逐文件 SHA-256 校验两侧均一致；审查场景完成后比较发现 marketplace 新增单个 staging 目录（20 文件），原文件内容无变化，plugin cache 无变化。已仅删除该新目录；再次核对两棵树的路径清单均与快照一致，随后清除本轮测试备份。此前未建立快照的旧测试无法还原到其测试前状态。
- 验证与审查阶段真实只读场景：要求审查 Git 回退点检查是否漏掉未提交变更，未指定专家技能。精简事件流保留本轮所有命令和最终结论，未见模型读取代码审查技能；模型静态提出子模块 ignore 配置及传入子目录作为根目录可能绕过检查两项候选，均未复现，不能当作已确认缺陷。模型有源码依据和复现建议，说明未读取专家技能并不自动代表审查无效；需独立复验结果，再与候选引导比较。报告 usage input 277171（cached 236416）、output 1834。模型列表刷新超时，最终 turn 完成后 MCP 退出异常，手动结束退出等待。
- 用任务目录内的真实 Git 临时仓库复验上述审查结果：`.gitmodules` 将子模块 `ignore` 设为 `all` 且子模块文件已修改时，手工在夹具的 `.git` 写入与 HEAD 一致的测试基线后，`version-baseline check` 返回 0，而 `git status --ignore-submodules=none` 显示 ` M module`；将仓库子目录传为 root 时脚本也直接返回 0。初次用 Windows 系统 `bash` 因 WSL 权限失败，改用 Git Bash；在此沙箱中 init 因 Git 返回的 Windows Git 路径被 Bash 当成相对路径而失败，因此手工建立夹具基线，只验证 check 而非完整生命周期。子目录是否为受支持 root 仍须对照接口契约；子模块问题及完整入口需另行处理，不将其计入本任务修复完成。
- 审查阶段候选提示对照：复用相同审查任务，加上按工作内容检查可用审查能力、适用时先读取指引的提示（未指定名称）。模型读取 `code-review-and-quality`，最终仍报告与基线相同的子目录和子模块两个候选。基线和候选各一次，能观察能力选择不同，不足以证明提示改善发现质量；调用日志过滤掉源码输出，只保留命令和最终结论。报告 usage input 243237（cached 197504）、output 1897。
- 回退点候选缺陷独立登记为 `TF-20261112-f593c5`。Git Bash 在默认沙箱内解析工作区路径两次报权限错误；获得执行权限后，`hooks/task intake` 成功，仅登记待办，尚未实现修复或验证完整生命周期。
- 本轮测试前逐文件 SHA-256 校验市场和插件缓存快照一致。测试后市场 `taskflow` 副本新增 8 文件、缺失 3 文件、16 文件内容改变；插件缓存 `openai-curated-remote/visualize` 缺失 49 文件。用户明确要求保留官方渠道更新、删除本次自行创建的内容；TaskFlow 市场更新保留，visualize 的删除来源不明，未覆盖。市场 staging 目录为空，项目内本轮测试快照已删除。

- 2026-11-13：Codex 0.167.0 的 App Server 报告已安装 TaskFlow 的 SessionStart 和 UserPromptSubmit 均失败（code 1）。PowerShell 原样执行配置中的带引号路径和参数时报语法错误，修复为经 `cmd.exe /d /c call` 启动。新增 Windows 配置入口回归；七个命令在带空格路径下经 PowerShell 与 cmd 均返回成功。临时安装待测插件并单独信任提醒 hook 后，真实 App Server 报告该插件 SessionStart、UserPromptSubmit 完成并注入合成任务状态；模型复述任务 ID 和 in_progress。该次只验证提示送达，不证明七阶段能力选择或产物质量。终端输出中中文显示异常，尚未区分测试管道显示编码与模型实际收到的文本，待字节级复验。完整 Windows smoke 在 `complete` 步骤报 no active task；此前原样主分支已复现。测试配置已按哈希恢复，临时插件缓存已移除。日志模块本轮未实施：宿主事件已识别失败来源，若后续确需日志，用户要求不阻塞并脱敏代码、个人信息与密钥。

- 2026-11-13：再次临时安装并单独信任待测插件的 UserPromptSubmit，准备复测规格、构思和审查。规格场景进程收到开发请求后，一条命令触发路径范围监控并被终止；监控器没有保存触发命令或原因，故无法判断是启动器路径误报还是实际访问越界，也无法证明越界读取未发生。该运行不作为通过证据。原配置按哈希恢复，测试插件缓存删除；后续试验须先改善监控审计，只保存允许范围与原因、不记录敏感内容。

- 2026-11-13：用户允许继续本机受监督试验。修正监控器对双反斜杠转义及技能目录的误判；它只按工具启动事件检查路径，非隔离，无法证明进程在中断前没有越界读取。真实 Codex 0.167.2、临时安装并单独信任候选插件：规格案例发起包含 `spec-driven-development` 的读取命令（未记录退出状态），草案覆盖全仓库、版本边界、纯任务文档例外、后续脏变更与失败场景；该仓库仅为合成夹具，草案未验证产品接入。头脑风暴发起包含 `idea-refine` 的读取命令（未记录退出状态），比较四种方向、代价和失败假设，提出接手人试验。审查发起包含 `code-review-and-quality` 的读取命令（未记录退出状态），识别此前独立复现的子模块忽略风险及尚需契约核实的子目录风险，模型本轮未运行复现。
- 本地合成研究正确指出 A/B 测量条件不一致且 C 无分母；未测试外部检索。决策记录发起包含 `documentation-and-adrs` 的读取命令（未记录退出状态），区分 README 事实和未验证部署。实现样本生成函数与四项边界测试，独立复跑通过，但未观察到明确的 Python 或 TDD 专家技能调用。以上均为单次或少量样本，研究与归档为只读模拟，不能代表完整生命周期。
- 规划基线两次读取 TaskFlow 并形成可执行计划，均未观察到任务拆解技能；因此将共享提醒补充为考虑生命周期之外、与当前工作匹配的研究、规格、任务拆解、实现、测试、审查及决策记录能力。更新临时插件后，Codex 因内容变化要求重新信任；只信任测试 UserPromptSubmit，App Server 确认新提示送达。一次规划复测发起包含 `planning-and-task-breakdown` 的读取命令（未记录退出状态） 并给出计划，但夹具比基线多了先前生成的函数，不能作严格对照。实现复测的四项测试独立通过，仍未观察到 Python/TDD 专家技能读取。新提示下简单拼写、计算和状态查询三项反例均直接回答，没有工具调用。不得将一次能力调用视为因果或长期有效性证据。
- 本轮 `python evals/runner.py` 为 PASS (6)，Bash 语法和 `git diff --check` 通过；临时配置差异仅为测试插件与测试仓库信任记录，已按原配置哈希恢复并删除测试插件，官方插件更新保留。真实外部证据检索、完整归档操作、其余阶段系统性正反例及跨平台宿主仍未验证，Step 4 不得标记完成。

- 2026-11-13：定位先前 Windows smoke 的归档失败：测试夹具位于现有 Git 工作树内且自身不是仓库，归档通过 `git rev-parse` 向上发现外层根目录。测试进程设置 `GIT_CEILING_DIRECTORIES` 后生命周期通过，并暴露旧 Windows 提示断言未随本任务修改；断言已更新。开放 stdin 自检的旧实现默认在系统临时目录创建子夹具，曾在项目外误建一次；已停止测试进程，通过创建时间和 smoke 任务 ID 唯一确认并删除该夹具。调整自检把子夹具放在项目内，并避免在子进程重复执行无关的 hook 命令检查。完整 Windows smoke 此后通过：双 shell 配置、launcher、SessionStart、lifecycle、pre-write gate、base guard、状态提醒、host parity、开放 stdin（71 秒）。`GIT_CEILING_DIRECTORIES` 仅用于测试进程，不改变用户 Git 配置。

- 2026-11-13：补充监控命令完成事件后，在 Codex 0.167.2 的三个独立只读样本中，包含 `planning-and-task-breakdown`、`spec-driven-development`、`idea-refine` 的命令均显示 completed、退出码 0 且有输出；命令可能包含多项操作，记录不含原始输出，仍不等于对技能产出贡献的证明。规划和构思结果分别提供可实施步骤以及方案取舍；规格样本增加忽略文件及修改后恢复仍强制提交等未确认假设，不能作为合格需求直接采纳。固定方向反例没有展开其他方向；简单规格修字和字符串长度直接回答。固定方向案例有一条 TaskFlow 命令退出 1，不能声称该命令成功。规划测试中 Git 尝试读取全局忽略配置并遭系统拒绝，说明命令级监控无法覆盖子进程间接读取；后续反例通过测试进程环境将 Git 全局和 XDG 配置指向测试仓库，未修改用户配置。
- 自动审批拒绝将当前 Codex 配置再次复制到测试目录，理由是可能包含认证和个人配置；采用只记录哈希的替代方式。结束时确认当前配置相对已有测试前备份仅有测试插件及测试仓库信任项的差异，检查无并发变化后恢复原配置并移除临时插件。测试前已获授权创建的备份随夹具删除。此处记录不足以证明所有间接读取都被阻止。

- 2026-11-13：构建独立合成 Git 仓库和任务工作树，使用真实插件提示测试完成归档。模型读取 TaskFlow 并检查批准、验收与脚本；首次因夹具验收字段缺失和关联 Git 元数据范围不明而拒绝归档，补齐合成事实及说明授权后重试，路径监控先后误拦 Git Bash 和另一个程序路径；另有一次包含归档路径的命令退出 1，未保存原始错误，模型未完成事务。随后在同一夹具提交由测试生成的仓库索引，直接执行 `hooks/task complete ... --user-accepted` 成功，独立回读确认活动目录不存在、归档目录存在、PRD/Plan 均 completed、Todo done。此项证明脚本事务，不证明模型端到端归档通过。
- 本轮自动审批拒绝在项目复制用户 Codex 配置，改为不创建配置副本：通过官方命令移除测试插件与测试市场，再仅移除预检确认原本不存在的 7 条测试 hook 信任项和 1 条测试仓库信任项；以 TOML 结构比较确认其余配置字段不变。自动审批还拒绝在未显示完整 hook 列表时一次性导航并确认；逐项展示并核对来源为测试插件的 UserPromptSubmit 后单独信任。

### 七阶段证据矩阵（未完成）

| 阶段 | 入口与可用能力 | 已观察到的行为与产物 | 反例与剩余缺口 |
| --- | --- | --- | --- |
| 需求定义／头脑风暴 | 阶段表的 divergent exploration；idea-refine | 真实模型调用含技能的命令退出 0；构思比较四个方向及代价和验证假设 | 方向已定的简单样本未发散；真实团队样本未验证 |
| 研究 | 阶段表的 literature and evidence review | 真实模型读取 openai-docs 的命令退出 0，调用网络检索并引用官方文档；核心结论已独立核对 | 简单计算直接回答；测试记录只保留检索事件及最终引用，未逐页审计全部搜索结果 |
| 设计／Spec | 阶段表的 technical specifications；spec-driven-development | 含技能的命令退出 0；草案覆盖全仓库和版本边界，但另一稿加入未确认假设 | 简单改字直接回答；必须审查并剔除越界假设，未证明技能输出直接带来质量改善 |
| 规划 | 阶段表的 work breakdown；planning-and-task-breakdown | 新提示下含技能的命令退出 0，形成步骤、测试和回退；旧提示两轮未观察到该技能 | 简单改字直接回答；复测夹具不同且样本少，不构成严格因果对照 |
| 实现 | 阶段表的 incremental implementation；Python／测试能力可用 | 两个合成模块样本的边界测试均经独立复跑通过；未观察到明确专家技能读取 | 简单单字符修复未观察到额外专家技能，实际提交并独立验证；更复杂任务的专家能力收益仍不确定 |
| 验证审查 | 阶段表的 testing strategy and code review；code-review-and-quality | 新提示下包含审查技能的命令完成、退出 0 且有输出；静态指出已独立复现的子模块风险 | 字符计数直接回答；子模块风险此前独立复现，本轮模型未动态复现 |
| 完成归档 | 阶段表的 documentation and decision；documentation-and-adrs | 决策记录草稿区分事实和验证缺口；真实模型执行合成归档命令成功，独立回读通过 | 简单状态请求直接回答；真实归档为单次合成样本，不代表其他宿主已验证 |

候选提示在规划样本中产生了可观察的技能命令，但各阶段样本量有限；在用户追加允许公开官方文档后，真实外部检索和模型驱动的合成归档均获得样本；仅一次、部分阶段仍是只读模拟，不能据此推断其他宿主或长期稳定性。当前任务保持 in_progress，待最终审查和用户验收。

- 2026-11-13：在新提示下补验审查阶段，`code-review-and-quality` 相关命令完成、退出码 0 且有输出；模型以源码为依据再次指出子模块忽略和子目录 root 候选，明确本轮只读未执行复现。子模块候选此前已独立复现，子目录是否受支持仍需核实。尽管测试进程设置 Git 全局/XDG 配置到夹具，模型报告 Git 曾尝试用户级 ignore 文件且被系统拒绝；该隔离策略未完全控制 Git 的间接读取，不能声称完全隔离。测试插件和测试市场通过 Codex 命令移除，只删除预检不存在的测试信任项并核对其余配置结构不变。

- 2026-11-13：用 WSL Ubuntu 在项目内、基于已提交版本 `fceeef5` 的独立 Git 副本运行 Linux Bash smoke，临时目录均放在该副本内。原样运行通过版本回退点、生命周期、无解释器等检查后，在归档不可写目录测试失败；在同一挂载点实测 `chmod a-w` 后仍可创建文件，表明 Windows 磁盘的 WSL 挂载无法构造该测试前提。仅在一次性测试副本中将该条断言明确标记 SKIP 后续跑，全部后续检查到达 `ALL SMOKE PASSED`，包括本次 prompt-reminder 的活动任务、无任务入口、顺序、只读和五宿主配置接线。由于有一项跳过，这不是完整无跳过通过；产品仓库测试脚本未删除或放宽该断言。Linux 测试副本已删除。

- 2026-11-13：为补验 WSL Windows 挂载不执行 chmod 的断言，在项目内临时目录建立仅该次进程可见的用户、挂载及网络命名空间，在其中挂载临时 Linux 文件系统；以去除 DAC 绕过能力的进程实测去写权限后写入被拒绝。将当前提交代码归档到该临时挂载的独立 Git 夹具，未修改 smoke 脚本，完整运行 `hooks/smoke-test`，包含不可写目录断言、五宿主接线和提醒回归，最终 `ALL SMOKE PASSED`。进程退出后确认私有挂载消失并清理项目内测试目录。此结果补足上一轮 Windows 挂载跳过项；真实其他宿主的行为验收仍不由此推断。

- 2026-11-13：用户明确允许测试模型访问公开官方文档，继续禁止读取其他本机文件。真实研究场景中 `openai-docs` 命令 completed、退出 0 且有输出，网络检索有启动与完成事件；模型引用官方文档判断插件安装不等于 hook 信任，已由本任务独立核对官方文档。日志仅保留检索事件类型及最终引用，未逐页记录或审计所有搜索结果，故不能证明所有搜索中间结果均来自官方站点。
- 真实归档场景使用合成 Git 工作树和已批准的模拟任务；首次模型正确因未提交的测试索引阻止归档。该索引在合成仓库单独提交后，模型执行 `task complete` 的命令 completed、退出 0；独立回读确认活动目录不存在、归档目录存在、Todo done 且指向归档、PRD 和 Plan completed。任务归档文档留在合成工作树未提交；本项仅是一次可控样本。
- 简单实现反例在合成任务工作树将减一修正为加一，没有观察到额外的 Python/TDD 专家技能命令；模型报告并实际创建代码提交 `c83821b`，独立检查提交差异及 -1/0/1 三个输入通过。模型一次报告 Git 元数据沙箱写入失败后重新尝试成功，不能推断所有权限环境一致。
- 规格草案曾将未确认的边界写成要求；将能力提示补充为核对已确认范围并标明未确认假设。重新安装测试插件并单项信任后，App Server 观察到包含新提示的 UserPromptSubmit 成功；模型的规格技能相关命令退出 0，一份完整样本将任务文档范围、撤销修改和回退点含义列为待确认，并保留对忽略文件的默认假设，不能声称范围风险完全消失。简单改字反例直接完成，已定方向反例没有发散；其一条 TaskFlow 命令退出 1，不能作为成功调用。`python evals/runner.py` PASS (6)，直接 hook 输出和 Bash 语法检查通过。

## Change Log

- 2026-11-12：应用户要求将工作树复制到项目 `.worktrees/capability-outcomes`，逐文件校验后修复 Git 登记。Codex 应用拒绝附加非托管工作树；旧目录保留，后续命令须显式使用项目内路径。

- 2026-11-12：同步已合并的 `main`；在任何产品代码修改前记录 v1 Git 基线 `d0b5ebc748703acd19f275f3d423959b0557a9fb`。真实 hook 夹具复现无关 MCP 事件可释放 Plan。

- 2026-11-12：用户确认分成两个关联任务，允许必要真实模型验证，先实测再决定机制；明确允许上述仓库数据发送，试验发生范围外读取并已中断。

## Follow-ups

真实宿主验证与既有 TF-20261110-0c7346 的边界待后续确认。

## Version History

- v1 — planning；按用户批准的数据边界运行行为对照，再选择覆盖七阶段缺口的方案。
