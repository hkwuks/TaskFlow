# 任务关系与会话延续：sessions.md 触发条件、重叠上报、父子任务协调
> Task version: v1
> Status: completed

## Goal

补上 TaskFlow 里三条属于「任务与任务之间、会话与会话之间」的规则，让它们可判定、可记录、可检查：

1. `sessions.md` 从「觉得有用就用」变成有条件、有义务，不再是 `SessionStart` hook 的偶然副产品；
2. 重复、重叠或冲突的任务不再静默并存，Agent 主动报给用户；
3. 父子任务共享需求时，变更往哪个方向传播、谁改哪一份文档。

三条都是**规则与记录的缺口**，不是缺一个机制：现有 hook、命令、目录结构都够用，缺的是「什么条件下必须做什么」这句话，以及能发现漏做的检查。

## Background / Confirmed Facts

### B1·需求来源

用户于 2026-10-08 提出 8 条改进需求（Source 统一记为 `user request 2026-10-08, 8-item doc/tooling batch`），本任务收编其中三条：`TF-20261008-b1f5e0`（sessions.md）、`TF-20261008-ee2c27`（重复/冲突上报）、`TF-20261008-73facd`（父子任务协调）。三条被合并为一个任务，是因为它们都改 `SKILL.md` 的相邻小节、且都要动 `artifacts.md` 的同一批模板——拆开会在同一批文件上反复撞车（用户已确认按 4 个任务落地，而非 8 个）。

需求澄清通过一轮结构化提问完成（三个依赖有序的问题，各自带推荐项），用户的选择记录在 Open Questions 与 Requirements 中。

### B2·sessions.md 的现状：有定义、无触发条件

- 定义位置齐全：`SKILL.md:41`（条件性产物）、`SKILL.md:289`（`## Sessions and collaboration`）、`artifacts.md:182-207`（Session outline 模板）、`artifacts.md:146`（routing 表）、`README.md:74`。
- 文件名统一为**复数** `sessions.md`；全仓库不存在单数 `session.md`。
- 唯一的代码写入者是 `hooks/session-record`（`hooks/session-record:99`），由 `hooks/session-start:165-167` 以 best-effort 方式调用。它只写 hook 自有字段（session id、agent、availability、时间戳、目录、Task version/phase）。
- `Last completed` / `Next step` / `Notes` 归 Agent（`SKILL.md:289`、`artifacts.md:184`、`runtime.md:99`），而**没有任何条件要求 Agent 去写**。`SKILL.md:289` 的原话是「Use `sessions.md` only when cross-session or cross-agent continuation is useful」——一个不可判定的条件。
- 实测后果：88 个任务目录中只有 2 个存在 `sessions.md`，且两份都只有 hook 写的块，`Last completed` / `Next step` / `Notes` 三个字段**从未出现过**。即：文件由 hook 意外产生，Agent 的交接义务从未落地。

结论：缺的不是定义，是**触发条件**与**归属**。用户明确选择「给出触发条件」，而非把它降级为纯 hook 产物。

### B3·重复/冲突：只有字节级去重

- `hooks/task:220-228`：`intake` 在写入前拒绝 **goal 字符串完全相同**的条目（`die("duplicate Todo goal")`），并按 goal 的 `cksum` 派生 ID 以避免并行分支撞车。
- 只此一层。近义、包含、范围重叠、目标冲突一律不报。
- `SKILL.md:54` 的「Deduplicate imported items by source plus external identifier」只覆盖**同一批导入**内的同源条目，不处理跨时间的语义重复。
- `SKILL.md:60-71` 的 Existing-task-first selection 表比较的是**新请求 vs 已有任务**，没有 Todo 与 Todo 之间的比较；`:71` 只在「与已有任务混合」时要求呈现拆分并等用户选择。
- 语义判断只有 Agent 能做，hook 只能做词面近似。用户在澄清中确认采用**两层**：hook 给候选、Agent 下判断并对用户负责。

### B4·父子任务：有创建规则，没有协调规则

