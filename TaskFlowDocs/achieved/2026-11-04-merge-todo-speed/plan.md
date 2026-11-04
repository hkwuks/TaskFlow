# Plan — Todo 合并驱动在 125 条目上耗时 180 秒，且中断后静默丢一侧

> Task version: v1
> Status: completed

No spec required — 单文件重写加断言，契约由既有 driver 头部注释与 smoke 节固定。

## Reference Pointers

- `hooks/merge-todo` — 被重写的文件；头部注释是它的对外契约。
- `hooks/smoke-test`（`merge driver` 相关节）— 既有断言，新断言必须与之并列而不是替代。
- `TaskFlowDocs/todo.md` — 真实规模数据，AC1 的基线来源。

## Related Tasks

- 来源：TF-20261104-b1681b。
- 与 `2026-11-04-ci-skip-archive`、`2026-11-04-skip-guard` 无依赖（那两个已合并）。

## Skills / Tools Used

- [PRD] Unaided — considered: requirements elicitation and framing。目标与判据由实测数据直接决定。
- [Plan] Unaided — considered: work breakdown and task decomposition。单文件重写 + 断言。
- [Test] Unaided — considered: testing strategy。沿用 smoke 既有风格，新增计时与失败语义两组。

## Preconditions

- 工作在 `.worktrees/2026-11-04-merge-todo-speed`，分支 `fix/2026-11-04-merge-todo-speed`，基于 `ee6495a`。
- 基线先在旧实现上测出来，再动新实现。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-04 17:41 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 先固定基线

- Goal: 在改动前把旧实现的行为与耗时刻下来，作为 AC1/AC2 的对照。
- Dependencies: 无。
- Files: 无（只产生临时目录下的基线文件）
- Implementation checklist:
  - [x] 取 `eed6fdf` / `35b8151` / `8953f72` 三个版本的 `todo.md` 作为 `%O`/`%A`/`%B`。
  - [x] 在旧实现上跑一次，保存输出为基线，记录耗时。
  - [x] 构造 125 条目的合成 fixture（可复现、不依赖仓库历史），旧实现上测耗时。
- Acceptance: 基线输出与耗时都记进本 Plan。
- Verification: `cmp` 基线稳定（连跑两次一致）。
- Rollback: 无需。
- Status: done

### Step 2 — 单进程重写

- Goal: 切分、索引、匹配都在一个 awk 里完成，输出与原实现逐字节一致。
- Dependencies: Step 1。
- Files: `hooks/merge-todo`
- Implementation checklist:
  - [x] 一个 awk 读三份文件，按 `## ` 切条目，键为 `ID` 首 token、无 ID 时用 heading、`## Removed` 固定为 `head:Removed`。
  - [x] 按原规则决定每条目取哪一侧：只在一侧、两侧相同、仅一侧改动、`## Removed` 并集、两侧都改则冲突标记 + exit 1。
  - [x] 顺序：ours 的顺序在前，只在 theirs 的条目按其在 theirs 中的顺序追加。
  - [x] 输出先写临时文件，最后一次性落地到 `%A`。
  - [x] 只用 POSIX awk 子集。
- Acceptance: 与基线逐字节相同。
- Verification: `cmp` 基线；真实数据计时。
- Rollback: `git checkout -- hooks/merge-todo`。
- Status: done

### Step 3 — 断言

- Goal: smoke 覆盖真实规模、正确性、失败语义。
- Dependencies: Step 2。
- Files: `hooks/smoke-test`
- Implementation checklist:
  - [x] 既有 `merge-todo` 断言全绿（不加改动就应通过）。
  - [x] 新增：构造 125 条目 fixture，断言耗时低于阈值、条目数不变、两侧改动都保留。
  - [x] 新增：一次拒绝运行时 `%A` 未被改坏且退出码非 0。
- Acceptance: AC1–AC5。
- Verification: `bash hooks/smoke-test`（本地跑相关节）；CI 三平台。
- Rollback: `git checkout -- hooks/smoke-test`。
- Status: done

## Checkpoints

- Step 1 的基线必须在 Step 2 之前完成，否则「逐字节一致」没有对照物。
- 阈值由实测决定，不预先写死一个看起来合理的数字。

## Verification / Review

### 基线（改动前，旧实现）

| 输入 | 条目 | 耗时 | 输出 md5 |
| --- | --- | --- | --- |
| 真实三方（`eed6fdf`/`35b8151`/`8953f72`） | 125 | 154 s（复测 176 s） | `18478305dfaa20b63473c2ed8d90684d` |
| 合成不相交 125 条目 | 125 | 227 s | `8fb4d56bffaf0c448872b826b8c05138` |

基线连跑两次逐字节一致，所以它可以作为对照物。

