# Plan — 让能力库失步后可以真正恢复，而不是只有删库重来
> Task version: v1
> Status: completed

No spec required — the PRD's R1–R6 fix the contract; the change is one subcommand plus two messages.

## Reference Pointers

- `hooks/capability-gate:139-162` — 释放条件 `total > consumed`，以及 1.1.8 新增的失步分支
- `hooks/task:1115-1190` — `unaided` 的两行写入与它已有的失步拒绝
- `hooks/task:1249` — `approve` 只读 `released`
- `skills/taskflow/references/runtime.md:61-67` — 库的定义、三个写者、不变量
- `hooks/smoke-test:2804-2865` — 1.1.8 的失步断言，本任务在同一夹具上扩展
- `TaskFlowDocs/achieved/2026-10-25-gate-desync-diagnosis/plan.md` — 那条任务留下的三个撤回结论

## Related Tasks

- `TF-20261025-537a8a`（已完成，1.1.8）— 让门说出真实原因。本任务是它的续集：那条只改诊断，本条补恢复。
- `TF-20261012-c66ad3`（inbox）— 版本提升重复记账。**不合并**：它动的是键的选择，本条动的是损坏后的恢复。
- `TF-20261025-645ef4`（inbox）— Windows 套件 throw 挂起，可能妨碍 A8 的本地验证。

## Skills / Tools Used

- [PRD] `agent-skills:api-and-interface-design` — purpose: 定 `recover` 的退出码与幂等契约；outcome: `succeeded`；incorporated: 干净库、恢复成功、库不存在三者都退出 0，因为对使用者而言都是「现在可以继续」；非 0 只保留「库存在但不可读写」一种。
- [Spec] `Unaided — no capability applied to this phase; considered: architecture and design` — 这条 spec 记录的是本条自己新定的接口形状（退出码表、I1–I4、`K` 是行数不是缺口），没有哪个设计类能力会产出它：它描述的是刚被这条任务定下来的东西。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 把恢复口径拆成可验证的 Step；outcome: `succeeded`；incorporated: 先证明「删行后 `approve` 行为符合预期」再写码——那是本条唯一的正确性依据，写码之后再发现口径错了，改的是实现而不是假设。
- [Test] `Unaided — no capability applied to this phase; considered: testing strategy` — the assertions follow the shapes already in `hooks/smoke-test`: a fixture store built by `printf`, the command run against `--root`, and the resulting file compared byte for byte. No capability would have supplied that shape, and the three properties under test (keeps backed rows, no-op when healthy, idempotent) are checked by comparison rather than by assertion, which is what an invocation would have had to invent.

## Preconditions

- 工作树 `.worktrees/capability-store-recover`，分支 `fix/capability-store-recover`，基线 `4a2b407`。
- `main` 上 1.1.8 已发布，门已有失步分支。
- 并行任务 `untrack-sessions` 只动 `achieved/` 下的文件与 CHANGELOG，不碰 `hooks/task`、`hooks/capability-gate`、`hooks/smoke-test`。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-25 23:16 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 先证明恢复口径成立，再写码

- Goal: 在动手前用一次性的探针确认「删掉 `released` 里 `seq > total` 的行后，`approve` 对剩余阶段仍然放行、被删阶段要求重新声明」。若这条不成立，R1 的整个前提就错了。
- Dependencies: 无。
- Files: 无（探针在 `/tmp` 的夹具仓库里跑，不碰本仓库）。
- Implementation checklist:
  - [x] 造夹具：`released` 含 `v1|PRD|1`、`v1|Spec|2`、`v1|Plan|5`，`evidence` 3 行；plan.md 写 `> Task version: v1` 且 `## Skills / Tools Used` 有三行。
  - [x] 记录恢复前 `approve` 的输出（预期：拒绝，指名 `[Plan]`）。
  - [x] 手工把 `released` 截到 seq ≤ 3，再跑 `approve`（预期：PRD/Spec 通过、Plan 仍拒绝）。
  - [x] 把结果写进本 Step 的 Verification。
