# Plan — 任务关系与会话延续：sessions.md 触发条件、重叠上报、父子任务协调
> Task version: v1
> Status: checking

No spec required — 改动集中在一份 Skill 文档、一份 reference 与 `hooks/task` 的一个子命令；无跨层契约、无数据结构变更、无兼容性决策，边界由 PRD 的 Acceptance Criteria 完全界定。

## Spec Pointers

None.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — applicable repository documents and their phases.
- `CONTRIBUTING.md:16-33` — branch/worktree isolation, the base for Step 0.
- `skills/taskflow/references/runtime.md:94-110` — the hook must/may-not boundary that constrains R2a.
- `skills/taskflow/references/versioning-and-recovery.md` — the version transition R3b(3) relies on.

## Related Tasks

- Depends on: None.
- Blocks: None.
- Related: `TaskFlowDocs/<not created yet>` — the remaining 2026-10-08 batch (worktree migration, reference sync + version guidance, loop compatibility, brainstorming concept class) shares `SKILL.md` and therefore merges serially behind this task.

## Skills / Tools Used

- [PRD] Unaided — no capability applied to this phase; considered: requirements elicitation
- [Plan] Unaided — no capability applied to this phase; considered: work breakdown

Both stages were declared with `hooks/task unaided` rather than asserted in prose. The phase's work was reading this repository's own documents (`SKILL.md`, `artifacts.md`, `runtime.md`, `hooks/task`) against the three requirements — no external capability had anything to add that those documents did not already carry. The requirements clarification ran as a direct three-question exchange with the user, which is the artifact's own input rather than a capability applied to produce it.

## Preconditions

- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded. `repository-docs/index.md` routes `CONTRIBUTING.md` (design,code,commit,pr,release) and `CODE_STYLE.md` (code,review); no repository document governs `sessions.md` or task-to-task relations, so no conflict arises. No personal rule is present in this clone.
- [x] For remote/fork/PR work: not applicable to this task's implementation. `origin` is `hkwuks/TaskFlow`, base is `main`; Step 4 records what was established before any push.
- [x] For PR creation/update: applicable template path, every required-field mapping, and template verification recorded. `.github/pull_request_template.md` is routed for phase `pr`; read and mapped in Step 4 before any PR mutation.
- [x] Missing governance drafts and explicit approvals recorded before they become binding. Not applicable — no missing governance document is created by this task.
- [x] Named owner for core documents: Primary Agent (Claude), single writer. Branch and worktree: `docs/task-open-and-continuation` in `.worktrees/2026-10-08-task-open-and-continuation`.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-08 22:31 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — sessions.md 的触发条件与归属
- Goal: 把 `SKILL.md:289` 的不可判定条件换成可判定的义务，使 `sessions.md` 不再依赖 hook 的偶然产生。
- Dependencies: None.
- Files: `skills/taskflow/SKILL.md` (`## Sessions and collaboration`), `skills/taskflow/references/artifacts.md` (`## Session outline`), `hooks/smoke-test`.
- Implementation checklist:
  - [x] 用「会话结束时任务尚未 `completed` → 必须在当前条目写 `Next step`（`Last completed` 非空时同写）」替换 `only when cross-session or cross-agent continuation is useful`。
  - [x] 保留 hook 与 Agent 的字段归属边界原文（`Last completed` / `Next step` / `Notes` 归 Agent，hook 只写机械字段，Agent 是唯一能 `closed` 的写入者）。
  - [x] 写明 hook 不可用时的降级路径：按 `artifacts.md` 的 Session outline 自行创建文件。
  - [x] 处理与 `SKILL.md:41`「optional」的措辞冲突：条件触发时它是义务，措辞不得互相矛盾。
  - [x] `artifacts.md` 的 Session outline 指向 `SKILL.md` 的触发条件，不重述它。
  - [x] 在 `hooks/smoke-test` 增加对触发句的 pin，并在同一处断言旧的不可判定措辞不再出现。
- Acceptance: PRD A1 成立。
- Verification: `bash hooks/smoke-test`（新增段与全量）通过；`grep -n 'only when cross-session' skills/taskflow/SKILL.md` 无输出。
- Rollback: revert the commit carrying this Step.
- Status: done

