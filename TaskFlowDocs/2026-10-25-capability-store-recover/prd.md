# PRD — 让能力库失步后可以真正恢复，而不是只有删库重来
> Task version: v1
> Status: in_progress

## Goal

能力库（`<absolute-git-dir>/taskflow` 下的 `evidence` 与 `released`）一旦失步——`released` 指向的记录序号超过了 `evidence` 的行数——今天唯一的出路是删掉整个库、把所有阶段重新声明一遍，代价是丢掉库里的全部释放记录。本任务给出一条**保留有凭据的释放、只丢弃无凭据的那几行**的恢复路径：`hooks/task recover`。

## Background / Confirmed Facts

三条已有的 Todo 记录是同一个缺口的三个投影，本任务一次收口：

1. **`TF-20261025-ef6c18`（本条）**：证据文件被截断或删除后，`released` 仍指向不存在的记录，恢复手段只有删库。
2. **`TF-20261012-c66ad3`**：`seq` 是全局单调计数器，而 release 的幂等键是 `(version, stage)`；版本提升要重走一遍声明。它的更正记录（2026-10-18）已经实测出 `unaided` 能零调用恢复，剩下的问题是**每次版本提升都要重复 N 次声明**——那是记账口径问题，与本条不同。本条只解决「库坏了怎么办」，不解决「版本提升要不要重走」。**不合并**，但本条的恢复路径会让 c66ad3 的现场少一次全量重建。
3. **`TF-20261025-537a8a`（已发布 1.1.8）**：门现在会说清楚「库失步」并给出两条路。但它给出的两条路是「补齐记录」和「删库」——后者会丢释放记录。本条是把那条路改成不丢东西。

机械事实（本次实测，`1.1.8` 的码）：

- **门的释放条件**：`evidence` 行数 > `released` 里最大的 seq。见 `hooks/capability-gate:139-162`。
- **`unaided` 的写入口径**：`consumed` 只从 `released` 取，然后 `mkdir -p` 再追加两行。它已经有一道 `[ "$consumed" -le "$total" ]` 的拒绝，是三个写者里唯一检查不变量的一员。见 `hooks/task:1143`。
- **`approve` 只读 `released`**（`hooks/task:1249`），不碰 `evidence`。所以**删掉 `released` 里无凭据的行，等价于把那几个阶段「退回未释放」**，已释放的其余阶段不受影响——这是本条能成立的全部依据。
- **三个写者**：门（消费 `evidence` 并写 `released`）、`unaided`（写两行）、`approve`（只读）。三者都维持「`released` 的最大 seq == `evidence` 行数」这一不变量；失步只可能来自外部损坏。
- **失步时 `unaided` 会进一步扩大缺口**，所以它拒绝；它现在给出的唯一恢复是删库（`hooks/task:1144`）。这是本条落地后必须同步改的第二处文案。

## Requirements

**R1 — 新增 `hooks/task recover` 子命令，语义是「丢掉无凭据的释放」。** 它读取 `evidence` 的行数 `total`，把 `released` 里 `seq > total` 的行移出。剩下的每一行都指向一条真实存在的记录，因此不变量恢复，门立刻可以继续释放。

**R2 — 被丢弃的行要留痕，不能静默消失。** 丢弃的行追加到 `<store>/released.discarded`（append-only）。理由：这八行是「哪些阶段真的被释放过」的唯一证据，删掉它们是本操作唯一的破坏性部分；留一个文件使这次操作可审计，也使得重复运行不会把上一次的丢弃记录覆盖掉。

**R3 — 幂等，且干净库上是无操作。** 第二次运行 `recover` 找不到 `seq > total` 的行，不改任何文件，打印一行说明并退出 0。库根本不存在时同样退出 0 并说明。**不修改 `evidence`**——`evidence` 里已有的行是真实调用记录，一条都不删。

**R4 — 恢复后各阶段的处境必须说清楚。** 被丢弃释放的阶段退回「未释放」，需要重新声明（`unaided`）或重新调用能力；其余阶段保持已释放，`approve` 立刻可过。命令的输出要同时给出这两个数字：丢弃了几行、还剩几行/最大 seq 是多少。

**R5 — 门与 `unaided` 的拒绝文案改指向 `recover`。** 两处今天都写「remove the store and declare again」。改后应说明：`recover` 保留有凭据的释放、只丢无凭据的；删库仍然可行但会丢全部。**保留删库这条**——它是 `recover` 之外的彻底重置，代价不同，不该被藏起来。

**R6 — 门与 `unaided` 的判定逻辑不改。** 门的释放条件、`unaided` 的拒绝条件都保持原样；本条只加一个恢复入口和改文档。**特别地：`recover` 不由任何路径自动调用**——包括不由 `unaided` 在失步时自动先修再写。把账本的修改藏进一个声明动作里，与 `unaided` 现在明确拒绝的立场相反。

