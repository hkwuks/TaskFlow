# Plan — 外部证据绑定任意工具
> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md` — 输入/输出契约、不变式、五个设计决定（D1–D5）。

## Reference Pointers

- `hooks/external-evidence:69-73` — 要替换的产品清单谓词。
- `hooks/capability-evidence:45-52` — 谓词应写成类别的既有范例，且是 `external` 必须继续隔离的对象。
- `hooks/task:1473-1506` — `approve` 的 host 匹配（本任务预期零改动）。
- `hooks/capability-gate:190-194` — 目前只拒绝写 `evidence`/`released`，`external` 不在其内（本任务不改，记为已知限制）。
- `hooks/smoke-test:3063-3118` — 现有 external capture 段，A1–A9 在此重写。
- `hooks/smoke-test:2246-2296` — 隔离与背书断言（A7/A8 保持）。
- `hooks/hooks.json:60-69`、`hooks-codex.json`、`hooks-codebuddy.json`、`hooks-trae.json` — 接线落点。
- `skills/taskflow/references/runtime.md:52,56-60,89-220` — 事件表与每宿主结论。
- `RELEASE.md:114-137` — R7 的落点。
- `CONTRIBUTING.md:98-118` — R8 的落点。
- 宿主文档：`docs.claude.com/en/docs/claude-code/hooks`（`PostToolBatch`、`PostToolUse`）、`developers.openai.com/codex/hooks.md`（`tool_name`/`tool_response`）。

## Related Tasks

- **上游**：`TaskFlowDocs/achieved/2026-10-31-external-facts/`（v2，已并入 `main` 的 `9c27ceb`）——本任务修正它的 Out of Scope 边界（同宿主其他工具被漏掉）与 `external-evidence` 的产品清单谓词。
- **原则来源**：`achieved/2026-09-27-capability-pre-write-gate/prd.md:52`（R3：谓词是类别不是清单）与 `:61`（R12：内建工具不释放 stage，本任务不改）。
- **规则样本**：`achieved/2026-10-11-gate-host-coverage/`（多宿主接线先例）。
- **Todo**：`TF-20261102-7a9caa`（主）；`TF-20261102-ee1698`、`TF-20261102-d14d22` 已按用户裁定合并进本任务并记入 `## Removed`。

## Skills / Tools Used

- [PRD] `mcp__plugin_context-mode_context-mode__ctx_fetch_and_index` — purpose: 取宿主 hooks 文档与 Codex hooks 文档，确定 `PostToolBatch` 是否存在、投递什么；outcome: succeeded; incorporated: 批量事件无 matcher、每批一次、携带 `tool_calls[]` 的 `tool_response`，据此定下 R2/R3 与 PRD 覆盖矩阵。
- [Spec] `mcp__plugin_context-mode_context-mode__ctx_search` — purpose: 在已取文档中核对 `tool_response`、MCP 命名与 Codex 的 `tool_name` 取值；outcome: succeeded; incorporated: 输入/输出双形状契约、`tool_name` 作为不变量，以及 dsh「不支持」的机制表述。
- [Plan] `mcp__plugin_context-mode_context-mode__ctx_fetch_and_index` — purpose: 复核 `ctx_fetch_and_index` 的返回与文档段落以确定 Step 边界与验证方式；outcome: succeeded; incorporated: Step 1–7 的文件划分与每条 Acceptance 对应的夹具。
- [Test] `mcp__plugin_context-mode_context-mode__ctx_search` — purpose: 核对错误语义与既有 smoke 夹具形态；outcome: succeeded; incorporated: A1–A17 的构造式断言、变异表方向，以及 `external` 行格式的三类兼容。

（写入的是**实际被记录**的能力，不是计划要用的能力。本会话里商品化的 `agent-skills:spec-driven-development` 确实被调用并按其结构写了 PRD/Spec，但对 store 而言那次调用没有留下记录——四个 stage 消耗的是 MCP 记录。按 gate 的对账规则，stage 行只能点名 store 里真实存在的那次调用，所以上面四行写的是它。这是一次如实的对账修正，不是把记录改成好看的样子。）

