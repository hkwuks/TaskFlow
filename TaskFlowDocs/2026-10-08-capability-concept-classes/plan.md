# Plan — 让「发散与想法精炼」成为 phase 表里的独立概念类
> Task version: v1
> Status: checking

No spec required — 改动是三处文本的一处数据点（phase 表一行、`concept_class_re` 一行、`SKILL.md` 一段）加一个校验段；无跨层契约、无数据结构变更、无兼容性决策。唯一有设计成分的是 R4 的对账断言，其面与备选方案已界定在 PRD 的 Risks 与 Step 2 的 checklist 内。

## Spec Pointers

None. `### 3. Design — Spec decision` 的判定：改动面虽含一个新增校验，但不引入接口/数据流/错误契约；规模判定仍为 small。

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — 适用的仓库文档与阶段。
- `CONTRIBUTING.md:16-33` — 分支/worktree 隔离。
- `skills/taskflow/references/runtime.md:94-110` — hook 的 must/may-not 边界。
- `TaskFlowDocs/achieved/2026-10-08-task-open-and-continuation/` — 同批 Task A，其 PR 与验证记录是本任务的直接先例。

## Related Tasks

- Parent: None.
- Children: None.
- Depends on: `TaskFlowDocs/achieved/2026-10-08-task-open-and-continuation/` (Task version: v1) — 本任务从它合并后的 `main`（`e471857`）起分支。
- Blocks: None.
- Related: `TF-20261008-a4454d` + `TF-20261008-4d37b2`（Task C）、`TF-20261008-ca2fce`（Task D）——同批，均改 `SKILL.md`，须排在本任务之后或另行 rebase。

## Skills / Tools Used

- [PRD] Unaided — no capability applied to this phase; considered: requirements elicitation
- [Plan] Unaided — no capability applied to this phase; considered: work breakdown

两个阶段都用 `hooks/task unaided` 声明而非散文断言。这一阶段的工作是读本仓库自己的文档（`SKILL.md` 的 phase 表、`hooks/task:606` 的类注册表、`hooks/capability-gate:28-35` 的 `stage_class()`、`hooks/smoke-test:1447-1458` 的既有断言）并核对其间的约束，没有外部能力可补充这些文档未承载的信息；需求澄清是一轮与用户的三选一问答。

## Preconditions

- [x] 适用的仓库文档与个人规则已检查、优先级/冲突已记录。`repository-docs/index.md` 路由 `CONTRIBUTING.md`（design,code,commit,pr,release）与 `CODE_STYLE.md`（code,review）；无仓库文档规范概念类词表或 `sessions.md` 类事项，无冲突。本 clone 无个人规则。
- [x] 远程/fork/PR 工作：`origin` = `hkwuks/TaskFlow`，base = `main`，本分支从 `e471857`（含 Task A 的合并）起。Step 4 在任何推送前复核。
- [x] PR 模板：`.github/pull_request_template.md` 为 phase `pr` 的适用文档；Step 4 逐字段映射并记录模板路径与验证。
- [x] 缺失治理草案与显式批准：不适用——本任务不创建任何缺失的治理文档。
- [x] 核心文档单一写者：Primary Agent（Claude）。分支 `docs/capability-concept-classes`，worktree `.worktrees/2026-10-08-capability-concept-classes`。
- [x] 既有用户裁定已记录：方案 A（独立概念类），见 PRD 的 Open Questions。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-09 21:10 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 新增概念类并把三处副本改一致
- Goal: 让 `divergent exploration` 成为可匹配、可记录的独立类，且 phase 表、类注册表、文档三处一致。
- Dependencies: None.
- Files: `skills/taskflow/SKILL.md`（phase 表 phase 1 行、`### 1. Define — PRD`）、`hooks/task`（`concept_class_re`）。
- Implementation checklist:
  - [x] phase 1 行的概念类列改为 `requirements elicitation and framing; divergent exploration`；表头行与 phase 2–7 行**逐字不动**（改完用 `git diff` 核对只有一行变化）。
  - [x] phase 1 行的「Consider a capability for」列**增加**一项 ideation 表述（让模糊想法变清晰、展开多个方向、在对象/边界未定时先发散），保留原三项。
  - [x] `hooks/task:606` 的 `concept_class_re` 末尾追加 `|divergent exploration`，保持"类名词根一致、后缀可选"的既有约定。
  - [x] `### 1. Define — PRD` 补一条可判定的发散前置条件（目标/方案未定或多方向并存时，先发散再收敛，不得直接写需求），并写明**不构成强制**——`SKILL.md:144` 与 `:156` 的既有权衡句不动。
  - [x] **不改** `hooks/capability-gate:stage_class()`（A5）。
  - [x] 全仓库确认无第三处依赖「类名 → 唯一 stage」的映射（复核 `hooks/capability-gate`、`hooks/task` 的 `unaided`/`approve`）。
- Acceptance: PRD A1、A2、A3、A5 成立。
- Verification: `git diff` 逐行核对只动了预期行；`./hooks/task unaided PRD --considered "divergent exploration"` 退出 0；`--considered "随便什么"` 退出 2；`grep` 确认 phase 2–7 行与 `capability-gate` 的 `stage_class` 未变。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

