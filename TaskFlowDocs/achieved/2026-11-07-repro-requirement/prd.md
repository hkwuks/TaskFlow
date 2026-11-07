# 缺陷调查必须先被点名，才能被选择

> Task version: v1
> Status: completed

## Goal

当一个请求是「修掉已报告的错误」时，TaskFlow 必须先把「查清根因」这件事请进来，再写需求；现在它把修 bug 和做新功能走同一条路，于是模型只看见手边最顺的动作（加标记、改文档），把症状处的工作当成了任务本身。

## Background / Confirmed Facts

**缺陷（已读代码确认，修复前）。** TaskFlow 用一张「phase → 概念类别」表决定每个阶段该去找什么能力，`skills/taskflow/SKILL.md:169-177`。七个阶段对应八个类别，全部列在 `hooks/task:767` 的正则里：

```
requirements elicitation|literature and evidence|architecture and design|work breakdown|incremental implementation|testing strategy|documentation and decision|divergent exploration
```

**这八个类别里没有一个是「查根因」。** 而 `SKILL.md:12` 明确把 `bug fix` 列为 TaskFlow 适用的请求类型。它进来之后与 `feature` 走完全相同的路径：intake → promote → Phase 1 写 PRD。

**后果。** `systematic-debugging` 这类能力在流程里**没有一个可以被点名要它出现的类别**：没有任何规则要求它出现，`task unaided <stage> --considered` 也点不出它（`hooks/task:1250` 用上面那条正则校验 `--considered`，不在表内直接拒绝）。模型只能用手边就有的东西，而手边最顺的是改文档——这不是模型偷懒，是可用能力的集合里本来就没有「调查」。

**这不是把别的方法抄进来的问题。** `SKILL.md:163` 已经写明 TaskFlow 是任务生命周期层、不是专家能力层，它只负责选择并调用能力。本次修的正是它自己那一层：**让「调查」成为一个可被点名、可被记录的类别**，至于调查怎么做，属于被调用的能力。

**判据来自既有机制。** 修复完全复用现成的 stage/capability 证据链（`taskflow/evidence` + `taskflow/released` + `capability-gate` + `approve` 对账），不新增存储、不新增验证方法。

## Requirements

**R1 — 显式声明任务种类。** `hooks/task intake` 与 `hooks/task promote` 增加 `--kind defect|capability|internal`。
- `intake` 省略时默认 `capability`（多数请求是新增，且 inbox 阶段允许便宜）。
- `promote` **必须**显式给出；缺省即拒绝，且拒绝信息给出三个取值。
- `kind` 写入 Todo 条目的 `- Kind:` 字段，并在 `promote` 时写入 `prd.md` 的 `## Task Kind`。

**R2 — 缺陷类任务的 PRD 阶段必须点名调查能力。** `approve` 对 `kind=defect` 的任务额外要求：`## Skills / Tools Used` 里 `[PRD]` 那一行**不得是 `Unaided`**，且其能力名必须来自调查类词汇（`diagnos`/`debug`/`root cause`/`investigat`）。非缺陷类不受此约束。

**R3 — 类别表新增调查类。** `SKILL.md` 的 phase 表在 Phase 1 一行补上「缺陷调查」类别；`hooks/task:767` 的正则同步加入 `defect investigation|root cause`，否则 R2 要求的能力名无处可写。

**R4 — 兜底不劣化。** 环境中确实没有调查类能力时，缺陷类任务仍然可以推进，但必须走 `task unaided PRD --considered 'root cause investigation'`——即"我确认没有可用的调查能力"是一个**显式记录的决定**，而不是默认发生的事。这是用户已指出的 b48e56 方向，本次只做最小接线，不提前实现 b48e56。

**R5 — 既有任务不受影响。** 没有 `- Kind:` 字段的历史 Todo 条目与已归档任务不做推断、不重写；`approve` 只对显式声明为 `defect` 的任务施加 R2。

