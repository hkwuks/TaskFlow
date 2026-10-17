# Plan — The entry signal for unregistered work never fires in the state a session actual

> Task version: v1
> Status: completed

No spec required — 改动集中在 `hooks/summarize-state` 的条件与输出顺序，无跨层契约、无数据结构变更、无兼容性决策。唯一有设计成分的是 R1 的单一判据与 R3 的解耦，其边界与已知后果已界定在 PRD 的 D1–D3。

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — 适用的仓库文档与阶段。
- `CONTRIBUTING.md:18` / `:20-32` — 「Never implement in the base working tree」与分支前缀；本任务的分支名与隔离依据。
- `.github/pull_request_template.md` — phase `pr` 的适用文档；Step 3 逐字段映射。
- `hooks/README.md` — hook 清单与 SessionStart 的边界。
- `skills/taskflow/references/runtime.md` — SessionStart 的 must / may-not 边界（只读、可失败、不写核心文档）。
- `capability-gate:66-68` — 「a gate that silently stops gating is worse than no gate」；D1 的押注依据。
- `TaskFlowDocs/achieved/2026-10-10-entry-point-silence/` — 上一轮补静默的任务，其三段输出的守卫与注释是本条的直接前身。

## Related Tasks

- Parent: None.
- Children: None.
- Depends on: None.
- Blocks: None.
- Related:
  - `TF-20261009-cc463b`（done）— 母条目，其第四、第五失败模式即本条来源。
  - `TF-20261001-efbc51`（done，`achieved/2026-10-11-evidence-anchor/`）— hook 侧锚点修复，cc463b 第五模式记录的等待对象，已解除；其范围与本条不重叠（见 PRD B5）。
  - `TF-20261012-c79e31` / `TF-20261012-c66ad3`（inbox）— 同属 2026-10-12 发现的记账层问题，与本条无依赖。

## Skills / Tools Used

- [PRD] Unaided — no capability applied to this phase; considered: requirements elicitation and framing, divergent exploration
- [Plan] Unaided — no capability applied to this phase; considered: work breakdown and task decomposition

两阶段都用 `hooks/task unaided` 声明。本阶段的工作是读本仓库自己的 hook 与其 smoke 断言（`summarize-state:27/54/84-96`、`smoke-test:48-132`），核对其间的约束；方案三个决定已由用户 2026-10-12 裁定，没有外部能力可补充这些文件未承载的信息。定性为**收敛型**：目标与路径都已固定，不存在需要发散探索的候选方向。

## Preconditions

- [x] 适用的仓库文档与个人规则已检查、优先级/冲突已记录。`repository-docs/index.md` 路由 `CONTRIBUTING.md`（design,code,commit,pr,release）、`CODE_STYLE.md`（code,review）、`RELEASE.md`（release）、`.github/pull_request_template.md`（pr）。无仓库文档规范 SessionStart 的输出内容，无冲突。本 clone 无个人规则（`personal.md` 不存在）。
- [x] 远程/fork/PR 工作：`origin` = `hkwuks/TaskFlow`，base = `main`（`git symbolic-ref refs/remotes/origin/HEAD` = `refs/remotes/origin/main`），本分支从 `6f0c4bf` 起。Step 3 在任何推送前复核。
- [x] PR 模板：`.github/pull_request_template.md` 为 phase `pr` 的适用文档；Step 3 逐字段映射并记录模板路径与验证。
- [x] 缺失治理草案与显式批准：不适用——本任务不创建任何缺失的治理文档。
- [x] 核心文档单一写者：Primary Agent（Claude）。分支 `fix/summarize-state-entry-signal`，worktree `.worktrees/2026-10-17-summarize-state-entry-signal`。
- [x] 既有用户裁定已记录：三个决定（走完整流程 / 触发条件为无活跃任务 / base 解析不做）见 PRD Open Questions 与 R1、R6。
- [x] 隔离先于第一份文档：worktree 与分支在任何 `TaskFlowDocs/` 文件之前创建；`promote` 在该工作树内运行。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-17 21:49 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 把义务句的触发判据改为「没有活跃任务」

