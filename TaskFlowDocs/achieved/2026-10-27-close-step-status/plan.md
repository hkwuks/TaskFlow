# Plan — 一个 Step 什么时候算「关闭」
> Task version: v1
> Status: completed

No spec required — small, self-contained task: one `awk` condition in one hook, its assertions, and three doc lines. No cross-layer contract, no new file, no interface change.

## Reference Pointers

- `hooks/completion-gate:67` — 当前的黑名单：`/^- Status: (pending|in_progress|blocked)$/ { unfinished = 1 }`。
- `hooks/completion-gate:59-75` — 一次 `awk` 读完整个 Plan 的既有形状，与 `:22-31` 记的 `pipefail` / SIGPIPE 原因；本任务沿用，不引入管道。
- `hooks/task:449-460` — 写侧定位 Step 的方式（`### Step ` 前缀 + 纯数字 + 数字后不接字母数字下划线），R2 要镜像的就是这一段。
- `hooks/task:1099-1101` — 写侧取值集合 `pending|in_progress|done|blocked`。
- `hooks/smoke-test:33-60` — `cg_case` 辅助函数与 `cg_approved` 夹具，新断言按它加。
- `skills/taskflow/SKILL.md:313` — 待改的黑名单措辞。
- `skills/taskflow/references/runtime.md:244-245` — 同上，两行。
- `TaskFlowDocs/todo.md` → `TF-20261027-131c2b` — 本任务的来源条目与三条已裁定决定。

## Related Tasks

- `TF-20261027-e4ba77`（长实现里保持在场）——同源但不同层：那条改注入节奏，本条改门的判据。本条不依赖它。
- `TF-20261027-e8c6dc`（先问结论是否依赖外部事实）——同批记下的另一条，无依赖。
- `TF-20261027-131c2b` — 本任务。

## Skills / Tools Used

- [PRD] Unaided — no capability applied to this phase; considered: requirements elicitation and framing
- [Plan] Unaided — no capability applied to this phase; considered: work breakdown and task decomposition
- [Test] Unaided — no capability applied to this phase; considered: testing strategy

## Preconditions

- 工作树 `.worktrees/close-step-status`，分支 `fix/close-step-status`，base `main` @ `b47ea3f`。
- `TaskFlowDocs/todo.md` 的未提交改动（三条 2026-10-27 条目）已随本任务进入本工作树。
- 用户已裁定三个岔口（PRD 的 Open Questions）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-27 21:59 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 把门的 unfinished 判定改成块内的白名单，并用断言钉住

- Goal: `hooks/completion-gate` 只在一个 `### Step N` 块里确实写着列首 `- Status: done` 时才认为该块关闭；其余一切算未完成。行为变化只发生在这一处。
- Dependencies: 无（第一步）。
- Files: `hooks/completion-gate`、`hooks/smoke-test`。
- Implementation checklist:
    - [x] 删除 `hooks/completion-gate:67` 的列首黑名单行，改为块内白名单：`### Step <数字>` 处开启块，`## ` 或下一个 `### Step <数字>` 或文件尾关闭块；`END` 时也要结算最后一个块。
    - [x] 块的开启判定镜像 `hooks/task:449-460`：`### Step ` 前缀、纯数字、数字后不接 `[A-Za-z0-9_]`。不按 `## Steps` 段落过滤（PRD 第 5 条）。
    - [x] 关闭的判据只认列首 `- Status: done`，行尾空白容忍（`[[:space:]]` 在 `LC_ALL=C` 下含 `\r`）。一个块里出现多行 `- Status:` 时以最后一行为准，并写进注释。
    - [x] 保持 `unfinished` 的既有输出：`Plan has unfinished Steps`、`exit 1`；`--approval-only` 分支不检查 Step（R4）。
    - [x] 在 `awk` 的注释里写明 R5 的残留：没有 `### Step` 的 Plan 此项通过，这是本规则明确留下的 fail-open，属于另一个问题。
    - [x] `hooks/smoke-test` 在既有 completion-gate 段加 `cg_case`：A1（`done`→0）、A2（`completed`→1）、A3（`complted`/`skipped`/`wip`/`DONE`/`done (v1)`/空值/缺行→1）、A4（三个旧词→1）、A5（一 done 一 completed→1）、A6（`## Approval` 段与 `## Verification / Review` 段下的块，`completed`→1 且 `done`→0）、A7（无 `### Step`→0）、A8（`--approval-only` 对 A2 的 Plan→0），外加补 `\r` 与行尾空白的容忍。
    - [x] 断言里带一句注释，说明 A7 是**故意断言 fail-open**，不是漏写。
