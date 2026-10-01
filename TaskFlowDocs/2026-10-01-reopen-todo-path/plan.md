# Plan — hooks/reopen does not rewrite the Todo Task: path back to the active root, so ta
> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

无独立 `reference/`。判据全部来自仓库自身的实现与既有测试，已写入 `prd.md` 的 Confirmed Facts：

- `hooks/reopen`（43 行，只有 `mv` + Plan Change Log 插入）。
- `hooks/archive:23-121`（预检 / 备份 / 写 / 校验 / 回滚 / stage 行——本次要对齐的纪律）。
- `hooks/task:120-127` `findsec`（字面子串定位条目的谓词）。
- `hooks/smoke-test:519` 的归档 fixture 与 `:645-648` 的 reopen 一节；`:605-643` 用 stub 注入 archive 失败的既有手法。

## Related Tasks

- Depends on: None
- Blocks: None
- Related: `TaskFlowDocs/achieved/2026-10-01-taskflow-commit-path/`（该任务 reopen 时撞上本缺陷，Todo 行被手工修改）；`TaskFlowDocs/achieved/2026-09-15-hook-integrity/`（`archive` 的预检/回滚/校验纪律来自这里）

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — purpose: 用其六要素清单核对 PRD 是否把要求写成可观察结果、失败语义是否写成可测条件；outcome: succeeded；incorporated: 据此把「失败时**不得发生**什么」写成 R3 与 A3/A4 两条可执行的断言（而不是只写「要回滚」），并把「Todo 条目缺失过去能搬、今后被拒」这一行为改变显式记入 Risks，避免它被当成回归。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 用其依赖与「先建地基」的纪律决定这串变更的先后，使回滚要撤销的东西最少；outcome: succeeded；incorporated: 把全部**文件内容**变更（Todo 改回、Plan 插行）排在 `mv` **之前**完成，让 `mv` 成为最后一次改动且只是一次目录改名——回滚于是只剩「撤销一次 `mv` + 还原两份备份」，不必再处理「Plan 已经被改过但目录已经搬走」这种跨位置的半成品状态。校验放在 `mv` 之后、打印之前。

## Preconditions

- [x] Worktree `.worktrees/reopen-todo-path`，分支 `fix/reopen-todo-path`，基于 `main` 的 `35a4071`；**且会话 cwd 已切入该工作树**——`capability-evidence` 按事件 `cwd` 定位证据库与活动任务，会话停在主检出时阶段证据不落盘，门随后拒绝写入（`TF-20261001-efbc51` 记的就是这件事）。
- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded. 适用：`CONTRIBUTING.md`（Checks、§ Where the commit lands）、`CODE_STYLE.md`（Shell 一节：`#!/usr/bin/env bash`、`set -euo pipefail`、引用路径）。不适用：`RELEASE.md`。无冲突。
- [x] For remote/fork/PR work: remotes, target repository, base branch, local branch/base, freshness limits, and required checks recorded. `origin` = `hkwuks/TaskFlow`（非 fork），base `main`，本地分支自 `35a4071` 分出。改动是 hook 与其测试，按 § Where the commit lands 属「hooks」，走 PR；CI `Hooks` 三平台为准。
- [x] For PR creation/update: applicable template path, every required-field mapping, and template verification recorded. 模板 `.github/pull_request_template.md`，Step 3 逐项映射。
- [x] Missing governance drafts and explicit approvals recorded before they become binding. 无缺失治理文档。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-01 13:23 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — Make reopen the inverse of archive

- Goal: `hooks/reopen` 在取回目录的同时把 Todo 改回活动根，并对失败保持 fail closed；变更顺序使回滚只需撤销一次 `mv` 加还原两份备份。
- Dependencies: None
- Files: `hooks/reopen`
- Implementation checklist:
  - [x] 预检扩到四项：`achieved/$task` 存在、活动根不存在、`todo.md` 存在、且 Todo 里能找到 `` `TaskFlowDocs/achieved/$task/` ``；任一不成立即退出非零，**不动目录**。
  - [x] `mktemp` 备份 `todo.md` 与 `$docs/achieved/$task/plan.md` 两份（备份落在 `$docs` 下，不随 `mv` 移动，与 `archive:42` 同法）。
  - [x] 先在**原位置**改 Todo：`Task:` 回 `` `TaskFlowDocs/$task/` ``、`Status:` → `promoted`、`Next action:` → `Re-approve the new Task version before core changes.`、`Updated:` → 当天；其余字段逐字保留。沿用 `archive:55-92` 的按条目定位法（`## ` 段边界 + 子串定位）。
  - [x] 再在**原位置**给 Plan 的 Change Log 插重开行（保留原 awk 与其无 `## Change Log` 时的兜底）。
  - [x] 最后才 `mv` 目录回活动根——这是整串里唯一的目录级改动。
  - [x] 写后校验：活动根存在、`achieved/$task` 不存在、条目能被活动路径找到且三字段正确、Plan 里有 `reopen` 行、且 achieved 拼写不再残留。校验谓词用 `findsec` 的同一子串，不另造判据。
  - [x] 任一步失败：还原 Todo 与 Plan 备份、把目录搬回 `achieved/`、清掉临时文件，退出非零并说明失败在哪一步。
  - [x] 成功后删掉两份备份，打印提交用的 stage 行（`TaskFlowDocs/<task>`、`TaskFlowDocs/achieved/<task>`、`TaskFlowDocs/todo.md`），措辞与 `archive:119-121` 对称；成功提示改为不再让 Agent 去补 Todo。
  - [x] 只写 POSIX sh + awk/sed，不引入解释器；退出码只用 0 与 1（本 hook 无「需要用户输入」路径）。
