# Plan — 归档那次提交不必再等一整轮 CI

> Task version: v1
> Status: planning

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
- Approved at: 2026-11-04 13:55 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 在 CONTRIBUTING 写入免等判据

- Goal: PR 章节写清「最后一次 push 只动任务自己的目录时，不必等那一轮 CI」。
- Dependencies: 无。
- Files: `CONTRIBUTING.md`
- Implementation checklist:
  - [ ] 在「Open it as a draft…」那段之后新增一段，标题与既有风格一致。
  - [ ] 判据：最后一次 push 的 diff 全部落在 `TaskFlowDocs/<task>/` 或 `TaskFlowDocs/achieved/<task>/`。
  - [ ] 前提：代码提交那一轮 CI 已绿，且 PR body 记录了该 run。
  - [ ] 显式排除：`TaskFlowDocs/todo.md`、`TaskFlowDocs/repository-docs/`，以及任何 `hooks/`、`skills/`、`.github/`、manifest 改动。
  - [ ] 给出一个「不适用」的例子（归档同时改 todo.md）。
  - [ ] 说明这是**省等待**，不是省 CI 运行：main 的 push 照常跑全矩阵。
- Acceptance: AC1–AC4。
- Verification: `bash hooks/repository-check .`；`git diff --check`；CI 结果。
- Rollback: `git checkout -- CONTRIBUTING.md`。
- Status: pending

## Checkpoints

- 判据写成路径集合，不写成「只动文档」——后者会把 `todo.md` 一并放进来，而它是有断言的。

## Verification / Review

（实现后填写）

## Change Log

- v1 — 初始计划。

## Follow-ups

- 若判据被误用，升级为机器检查（PR label 或 pre-merge 脚本）。

## Version History

- v1 — planning.
