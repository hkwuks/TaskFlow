# hooks/reopen does not rewrite the Todo Task: path back to the active root, so ta
> Task version: v1
> Status: in_progress

## Goal

让 `hooks/reopen` 与 `hooks/archive` 真正互逆：把已归档任务取回活动根的同时，把 `archive` 写进 Todo 的那几处改动**做回去**，使 reopen 一结束，`hooks/task` 的任何命令都还能找到这条目。

现状是单向的：`archive` 会改 Todo，`reopen` 不会。于是 reopen 之后条目指向一个已经不存在任务的活动路径（`achieved/…`），`task state` 找不到它，流程在第一次调用时就断。

## Background / Confirmed Facts

**缺陷本身**

- `hooks/archive:55-99` 把 Todo 条目的 `Task:` 改写成 `` `TaskFlowDocs/achieved/<task>/` ``、`Status:` 改成 `done`、`Next action:` 清成 `None — completed and archived.`。
- `hooks/reopen` 只做两件事：把目录 `mv` 回活动根（`:12`），给 Plan 的 Change Log 插一行（`:14-41`）。Todo 一字未动。
- `hooks/task:120-127` 的 `findsec` 用**字面子串**定位条目：`rfind(a, b, "`TaskFlowDocs/" task "/`")`，底层是 `index()`。`achieved/` 拼写下，`` `TaskFlowDocs/ `` 之后紧跟的是 `achieved/`，该子串不成立——所以查找必然落空。

**实测（2026-10-01，本会话早段）**

`hooks/reopen` 取回 `2026-10-01-taskflow-commit-path` 之后，`bash hooks/task state 2026-10-01-taskflow-commit-path` 报 `Todo entry not found`，我手工改掉 Todo 里那一行才继续。这不是推测出来的路径，是实际撞到的。

**断点位置**

`hooks/version` 不读写 Todo（`grep` 过整个文件，无匹配）。所以断点是 reopen 之后**第一次**调用需要按 task 定位条目的子命令：`task state`、`task get`、`task progress`、`task complete`。其中 `task state` 通常紧接着就来（取回后要升版本、重新批准，然后 `state ready`），所以它最先撞上。

**契约现状与其缺口**

`SKILL.md:100` 与 `:279` 要求：取回整个目录到活动根、**记录 Todo source 与 reopen 原因**、创建新 Task 版本、重新批准。即「记录」这一步本就指派给 Agent。但 hook 自己把条目改成了查不到的形状，Agent 即使照做，用的也是坏掉的前提；`reopen` 的成功提示仍写着 `record Todo source`（`hooks/reopen:43`），与实际不符。

**`archive` 已有的纪律，`reopen` 一样都没有**

`hooks/archive`：Todo 条目缺失即**不开始**（`:23-25`）；Todo 写失败或校验不过即回滚 `mv` 并恢复 Todo（`:29-37`、`:93-98`）；写后 `verify`（`:101-113`）；成功后打印提交用的 stage 行（`:119-121`）。`reopen` 既无预检、无回滚、无校验，也不打印 stage 行。

**可复用的既有测试设施**

`hooks/smoke-test:519` 已经把 fixture `2026-09-08-smoke` 归档，其 Todo 条目随即带上了 `achieved/` 拼写与 `- Status: done`；`:645-648` 的 reopen 一节紧接其后运行，因此那一节天然具备「已归档 + Todo 已改」的初始状态，可直接加断言。现有 reopen 断言只验目录搬回与 change log 行，不碰 Todo。

**本机限制**

整段 `hooks/smoke-test` 在这台 Windows + MSYS 上跑不完（无解释器一节因软链启动的二进制找不到 DLL 而中止，未修改的 `origin/main` 在同一处同样失败）。因此新增断言在本地以「抽取该节单独运行」验证，整体判定交给 CI 三平台。

## Requirements

- **R1 —— 条目必须重新可见。** reopen 结束后，Todo 条目必须能被 `hooks/task` 的**同一谓词**（`` `TaskFlowDocs/<task>/` ``）找到。
- **R2 —— 与 archive 互逆。** archive 改到的每个字段，reopen 都改回去：`Task:` 回活动根、`Status:` 回 `promoted`、`Next action:` 换成重开语义；并盖 `Updated:`。既有 `- ID:`、`- Source:`、`- Goal:`、`- Notes:` 等一律逐字保留。
- **R3 —— fail closed。** Todo 中没有该条目的已归档任务，reopen **不移动目录**就退出非零并说明缺失。Todo 写失败或写后校验不过，**回滚 `mv` 并恢复 Todo**；不允许「目录已搬回、Todo 未改」或反之共存。
- **R4 —— 校验谓词与查找谓词一致。** 写后校验用 `` `TaskFlowDocs/<task>/` `` 这个子串，即 `findsec` 判据本身，而不是另造一个更宽松的判据。
- **R5 —— 不扩散。** 不新增命令、不改 `hooks/task` 的 `findsec`、不改 `hooks/archive`、不改 `skills/**`。
- **R6 —— 打印 stage 行。** 校验通过后打印本次翻动需要提交的路径，措辞与 `archive` 对称。
- **R7 —— 进测试。** 新行为进入 `hooks/smoke-test` 的 reopen 一节：一条正向断言（条目被改回且 `task state` 重新找到它）、一条负向断言（条目缺失时拒绝且目录未动）、一条回滚断言（Todo 写不出来时目录留在 achieved/ 且 Todo 逐字节未变）。
- **R8 —— 不追溯。** 历史上已处于「reopen 过但 Todo 未修」状态的条目不由本任务批量修复；如需，另立待办。

## Acceptance Criteria

- **A1 —— 字段逐项正确。** 对已归档且 Todo 条目齐全的任务跑 `hooks/reopen` 后，`todo.md` 中该条目满足：`- Task: \`TaskFlowDocs/<task>/\``（精确整行）、`- Status: promoted`、`- Next action: Re-approve the new Task version before core changes.`、`- Updated: <今天>`；且 `- ID:`、`- Source:`、`- Goal:` 与运行前逐字节相同。
- **A2 —— 端到端（缺陷的直接反面）。** 紧接着 `bash hooks/task state <task> planning --root <fixture>` 成功——旧代码在此必失败。这条是「修好了」的定义。
- **A3 —— 负向不漏。** Todo 中没有该条目的已归档任务：reopen 退出非零、打印指明缺失的提示，且目录**仍在 `achieved/`**、活动根**没有**它。
- **A4 —— 回滚。** 用一个必然失败的 `awk` stub 注入（fixture PATH），使 Todo 那一步写不出来：reopen 退出非零，目录**仍在 `achieved/`**，`todo.md` 与运行前**逐字节相同**。手法与套件既有的 archive 回滚测试同型（`:605-643` 用 stub 的 `archive`）。
- **A5 —— 无回归。** 既有断言继续通过：目录搬回、Plan 的 Change Log 多出一行 `reopen`（`hooks/smoke-test:645-648` 原三项）。
- **A6 —— 改动面可核。** `git diff --stat` 只含 `hooks/reopen` 与 `hooks/smoke-test`；`hooks/task`、`hooks/archive`、`skills/**` 零改动。
- **A7 —— CI 为准。** `Hooks` 工作流三平台通过，run URL 记入 Plan。
- **A8 —— 未跑的要如实记。** 本机跑不完整段 smoke 套件；本地只跑抽取出来的 reopen 一节，其余交给 CI。Plan 中「未跑」与「跑并不过」不得读成同一件事。

## In Scope

- `hooks/reopen` —— 预检、Todo 写回、回滚、写后校验、stage 行、成功提示措辞。
- `hooks/smoke-test` —— reopen 一节内的新增断言（正向 / 负向 / 回滚）。

## Out of Scope

- 不改 `hooks/task` 的查找器（R5）。条目才是错的一方——它声称任务在 `achieved/`，而任务已经回到活动根；把查找器改宽等于把「条目应反映任务当前所在」这条规则废掉。
- 不改 `hooks/archive`（R5）。
- 不改 `skills/taskflow` 的任何措辞（R5）：`SKILL.md:100/:279` 说的「记录 Todo source 与 reopen 原因」仍由 Agent 负责，本次只让被 hook 改坏的条目重新可读。
- 不批量修复历史上已被 reopen 且 Todo 未修的条目（R8）。
- 不新增 `--reason` 之类的参数；reopen 原因仍写在 Plan 的 Change Log 与 Todo 的 Notes 里（Agent 写）。

## Risks / Deferred Items

- **风险：fail closed 会改变既有行为。** 过去「Todo 条目缺失」的已归档任务仍能被搬回（留下烂摊子），今后会被拒绝。这是有意收紧，A3 把它钉住，也在本计划里明说不算回归。
- **风险：与 archive 的字段集漂移。** archive 改三处、reopen 改四处（多 `Updated:`）。缓解：A1 逐字段断言，且套件在 archive 与 reopen 两侧各有一组断言，漂移会立刻红。
- **风险：回滚测试只覆盖一个注入点。** PATH-stub 让 `awk` 失败，覆盖的是「Todo 那一步写不出来」；`mv "$todo.tmp" "$todo"` 自身失败、或磁盘层错误等未覆盖。记入 Verification 的未覆盖项，不声称已覆盖。
- **遗留：reopen 不记录重开原因到 Todo。** 无参数，原因仍由 Agent 写进 Plan 的 Change Log 与 Todo 的 Notes。
- **遗留：历史上已被 reopen 且 Todo 未修成的条目。** 本次不扫（R8）。

## Open Questions

无。三项决策（完全对称 archive / 与 archive 同纪律 / `Status: promoted`）已由用户在 2026-10-01 裁定。

## Version History

- v1 — planning.