### 改动后

| 输入 | 条目 | 耗时 | 对照 |
| --- | --- | --- | --- |
| 真实三方 | 125 | **1 s** | `cmp` 逐字节相同 |
| 合成不相交 | 125 | **1 s** | `cmp` 逐字节相同 |

**AC1 通过**：两组输出都与基线逐字节相同，不是「看起来差不多」。

**AC2 通过**：1 s，远低于 5 s 目标（断言里写 10 s 预算，给慢机器留余量）。

**AC3 通过**：`merge-todo` 四个既有 smoke 节全绿（keep both / conflict / one-sided / `## Removed`）。

**AC4 通过，判据在实现中改写，理由记录在此。** 原计划用 `timeout` 在 driver 中途杀掉。实测 `timeout 0` 在 Git Bash 上不生效；更要紧的是，「被杀」与「拒绝运行」留下的是同一种证据——`%A` 未改、退出码非零——而两者依赖的都是同一个 write-once 形状。所以断言改为注入一次参数缺失的拒绝，检查的是那个形状本身。这不是放宽判据：形状是唯一能同时覆盖两种中断的东西。

**AC5 — 部分由 CI 承担。** `bash hooks/repository-check .` STATUS: pass；`git diff --check` clean。本机全量 `bash hooks/smoke-test` 仍在 `no interpreter` 节失败（本机 Git Bash 经符号链接调用 bash 时丢 DLL，改动前就在，与本次无关）。新增与既有的 merge-driver 节用隔离运行验证，六节全绿。

### 变异检验

| 变异 | 结果 |
| --- | --- |
| `emit()` 每次调用 `sleep 0.2` | 红：*merge driver took 36s on 125 entries; the budget is 10s* |
| 拒绝路径上截断 `%A` | 红：*a refused run rewrote %A; it must leave Git's content alone* |

两次变异各自只红一条断言；恢复后 `cmp` 确认与改动前逐字节一致。

## Change Log

- v1 — 初始计划。
- Step 1 — 基线固定在临时目录：真实数据与合成数据各一份，两次连跑一致。
- Step 2 — 重写为单 awk 进程。过程中修掉四个实现缺陷，每个都是先红后绿：`k in idx[side]` 是 awk 不实现的切片语法（改用 `SUBSEP` 扁平键）；`FNR==1` 上的 `next` 吞掉每侧第一行（本文件第一行正是 `## Item template`）；`match_of`/`base_of` 给已经带 `head:` 前缀的键又加了一次；`split(v, a, /[ \t]+/)` 在整段记录上会把 ID 后留下 `\n-`，导致墓碑 ID 匹配不上自己的 live 条目。最后一个是既有 smoke 节抓到的，不是新断言。
- Step 3 — 两个新节：125 条目真实规模计时（10 s 预算）与失败时不改 `%A`。计划里的 `timeout` 中断改成拒绝注入，理由见 Verification。

## Follow-ups

- 若 GitHub 网页端合并仍有问题，另开任务（driver 在平台侧不运行，属另一类问题）。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-11-04 实测**。`hooks/merge-todo` 在一份 125 条目的真实 `todo.md` 上跑一次要 **180 秒**（`%O`/`%A`/`%B` 取自 `eed6fdf` / `35b8151` / `8953f72`，即 #117 合并的三方）。同一组输入它**结果是对的**（两侧条目各自取正确的一侧），所以这不是逻辑错误。
  **真正的问题是中断后的行为**：#117 的首次 `git merge` 被 120 秒超时杀掉，driver 写到一半，`%A` 停在「ours」原样；随后清掉 `index.lock` 重跑，那次合并落下的 merge commit 里 `TaskFlowDocs/todo.md` **与 ours 逐字节相同**——一方的结果被静默丢弃，`git merge` 报告成功。取证：`git show 7d9d979:TaskFlowDocs/todo.md` 与 `git show 35b8151:` 的 `cmp` 相同。
  **代价**：main 上 `fa9090` 的 done 被覆盖成 inbox，`af456a` 的 Notes 丢失，靠手工提交 `e110454` 修正。
  **复杂度来源**：`index_side`/`match_of`/`base_of` 每条目一次 `grep -nxF | head -1 | cut -d: -f1` 子进程，125 条目 × 3 侧 → 近千次进程启动。Windows/Git Bash 上每次 ~150ms。
  **要定的方向**：(a) 把三方索引与匹配搬进单个 awk 进程（一次性 split + 内存 dict），去掉逐条目子进程；(b) 保持实现不变，只给 driver 加超时保护与「未完成就走 Git 内置冲突」的显式失败；(c) 两者都做。(a) 是根因，(b) 是安全网。
