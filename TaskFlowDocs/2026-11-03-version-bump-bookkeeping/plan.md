# Plan — Bookkeeping the stage ledger by a globally monotonic evidence queue makes a Task
> Task version: v1
> Status: planning

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
