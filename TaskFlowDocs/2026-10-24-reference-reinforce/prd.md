# 参考资料增强：任务执行期把部分资料带回注意力

> Task version: v1
> Status: checking

## Goal

让一类资料在任务执行期间反复回到 Agent 的视野，而不只是在 SessionStart 读一次。

## Background / Confirmed Facts

用户原话（2026-10-23）：参考资料增强：有一些资料是需要任务进行中时刻提醒参考的。

用户 2026-10-24 追问的三个问题，就是本任务真正的难点：谁来标记、怎么标记、怎么判定哪些重要、哪些不重要或本身是错的。

测得的现状：

- `hooks/repository-docs-context` 派生路由清单，`hooks/session-start:179` 是它唯一的调用方。路由因此只进会话一次，之后不再出现。
- `hooks/prompt-reminder` 已经每轮 prompt 触发，输出固定三行（在飞任务行 + 两行分类问题），是唯一存在的每轮载体。它的头部注释把「阶段门是唯一限流，没有 marker 文件、没有计数」写成了设计理由。
- `TaskFlowDocs/repository-docs/index.md` 的 Phases 列（design / code / commit / pr / release / all）表达的是「哪个阶段读」，没有「任务中反复读」的概念。
- `skills/taskflow/references/artifacts.md` 与 `hooks/task:797` 的 Plan 脚手架都已有 `## Reference Pointers` 段，所以 Plan 本来就能点名资料，只是没有任何东西把它带回视野。
- 度量（2026-10-24）：84 份 plan.md 中 75 份的 `## Reference Pointers` 有内容，平均 362 字节、最多 1305 字节。内容是「我读过这些」，不是「我还要再读」。
- `hooks/summarize-state` 实测 54ms，`hooks/repository-docs-context` 实测 226ms。每轮只读一个 plan.md 的代价可忽略。
- `hooks/repository-docs-context:223` 已经有一种表达不确定性的状态：`needs-review`，来自 `*GOVERNANCE*.md` 候选行，意思是「这是文件不是规则，未分类，别当真」。
- 同一文件的 `:318` 已经是「存在性单独成一个状态」的先例：`Status: missing` 的仓库文档会印成 `- Missing catalog entries: ...`，而不是当作不存在而消失。资料消失这件事在这个仓库里已经有一个正确的表达手法，本任务照抄它。

用户 2026-10-24 追问的第二个问题：开发过程中发现 reference 里的资料是错的、甚至文件没了，有没有对应机制。答案分三种情况，机制不同：

| 情况 | 承载机制 | 本任务要补的部分 |
|---|---|---|
| 文件被删 / 改名 | 钩子每轮查存在性 | 现在是静默丢弃，改为印 `MISSING:`，让消失可见（R3） |
| 资料内容与实现冲突 | `SKILL.md` 的 User-change trigger：修正指向是 work revision（改文档 + Change Log 一行，版本不变）；若推翻已批准需求则是 Task-version material change | 无新增机制；本功能让资料持续出现在视野里，就是让「它还对不对」持续可被核对 |
| 仓库文档本身是错的 | 独立 deliverable，另立任务 | 无，不在本任务范围 |

## Requirements

- R1. Plan 的 `## Reference Pointers` 中，以 `- [Reinforce] \`<repo-relative path>\` — <reason>` 形式书写的条目，表达「这条资料在任务执行期需要被反复带回」。
- R2. `hooks/prompt-reminder` 在它已经输出时，把满足 R1 的路径额外印成一行 `- Reinforce while this task runs: a, b, c`，位置在现有任务行之后、分类问题之前。
- R3. 一条 `[Reinforce]` 行要进入输出，必须满足：带 `- [Reinforce] ` 行首、带 `— <reason>` 且理由非空、路径是仓库内相对路径（不是 URL、不由 `../` 或绝对路径开头）。缺任一条静默跳过。
- R4. 满足 R3 的条目再按存在性分两类印在同一条 Reinforce 行里：文件存在的正常列出，文件不存在的带 `MISSING:` 前缀。**资料消失不得静默** —— 静默消失正是这条要防的失效。
- R5. 一条满足 R3 的条目都没有时，不输出 Reinforce 行，现有三行逐字节不变。
- R6. `hooks/README.md`、`skills/taskflow/references/runtime.md`、`skills/taskflow/references/artifacts.md` 说明这条能力的位置、判据、由谁标记、以及「钩子不判对错」的边界。