- Acceptance: 两次 `approve` 的差异恰好落在被丢弃的那一行对应的阶段上，其余不变。
- Verification: 已在批准前跑过（`/tmp/recprobe/repo` 一次性夹具，2026-10-25）。**结果与预期相反的一半必须记下来**：
  - `released` seq 1,2,4 / `evidence` 3 行时：`approve` 输出 `stages released by the gate: 3 invoked, 0 unaided` + `approve OK: 2026-01-01-rec (user, v1)`。它没查 seq 4 背后有没有记录。
  - 把 seq 4 那行删掉后：`approve blocked: stage [Test] was never released by the pre-write gate.`
  - 同一个库、同一份文档，批与不批只差一行无凭据的释放记录。**这就是 R7 的来源**，也是 Step 2 必须先改 `approve` 的原因：不改它，`recover` 修好的库在批准这一侧仍然可以蒙混。
  - 同时确认了两件预期内的事：门的失步分支正常触发；`unaided` 正常拒绝（且 `fail` 打印消息但退出码是 0，这是既有的 `fail` 实现，不在本条范围）。
- Rollback: 无（一次性夹具，`/tmp/recprobe` 可随时删）。
- Status: done

### Step 2 — `approve` 先拒绝失步的库（R7）

- Goal: 在任何 Approval 字段写入之前，`approve` 做与 `unaided` 相同的 `consumed <= total` 检查并 fail closed，指名 `recover`。
- Dependencies: Step 1（它证明了这个检查缺失）。
- Files: `hooks/task`
- Implementation checklist:
  - [x] 在 `approve)` 分支里、`cap_released="$(git -C "$root" rev-parse --absolute-git-dir ...)/taskflow/released"` 之后立刻插入检查，**在 `cap_skills` 读取之前**（越早越好，不能等到写字段时才拦）。
  - [x] `consumed` 与 `total` 的算法与门、`unaided` 逐字相同（同一个 awk），这样三处对照时不会出现第四个口径。
  - [x] 文案与 `unaided` 的失步 `fail` 同形，并把 `bash hooks/task recover` 放在最前。
  - [x] 不改变 `approve` 其余任何判定：`require_stage` 的三处 fail、`cap_size`、`cap_pool` 全部原样。
- Acceptance: A9。
- Verification: Step 1 的夹具上重跑，期望从 `approve OK` 变成拒绝；删行后再跑，期望 `approve OK`。
- Rollback: `git checkout -- hooks/task`。
- Status: done

### Step 3 — 实现 `hooks/task recover`

- Goal: R1–R4。
- Dependencies: Step 1 的结论、Step 2 的位置（同一个文件，同一个分支）。
- Files: `hooks/task`
- Implementation checklist:
  - [x] usage 行加入 `recover`（`hooks/task:606`）。
  - [x] 新增 `recover)` 分支，紧跟 `unaided)` 之后：
    - `split_root "$@"`，`git_dir="$(git -C "$root" rev-parse --absolute-git-dir 2>/dev/null)"`；失败 fail 并说明。
    - `store="$git_dir/taskflow"`；目录或 `released` 不存在 → 打印 `recover OK: no capability store at <store>, nothing to repair`，exit 0。
    - `total="$(awk 'END{print NR}' "$evidence" 2>/dev/null || echo 0)"`（`evidence` 不存在时为 0）。
    - `consumed` = `released` 最大 seq（与两个写者逐字相同的 awk，便于对照）。
    - `[ "$consumed" -le "$total" ]` → 打印 `recover OK: in step (released seq N, M evidence line(s)), nothing to discard`，exit 0，**不创建 `released.discarded`**。
    - 否则：`awk -F'|' -v t="$total" '$3+0 > t+0' "$released" >> "$released.discarded"`，然后 `awk -F'|' -v t="$total" '$3+0 <= t+0' "$released" > "$released.tmp" && mv "$released.tmp" "$released"`；任一步失败 fail 且不改 `released`（先写 tmp 再 mv）。
    - 打印：丢弃行数、恢复后的最大 seq、`evidence` 行数、以及「these stages are unreleased again — declare each with `hooks/task unaided` or invoke a capability for it」。
  - [x] 幂等由「`consumed <= total` 直接返回」保证，不靠内容比较。
