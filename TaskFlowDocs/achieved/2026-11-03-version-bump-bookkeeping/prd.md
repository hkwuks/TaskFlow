# 版本提升不再强制重走一遍能力记账

> Task version: v1
> Status: completed

## Goal

Task 版本从 vN 升到 vN+1 时，若某个阶段的**需求与选择都没变**，该阶段沿用上一版本的 release 行，不再要求重新申报一次或重新调用一次能力。今天每升一次版本都要重走 N 次（N = 需要记录的阶段数），即使只改了版本号。

## Background / Confirmed Facts

**记账行的形状**（`hooks/capability-gate:126-140`、`hooks/task:1238`）：

```
<任务>|<版本>|<阶段>|<序号>|<kind>|<能力名或概念类>
2026-11-03-probe|v2|PRD|5|unaided|requirements elicitation and framing
```

**两个键，两个语义，被同一个序号绑死**：

- `approve` 的幂等键是 **(任务, 版本, 阶段)**（`hooks/task:1180-1184`、`hooks/capability-gate:126-131`）——它问的是「这个版本的这个阶段付过账没有」。
- 而 release 的**供给**条件是 `evidence 行数 > released 的最大序号`（`hooks/capability-gate:250-260`）——序号是**全局单调**的，一次调用只能被花掉一次。

于是：每次版本提升，`approve` 都要看到 `(task, vN+1, stage)` 的新行，而新行只能靠新序号，新序号只能靠新证据。**升版本这件事本身不产生任何新信息，却强制产生 N 条新证据。**

**实测（2026-11-03，探针仓库，1.1.12 代码）**：

```
v1: 申报 PRD/Spec/Plan/Test → evidence 4 行
v2: 再申报四次              → evidence 8 行
v3: 再申报四次              → evidence 12 行
```

12 行里 8 行是重复内容。全程零真实能力调用——`unaided` 自己写 evidence 再写 release（`hooks/task:1237-1238`），所以这不是死锁，是**重复劳动**。

**这条规则有它正当的一半**，必须保住：同一个已花掉的调用不能被两个文档再花一次（`hooks/capability-gate:283-285` 的注释），且版本提升不能拿旧版本用剩的证据充数。问题只在于**它没有和「版本提升」的语义对齐**——升版本不等于阶段重走了一遍。

**已有的相关判断**（本条 Notes，2026-10-18 更正）：早先认为「evidence 用尽后 approve 永远写不进」是**错的**，`unaided` 自写 release 使零调用恢复成为可能。所以本条的正确表述是**消除重复**，不是解锁。

## Requirements

### R1 — 版本提升时沿用上一版本的阶段记录

`approve` 核对阶段时，若 `(task, vN, stage)` 无记录但存在某个更低版本的 `(task, vM, stage)`（M < N）记录，**且该记录是最后一个**，则视为该阶段在本版本已满足。

### R2 — 继承是有条件的，不是无条件的

必须同时满足，否则仍要求重新申报：

- 上一版本的该阶段记录存在；
- 本版本该阶段**没有**自己的记录（有则以自己的为准，覆盖继承）。

### R3 — 序号不变量不变

继承**不写新的 release 行、不消耗 evidence**。因此「`released` 最大序号 == `evidence` 行数」这条不变量原样成立，`hooks/task recover` 与 `unaided` 的越界检查都不受影响。

### R4 — 拒绝提示说清楚

若某阶段既无本版本记录、也无可继承的上一版本记录，`approve` 的拒绝消息说明这一点，而不是笼统说「从未被门释放」。

### R5 — 门（`capability-gate`）**不**继承

原本要求门也继承。实测后否掉：门管的是**同一版本内逐阶段消耗**（`cg_verdict spec.md deny`——一次调用不能服务两个阶段），继承会直接破坏它。`released` 里没有「这个版本刚被提升」的信息，门无从区分「新版本」与「同版本第二个文档」。

所以分工明确：**门保留原语义，`approve` 负责继承**。升版本后写第一个被改动的文档仍要一次真实调用或一次申报，但 `approve` 不再要求 N 次。

## Acceptance Criteria

- **A1**：探针场景复现——v1 申报四个阶段并 approve，升到 v2 后**不申报任何阶段**，`approve` 直接通过，且 `evidence` 行数不增。
- **A2**：v2 若某阶段有自己的新记录，用新的，不用继承的（不被旧记录覆盖）。
- **A3**：v2 若某阶段既无新记录也无旧记录，`approve` 拒绝，消息点名该阶段并说明两种补救。
- **A4**：整个过程中 `evidence` 行数与 `released` 最大序号保持相等（R3 不变量）。
- **A5**：`bash hooks/smoke-test` 全绿，新增断言覆盖 A1–A4。
- **A6**：变异验证——删掉继承逻辑，A1 变红；去掉版本上限，辅助函数断言变红。

## External Facts

- Depends on external facts: no
- Why not: 结论全部来自 `hooks/task`、`hooks/capability-gate`、`hooks/task recover` 的代码与 2026-11-03 的探针实测。

## In Scope

- `hooks/task` 的 `approve`：阶段核对加入继承。
- `hooks/smoke-test`：新断言。
- 本任务的两份核心文档。

## Out of Scope

- 改变序号的分配方式或 `released` / `evidence` 的文件格式。
- 让继承跨任务（只继承**同一任务**的更低版本）。
- `TF-20261009-8abbd6`（阶段选择与工具流解耦）。

## Risks / Deferred Items

- **R1 风险**：继承会造成「旧版本花的调用被新版本反复使用」。这是有意的——版本提升不重跑阶段——但要在文档里写明，否则下一个人会以为这是漏洞。缓解：`approve` 输出里注明哪些阶段是继承来的。
- **R2 风险**：`recover` 丢弃记录后，继承链可能断裂。继承按「存在的记录」判断，缺失即要求重新申报，方向安全。
- **接受的残留成本**：升版本后第一次写某个文档时，门仍要求一次真实调用或一次 `unaided` 申报（R5）。这不是重复申报——那是每阶段一次，这是「被改动的文档」一次。
- **Deferred**：把「哪个阶段变了才需要重记」做成显式声明，属更进一步的设计。
