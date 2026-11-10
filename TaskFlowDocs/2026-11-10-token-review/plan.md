# Plan — 审视 TaskFlow 流程中的不合理环节和 Token 开销
> Task version: v1
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

## Plan Review

- Verdict: sound
- Coverage: 中文 Todo 候选缺口有可复现修复和验证；历史样本、子 Agent 与文档重复继续调查，缺少证据时不强行重构。
- Verifiability: token_count 为多次模型请求的累计，不直接代表任务成本；缓存单独统计。
- Layer ownership: 从用户授权的会话提取脱敏证据，再修改插件自身拥有的规则或脚本。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-10 16:51 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 历史样本与流程检查

- Goal: 比较真实会话和当前流程，发现可验证、值得简化的环节。
- Dependencies: 用户授权脱敏查看。
- Files: 当前任务记录与必要的脱敏证据。
- Implementation checklist:
  - [ ] 对照同一会话不同任务及其他适用历史会话，分析耗时、调用和可用 token 记录。
  - [ ] 比较 Todo 去重、子 Agent 和文档历史重复的范围。
- Acceptance: 形成证据、限制与具体候选，不把关联推为因果。
- Verification: 按会话、时间与任务边界核对差值及来源，保护敏感数据。
- Rollback: 更正记录，不改用户历史会话。
- Status: pending

### Step 2 — 审核并实施选定改进
- Goal: 在 Todo intake 的现有候选比较中识别常用中文的相邻双字，不自动合并条目。
- Dependencies: 第一阶段取证完成、具体方案与用户批准。
- Files: `hooks/task` 和候选比较相关回归测试。
- Implementation checklist:
  - [x] 实现不依赖新运行时的 UTF-8 常用汉字相邻双字候选；保留既有英文及提示上限。
  - [ ] 验证中文改写、无关目标、混合语言、重复词和正常英文，明确扩展字集限制。
- Acceptance: 复现的中文近似目标提示候选，不误合并，也不牺牲关键验证或用户决策；无可比数据时不声称节省百分比。
- Verification: 在隔离 Todo 夹具验证命中、误报及跨平台 CI。
- Rollback: 回退本任务改动。
- Status: in_progress

## Checkpoints

## Verification / Review
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

## Change Log
- 2026-11-10：按用户要求开始只读历史会话和当前架构的脱敏取证；尚未制定或批准实现方案。

## Follow-ups

## Version History

- v1 — planning.
