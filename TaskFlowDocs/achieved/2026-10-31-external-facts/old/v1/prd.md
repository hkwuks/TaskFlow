# 外部事实：先判断，再取证
> Task version: v1
> Status: in_progress

## Goal

让每个任务在 `prd.md` 里回答一次「这个任务的结论是否依赖仓库外的事实」，并在答案为「是」时真的去检索、把来源记下来。答案不是靠自觉写散文，而是 `task approve` 读得出、能拒绝的一种形态。

## Background / Confirmed Facts

**为什么现在做。** 2026-10-11 用户观察到「用了 TaskFlow 之后 Agent 似乎变得不喜欢做网络搜索」，要求先查是不是真的。当时立的 Todo `TF-20260919-90797c` 只覆盖测量，后又分出 `TF-20261027-e8c6dc`。2026-10-31 用户把它重新界定为：**「在判断需要外部信息、调研、外部信息确认等需求的时候，调用搜索」** —— 要的不是「多搜」，而是「该搜的时候真的搜」。测量因此从目的降为背景。

**三处机制，2026-10-31 逐条复核仍成立。** 原 Todo 引的是旧行号，位置已经漂移，结论没变：

1. `skills/taskflow/SKILL.md:54` 的 `inspect` 枚举八项 —— repository、`index.md`、project rules、active and achieved tasks、tests、configuration、Git state、uncommitted changes —— **全部在仓库内或 Agent 自己的状态里，没有一项指向仓库外**。
2. 「取外部事实」不是一个动作，只是 Phase 2 的一个产物描述。`skills/taskflow/SKILL.md:172` 把 `searching external sources` 挂在 Phase 2 的能力列，而 `SKILL.md:44` 和 `SKILL.md:219` 都写明 `reference/` 是 **optional**。于是模型里的因果关系是「因为要写 reference 笔记，所以去搜」，而不是「因为答案在仓库外，所以去搜」—— 不写笔记就不触发。
3. `hooks/capability-evidence:48-50` 只认 `Skill` / `Agent|Task` / `mcp__*`，`WebSearch` / `WebFetch` 不被计入任何证据。这是 2026-09-27 的 R12 有意为之（`achieved/2026-09-27-capability-pre-write-gate/prd.md:61`），目的是不让内置工具满足能力门禁。后果是：**检索在 TaskFlow 里既不拦也不奖。**

**测量数据，2026-10-31 在 94 个 achieved 任务上重跑：**

| 指标 | 原 Todo（2026-10-27，91 任务） | 今天（94 任务） |
|---|---|---|
| `## Reference Pointers` 的 bullet 总数 | 365 | **382** |
| 其中含 URL 的 | 0 | **0** |
| 整个任务目录含 `reference/` 的 | 3 / 91 | **3 / 94** |
| 整个归档里第三方主机 URL 总数 | 4 | **4**，且全部集中在同一个任务（`2026-09-10-audit-hook-opportunities`） |
| 其余 URL | 71 条 | **71 条，全是 `github.com/hkwuks/TaskFlow` 自身** |

**这个数字不能用来证明 TaskFlow 抑制了搜索。** 本仓库的绝大多数任务是内在工作：改自己的 bash hook、改自己的 `SKILL.md`、修自己的 smoke 套件。这类任务本来就应当 0 个外部 URL。原 Todo 自己写了这一句，但它的 Next action 跳过了它直接给方案。**所以本任务不承诺「外部检索次数会上升」，也不做对照实验** —— 用户 2026-10-31 裁定：接受这个混淆，只写明。

**能检查的只能是「问题被问了并记录」，不是「行为被改变了」。** 这是本任务验收标准的形状，也是它和「加一句散文」的根本区别：散文无法被检查，字段可以。

## Requirements

- **R1 — 一份文档承担这个判断，且它必须是 PRD。** 判断属于需求阶段（决定要不要查），不属于计划阶段（决定怎么查）。因此字段只加在 `prd.md`。
- **R2 — 字段是一个顶层小节 `## External Facts`，内容是下面两种形态之一**，第一行由 `hooks/task approve` 逐字匹配：
  - `- Depends on external facts: no` —— 下一行必须是 `- Why not: <一句话>`。
  - `- Depends on external facts: yes` —— 后面必须跟至少一条 `- Source: <URL>`，每条带 `- What it settled: <这句话改变了哪个结论>`。
