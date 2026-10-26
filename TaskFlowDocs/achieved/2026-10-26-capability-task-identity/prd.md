# PRD — 能力库的释放在任务之间串了线，`approve` 据此拒绝一个本已合规的阶段
> Task version: v1
> Status: completed

## Goal

能力库（`<absolute-git-dir>/taskflow`）的 `released` 只按 `(version, stage)` 记账，不带任务身份。两个任务共用同一个 worktree 时——或者更常见地，一个任务归档后下一个任务落在同一个 worktree——后者的释放记录会**命中前者的行**，于是：门认为该阶段「已经释放过」而直接放行，`approve` 却要求 Plan 里那一行写出**前者记录的**能力名。本任务给 `released` 行加上任务身份，让两个消费者按 `(task, version, stage)` 对账，并**一并修掉** `approve` 只看第一条 `- [Stage]` 行这件事。

## Background / Confirmed Facts

2026-10-26 在临时仓库里逐条实测（`/tmp` 一次性夹具，跑的是 `d06174e` 的码）：

1. **跨任务串线是可复现的，不是推测。** 任务 A 在 v1 释放了 `PRD`（`v1|PRD|1|invoke|agent-skills:spec-driven-development`）。任务 B 是**另一个任务**、同样 `> Task version: v1`，第一次写 `prd.md` 时门**直接放行**，`released` 没有新增任何行——它命中的是 A 的 `(v1, PRD)`。证据文件此时有 3 行，A 只用了 1 行。
2. **`unaided` 也救不回来。** 在 B 的目录下跑 `bash hooks/task unaided PRD --considered '…'`，输出是 `unaided OK: PRD in 2026-01-01-first -> … (already released)`——注意它写的是**任务 A 的名字**，因为 `hooks/task:1093-1099` 取的是 `TaskFlowDocs` 下第一个有 `plan.md` 的目录，不是当前 cwd 对应的那一个。随后 `approve 2026-01-02-second` 仍报 `stage [PRD] does not name a capability invoked in this Task version (agent-skills:spec-driven-development)`。
3. **`approve` 只读第一条 `- [Stage]` 行。** `hooks/task:1362` 是 `head -1`。实测：把记录里的能力名放在第二条 `- [Plan]` 行、第一条写另一个能力，`approve` 仍然拒绝。这条与第 1 条**互相独立**：即使 store 分任务，一个阶段如实记了两次调用也会被拒。`skills/taskflow/references/artifacts.md:132` 只说「Record a stage-tagged line」，按它写多行是合规的。
4. **没有任何东西清理这个 store。** `hooks/` 里没有一处删除或重置 `taskflow/`（`grep` 空）。`archive` / `complete` 都不碰它。所以第 1 条不是「复用 worktree 的边角情况」——同一个 worktree 跑完任务 A 再跑任务 B 就会触发，而规则要求每个任务新开 worktree，恰好挡住了最常见的那条路径，也恰好让这个缺陷长期不可见。
5. **一行写坏会让全部门都拒。** 因为 `consumed` 是对整列 `$3` 取最大值，一行 `$3` 非数字就会让 `awk` 的 `m` 落到该行上，`consumed` 变成非数字，所有数值比较都假。所以新格式不能让既有解析器看到它们不认识的字段。
6. **现场代价。** `TF-20261026-726ec4` 的 Notes 记着：为了对上记录，我直接改过 `.git/worktrees/ppt-design-layer/taskflow/released`——跨任务共享记录的越权写。已改回。这个缺陷的唯一自救手段是改别人的账本。

## Requirements

**R1 — `released` 行带任务身份。** 新写入的行是 6 个字段：`task|version|stage|seq|kind|capability`。任务名来自被释放文档所在的目录名（门）或当前活动任务名（`unaided`），也就是 `TaskFlowDocs/<task>` 的那个 `<task>`，与 `hooks/task-id` 的合法形状一致。

**R2 — 门的「已释放」判定按 `(task, version, stage)`。** 判定从 `$1==v && $2==s` 变成 `$1==t && $2==v && $3==s`（字段整体右移一位）。**这是本任务唯一改变「门放不放行」的地方**：串线从「静默放行」变成「各记各的」。

**R3 — `approve` 与 `unaided` 的「已释放」判定同步。** 两处都按 `(task, version, stage)`。`approve` 取记录、取 `cap_pool` 时都带上任务名。`unaided` 的幂等键同样加上任务名——否则任务 B 声明退回到任务 A 的旧行上。

**R4 — `approve` 接受任意一条 `- [Stage]` 行，不只是第一条。** 该阶段的多行里，只要**有一行**与记录对得上（`Unaided` 分支比 `considered`，invocation 分支比 `cap_pool` 里的名字），即通过。多行的语义是「本阶段调用过多个能力」，这正是 `artifacts.md:132` 已经允许的写法。

**R5 — `recover` 按新字段位工作，继续只丢「序号超过 `evidence` 行数」的行。** seq 从 `$3` 变成 `$4`。`released.discarded` 里留的是原样整行，不重排。