- Acceptance: A1–A8 全绿；A4（`pending`/`in_progress`/`blocked` 仍被拒）与既有 `cg_case unfinished` 无回归；A10（既有 completion-gate 断言不改）。
- Verification: 5 次变异全部验证过（记录在 `## Verification / Review`），`bash hooks/smoke-test` `ALL SMOKE PASSED`，`diff` 确认每次改完都按字节还原。
- Rollback: `git checkout -- hooks/completion-gate hooks/smoke-test`（本步不碰其它文件，回滚无连带）。
- Status: done

### Step 2 — 让文档说白名单，并全量验证

- Goal: 三处文档不再描述黑名单；整仓检查通过。
- Dependencies: Step 1（措辞要描述已实现的规则）。
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/runtime.md`、`CHANGELOG.md`。
- Implementation checklist:
    - [x] `SKILL.md:313`：把「no Step still `pending`, `in_progress`, or `blocked`」改成白名单措辞——每个 Step 必须写着 `- Status: done`，其余一律算未完成，并点明这与 `task progress` 只肯写 `done` 是同一条规则的两侧。
    - [x] `runtime.md:244-245`：同义修改，两行都要动（一行描述 `archive`，一行描述 `completion-gate`）。
    - [x] `CHANGELOG.md`：`## [Unreleased]` 下加 `### Fixed` 与 `### Compatibility` 两段——症状（`completed` 在内的七种写法都放行）、根因（黑名单 fail-open）、块定位与写侧一致的理由、R5 的已知残留，以及 5 份归档 Plan 逐条点名不重写。
    - [x] 扫一遍是否还有别处复述黑名单：`grep -rn 'in_progress\`, or \`blocked\|pending, in_progress, or blocked' skills/ hooks/README.md`。
- Acceptance: 三处文档与实现一致；`grep` 不再命中旧措辞。
- Verification: `bash hooks/smoke-test`；`bash hooks/repository-check .`；`bash hooks/release-check .`；`git diff --check`；`python3 <skill-creator>/scripts/quick_validate.py skills/taskflow`。
- Rollback: `git checkout -- skills/ CHANGELOG.md`。
- Status: done

## Checkpoints

- Step 1 之后：`git diff` 只含 `hooks/completion-gate` 与 `hooks/smoke-test`；A1–A8 逐条驱动过一次；至少 A2、A6 各做过一次变异验证（改坏→断言红→改回）。
- Step 2 之后：全量验证四条命令的记录写进 `## Verification / Review`。

## Verification / Review

