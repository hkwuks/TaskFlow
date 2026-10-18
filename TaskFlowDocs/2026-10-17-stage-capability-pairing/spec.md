# Spec — Pair a release to the capability its phase reported

> Task version: v1

## Objective and Success Criteria

把 `hooks/task approve` 对 invoke 形状 stage 行的校验域，从**单一 release 行**（按 (version, stage) 配对）扩到**本版本的 release 记录集合**，使如实填写的 `## Skills / Tools Used` 能通过，而凭空写出的能力名仍被拒。判据域扩大一格，判据本身（「这个名字被记录过」）保留。

成功判据即 PRD A1–A7；核心是 A1 与 A2 能在**同一份** `released` 上同时成立。

## Architecture Boundaries and Responsibilities

涉及四个层次，各自职责不变：

| 层 | 文件 | 本次是否改行为 |
| --- | --- | --- |
| 记录 | `hooks/capability-evidence` | 否 |
| 释放 | `hooks/capability-gate` | 否（只改注释） |
| 声明释放 | `hooks/task`（`unaided` 分支） | 否 |
| 对账 | `hooks/task`（`approve` 分支） | **是，唯一行为改动** |

边界：`hooks/task` 的 `approve` 之前只读 `released` 里与 (version, stage) 相符的那一行；改动后对 invoke 情形额外读**同版本**的其他行。它仍然不写任何 store 文件，仍然在写入任何 Approval 字段之前 fail closed。

`hooks/` 下的 hook 不随 `version` 命令回滚（store 在 git dir 里，`version` 只搬文档）；本次不改这一点。

## Project Structure / Affected Files

- `hooks/task` — `require_stage()` 内 invoke 分支（`hooks/task:1112-1118`）与紧邻注释；`approve` 的段首注释（`:1055-1069`）。
- `hooks/smoke-test` — `== task approve records the five-field block ==` 一节（起始 `smoke-test:1088`）内，改写 1 条断言、新增 3 条夹具（如实错配通过 / 未释放的名字不背书 / 从未记录的名字仍拒）。
- `skills/taskflow/SKILL.md:177`；`skills/taskflow/references/artifacts.md:127` 与 `:129`；`hooks/README.md:197-201`；`hooks/capability-gate:126-142, 146-152`（注释）；`hooks/task:1055-1069`（注释）。
- `TaskFlowDocs/todo.md` — `TF-20261012-c66ad3` 条目。

## Interfaces, Data Flow, and Contracts

### 存储契约（不改）

```
<absolute-git-dir>/taskflow/evidence   ← capability-evidence 追加，一行一次调用
  <kind>|<capability>

<absolute-git-dir>/taskflow/released   ← 门与 unaided 追加，一行一次释放
  <version>|<stage>|<seq>|<kind>|<capability>
```

### 门选择的不是「该阶段的记录」，而是「队列的下一条」

```
consumed := max(released[*].seq)          # 0 若无文件
total    := 行数(evidence)
if total > consumed:
    next := consumed + 1
    record := evidence 的第 next 行         # 位点，不是阶段
    append released: version|stage|next|record.kind|record.capability
```

**这是一个已定的、不由本次改动的契约**。「每条记录只被释放一次」成立（`seq` 全局唯一）；「每条释放归因到记录来源的那个阶段」**不成立**，且不可由现有事件恢复——`capability-evidence` 的 `PostToolUse` 事件不含阶段信息。

### approve 的对账契约（本次唯一改动点）

对每个必需阶段（`PRD`、`Plan`，以及存在 `spec.md` 时的 `Spec`）：

1. 取该阶段在 `released` 里 (version, stage) 相符的行，仍称为**该阶段的记录**。取不到 → `was never released by the pre-write gate`（不变）。
2. 取该行第 4、5 字段为 `kind` 与 `capability`（不变）。
3. 取 `## Skills / Tools Used` 里该阶段的第一条 `- [Stage] ` 行（不变）。
4. 分支：
   - **含 `Unaided`**：要求 `kind == unaided`；要求行内含 `considered:`；要求行内 `-F` 出现记录的 `capability`（即类名）。**三条全不变**。
   - **否则（invoke 形状）**：
     - 要求 `kind == invoke`（**不变**——用 invoke 名义冒领一次 unaided 声明仍被拒）。
     - **判据由「行内出现该阶段记录的 capability」改为「行内出现 `released` 中任一 `kind == invoke` 行的 capability」，域限定在 `$1 == 该版本的 approved_version`。** 该集合记为**池**。
     - 池为空（本版本只有 `unaided` 记录）时，invoke 形状的 bullet **必拒**——不是通过。
     - **池取自 `released`，不取自 `evidence`。** 这是有意的：仍在队列里、尚未被任何阶段释放的记录**不在池中**。实测后果见下方 I9 与 PRD Risks ①。

第 4 条的后半句是本 Spec 的唯一新增语义。其余每一行都是「不变」。

## Invariants and Compatibility

