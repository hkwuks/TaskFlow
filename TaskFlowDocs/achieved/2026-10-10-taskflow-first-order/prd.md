# 进入顺序：先 TaskFlow，再阶段，然后才是能力

> Task version: v1
> Status: completed

## Goal

把「进入顺序」变成 Skill 里一条可读的约束：**当适用闸门判定这份工作要走 TaskFlow 时，工作在任何一件被做之前先登记，而每一项能力都在某个阶段之内被选择与调用，而不是在阶段存在之前。**

它修的是「入口」层的一类失败：两个本来分开写的规则——适用闸门（什么时候该建任务）与阶段到能力的匹配（每个阶段该找什么能力）——之间没有写明的先后，于是下面三件事都会发生，而且都不是罕见情形：

1. **先调研、后建档**：调研在记录存在之前就发生了，于是记录写出来时没有阶段可以归属它；读者无法从记录里看出那段调研从何而来。
2. **工作已经做出结论才有人问「这份工作该不该登记」**：此时登记变成事后补办的手续。
3. **阶段在没有能力的情况下进入**：有用的能力最容易在**做那个阶段的时候**被注意到，所以一个没有能力进入的阶段往往也不会再获得能力。

这三条与 `TF-20261009-cc463b` 目标里记的三个失败模式一一对应，区别只在措辞：本条把「没有写明的先后」变成「写明的顺序」，并且只做这一点。

同时并入该条的第四个失败模式——**未登记的工作在场时入口完全静默**——但只补它剩下的一半：`TaskFlowDocs/` 存在却从未登记过任何东西的仓库没有信号。

## Background / Confirmed Facts

### B1·顺序确实没写

`SKILL.md:10`（Applicability gate）与 `SKILL.md:~147`（phase 表前的 capability 段）是两段独立的规则。前者说「请求要求修改仓库时自动适用」，后者说「写阶段产物前先看可用能力」。**没有任何一句说谁先谁后**，也没有一句把「先登记」放到「先调研」之前。

后果不是理论推演，本条自己的来源就是实例：`TF-20261009-cc463b` 的 Source 记的是「user request 2026-10-09, found while writing the trae-host PRD」——调研与 PRD 写作发生在建档之前，于是 `2026-10-09-trae-host` 的两份文档里没有可供归属的阶段记录。

### B2·phase 表的措辞不是本条范围

`TF-20261008-5b5635`（已 done，1.1.4 的 `divergent exploration` 即出自它）已经处理过「没有能力广告阶段名」这一类；本条不重新处理 phase 表的措辞，只加顺序。

### B3·入账那一半（「已发生的调研可归属当前阶段」）不做

工作已经做过的调用要能补记到当前阶段，需要先定下 `capability-evidence`（按事件 `cwd` 定位证据库）与 `capability-gate`（按目标文件路径定位）两个锚点的统一语义。这正是 `TF-20261001-efbc51` 的目标，且它已吸收 `TF-20261008-84a0ce`。

在锚点未定之前改 `capability-evidence`，只能修一半：我实测过锚点错配的后果——`capability-evidence` 把 `invoke|` 写进了主检出的 git dir，而 gate 去查任务工作树的 git dir，于是 gate 末尾的 `summary` 分支报「the most recent invocation was already spent by an earlier document」，把阻塞归因到「上一个文档花掉了它」，而实际原因是**根本没记到这里**。先做顺序，入账紧随 efbc51。

### B4·第四个失败模式的剩余一半

2026-10-10 落地的 `summarize-state` 入口提示（PR #73）覆盖了「无 `TaskFlowDocs/`」「分支 slug 不匹配任何任务目录」两种静默。**没有覆盖**的是：

- `TaskFlowDocs/` 存在、但 `todo.md` 不存在、也没有任何活跃任务——此时任务列表为空、inbox 为空、分支报告在 base 分支或不含 slug 的分支名上也不触发，四类信号同时缺席。

这个状态在每个新仓库**第一次使用 TaskFlow 的首个会话**里是常态（`repository-docs/index.md` 已由 SessionStart 建好，`todo.md` 还没建）。

### B5·`UserPromptSubmit` 这条路仍然关闭

`achieved/2026-09-10-audit-hook-opportunities/reference/hook-audit.md:81` 已否决，`references/runtime.md` 亦明写写入命令永不绑它。所以入口信号只能落在 `summarize-state`（SessionStart 的唯一输出），不能加 prompt hook。

### B6·既有约束