### Step 2 — 重叠候选提示与上报义务
- Goal: 让重复/重叠/冲突在写入与选题两个时点被看见。
- Dependencies: None.
- Files: `hooks/task` (`intake`), `skills/taskflow/SKILL.md` (triage 段), `hooks/smoke-test`.
- Implementation checklist:
  - [x] 先确认 `intake` 的 stdout 契约：`grep -rn 'intake OK' hooks/ evals/ tools/ .github/` 找全部解析方。已知两处：`hooks/smoke-test:2041` 用 `awk '{ print $NF }'` 取末字段当 ID，`hooks/smoke-test:1247` 用 `grep -q 'intake OK:'` 判成功。因此候选**走 stderr**，stdout 一行不加。
  - [x] 在 `intake` 写入前实现词面重叠检测：与现存 live 条目（非 `done`/`cancelled`）比较，最多 3 条候选（ID + 标题）经 stderr 报出，无判决词。
  - [x] 保持字节级重复 goal 的拒绝行为、成功退出码、stdout 逐字不变；重叠候选**不得**改变其中任何一项。
  - [x] 实现须落在既有 POSIX `awk` 能力内（`runtime.md:126` 的 bash 3.2 + BSD 地板），不得引入 grep -P、mapfile 等。
  - [x] 在 `SKILL.md` triage 处写入 R2b 的义务句：记录 Todo 后、创建/选择任务前，必须检查 Todo-vs-Todo 与 request-vs-task 两种关系；重复或冲突先报用户并取得选择，不得静默并存、不得自行合并。
  - [x] `hooks/smoke-test` 增加断言：有近似条目时打印候选、无近似条目不打印、退出码两种情况均不变。
- Acceptance: PRD A2、A3 成立。
- Verification: `bash hooks/smoke-test`；手工在临时 fixture 上跑 `intake` 两次（近义 goal / 无关 goal）核对输出与退出码；`bash -n hooks/task`。
- Rollback: revert the commit carrying this Step.
- Status: done

### Step 3 — 父子任务的需求协调
- Goal: 定义父子方向与三条传播规则，并让子任务记录其所依据的父版本。
- Dependencies: None.
- Files: `skills/taskflow/references/artifacts.md` (`## Related Tasks`), `skills/taskflow/SKILL.md` (`Existing-task-first selection` 与相邻段), `hooks/smoke-test`.
- Implementation checklist:
  - [x] `## Related Tasks` 增加 `Parent:` / `Children:`，与 `Depends on` / `Blocks` / `Related` 并存，并说明与 `Related` 的区别（方向 vs 对称）。
  - [x] 写明子任务**不修改**父任务文档，发现记入自己的 `plan.md` 并呈现给用户。
  - [x] 写明父任务已批准需求的变更走它自己的 User-change trigger，在父任务自己的工作树里进行，引用 `SKILL.md` 的分类而不重述。
  - [x] 写明子任务在自己的 `plan.md` 记录规划时依据的父任务版本；父升版后须重记；仅当变更触及子任务自己的已批准契约时才重新批准。
  - [x] `hooks/smoke-test` 增加对上述规则句的 pin。
- Acceptance: PRD A4 成立。
- Verification: `bash hooks/smoke-test`；人工核读 `SKILL.md` 相关段落，确认三条规则各自可判定、无互相引用成环。
- Rollback: revert the commit carrying this Step.
- Status: done

### Step 4 — 一致性收尾与全量验证
- Goal: 确认改动没有打破 Skill 文档与 hook 的既有对账，并留下可复核的验证记录。
- Dependencies: Step 1, Step 2, Step 3.
- Files: 本任务 `plan.md`（验证记录）, `TaskFlowDocs/todo.md`（状态）, 无新增实现文件。
- Implementation checklist:
  - [x] 确认 `SKILL.md` 的 phase 表与 `hooks/task:509` 的 `concept_class_re` 仍逐字一致（本任务不改该表）。
  - [x] 运行 `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow`。
  - [x] 运行 `git diff --check`。
  - [x] 运行 `bash hooks/release-check .`（版本/catalog 一致性；本任务不改版本，须仍通过）。
  - [x] 在 Web UI 之外的本地合并路径下确认 `TaskFlowDocs/todo.md` 的 merge driver 行为未受影响（本任务只改条目内容）。
  - [x] 在 `## Verification / Review` 记录每条命令与结果，区分既有失败/新引入失败/环境失败。
  - [x] 读 `.github/pull_request_template.md`，把每个必填字段映射到 PR 标题/正文/检查/用户决定，并记录模板路径与验证结果。
  - [x] 记录无法运行的检查及其限制；不声称未发生的检查。
- Acceptance: PRD A5、A6 成立。
- Verification: 上述命令的输出逐条记录在 `## Verification / Review`。
- Rollback: revert the commit carrying this Step；本任务不涉及数据或发布状态。
- Status: done

## Checkpoints

