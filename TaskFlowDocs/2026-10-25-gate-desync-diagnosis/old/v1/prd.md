# 让 pre-write 门在 store 失步时给出它真正的原因，而不是说错话
> Task version: v1
> Status: in_progress

## Goal

门（`hooks/capability-gate`）在能力账本失步时，说出的原因必须是真实的那一个：今天它把「账本坏了」报告成「刚才那次调用已经被别的文档用掉了」，并因此把人送去一条走不通的路。

## Background / Confirmed Facts

以下都是 2026-10-25 在本仓库实测的。

- **门只按 `consumed` 是否为 0 二分措辞，从不比较 `consumed` 与 `total`。** `hooks/capability-gate:136-139` 从 `released` 取最大 seq 作 `consumed`，`:149-152` 取 `evidence` 的行数作 `total`，`:154` 只在 `total > consumed` 时放行；拒绝分支 `:223-227` 的全部判断是 `if [ "$consumed" -gt 0 ]`。
- **实测：失步时门说的那句话是假的。** 在临时仓库里造出 `released` 有一行 `v1|PRD|5|invoke|a:prd`、`evidence` 为空，门拒绝并说 *the most recent invocation was already spent by an earlier document*。这个 store 里没有任何一行被用掉——根本没有 evidence 行——被「用掉」的 5 个 seq 从来没有对应的记录。
- **实测：门在失步时不是永久卡死，补记录可以「追平」。** 同一个 store，每补一行 evidence，`total` 就逼近 `consumed`；补到第 6 行时 `6 > 5` 成立，门正常释放该阶段。`released` 里那 5 行完好无损，`approve` 只读 `released`，所以追平之后整条流程照常。
- **`unaided` 面对同一个 store 给出的是另一个结论。** `hooks/task:1143-1144` 拒绝并说出两个数字，但它给的恢复方式只有一种：「删掉 `<absolute-git-dir>/taskflow` 重新声明每个阶段」。删掉会连同 `released` 里完好的记录一起丢掉。
- **于是两个写者对同一个 store 说两套话**，一套是「删掉重来」（代价被高估），一套是一句假话（原因被说错）。真情况介于两者之间：记录丢失、`released` 完好、可以追平。

## Requirements

- **R1 —— 门在拒绝前先判断失步。** 进入拒绝分支后先比 `total` 与 `consumed`：`total < consumed` 即失步，走新措辞；否则保持现有二分支。
- **R2 —— 失步的措辞说出两个真实数字与真实原因。** 必须点名 `released` 到达的 seq、`evidence` 实际持有的行数，并明说这是账本失步而不是这个阶段没有调用过能力。
- **R3 —— 失步的措辞给出两条真实可行的恢复路径，并写明代价。**
  - 追平：再产生 `consumed - total + 1` 条能力记录，门即恢复放行，`released` 里的旧记录不丢。这是代价较小的一条，先说。
  - 重建：删掉整个 store 重新声明每个阶段，代价是丢掉 `released` 里的记录。
  - 不能只给一条：`unaided` 只给了第二条，而第一条在本票描述的实测里确实可行。
- **R4 —— 未失步时的两条措辞逐字节不变。** `total == consumed`（队列用尽）仍是 *the most recent invocation was already spent by an earlier document*；`consumed == 0`（空账本）仍是 *no capability invocation is recorded for this task version*。
- **R5 —— `hooks/smoke-test` 断言失步与两种未失步的措辞。** 失步用例要断言两个数字与「不再出现假话」，两条未失步用例断言原文不变。
- **R6 —— `skills/taskflow/references/runtime.md` 的 store 段落补一句：门也会这样诊断。** 那里第 77 行已经写了门在跨工作树时会点名记录去向，本条是同一类「拒绝时说真话」。
- **R7 —— `CHANGELOG.md` 的 `[Unreleased]` 加一条 `### Fixed`。**

## Acceptance Criteria

| # | 可观察条件 |
| --- | --- |
| A1 | 失步 store（`released` 到 seq 5、`evidence` 0 行）上，门的拒绝消息含 `out of step`、`released reaches seq 5`、`evidence holds 0 line`（单复数与 `unaided` 一致），且**不含** *the most recent invocation was already spent* |
| A2 | 同一消息含需要补的记录条数，且该条数与实测一致：照它补足后门在同一条 evidence 到达时放行 |
| A3 | 健康但队列用尽（`total == consumed > 0`）时，消息逐字节等于改动前 |
| A4 | 空账本（`consumed == 0`）时，消息逐字节等于改动前 |
| A5 | `bash hooks/smoke-test`、`bash hooks/release-check .`、`git diff --check` 全绿；CI 7/7 |

## In Scope

- `hooks/capability-gate` —— 拒绝分支增加失步判断与新措辞（约 10 行，含注释）。
- `hooks/smoke-test` —— A1–A4 的断言，放在既有「pre-write gate」小节内，复用它已有的 fixture 风格。
- `skills/taskflow/references/runtime.md` —— R6 的那一句。
- `CHANGELOG.md` —— R7。
- `TaskFlowDocs/todo.md` —— `TF-20261025-537a8a` 的推进与收尾。

## Out of Scope

- **让失步的 store 真正可恢复（`TF-20261025-ef6c18`）。** 本任务只让门把话说对，不改 `evidence` / `released` 的任何写入语义，也不引入重建命令。用户 2026-10-25 明确取了「只修门的诊断」。
- **合并两个 store 文件。** 从结构上消灭失步，代价是改四个 hook 与大量夹具，还要为已存在的 store 写迁移码（需另外授权）。
- **`unaided:1144` 那句话里「The lost records cannot be rebuilt」的措辞。** 它在「删掉重来」这条路上仍然成立；本任务不动它，避免一次改动同时改两个写者的语义。如果读者觉得它与门新增的「追平」路径矛盾，那是 `ef6c18` 的范围。

## Risks / Deferred Items

- **新措辞会把「追平」当成一条推荐路径，而它烧掉的是真实调用。** 一条本来就该发出的调用顺带追平是无害的；为了追平而空转调用则是浪费。措辞只陈述事实与代价，不替读者选。
- **`total < consumed` 只在 store 被外部破坏时出现**（截断、删文件、手工编辑）。`evidence` 与 `released` 都只有本仓库的三个写者会碰，所以这不是一条日常路径，断言也就只覆盖构造出来的失步状态。

## Open Questions

无。范围已由用户 2026-10-25 定。
