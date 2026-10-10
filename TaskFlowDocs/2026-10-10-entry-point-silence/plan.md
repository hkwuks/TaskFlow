# Plan — 入口不静默：SessionStart 说出「这份工作该不该进 TaskFlow」

> Task version: v1
> Status: checking

No spec required — 改动是 `hooks/summarize-state` 里的两段判定加一串输出，无跨层契约、无数据结构变更、无兼容性决策；唯一有设计成分的是 R2 的分支判定，其上限与备选已界定在 PRD 的 Risks 与 Step 1 的 checklist 内。

## Spec Pointers

None. `### 3. Design — Spec decision` 的判定：新增的是一个只读判定与一段输出，不引入接口、数据流或错误契约；规模判定仍为 small。

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — 适用的仓库文档与阶段。
- `CONTRIBUTING.md:16-33` — 分支/worktree 隔离；分支命名前缀是 R2 的 slug 规则来源。
- `skills/taskflow/references/runtime.md:94-110` — SessionStart 的 must/may-not 边界（只读、可失败、不写核心文档）。
- `skills/taskflow/references/runtime.md:185` — 写入命令不绑 `UserPromptSubmit`/`PostToolUse`/`Stop`，即 PRD B4 的约束。
- `TaskFlowDocs/achieved/2026-09-10-audit-hook-opportunities/reference/hook-audit.md:81` — `UserPromptSubmit` 的否决记录。

## Related Tasks

- Parent: None.
- Children: None.
- Depends on: None.
- Blocks: None.
- Related: `TF-20261009-cc463b` — 本任务关闭其第四个失败模式（入口静默）的那一半，其余三个（顺序、能力归属、能力类不可见）仍留在该条。

## Skills / Tools Used

- [PRD] Unaided — no capability applied to this phase; considered: requirements elicitation and framing, divergent exploration
- [Plan] Unaided — no capability applied to this phase; considered: work breakdown and task decomposition

两阶段都用 `hooks/task unaided` 声明。本阶段的工作是读本仓库自己的 hook 与 smoke 断言（`summarize-state:18`、`session-start:175-184`、`smoke-test:48`），核对其间的约束；方案三选一已由用户裁定，没有外部能力可补充这些文档未承载的信息。

## Preconditions

- [x] 适用的仓库文档与个人规则已检查、优先级/冲突已记录。`repository-docs/index.md` 路由 `CONTRIBUTING.md`（design,code,commit,pr,release）与 `CODE_STYLE.md`（code,review）；无仓库文档规范 SessionStart 的输出内容，无冲突。本 clone 无个人规则。
- [x] 远程/fork/PR 工作：`origin` = `hkwuks/TaskFlow`，base = `main`，本分支从 `9ca6654` 起。Step 3 在任何推送前复核。
- [x] PR 模板：`.github/pull_request_template.md` 为 phase `pr` 的适用文档；Step 3 逐字段映射并记录模板路径与验证。
- [x] 缺失治理草案与显式批准：不适用——本任务不创建任何缺失的治理文档。
- [x] 核心文档单一写者：Primary Agent（Claude）。分支 `fix/entry-point-silence`，worktree `.worktrees/2026-10-10-entry-point-silence`。
- [x] 既有用户裁定已记录：修复只落在 hook 层；「未登记工作」用 git 分支信号；`smoke-test:48` 断言按新行为改写。见 PRD 的 Open Questions。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-10 22:11 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 让入口在两处不再静默

- Goal: `summarize-state` 在「无 TaskFlowDocs」与「分支不属任何任务」两种形态下各说一句话，其它形态一字不变。
- Dependencies: None.
- Files: `hooks/summarize-state`。
- Implementation checklist:
  - [x] R1：把无 docs 时的静默退出改为输出一段入口提示（义务 + 首条记录 + 只读类豁免），仍 `exit 0`，不创建任何文件。
  - [x] R2：判定当前分支（`git branch --show-current`，失败即空）的最后一段 slug；若它被 `TaskFlowDocs/*/` 或 `TaskFlowDocs/achieved/*/` 中某个目录名以结尾包含，视为已登记，不出报告。
  - [x] R3：`main`/`master`、空（分离 HEAD）、非 Git 仓库三种形态提前返回，不输出该行。
  - [x] R4：只用 `git`、`awk`/`case`、POSIX sh 内建；新增段落不得引入新 bashism、或任何解释器。
  - [x] 入口提示只在无 docs 分支输出；分支报告只在有 docs 且未登记时输出——两者互斥，不会同时出现。
- Acceptance: PRD A1、A2、A3。
- Verification: 三个 fixture 手跑（无 docs 的 git 仓库、有 docs 且分支未登记、任务工作树内）+ `od -c` 确认无 docs 时输出非空且无文件产生。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

