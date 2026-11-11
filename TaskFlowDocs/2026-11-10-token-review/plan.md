# Plan — 审视 TaskFlow 流程中的不合理环节和 Token 开销
> Task version: v3
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers

## Related Tasks
- TF-20261110-84d1a9；与 TF-20260919-90797c 子 Agent 成本和 TF-20261011-e27329 文档历史重复相关，保留独立 Todo，不擅自合并。

## Skills / Tools Used
- [PRD] Unaided — none applied; considered: requirements elicitation and framing.
- [Spec] Unaided — none applied; considered: architecture and design specification.
- [Plan] Unaided — none applied; considered: work breakdown and task decomposition.
- [Test] Unaided — none applied; considered: testing strategy.

## Preconditions
- 历史会话只提取与流程和 Token 有关的脱敏证据。
- 本版本工作区为 `.worktrees/2026-11-11-token-review`，分支为 `feature/token-review`；保留两个专项 Todo 的独立验收边界。

## Plan Review

- Verdict: sound
- Coverage: Step 5 覆盖各阶段证据、对照与未知项，Step 6 覆盖有明确收益的候选及不修改的结论；已完成的去重专项保留原记录。
- Verifiability: 核对各阶段命令输出与只读会话事件；输入包含缓存、单次峰值不等同累计量；CI 复用及宿主送达分别按真实证据判断。
- Layer ownership: Todo 检索指导属于 Skill；宿主工具指令和 GitHub 检查不由 Skill 代替，测试不得靠修改中间产物掩盖问题。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-11 16:08 +0800
- Approved version: v3
- Approved scope: PRD / Spec / Plan

## v3 初步证据与待判定事项

- **入口与定位：** 当前 `todo.md` 为 79,691 字节；对已知 ID 运行 `hooks/task get` 的两个示例输出分别为 1,024 与 5,173 字节。输出大小不等于 Token，但说明针对已知条目不必默认读取整份文件；完整条目仍包含原有说明。跨条目重叠检查不能因只看一个 ID 而省略。
- **规划与提示：** 当前 Skill 70,173 字节。模拟规划阶段的 `UserPromptSubmit` 输入得到 326 字节、两行提示；无活动任务入口文案为 664 字节、六行。这只验证本地合成输出和静态大小，不能证明每个宿主实际送达，也不代表 Token 或成本。
- **执行与委派：** 一组同模型同题 CLI 试验，直接组累计输入 156,763（缓存 78,592）、输出 1,030，主线单次输入峰值 49,972；委派组主 Agent 输入 217,010（缓存 174,976）、输出 913、峰值 41,676；子 Agent 输入 165,794（缓存 142,720）、输出 669。父子分别来自各自会话记录，缓存包含在输入中；按父子相加是样本指标，不等同账单。CLI 总耗时约 119.3 秒和 132.7 秒，含初始化和等待。两组主要结论接近，单样本不能推导通用委派阈值。
- **工具结果体积：** 同一试验中，直接组工具输出合计约 71 KB；委派组主 Agent 约 36 KB、子 Agent 约 73 KB。它们是日志输出字节，不等同主线上下文增量或 Token；在这一题中委派降低主线单次输入峰值但增加父子累计输入。
- **验证与归档：** PR #136 归档提交修改 `TaskFlowDocs/todo.md`，该路径被 CI 复用方案明确排除，三系统完整 CI 重跑并通过。这是按原安全设计的保守回退；不能称复用故障，也不能未经差异安全证明就跳过。
- **历史与宿主边界：** 文档历史重复已由 `23e4a89` / `TF-20261018-0f2f6a` 解决，当前模板只在 Plan 中生成历史章节；旧归档不改。Codex 桌面 worktree 路径/托管冲突来自宿主工具要求，TaskFlow 不能覆盖更高层指令。
- **仍未知：** 一组委派样本不能给出通用阈值；外部搜索组未隔离宿主指令且样本仅一题，不能证明搜索倾向的因果变化。只有两条持久 CLI 试验会话及可能的子会话得到用户授权，不新增项目外试验会话。

## v3 候选及决策

