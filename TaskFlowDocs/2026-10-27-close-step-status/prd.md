# PRD — 一个 Step 什么时候算「关闭」
> Task version: v1
> Status: checking

## Goal

让 `hooks/completion-gate` 和 `hooks/task progress` 对「Step 关闭」给出同一个答案：`- Status: done` 是唯一表示关闭的写法，其余一律算未完成。今天门对任何它不认识的写法都**放行**，所以 `completed`、`done (v1)`、`complted`、空值、甚至没有这一行，全都能把一个没做完的 Plan 送到 `achieved/`。

## Background / Confirmed Facts

2026-10-27 在本仓库直接驱动 `hooks/completion-gate` 实测（`/tmp` 一次性夹具，跑的是 `b47ea3f` 的码）：

1. **门是 fail-open 的，缺陷比「两套词表」说法更宽。** 一个只带 `- Status: complted` / `skipped` / `wip` / 空值 / 裸 `x` 的 Plan，门一律 `exit 0`「finished」。真正被拒的只有 `pending`、`in_progress`、`blocked` 三个词——因为 `hooks/completion-gate:67` 是一条黑名单：`/^- Status: (pending|in_progress|blocked)$/ { unfinished = 1 }`。任何没被列出来的值都落进「完成」。
2. **写侧只认四个词。** `hooks/task:1099-1101` 把 `- Status:` 的取值限定在 `pending|in_progress|done|blocked`，别的直接 `fail`。所以 `completed` 这类写法**不可能**由 `task progress` 写出，它只能是手改的结果——两处对同一个字段的分歧，正是那些手改的成因。
3. **真实 Plan 里已经有非规范写法。** 91 份 achieved Plan 的列首 `- Status:` 分布：254 `done`、78 `approved`（Approval 段）、6 `pending`、6 `completed`、4 `requested`（Approval 段）、3 `done (v1)`、1 `not required for read-only research`（Approval 段）。
4. **按新规则重扫这 91 份，5 份会被判为未完成**，原因分三类：`2026-09-07-repository-standards-and-doc-root` 三个 Step 是 `done (v1)`；`2026-10-11-gate-host-coverage` 四个 Step 是 `completed`；`2026-09-08-token-efficiency`、`2026-09-14-personal-docs-git-boundary` 是真的 `pending`（这两个 `> Status: completed`，Step 却从没被改过——另一个方向的同一件事）；`2026-10-22-taskflow-drift-guard` 的 `## Verification / Review` 段里有一个同名小节 `### Step 1 — per-host contract`，内容是表格不是计划步骤，没有 Status 行。
5. **写侧定位 Step 的方式是「只看标题、不分段落」。** `hooks/task:449` 扫全文件找 `### Step <数字>`，块尾是下一个 `### Step ` 或 `## `。`setr` 又只认列首 `- Status:`。所以门若按「`## Steps` 段内」来找，会和写侧看到不同的块——`2026-09-10-repository-governed-development` 就有两个 Step 块挂在 `## Approval` 段下，写侧能改、门读不到。
6. **`--approval-only` 是另一条路径。** `task state in_progress` 和 `task progress` 用它问「当前 Task version 批准了吗」，它们本来就不该要求 Plan 已完成。

## Requirements

**R1 — 关闭的判据是白名单。** 一个 Step 块算关闭，当且仅当块内**列首**存在一行 `- Status: done`（行尾空白容忍）。其余一切——`completed`、`done (v1)`、拼写错误、空值、没有这一行——都算未完成。

**R2 — Step 块的定位与写侧一致。** 块由 `plan.md` 里任意位置的列首 `### Step <数字>` 开启（数字后不能紧跟字母数字或下划线），到下一个同类标题、或下一个列首 `## `、或文件尾结束。**不按 `## Steps` 段落过滤**：过滤会重新制造本任务要消除的那种分叉（第 5 条实测）。

**R3 — 门仍然只报一句话。** 有未关闭的 Step 时仍是 `Plan has unfinished Steps`、`exit 1`。不加 Step 编号，不改既有措辞——四个调用方和既有断言都靠这句话。

**R4 — `--approval-only` 不变。** 它继续只回答批准问题，不检查 Step。

**R5 — 没有 Step 块时此项通过，且写进注释。** 一个连 `### Step` 都没有的 Plan 不因本规则被拒。这是本规则明确留下的 fail-open 残留，属于另一个问题（「Plan 可以没有 Step」），不在本任务范围内，必须在 `hooks/completion-gate` 的注释里写清，免得下一个人以为这里是全封闭的。