- Goal: `summarize-state` 在「没有任何活跃任务」的三种形态下各说一次义务句，在有活跃任务时一字不说；分支报告与义务句解耦；输出仍然惰性。除这三处外，其余输出与字节不变。
- Dependencies: None.
- Files: `hooks/summarize-state`。
- Implementation checklist:
  - [x] R1：第 27-34 行与第 54-70 行两段合并退出，改为在 `active` 建好后求值的单一判据。义务句的字面量 `Applicable work enters TaskFlow` 与 `TaskFlowDocs/todo.md` 原样保留。
  - [x] R1：新判据放在 `active` 数组（现 98-105 行）**之后**；两段提前退出随之删除。
  - [x] R1/A6：状态短句随形态变化。**偏离原清单一处**：原写「用 `nothing recorded yet` 字面量」，实际改为两种标题——`# TaskFlow (not started in this repository)`（无任何记录证据）与 `# TaskFlow (no active task)`（有 `todo.md` 或扩展条目）。理由：「nothing recorded yet」对「已用过、只是没有在办任务」的仓库是**假的**，而那个形态正是本条要补的；A6 禁止谎报，故弃用该字面量（详见 `## Verification / Review` 的「对验收面的偏离」）。
  - [x] R2：`active` 非空时义务句不出现。
  - [x] R3/R4：义务句在基检出（`main`）上出现；`No task for branch` 的判据一行未改（仍含 `achieved/` 匹配）。
  - [x] R5：新路径全部走 `echo` 到 stdout 并落到既有的 `exit 0`，不创建任何文件或目录。
  - [x] B4：新代码只用 `echo`/`[ ]`/`case`/`for`/数组长度，未引入新 bashism 或任何解释器。
- Acceptance: PRD A1、A2、A4、A6。
- Verification: 四种形态手跑，输出与 A1–A4、A6 逐条对上（见 `## Verification / Review`）。
- Rollback: revert `99e4eb2`。
- Status: done

### Step 2 — 改写被取代的断言，并钉住新行为

- Goal: 让 R1/R2/R3 由检查而不是靠人记着；把两条锁旧行为的断言按新行为改写并注明是有意的行为变更。
- Dependencies: Step 1.
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 改写 `smoke-test:77`：由「`todo.md` 一存在入口行就不许出现」改为「有 `todo.md`、无活跃任务时义务句必须在，且标题必须是 `no active task` 而不是 `not started in this repository`」；节注释写明这是有意变更及其理由。
  - [x] 改写 `smoke-test:123`：`branch_says` 全部保留，并新增一段用**同一个仓库、同一个 commit** 断言基分支与未登记分支的差别——基分支：义务句在、`No task for branch` 不在；未登记分支：两者都在。
  - [x] 新增 R2 反向断言：同一 `bare` fixture 内加一个活跃任务 → 义务句不出现（防噪声回潮的那条）。
  - [x] 新增 R1 正向断言：有 `todo.md`、无活跃任务 → 义务句在、含两个字面量、且不出现 `not started in this repository`。
  - [x] `Applicable work enters TaskFlow` 与 `TaskFlowDocs/todo.md` 两个字面量断言保留；`nothing recorded yet` 的断言随该字面量一并撤下（见 Step 1 的偏离说明）。
  - [x] 新断言只用既有 POSIX 工具，无撇号嵌在 `$( )` 的 heredoc 中；bash 3.2 解析通过。
- Acceptance: PRD A2、A3。
- Verification: `bash hooks/smoke-test </dev/null` 全量通过（72 节 `ok`）；两个变异方向各红一次后恢复全绿（见 `## Verification / Review`）。
- Rollback: revert `85a3e14`。
- Status: done

### Step 3 — 全量验证与收尾

- Goal: 确认没有打破既有断言与无解释器不变量，并留下可复核的记录。
- Dependencies: Step 1, Step 2.
- Files: 本任务 `plan.md`（验证记录）、`TaskFlowDocs/todo.md`（状态）。
- Implementation checklist:
  - [x] `bash hooks/smoke-test </dev/null` 全量（72 节 `ok`，`ALL SMOKE PASSED`）；`no interpreter available` 一节仍通过（A5）。
  - [x] `git diff --check` → `CLEAN`。
  - [x] `bash hooks/release-check .` → `STATUS: pass`。
  - [x] `quick_validate.py skills/taskflow` → `Skill is valid!`。
  - [x] `bash -n hooks/summarize-state` 与 `bash -n hooks/smoke-test`；`docker run bash:3.2` 对两文件解析通过。
  - [x] 在 `## Verification / Review` 记录每条命令与结果，并记录两个方向的变异验证。
  - [x] 读 `.github/pull_request_template.md`，逐字段映射并记录模板路径与验证结果。
  - [x] 推送后 CI 三 host 矩阵结果：结果落在 PR 正文（`CONTRIBUTING.md:43`：landing claim 记在 PR 里，不写回任务文档）。本行保留为改前写下的判据，事后按它核对，不按结果改写。