- **R3 — 答案为 `yes` 时，`Source` 必须是绝对 `http` / `https` URL。** 不是仓库内路径、不是「我读了很多代码」、不是 `mcp__` 工具名。判断标准是这句话**能否在仓库里被证伪** —— 不能，才是外部事实。`http` 合法（允许内网文档站），`ftp` / `file` / `git@` 不合法。
- **R4 — `approve` 在写 `## Approval` 之前校验 R2/R3，失败即拒绝并给出可执行的修法。** 与现有 `Skills / Tools Used` 的校验同一位置、同一形态：先于任何写入，一次只报一条具体原因。
- **R5 — 骨架与文档同步。** `hooks/task promote` 写出的 PRD 骨架、`skills/taskflow/references/artifacts.md` 的 PRD outline 与「hook 匹配的字段清单」三处都要出现该小节，且字段名逐字一致。
- **R6 — 不引入门禁以外的行为变化。** 不改 `capability-evidence` 的谓词（R12 的理由仍成立），不新增 hook，不联网，不改 `hooks/completion-gate`。
- **R7 — 已归档的 94 个任务不回填，且 `approve` 不在 `achieved/` 上运行。** 与 `done`-only 规则那次同处理。

## Acceptance Criteria

- **A1** 一个 `prd.md` 含 `## External Facts` + `- Depends on external facts: no` + `- Why not: …` 的任务可以 `approve` 通过。
- **A2** 同一文档把答案改成 `yes` 却不写任何 `- Source:` 行时，`approve` 退出非 0 并点名「yes 需要至少一条 Source」。
- **A3** 答案是 `yes` 且 `- Source:` 的值是 `hooks/task` 这类仓库内路径时被拒绝，消息说明「不是 URL」。
- **A4** `- Source:` 写成 `ftp://` 或 `git@…` 时被拒绝；写成 `http://` 时通过。
- **A5** 整个小节缺失时 `approve` 拒绝，消息同时给出两种合法写法中的一行，让人照抄即可。
- **A6** 上述四条由 `hooks/smoke-test` 在既有 `task approve` 夹具上覆盖，且每条都有一个能被变异打红的具名断言。
- **A7** `skills/taskflow/references/artifacts.md` 的「Section headings a hook matches by name」清单里出现 `## External Facts`，`## Items` 之外的位置不变。
- **A8** 一个 `prd.md` 只有 `## External Facts` 标题、正文为空时被拒绝（与 `Skills / Tools Used` 现有「missing or empty」同形），而不是当成 `no`。

## External Facts

- Depends on external facts: no
- Why not: 这条规则本身就是判断标准 —— 「结论能否被仓库外的事实证伪」。本任务的每一条要求、每一个验收标准都由仓库内的既有实现（`hooks/task`、`hooks/smoke-test`、`artifacts.md`、`SKILL.md`）判定，无一处依赖外部规范、版本或第三方文档。三项能力调用均为本机可执行，不涉及远端。

## In Scope

- `hooks/task` 的 `approve`：新增一段校验，位置在 `cap_skills` 检查之后、任何 `## Approval` 写入之前。
- `hooks/task` 的 `promote`：PRD 骨架增加该小节。
- `hooks/smoke-test`：在既有 approve 夹具上新增用例。
- `skills/taskflow/references/artifacts.md`：PRD outline 与字段清单。
- `skills/taskflow/SKILL.md`：在 Phase 1 说明该字段的含义。

## Out of Scope

- **不改 `SKILL.md:54` 的 `inspect` 八项枚举。** 加第九项「外部事实」会让一个判断问题伪装成一个检查动作，而这八项是「打开仓库就能看」的清单，性质不同。机制 (1) 的修补方式是让 `## External Facts` 每个任务都必须回答，而不是往枚举里塞一条。
- **不改 `capability-evidence` 的谓词。** R12 的理由（内置工具不得满足能力门禁）仍然成立，让 `WebSearch` 进入证据池会把门禁变成一个「搜一下就能过」的东西。
- **不做对照实验，不承诺外部检索频率上升。** 见 Background 的混淆说明。
- **不检查 URL 可达性。** 与 `hooks/release-check` 的 `$schema` 断言同一理由：联网检查会在 DNS 抖动时变红，却仍在远端搬家时是错的。
- **不改 Phase 2 的可选性。** `reference/` 仍然 optional；它记录的是研究成果，`## External Facts` 记录的是判断与出处，两者不合并。

## Risks / Deferred Items

- **`no` 分支可能被当成橡皮图章。** 一句 `- Why not: 这是仓库内部重构` 就能过。这是本任务接受的代价：字段保证「这个问题必须被显式回答」，不保证答案诚实 —— 而散文连前者都不保证。若将来发现 `no` 的比例接近 100% 且理由雷同，再考虑加反向抽查。
- **`TF-20260919-90797c` 的对照测量仍然悬空。** 它测的是「委派 subagent 是否省 token」，与外部检索是两条独立线索，2026-10-31 用户裁定不合并。

## Open Questions

- 无。三个实现层面的岔口（产出形态、落点、对照）已于 2026-10-31 由用户裁定。