- **`Hooks` workflow, run [40519266846](https://github.com/hkwuks/TaskFlow/actions/runs/40519266846)** at `f03b806` — **`success`, all seven jobs**: `changes`, `evals`, `release`, `todo-merge-audit`, and `smoke` on `ubuntu-latest` (20s), `windows-latest` (39s) and `macos-latest` (1m7s). Run time 1m25s. CI is the test authority per `CONTRIBUTING.md`, so the new assertions ran on all three hosts rather than only on this one; the local run recorded below was made before CI existed for this branch and stands as the same tree's result.
- 2026-10-27 Step 2: bash hooks/smoke-test ALL SMOKE PASSED; 5 mutations each reddened a named assertion; release-check pass; quick_validate valid; git diff --check clean

2026-10-27，本地（本工作树 `fix/close-step-status`）执行：

- `bash hooks/smoke-test` — `ALL SMOKE PASSED`（含新增的 19 条 completion-gate 断言）。
- `bash hooks/release-check .` — `STATUS: pass`；两侧 marketplace pin 仍是 `v1.1.9 -> 800e7f1…`。
- `bash hooks/repository-check .` — `STATUS: needs-user-input`，三条原因都是本任务进行中的正常状态而不是缺陷：`Base: ambiguous`（新分支尚无 upstream）、`Working tree: has changes`、任务目录未跟踪。`Orphan task directories: none`、`Stale task worktrees: none`。
- `git diff --check` — 干净。
- `quick_validate.py skills/taskflow` — `Skill is valid!`。
- 逐步驱动 `/tmp` 夹具跑过 A1–A8 与四个边界（`### Step 1b` 不算块、`### Step 12` 算块、`
` 尾、行尾空白）。
- **五次变异验证，每次改坏后按字节还原**（`diff -q` 确认）：
    1. 换回旧的黑名单行 → `FAIL completion-gate clean: rc 1 != 0 (Plan has unfinished Steps)`（白名单被删，`done` 的 Step 反而被拒）。
    2. 把块定位限制在 `## Steps` 段内 → `FAIL completion-gate unfinished: rc 0 != 1`；并且单独证实新夹具 `block-outside-steps-section` 在变异下 return 0（应为 1），即它独立捕获了这一变异，不是搭了别的断言的便车。
    3. 删掉 `END` 里的 `flush()` → `FAIL completion-gate unfinished: rc 0 != 1`（最后一个块不被结算）。
    4. 把 `done` 判据收紧成整行精确相等 → 第一轮 `ALL SMOKE PASSED`，**断言没抓住**；补了 `printf` 生成的行尾空白与 `\r` 两条夹具后重跑，`FAIL completion-gate closed-done-trailing-space: rc 1 != 0`。
    5. `done` 判据放宽成 `(done|completed)` → `FAIL completion-gate closed-completed: rc 0 != 1`（正是本任务要消除的那个词）。

第 4 次值得留档：第一版断言只写了字面上的 `done`，于是「容忍行尾空白」这条实现细节根本没有被钉住——变异验证发现了断言的漏洞，不是代码的漏洞。

**回归对照（`git show main:hooks/completion-gate` 对同一个 `achieved/` 跑一遍）**：91 份里 `main` 拒 17 份，改后拒 19 份，**新变化的只有 2 份**——`2026-10-11-gate-host-coverage` 与 `2026-10-22-taskflow-drift-guard`。另外 3 份（`repository-standards-and-doc-root`、`token-efficiency`、`personal-docs-git-boundary`）在 `main` 上就已经因为「current Task version is not approved」被拒，本次改动没有改变它们的判定。`achieved/` 不过门，所以这 2 份在运行时也没有后果；写进 CHANGELOG 的是事实而不是影响。

## Change Log

- 2026-10-27 work revision — 变异验证发现第一版断言没钉住「行尾空白容忍」：实现里 `[[:space:]]` 允许 `done` 后面有空格与 `\r`，但夹具只写了字面的 `done`，把判据收紧成整行精确相等仍然全绿。补了两条用 `printf` 生成字节的夹具（行尾两空格、CRLF）后，同一变异变红。改的是断言，不是行为。
- 2026-10-27 work revision — CHANGELOG 的 Compatibility 段补上回归对照的结论：91 份里 `main` 拒 17、改后拒 19，新变化只有 2 份，其余 3 份在 `main` 上已因别的条件被拒。原措辞只说「5 份算未完成」，会被读成「5 份的判定都变了」。

## Follow-ups

- 「Plan 可以没有 `### Step`」这条残留口径（R5）不在本任务内，若要做需另立条目。
- `2026-10-22-taskflow-drift-guard` 在 `## Verification / Review` 段下复用 `### Step 1` 作普通小标题——写侧本来就把它当 Step，本条只是让读侧与写侧一致；若要禁止这种复用，也另立条目。

## Version History

- v1 — 初版：白名单 `done`、任意 `### Step N`、归档 5 份不动。

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-10-27 measured, and the hole is wider than the two vocabularies.** The two writers disagree — `hooks/task progress` accepts exactly `pending|in_progress|done|blocked` (`hooks/task:1100`) while `hooks/completion-gate:67` treats only `pending|in_progress|blocked` as unfinished — but the real defect is that the gate **fails open on every unrecognized value**. Driven through the gate directly, a Plan whose only Step reads `- Status: complted` / `skipped` / `wip` / empty / a bare `x` returns **exit 0, "finished"**. `completed`, `done (v1)` and `DONE` do the same, so the case that started this item is one instance of a general shape rather than a special one.
  **Real Plans already carry the non-canonical spellings:** over 91 achieved Plans, Step statuses are 254 `done`, 6 `pending`, **4 `completed`** (`2026-10-11-gate-host-coverage`), **3 `done (v1)`** (`2026-09-07-repository-standards-and-doc-root`). Both spellings exist because `task progress` refused the word and the Step was hand-edited instead — the validator and the reader disagreeing is what produced them.
  The choice is a user decision, not a tidy-up: a whitelist would refuse those archived Plans' shapes and is the fail-closed side, while the blacklist is what the gate already is. Whichever wins, `task progress` must move with it, or the next hand edit recreates the split.
