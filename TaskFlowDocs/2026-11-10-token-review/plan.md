# Plan — 审视 TaskFlow 流程中的不合理环节和 Token 开销
> Task version: v2
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers

## Related Tasks
- TF-20261110-84d1a9；与 TF-20260919-90797c 子 Agent 成本和 TF-20261011-e27329 文档历史重复相关，保留独立 Todo，不未经决策合并。

## Skills / Tools Used
- [PRD] Unaided — none applied; considered: requirements elicitation and framing.
- [Spec] Unaided — none applied; considered: architecture and design specification.
- [Plan] Unaided — none applied; considered: work breakdown and task decomposition.
- [Test] Unaided — none applied; considered: testing strategy.

## Preconditions
- 历史会话只提取与流程和 Token 有关的脱敏证据。
- 本版本工作区为 `.worktrees/2026-11-11-token-review`，分支为 `feature/2026-11-10-token-review`；保留两个专项 Todo 的独立验收边界。

## Plan Review

- Verdict: sound
- Coverage: 覆盖整体流程、委派与外部搜索倾向对照、文档重复；专项 Todo 保留独立验收。
- Verifiability: 保持同题、相同基线与评价标准；主线和子 Agent 用量分别报告，无法取得子 Agent 用量时明确不可测，不计算总节约。
- Layer ownership: 从用户授权的会话提取脱敏证据，再修改插件自身拥有的规则或脚本。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-11 14:47 +0800
- Approved version: v2
- Approved scope: PRD / Spec / Plan

## Steps

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
  - [ ] 执行针对性测试及 CI，并明确剩余验证。
- Acceptance: 不损害必要质量和追溯，实测证据支持改进。
- Verification: 针对性测试、适用的跨平台 CI 和复核。
- Rollback: 回退任务变更。
- Status: in_progress

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

## 候选改进（待用户确认）
- 在 `skills/taskflow/SKILL.md` 的 Todo 重叠规则中明确：如果用户在当前会话已经清楚决定相关条目的关系或处理方式，报告该决策并沿用；只有决策尚不明确时才再次询问。保留发现重叠、保留独立需求和不擅自合并的要求。现有文字对所有真实重叠一律要求再次取得选择，可能重复用户已作出的决定；不将本次宿主工具冲突误归因于此规则。
  - 拟替换语义：`If the user has already clearly decided how the overlap is handled, state and follow that decision; otherwise ask the user before planning.` 其余不静默合并、不覆盖独立需求的规则保留。
- 删除状态定义中与归档章节重复的事务细节，保留状态含义和指向完整归档事务的引用；归档章节、完整性校验及失败处理保持原样。涉及 `skills/taskflow/SKILL.md` 一处，现有发布和语法检查仍适用；这只是几百字节级的静态精简，不宣称实测 Token 或时间节省。
- 不因单次对照添加强制委派、搜索或额外监控；不改写任何旧归档。候选通过后再验证、审查并根据结果决定是否保留。

## Change Log
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