- Acceptance: PRD A5。
- Verification: 上述命令输出逐条记录在 `## Verification / Review`。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

## Checkpoints

- CP1（Step 1 后）：四种形态 × 两种分支的手跑结果与 PRD A1–A4、A6 逐条对上；**有活跃任务时义务句必须不出现**（否则每个在办会话都被念，噪声）。
- CP2（Step 2 后）：两个方向的变异各触发一次失败，恢复后全量通过；`no interpreter` 一节未被新代码破坏。
- CP3（Step 3 收尾）：全套命令通过、验证记录与 PR 模板映射写入本文件、CI 绿。

## Verification / Review

记录格式：逐条命令与结果。区分 **既有失败** / **新引入失败** / **环境失败**。

### 对验收面的偏离（先说，因为它改了计划里写下的一个字面量）

**Step 1 原清单要求复用 `nothing recorded yet` 字面量；实现时没有复用，这是有意的偏离。**

那个字面量对「**已经用过** TaskFlow、只是当前没有在办任务」的仓库是**假的**——它已经记录过东西。而那个形态正是本条要补的那一个（`todo.md` 存在、`active` 为空）。PRD A6 明写「有扩展任务时不得说 nothing recorded yet」，所以保留该字面量会直接违反同一份 PRD 的验收面。改法是两种标题：

| 形态 | 标题 | 理由 |
| --- | --- | --- |
| 无任何已记录证据 | `# TaskFlow (not started in this repository)` | 与旧文案一致 |
| 有 `todo.md` 或扩展条目 | `# TaskFlow (no active task)` | 陈述当前状态，不谎报历史 |

义务句两行（`Applicable work enters TaskFlow …`、`Read-only work …`）在两种形态下**逐字相同**。属性上仍满足 PRD R1 的「三种形态文案可以不同，触发条件必须只有一个」。已记入 Change Log。

### 手跑：四种形态

| 形态 | 分支 | 输出 | 判定 |
| --- | --- | --- | --- |
| 无 `todo.md`、无扩展条目 | 基分支 | `not started in this repository` + 义务句 + `# Active tasks` | 通过（A4） |
| 有 `todo.md`、无活跃任务 | 基分支 | `no active task` + 义务句 + inbox + `# Active tasks` | **通过（A2，本轮修复点）** |
| 同上 | `fix/never-registered` | 义务句 + 分支报告 | 通过（A3） |
| 有活跃任务 | 基分支 | 只有 `# Active tasks` + 任务行 | 通过（A1、R2） |

A4 的「不创建任何文件」：四种形态跑完后 fixture 里只有脚本自己没碰过的原文件；无 `TaskFlowDocs/` 的形态跑完后（改前）亦未产生目录（`smoke-test` 的 no-docs 一节在守）。

### 命令与结果

| 检查 | 结果 | 分类 |
| --- | --- | --- |
| `bash hooks/smoke-test </dev/null`（全量） | exit 0，`ALL SMOKE PASSED`，**72** 节 `ok`（改前同为 72：改写了 2 节、新增断言在既有节内） | 通过 |
| **变异 1**：把义务句判据改回 `[ ! -d "$docs" ]` | `FAIL unrecorded-repo output does not name the first record` | 断言有效（R1 被咬住） |
| **变异 2**：把判据改成 `if true`（去掉活跃任务抑制） | `FAIL the obligation line survived an active task` | 断言有效（R2 反被咬住） |
| 恢复两处后重跑全量 | `ALL SMOKE PASSED`，`git diff --stat` 为空 | 通过 |
| `git diff --check` | `CLEAN` | 通过 |
| `bash hooks/release-check .` | `STATUS: pass`（版本字面量 1.1.5 一致，catalog pin 指向 `93dcec3`） | 通过 |
| `quick_validate.py skills/taskflow` | `Skill is valid!`（`/home/hk/miniconda3/envs/torch/bin/python`） | 通过 |
| `bash -n hooks/summarize-state`、`bash -n hooks/smoke-test` | 无输出 | 通过 |
| `docker run --rm -v "$PWD:/w" -w /w bash:3.2` 对两文件 `bash -n` | `bash 3.2 OK` | 通过（B4、A5） |
| 无解释器不变量 | `smoke-test` 的 `hooks run with no interpreter available` 一节仍 `ok`；新增代码只用 `echo`/`[ ]`/`case`/`for`/数组长度 | 通过 |

