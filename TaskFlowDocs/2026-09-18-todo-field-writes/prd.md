# Move the deterministic Todo field writes into hooks/task

> Task version: v2
> Status: checking

## Goal

把那部分**没有语义判断**的 Todo 字段写入交给 hook，省掉 Agent 为了改两行而读整个 `todo.md` 的 token；再让 Agent 能在**不回读整份 `todo.md`** 的前提下确认条目现状。具体落点是新增 `hooks/task next`（原子写入 `- Next action:`、`- Updated:`，按需追加 Notes）与 `hooks/task get`（只打印指定条目的字段）。

## Background / Confirmed Facts

- **成本实测**：`TaskFlowDocs/todo.md` 现为 692 行 / 30,881 字节。本会话为改一条条目的 `Next action`，读了整个文件（约 8k token），实际改动是 2 行。比例的荒谬之处就是本条 Todo 的由来。
- **具体实例（用户提出本条的直接触发点）**：`TF-20260918-ad8348` 在 PR #40 打开后，`Next action` 从 `Complete PRD / Spec / Plan and request approval.` 改成 `PR open on \`fix/conflict-side-review\`; await review and merge.`。这句话完全由已知状态推出——是模板填空，不是判断。
- **边界所在**：不是所有写入都能挪。`Goal`、`Notes` 的**内容**、条目标题仍需 Agent 写（要判断）。能挪的是「字段位置 + 固定/给定值 + 日期」这一类。
- **既有先例（照抄其形状，不另造）**：
  - `hooks/task state` 已经是机械化写入：推进状态时顺带写 `- Status:` 与 `- Updated:`（`hooks/task:547-554`），并且**刻意不碰** `Next action`——它无法知道下一步是什么。所以 `Next action` 需要一个独立的入口，而不是塞进 `state`。
  - `hooks/archive` 已在自己的 AWK 里写 `- Next action: None — completed and archived.`（`hooks/archive:54-63`），且**当字段缺失时补一行**而不是报错，理由写在注释里：不要因为 Todo 形状问题让归档失败。
  - `hooks/task progress` 的可选第 4 参 `verification` 是位置参数（`hooks/task:560`）——本命令的可选 notes 沿用同一房型。
- **现成机制足够，不需要新技术**：`TASK_AWK` 里的 `findsec(id, task)` 按 `- ID:` 定位 section（`hooks/task:91-98`）；`setr` 替换范围内首个 `^- <name>:` 行（`hooks/task:100-104`）；`run_awk_to` 经同目录临时文件落盘，失败则原文不动（`hooks/task:248-263`）。
- **寻址必须用 Todo ID，不能用 task-id**：未 promote 的条目里没有 `TaskFlowDocs/<task>/` 链接，归档后路径又变成 `achieved/<task>/`。只有 `- ID:` 三个状态下都稳定。
- **`task get` 应当保留既有的机读形态（R8）**：`hooks/task:461-466`、`:666` 内部已经用 `TASKFLOW_CMD=get` + `TASKFLOW_KEYS` 取字段，并靠 `sed -n '2p'`、`awk '{print $NF}'` 这类 position 解析读取。新命令行若改输出格式，会同时改掉这三处的既有行为；因此 `task get` 的输出形状必须与既有 awk 分支一致，并且**不动那三个内部调用点**。
- **为什么不需要批准门禁**：`require_approval` 保护的是已批准任务的实施；Todo 是三分诊元数据，不是批准过的产物。`state`/`progress`/`complete` 用它，`intake` 和 `promote` 不用。
- **v1 那一侧的代码已经落地但尚未提交**：`hooks/task` 的 `next` 子命令与 `hooks/smoke-test` 的对应节在 v1 下完成，工作区里是未提交状态。v2 的 `task get` 与它们同属一次交付，因此本版本变更**沿用同一分支、同一次提交**，不另起提交。这不是流程例外，是同一交付物在同一分支上的继续。

## Requirements

- R1：新增 `hooks/task next <todo-id> <next-action> [notes]`，一次调用原子完成：写 `- Next action: <next-action>`、刷新 `- Updated: <今天>`、当给了第三个参数时追加一条 Notes。
- R2：按 **Todo ID** 定位条目，经既有 `findsec` 复用；inbox、已 promote、已归档三种状态下都能命中。
- R3：不设批准门禁——与 `intake`、`promote` 一致，而非与 `state`、`progress`、`complete` 一致。
- R4：Notes 追加落在 **Notes 块末尾**（`- Notes:` 起，直到出现下一个 `- <字段名>:` 行为止），而不是无条件追加到条目末尾——否则会插到 `- Updated:` 之后。
- R5：字段缺失时**补行而不是失败**，与 `archive` 对缺失 `Next action` 的既有处理一致；`Next action` 补在 `- Status:` 之后，`Notes` 补在条目字段块末尾。
- R6：只用 POSIX awk/sed + bash 3.2，不引入语言运行时——与 `hooks/` 其余部分的边界相同。
- R7：新增 `hooks/task get <todo-id>`，只打印该条目的字段行，不打印整份 `todo.md`。这是本任务原本列为 Follow-up 的「读」的一侧，现提升为范围内。
- R8：`task get` 的输出按 whitespace 切成词后仍可解析（字段名是单个词，值可含空格），使 `awk '{print $NF}'`、`grep`、`sed -n '2p'` 之类的读取方式无需改动即可用。

