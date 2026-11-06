# Plan — 修复活跃任务识别：按证据而非目录顺序
> Task version: v1
> Status: in_progress

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

CI 三宿主矩阵在推送后读取。

## Change Log

- v1 — 初始计划；同日完成三个 Step 并记录验证。

## Follow-ups

- 若后续觉得环境变量别扭，可加 `--task` 作为 `TASKFLOW_TASK_ID` 的同义写法；届时两者应共用一个入口，避免第二个猜测点。

## Version History

- v1 — planning.
