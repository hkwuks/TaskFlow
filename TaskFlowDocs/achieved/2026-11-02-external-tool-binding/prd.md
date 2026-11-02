# 外部证据绑定任意工具，而不是两个产品名
> Task version: v1
> Status: completed

## Goal

让「这个任务是否去过仓库外」这个问题对**任何**工具都成立，而不是只对 `WebSearch`/`WebFetch` 两个产品名成立；同时把判据的代价降到「每批工具调用一次」，而不是「每次调用一次」。顺带落两条仓库规则：release 标题/tag 格式，以及「已声明的宿主尽量都支持」。

## Background / Confirmed Facts

**用户 2026-11-02 的判断。** 「外部事实工具的绑定只绑定了官方的 websearch 和 webfetch……其他所有可以搜索的工具也应该支持这个绑定」「这个实现感觉偏离了支持任意工具的预期」。随后追加两条仓库规则。

**用户对方案的裁定（同一天，三问三答）：**
1. 拆分：合成一个任务（不再另开规则小任务）。
2. 判据：URL 判据是对的（含 `Bash`），但**「没有必要每次调用都跑 hook」**——「我的目的只是为了判断是否执行过搜索对吧？那代码有点大」。
3. 宿主：按能接的宿主全接。

**代码现状（本仓库，2026-11-02 读）。** 外部证据的谓词是产品清单，位置有两处：
- `hooks/hooks.json:61` — `PostToolUse` 的 matcher 是 `WebSearch|WebFetch`；
- `hooks/external-evidence:69-73` — `case "$tool_name"` 只有这两个分支，注释自称「Two tool names, both built in」。

**这与仓库自己立的原则冲突。** `achieved/2026-09-27-capability-pre-write-gate/prd.md:52`（R3）：「谓词是工具类别，不是产品清单」；`hooks/capability-evidence:45-46` 把同一句话写成注释。R12（同 PRD:61）只决定「内建搜索不能算进能力谓词」，从未要求外部取证按名字绑。v2 的 Out of Scope（`achieved/2026-10-31-external-facts/prd.md:85`）只排除了**其他宿主**的 web 工具，同宿主上的 MCP/Skill/CLI 检索根本没被讨论过——所以这不是一个被辩护过的取舍，是隔离论证顺手带出来的范围收缩。

**实测缺陷（本会话，2026-11-02，就是这次调研）。** 本任务的三次外部查证：
- 一次 `WebFetch`（`https://docs.claude.com/en/docs/claude-code/hooks`）被 context-mode 的 `PreToolUse` hook 拦截并重定向到 `mcp__plugin_context-mode_context-mode__ctx_fetch_and_index`，**`WebFetch` 事件从未发生**；
- 另一次 `ctx_fetch_and_index` 与七次 `ctx_search` 全部走 `mcp__*`；
- 结果：该 worktree 的 `taskflow/evidence` 有 8 行 `invoke|mcp__…`，而 `taskflow/external` **不存在**。

即：一次真实的、有明确 Source URL 的外部查证，在现行判据下**零记录**。这不只是「少支持几个工具」，是判据可以被一个 hook 的转发整条绕过。

**宿主事实（2026-11-02 读官方文档，非记忆）。**
- Claude Code `PostToolBatch`：文档写明「runs once after every tool call in a batch has resolved」「There is no matcher for this event」，输入为 `tool_calls[]`，每项含 `tool_name`、`tool_input`、`tool_response`。本机 `claude --version` = 2.1.309。
- Claude Code `PostToolUse`：输入含 `tool_input` 与 `tool_response`（「the result it returned」）。
- Codex hooks（`developers.openai.com/codex/hooks.md`）：`PostToolUse` 的 `tool_name` 可为 `Bash`、`apply_patch` 或 `mcp__fs__read` 这类 MCP 名；`tool_input` 与 `tool_response` 均按工具而异。未见到与 `PostToolBatch` 对应的事件。
- CodeBuddy / Trae：已在 `runtime.md` 记录为使用 `PostToolUse`（`Skill|Agent|Task`、`mcp__.*` 已接线）；dsh 的 `tool_name` 是小写且桥接不翻译，未接任何工具事件。

