# Plan — 进入顺序：先 TaskFlow，再阶段，然后才是能力

> Task version: v1
> Status: checking

No spec required — 改动是 SKILL.md 里两段声明、`capability-gate` 的一句 deny 文案、`summarize-state` 的一个入口分支，加两组 smoke 断言。无跨层契约、无数据结构变更、无兼容性决策；有设计成分的只有 R4/R5 的触发条件，其边界已界定在 PRD 的 Risks 内。

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — 适用的仓库文档与阶段。
- `CONTRIBUTING.md:16-33` — 分支/worktree 隔离；本任务从 `origin/main` 的 `85ba7c7` 起在 `.worktrees/2026-10-10-taskflow-first-order`。
- `skills/taskflow/references/runtime.md:165-180` — SessionStart 综合的边界与 `summarize-state` 的既有契约（R6、A6 的来源）。
- `skills/taskflow/SKILL.md:10-18` — Applicability gate 段，R1/R2 的落点。
- `hooks/capability-gate` 末尾的 `deny` 文案 — R3 的落点，也是既有断言钉住的三处（`[<STAGE>]`、概念类别、`task unaided`）。
- `TaskFlowDocs/achieved/2026-09-10-audit-hook-opportunities/reference/hook-audit.md:81` — `UserPromptSubmit` 的否决记录（PRD B5）。

## Related Tasks

- Parent: None.
- Children: None.
- Depends on: None.
- Blocks: None.
- Related: `TF-20261001-efbc51` — 本条明确不做的「已发生调研的入账」由它承担；它的统一锚点定下来之前改动 `capability-evidence` 只能修一半（PRD B3）。`TF-20261009-8abbd6` — 同族，讲 gate 读不到归属；本条只钉顺序。`TF-20261010-82ec77` — 第四个失败模式的前两半由它落地（PR #73），本条补第三半。`TF-20261008-5b5635` — phase 表措辞，已 done。

## Skills / Tools Used

- [PRD] Unaided — no capability applied to this phase; considered: requirements elicitation and framing
- [Plan] Unaided — no capability applied to this phase; considered: work breakdown and task decomposition

两阶段都用 `hooks/task unaided` 声明。本阶段的工作是读本仓库自己的两个 hook、SKILL.md 的入口段与既有 smoke 断言，核对其间的约束；三个设计决定已由用户裁定，没有外部能力可补充这些文档未承载的信息。

## Preconditions

- [x] 适用的仓库文档与个人规则已检查、优先级/冲突已记录。`repository-docs/index.md` 路由 `CONTRIBUTING.md`（design,code,commit,pr,release）与 `CODE_STYLE.md`（code,review）；无仓库文档规范入口顺序。本 clone 无个人规则。
- [x] 远程/fork/PR 工作：`origin` = `hkwuks/TaskFlow`，base = `main`，本分支从 `85ba7c7` 起。Step 3 在任何推送前复核。
- [x] PR 模板：`.github/pull_request_template.md` 为 phase `pr` 的适用文档；Step 3 逐字段映射并记录模板路径与验证。
- [x] 缺失治理草案与显式批准：不适用——本任务不创建任何缺失的治理文档。
- [x] 核心文档单一写者：Primary Agent（Claude）。分支 `docs/taskflow-first-order`，worktree `.worktrees/2026-10-10-taskflow-first-order`。
- [x] 既有用户裁定已记录：范围只钉顺序（入账留给 efbc51）；强度为声明 + smoke 钉住；第四个失败模式的剩余一半并入本条。见 PRD 的 Open Questions。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-10 23:52 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 把顺序写进 Skill 与 gate 的拒绝文案