- CP1（Step 1 后）：确认改的是规则句而非新增产物；`grep` 证明旧措辞已消失。
- CP2（Step 2 后）：确认 `intake` 的 stdout 契约在所有解析方处仍然成立——这是本任务唯一有回归面的改动。
- CP3（Step 3 后）：三条协调规则可判定，且未与 `SKILL.md:60-71` 的表重复或冲突。
- CP4（Step 4 收尾）：全套命令通过，验证记录写入本文件。

## Verification / Review

- 2026-10-08 Step 4: phase table + concept_class_re both untouched (verified via git diff -U0); bash hooks/release-check . -> STATUS: pass; git diff --check -> 1 pre-existing hook defect (todo.md:26 trailing space from intake); quick_validate unavailable (env: no PyYAML, not installed); PR template mapped field-by-field in plan; CI matrix deferred to push per CONTRIBUTING.md:66-71

逐条记录命令与结果。区分：**既有失败**（改动前就存在）/ **新引入失败** / **环境失败**。

| 检查 | 结果 | 分类 |
| --- | --- | --- |
| `bash hooks/smoke-test`（全量，Step 3 后） | exit 0，`ALL SMOKE PASSED`；新增 3 段（resume 触发句、重叠候选报告、父子规则）各自 `ok` | 通过 |
| `bash -n hooks/task` | 无输出 | 通过 |
| `intake` stdout 契约：pristine vs 本分支逐字节 diff | `diff` 空，`STDOUT IDENTICAL` | 通过 |
| `intake` 退出码：首次 / 重复 goal | `0` / `1`（与改动前一致） | 通过 |
| 候选上限：6 个近似条目的 fixture | 恰 3 行 + `... and more` | 通过 |
| `concept_class_re` 与 `SKILL.md` phase 表 | 两处均**未被本任务触及**（`git diff -U0 skills/taskflow/SKILL.md` 中无 phase 表行）；`hooks/task` 的 `concept_class_re` 未改，`unaided` 仍以子串匹配接受表内类名 | 通过（不变量成立） |
| `bash hooks/release-check .` | `STATUS: pass`，全部字面量 `1.1.3`，两个 marketplace pin 解析到 `ff4b403` | 通过 |
| `git diff --check` | `CLEAN`。原先那处 `TaskFlowDocs/todo.md:<heading> trailing whitespace` 是 `hooks/task` 的 `intake` 缺陷：字节截断落在 goal 中段的空格串里，尾空格被写进 `## ` 标题行。已在 Step 2 的范围内修复（标题生成前 rstrip、截断后 `rtrim`），并清掉既有条目标题上的那一个空格；新增 smoke 段锁住回归 | 通过 |
| `quick_validate.py skills/taskflow` | `Skill is valid!`（exit 0）。用 `/home/hk/miniconda3/envs/torch/bin/python` 运行——系统 `python3` 与 base conda 均无 PyYAML，torch 环境有（yaml 6.0.2）。未安装任何依赖，只换了执行解释器 | 通过 |
| `todo.md` merge driver 未受影响 | 未执行独立合并实验：本任务对 `todo.md` 的改动只是 `intake` 写入的条目内容，未触碰 `hooks/merge-todo`、`hooks/install-merge-driver` 或 `merge.taskflow-todo` 配置，而全量 `smoke-test` 中的并行 intake 合并段（`== Todo IDs are derived from the goal… ==`）已覆盖驱动路径并通过 | 通过（由 smoke 覆盖，未另做实验） |

**未做的检查与限制**：CI 的三 host 矩阵（ubuntu / macos / windows）未在本地复现，按 `CONTRIBUTING.md:66-71` 由推送后的 CI 裁决——本任务尚未推送。

### PR 模板映射（`.github/pull_request_template.md`，phase `pr` 的适用文档）

模板路径与版本已核对（24 行、5 节）。每个字段的映射：

| 模板字段 | 落点 | 状态 |
| --- | --- | --- |
| Summary | PR 正文首节——三条规则的缺口与改法 | 待推送时写 |
| TaskFlow traceability: Task | `TaskFlowDocs/2026-10-08-task-open-and-continuation/` | 已确定 |
| TaskFlow traceability: Scope | 见 PRD 的 In Scope：`SKILL.md`、`references/artifacts.md`、`hooks/task`、`hooks/smoke-test`、本任务文档 | 已确定 |
| TaskFlow traceability: Base branch | `main`（`origin` = `hkwuks/TaskFlow`，已 fetch，本地 `main` 为 `origin/main` 的祖先） | 已验证 |
| TaskFlow traceability: Target repository | `hkwuks/TaskFlow`，凭据不写入 | 已验证 |
| Verification: Hooks workflow pass | 推送后由 CI 裁决，链接写进 PR 正文 | 待推送 |
| Verification: `git diff --check` | 见上表：1 处既有缺陷尾空格，如实说明 | 已记录 |
| Verification: Skill/plugin validation | `quick_validate` 环境不可用（缺 PyYAML），`release-check` 通过 | 已记录 |
| Verification: Results recorded in the Plan | 本节 | 已完成 |
| Review boundaries: no secrets / no unrelated files / remote-base stated / limitations documented | 四条分别由：无凭据写入；`git status` 仅本任务 5 个文件 + 任务目录；`origin`/`main` 已验证；见 `## Follow-ups` | 已完成 |
| 未勾选字段是否视为必填 | 是——按 `SKILL.md` 的 PR 规则，未勾选的字段在推送前必须确有对应事实，不得空置 | 已核对 |

