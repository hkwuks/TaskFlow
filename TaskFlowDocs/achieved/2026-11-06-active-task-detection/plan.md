# Plan — 修复活跃任务识别：按证据而非目录顺序
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/task` — 缺陷所在；`unaided` 与 `external` 两个分支。
- `CODE_STYLE.md:16` — 退出码约定，决定拒绝用 `2` 而非 `fail` 的 `1`。
- `skills/taskflow/references/runtime.md:270,273` — `TASKFLOW_TASK_ID` 的既有语义。
- `hooks/smoke-test:1996` 起 — 新增断言插在 `task approve` 段之前。
- `TaskFlowDocs/achieved/2026-11-06-*` — 无；本任务是 `TF-20261106-3efcd7` 的落地。

## Related Tasks

- 无。缺陷独立，不依赖其他任务的产物。

## Skills / Tools Used

- [PRD] Unaided — 需求来自用户给出的缺陷描述与仓库内已确认事实；considered: requirements elicitation
- [Plan] Unaided — 单步修复，无需拆解工具；considered: work breakdown
- [Test] Unaided — 复用仓库既有的 smoke 断言与变异验证方式；considered: testing strategy

## Preconditions

- 本 worktree 在 `fix/active-task-detection` 分支上。
- `repository-check` 开工前为 pass。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-06 23:43 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 用 resolver 替换两处重复循环

- Goal: 新增 `active_task_names` 与 `resolve_active_task`，把 `unaided` 与 `external` 的目录序猜测换掉。
- Dependencies: 无
- Files:
  - `hooks/task`
- Implementation checklist:
  - [x] 新增 `active_task_names <root>`：列出全部活跃任务。
  - [x] 新增 `resolve_active_task <root>`：`TASKFLOW_TASK_ID` → cwd → 唯一；否则拒绝并列出候选。
  - [x] `unaided` 改用 resolver，拒绝码保留 `2`。
  - [x] `external` 改为只检查存在性，不再解析名字。
- Acceptance: PRD 第 1、2、3、4、5、6 条。
- Verification: 手工 fixture 覆盖四条路径；`bash hooks/smoke-test`。
- Rollback: `git checkout -- hooks/task`。
- Status: done

### Step 2 — 断言与变异验证

- Goal: 在 `hooks/smoke-test` 增加覆盖，并证明断言能捕获旧行为。
- Dependencies: Step 1
- Files:
  - `hooks/smoke-test`
- Implementation checklist:
  - [x] 新增 `== a stage declaration names its task by evidence, never by directory order ==` 段。
  - [x] 断言字母序第一的任务**不是**被选中的那个（否则旧实现也能通过）。
  - [x] 变异验证：退回目录序、拒绝码改 1、忽略 `TASKFLOW_TASK_ID`。
- Acceptance: PRD 的最后两条验收。
- Verification: 三个变异各自触发不同断言。
- Rollback: `git checkout -- hooks/smoke-test`。
- Status: done

### Step 3 — 文档

- Goal: 在 `runtime.md` 记录解析顺序。
- Dependencies: Step 1
- Files:
  - `skills/taskflow/references/runtime.md`
- Implementation checklist:
  - [x] 在 `unaided`/`external` 相关段落说明 resolver 的三个来源与拒绝行为。
- Acceptance: 文档与实现一致。
- Verification: 读回核对。
- Rollback: `git checkout -- skills/taskflow/references/runtime.md`
- Status: done

## Checkpoints

- Step 1 + 2 后：本地 smoke 全绿再进 Step 3。

## Verification / Review

**改了什么**

| 文件 | 改动 |
| --- | --- |
| `hooks/task` | 新增 `active_task_names`、`resolve_active_task`；`unaided` 改用 resolver 并把拒绝码透传为 `2`；`external` 改为只判存在性 |
| `hooks/smoke-test` | 新增 12 条断言，含旧实现的直接反例 |
| `skills/taskflow/references/runtime.md` | 记录解析顺序 |

**手工验证（fixture 覆盖四条路径）**

| 场景 | 结果 |
| --- | --- |
| 两个任务、cwd 在仓库根 | 拒绝，exit 2，列出两个候选 |
| cwd 在字母序第二的任务目录 | 记录到该任务 |
| cwd 在该任务的 `reference/` 子目录 | 记录到该任务 |
| `TASKFLOW_TASK_ID` 覆盖 cwd | 记录到指定的那个 |
| `TASKFLOW_TASK_ID` 指向不存在 | 拒绝，exit 2，列出候选 |
| 只剩一个任务、cwd 在根 | 直接解析成功 |

**变异验证**

| 变异 | 结果 |
| --- | --- |
| resolver 退回「取字母序第一」 | caught — `FAIL ambiguous declaration exited 0, not 2` |
| 拒绝码改为 `fail`（exit 1） | caught — `FAIL ambiguous declaration exited 1, not 2` |
| 忽略 `TASKFLOW_TASK_ID` | caught — `FAIL cwd overrode an explicit TASKFLOW_TASK_ID` |

第一个变异是这次修复的核心证据：把旧行为放回去，断言确实变红。

**其他检查**

| 检查 | 结果 |
| --- | --- |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED`，exit 0 |
| `git diff --check` | 通过 |
| CI 三宿主矩阵 | PR #123，run [42245953034](https://github.com/hkwuks/TaskFlow/actions/runs/42245953034) | 
| └ smoke macOS / Ubuntu / Windows | pass |
| └ evals / changes / todo-merge-audit | pass |