- Goal: R1/R2 落在 Applicability gate 段内，R3 让 gate 的 deny 文案说同一套规则。
- Dependencies: None.
- Files: `skills/taskflow/SKILL.md`、`hooks/capability-gate`。
- Implementation checklist:
  - [x] R1：在 `SKILL.md` 的 Applicability gate 段内加顺序声明，含「先登记、再阶段、能力在阶段内」，并写明它不是第二道闸门、也不把每个请求变成任务。
  - [x] R2：同段写明「先」的含义：Todo 在实现之前存在；阶段的能力在该阶段开始时选择。
  - [x] 避开既有断言钉住的子句（`smoke-test:1353-1362` 区段）。
  - [x] R3：`capability-gate` 的 deny 文案加入同一句顺序，保留既有断言要求的三处（`[<STAGE>]`、概念类别、`task unaided <STAGE> --considered`）。
- Acceptance: PRD A1、A2。
- Verification: `bash hooks/smoke-test` 全量；变异验证——删掉顺序句 → A1 红；把 deny 文案改回旧措辞 → A2 红；恢复后全绿（一次一个变异，做完确认工作树干净）。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

### Step 2 — 补入口的第三种静默

- Goal: R4/R5 落在 `summarize-state`，并把它钉进断言。
- Dependencies: None（与 Step 1 无文件重叠）。
- Files: `hooks/summarize-state`、`hooks/smoke-test`。
- Implementation checklist:
  - [x] R4：`TaskFlowDocs` 存在但从未登记任何条目时输出入口边界，复用既有措辞，不创建任何文件。
  - [x] R5：触发条件为 `todo.md` 不存在且除 `repository-docs` 外没有任何任务目录；`repository-docs/` 单独存在不算登记过，`achieved/` 算。
  - [x] 断言三个方向：无 `todo.md` 且无任务 → 输出该行；写入 `todo.md` → 该行消失；只有 `achieved/` → 不输出。
  - [x] R6：只用 POSIX sh 内建与既有 `case`/glob，不引入新 bashism、不新增解释器。
- Acceptance: PRD A3、A4、A5。
- Verification: `bash hooks/smoke-test` 全量；变异验证——把入口分支改成 `if false` → A3 红；恢复后全绿。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

### Step 3 — 全量验证与收尾

- Goal: 确认没有打破既有断言与无解释器不变量，并留下可复核的记录。
- Dependencies: Step 1, Step 2.
- Files: 本任务 `plan.md`（验证记录）、`skills/taskflow/references/runtime.md`（A6）、`TaskFlowDocs/todo.md`（状态）。
- Implementation checklist:
  - [x] `bash hooks/smoke-test` 全量；确认 no-interpreter 一节仍通过（A5）。
  - [x] A6：`references/runtime.md` 对 `summarize-state` 的描述与 R4 一致（原文写「Prints nothing when no TaskFlowDocs exists」，已不成立）。
  - [x] `git diff --check`。
  - [x] `bash hooks/release-check .`。
  - [x] `quick_validate.py skills/taskflow`（`/home/hk/miniconda3/envs/torch/bin/python`）。
  - [x] `bash -n hooks/summarize-state` 与 `docker run --rm -v "$PWD:/w" -w /w bash:3.2 bash -c 'bash -n …'`。
  - [x] 在 `## Verification / Review` 记录每条命令与结果，区分既有/新引入/环境失败，并记录三个方向的变异验证。
  - [x] 读 `.github/pull_request_template.md`，逐字段映射并记录模板路径与验证结果。
  - [x] 推送后记录 CI 三 host 矩阵结果（含 run 链接）。
- Acceptance: PRD A6。
- Verification: 上述命令输出逐条记录在 `## Verification / Review`。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

## Checkpoints

- CP1（Step 1 后）：顺序句与 deny 文案读起来是同一套规则；既有 smoke 全绿。
- CP2（Step 2 后）：三个方向的入口断言各触发一次；no-interpreter 一节未被新代码破坏。
- CP3（Step 3 收尾）：全套命令通过、验证记录与 PR 模板映射写入本文件、CI 绿。

## Verification / Review

- 2026-10-10 Step 3: bash hooks/smoke-test: ALL SMOKE PASSED (66 ok sections); three mutations each red then restored

逐条记录命令与结果。区分：**既有失败**（改动前就存在）/ **新引入失败** / **环境失败**。

