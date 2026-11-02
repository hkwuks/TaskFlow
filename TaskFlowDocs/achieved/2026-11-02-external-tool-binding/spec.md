# Spec — 外部证据绑定任意工具
> Task version: v1

## Objective and Success Criteria

把「任务是否去过仓库外」的判据从**工具名白名单**换成**结果里的绝对 URL**，并把记录频率从「每次工具调用」降到「每批工具调用」一次。成功判据即 PRD 的 A1–A12。

## Architecture Boundaries and Responsibilities

| 组件 | 责任 | 不负责 |
|---|---|---|
| `hooks/external-evidence` | 从宿主事件中抽取绝对 URL，写 `taskflow/external` | 判断是否值得记录、校验可达性、访问网络、读仓库 |
| `hooks/capability-evidence` | 记录能力类调用，喂 stage 门 | 外部证据（保持隔离） |
| `hooks/capability-gate` | 写入前按 stage 放行 | 读 `external` |
| `hooks/task approve` | 用 `external` 为 `- Source:` 背书 | 写入 `external` |
| `hooks.json` / `hooks-*.json` | 把接收器接到各宿主的事件上 | 任何判定 |

边界不变：**两个 store、两条消费路径**。`external` 只被 `approve` 读，永不释放 stage。

## Project Structure / Affected Files

```text
hooks/external-evidence        重写（本任务的主体）
hooks/hooks.json               PostToolBatch 接线
hooks/hooks-codex.json         PostToolUse 无 matcher
hooks/hooks-codebuddy.json     PostToolUse 无 matcher
hooks/hooks-trae.json          PostToolUse 无 matcher
hooks/smoke-test               A1–A12
hooks/README.md                钩子清单描述
skills/taskflow/references/runtime.md    事件表 + 每宿主结论
skills/taskflow/references/artifacts.md  external 的行格式
CONTRIBUTING.md                宿主覆盖规则推广
RELEASE.md                     release 格式规则
CHANGELOG.md
```

## Interfaces, Data Flow, and Contracts

### 输入契约（两种形状，同一判据）

**形状 A — 批量事件（Claude Code `PostToolBatch`）**

```json
{"hook_event_name":"PostToolBatch","cwd":"…",
 "tool_calls":[{"tool_name":"WebSearch","tool_input":{…},"tool_response":{…}}, …]}
```

**形状 B — 单调用事件（Codex / CodeBuddy / Trae `PostToolUse`）**

```json
{"hook_event_name":"PostToolUse","cwd":"…","tool_name":"…","tool_input":{…},"tool_response":{…}}
```

记录器**不区分两者**：它只把整段事件 JSON 当作待扫描文本，因为 URL 出现在哪个字段对判据没有影响。`hook_event_name` 只用于拒绝非工具事件（`PreToolUse`、`SessionStart` 等）。

这不是「偷懒的文本搜索」——它正是判据的定义：**判据是「这个事件里有没有一个仓库外的绝对 URL」，不是「哪个工具的哪个字段里有」**。按字段解析会重新引入 R1 要消除的白名单：每接一个新工具就要知道它的响应形状。

### 输出契约

```text
<absolute-git-dir>/taskflow/external
https://docs.claude.com/en/docs/claude-code/hooks
https://developers.openai.com/codex/hooks.md
declared|https://example.com/spec — the retry limit another service documents
```

- 观测得到的行：**一行一个 URL**，无前缀。
- 声明得到的行：`declared|<url> — <why>`，只由 `hooks/task external` 写。前缀是这个格式里唯一的 kind 字段，理由是「谁写的」在审计时需要看得见，而观测不需要区分来源工具。
- 事件内去重（同一个 URL 只写一行）；**跨事件不去重**（读 store 去重会让每次写入都读一遍文件，而 `approve` 只做包含匹配，重复行无害）。
- 单事件上限 50 个 URL，单行上限 400 字符。
- 只接受 `http://` 与 `https://`；`file://`、`ftp://`、`git@`、`ssh://` 不收。
- **排除 loopback**：`localhost`、`127.0.0.1`、`[::1]`、`0.0.0.0`。`dg` 背后是 `localhost:8888` 的 SearXNG，把它的地址记成外部来源是错的。私网地址**不排除**——内网文档站是合法来源。

### 声明通道的输入契约

```bash
bash hooks/task external <absolute-http(s)-url> --why "<the conclusion it changed>"
```

- 两者都必填，URL 必须是绝对 `http(s)`，`--why` 非空且不含 `|`/换行。
- 写成 `declared|<url> — <why>`，追加到同一个 store。
- 幂等：同一 URL 已在 store 中出现（任意格式）则不重复写，打印 `already recorded`。
- 无活动任务、非 TaskFlow 仓库、store 不可写 → 拒绝并说明，**不静默**——这是显式动作，不是后台记账。

