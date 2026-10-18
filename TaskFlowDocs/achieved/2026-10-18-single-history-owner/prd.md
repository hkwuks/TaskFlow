# 让 Task 版本史只有一个归属文档

> Task version: v1
> Status: completed

## Goal

`> Task version:` 的演进史（`## Version History`）现在在 `prd.md` 与 `plan.md` 里各写一份，两份都由人手维护、会漂移；把归属收进 `plan.md` 一份。

## Background / Confirmed Facts

- `hooks/task promote` 同时给 `prd.md` 与 `plan.md` 写骨架，两份骨架里都有 `## Version History`（`hooks/task:778`、`hooks/task:837`）。
- `skills/taskflow/references/artifacts.md` 的 PRD outline（`:64`）与 Plan outline（`:120`）同样各列一次。
- 归档任务实测（`TaskFlowDocs/achieved/` 75 个目录，按 `^## Version History` 统计）：`prd.md` 有 70、`plan.md` 有 73、`spec.md` 有 0、两份都有 70。**71% 的任务在两份文档里各维护一份版本史。**
- `## Version History` 全仓库没有读取方：命中全是写出方（`hooks/task:778`、`hooks/task:837`、`artifacts.md:64`、`artifacts.md:120`）。没有 hook、测试或 eval 解析它，它也不在语言规则的英文边界名单里（`references/artifacts.md:23`）。
- 版本号本身已经是 Plan 归属：`hooks/version:17` 从 `plan.md` 读 `> Task version:`；`hooks/task` 的 `require_approval`（`:643-644`）、`hooks/capability-gate:116`、`hooks/session-record:60,73`、`hooks/summarize-state:54,159,214` 全部读 `plan.md`。`references/versioning-and-recovery.md:11` 已写明「`plan.md` 拥有 Task 版本；`prd.md`/`spec.md` 为可读性重复它」。
- 惯例已在向这个方向漂：最近四个任务里有三个（`2026-09-30-release-ci-test-policy`、`2026-10-01-taskflow-commit-path`、`2026-10-17-stage-capability-pairing`）只在 `plan.md` 保留了这一节。

## Requirements

- `plan.md` 是 `## Version History` 的唯一归属文档；`prd.md` 与 `spec.md` 都不再持有该节。
- `hooks/task promote` 写的 `prd.md` 骨架不再包含该节；`plan.md` 骨架保持不变。
- `references/artifacts.md` 的 PRD outline 不再列该节；Plan outline 保持列出。
- `SKILL.md` 里把「current Task version and version history」列为 PRD 应含内容的条目，改为只要求 Task 版本，历史指向 Plan。
- 新增一条 smoke 断言：`promote` 产生的 `prd.md` 不含 `^## Version History$`，而 `plan.md` 含。
- 已归档文档与既有活动任务目录一律不改写（`TaskFlowDocs/achieved/` 是只读历史）。

## Acceptance Criteria

- 在干净 fixture 上跑 `hooks/task promote`，产出的 `prd.md` 无 `## Version History` 节，`plan.md` 有。
- 产出的 `prd.md` 仍带 `> Task version: v1`（`hooks/version` 依赖它：`:16,31-35,134-137`）。
- `bash hooks/smoke-test` 全绿；把骨架改回去时新断言变红。
- 全仓库对 `## Version History` 的引用只剩 Plan 侧（骨架 + Plan outline）。
- `bash hooks/repository-check .`、`git diff --check`、`quick_validate.py skills/taskflow` 全部通过。

**真实收益（口径）**：没有任何东西在 bump 时往这一节追加内容——`hooks/version` 只改 `> Task version:` 行。所以保留下来的那份是**结构性过期**的：v2 的 PRD 会永远写着 `- v1 — planning.`。删掉它消除的是这一整类过期，而不只是少一份重复。

**定价**：PRD 少了版本史后，「这个 PRD 是 v2 的、v1 改了什么」要在两份文档间跳转。`> Task version:` 仍在 PRD 里，`old/vN/` 仍是权威存档。

## In Scope

- `hooks/task` 的 `promote` 分支（`prd.md` 骨架的字面量，`:777-780`）。
- `hooks/smoke-test`（在 `== task lifecycle dispatcher ==` 段新增断言）。
- `skills/taskflow/SKILL.md:208`（整项删除）。
- `skills/taskflow/references/artifacts.md:64`（PRD outline 一行）。
- 本任务自身的文档与 `TaskFlowDocs/todo.md` 的条目（按 `CONTRIBUTING.md` 随任务一起进 PR）。

## Out of Scope

- `hooks/version` 的行为：本次不让它在 bump 时自动写历史（用户 2026-10-18 选定「只改骨架与文档」）。
- `## Change Log` 的归属（它已经是 `plan.md` 独占）。
- `skills/taskflow/references/versioning-and-recovery.md`：其 `:11` 讲的是 `> Task version:` **字段**的归属，不是这一节，改了反而是错的。
- `skills/taskflow/references/artifacts.md:29`：那句仍在 `hooks/smoke-test:1550` 的 clause-pin 循环里，且改后依然为真。
- 任何 `TaskFlowDocs/achieved/` 下的文档改写。
- `CHANGELOG.md`：本次改动不发布，按 `RELEASE.md` 该节由发布事务写。
- `hooks/version`、`hooks/archive`、`hooks/reopen` 的既有行为。

## Risks / Deferred Items

- **风险**：`prd.md` 少了版本史后，读者要在两份文档间跳转才能看清版本演进。缓解：`> Task version:` 仍在 PRD 里，`old/vN/` 仍是权威存档，`plan.md` 的 `## Change Log` + `## Version History` 是唯一演进记录。
- **已声明不做**：让 `hooks/version` 自动维护该节——留作后续（列在 Plan 的 Follow-ups）。
- 既有活动任务目录里的 PRD 仍带着这一节；本次不回填、不清理（`achieved/` 是只读历史，活动任务也不做追溯适用）。
- **唯一一处为「共享版本边界」说话的措辞**是两份 README 里那句「one shared set of task facts and version boundaries」（`README.zh-CN.md:31` 及英文对应）。它讲的是任务事实与版本边界的**共享**，不是「PRD 必须自带历史节」，但仍要在 Step 1 里判断是否顺带澄清；`CODE_STYLE.md:8` 要求两份 README 行为对齐，动则两份一起动。

## Open Questions

无阻塞问题。

## Version History

- v1 — planning：把 `## Version History` 的归属收进 `plan.md`，PRD 只留 `> Task version:`。