- **I1** 每个必需阶段仍必须有 (version, stage) 相符的 release 行。放宽的是**名字**的出处，不是**记录的存在**。
- **I2** 用 invoke 名义冒领 unaided 声明仍不可能：`kind` 一字不改。
- **I3** Unaided 类名的逐字相等仍成立（那一侧的归因是真的）。
- **I4** 放宽后的判据只在**同一 `version`** 内成立；跨版本不可借（沿用既有 `$1 == v` 过滤）。**注意 `v` 是释放那一刻从 `plan.md` 读到的标签，不是调用发生的时刻**，所以一次 `version` 提升之前发生的调用，会在提升后以旧标签留在 `released` 里——池按标签过滤，不按时刻。
- **I5** approve 仍不写任何 store 文件，仍在写 Approval 之前 fail closed。
- **I6** 无解释器不变量：新代码只用 `awk`、`grep`、`tr`、`echo`。
- **I7** 反斜杠安全：新代码不得用 `awk -v` 传路径或能力名；沿用本文件做法，值走 `ENVIRON`。
- **I8** store 格式、`seq` 算法、`unaided` 两个写入点、门的选择规则：均不变；已存在的 `released`/`evidence` 文件无需迁移。
- **I9** 池只含**已释放**的记录，不含仍在 `evidence` 尾部未消费的。这条以前后顺序可实测：一条在 `prd.md` 之后调用、尚未被释放的记录**不**能背书 `[PRD]` 的 bullet；它被某个后续阶段释放之后才能。（由 Step 3 的对抗性检查指出，本人在放宽后的副本上复现并确认方向是更严而非更松。）
- **I10** 池为空的两种输入都必须安全：`released` 文件不存在 / 只有非 `invoke` 行 → 得空池 → invoke 形状的 bullet 被拒；不得因 `awk` 读不存在的文件而在 `set -e` 下中止。

## Validation and Error Semantics

- 失败仍用 `fail`（stderr + exit 1），仍**在写入任何 Approval 字段之前**。
- 既有消息文案保留；唯一改动的消息是 A2 的新情形。原 `does not name the recorded capability (<cap>)` 在放宽后不再可能由「名字属于别的阶段」触发，因此该文案在新情形下改为点名「本版本记录过的能力」这一要求。**改动这条文案会移动一条既有断言**（`smoke-test:1187`），必须同步，并在该节注释里写明这是有意的行为变更。
- 新增的拒绝消息必须自解释：点名阶段、点名 bullet 里写的名字、说明要求是「本版本被调用过」。

## Code and Test Constraints

- bash 3.2 + BSD userland 下限：不得 `declare -A`、`mapfile`、GNU-only `sed -i`、`grep -P`、`$'…'`、`<<<`。
- Launcher 形态不变（无扩展名、`#!/usr/bin/env bash`、`set -euo pipefail`）。
- 测试纪律沿用 `smoke-test` 该节既有夹具（`ap` / `ap_large` 两棵 worktree），不新建夹具仓库。
- **池判据只贴在 invoke 分支上**：Step 3 的对抗性检查实测，把池也贴到 Unaided 分支会让既有通过用例在两处变红（`smoke-test:1278-1279`），因为 `considered:` 的语义是逐字相等。这不是风格问题，是 I3。
- **不能靠 `< <(…)` / `<<<` 传池**：`$'…'`、`<<<`、进程替换都超出下限；用单引号 heredoc 逐行喂 `while IFS= read -r`。
- 变异验证一次一个，跑前 `pkill -9 -f hooks/smoke-test`，跑时 `< /dev/null`。

## Design Decisions and Alternatives

**D1（用户 2026-10-12 定）：放宽 approve 的判据域，而不是改记账格式。**
替代方案是让释放记录阶段窗口（一条 release 记多条能力，或加计数字段），approve 改判「bullet 的名字属于该阶段窗口」。归因更真，但要改 `released` 的行格式与两个写入点，且已存在的 store 文件需要迁移策略。用户选不改格式。

**D2（用户 2026-10-12 定）：接受溢出，文档写明不归因。**
替代方案是一个阶段一次花完窗口内所有记录（溢出消失，但改消费规则），或把多出的记录标为已花（会改变「先多调几次再写文档」这一正常用法）。用户选接受，并把「账本不按阶段归因」写进文档。

**D3：Unaided 一侧不动，两侧强度**故意**不同。**
类名由 Agent 在 `unaided` 那一刻输入，并被**同一条命令**写进记录，所以「记录里的类名」与「输入过的类名」是同一件事，逐字相等是真的约束。invoke 一侧没有这个性质（`capability-evidence` 不知道阶段），所以它只能判到「本版本被释放过」，Spec 明写这一点以免后人「统一」掉它。

**D4：不引入「阶段窗口」概念。**
门已经知道阶段（它读文件的 basename），本可以让释放带上窗口信息。但那要改 `released` 格式（D1 已否），且窗口边界在「同一阶段写第二个文档」时没有定义。不做。

## Open Questions

无。三个方向性决定已由用户在 2026-10-12 与 2026-10-17 裁定（D1、D2 与任务范围）。
