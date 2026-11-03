# Plan — Bookkeeping the stage ledger by a globally monotonic evidence queue makes a Task
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/task:44-68` — `rel_max_seq` / `rel_inherit`，继承规则的唯一实现。
- `hooks/task:1630-1645` — `require_stage` 里取记录的位置，继承接在这里。
- `hooks/capability-gate:262-272` — 门的 skip 语义；**保持原样**，理由见 PRD R5。
- `hooks/smoke-test:4045` 起 — 新增的「版本提升继承」一节。

## Related Tasks

## Skills / Tools Used

- [PRD] `agent-skills:spec` — 收敛目标与验收，并核对 R5（门是否也继承）。
- [Spec] Unaided — considered: architecture and design specification。改法由 PRD 的 R1–R5 决定。
- [Plan] Unaided — considered: work breakdown and task decomposition。
- [Test] Unaided — considered: testing strategy。断言写进 `hooks/smoke-test`，含辅助函数的直接断言。

## Preconditions

## Approval

- Status: approved
- Approved by: hk
- Approved at: 2026-11-03 23:00 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — `approve` 的阶段核对接受继承

- Goal: 当前版本无记录时，取本任务该阶段在更低版本中最高的一条。
- Dependencies: 无
- Files: `hooks/task`
- Implementation checklist:
  - [x] `rel_inherit` 辅助函数：按任务、阶段过滤，版本上限为当前版本，取最高。
  - [x] `require_stage` 在自身记录为空时调用它。
  - [x] 继承来的阶段在输出里点名，避免与「本版本有记录」混淆。
  - [x] 拒绝文案说明「也查过更早版本」。
- Acceptance: A1、A2、A3、A4。
- Verification: 端到端探针 + smoke。
- Rollback: `git checkout -- hooks/task`
- Status: done

### Step 2 — smoke 断言

- Goal: 覆盖继承、自身优先、无记录拒绝、不变量不变。
- Dependencies: Step 1
- Files: `hooks/smoke-test`
- Implementation checklist:
  - [x] 完整任务夹具：v1 申报三次并 approve，v2 零申报 approve 通过。
  - [x] 断言继承未写 evidence、未写 release、最高序号仍等于 evidence 行数。
  - [x] v3 自带 PRD 记录时不被继承覆盖（用不同概念类证明）。
  - [x] `rel_inherit` 的版本上限、按阶段、按任务三条直接用辅助函数断言。
  - [x] 任何版本都没释放过的阶段仍被拒绝，文案点名。
- Acceptance: A5、A6。
- Verification: 四个变异全部变红。
- Rollback: `git checkout -- hooks/smoke-test`
- Status: done

### Step 3 — 确认门不继承

- Goal: 验明门若继承会破坏同版本内逐阶段新鲜度，据此把继承限定在 `approve`。
- Dependencies: Step 1
- Files: 无（结论记入 PRD R5）
- Implementation checklist:
  - [x] 给门加继承 → `cg_verdict spec.md deny` 变红，证明破坏逐阶段新鲜度。
  - [x] 回退门的改动，保留在 `approve`。
- Acceptance: PRD R5 与实际代码一致。
- Verification: 门对同版本第二个文档仍拒绝。
- Rollback: 不适用（未落地改动）
- Status: done

## Checkpoints

## Verification / Review

- [x] CI `Hooks` 工作流 three-host 矩阵全绿：smoke ubuntu 25s / windows 1m2s / macos 1m16s，changes 与 todo-merge-audit 通过（run 41663686400，PR #115）
- [x] `bash hooks/smoke-test` 本地全绿（ALL SMOKE PASSED）
- [x] 变异验证：删继承→A1 红；去版本上限→辅助断言红；无记录→拒绝且文案点名
- [x] 端到端：v1 申报四次并 approve，升 v2 后零申报 approve 通过，evidence 仍 4 行

## Change Log

## Follow-ups

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- 2026-10-12 用户报告：某任务的 v13 已获批准，但 `hooks/task approve` 写不进文件。
**用户给的现场**：approve 拒了，理由是 pre-write 门的证据账本**全局单调**——已消费到第 34 条，v12 把可用证据用尽，第 35 条之后再没产生过；`approve` 与 `unaided` 两条路都试过；失败原因已写进该任务的 `plan.md`；用户给的恢复路径是「新会话里做一次 MCP/Skill 调用 + 用 Write/Edit 碰一次 plan.md，门就会释放 v13 的三个阶段」。
**2026-10-18 更正：我在这一点上判错了，用户是对的。** 原文写「按 1.1.5 的码读，做不到」。实测（干净探针：34 条证据全部消费，`evidence > consumed` 为假，门自己已无法释放任何阶段）：连续三次 `hooks/task unaided PRD|Spec|Plan` → `stages released by the gate: 0 invoked, 3 unaided` → `approve OK (user, v13)`。**零工具调用就能恢复**，因为 `hooks/task unaided` 在版本提升后会往 `evidence` **自己追加一行**再写 release 行（`hooks/task:1042-1043`，由 `2026-10-11-gate-host-coverage` 加入）。我漏掉了这条路径，只按门的供给条件（`evidence 行数 > max(seq)`）推，而 `unaided` 不受它限制。用户给的恢复路径（新会话做一次 MCP/Skill 调用）也能用，但**不需要三次真实调用**：一次真实调用释放一个阶段，剩下两个用 `unaided` 声明即可。顺序那半句仍然成立：先补证据再动文档，反了会被门拦下。
**本条的真正缺陷（与「证据用尽」这个现场分开记）**：`seq` 是**全局**计数器，而 `release` 的幂等键是 **(version, stage)**（`capability-gate:126-131`）。两个键不同源，于是任何一次 Task 版本提升都会**要求重新走一遍**，无论旧证据是否还能证明「这个阶段确实调用过能力」——代价是**重复劳动**（每次重走 N 次声明或调用，N = 所需阶段数），不是死锁。用户现场里 v12→v13 只是把版本号从 12 提到 13，需求、阶段、可用能力都没变，却要重新走一遍能力选择——这正是 `TF-20261009-8abbd6`「把阶段的能力选择与宿主工具流解耦」想要消除的那件事，现在多了一个机械版本：**版本提升与证据消耗被同一个全局队列绑死**。
**在「全局单调」这一条上我不认为是缺陷**：它买的是「一个已花掉的调用不能被第二个文档再花一次」（`capability-gate:133-135` 的注释），以及「版本提升不能拿旧版本用剩的证据来满足」。这两件都是真的、且值得。问题只在**它没有与版本提升的语义对齐**（2026-10-18 更正：对齐的缺口的代价是重复劳动，不是「版本提升变死路」——`unaided` 自写 release 行使零调用恢复成为可能）——`approve` 对账的是「本版本每个阶段都有 release 行」，而 release 行的**供给**是全仓库一条队列。
**可核验的机械事实（本次实测 1.1.5，仓库根）**：`git rev-parse --absolute-git-dir` = `.git`，**本仓库根没有证据库**（`.git/taskflow/` 不存在）；六个链接工作树各有自己的库，`evidence`/`consumed` 分别为 4/2、3/2、3/2、2/2、2/2、3/3，即**每一个都处于或接近耗尽**（`evidence > consumed` 才算可释放）。这符合设计（库随工作树分开，见 `capability-gate:160-178`），但也说明「耗尽」在本仓库不是偶发：六个工作树里四个耗尽、两个各只剩 1 条。
**为什么值得单记而不是并入 `TF-20261009-8abbd6`**：8abbd6 要解决的是「宿主没有工具流 / cwd 不在任务工作树」造成的假拒绝，方向是**让阶段选择不必是工具调用的产物**；本条是**记账方式**本身使版本提升变死路，即使宿主有门、cwd 也对，一样会发生。两条的修复面不同（8abbd6 动能力表示层，本条动 `released`/`evidence` 的键或 `approve` 的对账口径）。相关：`TF-20261009-8abbd6`、`TF-20261011-39bda8`（已 done，`unaided` 现在自己写 release 行）。