**未做的检查与限制**：CI 三 host 矩阵由推送后的 CI 裁决，本地不重跑。`smoke-test` 的 `dsh wiring` / `Trae wiring` 两节会创建 `sessions.md`（既有行为，非本轮引入），本次全量跑里同样出现，未改动其断言。

### PR 模板映射（`.github/pull_request_template.md`，phase `pr` 的适用文档）

模板路径已核对（4 节）。每个字段的映射：

| 模板字段 | 落点 | 状态 |
| --- | --- | --- |
| Summary | PR 正文首节——义务句的投放条件与适用条件相反，以及改判据后的四种形态 | 待推送后写入 |
| TaskFlow traceability: Task | `TaskFlowDocs/2026-10-17-summarize-state-entry-signal/` | 已确定 |
| TaskFlow traceability: Scope | PRD 的 In Scope：`hooks/summarize-state`、`hooks/smoke-test`、本任务文档、`todo.md` 状态 | 已确定 |
| TaskFlow traceability: Base branch | `main`（`origin` = `hkwuks/TaskFlow`），本分支从 `6f0c4bf` 起 | 已验证 |
| TaskFlow traceability: Target repository | `hkwuks/TaskFlow`，凭据不写入 | 已验证 |
| Verification: Hooks workflow pass | PR 正文（run 链接写在那里，不写回本文件） | 已由 PR 承载 |
| Verification: `git diff --check` | 见上表：`CLEAN` | 已记录 |
| Verification: Relevant Skill/plugin validation | `quick_validate` `Skill is valid!`、`release-check` `STATUS: pass` | 已记录 |
| Verification: Results recorded in the TaskFlow Plan | 本节 | 已完成 |
| Review boundaries（4 条） | 无凭据写入；`git status` 仅本轮 2 个 hook + 任务目录 + `todo.md`；`origin`/`main` 已核对；见 `## Follow-ups` | 已完成 |

## Change Log

- 2026-10-17 work revision — 任务由 `TF-20261012-50164f` promote 创建；用户 2026-10-12 的三个设计决定（按 small task 走完整流程 / 触发条件为「没有任何活跃任务时印」/ base 分支解析不做并另记）写入 PRD R1、R6 与本 Plan 的 Preconditions；affects `prd.md`, `plan.md`, `TaskFlowDocs/todo.md`。
- 2026-10-17 work revision — **表达层偏离**：义务句的状态标题由复用的 `nothing recorded yet` 改为 `not started in this repository` / `no active task` 两分。原因是该字面量对「已用过但没有在办任务」的仓库不成立，而 PRD A6 禁止这种谎报；属性上仍满足 R1（触发条件单一、文案可随形态不同）。不影响任何 requirement 或验收判据，故不提升 Task 版本；affects `hooks/summarize-state`, `hooks/smoke-test`, `plan.md`。
- 2026-10-17 work revision — Step 1/2 实现完成并提交（`99e4eb2`、`85a3e14`）；四种形态手跑通过，两个变异方向各红一次后恢复全绿；affects `plan.md`。

## Follow-ups

- 若 D1 的噪声风险实测成立（义务句被当噪声忽略），收紧触发条件为「无活跃任务 **且** Todo 内存在 inbox 条目」。
- base 分支解析（R6）：把 `case "$current_branch" in ""|main|master)` 改成解析 `git symbolic-ref refs/remotes/origin/HEAD`，并处理无远程时的失败分支；用户 2026-10-12 裁定另记。
- 陈旧工作树的形态（D2）：`active` 为空的工作树多出一行义务句，而分支 slug 仍匹配 `achieved/`，分支报告不出现（R3 只解耦两者，未改分支报告判据）。若实测噪声，考虑把 `achieved/` 从分支报告的扫描里移出，但那时需要另一条判据区分「陈旧工作树」与「未登记工作」。
- `summarize-state` 的 120 字节 goal 截断（`substr(g,1,120)`，字节级、断在词中、无标记）使 inbox 条目可被误读为更小的真实条目；`TF-20261012-50164f` 的 Notes 记录了一次由此产生的幽灵需求。属 `TF-20260919-6b4e21` 那一类，另记。

## Version History

- v1 — planning，等待用户批准。
