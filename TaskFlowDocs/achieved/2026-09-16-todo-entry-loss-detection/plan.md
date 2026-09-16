# Plan — Detect a Todo entry a merge dropped
> Task version: v1
> Status: completed

No spec required — one new read-only hook plus its smoke section.

## Reference Pointers

- `hooks/release-check`、`hooks/repository-check` — 只读检查的输出形状与退出码范式（`Repository:` / `- ` 明细 / `STATUS: ...`）。
- `hooks/merge-todo`（头部 9-28 行）— 它写下的「Todo 条目不删除、标题不改写」这条承诺，就是本检查要执行的不变量。
- `hooks/smoke-test` 的 `== todo merge driver ... ==` 几节 — 真实 Git fixture 的写法（`git init` + 分支 + 合并），本任务的 fixture 照此形状。

## Related Tasks

- Depends on: None
- Related: `TaskFlowDocs/2026-09-16-web-ui-merge-loss-guard/`（本任务的 CI 接线与合并路径保护，独立验收标准，另立任务）、`TaskFlowDocs/achieved/2026-09-15-todo-merge-driver/`（同一条问题线的前一个任务；它的 Follow-ups 里「web UI 合并是唯一结构性缺口」的记录是本任务线的来源）

## Skills / Tools Used

Unaided — no capability applied to the PRD or Plan phase; considered: `superpowers:brainstorming` / `addy-agent-skills:idea-refine` and `interview-me` for requirements framing, `superpowers:writing-plans` / `addy-agent-skills:planning-and-task-breakdown` for the Plan. All were judged unnecessary: the requirement and its evidence were established by direct reproduction in the repository (three-way conflict inputs, blob identity between the two merge parents, and a full `git rev-list --all` sweep), not by elicitation, and the Plan is one new read-only hook plus its assertions.

`docker` (`bash:3.2`) — purpose: confirm the new hook parses and runs under stock macOS bash; outcome: succeeded; incorporated: `bash -n` passes for `hooks/todo-check` and `hooks/smoke-test`.

## Preconditions

- [x] 适用仓库文档已读：`CONTRIBUTING.md`（分支前缀与 PR 规则）、`CODE_STYLE.md`（退出码与「检查默认只读」）、`.github/pull_request_template.md`。
- [x] 分支：`fix/todo-entry-loss-detection`，基于 `main`。
- [x] 远程基线：`origin` 即 `hkwuks/TaskFlow`，目标 `main`；非 fork。
- [x] 本任务不新建治理文档。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-16 23:05 +0800
- Approved version: v1
- Approved scope: PRD / Plan v1 —— 新增只读的 `hooks/todo-check` 及其 smoke 断言。用户回复「先做A」即批准本任务的 v1 方案。

## Steps

### Step 1 — 新增 `hooks/todo-check`

- Goal: 用一条只读命令回答「这次提交有没有让某个父提交持有的 Todo 条目消失」。
- Dependencies: 无。
- Files: `hooks/todo-check`（新）、`hooks/smoke-test`、`hooks/README.md`、`skills/taskflow/references/runtime.md`。
- Implementation checklist:
  - [x] `hooks/todo-check [root] [commit]`：解析 root（默认 `git rev-parse --show-toplevel`）与 commit（默认 `HEAD`）；非 Git 目录或 commit 不可解析 → `STATUS: blocked` 退出 `3`。
  - [x] 取 `git rev-list --parents -n1 <commit>`；父提交少于两个 → `STATUS: pass`。
  - [x] 对每个父提交：取 `git show <parent>:TaskFlowDocs/todo.md` 的 `- ID:` 值；文件不存在则跳过该父提交。与 `git show <commit>:TaskFlowDocs/todo.md` 的同集合求差；有差即列出 `- <id> present in <parent> but missing from <commit>`。
  - [x] 有差 → 末行 `STATUS: needs-user-input`，退出 `2`；否则 `STATUS: pass`。
  - [x] 纯 bash 3.2 + POSIX 工具；不写文件；不自动恢复条目。
  - [x] smoke 新增一节：干净的非合并提交通过（含手工删条目也算有意编辑）；人造合并丢掉一条 → 退出 `2` 且输出指名该 ID；坏的 commit → `3`；非 Git 目录 → `3`；父提交无 `todo.md` → 跳过并通过。
  - [x] 两个 hook 清单补上 `todo-check`。