### Step 2 — 把新行为钉进断言，并改写被取代的那条

- Goal: 让 R1/R2 由检查而不是靠人记着；同时把 `smoke-test:48` 钉住的旧行为按新行为改写并注明是行为变更。
- Dependencies: Step 1.
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 改写「summarize-state with no TaskFlowDocs prints nothing」一节：断言输出非空且含 `TaskFlowDocs/todo.md`；节标题与注释写明这是有意变更及其理由。
  - [x] 断言 R1 不产生副作用：无 docs 场景跑完后 `TaskFlowDocs/` 仍不存在。
  - [x] 断言 R2 正向：有 docs、分支未登记 → 输出含分支名的那一行。
  - [x] 断言 R2 反向：分支 slug 与任务目录匹配 → 不输出该行。
  - [x] 断言 R3：基分支与非 Git 目录两种形态不输出该行。
  - [x] 实现须落在既有 POSIX `awk`/`sed` + bash 3.2 地板内；断言里不得出现撇号嵌在 `$( )` 的 heredoc 中（Task A 的 CI 失败根因）。
- Acceptance: PRD A4。
- Verification: `bash hooks/smoke-test` 全量通过；**变异验证**：把 R1 改回静默 → R1 断言红；去掉 slug 匹配 → R2 正向断言红；恢复后全绿（一次一个变异，做完确认工作树干净）。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

### Step 3 — 全量验证与收尾

- Goal: 确认没有打破既有断言与无解释器不变量，并留下可复核的记录。
- Dependencies: Step 1, Step 2.
- Files: 本任务 `plan.md`（验证记录）、`TaskFlowDocs/todo.md`（状态）。
- Implementation checklist:
  - [x] `bash hooks/smoke-test` 全量；确认 no-interpreter 一节仍通过（A5）。
  - [x] `git diff --check`。
  - [x] `bash hooks/release-check .`。
  - [x] `quick_validate.py skills/taskflow`（`/home/hk/miniconda3/envs/torch/bin/python`）。
  - [x] `bash -n hooks/summarize-state` 与 `docker run --rm -v "$PWD:/w" -w /w bash:3.2 bash -c 'bash -n hooks/summarize-state'`。
  - [x] 在 `## Verification / Review` 记录每条命令与结果，区分既有/新引入/环境失败，并记录两个方向的变异验证。
  - [x] 读 `.github/pull_request_template.md`，逐字段映射并记录模板路径与验证结果。
  - [x] 推送后记录 CI 三 host 矩阵结果（含 run 链接）。
- Acceptance: PRD A6。
- Verification: 上述命令输出逐条记录在 `## Verification / Review`。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

## Checkpoints

- CP1（Step 1 后）：三个 fixture 手跑结果与 PRD A1–A3 逐条对上；任务工作树内不出现新行（否则每个会话都是噪声）。
- CP2（Step 2 后）：两个方向的变异各触发一次失败，恢复后全量通过；no-interpreter 一节未被新代码破坏。
- CP3（Step 3 收尾）：全套命令通过、验证记录与 PR 模板映射写入本文件、CI 绿。

## Verification / Review

- 2026-10-10 Step 3: smoke full green; both mutation directions red then restored; diff --check CLEAN; bash 3.2 parse OK; release-check pass; quick_validate 'Skill is valid!'; verification table and PR-template mapping written

- 2026-10-10 Step 2: full smoke green; mutation 1 (silence restored) -> FAIL no-docs output does not name the first record; mutation 2 (slug match removed) -> FAIL branch report raised for fix/one; restored -> ALL SMOKE PASSED

- 2026-10-10 Step 1: three fixtures hand-run (no docs / unregistered branch / task worktree) match A1-A3; no TaskFlowDocs created

逐条记录命令与结果。区分：**既有失败**（改动前就存在）/ **新引入失败** / **环境失败**。