- 无解释器不变量：`summarize-state` 只用 POSIX sh + awk；`smoke-test` 的 no-interpreter 一节在只 link 了 `awk`/`git` 等的 PATH 上钉住它。
- `gate` 的 deny 文案是对 agent 可见的唯一提示处，既有断言钉住它必须含 `[<STAGE>]`、概念类别、`task unaided <STAGE> --considered`。
- 既有断言用 grep 钉住 SKILL.md 的若干原句子句（`smoke-test:1353-1362` 区段），所以改动必须避开那些子句。

## Requirements

- **R1**　在 `SKILL.md` 的 Applicability gate 段内写明进入顺序：先 TaskFlow、再阶段、然后能力；并说明它**不是**第二道闸门（适用判定错了仍可纠正；早建的任务比无法复原来源的工作更便宜改范围），也**不是**把每个请求都变成任务。
- **R2**　同一段说明「先」的具体含义：Todo 记录在实现之前存在；阶段的能力在该阶段开始时选择——这正是它能被记成「该阶段的」而不是「一次无归属调用」的原因。
- **R3**　`hooks/capability-gate` 的 deny 文案加入同一句顺序，使「文档说的」与「被拒绝时收到的」是同一套规则。
- **R4**　`hooks/summarize-state` 增加入口形态：`TaskFlowDocs` 存在但从未登记任何条目时，输出适用边界（复用既有措辞），且**不创建任何文件**。
- **R5**　R4 的触发条件以「什么都没登记过」为准：`todo.md` 存在即不触发（intake 至少跑过一次，义务已被看见）；`repository-docs/` 单独存在**不**算登记过（SessionStart 自己会创建它），而 `achieved/` 或任何其他目录的存在算登记过。
- **R6**　新增代码与断言仍落在 POSIX `awk`/`sed` + bash 3.2 地板内，且不新增解释器。

## Acceptance Criteria

- **A1**　`smoke-test` 新增断言钉住 R1 的三句：顺序句、顺序句的标题行、以及「能力在阶段内选择」那一句。删掉其中任一句即红（变异验证）。
- **A2**　同一定言钉住 R3：gate 的 deny 文案含该顺序句；把文案改回旧措辞即红。
- **A3**　`smoke-test` 断言 R4：`TaskFlowDocs/` + `repository-docs/` 而无 `todo.md`、无任务目录时，输出含 `TaskFlowDocs/todo.md` 与状态句（`nothing recorded yet`），且 `TaskFlowDocs/` 内不新增文件。
- **A4**　断言 R5 的三个方向：写入 `todo.md` 后该行消失；只有 `achieved/` 内容时不出现该行。
- **A5**　`bash hooks/smoke-test` 全量通过；no-interpreter 一节仍通过。
- **A6**　`references/runtime.md` 对 `summarize-state` 的描述与 R4 一致（旧文写「Prints nothing when no TaskFlowDocs exists」，已不成立）。

## In Scope

- `skills/taskflow/SKILL.md`（Applicability gate 段内的顺序声明）
- `hooks/capability-gate`（deny 文案）
- `hooks/summarize-state`（入口形态 + 注释）
- `hooks/smoke-test`（两组断言）
- `skills/taskflow/references/runtime.md`（描述对齐）
- 本任务的 `prd.md` / `plan.md` / Todo 条目

## Out of Scope

- 「已发生的调研可归属当前阶段」的入账打通——`TF-20261001-efbc51`。
- phase 表的措辞——`TF-20261008-5b5635` 已 done。
- `capability-evidence` 的锚点语义——efbc51。
- 把 gate 从硬 deny 降为 approve 时对账——用户 2026-10-09 裁定的候选 (c)，本次未选。
- `UserPromptSubmit` 钩子——B5。

## Risks / Deferred Items

- **顺序声明是 prose，不是机制。** 没有任何 hook 会拒绝「先调研后建档」。可检查的部分只有它有没被写下来（A1）。这是用户裁定的强度（「声明 + smoke 钉住」）。
- **第五个失败模式仍然不可上报。** 在 base 检出上尚未建分支就开始改仓库、或分支名本就不含 slug（如 `user/foo`）时，五类信号同时为空。与第四个同源，但触发条件落在分支命名上。已记入 Todo Notes，本条不修。
- **入口形态仍有余量。** 建了 `TaskFlowDocs/`、也建了 `todo.md`、但从未写入任何条目时，R4 不触发（按 R5 的判定 `todo.md` 即「见过义务」）。这是有意的边界，不是遗漏。
- **`repository-docs` 的排除是必要的。** 若把它算作「登记过」，R4 在本仓库永远不触发——`hooks/repository-docs-context` 在每次 SessionStart 都确保该目录与 `index.md` 存在。

## Open Questions

无。三个设计决定已由用户 2026-10-10 裁定：范围只钉顺序（入账留给 efbc51）、强度为声明 + smoke 钉住、第四个失败模式的剩余一半并入本条。

## Version History

- v1 — planning。