### Step 2 — 用断言锁住一致性与记录能力
- Goal: 让"三处必须同批改"和"新类真的可记录"由检查而不是靠人记着。
- Dependencies: Step 1.
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 新增断言：phase 1 行含 `divergent exploration`；phase 表仍无产品名（并入既有 `:1458` 那段）。
  - [x] 新增断言：`unaided` 接受 `divergent exploration`（退出 0）且仍拒绝词表外的类（退出 2）；与既有的 `cg_unaided` 段同风格、不重复造 fixture。
  - [x] 实现对账断言：把 phase 表的概念类列与 `concept_class_re` 的备选集合抽出比对，**任一新增类只出现在一处即失败**。先试集合比对；若解析不稳，退回逐类名双向 grep 存在性（更钝但可靠，能捕获单向新增），并在本文件记录选了哪条路径及原因。
  - [x] 对账断言必须**双向**：`concept_class_re` 里有而表里没有 → 失败；表里有而 `concept_class_re` 里没有 → 失败。
  - [x] 实现须落在既有 POSIX `awk`/`sed` + bash 3.2 地板内（`runtime.md:126`）；断言里**不得出现撇号嵌在 `$( )` 的 heredoc 中**（Task A 的 CI 失败根因）。
- Acceptance: PRD A4 成立。
- Verification: `bash hooks/smoke-test` 全量通过；**变异验证**：临时从 phase 表删掉新类、确认对账断言失败，再恢复（一次一个变异，做完确认工作树干净）。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

### Step 3 — 全量验证与收尾
- Goal: 确认没有打破既有的表/hook 对账，并留下可复核的记录。
- Dependencies: Step 1, Step 2.
- Files: 本任务 `plan.md`（验证记录）, `TaskFlowDocs/todo.md`（状态）。
- Implementation checklist:
  - [x] `bash hooks/smoke-test` 全量。
  - [x] `git diff --check`（必须 CLEAN，不得重复 Task A 那个尾空格问题）。
  - [x] `bash hooks/release-check .`。
  - [x] `quick_validate.py skills/taskflow`（`/home/hk/miniconda3/envs/torch/bin/python`）。
  - [x] `bash -n hooks/task` 与 `docker run --rm -v "$PWD:/w" -w /w bash:3.2 bash -c 'bash -n hooks/task'`（bash 3.2 解析，Task A 踩过的坑）。
  - [x] 在 `## Verification / Review` 记录每条命令与结果，区分既有/新引入/环境失败，并记录变异验证。
  - [x] 读 `.github/pull_request_template.md`，逐字段映射并记录模板路径与验证结果。
  - [x] 推送后记录 CI 三 host 矩阵结果（含 run 链接）；失败则记录根因与修复。
- Acceptance: PRD A6 成立。
- Verification: 上述命令输出逐条记录在 `## Verification / Review`。
- Rollback: revert 承载本 Step 的 commit；本任务不涉及数据或发布状态。
- Status: done

## Checkpoints

- CP1（Step 1 后）：`git diff` 证明只动了 phase 1 行、`SKILL.md` 的 PRD 段、`concept_class_re` 一行；phase 2–7 行与 `capability-gate` 未变。
- CP2（Step 2 后）：对账断言**双向**有效——两个方向的变异各触发一次失败（先表缺、再注册表缺），恢复后全量通过。
- CP3（Step 3 收尾）：全套命令通过、验证记录与 PR 模板映射写入本文件、CI 绿。

## Verification / Review

- 2026-10-09 Step 3: smoke full green; diff --check CLEAN; bash 3.2 parse OK via docker; quick_validate 'Skill is valid!' via conda torch interpreter; release-check STATUS pass; capability-gate byte-identical (A5)

- 2026-10-09 Step 2: smoke-test: reconciler comparing the phase table's class column against concept_class_re in one awk, both directions; class-record assertions on an isolated fixture repo. Mutation-verified both directions: removing the class from the table -> 'vocabulary names a class no phase offers'; removing it from the regex -> 'phase table offers a class the vocabulary rejects'; full suite green after restore

- 2026-10-09 Step 1: phase table phase-1 row and concept_class_re changed; git diff shows only the intended lines (phase 2-7 rows and phase-table header untouched); unaided PRD --considered 'divergent exploration' -> 0, off-vocabulary -> 2; capability-gate byte-identical

待执行（Step 3）。

## Change Log

- 2026-10-08 work revision — 任务由 `TF-20261008-5b5635` promote 创建；用户裁定方案 A（新增独立概念类，记录可区分），写入 PRD 与 `Skills / Tools Used`；affects `prd.md`, `plan.md`, `TaskFlowDocs/todo.md`。
- 2026-10-08 work revision — 调研落地：核出概念类有三个位置（phase 表 / `hooks/task:606` / `capability-gate:stage_class`）且**没有对账断言**，据此把"三处同批改"升级为 R4 的可执行断言，并确认 `stage_class` 不必改（A5）；另记录 `concept_class_re` 子串匹配过宽的既有缺陷为 follow-up；affects `prd.md`, `plan.md`。

## Follow-ups

- `concept_class_re` 用子串匹配，`unaided PRD --considered "work"` 会通过（匹配 `work breakdown`）。改动前即存在；修它需评估既有 `unaided` 记录的接受集合，另立任务。
- phase 表与 `concept_class_re` 长期是手工同步的两份副本；本次只加对账断言，未做单一来源重构。
- 对账断言从 markdown 表格抽列的稳健性是新增面；若后续 phase 表加列或改分隔符导致它脆化，优先改成逐类名双向 grep 而非放宽断言。
- Task A 遗留：`sessions.md` 的触发条件已落地，但"父任务升版后子任务须重记"仍无可执行检查（跨任务目录不可见）。

## Version History

- v1 — 规划中，等待用户批准。