具体：`smoke (macos-latest)`、`smoke (ubuntu-latest)`、`smoke (windows-latest)`、`evals`、`changes`、`todo-merge-audit` 六项全部 pass；`release` 按预期 skipping。本地 smoke 只是预检，CI 是判定。

## Change Log

- v1 — 初始计划；同日完成三个 Step 并记录验证。

## Follow-ups

- 若后续觉得环境变量别扭，可加 `--task` 作为 `TASKFLOW_TASK_ID` 的同义写法；届时两者应共用一个入口，避免第二个猜测点。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-11-06 用户原话**：「审批辅助命令暴露了一个旧任务布局限制：它按目录顺序识别活跃任务，无法准确给当前任务补录阶段记录。我不会改全局 TaskFlow 工具或伪造记录；会在当前计划中注明原因，并手工转录你已经给出的批准，然后继续实现」
  **根因（已读代码确认）**：hooks/task 的 unaided 分支（第 1166-1174 行）与 external-evidence 分支（第 1293-1301 行）用同一段循环找活跃任务：
    for dir in "$root"/TaskFlowDocs/*/; do ... if [ -f "$dir/plan.md" ]; then active="$name"; break; fi; done
  它取的是 glob 展开后**字母序第一个**含 plan.md 的目录，与调用者的 cwd、分支、当前任务毫无关系。同一棵树里只要有两个未归档任务目录，就可能给错的那个补录记录——而记录一旦写进 released，approve 会拿它去对账，等于把一个任务的证据记到另一个任务上。
  **为什么现在才暴露**：隔离规则要求一任务一 worktree，正常情况下每个 worktree 只有一个任务目录，因此这个缺陷在常规流程里不可见。它在两种情形下现形：任务文档被复制/合并进同一棵树（例如从别的分支取文档），或在一个 worktree 里同时存在父任务与子任务的目录。
  **用户已作出的决定**：不改全局工具、不伪造记录，在 plan.md 里注明原因并手工转录已给出的批准。这是正确的取舍——为了补一条记录去改证据写入逻辑，正是 SKILL.md Phase 5 禁止的「让检查看起来通过」。
  **修复方向（待澄清时定）**：候选一，让 active 取 cwd 所在的任务目录（cwd 在 TaskFlowDocs/<slug>/ 内时直接用，否则回落到现有顺序并在有歧义时报错）；候选二，加 --task 参数显式指定；候选三，两个都做——显式参数优先，cwd 推断次之，多任务且无法判定时拒绝并列出候选。倾向候选三，因为「静默选错」是这个缺陷的全部危害，而拒绝是唯一不猜答案的选项。