| 检查 | 结果 | 分类 |
| --- | --- | --- |
| `bash hooks/smoke-test`（全量，Step 1+2 后） | exit 0，`ALL SMOKE PASSED`，66 个 `ok` 节；新增两节各自 `ok` | 通过 |
| **变异验证 1**：删掉 `SKILL.md` 的顺序句 | `FAIL the entry order is not stated` | 断言有效（R1 被咬住） |
| **变异验证 2**：把 `summarize-state` 的入口分支改成 `if false` | `FAIL unrecorded-repo output does not name the first record` | 断言有效（R4 被咬住） |
| **变异验证 3**：把 `capability-gate` 的 deny 文案改回旧措辞 | `FAIL the gate denial does not state the order` | 断言有效（R3 被咬住） |
| 恢复三处后重跑全量 | `ALL SMOKE PASSED`，`git status` 仅预期文件 | 通过 |
| R4/R5 三个方向手跑（断言内） | 无 `todo.md` 且无任务 → 输出该行；写入 `todo.md` → 该行消失；只有 `achieved/` → 不输出 | 通过（PRD A3、A4） |
| R1 的既有子句未被破坏 | `smoke-test` 原 section 的 `grep` 断言全绿（顺序声明加在 Applicability gate 段末，未改动被钉住的子句） | 通过 |
| 无解释器不变量 | no-interpreter 一节仍通过；新代码只用 `case` 与 glob，未新增解释器 | 通过（PRD R6、A5） |
| `bash -n hooks/summarize-state`、`hooks/smoke-test`、`hooks/capability-gate` | 无输出 | 通过 |
| `docker run --rm -v "$PWD:/w" -w /w bash:3.2 bash -c 'bash -n …'` | 三个文件都 `bash 3.2 OK` | 通过 |
| `git diff --check` | `CLEAN` | 通过 |
| `bash hooks/release-check .` | `STATUS: pass` | 通过 |
| `quick_validate.py skills/taskflow` | `Skill is valid!`，用 `/home/hk/miniconda3/envs/torch/bin/python` | 通过 |

一处实现期修正：`summarize-state` 的第一版把 `achieved` 与 `repository-docs` 一并从「登记过」里排除，导致「只有归档任务」的仓库也被判成「什么都没登记」。断言的第三个方向（`only achieved/` → 不输出该行）把它咬出来，随后只排除 `repository-docs`。留下的 `repository-docs` 排除是必要的：`hooks/repository-docs-context` 每次 SessionStart 都会确保该目录与 `index.md` 存在，不排除则本仓库永不触发。

**未做的检查与限制**：CI 三 host 矩阵由推送后的 CI 裁决，本地不重跑。

**CI 结果**（`Hooks` workflow）：（推送后补记）

### PR 模板映射（`.github/pull_request_template.md`，phase `pr` 的适用文档）

（推送后补记）

## Change Log

- 2026-10-10 work revision — 任务由 `TF-20261009-cc463b` promote 创建；用户裁定三个设计决定（只钉顺序 / 声明 + smoke 钉住 / 第四个失败模式的剩余一半并入），写入 PRD 的 Open Questions 与本文件的 `Skills / Tools Used`；affects `prd.md`, `plan.md`, `TaskFlowDocs/todo.md`。

## Follow-ups

- 第五个失败模式仍不可上报：base 检出上未建分支就改仓库、或分支名不含 slug（如 `user/foo`）时，四类信号同时为空。同源于第四个失败模式，触发条件落在分支命名上；需与 `TF-20261001-efbc51` 的锚点语义一起定。
- 顺序声明是 prose 而非机制：没有 hook 会拒绝「先调研后建档」，可检查的只有它有没有被写下来（A1）。
- 建了 `TaskFlowDocs/` 与 `todo.md`、但从未写入任何条目时，R4 不触发。这是按 R5 有意划出的边界。
- 本任务落地后需一次发布才惠及已安装用户。

## Version History

- v1 — 规划中，等待用户批准。