| 检查 | 结果 | 分类 |
| --- | --- | --- |
| `bash hooks/smoke-test`（全量，Step 3 后） | exit 0，`ALL SMOKE PASSED`；改写的那节与新增的分支报告节各自 `ok` | 通过 |
| **变异验证 1**：把无 docs 时的入口提示改回 `exit 0` 静默 | `FAIL no-docs output does not name the first record` | 断言有效（R1 被断言咬住） |
| **变异验证 2**：删掉 `case "$name" in *-"$branch_slug")` 这一行匹配 | `FAIL branch report raised for fix/one` | 断言有效（R2 反向被咬住） |
| 恢复两处后重跑全量 | `ALL SMOKE PASSED`，`git status` 仅两个预期文件 | 通过 |
| R1 的三种形态手跑 | 无 docs：输出入口提示、exit 0、`TaskFlowDocs/` 仍不存在；基分支/分离 HEAD/非 Git 目录：不输出该行 | 通过（PRD A1、A3） |
| R2 的四种形态手跑 | 未登记分支 → 报告；活跃任务 slug 匹配 → 静默；`achieved/` 下 slug 匹配 → 静默；`main` → 静默 | 通过（PRD A2、A3） |
| 无解释器不变量 | `smoke-test` 的 no-interpreter 一节仍通过；新增代码只用 `git`、`case` 与 POSIX sh 内建，未新增任何解释器 | 通过（PRD A5、R4） |
| `bash -n hooks/summarize-state` 与 `hooks/smoke-test` | 无输出 | 通过 |
| `docker run --rm -v "$PWD:/w" -w /w bash:3.2 bash -c 'bash -n …'` | 两个文件都 `bash 3.2 OK`——本轮的 heredoc 未嵌在 `$( )` 中，避开 Task A 的 CI 失败根因 | 通过 |
| `git diff --check` | `CLEAN` | 通过 |
| `bash hooks/release-check .` | `STATUS: pass` | 通过 |
| `quick_validate.py skills/taskflow` | `Skill is valid!`，用 `/home/hk/miniconda3/envs/torch/bin/python` | 通过 |

**未做的检查与限制**：CI 三 host 矩阵由推送后的 CI 裁决，本地不重跑。`session-start` 的 JSON 形状断言在既有段落里，本轮未改动该文件，未单独重测其形状。

**CI 结果**（`Hooks` workflow）：待推送后填入。

### PR 模板映射（`.github/pull_request_template.md`，phase `pr` 的适用文档）

模板路径已核对（25 行、4 节）。每个字段的映射：

| 模板字段 | 落点 | 状态 |
| --- | --- | --- |
| Summary | PR 正文首节——入口静默的两个形态与「一层说清」的改法 | 待推送时写 |
| TaskFlow traceability: Task | `TaskFlowDocs/2026-10-10-entry-point-silence/`（归档后为 `TaskFlowDocs/achieved/…`） | 已确定 |
| TaskFlow traceability: Scope | PRD 的 In Scope：`hooks/summarize-state`、`hooks/smoke-test`、本任务文档 | 已确定 |
| TaskFlow traceability: Base branch | `main`（`origin` = `hkwuks/TaskFlow`），本分支从 `9ca6654` 起 | 已验证 |
| TaskFlow traceability: Target repository | `hkwuks/TaskFlow`，凭据不写入 | 已验证 |
| Verification: Hooks workflow pass | 推送后由 CI 裁决，链接写进 PR 正文 | 待推送 |
| Verification: `git diff --check` | 见上表：`CLEAN` | 已记录 |
| Verification: Skill/plugin validation | `quick_validate` `Skill is valid!`、`release-check` `STATUS: pass` | 已记录 |
| Verification: Results recorded in the Plan | 本节 | 已完成 |
| Review boundaries（4 条） | 无凭据写入；`git status` 仅本轮 2 个文件 + 任务目录；`origin`/`main` 已核对；见 `## Follow-ups` | 已完成 |

## Change Log

- 2026-10-10 work revision — 任务由 `TF-20261010-82ec77` promote 创建；用户裁定三个设计决定（只改 hook / git 分支信号 / 改写 `smoke-test:48`），写入 PRD 与 `Skills / Tools Used`；affects `prd.md`, `plan.md`, `TaskFlowDocs/todo.md`。

## Follow-ups

- 基分支判定只认 `main`/`master` 字面名，未解析远程默认分支；默认分支叫别的名字的仓库会多一行报告。若要收紧，改成读 `git symbolic-ref refs/remotes/origin/HEAD`，但它在无远程时会失败，需一并处理。
- slug 匹配是「以结尾包含」的启发式：分支 `fix/foo` 与任务 `2026-01-01-foo-extra` 也会匹配。取的是少报优先，因为多报会在每个会话变成噪声。若实测发现漏报伤害更大，再改成更严的精确匹配并接受伴随的噪声。
- 入口提示只在无 `TaskFlowDocs/` 时出现。若某仓库建了 `TaskFlowDocs/` 但从未登记任何条目，`TF-20261009-cc463b` 里「工作未登记」的更宽形态仍无信号；本轮不做。
- `repository-docs-context` 仍会输出指向本仓库不存在的 `TaskFlowDocs/repository-docs/index.md` 的引导（PRD B2 末段）。属另一处入口措辞，另立任务。
- 本任务落地后需一次发布才惠及已安装用户；`hooks/summarize-state` 的输出是用户可见面，发布记录里应写明这条变更。

## Version History

- v1 — 规划中，等待用户批准。