## Acceptance Criteria

**A1** `bash hooks/task promote <id> <task> small` 缺 `--kind` 时以非零退出，信息含 `defect|capability|internal` 三个取值；给出 `--kind` 后成功。

**A2** 给出的 `--kind` 不在三值内时拒绝，信息点名该非法值。

**A3** `intake` 省略 `--kind` 时写入 `- Kind: capability`；给出 `--kind defect` 时写入 `- Kind: defect`。

**A4** `promote --kind defect` 产出的 `prd.md` 含 `## Task Kind` 节，且该节含 `- Kind: defect`；`--kind capability` 同样产出该节。

**A5** `kind=defect` + `[PRD] Unaided — …; considered: requirements elicitation` 时，`approve` 拒绝，信息说明缺陷类任务的 PRD 阶段必须点名调查类能力。

**A6** `kind=defect` + `[PRD] Unaided — …; considered: root cause investigation` 时，`approve` 通过（R4 的显式兜底）。

**A7** `kind=capability` + `[PRD] Unaided — …; considered: requirements elicitation` 时，`approve` 通过（R5：非缺陷类不受 R2 约束）。

**A8** `bash hooks/task unaided PRD --considered 'root cause investigation'` 被接受（正则已同步）；`--considered 'defect investigation'` 同样被接受。

**A9** 无 `- Kind:` 字段的既有 Todo 条目在 `task get` 下仍可读出，字段集合不变。

**A10** `bash hooks/smoke-test` 全量通过；新增断言各自可被至少一条变异打红。

## External Facts

- Depends on external facts: no
- Why not: 全部结论都落在本仓库的既有机制上——类别表在 `skills/taskflow/SKILL.md:169-177`，正则与校验在 `hooks/task:767` 与 `hooks/task:1250`，证据存储与对账在 `hooks/capability-gate` 与 `hooks/task` 的 `approve` 分支。没有一条结论依赖本仓库之外的版本、规范或他人行为。

## In Scope

- `hooks/task`：`intake`/`promote` 的参数与写入；`concept_class_re`；`approve` 的缺陷类分支；`promote` 的 PRD 骨架。
- `skills/taskflow/SKILL.md`：Phase 1 的类别表与分流说明。
- `skills/taskflow/references/artifacts.md`：PRD 轮廓新增 `## Task Kind`。
- `hooks/smoke-test`：新增断言与既有夹具的 `--kind` 补齐。
- `TaskFlowDocs/todo.md`：本任务条目。

## Out of Scope

- **不实现任何调查方法。** 不写「怎么找根因」、不规定必须先重现、不要求 red-green。那是被调用的能力该做的事。
- **不新增 stage。** 调查折进 PRD 阶段（用户已定），阶段集合仍是 `{PRD, Spec, Plan, Test}`。
- **不实现 b48e56**（无能力时的回退语义）。本次只让「确认无可用能力」成为一条可记录的显式声明。
- 不为已归档任务补 `- Kind:`。
- 不改 `hooks/archive` 的关闭条目字段白名单（`- Kind:` 会随条目一起被裁剪，这正是期望行为）。

## Risks / Deferred Items

**风险：`kind` 判错。** 把缺陷类误标为 `capability` 会让 R2 静默失效。缓解：`promote` 强制显式给出，而不是默认值；默认值只在 `intake` 阶段存在，且 `promote` 会把它写进 PRD 供人复核。

**风险：词汇正则太松。** A6 要求 `root cause investigation` 被接受，而模型可能用一个含 `investigat` 但实际无关的能力名糊过去。接受此风险：门只保证「类别被点名」，不保证「能力合适」——后者与 `## Plan Review` 的诚实边界同类，写入 artifacts.md 而不是装作能测。

**延后：** 非缺陷类任务是否也该有 anti-goal（本次未做，见 Not Doing）。

## Open Questions

无阻塞项。