- Acceptance: A1、A2、A3、A4、A5、A6
- Verification: 本地复刻场景跑正向 / 负向 / 回滚三例（见 Step 3）；`bash -n hooks/reopen` 语法自检。
- Rollback: `git checkout -- hooks/reopen`
- Status: done

### Step 2 — Assert the inverse in the reopen section

- Goal: 把新行为钉进 `hooks/smoke-test` 既有的 reopen 一节，含正向、负向与回滚三例。
- Dependencies: Step 1（断言钉的是最终措辞与行为）
- Files: `hooks/smoke-test`
- Implementation checklist:
  - [x] 正向：在既有的 `:645-649` 之后断言 Todo 条目被改回——整行 `- Task: \`TaskFlowDocs/2026-09-08-smoke/\``、`- Status: promoted`、新的 `- Next action:` 行、`- Updated:`。
  - [x] 端到端：紧接着跑 `bash "$HERE/task" state 2026-09-08-smoke planning --root "$tmp"`，必须成功——这正是旧代码必失败之处（缺陷的直接反面）。
  - [x] 负向：另建一个已归档但 Todo 无条目的 fixture，reopen 必须退出非零、**输出含缺失提示**（断言提示文字，不只断言退出码），且目录仍在 `achieved/`、活动根没有它。
  - [x] 回滚：条目带 achieved 的 `Task:` 行但不带 `- Status:`，使写成功而校验失败；断言 `reopen` 退出非零、**输出含 `FAIL: Todo status not promoted`**（把回滚与「预检就拒绝」区分开），目录仍在 `achieved/`，`todo.md` 与 `plan.md` 的 `digest` 与运行前相同。
  - [x] 不改既有断言、不改该节之外的内容；负向与回滚用各自的临时 fixture，不复用 `2026-09-08-smoke`。
- Acceptance: A3、A4、A5、A7、A8
- Verification: 本地按下方方式跑等价场景；最终判定交 CI。
- Rollback: `git checkout -- hooks/smoke-test`
- Status: done

### Step 3 — Verify, then land by pull request

- Goal: 完成 A1–A8 的验收并按仓库落地规则以 PR 提交。
- Dependencies: Step 1、Step 2
- Files: 无（验收与提交；PR body 依据 `.github/pull_request_template.md`）
- Implementation checklist:
  - [x] 本地复刻场景：在一个临时 root 上走 intake → promote → 补批准 → `state in_progress` → `complete --user-accepted` 得到已归档状态，然后 `hooks/reopen`，逐条核对 A1/A2；再各建一个 fixture 核对 A3/A4（含**反向验证**：把改前的 `reopen` 换回，断言必须失败）。脚本以临时文件交给 `bash`，跑完即删，不落盘、不留在仓库里。
  - [x] `git diff --stat` 复核改动面；`hooks/task`、`hooks/archive`、`skills/**` 零改动（A6）——任务自带 `todo.md` 的字面偏差同前记入 Verification。
  - [x] 两条本地静态检查：`git diff --check`；`bash -n hooks/reopen`。`quick_validate.py` 只适用于 Skill，本次未改 Skill，不跑。
  - [ ] 推分支、开 PR、按模板逐项填字段；smoke 套件整体不在本地重跑，判定以 CI `Hooks` 三平台为准（A7）。
- Acceptance: A1–A8 全部满足；CI `Hooks` 三平台通过。
- Verification: CI run URL 记入本 Plan；PR 模板字段逐项映射。
- Rollback: 丢弃分支即可，`main` 未受影响。
- Status: in_progress

## Checkpoints

- [x] Step 1 后：`bash -n hooks/reopen` 通过；本地三例（正向 / 负向 / 回滚）全绿。
- [x] Step 2 后：本地跑抽取出的测试代码全绿，且反向验证（换回改前 `reopen`）在第一节即失败。
- [ ] Step 3 后：A1–A8 逐条有结论，CI `Hooks` 通过，PR 已开且模板字段完整。

