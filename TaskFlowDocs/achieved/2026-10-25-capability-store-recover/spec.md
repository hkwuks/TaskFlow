# Spec — 能力库失步后的恢复契约
> Task version: v1
> Status: approved

## Objective and Success Criteria

`hooks/task recover` 的契约在 PRD 的 R1–R6 里定死。本 spec 记录实现选定的接口形状与它依赖的不变量，使后续改动有可对照的书面契约，而不是去读一个 `awk` 表达式。

## Architecture Boundaries and Responsibilities

三个写者与一个新入口的分工不变：

| 角色 | 读 | 写 | 对本条的关系 |
| --- | --- | --- | --- |
| `capability-gate` | `evidence`、`released` | `released`（追加一行） | 判定不动；只有失步消息的措辞把 `recover` 列为第一条路 |
| `hooks/task unaided` | `evidence`、`released` | 两者（各追加一行） | 判定不动；失步时的 `fail` 文案改指 `recover` |
| `hooks/task approve` | `released`、`Plan`、`Todo` | `Plan` 的 Approval 块 | **新增**一条前置检查：`consumed <= total`，不成立即 fail closed |
| `hooks/task recover` | `evidence`、`released` | `released`、`released.discarded` | **新增**；只删除 `seq > total` 的行 |

`recover` 不写 `evidence`，不写 `Plan`，不碰 `Todo`，不调用任何其他 hook。

## Project Structure / Affected Files

```text
hooks/task                          recover 分支 + approve 前置检查 + 两处文案 + usage 行
hooks/capability-gate               失步消息的措辞（判定未动）
hooks/smoke-test                    三段新断言 + 两个既有夹具补 evidence
hooks/README.md                     task 的子命令列表与 Lifecycle 段
skills/taskflow/references/runtime.md   §store 的两处恢复说明
skills/taskflow/references/artifacts.md approve 的失步拒绝
CHANGELOG.md                        [Unreleased]
```

## Interfaces, Data Flow, and Contracts

```text
task recover [--root <path>]
```

| 退出码 | 条件 | 输出 |
| --- | --- | --- |
| 0 | `released` 不存在 | `recover OK: no capability store at <store>, nothing to repair` |
| 0 | `released` 的最大 seq ≤ `evidence` 行数 | `recover OK: in step (released reaches seq N, M evidence line(s)), nothing to discard`；不创建 `released.discarded` |
| 0 | 丢弃了至少一行 | `recover OK: discarded K release line(s) whose record is gone; released now reaches seq N with M evidence line(s)` + 一行「这些阶段要重新声明」 |
| 非 0 | 参数多于 `--root`，或 `released` / `released.discarded` 不可写 | `fail`；**不改变 `released`**（先写 `released.tmp` 再 `mv`） |

**幂等**：第二次运行落入第二行那个分支，因为第一次之后 `consumed ≤ total` 必然成立。不靠内容比较。

**`K` 是行数，不是 `consumed - total`。** 两者只在幸存 release 从 seq 1 连续时相等：seq 1,2,3,5 对 3 行 evidence 的缺口是 2，实际只丢 1 行。实测过这个差，`K` 按行数算。

## Invariants and Compatibility

**I1 — `released` 的最大 seq == `evidence` 行数。** 三个写者都维持它；失步只来自外部损坏。`recover` 是把它恢复回来的唯一入口。

**I2 — `recover` 不新增行。** 它不写 `evidence`，也不写 `released` 的新行。这是它与「编辑账本」的界线：能写 release 的命令会让门失去意义。

**I3 — 被丢弃的行仍在 `released.discarded` 里。** append-only，两次修复不互相覆盖。

**I4 — 丢弃之后，被丢弃阶段退回未释放；其余阶段保持已释放。** 依据是 `approve` 只按 `(version, stage)` 查 `released`。

**兼容性**：`approve` 的新检查会让「失步库 + 已批准文档」从通过变成拒绝。这是**故意**的更严：实测证明不检查时，一行无凭据的 release 足以让一个从未被释放的阶段通过批准。

## Validation and Error Semantics

- 参数面只有一个可选的 `--root`；除它之外的任何参数都是用法错误。**不接受「删哪几行」这种参数**——那会把恢复变成编辑。
- 失败一律 fail closed，且在写入前判定；`released` 的替换是 `tmp` + `mv`，中断不会留下半个文件。
- 门只改字符串：`git diff hooks/capability-gate` 必须是 2 行（一条 `deny` 字符串）。这是 R6 的机械判据。

## Code and Test Constraints

- 只用 POSIX `awk` / `sed` / `mv`，不引入新依赖（仓库既有的 `taskflow-no-python-direction`）。
- 三处序列算法逐字相同，避免出现第四个口径。
- 断言用 `printf` 造库、`--root` 指夹具、`cmp` / 字符串比较判定；不引入测试框架。

## Design Decisions and Alternatives

1. **丢弃无凭据的行，而不是删库。** 删库会连有凭据的释放一起丢。备选「从 achieved 的 Approval 块重建 `released`」被否：Approval 只证明某阶段批过，不证明证据序号，重建出的 seq 是编的。
2. **入口是 `hooks/task recover`，不是新 hook 文件。** `task` 已经拥有 `unaided`、`approve` 这些写库入口，恢复属于同一族；且门的拒绝消息里能给出一行可复制的命令。
3. **不自动调用。** 让 `unaided` 在失步时先修再写，会把账本修改藏进一个声明动作，与它现在明确拒绝的立场相反。
4. **`approve` 必须一起改。** 这是澄清阶段没料到的：probe 显示不改的话，`recover` 修好的库在批准这一侧仍可被一行无记录释放蒙混，而 `recover` 的整个立论就是「删掉无凭据的行 == 退回未释放」。
5. **撤回的一项**：门在 cwd 偏离时说「已花掉」的那句假话。变异验证证明它无法用行为断言覆盖，见 PRD 的 R8。

## Open Questions

无。