**覆盖矩阵（回答「不用 MCP 怎么办」）。** 判据是事件里有没有 URL，所以下表每一行都走同一条代码路径；「事件」列才是决定性的。

| 检索路径 | 事件 | URL 在 | 无 MCP 时 |
|---|---|---|---|
| 内建 `WebSearch` | `PostToolBatch` / `PostToolUse` | `tool_response` | ✓ |
| 内建 `WebFetch` | 同上 | `tool_input.url` + 响应 | ✓ |
| MCP 检索/抓取（exa、tavily） | 同上 | 响应 | —（有 MCP 时额外覆盖）|
| `Bash` 跑 `dg` / `tvly` / `sxng` / `curl` | 同上 | 命令 + `stdout` | ✓ |
| Skill 内部再起外部命令 | 内层 `Bash` 事件 | 内层响应 | ✓ |
| 子代理做的检索 | 子代理自己的工具事件（cwd 指向同一 worktree） | 响应 | ✓ |
| `Read` 含 URL 的仓库文件 | 同上 | 响应 | ✓（误报，见 Risks）|
| 用户自己查完给出 URL | **无工具事件** | — | 只有 R10 的声明通道 |
| 宿主未装 hook / dsh | **无工具事件** | — | 只有 R10 的声明通道 |

**两条新规则的现状（本仓库，已核对）。**
- Release：tag 全部是 `vX.Y.Z`（`v1.0.3`…`v1.1.10`）；**annotated tag 的 subject 不一致**——`v1.0.x` 是 `TaskFlow v1.0.9`，`v1.1.0`–`v1.1.10` 是 `TaskFlow 1.1.10`；GitHub Release 标题同样分裂。`RELEASE.md:121` 只写「an annotated tag such as `vX.Y.Z`」，第 135 行只写「create the GitHub Release from the tag with the approved notes」——**格式从未被写下来**，所以偏移没有被拦住。
- 宿主覆盖：`CONTRIBUTING.md:98-118` 已有「a hook change lands on every host the repository declares, or it says why not」，并区分 not wired / not supported。但它的主语是 **hook**，不是「任何能力」。用户要的是后者。

## Requirements