## Change Log

- 2026-10-08 work revision — 任务由 `TF-20261008-b1f5e0` promote 创建，并把同批的 `TF-20261008-ee2c27`（重叠上报）与 `TF-20261008-73facd`（父子协调）合并进本任务：三条同改 `SKILL.md` 相邻小节，拆开会在同一批文件上反复撞车；affects `prd.md`, `plan.md`, `TaskFlowDocs/todo.md`。
- 2026-10-08 work revision — Stream 1 落地：验证 `intake` 无 stdout 契约解析方（`hooks/task` / `evals` / `tools` / `.github` 全 0 命中），`Related Tasks` 全仓库无人解析，跨 worktree 任务目录不可见；据此把 R2a 的输出定为 stderr、并把 R3b(3) 记为不可机械强制；affects `prd.md`, `plan.md`。
- 2026-10-08 work revision — Step 1–3 实现并全量验证；R2a 的词面阈值在真实 `todo.md` 上标定后从「Jaccard 或包含度」收敛为 Jaccard + 共享词下限（包含度会把任何含 "README" 的条目判为重叠）；affects `SKILL.md`, `references/artifacts.md`, `hooks/task`, `hooks/smoke-test`。
- 2026-10-08 work revision — Step 4 验证的部分结果记录进 `## Verification / Review` 与 `## Follow-ups`：phase 表与 `concept_class_re` 均未被本任务触及（`git diff` 中无相应用例）、`release-check` 通过、`quick_validate` 因环境缺 PyYAML 无法运行、`git diff --check` 剩一处既有 hook 缺陷产生的尾空格；affects `plan.md`。
- 2026-10-08 work revision — 两处验证缺口关闭：`quick_validate` 改用 conda `torch` 环境（有 PyYAML 6.0.2）运行，`Skill is valid!`；`intake` 标题尾空格作为既有缺陷一并修掉（截断前 rstrip、截断后 `rtrim`），并清掉既有标题上的那一个空格，`git diff --check` 转 CLEAN，另加 smoke 段锁回归；affects `hooks/task`, `hooks/smoke-test`, `TaskFlowDocs/todo.md`, `plan.md`。

## Follow-ups

- R2a 的重叠检测只做词面近似；若误报率值得处理，再考虑更细的启发式或让 Agent 侧完全接管。**实测标定**：token 下限 2 字符、共享词下限 2、Jaccard 阈值 40%（`TASKFLOW_MIN_TOKEN` / `TASKFLOW_MIN_SHARED` / `TASKFLOW_OVERLAP_PCT` 可覆盖，供调参与测试）。曾试过把「较短语覆盖率」也作为触发条件（包含度），在真实 todo 上退化为噪声——它会把 `fix a typo in the README title` 判为与任何提到 README 的条目重叠——已放弃并保留 Jaccard 单测度。
- R3b(3) 的「子任务父版本落后」目前无可执行检查（需跨两个任务目录读 `plan.md`），记为待机制成本被证明后补。
- 本任务落地后，同批其余任务的 `SKILL.md` 变更必须基于本分支合并后的 `main` 起分支。
- `hooks/task` 的 `toksets`/`lcsub` 为 `intake` 而写；若其他子命令也需要词面比较，复用它们而不是再写一份。
- 触发词面重叠报告的第 26 行标题曾带尾空格，来自 `intake` 截断前的旧行为；已随本次修复清掉。`## Removed` 里 `TF-20261008-6b6ecf` 是我验证退出码时误建的探针条目，墓碑理由已写明，不是真实需求。

## Version History

- v1 — 规划中，用户批准；Step 1–3 已实现并通过全量 `smoke-test`。
- 待办：Step 4 的 `git diff --check` 剩一处 trailing whitespace，出在 `TaskFlowDocs/todo.md` 一个由 `intake` 生成的条目标题上（`hooks/task` 在 `cutbytes` 前未去尾空格）。属改动前已存在的 hook 缺陷，不在本任务范围；记于此以免当作本任务引入。