**R6 — 不写兼容代码，不回填历史。** 不放宽到接受 `completed` / `done (v1)`，不改 `TaskFlowDocs/achieved/` 里的任何文件。已归档 Plan 不过门，新规则对它们没有运行时后果，第 4 条的 5 份只在 CHANGELOG 里记录事实。

**R7 — `hooks/task progress` 一个字都不用改。** 它已经是这条规则的写侧与校验侧；本任务只是让读侧与它对齐。

**R8 — 文档同步。** `skills/taskflow/SKILL.md:313` 与 `skills/taskflow/references/runtime.md:244-245` 现在写的是「no Step still `pending`, `in_progress`, or `blocked`」，那是黑名单的措辞，必须改成白名单；`CHANGELOG.md` 增一条，Compatibility 段声明「归档文档不重写，其中 5 份按新规则算未完成」。

## Acceptance Criteria

- **A1** 一个 Step 写 `- Status: done` → 门 `exit 0`。
- **A2** 一个 Step 写 `- Status: completed` → 门 `exit 1`，消息含 `unfinished Steps`。（这是本条缺陷的原始症状。）
- **A3** 一个 Step 写 `complted` / `skipped` / `wip` / `DONE` / 空值 / 整行缺失 → 六种都 `exit 1`。
- **A4** 一个 Step 写 `pending` / `in_progress` / `blocked` → 仍 `exit 1`（不得回归）。
- **A5** 两个 Step 一个 `done` 一个 `completed` → `exit 1`（不能因为有一个对就整体放行）。
- **A6** Step 块写在 `## Approval` 段或 `## Verification / Review` 段下，`- Status: completed` → `exit 1`；同位置写 `done` → `exit 0`。证明定位不分段落。
- **A7** 一个没有 `### Step` 的 Plan → `exit 0`（R5 的残留，被断言钉住，而不是默默存在）。
- **A8** `--approval-only` 对 A2 的 Plan 仍 `exit 0`（批准就够了，这是 `task progress` 问的问题）。
- **A9** `bash hooks/smoke-test` 全绿，新增断言覆盖 A1–A8。
- **A10** `bash hooks/smoke-test` 的既有 completion-gate 断言不变（`cg_case unfinished` 等）——它们的 Step 用的是 `pending`/`done`，本来就在规则内。

## In Scope

- `hooks/completion-gate`：`unfinished` 判定改写为白名单 + 块定位，附注释说明 R5 的残留。
- `hooks/smoke-test`：新增 `cg_case`（A1–A8）。
- `skills/taskflow/SKILL.md`、`skills/taskflow/references/runtime.md`：措辞同步。
- `CHANGELOG.md`。

## Out of Scope

- `TaskFlowDocs/achieved/` 里 5 份 Plan 的内容（R6）。
- `hooks/task progress` 的取值集合（R7：已经是 `pending|in_progress|done|blocked`）。
- 「Plan 可以没有 Step」这条残留口径（R5）——只记录，不关掉。
- `TF-20261027-e4ba77`（长实现里不打扰）与本条同源，但那条要改的是注入节奏，不是门的判据。
- `TF-20261027-e8c6dc`（先问结论是否依赖外部事实）——同一个 session 里记下的另一个问题。

## Risks / Deferred Items

- **这是收紧，会让某些今天能归档的 Plan 被拒。** 缓解：被拒的只有「Step 没写 `done`」的 Plan，而 `task progress` 一直只肯写 `done`，所以正常流程产出的 Plan 不受影响；受影响的是手改过的，而它本来就该被拒。
- **`### Step N` 这个形状被别处复用作普通小标题会误判。** 实测 91 份里有 1 份（`2026-10-22-taskflow-drift-guard`）。选「任何 `### Step N`」而不是「`## Steps` 段内」是为了和写侧一致（第 5 条）；代价是这种复用会被算成未关闭的 Step。写侧本来也把它当成 Step 来改——所以这不是新分叉，是同一个已存在的约定。
- **CRLF。** 仓库 `.gitattributes` 是 `* text=auto eol=lf`，实测归档 Plan 全是 LF。行尾仍按空白容忍处理，`[[:space:]]` 在 `LC_ALL=C` 下含 `\r`，不需要额外分支。

## Open Questions

无。三个岔口已于 2026-10-27 由用户裁定：白名单只认 `done`；块定位用任意 `### Step N`；归档的 5 份不动、只记录。