## Acceptance Criteria

- `bash hooks/task next <todo-id> "<text>"` 后：该条目的 `- Next action:` 为新值、`- Updated:` 为当天，且**条目其余部分逐字节不变**。
- 带第三个参数时，新行出现在 Notes 块末尾，而不是 `- Updated:` 之后。
- 对无 `- Next action:` 的条目：补行后成功，不报错。
- 对无 `- Notes:` 的条目：补出 `- Notes:` 行后成功。
- 命令对 **inbox**（无 Task 链接）与 **已归档**（`achieved/` 路径）条目都能命中；对不存在的 ID 报 `Todo entry not found: <id>` 并非零退出。
- `bash hooks/task get <todo-id>` 只输出该条目的字段行——**不含条目标题、不含其他条目**——字段顺序与 `todo.md` 中一致；对不存在的 ID 报同样的 `Todo entry not found` 并非零退出。
- `task get` 的输出可被 position 解析：`awk '{print $NF}'` 取 `ID` 值得到 `TF-…`。
- `bash hooks/smoke-test` → `ALL SMOKE PASSED`；`bash hooks/release-check .` → `pass`；`git diff --check` clean。
- 改动范围只含 `hooks/task`、`hooks/smoke-test` 与本任务目录。

## In Scope

- `hooks/task`：新增 `next` 与 `get` 两个子命令及配套的 `TASK_AWK` 分支。
- `hooks/smoke-test`：新增一节覆盖这两个命令。
- 本任务 PRD / Plan。

## Out of Scope

- 需要判断的字段：`Goal`、条目标题、Notes 的**内容**仍由 Agent 写。本命令只负责把 Agent 给定的文字放到正确位置。
- `TF-20260918-88e04c`（归档的 stage 步骤与分支选择）——同一家族，但卡在「hook 不碰 Git」这条设计边界上，需要的是架构决断而非机械写入，单独处理。
- 改 `task state` 让它顺带写 `Next action`（见 Background：状态推进与下一步并非总是同时变化）。
- `TF-20260918-172455`（archive 事务往 todo.md 插空行）——独立的既有 bug。
- 重排或回填 `todo.md` 里历史条目的字段顺序。

## Risks / Deferred Items

- **Notes 块的边界靠字段名清单判定**：`- Notes:` 之后连续以 `- ` 开头、且不匹配 `- <字母/空格>+:` 的行都算该块。若某条续行写成 `- Goal: ...` 这种形状，会被误判为块尾，新行插在它前面。最坏后果只是**位置偏差，不丢内容**——这是 append，不是覆盖。
- **新增了两个插件对外的子命令**，属于扩大公开面。因此必须有 smoke 覆盖，否则宿主上出错无声。
- **`task get` 把条目内容（含 Notes）带进 Agent 上下文**。相对读整份 `todo.md` 是净减少，但它让「取一条」的成本再次随条目长度增长。Notes 写得很长的条目仍会占上下文——这是本命令的固有形态，不是缺陷；真要压，只能让调用方自己截断。
- **`hooks/summarize-state` 不受影响，但它自己复制了一份 Todo 字段解析**：`hooks/summarize-state:37-64` 内联了一段 `rfield` + section 扫描，直接读 `todo.md`，**不经过** `hooks/task` 的 awk。所以新增 `task get` 命令行不改变它的行为（SessionStart 每次会话都会跑，这一点很重要）。代价是同一套解析规则现在有两份实现；合并它们是独立的重构，见 Follow-ups。

## Open Questions

- 无阻塞项。范围与命名由用户在 2026-09-18 定稿：写入侧取 `Next action` + `Notes`，寻址用 Todo ID，子命令名 `task next`；同日追加「读」的一侧为 `task get`，并入本任务而不另开任务。

## Version History

- v1 — planning：写入侧（`task next`）。
- v2 — 用户追加「读」的一侧（`task get`），并入本任务。Goal、Requirements（新增 R7/R8）、Acceptance Criteria、In Scope 随之更新。