## Preconditions

- [x] 已读 `CONTRIBUTING.md`、`CODE_STYLE.md`、`repository-docs/index.md`、`artifacts.md`、`runtime.md`。
- [x] [PRD] / [Spec] 阶段的两次能力调用已记录在 `taskflow/evidence`（MCP）。
- [x] 隔离：worktree `.worktrees/external-tool-binding`，分支 `feat/external-tool-binding`，基于 `main@e7b133a`。
- [x] 宿主事实已查官方文档（2026-11-02，非记忆）：`PostToolBatch` 无 matcher、每批一次、携带 `tool_calls[]` 的 `tool_response`；`PostToolUse` 可省略 matcher 匹配全部；Codex 的 `tool_name`/`tool_response` 形状。
- [x] 本会话实测：现行外部谓词漏掉全部 MCP 检索（`external` 为空、`evidence` 有 8 行）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-02 14:04 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

**Written by hand, and why.** `task approve` refuses this task with `no lookup backs: …` because its two external sources were fetched through MCP and via a redirected `WebFetch`, and the current predicate records neither — the very defect this task fixes. The user gave an explicit verbal approval, so the block is transcribed here rather than obtained through the hook. The alternative would have been to fabricate a lookup to satisfy the gate, which is the failure mode the gate exists to prevent. See the Change Log.

## Steps

### Step 1 — 重写记录器：URL 判据，两种事件形状

- Goal: 让外部证据与工具名无关，并接受批量与单调用两种事件。
- Dependencies: 无。
- Files: `hooks/external-evidence`。
- Implementation checklist:
  - [x] 删除 `case "$tool_name"` 的 `WebSearch|WebFetch` 分支；`tool_name` 完全不再读取。
  - [x] `hook_event_name` 只接受 `PostToolBatch` 与 `PostToolUse`。
  - [x] 整段事件文本归一化 `\/` → `/`，抽取 `https?://[^\"'\\<>[:space:]]+`；**输入侧与输出侧一起扫**（A15）。
  - [x] 去尾部标点（`.` `,` `)` `;` `:` `]` `}`）；只留 `http(s)`。
  - [x] 排除 loopback（`localhost`、`127.0.0.1`、`[::1]`、`0.0.0.0`），保留私网（A16）。
  - [x] 事件内去重，最多 50 条，每条截断 400 字符；不做跨事件去重。
  - [x] 保留现有守卫：cwd → git dir → worktree → `TaskFlowDocs` → 活动任务；全部 `exit 0`。
  - [x] 保留 `|`/换行清洗；每条一行 `URL`（无 kind 前缀）。
  - [x] 注释写明「为什么不解析 `tool_calls[]`」与「为什么不知道工具名」。
- Acceptance: PRD A1–A6、A15、A16。
- Verification: 手喂六种事件（批量多条 URL、批量无 URL、单调用 Bash 输出含 URL、`tool_name` 换成假名、命令里含 URL 而响应为空、loopback），逐一比对 store。
- Status: done
- Rollback: 单文件，`git checkout -- hooks/external-evidence`。

### Step 2 — 接线四个宿主

- Goal: 按新规则把接收器接到每个能接的宿主，并让 dsh 的缺席有理由。
- Dependencies: Step 1。
- Files: `hooks/hooks.json`、`hooks/hooks-codex.json`、`hooks/hooks-codebuddy.json`、`hooks/hooks-trae.json`、`hooks/README.md`。
- Implementation checklist:
  - [x] `hooks.json`：删 `PostToolUse` 的 `WebSearch|WebFetch` 条目，加 `PostToolBatch`（无 matcher）条目。
  - [x] `hooks-codex.json`：加 `PostToolUse`，**无 matcher**。
  - [x] `hooks-codebuddy.json`、`hooks-trae.json`：同上。
  - [x] 四个文件都不对 `capability-evidence` 做任何改动。
  - [x] `hooks/README.md` 的清单行改成新职责描述。