### 兼容

旧行 `search|<query>` 与 `fetch|<url>` 继续留在文件里：`approve` 用整行包含 host 匹配，三种格式（旧两种 + `declared|`）都命中，**无迁移代码**。

## Invariants and Compatibility

1. **隔离**：`external-evidence` 永不写 `evidence`；`capability-gate` 永不读 `external`。（smoke 反向断言）
2. **不联网、不读仓库、不校验可达性。**
3. **每个错误路径 `exit 0`。** 记账失败绝不能阻断被观察的工具调用。
4. **非 TaskFlow 仓库、仅 achieved 的仓库、非活动任务目录一律 no-op。** 现有守卫原样保留。
5. **`tool_name` 不参与判定。** 把事件里的 `tool_name` 换成任意值，输出必须逐字节相同（A6 用这个不变量）。

## Validation and Error Semantics

| 情形 | 行为 |
|---|---|
| 事件 JSON 非法 | `exit 0`，不写 |
| `hook_event_name` 不是 `PostToolBatch`/`PostToolUse` | `exit 0` |
| 事件里没有绝对 URL | `exit 0`，不写 |
| URL 只有 loopback | `exit 0`，不写 |
| `cwd` 不在 git 仓库 | `exit 0` |
| 仓库无活动 TaskFlow 任务 | `exit 0` |
| `mkdir`/追加失败 | `exit 0` |
| URL 含 `|` 或换行 | 截断/替换后写入（沿用现有清洗） |
| **`task external` 参数不合法** | **拒绝（exit 1），store 零变化**——显式动作不 fail-open |

## Code and Test Constraints

- POSIX shell + `awk`/`sed`，bash 3.2 + BSD userland 下限；不引入解释器（`hooks/README.md` 的既有约束）。
- extensionless，`run-hook.cmd` 兼容。
- 只改动本任务列出的文件。
- 断言写在 `hooks/smoke-test`，形态沿用既有夹具（构造事件 JSON → 喂脚本 → 比对 store）。

## Design Decisions and Alternatives

### D1 — 判据从「工具名」改为「结果里的 URL」（相对方案：绑类别）

绑类别（`Skill|Agent|Task|mcp__.*|Bash|WebFetch|WebSearch`）能覆盖现有工具，但每个新宿主/新类别都要改代码，且 `mcp__codegraph__*` 会被当成外部检索。URL 与工具名无关，是**唯一**既能覆盖任意工具、又不需要维护清单的判据。

**代价（已知并接受）：** 读一个含 URL 的本地文件也算。见 PRD Risks 第 1 条与升级路径。

### D2 — 用 `PostToolBatch` 而不是 `PostToolUse`（相对方案：逐调用）

用户裁定「没必要每次调用都跑 hook」。`PostToolBatch` 每批触发一次且携带整批 `tool_response`，既省调用又让「一批里的搜索」一次扫完。宿主不支持批量事件时退回 `PostToolUse` + matcher `"*"`，这一差异必须写进 `runtime.md`，不能含糊成一个 「已接线」。

### D3 — 记录器不解析 JSON 结构

理由见「输入契约」。副作用是 `json-field` 不参与本 hook——它按字段取值，而这里要的是整段文本。实现是 `tr` 归一化 `\/` → `/`，再 `grep -o` 取 URL，再 `awk` 去重并施加上限。**扫整段事件而不是某一字段**同时解决了截断问题：`tool_input.command` 里的 `curl https://…` 不会像大响应那样被中段截断。

### D4 — 不记录 `tool_name`

它不改变「有没有搜索过」的答案，却要在 `tool_calls[]` 里切对象边界，正是用户点名的「代码有点大」。若将来需要按工具排除（PRD Risks 的升级路径），那时再解析。

### D5 — 宿主覆盖按 `CONTRIBUTING.md` 的新规则逐条落

Claude Code 全量；Codex/CodeBuddy/Trae 逐调用；dsh 记录为**不支持的机制**（`tool_name` 小写且桥接不翻译），而不是「未接」。这条同时是新规则的第一个受用者——规则和它的样本一起落地。

### D6 — 无事件时用显式声明，而不是放宽 checks

`approve` 要求每个 `- Source:` 有记录，而「用户自己查完给了 URL」「宿主没装 hook」「dsh 接不上」都不产生事件。三个选项：fail-closed 永远是红的、store 不存在时放行、显式声明通道。选了第三个，理由是它与既有的 `unaided` 是同一个信任模型——**显式、可见、可审计**，而不是让检查在看不见的地方失效。代价是声明不可验证，所以 `approve` 的输出必须把「实测」与「声明」分开列，否则这条通道会把 v1 的橡皮图章搬回来。

## Open Questions

无。用户已就拆分、判据与开销、宿主覆盖三项裁定。