- Acceptance: A1–A5。
- Verification: Step 5 的三段断言 + 本文件 Verification / Review 的变异表。
- Rollback: `git checkout -- hooks/task`；`recover` 只在被调用时改文件。
- Status: done

### Step 4 — 把门与 `unaided` 的文案指向 `recover`

- Goal: R5、R6。
- Dependencies: Step 3（命令必须真的存在，文案才能指它）。
- Files: `hooks/capability-gate`、`hooks/task`
- Implementation checklist:
  - [x] 门的失步分支改成三条路：`recover`（保留有凭据的释放）、补齐记录、删库（丢全部）。三者各带代价，不推荐其一。
  - [x] `unaided` 的 `fail` 文案改成同样的形状；它今天只说删库。
  - [x] 两处都保留可复制的 `bash hooks/task unaided <stage> --considered '...'`（它现在是恢复之后的**下一步**，而不是恢复手段）。
  - [x] **不改任何判定条件**：`if [ "$total" -gt "$consumed" ]`、`[ "$consumed" -le "$total" ]` 必须原样。
- Acceptance: A6；`git diff hooks/capability-gate` 里只有消息字符串与注释变化。
- Verification: A6 的断言 + 人工读一次 diff。
- Rollback: `git checkout -- hooks/capability-gate hooks/task`。
- Status: done

### Step 5 — 断言与文档

- Goal: A7、A8 与三处文档同步。
- Dependencies: Step 2、3。
- Files: `hooks/smoke-test`、`hooks/smoke-test-windows.ps1`、`hooks/README.md`、`skills/taskflow/references/runtime.md`、`skills/taskflow/references/artifacts.md`、`CHANGELOG.md`
- Implementation checklist:
  - [x] `hooks/smoke-test`：在 `gds` 夹具之后新增一段。A1（seq 5 / evidence 0 行 → `recover` → `unaided PRD` 成功）、A2（部分失步：`released` 1,2,3,5 + evidence 3 行 → 只剩 1,2,3，`released.discarded` 含 5）、A3（连跑两次，三文件逐字节相同）、A4（干净库不产生 `released.discarded`）、A5（无库 exit 0）。
  - [x] A6 两处文案各一条 `case`。
  - [x] ~~`hooks/smoke-test-windows.ps1`：一条 `recover` 路径（A1）。~~ **未做**：该套件在 launcher 段之后的 `throw` 间歇性挂起（三次里一次 88s 无输出），没有稳定环境就无法把「绿」和「没跑到」分开。记进 Follow-ups，不写成通过。
  - [x] `hooks/README.md`：`task` 那一行的子命令列表加 `recover`。
  - [x] `runtime.md:67`、`runtime.md:78`：把「唯一的恢复是删库」改成两条路并加 `recover`。
  - [x] `artifacts.md`：只改提到恢复的句子（`unaided` 的表格行）。
  - [x] `CHANGELOG.md` `[Unreleased]` → `### Added`（它是一条新命令）。
  - [x] `[Test]` 行写进 `## Skills / Tools Used`。
- Acceptance: A7、A8、`bash hooks/smoke-test` 全绿。
- Verification: `bash hooks/smoke-test`；Windows 套件**未跑**，理由见本节末尾与「未做」。
- Rollback: 各自 `git checkout --`。
- Status: done

## Checkpoints

- 每个 Step 结束：`git diff --check` 干净。
- Step 4 之后：`git diff hooks/capability-gate` 只有字符串与注释变化——这是 R6 的机械判据，比读 diff 可靠。
- Step 2 之后：`git diff hooks/task` 里 `approve)` 分支的改动只有新增的那一段检查，`require_stage` 未被触碰。
- Step 4 之后：全量 `bash hooks/smoke-test` 至少一次，且做一次变异验证（把 `$3+0 <= $t+0` 改成 `$3+0 < $t+0`，A2 必须变红）。

## Change Log