- **已实施，待 CI：** 使用已有 `task get` 定位已知 Todo；比较重叠时仍读取每个相关条目，全库结构审查可读全文。不增加脚本、模式或依赖；实际模型采纳和 Token 节省未验证。
- **暂不改：** 规划阶段提示的合成输出为 326 字节，无任务入口为 664 字节；真实送达及必要提醒的效果未测，暂不为少量静态文字牺牲防漏保护。
- **暂不改：** Skill 全长 70,173 字节和一次试验的输出体积提示有进一步调查价值，但单样本不支持大规模拆分或删除规则。
- **单独保留：** 归档 `todo.md` 不复用 CI 是已批准的保守设计；无可靠差异证明不跳过。子 Agent 成本及搜索因果效应留在原专项，文档历史重复由既有任务解决。



## Steps

### Step 5 — 补齐总体流程结论
- Goal: 对任务入口、规划、实施、验证和收尾分别建立证据与成本矩阵，不把个别修复等同整体优化完成。
- Dependencies: v3 计划审核和用户批准；利用已授权的脱敏历史记录及两组试验，不擅自新增项目外会话。
- Files: 本任务记录、现有 `skills/taskflow/SKILL.md` 与相关 hooks；必要时引用关联 Todo。
- Implementation checklist:
  - [x] 复核现有同题会话：分开报告主线单次输入峰值、父子会话累计输入、缓存、输出、耗时和结果质量，写明单样本局限。
  - [x] 对入口、规划、实施、验证、归档逐项梳理已观察的重复、必要成本、尚不能确认的问题和已有修复，区分 TaskFlow 与宿主规则。
  - [x] 对候选按收益、风险和实现/验证成本排序；仅对证据充分且值得修的问题提出具体轻量方案。
- Acceptance: 每个阶段有明确结论或可追溯的未知项，既有两项已交付改进不冒充整体完成；无可靠数据时不虚构节省数。
- Verification: 核对日志事件、源文件、任务和 CI 记录；缓存不重复计入，工具调用数不等于 Token。
- Rollback: 纠正记录，不修改用户历史会话。
- Status: done

### Step 6 — 经确认的候选改进
- Goal: 只实施用户明确确认、收益足以覆盖复杂度的具体改进。
- Dependencies: Step 5 的证据与具体方案；如没有值得实施的候选，如实保留调查结论。
- Files: 按候选明确，不预设增加脚本或依赖。
- Implementation checklist:
  - [x] 审阅并按用户确认决定实施或不实施每个候选。
  - [ ] 验证获批改动，并记录未验证的行为。
- Acceptance: 具体变更与结论相符，不损害用户控制、验证和可追溯性。
- Verification: 按候选运行必要检查和 CI；不改代码时核对引用与统计即可。
- Rollback: 回退获批改动。
- Status: in_progress

### Step 3 — 整体流程与专项对照
- Goal: 检查整体流程 Token 成本、委派及外部搜索对照，以及文档语义重复。
- Dependencies: 形成完整可审阅方案、Plan Review 并获得 v2 批准。
- Files: 当前任务材料；只读样本来自现行 `skills/taskflow/SKILL.md`、`hooks/task`、`hooks/prompt-reminder`、`hooks/archive`、`hooks/reopen`、Todo 及用户授权的脱敏历史会话。
- Implementation checklist:
  - [x] 脱敏检查真实历史会话和现行流程，在不等同调用次数与 Token 的前提下列出具体候选。
  - [x] 做少量同题对照，控制任务、基线、工具可用性、时间及输出要求；分别记录主线上下文、总 Token、耗时、事实覆盖、正确性与来源。独立设计有无 TaskFlow 上下文的外部搜索对照；无法观测或控制的字段如实报告。
  - [x] 审查文档语义和历史重复，不改写旧归档。
- Acceptance: 可追溯数据及限制，提出最小候选；小样本不外推。
- Verification: 核对实验边界、口径、计数及来源；与现有 Todo 独立交叉引用。
- Rollback: 更正任务记录，不更改历史会话。
- Status: done