- **R1 — 判据与工具名无关。** 记录器**不读 `tool_name`**，不做产品清单，也不做类别清单。判据是事件里是否出现绝对 `http(s)` URL。任何工具——现有 MCP server、Skill 经 `Bash` 调起的 CLI、将来新增的检索工具——自动覆盖，无需再加一行代码。**不需要任何 MCP**：内建 `WebSearch`/`WebFetch` 与 `Bash` 跑的 `dg`/`tvly`/`sxng`/`curl` 同样命中。
- **R1a — 输入与输出两侧都扫。** 大输出会被宿主中段截断，而 `curl https://…` 的命令行永远完整；只扫 `tool_response` 会在截断时丢掉唯一完整的那份。判据是「`tool_input` 或 `tool_response` 里出现 URL」。
- **R1b — 排除 loopback。** `dg` 背后是 `localhost:8888` 的 SearXNG；把 `http://localhost:…` 记成外部来源是错的。排除 `localhost`、`127.0.0.1`、`[::1]`、`0.0.0.0`，**不排除**私网地址（v1 已裁定内网文档站算合法来源）。
- **R10 — 没有工具事件时留一条声明通道。** 用户自己查完给了 URL、hook 未安装、dsh 这类接不上工具事件的宿主，都产生不了记录。新增 `bash hooks/task external <url> --why "<它改变了什么>"`，写入 `declared|<url>`。`approve` 一并接受，但**在输出里把「实测」与「声明」分开列出**——声明不是伪造，但它也不是观测，两者不能读成同一件事。信任模型与 `unaided` 相同：显式、可见、可审计。
- **R2 — 每批一次，不是每次调用一次。** Claude Code 接 `PostToolBatch`（无 matcher，每批工具调用结束后触发一次，携带整批 `tool_name`/`tool_input`/`tool_response`）。这是用户第 2 条裁定的直接落点：hook 的调用次数从「每个工具调用」降到「每个批次」，且批次里所有工具的结果都在一个事件里，扫描一次即可。
- **R3 — 不支持批量事件的宿主用 `PostToolUse` 无 matcher。** Codex / CodeBuddy / Trae 没有 `PostToolBatch`，改用 `PostToolUse` 且 matcher 为 `"*"`（文档明写省略 matcher 或 `"*"` 即匹配所有工具）。`runtime.md` 如实记录两种接线方式与各自代价，不是同一句话含糊过去。
- **R4 — 存储与隔离不变。** 仍写 `<absolute-git-dir>/taskflow/external`，一行一个绝对 URL；仍与 `taskflow/evidence` 完全隔离，检索记录**永远不能**释放 stage。
- **R5 — `approve` 的背书判定不重写。** 仍是「`- Source:` 的 host 出现在 `external` 中」。旧格式行（`search|<query>`、`fetch|<url>`）因整行包含 host 而继续命中，因此**不需要迁移代码**。
- **R6 — 记录器不联网、不读仓库、不校验可达性**（沿用 v2 的 R5）。只读宿主已投递的事件。
- **R7 — 仓库规则一：release 标题与 tag 格式写进 `RELEASE.md`。** tag 名 `vX.Y.Z`；annotated tag subject、GitHub Release 标题、Release body 首行统一为 `TaskFlow X.Y.Z`（不带 `v`，取 11 个 `1.1.x` release 的现行写法）；body 首行形如 `TaskFlow X.Y.Z — YYYY-MM-DD`。
- **R8 — 仓库规则二：`CONTRIBUTING.md` 的宿主规则从 hook 推广到任何能力。** 主语改成「可以被宿主承载的能力」（hook、skill、命令、manifest、安装说明）；保留 not wired / not supported 的二分并要求 `runtime.md` 逐宿主写结论。
- **R9 — 本任务的接线按 R8 执行。** Claude Code 全量（`PostToolBatch`）；CodeBuddy 与 Trae 接 `PostToolUse` 无 matcher（它们已投递 `tool_name`/`tool_input`，`tool_response` 未见实测）；Codex 接 `PostToolUse` 无 matcher 并标注「文档如此、未实测」；dsh 明确写「不可接」及原因（`tool_name` 小写且桥接不翻译）。
- **R11 — 流程引导里明说「需要搜索就去搜」。** 现有三处停顿点只问「这件事依赖仓库外吗」，**没有一处说搜索是允许的**；一个模型读到「每个结论都要能在仓库内指认」很容易把搜索读成越界。在 `SKILL.md` 的三处停顿点各补一句授权措辞（需要外部事实时允许并鼓励直接检索，检索会被记录、不会被当作越界），并在 `hooks/prompt-reminder` 的任务行里加一行同义短句——它每回合都在，是三处停顿点唯一覆盖不到的时段。

## Acceptance Criteria

