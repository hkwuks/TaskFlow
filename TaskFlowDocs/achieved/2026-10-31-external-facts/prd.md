# 外部事实：先判断，再取证
> Task version: v2
> Status: completed

## Goal

让 TaskFlow 在「这件事的答案在仓库外」时真的去看，而不是把判断记录成 `no` 就过去。v1 造了一个字段，它记录判断但不改变行为 —— 一个不搜索的模型写一句 `no` 加个像样的理由就能通过。v2 要解决的是产生那句 `no` 的倾向本身。

## Background / Confirmed Facts

**用户 2026-11-01 重述问题**：「不是说只要求 prd 必须包含外部事实，而是说在当前的 taskflow 框架下模型会倾向于不搜索解决问题，因此可能需要一些机制来矫正这个问题。」

**倾向是被框架塑造的，这一点可以指到具体位置。** 每一处都在把注意力向内拉：

| 位置 | 现状 |
|---|---|
| `skills/taskflow/SKILL.md:54` | `inspect` 枚举八项 —— repository、`index.md`、project rules、active and achieved tasks、tests、configuration、Git state、uncommitted changes —— **没有一项指向仓库外** |
| `hooks/summarize-state` | 会话开场注入的全是内部结论与内部路径 |
| `hooks/prompt-reminder` | 每回合只说「当前任务是什么、这条指令算不算变更」，不说「这件事的答案在哪」 |
| `skills/taskflow/SKILL.md:172` | `searching external sources` 只挂在 Phase 2 的能力列，而 `SKILL.md:44`/`219` 写明 `reference/` 是 optional —— 因果被写成「因为要写笔记所以去搜」 |
| `hooks/capability-evidence:48-50` | 只认 `Skill`/`Agent|Task`/`mcp__*`；`WebSearch`/`WebFetch` **完全不可见** |

结果是「答案在仓库外」这个判断**没有任何一个时刻被触发**。加字段不会触发它。

**但能力是有的，而且有实证。** `achieved/2026-09-08-runtime-hooks/plan.md` 的 `## Reference Pointers` 写着：

```
- Claude Code hooks reference (docs.anthropic.com) and Codex Hooks guide
  (learn.chatgpt.com/docs/hooks, plus openai/codex repo schemas) — verified
  event names, config locations, and output contract.
```

那次模型**确实去查了**。缺的不是能力，是让这件事可检查、可追溯：没有 URL，没有日期，`learn.chatgpt.com/docs/hooks` 今天还成不成立无从判断。

**测量（2026-10-31，94 个 achieved 任务）**：`## Reference Pointers` 共 **382 条 bullet，含 URL 的 0 条**；有 `reference/` 的 **3/94**；整个归档第三方 URL 共 **4 条**，全在一个任务里；其余 71 条全是 `github.com/hkwuks/TaskFlow` 自身。

**这个数字不能证明 TaskFlow 抑制了搜索** —— 本仓库多数任务是内在工作，本来就不该引用外部。它证明的是另一件事：**这个框架里没有任何地方能区分「查过了」和「没想到要查」**。v2 修的是这个可区分性。

**宿主事实（2026-11-01 查 Claude Code hooks 官方文档，非记忆）**：`PostToolUse` 的匹配取值为「Matches on tool name, same values as PreToolUse」，而 `PreToolUse` 的匹配范围明确列出 `WebFetch` 与 `WebSearch`。`WebSearch` 的 `tool_input` 字段为 `query`、`allowed_domains`、`blocked_domains`。因此接上这两个工具是可行的，不是假设。

## Requirements

- **R1 — 三个停顿点。** 在三个收敛动作之前各问一次「这一条依赖仓库外的事实吗」：Phase 1 收敛成 `prd.md` 之前、Phase 3 决定 Spec 之前、Plan 定稿之前。判断在 Phase 1 定，但**问题要在它可能被推翻的每一处重问** —— 一个 Phase 1 答 `no` 的任务，在 Phase 3 才可能第一次意识到自己在定义一个新的接口契约。
- **R2 — 检索变成可见事件，且与能力完全隔离。** 新增一个记录器把 `WebSearch`/`WebFetch` 记成外部证据。**它与 `taskflow/evidence` 是两套存储、两条消费路径**：`capability-gate` 与 `task approve` 的 stage 对账继续只认 `Skill`/`Agent`/`mcp__*`，检索记录**永远不能**释放 stage、**永远不能**满足 `[PRD]`/`[Plan]`/`[Test]`（R12 不变）。隔离的判据是可检查的：一个只有检索记录的任务，`approve` 必须仍因缺 stage 被拒。
- **R3 — `## External Facts` 从「记录判断」升级为「记录判断 + 证据」。** `yes` 的每条 `- Source:` 必须能在外部证据存储里找到对应的检索记录（同一任务版本、URL 域名或 query 匹配）。没有记录 = 拒绝。
- **R4 — 无外部证据则拦。** 一个任务声明 `yes` 却拿不出检索记录时 `approve` 拒绝（R3 的推论）。一个任务声明 `no` 时不拦，但 `no` 的理由现在要面对一个问题：「你能指出这个结论在仓库内的哪一处被判定吗」—— 答不出的 `no` 就是 v1 的那个橡皮图章。
- **R5 — 不引入联网检查。** 记录器只读宿主已经投递的事件，不发起任何网络请求。可达性仍然不校验（与 `$schema` 断言同一理由）。
- **R6 — 不改变 Phase 2 的 optional 性质。** `reference/` 仍是可选产物；`## External Facts` 与外部证据记录都不是「必须写笔记」。