- 创建边界已有：`SKILL.md:69`（有独立可发布产物 + 独立验收标准 → 建 related task）、`:71`（混合时呈现拆分、等用户选择）、`:100`（属于已完成任务的请求 → 取回并升版）。
- 关联表达只有单向的三种：`artifacts.md:156-163` 的 `## Related Tasks` 提供 `Depends on` / `Blocks` / `Related`，**没有父子方向**。
- 变更分类已有且可复用：`SKILL.md:97-98` 的 User-change trigger（work revision vs Task-version material change）。
- 缺口：子任务发现的事实动摇了父任务**已批准**的需求时没有规则——谁改父 PRD、什么时候改、父任务发生 material change 时子任务要不要重新批准，全部未定义。用户确认此条指的是**父子任务之间**这一层（不是任务内 PRD↔Spec，也不是仓库文档→任务 PRD）。

### B5·可用的机械手段（决定改法）

- hook 只解析固定名单的标题与字段（`artifacts.md:23-27`）；PRD 的其他标题属正文，可自由改动。`hooks/task:665-679` 的 `promote` 只负责写出骨架。
- 概念类校验表在 `hooks/task:509`（`concept_class_re`，7 个类），`hooks/task:879-917` 的 `unaided` 是唯一的校验点；`hooks/task:936-999` 的 `approve` 按 stage 对账发布记录。
- 该表就是 `SKILL.md:140-148` 的 phase 表本身，两处必须同批改。
- `hooks/smoke-test` 对 `SKILL.md` / `artifacts.md` / `CONTRIBUTING.md` / `RELEASE.md` 有大量字句 pin（`:1296-1339`、`:1405-1414`），是"文档是否漂移"的既有防线；本任务的规则句子应加入同一批 pin。

## Requirements

### R1 — sessions.md 的触发条件

`SKILL.md` 的 `## Sessions and collaboration` 必须给出**可判定的**触发条件，取代「when useful」：当会话结束时任务尚未 `completed`，Agent 必须在本任务 `sessions.md` 的当前条目写入 `Next step`（与 `Last completed`，当其非空时）。hook 不可用时，按 `artifacts.md` 的 Session outline 自行创建该文件。

触发条件取「任务未完成即离场」而不是「任务跨会话」，因为前者是可判定的（phase 是不是 `completed`），后者要预知未来。

### R2 — 主动上报重复/重叠/冲突

- **R2a（hook 层，候选而非判决）**：`hooks/task intake` 在写入前，把与新闻 goal 有词面重叠的**现存 live 条目**作为候选报出（ID + 标题，最多 3 条，无判决词）。候选走 **stderr**，`stdout` 保持逐字不变（仍只有 `intake OK: <id>`），因为 `hooks/smoke-test:2041` 以 `awk '{ print $NF }'` 取 stdout 末字段当 ID——任何多出来的 stdout 行都会让提取到错值。字节级相同的 goal 仍按现状拒绝。词面重叠是启发式，只用于提示，不得据此拒绝或自动合并。
- **R2b（Agent 层，义务）**：`SKILL.md` 在 triage 处写明：记录 Todo 之后、创建或选择任务之前，必须对照**现存 live 条目与活跃任务**检查重复/重叠/冲突，覆盖两种关系——新请求 vs 已有任务，以及 Todo vs Todo。发现重复或冲突时必须先报给用户并取得选择，不得静默并存、不得自行合并。

### R3 — 父子任务的需求协调

- **R3a**：`artifacts.md` 的 `## Related Tasks` 增加父子方向（`Parent:` / `Children:`），与既有 `Depends on` / `Blocks` / `Related` 并存。
- **R3b**：`SKILL.md` 写明三条协调规则：
  1. 每个任务的 PRD 只对自己的 scope 权威；子任务**不修改父任务文档**，只把发现记入自己的 `plan.md` 并向用户呈现；
  2. 父任务的已批准需求需要变更时，走它自己的 User-change trigger（`SKILL.md:97-98` 的分类），在**父任务自己的工作树**里、由父任务的所有者进行——与子任务是否在同批工作无关；
  3. 子任务在自己的 `plan.md` 记录它**规划时所依据的父任务版本**；父任务发生 Task-version material change 后，子任务必须重新记录新版本才能继续；仅当该变更触及子任务自己的已批准契约时，子任务才需要重新批准。

## Acceptance Criteria