- **A1** 一个 `PostToolBatch` 事件，`tool_calls` 中任一工具的 `tool_response` 含 `https://…`，`external` 出现该 URL 一行。
- **A2** 同一事件内同一 URL 出现多次，只记一行。
- **A3** 一个不含任何 URL 的事件（如纯 `Read`、纯 `Edit`）不写任何行。
- **A4** `Bash` 的 `tool_response` 中的 URL 被记录（覆盖 `dg` / `tvly` / `sxng` 这条 CLI 路径）。
- **A5** 记录器绝不写 `evidence`（现有断言保持为反向证明）。
- **A6** 记录器对 `tool_name` 无依赖：把同一个含 URL 的事件里的 `tool_name` 换成任意假名，记录结果不变。
- **A7** `approve`：`- Source:` 的 host 在 `external` 中出现 → 通过；不出现 → 拒绝并点名（现有断言保持）。
- **A8** 只有 `external` 记录、`released` 为空的任务，`approve` 仍以 `stage [PRD] was never released` 拒绝（隔离的反向证明，保持）。
- **A9** 旧格式行（`search|…`、`fetch|…`）在场时，host 匹配仍通过（零迁移）。
- **A10** `RELEASE.md` 含三条格式断言（tag 名、tag subject / Release 标题、body 首行），smoke 断言它们存在。
- **A11** `CONTRIBUTING.md` 的规则主语已从 hook 推广，`runtime.md` 的每宿主结论与该规则一致（smoke 断言两侧都提到）。
- **A12** 全部新断言在 `hooks/smoke-test` 里，每条都能被变异打红。
- **A13** `hooks/task external <url> --why "<…>"` 写入 `declared|<url>` 行；缺 `--why`、URL 非绝对 `http(s)`、URL 含 `|`/换行 → 拒绝且 store 零变化。
- **A14** 一条只有 `declared|<host>` 记录的 `- Source:` 足以让 `approve` 通过，且输出把该来源标为**声明**而不是实测。
- **A15** `Bash` 的 `tool_input.command` 里含 URL、`tool_response` 为空时仍被记录（截断兜底）。
- **A16** 含 loopback URL（`http://localhost:8888/…`、`http://127.0.0.1:…`）的事件不写任何行；含私网 URL 的事件照写。
- **A17** `SKILL.md` 三处停顿点各有一句「需要外部事实时允许检索」的授权措辞；`hooks/prompt-reminder` 的任务行含同义短句。两处均由 smoke 具名断言覆盖。

## External Facts

- Depends on external facts: yes
- Source: https://docs.claude.com/en/docs/claude-code/hooks
- What it settled: R2 能否成立——`PostToolBatch` 是否存在、是否每批只触发一次、是否携带每个工具的 `tool_response`。查前只有 R2 的推断（「应该有一批量级事件」），若不存在，整个「每批一次」就要退回 `PostToolUse` 逐调用，用户第 2 条裁定无法满足。文档明写它「runs once after every tool call in a batch has resolved」、「There is no matcher for this event」，输入为 `tool_calls[]` 且每项含 `tool_name`/`tool_input`/`tool_response`；同页写明 `PostToolUse` 的输入含 `tool_response`，省略 matcher 或 `"*"` 匹配所有工具。R2 与 R3 因此成立。
- Source: https://developers.openai.com/codex/hooks.md
- What it settled: R9 里 Codex 能否接——Codex 的 `PostToolUse` 是否投递 `tool_name`/`tool_input`/`tool_response`，以及 MCP 工具在此宿主上的名字形态。文档给出 `tool_name` 为 `Bash`/`apply_patch`/`mcp__fs__read` 这类值，并写明 `tool_input` 与 `tool_response` 按工具而异；未列出与 `PostToolBatch` 对应的事件，因此 Codex 走 R3 的逐调用形态。

**这两条来源的查证方式与它的后果（如实记录）。** 两条都实际查了，但都经 `mcp__plugin_context-mode_context-mode__ctx_fetch_and_index` / `ctx_search`，第一次 `WebFetch` 被 context-mode 的 `PreToolUse` hook 拦下并重定向。因此本任务版本在 `taskflow/external` 里**没有**任何背书记录，`task approve` 按现行规则拒绝本任务——这正是本任务要修的行为本身。修好之前，本任务只能由用户直接批准，不能靠伪造外部证据通过。

## In Scope