## Acceptance Criteria

- **A1** `WebSearch` 的 `PostToolUse` 事件被记为一条外部证据，记录含 `query` 与该事件的 cwd 所指向的任务。
- **A2** `WebFetch` 的同一路径可记，`tool_input.url` 被保留。
- **A3 — 隔离的反向证明。** 一个任务只有外部证据记录、没有任何能力调用记录时，`approve` 仍以「stage [PRD] was never released」拒绝。这条**必须**失败，才能证明检索记录不能顶替能力记录。
- **A4** 一个任务声明 `yes`，写了 `- Source:`，但外部证据存储里没有对应记录 → `approve` 拒绝并说出缺的是哪一条。
- **A5** 同上，但有对应记录 → `approve` 通过。
- **A6** 声明 `no` 且理由指向仓库内某处 → `approve` 通过；理由为空或只有一句泛泛而谈 → 拒绝。
- **A7** `SKILL.md` 的三处停顿点各有一句可执行的问句，且 `SKILL.md:54` 的 `inspect` 八项**不变**（加一项会让判断伪装成检查动作）。
- **A8** 全部断言在 `hooks/smoke-test` 里，每条都能被变异打红。

## External Facts

- Depends on external facts: yes
- Source: https://docs.claude.com/en/docs/claude-code/hooks
- What it settled: R2 的前提 —— `PostToolUse` 是否为 `WebSearch`/`WebFetch` 投递事件，以及 `WebSearch.tool_input` 有哪些字段。查前只知道 R12 把这两个工具排除在能力谓词外，不知道它们是否可被观察到；若不可观察，R2 整条（把检索变成可见事件）就没有落点，整个 v2 要改成纯停顿点方案。文档明写「`PostToolUse` … Matches on tool name, same values as `PreToolUse`」，而 `PreToolUse` 的匹配范围明确列出 `WebFetch`、`WebSearch`，并给出 `query`/`allowed_domains`/`blocked_domains`。R2 因此成立，方案不变。

## In Scope

- `hooks/external-evidence` — 新 hook，`PostToolUse` on `WebSearch|WebFetch`，写 `<absolute-git-dir>/taskflow/external`。
- `hooks/hooks.json` — 新增一条 `PostToolUse` 接线。
- `hooks/task` — `approve` 的 R3/R4 校验；`promote` 骨架措辞更新。
- `hooks/smoke-test` — A1–A8。
- `skills/taskflow/SKILL.md` — 三处停顿点；Phase 1 `prd.md` 段落更新。
- `skills/taskflow/references/artifacts.md` — 字段清单与存储说明。
- `skills/taskflow/references/runtime.md` — 事件表新增一行。
- `CHANGELOG.md`。

## Out of Scope

- **不改 `capability-evidence` 的谓词。** 它是 R12 的执行者，v2 不碰它。外部证据走另一个 hook、另一个文件、另一条消费路径 —— 隔离靠的是不同的代码，不是同一个 case 语句里的另一个分支。
- **不改 `SKILL.md:54` 的 `inspect` 八项枚举。** 理由同 v1。
- **不做对照实验。** 仍然无法从数据单独分离「TaskFlow 造成的」与「这类任务本就不需要」。
- **不检查 URL 可达性。**
- **不回填 94 个已归档任务。**
- **不为其他宿主的 `WebSearch` 接线。** Codex/Trae/CodeBuddy 的 web 工具名不同且未测；本版本只接 Claude Code，`runtime.md` 记录这个限制。

## Risks / Deferred Items

- **「无外部证据则拦」只在声明 `yes` 时触发。** 一个铁了心答 `no` 的模型仍然过得去 —— 这是真实的剩余漏洞。R4 的第二半（理由必须指向仓库内的判定处）只是把橡皮图章的代价抬高一点，不是消除它。**能彻底消除它的办法是要求每个任务都产出外部证据，而那会把大多数内部任务变成造假**。本任务选择接受这个漏洞并写明，而不是用一个会让所有任务说谎的规则去堵它。
- **外部证据存储会无限增长。** 每个 `WebSearch` 一行，一个长任务可能有几十行。与 `taskflow/evidence` 同样的问题，同样先不处理。
- **`PostToolUse` 对 `WebSearch` 的实际投递形态尚未在真实会话中测量** —— 依据是官方文档的匹配说明，不是一次观测。落地后第一次真实使用时应当核对（写进 Follow-ups）。

## Open Questions

- 无。三个岔口（矫正点、强度、#108 去留）已于 2026-11-01 由用户裁定。
