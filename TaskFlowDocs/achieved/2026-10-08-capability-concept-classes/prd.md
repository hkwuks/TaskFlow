# 让「发散与想法精炼」成为 phase 表里的独立概念类
> Task version: v1
> Status: completed

## Goal

让**发散与想法精炼**（ideation）在 TaskFlow 的阶段能力表里成为一个可被匹配、可被记录的概念类，从而不再被 phase 1 顺带跳过。

用户对 `TF-20261008-5b5635` 的描述与澄清结果（本轮问答，用户选择方案 A）：

> 之前增加了编写文档的其他工具引导，但是没有引导头脑风暴类的工具，导致头脑风暴类的工具被跳过，无法调用。

具体做法是**方案 A**：拆条列项——phase 1 的类名变为 `requirements elicitation and framing; divergent exploration`，并在 `hooks/task` 的概念类注册表里新增 `divergent exploration` 这个备选。这样 `## Skills / Tools Used` 的记录能**区分**「跳过发散直接写需求」与「考虑了发散」两种情况，而不是两者记录成同一个类名、事后无法判断。

## Background / Confirmed Facts

### B1·需求来源

`TF-20261008-5b5635`，Source 为 `user request 2026-10-08, 8-item doc/tooling batch`。本任务是该批 4 个任务中的 **Task B**（A 已完成并合并，见 `TaskFlowDocs/achieved/2026-10-08-task-open-and-continuation/`）。

### B2·当前状态：类名存在，但把「发散」混在「写需求文档」里

- phase 表在 `SKILL.md:146-154`，phase 1 一行为：
  `| 1. Define — PRD | prd.md | requirements elicitation and framing | interviewing the user, refining a vague idea into testable requirements, writing a requirements document |`
- 该行的「Consider a capability for」列把 `refining a vague idea into testable requirements` 与 `writing a requirements document` 并列。整格读起来指向**产出文档**，`interviewing` / `refining` 只是其中的附注，没有独立的概念类去匹配 ideation 能力。
- 因此按表走的结果就是**直接写 PRD**：ideation 类能力没有任何一栏"认领"它。
- 历史证据：项目曾真的调用过 `agent-skills:idea-refine`、`superpowers:brainstorming`（见 `achieved/2026-09-23-capability-invoke-gate/plan.md:22` 与 `old/v1/spec.md`），但这些用例没有回流成引导，只留在归档里。
- 全仓库 `skills/taskflow/` 内 `brainstorm` / `ideat` / `idea-refine` / `interview-me` **零命中**。

### B3·概念类是封闭词表，两个校验点 + 一份文档副本

| 位置 | 角色 |
| --- | --- |
| `SKILL.md:146-154` | phase 表，人读的文档副本 |
| `hooks/task:606` `concept_class_re` | **唯一**校验点：`unaided --considered` 用**子串**匹配它 |
| `hooks/capability-gate:28-35` `stage_class()` | 每个 stage 被拦时，把对应类名写进拒绝提示 |

`hooks/smoke-test:1447-1458` 校验 phase 表的行存在、"自变量列不带产品名"，但**两份副本之间没有对账断言**（`concept_class_re` 在 smoke 里只在 `unaided` 的行为断言中被间接覆盖）。**本任务必须自己保证三处同批一致**，并补一条对账断言（见 R4）。

### B4·硬约束：能力中立性

`achieved/2026-09-23-capability-invoke-gate/old/v1/spec.md:50` 立下不变量：校验绝不 grep `agent-skills`、`idea-refine`、MCP 工具名。`hooks/smoke-test:1458` 把它实现为"概念表不得出现产品名"。所以本次**只能加概念类，不能在任何地方点名具体 skill**——`brainstorming` 这类词也不能进表（用户已确认走概念类路线）。

### B5·既有缺陷（本任务不修，仅记录）

`concept_class_re` 是**子串**匹配，所以 `hooks/task unaided PRD --considered "work"` 会通过（匹配到 `work breakdown`）。这是改动前就存在的宽松校验，与本次新增类无关；修它会改变既有的接受集合，属独立缺陷，记为 follow-up。

## Requirements

### R1 — phase 表新增独立概念类

`SKILL.md` 的 phase 1 行的概念类列拆条列项为 `requirements elicitation and framing; divergent exploration`；「Consider a capability for」列须**增加**一项指ideation（让模糊想法变清晰、展开多个方向、在对象/边界未定时先发散），并保留现有三项。表头行与其余 6 行**逐字不变**。

### R2 — 注册表同批一致

`hooks/task:606` 的 `concept_class_re` 增加 `divergent exploration` 备选。加在**末尾**，并保持它与 phase 表在「类名词根一致、可选后缀」这一既有约定下成立（`requirements elicitation` / `requirements elicitation and framing` 即此约定）。

### R3 — PRD 阶段的触发条件可判定