**R6 — 旧行怎么处理：不迁移、不猜，遇到就明说。** 5 字段的行没有任务身份，**无法**从内容推断它属于哪个任务——第 2 条实测已经证明这个推断是错的（`unaided` 猜的第一个活动任务就是错的）。因此：

- 解析器一律按字段数区分：6 字段是当前格式，5 字段是旧格式。
- `consumed`（两边都算）**两种都读**，取整列最大值——否则升级就会把已有 store 的序号算丢。
- 门的「已释放」与 `approve`/`unaided` 的对账**只认 6 字段行**。一条 5 字段行永远不匹配任何任务。
- 三者只要看到 5 字段行，就在输出里点明「有一条旧格式释放记录，它不属于任何任务，已不再参与对账」，并给出一次性清理路径 `rm -rf <store>`（它本来就在 R6 之外的可选路径里）。**不自动删除**，也不假装它属于当前任务。

**R7 — 不写兼容代码，不留两套格式互读的模糊地带。** 按 `CLAUDE.md`「Do not write compatibility code」。R6 的字段数分流是**读取时的一次性判别**，不是可长期共存的兼容层：写侧只有一种格式，识别旧格式的唯一作用是**报错并让人删掉它**，不是让它继续生效。

## Acceptance Criteria

- **A1** 两个任务共用 store、同名阶段、同 version：任务 B 第一次写 `prd.md` 时门**追加**一行属于 B 的记录并放行；`released` 里 A 与 B 各一行。
- **A2** 在同一夹具上，`approve` 对 B 通过（B 的 `- [PRD]` 写的是 B 自己那次调用的能力），对 A 的判定不受影响。
- **A3** `unaided PRD` 在 B 的目录下输出里带的是 **B 的任务名**，不是 A 的；且写出的行是 6 字段、任务名是 B。
- **A4** 一个阶段有多条 `- [Plan]` 行，记录里的名字在**第二条**：`approve` 通过。
- **A5** 起一个 5 字段旧格式的 `released`：门的放行判定、`approve` 的对账都**不**被旧行满足；输出点名旧格式行；`consumed` 仍然把旧行的序号算进去（不会因为升级而少算，从而误放行 `evidence` 里已被消费的记录）。
- **A6** `recover` 在 6 字段 store 上按 `$4` 算 seq，行为与今天一致（丢超出的、留有效的、追写 `released.discarded`）。
- **A7** `bash hooks/smoke-test` 通过，新增断言覆盖 A1–A6。
- **A8** 文档同步：`artifacts.md:132` 补上「多行合法、`approve` 认任意一条」；`runtime.md` 的 store 一节写清行格式与任务身份。

## In Scope

- `hooks/capability-gate`：写入行加任务名、已释放判定改为键加任务名、旧格式检测与提示。
- `hooks/task`：`unaided`（两处写行 + 已释放判定 + 活动任务选取）、`approve`（对账键、`cap_pool`、任意一行匹配、旧格式检测）、`recover`（seq 字段位）。
- `hooks/smoke-test`：新断言。
- `skills/taskflow/references/artifacts.md`、`runtime.md`。
- `CHANGELOG.md`。

## Out of Scope

- 迁移旧行（R6 明确不猜）。
- `TF-20261012-c66ad3`（版本提升要重走 N 次声明）：那是供给侧，本条是对账侧。修好本条不会让它消失。
- `TF-20261009-8abbd6`（把阶段能力选择与宿主调用流解耦）：本条不碰「选择怎么来」，只碰「记录归谁」。
- `unaided` 取「第一个有 plan.md 的目录」这个扫描逻辑本身——R3 只要求它的输出与写入带上正确任务名，选取方式是否该改成读 cwd 另行判断，见 Risks。

## Risks / Deferred Items

- **`unaided` 的 `active` 选取本来就是错的（选第一个目录，不是 cwd 那个）**，第 2 条实测抓到了。本任务只让它的**输出与写入**带上它实际选中的那个任务名，不改变它的选取方式。改造选取方式会牵动 `unaided` 的其它调用面，且和本条的两个缺陷不同源，记为 Follow-up。
- **6 字段格式对任何直接读 `released` 的外部脚本是破坏性的**，因为字段位整体右移、`version` 从 `$1` 变成 `$2`。缓解：`released` 明确不是给人读的文件（`runtime.md:65` 已经这么写：「`released` is not a file anyone is meant to read」），且唯一读它的三个消费者都在本任务里一起改。若发现第四个消费者，本条的范围要扩大。
- **旧格式行会让 `approve` 拒**，这是故意的（R6）：留着一条不属于任何任务的释放记录，比升级后静默少算更安全。代价是升级后首次 `approve` 可能要求重跑一次阶段。

## Open Questions

无。三个决定已在 2026-10-26 由用户裁定：两个都修且根因优先、store 支持多任务共享（而不是禁止复用）。