- v1 — planning：PRD 与 Plan 写成，等待批准。
- v2 — 批准后并入两处实测发现（用户裁定「并进 A 任务」）：probe 证明 `approve` 在 `released` seq 4 / `evidence` 3 行时仍然 `approve OK`，删掉那行之后才拒绝——所以「删掉无凭据的行 == 退回未释放」在批准这一侧当时并不成立，补 R7/A9；同轮尝试的另一项（门在 cwd 偏离时说「已花掉」）已撤回，理由记在 PRD 的 R8 一段。Task version 保持 v1 不变：本轮改动落在同一批文件、同一轮批准之内，尚未开始实现，不构成新的交付版本。

## Follow-ups

- `TF-20261025-645ef4` — Windows 套件 throw 挂起，可能使 A8 只能记为「未能本地验证」。
- `TF-20261012-c66ad3` — 版本提升重复记账，本条不解决。

## Version History

- v1 — planning。

## Verification / Review

| 检查 | 结果 |
| --- | --- |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED`（含新增 3 段：recover 三分支、approve 拒绝失步、边界行） |
| `git diff --check` | clean |
| `bash -n hooks/task` / `hooks/capability-gate` | 语法通过 |
| `git diff hooks/capability-gate` | 只有 2 行字符串变化，判定未动（R6 的机械判据） |

**变异验证（6 个，5 个先红后绿，1 个证明不可测）**

| 变异 | 结果 |
| --- | --- |
| `$3+0 > t+0` → `>=`（discard 边界） | 红：discarded a different number of rows |
| `$3+0 <= t+0` → `<`（keep 边界） | 红：did not keep exactly the backed releases |
| 去掉 `approve` 的不变量检查 | 红：accepted a store whose releases outrun its evidence |
| 让 `approve` 在写字段之后才检查 | 红：wrote an Approval field before refusing（隐含在 `- Approved by: pending` 断言） |
| `recover` 的 `consumed <= total` 改成 `<` | 绿（健康库上仍返回 no-op；该分支只决定措辞，不改操作）— **未覆盖**，记为已知缺口 |
| 门的 `stray_evidence` 首句分支改成 `if false` | 绿：不可变异，据此**撤回 R8**（PRD 有记录） |

前两个变异第一次跑是绿的——夹具里没有 `seq == evidence 行数` 那一行，两个比较的边界因此不可观测。补上 seq 3 之后两者都红，这是本轮唯一一次「断言存在但没在测」。

**一处顺带修正**：`discarded` 起初按 `consumed - total` 算，实测发现它只在幸存 release 从 seq 1 连续时才等于行数（seq 1,2,3,5 对 3 行 evidence：缺口 4，实际只丢 1 行）。改成数行，并留了一条夹具专测这个差（seq 1,2,4,7 对 3 行：缺口 4，丢 2 行）。

## CI record

PR [#99](https://github.com/hkwuks/TaskFlow/pull/99)，head `790255c`，run
[40206672910](https://github.com/hkwuks/TaskFlow/actions/runs/40206672910)：**7/7 pass，无 skipped**。

| job | 结果 |
| --- | --- |
| smoke (ubuntu-latest) | pass 21s |
| smoke (macos-latest) | pass 55s |
| **smoke (windows-latest)** | **pass 25s** |
| release / evals / todo-merge-audit / changes | pass |

`smoke (windows-latest)` 这一条要单独说：本任务没有为 `recover` 写 Windows 断言，也没有在本地跑过那个套件
（理由见下）。所以这个 pass 证明的是**既有 Windows 断言在我改完 `hooks/task` 之后仍然通过**，不证明 `recover`
在 Windows 上工作。两者的差别写在 PR 的 Known limitations 里，不在这里抹平。

## 未做

- **Windows 侧断言没有加，也没有本地验证。** 原因不在本条：`hooks/smoke-test-windows.ps1` 在 launcher 段之后的 `throw` 会间歇性挂起（同一次 `throw` 三次里一次挂 88s 无输出、两次 14–18s 正常退出），已经在 `TF-20261025-645ef4`。在没有稳定复现的环境里加一条 PowerShell 断言，我无法把「它绿了」和「它没跑到」区分开，所以不加，也不写成通过。
