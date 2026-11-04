# Plan — 归档那次提交不必再等一整轮 CI

> Task version: v2
> Status: completed

No spec required — 只改治理文档的一段，判据由既有 CI 路径分类决定。

## Reference Pointers

- `CONTRIBUTING.md`「Open it as a draft, and mark it ready only once the task's documents are in it」 — 本次要扩写的那段。
- `tools/workflow-affected` — 既有的路径分类，`TaskFlowDocs/*/*` 已在 `none` 集合。
- `.github/workflows/hooks.yml` — `changes` job 与 smoke 矩阵的实际触发。

## Related Tasks

- 来源：TF-20261103-af456a。
- 并行任务 `2026-11-04-skip-guard`，不共享文件。

## Skills / Tools Used

- [PRD] Unaided — considered: requirements elicitation and framing。目标由用户现场说法与既有流程直接决定。
- [Plan] Unaided — considered: work breakdown and task decomposition。单文档一段。
- [Test] Unaided — considered: testing strategy。判据是给人读的治理文本，验证落在 CI 与既有检查，不新增断言。

## Preconditions

- 工作在 `.worktrees/2026-11-04-ci-skip-archive`，分支 `fix/2026-11-04-ci-skip-archive`，基于 `eed6fdf`。
- 用户已选定方向：docs-only 提交可不等待。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-04 14:30 +0800
- Approved version: v2
- Approved scope: PRD / Plan

## Steps

### Step 1 — 在 CONTRIBUTING 写入免等判据

- Goal: PR 章节写清「最后一次 push 只动任务自己的目录时，不必等那一轮 CI」。
- Dependencies: 无。
- Files: `CONTRIBUTING.md`
- Implementation checklist:
  - [x] 在「Open it as a draft…」那段之后新增一段 `### When the last push does not have to wait for CI`。
  - [x] 判据：最后一次 push 的 diff 全部落在 `TaskFlowDocs/` 之下（任务目录、`achieved/`、`todo.md`）。
  - [x] 前提：代码提交那一轮 CI 已绿，且 PR body 记录了该 run。
  - [x] 判据之外由路径集合本身排除：`hooks/`、`skills/`、`.github/`、manifest、README、`CONTRIBUTING.md` 都不在 `TaskFlowDocs/` 下。
  - [x] 给出「不适用」的例子（代码那轮 CI 未绿）。
  - [x] 说明这是**省等待**，不是省 CI 运行：main 的 push 照常跑全矩阵。
- Acceptance: AC1–AC4。
- Verification: `bash hooks/repository-check .`；`git diff --check`；CI 结果。
- Rollback: `git checkout -- CONTRIBUTING.md`。
- Status: done

## Checkpoints

- 判据写成路径集合 `TaskFlowDocs/` 而不是「只动文档」：`repository-docs/` 与 README 也能被叫作文档，而它们不在该路径下。

## Verification / Review

- **AC1/AC2/AC3 — 通过。** 新节 `### When the last push does not have to wait for CI` 写明了路径判据（每条都在 `TaskFlowDocs/` 之下）、检查命令 `git diff --name-only <base>...HEAD`、前提（代码提交那轮 CI 已绿且 PR body 命名该 run）、以及不改变 CI 运行只改变等待的说明。
- **AC4 — `bash hooks/repository-check .` STATUS: pass；`git diff --check` clean。**
- **事实依据已逐条核对**（v1 在这一点上是错的，v2 更正）：`hooks/smoke-test:2786` 与 `:2808` 是 smoke 唯一读 `todo.md` 的地方，两处都在 `## Item template` 一节；`hooks/archive` 只重写 `## Items` 下的条目。`tools/workflow-affected` 把 `TaskFlowDocs/*/*` 归入 none 集合，`todo.md` 归入 smoke 集合——这一点没有变，但 `archive` 的输出不会改变模板，所以该断言不会因归档而变红。
- **残余风险已写在 PRD**：`TaskFlowDocs/` 内的提交不经 CI 进 main；由「代码那轮已绿」和「该路径集对套件无输入」两条共同承担。

## Change Log

- v1 — 初始计划。

## Follow-ups

- 若判据被误用，升级为机器检查（PR label 或 pre-merge 脚本）。

## Version History

- v1 — planning.
- v2 — R2 corrected; back to planning for re-approval.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-11-03 用户的现场说法**：提交 PR 时，CI 已过、PR 格式也改完，只差合并——这时可以先归档，然后一并合并，减少一次「为归档记录再推一次、又触发一整轮 CI」的往返。
  **现状为什么多一次**：`CONTRIBUTING.md` 的发布顺序是 `push → 读 CI → 把 CI 结果写进 Plan → 提交推送 → 归档 → 提交推送 → gh pr ready`。归档之后那次 push 会**再触发一整轮 three-host 矩阵**，而这一轮在语义上几乎不可能失败——它只动了 `TaskFlowDocs/` 里的文档和 `todo.md`。
  **要定的判据**：什么条件下允许「归档前 CI 已绿、归档这一推不再等 CI」。候选是「归档提交只触及 `TaskFlowDocs/**`」，与既有的 CI 路径过滤器（`2026-10-20-ci-path-filter`）同源。注意不能放宽成「任何提交都不等」——`smoke-test` 对 `todo.md` 有断言，`archive` 也会改 Todo 条目。