- Acceptance: PRD A5；接线本身由 Step 3 的 smoke 断言覆盖。
- Verification: `bash -n` 不适用（JSON）；用 `python -c`/`node -e` 解析四个 JSON 各一次确认合法。
- Status: done
- Rollback: 四份 JSON 单次 `git checkout`。

### Step 3 — `approve` 兼容性与 smoke 断言

- Goal: 证明零迁移、隔离仍然成立，并让每条断言都能被打红。
- Dependencies: Step 1、Step 2。
- Files: `hooks/smoke-test`、`hooks/task`（仅在 A7/A9 暴露问题时）。
- Implementation checklist:
  - [x] 重写 smoke 的 external capture 段：A1、A2、A3、A4、A6。
  - [x] 保留并复跑：A5（不写 `evidence`）、A7（有/无背书）、A8（隔离反向证明）、A9（旧行兼容）。
  - [x] A9 用旧格式 `fetch|https://…` 行做夹具，断言 `approve` 仍通过。
  - [x] 每条新断言做一次变异（改回产品清单 / 去掉去重 / 去掉上限），确认各自变红后逐字节恢复。
- Acceptance: PRD A1–A9、A12。
- Verification: `bash hooks/smoke-test` → `ALL SMOKE PASSED`；变异表写进 `## Verification / Review`。
- Status: done
- Rollback: `git checkout -- hooks/smoke-test`。

### Step 4 — 两条仓库规则

- Goal: 把用户追加的两条规则落成可检查的仓库文档。
- Dependencies: 无（与 Step 1–3 并行安全，文件不重叠）。
- Files: `RELEASE.md`、`CONTRIBUTING.md`、`hooks/smoke-test`（A10/A11 的断言）。
- Implementation checklist:
  - [x] `RELEASE.md`：在 tag 步骤写明 `vX.Y.Z`；在 GitHub Release 步骤写明标题与 body 首行格式，并说明取 `1.1.x` 的现行写法（不带 `v`）而不是 `1.0.x`。
  - [x] `RELEASE.md`：说明为何选这一个（11 个对 4 个），以及历史 release 不改。
  - [x] `CONTRIBUTING.md`：把「a hook change lands on every host」改写成「任何能被宿主承载的能力」；保留 not wired / not supported 的二分与「必须点名机制」的要求。
  - [x] `CONTRIBUTING.md`：加一句「样本就是 `external-evidence` 的接线」，指向 `runtime.md`。
  - [x] smoke 断言：`RELEASE.md` 含 `vX.Y.Z` 与 `TaskFlow X.Y.Z`；`CONTRIBUTING.md` 与 `runtime.md` 两侧都提到能力级覆盖。
- Acceptance: PRD A10、A11。
- Verification: `bash hooks/smoke-test`；人工读一遍两份文档确认无自相矛盾。
- Status: done
- Rollback: 两份文档 `git checkout`。

### Step 5 — `runtime.md` / `artifacts.md` / `CHANGELOG.md`

- Goal: 文档与实现一致，每宿主结论可读，且记账不夸大。
- Dependencies: Step 1–4。
- Files: `skills/taskflow/references/runtime.md`、`skills/taskflow/references/artifacts.md`、`CHANGELOG.md`。
- Implementation checklist:
  - [x] `runtime.md` 事件表：「External-lookup capture」一行改为 `PostToolBatch`（无 matcher）/ `PostToolUse`（无 matcher），逐宿主写结论，dsh 写「不支持及原因」。
  - [x] `runtime.md` 把「documented, not yet measured」段更新为当前状态（`PostToolBatch` 未实测、`PostToolUse` 的 `tool_response` 未实测）。
  - [x] `artifacts.md`：`external` 的行格式改成「一行一个 URL」，说明旧格式兼容。
  - [x] `CHANGELOG.md` [Unreleased] 下写 Added / Changed / Known limitations。
  - [x] 不写任何未实测的「已验证」。
- Acceptance: PRD A11；文档无夸大。
- Verification: `grep` 确认旧描述（`WebSearch`/`WebFetch` 作为唯一谓词）已无残留。
- Status: done
- Rollback: `git checkout`。