- **A1**：`SKILL.md` 的 `## Sessions and collaboration` 含一条命名条件的触发句（任务结束时未 `completed` → 必须写 `Next step`），不再出现「only when cross-session or cross-agent continuation is useful」这一不可判定条件；该触发句被 `hooks/smoke-test` pin 住。
- **A2**：存在词面重叠的 live 条目时，`hooks/task intake` 在 **stderr** 报出不超过 3 条候选（含 ID 与标题）；**`stdout` 逐字不变**（仍只有 `intake OK: <id>` 与 base-tree 提示），成功退出码仍为 0；字节级重复 goal 仍以原方式失败。`hooks/smoke-test:2041` 的 `awk '{ print $NF }'` 提取结果在新旧行为下一致。
- **A3**：`SKILL.md` 的 triage 处写明 R2b 的义务句，明确覆盖 Todo-vs-Todo 与 request-vs-task 两种关系，并要求在创建第二个任务前先取得用户选择。
- **A4**：`artifacts.md` 的 `## Related Tasks` 含 `Parent:` / `Children:`，`SKILL.md` 含 R3b 的三条规则（子任务不改父文档、父变更走父自己的 trigger、子任务记录父版本并在父升版后重记）。
- **A5**：`hooks/task approve` 对本任务每个 stage 的对账通过（`[PRD]` / `[Spec]` / `[Plan]` 各有一条合格记录）；`SKILL.md` phase 表与 `hooks/task:509` 的概念类表仍一致（若本任务未改表，则两者逐字不变）。
- **A6**：`bash hooks/smoke-test`、`quick_validate.py skills/taskflow`、`bash hooks/release-check .`、`git diff --check` 全部通过；本任务不新增 hook，不改变 `hooks/task` 其余子命令的既有行为。

## In Scope

- `SKILL.md`：`## Sessions and collaboration`、`### Todo-first intake` / `### Existing-task-first selection`、`### Todo → PRD → Spec → Plan` 相关段落。
- `skills/taskflow/references/artifacts.md`：`## Related Tasks`、`## Session outline`（指向触发条件而非重述）。
- `hooks/task`：`intake` 的重叠候选提示（R2a）；仅在为通过 A5 所必需时才触碰概念类表。
- `hooks/smoke-test`：新增 pin（A1、A3、A4 的规则句）与 `intake` 提示的断言。
- 本任务的三个核心文档。

## Out of Scope

- **`TF-20261008-84a0ce`**：已提交到主目录的工作如何搬进 worktree（第 4 个任务）。
- **`TF-20261008-a4454d` / `TF-20261008-4d37b2`**：reference 同步与文档版本处理（Task C）。
- **`TF-20261008-ca2fce`**：loop / 长期任务兼容（Task D）。
- **`TF-20261008-5b5635`**：phase 表增加头脑风暴概念类（Task B；本任务若动该表，只为保持 B5 所述的一致性，不引入新类）。
- 重写既有文档、追溯修订 `TaskFlowDocs/achieved/`、`sessions.md` 的字段增删、把 `sessions.md` 降级为纯 hook 产物。
- 任何形式的自动语义判重、自动合并任务。
- `TF-20260919-6b4e21`（todo.md 墓碑压缩）：其 Next action 写明「用户研究后再定、不要动」。

## Risks / Deferred Items

- **R1 风险**：词面重叠是启发式，误报会让用户忽略提示。缓解：不设判决词、限 3 条、只在达到下限时打印；语义判断留给 Agent。
- **R2 风险**：R3b 的第 3 条（子任务记录父版本）**无法机械强制**——跨两个任务目录的检查超出既有 hook 的边界。本次以规则句 + smoke pin 落地，检查能力记为 follow-up。
- **R3 风险**：给 `intake` 增加 stdout 会否破坏解析其输出的调用方（含 `smoke-test` 自身）。Step 1 必须先确认；若会破坏，改用带固定前缀的单行。
- **Deferred**：把「重叠/冲突必须上报」做成可检查的断言（需要读 Todo 与任务目录的交叉检查），留待机制成本被证明值得时。

## Open Questions

无阻塞性未决问题。已由用户裁定的三项：

1. **sessions.md**：给触发条件，**不**降级为 hook 产物。
2. **重复/冲突**：分两层（hook 给候选、Agent 下判断并对用户负责）。
3. **父子协调**：指父子任务之间这一层。

## Version History

- v1 — 规划中。