## Verification / Review

- **A1 —— 达成。** 已归档 fixture 经 `reopen` 后，Todo 条目为：`- Task: \`TaskFlowDocs/2026-09-08-smoke/\``、`- Status: promoted`、`- Next action: Re-approve the new Task version before core changes.`、`- Updated: 2026-10-01`；`- ID:` 与 `- Goal:` 逐字未变，`updated` 之外无其他行被改动。
- **A2 —— 达成（缺陷的直接反面）。** 同一场景紧接着 `bash hooks/task state 2026-09-08-smoke planning --root <fixture>` 返回 0；改前版本在此必失败，见「反向验证」。
- **A3 —— 达成。** 负向 fixture（已归档目录存在、`todo.md` 里没有该条目）下 `reopen` 退出非零，输出含 `Todo entry for 2026-09-08-noreopen missing`，目录仍在 `achieved/`、活动根没有它。
- **A4 —— 达成。** 回滚 fixture 的条目带 achieved 的 `Task:` 行但**没有** `- Status:`，于是写成功、校验失败：`reopen` 退出非零，输出含 `FAIL: Todo status not promoted`（断言专门钉这条，以免把「预检就拒绝」误读成「回滚生效」），目录回到 `achieved/`，`todo.md` 与 `plan.md` 的 sha256 与运行前一致。
- **A5 —— 达成。** 既有的三项断言（目录搬回、Plan 有 `reopen` 行）继续通过；另外把紧随其后的 `== version bumps root + archives only changed docs ==` 一节也跑了，确认新增的 `task state … planning` 调用没有破坏后续流程。
- **A6 —— 达成，字面偏差同前。** `git diff --stat` 见下：两个目标文件之外还有本任务自己的 `TaskFlowDocs/todo.md` 与任务目录（本仓库每个任务提交都带着它们）。`hooks/task`、`hooks/archive`、`skills/**` **零改动**，逐条成立。
- **A7 —— 见下。** 判定以 CI `Hooks` 三平台为准。
- **A8 —— 如实记录，见下。**

**未在本地重跑、且如实记为「未跑」的检查**：整段 `bash hooks/smoke-test`。本机 Windows + MSYS 上它在无解释器一节（`:53-117`）中止，而那一节**早于** reopen 一节（`:645`），所以本机根本走不到相关断言。本地跑的是把 `:645-745`（reopen 三节 + 紧随的 version 一节）**抽取出来、配等价 fixture** 执行的**同一份测试代码**——不是另写一套，也不是套件运行结果，两者不得混读。

**反向验证（证明断言抓得住缺陷）**：把 `HEAD:hooks/reopen`（改前版本）换进一份 hooks 副本，同一段抽取代码在第一节即失败于 `FAIL reopen left the Todo at the achieved path`。这几条断言因此不是恒真的。

**本地静态检查**：`bash -n hooks/reopen` 通过；`git diff --check` 干净。

**实现与 Plan 的一处偏离（已改 Plan 文字，非事后改判据）**：Step 2 原写「用 PATH 里必然失败的 `awk` stub 注入回滚」。实现时发现该 stub 会让**预检**里的 `awk` 先失败，于是 reopen 在动任何东西之前就退出——测试会通过，但证明的是「预检拒绝」而不是「回滚生效」，是一条会假绿的测试。改用「条目带 achieved 的 `Task:` 行但不带 `- Status:`」触发**写后校验**失败：这条路径确定、可移植（不依赖 PATH 或宿主），且错误消息能让断言把它与预检区分开。

## Change Log

- 2026-10-01 v1 — 建立 v1：三项决策落为 R1–R8、A1–A8 与三个 Step；变更顺序取「文件内容全改完再 `mv`」，使回滚最小。`affects` `prd.md`、`plan.md`。
- 2026-10-01 v1 — Step 1–2 实现完成：`hooks/reopen` 重写（预检 / 备份 / Todo 改回 / Plan 插行 / `mv` / 校验 / 回滚 / stage 行），`hooks/smoke-test` 的 reopen 一节加上正向、端到端、负向、回滚四组断言。回滚注入手法由 `awk` stub 改为「缺 `- Status:` 触发校验失败」，理由是前者会假绿——Plan 的 Step 2 文字已同步改正。本地抽取运行全绿，反向验证证明断言非常真。`affects` `hooks/reopen`、`hooks/smoke-test`、`plan.md`

## Follow-ups

- 历史上已被 `reopen` 且 Todo 未改回的条目（R8）：本次不扫。若日后发现，用 `hooks/task next <todo-id> ...` 或手工改回即可，不必重开本任务。

## Version History

- v1 — planning.