### Step 4 — 验证并实施已批准的最小改进
- Goal: 只对有证据、值得修的流程或模板实施轻量改进。
- Dependencies: Step 3 和具体改进方案获批。
- Files: 以调查结果为准，候选集中在 `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`hooks/task` 和已有针对性测试；不提前扩大范围。
- Implementation checklist:
  - [x] 逐项评估性能、可靠性和用户决策的影响并实现获批项。
  - [x] 执行针对性测试及 CI，并明确剩余验证。
- Acceptance: 不损害必要质量和追溯，实测证据支持改进。
- Verification: 针对性测试、适用的跨平台 CI 和复核。
- Rollback: 回退任务变更。
- Status: done

### Step 1 — 历史样本与流程检查

- Goal: 比较真实会话和当前流程，发现可验证、值得简化的环节。
- Dependencies: 用户授权脱敏查看。
- Files: 当前任务记录与必要的脱敏证据。
- Implementation checklist:
  - [x] 对照同一会话不同任务及其他适用历史会话，分析耗时、调用和可用 token 记录。
  - [x] 比较 Todo 去重、子 Agent 和文档历史重复的范围。
- Acceptance: 形成证据、限制与具体候选，不把关联推为因果。
- Verification: 按会话、时间与任务边界核对差值及来源，保护敏感数据。
- Rollback: 更正记录，不改用户历史会话。
- Status: done

### Step 2 — 审核并实施选定改进
- Goal: 在 Todo intake 的现有候选比较中识别常用中文的相邻双字，不自动合并条目。
- Dependencies: 第一阶段取证完成、具体方案与用户批准。
- Files: `hooks/task` 和候选比较相关回归测试。
- Implementation checklist:
  - [x] 实现不依赖新运行时的 UTF-8 常用汉字相邻双字候选；保留既有英文及提示上限。
  - [x] 验证中文改写、无关目标、混合语言、重复词和正常英文，明确扩展字集限制。
- Acceptance: 复现的中文近似目标提示候选，不误合并，也不牺牲关键验证或用户决策；无可比数据时不声称节省百分比。
- Verification: 在隔离 Todo 夹具验证命中、误报及跨平台 CI。
- Rollback: 回退本任务改动。
- Status: done

## Checkpoints

## Verification / Review
- 2026-11-11 v3：按用户批准，在 `skills/taskflow/SKILL.md` 增加已知 Todo ID 时优先 `hooks/task get` 的指导；明确重叠检查仍需读取全部相关条目，全库审查仍可读取整文件。不增加 CLI 参数、脚本、依赖或守卫。
- 手工验证：对 `TF-20260919-90797c` 和 `TF-20261110-84d1a9`，分别比对 `task get` 与 Todo 中对应完整非空正文，输出为 5,173 和 533 字节；同期 Todo 全文为 79,694 字节。字节量不是 Token，不代表模型一定会按指导执行。`quick_validate.py` 与 `git diff --check` 通过；尚未运行本版 CI。
- 用户授权的同一 TaskFlow 聊天三段日志中，调用文本包含 Todo 路径分别为 9、22、94 次，包含 Skill 路径分别为 2、4、64 次，包含 Plan 路径分别为 5、24、191 次。仅是字符串命中；批量调用、重复记录和其他输出可能混入，不能视为实际文件读取次数、浪费或可归因 Token。

- 2026-11-11 Step 5: 已核对五阶段证据、计量口径和轻量候选；单样本与宿主边界明确。

- 2026-11-11 Step 4: 本地针对性检查及三系统 CI 通过；Token 与模型采纳边界已记录。
- 2026-11-11：修正旧文案检查后，[草稿 PR CI](https://github.com/hkwuks/TaskFlow/actions/runs/42976875246) 的 Ubuntu、macOS、Windows smoke、CI 复用测试、Todo 审计、changes 与 evals 全部通过；release 按路径分类跳过。真实 Agent 对文案的采纳、委派的子 Agent 总 Token、搜索倾向的因果效应仍无充分证据。
- 2026-11-11 草稿 PR 首轮 CI：Ubuntu 与 macOS smoke 均在旧文案固定检查失败，Windows smoke 通过。依据已批准的新规则更新 `hooks/smoke-test` 的现有契约检查，分别确认沿用既有决定、未决事项仍询问、不擅自合并；`bash -n hooks/smoke-test`、三项局部检查与 `git diff --check` 通过。该修改发生在检查拥有层，反映用户批准的行为变化，并非绕过失败；等待新一轮 CI。
- 2026-11-11：用户批准两项 Skill 文案改进后，仅修改 `skills/taskflow/SKILL.md` 中重叠选择与重复归档说明；主 Skill 从 70,351 字节变为 70,173 字节（净减 178 字节），不是 Token 测量。
- 本地验证：Skill `quick_validate.py` 通过；`git diff --check` 通过；只读断言确认已明确决定可沿用、未决事项仍需询问、不擅自合并的约束以及归档失败保护和完整事务说明均存在。未修改测试期望或归档脚本；尚未运行 CI，文本送达不等同模型采纳。

- 2026-11-11 Step 3: 已完成脱敏调查、单题对照及文档抽样；Token 和一般化结论不可测的边界已记录。
- 2026-11-11 主线直接对照与委派对照：两组回答同一 `hooks/task` get/next/state 问题，均说明写入与审批边界；直接组报告 3 次工具调用及约 28.3 秒，委派组自身 3 次（其中一次因失效 cwd 失败）、子 Agent 3 次，端到端时间不可比。双方最终指出临时文件和 state 非跨文件事务；实际主线和子 Agent Token 均不可得。仅单次样本，不能证明总成本或结论质量的普遍差异。
- 外部搜索小样本：两组回答同一 Git 官方文档问题，A 不额外加载 TaskFlow 指引，B 额外读取指定 Skill 段落；两组均查官方资料并正确回答。双方宿主指令和可用 Skill 未隔离，A 的问题还明确要求来源，仅能观察本次行为，不能推断 TaskFlow 是否改变一般搜索倾向；Token 和可比的端到端耗时不可得。
- 近期 25 个归档任务的长行相似度筛查发现多个高度相似对；抽查发现 PRD 的外部来源与 Plan 的参考指针，以及 PRD 实施范围与 Plan 的落点说明存在重复。部分承担不同职责，不能凭相似度自动删除，也未量化 Token 损失；本次不改旧归档。
- 当前 Skill 为 70,351 字节；其状态说明与完成归档章节中重复描述归档事务，明确重合的长段落分别位于 `skills/taskflow/SKILL.md:200` 与 `:361`。字节数不是 Token，精简后的实际节约和行为影响仍须验证。
- 单个授权历史长会话中记录 25 次问题工具调用、共 33 个问题；按字词粗筛 17 次含批准/同意/验收，16 次含范围/方案/处理/如何/哪些，两类重叠。它跨多个任务且含必要决策，不能认定任一调用多余或计算省费比例。
- 2026-11-11 试运行：同题只读检查 `hooks/archive` 与 `hooks/reopen`，主线有既有上下文且使用 1 次工具调用，子 Agent 用 3 次调用并报告命令时钟约 16 秒、额外发现归档复制会话记录；条件不等且未记录端到端同口径耗时，不能作成本或质量胜负结论。子 Agent 工具未提供 Token 用量；当前日志能观察主会话累计字段，但尚不能归并子 Agent 用量，禁止将不可测写作零。
- 最近 25 个归档任务的 PRD、Spec、Plan 中未检出至少 45 字符的逐行重复；该机械筛查不能排除语义重复或其他样本。
- 2026-11-10：只读抽样当前 TaskFlow 会话。README 文档任务单次相关轮次记录 12 条命令；宿主对齐及后续工具引导跨多个工作步骤的一轮记录 164 条命令。样本不是对照实验，命令数不是 Token 数，不能据此推导节省比例。已观察到归档文档提交及验证记录可触发后续 CI；具体是否不必要须结合当时规则和检查用途分析。
- 当前设计中 `tools/workflow-affected` 对整个 PR 与基线的差异分类；文档跟进的 CI 重跑由独立 Todo TF-20261110-b73d49 处理，本任务只记录跨流程成本。
- 2026-11-10：只读汇总当前历史会话的 token_count。最近一个分段最后一次统计为累计输入 261,825,512、缓存输入 259,895,680、输出 362,449；这属于长会话累计值，各分段可能共享累计口径，不能相加、不能把缓存输入等同于未缓存成本，也不能归因到某一任务或流程。后续应基于连续事件差值、实际阶段边界和可比样本评估。
- 进一步按 task_started/task_complete 与累计计数差值核对两个复合轮次：前者输入 55,570,057（缓存 55,262,464）、输出 87,888；后者输入 39,406,742（缓存 39,309,696）、输出 44,798。轮次分别包含多次用户交互和多个任务，非单个阶段或机制的因果成本，也不能直接作为浪费数。
- 对 Todo 比较的只读代码核对与隔离夹具发现：`hooks/task` 的 `tokset` 仅保留 ASCII 字母数字，虽然注释提及 CJK；两个纯中文、仅首词不同的目标连续 intake 都未报告候选。这证明当前机制无法比较该类重叠，但不证明所有中文任务都重复，也不量化 Token 浪费。需要评估轻量中文候选识别与误报、UTF-8/多平台约束；不静默合并。
- 2026-11-10：抽查最近四项已归档任务的 PRD、Spec 和 Plan 标题，未发现三个文档均各自带 Change Log/History 标题；其中两份 Plan 同时有 Change Log 和 Version History。该抽样不能排除正文重复，也不能据此关闭 TF-20261011-e27329。
- TF-20260919-90797c 同时要求对照评估子 Agent 主线上下文、总 Token 与质量，并包含 TaskFlow 对外部搜索倾向的对照问题。当前会话无法自动派生同任务对照，且只有历史多任务累计用量；不能宣称委派更省或改变外部搜索倾向，原 Todo 保留。
- 对该会话四段 JSONL 的工具名称做脱敏计数，没有发现名为 `spawn_agent` 或包含 `collaboration` 的调用；此检查依赖日志工具命名，不能排除其他形式的委派，更不是委派与直接执行的对照实验。
- 2026-11-10：用户批准中文 Todo 方案，Windows Git Bash 隔离输入分别验证纯中文近似命中、无关中文不提示、英文与中英混合命中；仍需 CI 跨平台和更广的误报评估。
- 另验证重复英文单词按集合去重计数后不降低相似度；本实现只识别 U+4E00–U+9FFF 的相邻双字，不声称支持扩展汉字或语义同义词。
- 对当前 12 条未完成 Todo 按相同阈值计算 66 对组合，未产生候选；这是小样本的噪声观察，不代表不存在漏报或误报，也不代替人工语义比较。
- 首轮 PR CI：macOS 的 Bash 3 在嵌入 shell 单引号的 awk 程序注释中遇到撇号而解析失败；Ubuntu 测试中 `head` 提前关闭管道触发 `pipefail`。移除注释撇号、先完整捕获命令输出后用 awk 读第一行，再等待新一轮 CI。
- 修复后的 [CI](https://github.com/hkwuks/TaskFlow/actions/runs/42791861336) 的 Ubuntu、macOS 和 Windows smoke 均通过；release 和 evals 按路径分类跳过。用户于 2026-11-10 按已验证范围验收并同意归档。

## v2 已交付的改进
- 在 `skills/taskflow/SKILL.md` 的 Todo 重叠规则中明确：如果用户在当前会话已经清楚决定相关条目的关系或处理方式，报告该决策并沿用；只有决策尚不明确时才再次询问。保留发现重叠、保留独立需求和不擅自合并的要求。现有文字对所有真实重叠一律要求再次取得选择，可能重复用户已作出的决定；不将本次宿主工具冲突误归因于此规则。
  - 拟替换语义：`If the user has already clearly decided how the overlap is handled, state and follow that decision; otherwise ask the user before planning.` 其余不静默合并、不覆盖独立需求的规则保留。
- 删除状态定义中与归档章节重复的事务细节，保留状态含义和指向完整归档事务的引用；归档章节、完整性校验及失败处理保持原样。涉及 `skills/taskflow/SKILL.md` 一处，现有发布和语法检查仍适用；这只是几百字节级的静态精简，不宣称实测 Token 或时间节省。
- 不因单次对照添加强制委派、搜索或额外监控；不改写任何旧归档。候选通过后再验证、审查并根据结果决定是否保留。

## Change Log
- 2026-11-11：用户指出整体结论和剩余问题未充分说明；重开 v3，保留 v2 已交付改动并补齐阶段性证据。
- 2026-11-11 reopen — retrieved achieved task `2026-11-10-token-review` for new work; re-approval required before core changes
- 2026-11-11：重启整体流程调查，建立 v2 方案草稿，委派与文档重复保持关联专项；批准前不实施代码或规则改动。
- 2026-11-11 reopen — retrieved achieved task `2026-11-10-token-review` for new work; re-approval required before core changes
- 2026-11-10：按用户要求开始只读历史会话和当前架构的脱敏取证；尚未制定或批准实现方案。

## Follow-ups
- 子 Agent 对照及搜索倾向继续由 TF-20260919-90797c 跟踪，文档历史正文重复继续由 TF-20261011-e27329 跟踪，不声称调查结论覆盖所有会话。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- 关注流程总成本、可观测性及质量，不预先假设删减有益；与待办 TF-20260919-90797c（子 Agent 成本实测）及 TF-20261011-e27329（文档历史重复）有范围重叠，实施前需确认分工；另参考已完成的 T-20260908-006。
- 2026-11-10 用户补充：新增 Todo 时应与现有条目比较，对可合并的重复或高度重叠事项进行合并，避免重复流程和不必要的 Token 消耗；调查现有比较规则的实际效果，保留不同需求和决策，避免误合并。