- `hooks/external-evidence` — 重写：去 `tool_name` 谓词，改为 URL 提取（输入侧与输出侧）；同时接受 `PostToolBatch` 与 `PostToolUse` 两种事件形状；排除 loopback。
- `hooks/hooks.json` — `PostToolBatch` 接线取代 `WebSearch|WebFetch` 的 `PostToolUse` 接线。
- `hooks/hooks-codex.json`、`hooks-codebuddy.json`、`hooks-trae.json` — `PostToolUse` 无 matcher 接线（R9）。
- `hooks/task` — 新子命令 `external`（R10）；`approve` 的背书分支改为「实测/声明」分开报告。**算法不变**：仍是 host 出现在 `external` 中即通过，旧行兼容靠字符串包含，不写迁移。
- `skills/taskflow/SKILL.md` — 三处停顿点的授权措辞（R11）。
- `hooks/prompt-reminder` — 每回合的授权短句（R11）。
- `hooks/smoke-test` — A1–A17。
- `hooks/README.md` — 钩子清单描述更新。
- `skills/taskflow/references/runtime.md` — 事件表、每宿主结论、gating 段。
- `skills/taskflow/references/artifacts.md` — `taskflow/external` 的行格式描述。
- `CONTRIBUTING.md` — R8。
- `RELEASE.md` — R7。
- `CHANGELOG.md`。

## Out of Scope

- **不做 URL 溯源过滤。** 读一个含 URL 的本地文件会让该 URL 进入 `external`。这是有意的：反向过滤（每个 URL 跑一次 `git grep`）正是用户所说「代码有点大」的来源，且只在批量事件上才勉强可负担。记为已知限制（见 Risks），不是遗漏。
- **不记录 `tool_name`。** 记录只有 `URL` 一个字段。理由同上：它不改变「有没有搜索过」的答案，却要求解析 `tool_calls[]` 里的对象边界。
- **不改 `capability-evidence` 的谓词。** R12 不变；外部证据仍永不释放 stage。
- **不给 `external` 加写保护。** 现行 `capability-gate` 只拒绝写 `evidence`/`released`，`external` 可被 `Write` 直接写。这是个真实的洞，但堵它需要把门扩展到第三个 store，属独立改动。
- **不改 `approve` 的背书算法。** 仍是「host 出现在 store 中即通过」；新增的 `declared|` 行只是让 store 多一种写入者，匹配逻辑不变。
- **不重排已有 release/tag。** R7 只管将来。
- **不让声明通道替代 `## External Facts` 的 `- What it settled:`。** `--why` 写进 store 的是一行说明，不是文档字段；文档仍要说清这条来源改变了哪个结论。

## Risks / Deferred Items

- **本地文件里的 URL 会算作外部证据。** `Read` 一个引用了 `https://docs.claude.com/…` 的旧 Plan，就能给一条 `- Source:` 背书。代价明确、方向单一（只能多记，不能少记），且真正的伪造仍需一个真实 URL。若将来实测误报率高，最小修法是记录 `tool_name` 并在 `approve` 排除 `Read|Grep|Glob` 三件只能用本机的能力——那时才值得解析对象边界。
- **`PostToolBatch` 的实际投递形态未在真实会话中观测。** 依据是官方文档，与本仓库既有的「documented, not measured」同一标准。落地后第一次真实使用时核对 `taskflow/external` 是否出现行；没有则按实际返回修正，并把 `runtime.md` 改成 measured。
- **`declared|` 行没有任何机制能验证。** 它记录的是「有人声称这条 URL 支撑了一个结论」，不是「有人打开过它」。所以 `approve` 的输出必须把两类分开写，否则这条通道会把 v1 的橡皮图章原样搬回来。它存在的理由是那个漏洞本来就有（无事件宿主上无解），而不是它无害。
- **每批扫描的代价随批次大小线性增长。** 一个批次里若有一次读大文件，事件 JSON 可能很大；记录器有单事件条数与单行长度上限，但没有总字节上限。先不处理，与 `evidence` 无限增长同一类问题。
- **Codex/CodeBuddy/Trae 的 `tool_response` 字段名未实测。** 文档对 Codex 明写有该字段；CodeBuddy/Trae 未确认。若缺字段，记录器读不到响应里的 URL，只能记录命令/参数里的 URL——仍比现状多，但会漏掉「搜索结果的 URL」。
- **R7 与已经发出去的 7 个 `TaskFlow v1.0.x` 标题不一致。** 规则只对将来生效，不改历史。

## Open Questions

- 无阻塞问题。三个岔口（拆分、判据与开销、宿主覆盖）已于 2026-11-02 由用户裁定。