**R7 — `approve` 也必须拒绝失步的库。** 2026-10-25 实测：`released` 最大 seq 4、`evidence` 3 行时，`approve` 只按 `(version, stage)` 查 `released`，没查过 seq 4 背后有没有记录，直接 `approve OK (user, v1)`；把 seq 4 的行删掉之后它才拒绝，指名那个阶段从未被释放。**同一个库、同一份文档，批与不批取决于一行无凭据的释放记录。** 这违反 PRD 立论所依赖的「删掉无凭据的行 == 退回未释放」——只要 `approve` 不查，那条等式在批准这一侧就不成立。R7 要求 `approve` 在任何 Approval 字段写入之前，先做与 `unaided` 相同的 `consumed <= total` 检查并 fail closed。这是本条唯一改动判定逻辑的地方，且方向是**更严**，不是更松。

**R8（撤回，未采纳）— 门在「证据落在隔壁库」时先说「已花掉」的那句假话，本次不改。** 原文要求 `stray_evidence` 非空且本库无记录时改用它作首句。实现并做了变异验证之后撤回：把判据换成 `if false`（即恢复原行为），整套 smoke 仍然全绿——唯一能拦住它的是我为它新写的那条断言，而那条断言只能靠状态摆布触发，不是行为判据（`detail` 全为空时那段代码根本不输出，`approve` 也从不调用 `stray_evidence`）。为一句措辞，在一个不改变任何放行/拒绝结论的位置引入不可变异的判据，测试无法验证，因此不做。理由记在这里，不是遗漏：同一条消息的后半段本来就指了名，`unaided` 与 `approve` 的失步消息也不受影响。

## Acceptance Criteria

- **A1** `bash hooks/task recover` 在失步库上（`released` 最大 seq 5、`evidence` 0 行）：退出 0，`released` 变为空，`released.discarded` 含那 5 行，`evidence` 不变。随后 `unaided PRD` 成功（证明门/写者已可用）。
- **A2** 在部分失步库上（`released` seq 1,2,3,5、`evidence` 3 行）：只剩 1,2,3，seq 5 进 `released.discarded`；`approve` 对已释放阶段的判定与恢复前一致，对被丢弃的阶段要求重新声明。
- **A3** 幂等：连续两次 `recover`，第二次不改变任何文件（`released`、`released.discarded`、`evidence` 三者逐字节相同），退出 0。
- **A4** 干净库上无操作：`released` 最大 seq == `evidence` 行数时，不产生 `released.discarded`，退出 0。
- **A5** 库不存在时：退出 0，说明无库可修。
- **A6** 门与 `unaided` 的失步文案都提到 `bash hooks/task recover`，且仍然提到删库这条路及其代价。
- **A9** 失步库上 `approve` 拒绝（在任何 Approval 字段写入之前），指名失步并给出 `recover`；删掉无凭据的行之后同一份文档 `approve` 通过。**这是 R7 的判据，也是本条唯一一条会改变已有行为的断言。**
- **A7** `hooks/smoke-test` 通过，且新增断言覆盖 A1–A5、A6、A9。
- **A8** `hooks/smoke-test-windows.ps1` 覆盖 `recover` 的基本路径（至少 A1：失步库 → 恢复 → 门放行）。**但**：本条任务的 Windows 侧断言必须能在本地跑通；如果 Windows 套件的 throw 挂起问题（`TF-20261025-645ef4`）妨碍验证，记录在 Follow-ups 而不是假装验证过。

## In Scope

- `hooks/task` 新增 `recover` 子命令（含 usage 行、退出码）。
- `hooks/task` 的 `unaided` 失步文案改指向 `recover`。
- `hooks/task` 的 `approve` 增加失步前置检查（R7）。
- `hooks/capability-gate` 的失步文案改指向 `recover`（只改字符串，不改判定）。
- `hooks/smoke-test` 新增断言；`hooks/smoke-test-windows.ps1` 新增一条。
- `hooks/README.md`（task 的子命令列表）、`skills/taskflow/references/runtime.md`（库那一节）、`skills/taskflow/references/artifacts.md`（若提到恢复路径）。
- `CHANGELOG.md` 一条。

## Out of Scope

- 改 `evidence` 的任何内容（R3）。
- 让 `unaided`、门、或任何 hook 自动调用 `recover`（R6）。
- 解决版本提升要重走声明的问题（`TF-20261012-c66ad3`），那是记账口径，另行处理。
- 让 `recover` 尝试「重建」丢失的记录。做不到：`released` 的 seq 是证据队列的位置，`Approval` 块只证明某阶段批过、不证明序号，重建出来的 seq 是编的。
- Windows 套件 throw 挂起的修复（`TF-20261025-645ef4`）。

## Risks / Deferred Items

- **`recover` 会让人手改账本变得容易。** 缓解：它只做一件事——删除指向不存在记录的行；不新增行、不改 `evidence`、不接受任何参数来指定要删哪几行。参数面越小，越不能被当成「编辑账本的工具」。
- **部分失步时「哪个阶段恢复了、哪个没有」需要人自己读。** 缓解：R4 要求打印两个数字；不要求逐阶段列举，因为 `released` 的 seq 与阶段的对应关系在失步后本来就不可靠。
- **Windows 侧验证可能被 645ef4 卡住。** 若如此，A8 记为「本地未能验证」，并在 Follow-ups 里写明原因，不写成通过。

## Open Questions

无。三个决定（恢复口径、入口位置、是否自动）已在澄清阶段由用户裁定：丢掉无凭据的、`hooks/task recover`、不自动。