## Acceptance Criteria

- A1. 一个 active 且 `in_progress` 的任务，Plan 含两条合格 `[Reinforce]` 条目，输出包含 `- Reinforce while this task runs: <a>, <b>`，位于任务行之后、分类问题之前。
- A2. 删掉其中一条的理由后，输出只剩另一条；再删掉最后一条的 `[Reinforce]` 标记后，输出不含该行，且现有三行逐字节不变。
- A3. 一条 `[Reinforce]` 指向仓库中不存在的路径时，该路径在 Reinforce 行里以 `MISSING:` 前缀出现，且不影响其他条目的正常列出。
- A4. 全部条目都不存在时，该行仍然输出（只含 `MISSING:` 项）—— 全部消失不等于没有声明。
- A5. 一条 `[Reinforce]` 指向 URL 或 `../` 开头时既不列出也不以 `MISSING:` 出现（无法验证的东西不归入任何一类）。
- A6. 任务处于 `planning` / `ready`、或存在两个 active 任务、或 cwd 在仓库外时，输出与改动前逐字节相同。
- A7. `bash hooks/smoke-test` 通过，A1–A6 的断言在其中。
- A8. `bash hooks/release-check .` 通过。

## In Scope

- `hooks/prompt-reminder`（读 Reference Pointers 并多印一行）
- `hooks/smoke-test`（A1–A6 的断言）
- `hooks/README.md`、`skills/taskflow/references/runtime.md`、`skills/taskflow/references/artifacts.md`
- `CHANGELOG.md`
- `TaskFlowDocs/todo.md` 的本条目

## Out of Scope

- **不判断资料内容是否正确。** 钩子只判断「是否需要每轮回到视野」。对错的处理：路径不存在现在会以 `MISSING:` 显示（R7），而不是消失；`needs-review` 已表示「未分类，别当真」；**发现某条资料与实现冲突时，删掉或改写那行标记属于 work revision** —— 按 `SKILL.md` 的 User-change trigger，改文档 + Change Log 一行，版本不变；若它推翻的是已批准需求，那才是 Task-version material change。这条路径已经存在，本任务不新建机制，只让诱发它的信息持续可见。
- **不做自动判定。** 不根据文件类型、大小、修改频率或 prompt 措辞推断哪些资料该 Reinforce。判据是三条可当场回答的性质（跨 Step、违反静默、代码无从提醒），写 Plan 的人填，审批的人看。
- **不改仓库文档本身。** 发现 `CONTRIBUTING.md` 之类的仓库文档写错，是独立 deliverable，另立任务；本任务既不检查也不修正它们的内容。
- **不改 `repository-docs/index.md` 加列。** index 是受跟踪的仓库级记录；塞一个 per-task 的「重读」标记等于把任务事实写进共享文件。
- **不做计数或降频。** 与 `prompt-reminder` 现有的「阶段门是唯一限流」一致；长会话的第二、三条指令才是漂移发生处，按条数截断正好漏掉它们。
- **不给已归档的 Plan 回填标记。** 历史文档不改写。
- **不改变现有三行的内容与顺序。**

## Risks / Deferred Items

- **标记通胀。** Agent 见资料就标则每轮输出退化成文件清单。缓解：理由必填（无理由不输出），且清单出现在审批屏上。这是有意的软约束 —— 没有能判「重要性」的硬判据。
- **写标记的人会漂移。** Plan 审批是唯一复核点，本任务不引入第二个。
- **已度量的上限**：Plan 的 Reference Pointers 平均 362 字节，整段读取代价可忽略；若单份 Plan 涨到数十 KB，应改为只解析 `[Reinforce]` 行而非整段。
- **延迟项**：外部资料（URL、其他仓库）若需要支持，必须先有可验证的存在性来源；目前没有。

## Open Questions

无阻塞问题。