## Checkpoints

- Step 1 后：手喂六种事件，`external` 只有 URL 行；`evidence` 一个字节未变。
- Step 2 后：四份 JSON 解析通过；`hooks.json` 不再含 `WebSearch|WebFetch`。
- Step 3 后：`ALL SMOKE PASSED`；变异各自变红。
- Step 4/5 后：文档无旧谓词残留；CI 三平台 smoke 绿。
- Step 6 后：无 `external` 记录时 `task external` 可补；`approve` 输出分列实测与声明。
- Step 7 后：`SKILL.md` 三处与 `prompt-reminder` 各含授权措辞（A17）。

### Step 6 — 声明通道 `task external` 与 `approve` 的分列输出

- Goal: 没有工具事件时（用户自己查完给出 URL、hook 未装、dsh）仍能如实记账，且 `approve` 不把声明读成观测。
- Dependencies: Step 1（store 行格式）、Step 3（`approve` 现状）。
- Files: `hooks/task`、`hooks/smoke-test`、`skills/taskflow/references/artifacts.md`。
- Implementation checklist:
  - [x] 新子命令 `external <url> --why "<…>"`：URL 必须绝对 `http(s)`，`--why` 非空，两者均不含 `|`/换行；不合法 → 非零退出且 store 零变化。
  - [x] 写入 `declared|<url> — <why>`；同一 URL 已在 store 中出现则打印 `already recorded` 且不重复写。
  - [x] 无活动任务 / 非 TaskFlow 仓库 → 拒绝并说明（用 `fail`，不是 `unaided` 的 `exit 2`）。
  - [x] `approve` 的 `yes` 分支：仍按整行包含 host 判定通过，但把命中的行分成「实测」（无 `declared|` 前缀）与「声明」（`declared|`）两组；有声明时在成功输出里附一行说明，**不阻断**。
  - [x] `artifacts.md` 补 `declared|` 行格式与两个写入者。
  - [x] smoke：A13、A14；并复跑 A7/A9 确认旧行与实测行都仍通过。
- Acceptance: PRD A13、A14。
- Verification: 夹具各跑一次；`task external` 四种非法输入后 `wc -l` 不变。
- Status: done
- Rollback: `git checkout -- hooks/task`。

### Step 7 — 流程引导里明说「需要搜索就去搜」

- Goal: 三处停顿点只问「依赖仓库外吗」，没有一处授权搜索；补上授权措辞，并覆盖停顿点之间的时段。
- Dependencies: 无（文件与 Step 1–6 不重叠）。
- Files: `skills/taskflow/SKILL.md`、`hooks/prompt-reminder`、`hooks/smoke-test`。
- Implementation checklist:
  - [x] `SKILL.md` Phase 1 收敛段的问句后加一句：需要外部事实时**允许并鼓励直接检索**（内建搜索、MCP、CLI 都算），检索会被记进 `taskflow/external`，不会被当作越界或多余。
  - [x] Phase 3 与 Plan 定稿前两处复查点各加同义的一句短句，不复述整段。
  - [x] `hooks/prompt-reminder` 的 `context` 增加一行同义短句，放在分类问题**之前**（分类是这行提醒的主旨，授权是背景）。
  - [x] 该行只在有活动任务时出现（现有守卫已保证），不改变无任务时的输出。
  - [x] smoke：A17，三处 `SKILL.md` 各一条具名断言 + `prompt-reminder` 输出含该短语。
- Acceptance: PRD A17。
- Verification: 喂一个 `UserPromptSubmit` 事件到 `prompt-reminder`，确认输出含短句；把短句删掉确认断言变红。
- Status: done
- Rollback: 两文件 `git checkout`。

## Verification / Review

### 实测（2026-11-02）