`SKILL.md` 的 `### 1. Define — PRD` 补一条：当目标或方案尚未确定、或存在多个可行方向时，PRD 必须先发散再收敛，不得直接落笔写需求。措辞必须可判定，且**不作为强制**——能力可用性、适配与"是否要做"仍由 Agent 判断（`SKILL.md:144` 的"类只说什么可找，从不说什么必须用"保持成立）。

### R4 — 三处一致性与记录能力由断言锁住

`hooks/smoke-test` 增加断言：

- phase 表行含 `divergent exploration`；
- `unaided` **接受** `divergent exploration` 与 `requirements elicitation and framing`（既有约定不破）；
- 新类与前 6 类一样**不引入产品名**；
- 「三处副本必须同批改」这件事本身，由**对账断言**落地：把 phase 表的概念类列与 `concept_class_re` 抽出比对，任一新增类只出现在其中一处即失败。

对账断言是本任务**唯一有回归面**的新增（解析一份文档表格、无先例），其局限见 Risks。

## Acceptance Criteria

- **A1**：`SKILL.md:146-154` 的表头行与 phase 2–7 行与改动前**逐字相同**；phase 1 行的概念类列为 `requirements elicitation and framing; divergent exploration`，且「Consider a capability for」列含 ideation 项。
- **A2**：`hooks/task` 的 `concept_class_re` 含 `divergent exploration`；`unaided PRD --considered "divergent exploration"` 退出 0，`--considered "随便什么"` 仍退出 2。
- **A3**：`SKILL.md` 的 `### 1. Define — PRD` 含一条可判定的发散前置条件，且明确不构成强制；`SKILL.md:144` 与 `SKILL.md:156` 的既有权衡句未被改动。
- **A4**：`hooks/smoke-test` 新增断言：phase 1 行含新类、两个类名都被 `unaided` 接受、概念表无产品名，以及**对账断言**（phase 表列出的类与 `concept_class_re` 的备选集合一致）。
- **A5**：`hooks/capability-gate` 的 `stage_class()` 文本**不变**（每 stage 的显示类名不因本次改动而变）；拒绝提示因此不含 `divergent exploration`，该选择在 Spec 判定中记录。
- **A6**：`bash hooks/smoke-test`、`release-check`、`git diff --check`、`quick_validate.py skills/taskflow`（用 conda `torch` 环境的解释器）全部通过；CI 三 host 矩阵在推送后全绿。

## In Scope

- `skills/taskflow/SKILL.md`：phase 表的 phase 1 行、`### 1. Define — PRD` 段。
- `hooks/task`：`concept_class_re` 一行。
- `hooks/smoke-test`：phase 表与类注册表的一致性/对账断言。
- 本任务的核心文档。

## Out of Scope

- `hooks/capability-gate` 的 `stage_class()` 文本（A5 明示不变）。
- 任何具体 skill 名、MCP 工具名（B4 的中立性不变量）。
- 修 `concept_class_re` 的子串宽松校验（B5，独立缺陷，记 follow-up）。
- 同批其余任务：`TF-20261008-a4454d` + `TF-20261008-4d37b2`（Task C）、`TF-20261008-ca2fce`（Task D）、`TF-20261008-84a0ce`（worktree 迁移）。
- 重写既有文档、追溯修订 `TaskFlowDocs/achieved/`。

## Risks / Deferred Items

- **R1 风险（对账断言的脆弱性）**：从 markdown 表格里抽出概念类列，会受列内分隔符与措辞影响；断言的措辞写紧会误报、写松会失效。缓解：断言只比对「两边的类名集合」，不比对整行；若实现中发现解析不稳，退回为「逐类名双向 grep 存在性」这一更钝但可靠的版本（两个方向都查，能捕获单向新增）。
- **R2 风险（spec 判定的边界）**：R4 的对账断言使本任务的实际改动面从一个数据点扩到「文档解析 + 一致性校验」。已在 `### 3. Design — Spec decision` 判定中记录：任意大小的任务、只要不涉跨层契约，仍按 small 走，但 Spec 判定必须显式做（见 Plan 的 `No spec required` 行与 Spec Pointers）。
- **R3 风险（叠加而非替换）**：新旧类名并存于同一行，`unaided` 的接受集合扩大，任何把「类名 → 唯一 stage」当前提的代码都会受影响。已核对：唯一读取类是 `concept_class_re`（子串匹配）与 `capability-gate:stage_class()`（自有一份文本，未改），无第三处依赖。
- **Deferred**：`concept_class_re` 子串匹配过宽（B5），修它需评估既有 `unaided` 记录的接受集合，另立任务。
- **Deferred**：phase 表与 `concept_class_re` 的长期单一来源（目前是手工同步的两份副本）；本次只加对账断言，不做重构。

## Open Questions

无阻塞性未决问题。用户已裁定：**方案 A**——新增独立概念类，记录可区分，而非并入 phase 1 现有类。

## Version History

- v1 — 规划中。