- Acceptance: 新增断言在真实 Git fixture 上通过；对 `77c25dd` 形态的输入退出 `2` 并指名丢失的 ID。
- Verification: `bash hooks/todo-check .` 在当前 `HEAD` 退出 `0`；对 `931c651`/`77c25dd` 形态的 fixture 退出 `2`；`bash hooks/smoke-test` 全绿；新增断言逐条 mutation 验证。
- Rollback: 删除 `hooks/todo-check` 与 smoke 一节；无其他文件受影响。
- Status: done

## Checkpoints

- 新增断言必须逐条 mutation 验证（把实现改坏 → 断言变红），否则新检查可能只是恒真。
- 这是新增的只读命令，不接任何自动流程，不改任何既有 hook 的行为。

## Verification / Review

- `bash hooks/todo-check . 1905984` → 退出 `2`，指名 `TF-20260915-01 present in 931c651… but missing from 1905984…`；这是历史上真正丢条目的那个合并提交（PR #17）。`bash hooks/todo-check . 77c25dd` → 同样退出 `2`，指名同一条与 `931c651`，即内层那次平台侧取舍。
- `bash hooks/todo-check .`（当前 `HEAD` = `f1208a4`）→ `STATUS: pass` 退出 `0`；两个父提交的条目都在。
- 全历史复核：`git rev-list --merges --all` 的 41 个合并提交逐个跑，只有 `1905984` 与 `77c25dd` 报出（同一条 `TF-20260915-01`），误报为零。
- `bash hooks/smoke-test` → `ALL SMOKE PASSED`（30 个 `ok`，新增 `== todo-check reports an entry a merge dropped ==` 一节）。
- mutation 验证（把实现改坏 → 新断言变红），逐条实际执行：
  - `comm -13` 的比较结果置空 → `FAIL dropped entry exit code: 0`。
  - 检测到丢失后的 `exit 2` 改成 `exit 0` → `FAIL dropped entry exit code: 0`。
  - 去掉「非合并提交直接通过」的守卫 → `FAIL hand-deleted entry in a plain commit rejected (2)`（该守卫原先无断言覆盖，为此补了一条「手工删条目属有意编辑」的用例）。
  - 去掉「父提交没有 todo.md 则跳过」→ `FAIL parent without a Todo file not reported as skipped`。
  - `commit` 不可解析时的 `blocked`/`exit 3` 改成 `pass`/`exit 0` → `FAIL unresolvable commit exit code: 0`。
  - 把 `comm -13` 反向写成 `comm -23` → `FAIL dropped entry not named with its parent`。
- 其它检查：`git diff --check` 干净；`python3 evals/runner.py` → `PASS (6 evals)`；`quick_validate.py skills/taskflow` → `Skill is valid!`；`bash hooks/release-check .` → `STATUS: pass`；全部 hook 在 `docker run --rm -v "$PWD":/w -w /w bash:3.2 bash -n` 下解析通过。
- 未跑：`hooks/smoke-test-windows.ps1`（本机无 PowerShell），由推送后的 CI `smoke` job 覆盖；`hooks/todo-check` 是新增脚本，未接任何自动流程，Windows 侧不新增对应实现（它不参与生命周期）。
- 顺带修一处会挡住 `git diff --check` 的既有缺陷：`hooks/task` 生成标题时按 80 字符截断，截在空格上会留下行尾空格（`## Make the Todo merge protection hold on the path where merges actually happen: a `），已去掉该行尾空格；截断逻辑本身未改。

## Change Log

- 2026-09-16 work revision — 新增 `hooks/todo-check` 与 smoke 一节；两个 hook 清单同步；按 PRD 的 R1-R6 实现，未偏离方案。实现过程中发现两处需要偏离 Checklist 措辞的细节，均属同一方案内的实现选择：(1) 判定「丢失」用 `comm -13`（父有而结果无），只在合并提交上做，非合并提交直接通过；(2) 缺失 `TaskFlowDocs/todo.md` 的父提交按「跳过」处理而非「判为丢失」。另清掉 `TaskFlowDocs/todo.md` 一处由 `hooks/task` 标题截断产生的行尾空格。

## Follow-ups

- `hooks/task` 生成标题时 `substr(t, 1, 80)` 的截断会切在词中间，也可能落在空格上留下行尾空格（本轮手工清了一处）。是否在截断后再 `rtrim` 并避免半个单词，留给后续任务；本任务不改 `hooks/task`。
- `TaskFlowDocs/achieved/2026-09-10-repository-document-placement/` 在全部历史里从未有过对应 Todo 条目（随 `660679a feat: release TaskFlow 1.0.2` 进入）。与本任务的缺口无关，未处理。

## Version History

- v1 — approved, implemented, and verified; acceptance evidence in `## Verification / Review`.