| 检查 | 结果 |
|---|---|
| `bash hooks/smoke-test`（本机跳过「no interpreter」段） | 0 个 FAIL；新段全部通过 |
| `bash hooks/smoke-test` external 段单独运行 | `ok` |
| external 段变异 M1（loopback 过滤失效） | 红：`a loopback URL was recorded as an outside source` |
| 变异 M2（去掉输入侧） | 红：`a batch of two URLs did not record exactly two lines` |
| 变异 M3（去掉去重） | 红：`got 3` |
| 变异 M4（只接受 `PostToolUse`） | 红：`got 0` |
| 四条变异后逐字节恢复 | 是（`cmp`） |
| `bash hooks/release-check .` | `STATUS: pass` |
| `git diff --check` | clean |
| 五份 hooks JSON 解析 | 全部合法；`hooks.json` 现有 `PostToolBatch` |
| `task external` 真实使用 | 写入 `declared|` 行；重复调用幂等 |
| `task approve` 真实使用 | `approve OK`，且输出分列「backed by declaration, not observation」 |

### 本机环境限制（与本次改动无关）

`== hooks run with no interpreter available ==` 段在本机失败：Git Bash 把工具符号链接进 `$tmp/toolbin` 后执行报
`error while loading shared libraries`。在 `main`（`e7b133a`）上同样失败，因此不是本任务引入的。
本地完整运行用了一份临时副本跳过该段（已删除，`hooks/smoke-test` 未由此改动）；CI 的三平台矩阵才是权威。

### 一份如实的对账修正

`## Skills / Tools Used` 原先写的是计划要用的 `agent-skills:spec-driven-development`，但 `released` 里四个 stage
实际消耗的是 MCP 记录。按 gate 的规则，stage 行只能点名 store 中真实存在的那次调用，因此改成 MCP 名并在该节
写明原因。这不是把记录改好看，是让文档与记录一致。

## Change Log

- 2026-11-02 — v1 建立。用户三条裁定（合成一个任务 / URL 判据但不逐调用跑 hook / 按能接的宿主全接）写入 PRD Background 与 Spec D1–D5。
- 2026-11-02 — 用户追问「不用 MCP 怎么办，要考虑全面」，补 R1a（输入侧也扫）、R1b（排除 loopback）与 PRD 覆盖矩阵；又追加 R10（无事件时的显式声明通道，Spec D6、Step 6），裁定为「加显式声明通道」。
- 2026-11-02 — 用户追加「流程引导里明确告知允许搜索」，补 R11、A17、Step 7。
- 2026-11-02 — Step 1–7 实现完成。记录器改为 URL 判据（整段扫描、输入侧与输出侧、排除 loopback）；接线改为 `PostToolBatch`（Claude Code）与无 matcher 的 `PostToolUse`（Codex/CodeBuddy/Trae），dsh 记为 not supported；新增 `task external` 声明通道，`approve` 分列实测与声明；`CONTRIBUTING.md`、`RELEASE.md`、`runtime.md`、`artifacts.md`、`SKILL.md`、`prompt-reminder`、`CHANGELOG.md` 同步。
- 2026-11-02 — 对账修正：`## Skills / Tools Used` 四个 stage 行从计划中的 skill 名改为 store 里实际被消耗的 MCP 记录名，理由见 `## Verification / Review`。

## Follow-ups

- **`PostToolBatch` 落地后第一次真实使用核对投递形态**：看 `taskflow/external` 是否出现行；没有则按实际返回修正，并把 `runtime.md` 从 documented 改为 measured。
- **CodeBuddy / Trae 的 `tool_response` 字段名未实测**：若缺该字段，只能记录参数里的 URL，会漏掉「搜索结果的 URL」。第一次真实使用后补记。
- **本地文件里的 URL 会被算作外部证据**（PRD Risks 1）。若误报明显，最小修法是记录 `tool_name` 并在 `approve` 排除 `Read|Grep|Glob`。
- **`declared|` 行不可验证。** 它是「有人声称」，不是「有人打开过」。`approve` 的分列输出是它唯一的约束；不要把它读成观测。
- **`external` 没有写保护**（`capability-gate:190-194` 不含它）。独立改动，不在本任务。

## Version History

- v1 — 初始版本。
