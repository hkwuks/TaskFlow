# 归档那次提交不必再等一整轮 CI

> Task version: v2
> Status: completed

## Goal

PR 的收尾路径是 `push → 读 CI → 把 CI 结果写进 Plan → 提交推送 → 归档 → 提交推送 → gh pr ready`。后两次推送各自触发一整轮三平台矩阵，而它们的 diff 只落在 `TaskFlowDocs/**`——语义上几乎不可能失败。要让这类仅文档的收尾提交（含归档）不必等待新一轮 CI 就能合并，从而少一次往返。

## Background / Confirmed Facts

来源：Todo 条目 TF-20261103-af456a（用户 2026-11-03 现场提出）。

- 现状的两轮等待各有来源，都不是必要的：`CONTRIBUTING.md`「Open it as a draft, and mark it ready only once the task's documents are in it」要求验证记录与归档都进同一个 PR，因此它们必然在代码提交之后、且在 CI 之后。
- PR #113 的实际耗时里，这两轮的 CI 都是全绿，失败的那次是 macOS runner 未分配到——与文档提交无关。
- CI 路径过滤器已经能把 `TaskFlowDocs/*/*`（任务目录、`achieved/`）判为「任何 job 都不需要跑」（`tools/workflow-affected` 的 `none` 集合）。但 `changes` job 本身、以及 PR 上的 required checks 仍会被这一轮触发。
- `TaskFlowDocs/todo.md` **是** smoke 输入，但只在一处：`hooks/smoke-test:2786,2808` 读它的 `## Item template` 一节，而 `hooks/archive` 只改 `## Items` 下的条目，从不碰模板。所以归档对 `todo.md` 的改写不会让任何断言变化——这一点 v1 写反了，v2 更正。
- `hooks/archive` 改的是两处：任务目录的移动（`TaskFlowDocs/<task>/` → `TaskFlowDocs/achieved/<task>/`）和 `todo.md` 的条目重写。后者落在 `TaskFlowDocs/todo.md` 这个 smoke 输入上。

## Requirements

- R1：在 `CONTRIBUTING.md` 的 PR 顺序里写清一条判据：合并前最后一次 push 的 diff **全部**落在 `TaskFlowDocs/<task>/` 与 `TaskFlowDocs/achieved/<task>/` 之内时，可以按其提交信息与内容直接合并，不再等那一轮 CI。
- R2：判据的范围是 `TaskFlowDocs/` 之下：任务目录、`achieved/`、以及 `todo.md` 都算。判据之外（`hooks/`、`skills/`、`.github/`、manifest、README、`CONTRIBUTING.md` 自身）任一出现即回到「等 CI」。
- R3：进入免等路径的前提写死在文档里：**代码提交那一轮的 CI 已经绿**，且 PR body 已记录该 run。没有这个前提就没有免等。
- R4：不改变现有的 draft → ready 顺序，也不改变 `task complete` 在 push 之前运行的规定。
- R5：本次只改治理文档（`CONTRIBUTING.md`）；不新增 hook、不改 CI 工作流，因为判据本身是给合并者读的，机器无法在合并那一刻读到「作者声明这是仅文档提交」。

## Acceptance Criteria

- AC1：`CONTRIBUTING.md` 的 PR 章节包含该判据、它的路径范围（`TaskFlowDocs/` 之下，含 `todo.md`）和它的前提（代码提交 CI 已绿并有 run 链接）。
- AC2：判据以可执行的路径形式写出（`TaskFlowDocs/<task>/`、`TaskFlowDocs/achieved/<task>/`），而不是「只要不碰代码」这类模糊表述。
- AC3：文档给出不适合该判据的情形，让边界可判：任何 `hooks/`、`skills/`、`CONTRIBUTING.md` 自身的改动，以及「代码提交那轮 CI 未绿」。
- AC4：`bash hooks/repository-check .` 与 `git diff --check` 通过；`hooks/smoke-test` 不受影响（只改 `CONTRIBUTING.md`，它被算在 smoke 集合里但断言不读取其正文——以 CI 结果为准）。

## External Facts

- Depends on external facts: no
- Why not: 判据的输入全部是本仓库内的文件路径与既有 CI 配置（`.github/workflows/hooks.yml`、`tools/workflow-affected`），没有需要外部规格或版本才能确认的结论。

## In Scope

- `CONTRIBUTING.md`：PR 章节新增「何时不必等最后一次 CI」一段。

## Out of Scope

- 让 CI 跳过仅文档提交（workflow 改动）。当前 `changes` job 已经按路径分类，但它仍会起一轮；减少的是**等待**，不是**运行**。
- 让 CI 跳过仅文档提交（workflow 改动）——本次只减少等待。
- CI 结果回写 Plan 的流程本身（`CONTRIBUTING.md` 已规定，本次不改）。

## Risks / Deferred Items

- **承担的风险**：`TaskFlowDocs/` 内的提交未经 CI 就进 main。缓解是 R3 的前提（代码那轮已绿），以及该路径集已由 `tools/workflow-affected` 判为「任何 job 都不需要」。残余风险是 `todo.md` 被改坏到某个解析式 hook 读不了——`archive` 只做条目重写，且它的结果由 `hooks/smoke-test` 在**下一次** CI 里读到。
- **靠人工判定的判据**：没有机器检查能确认「diff 只在任务目录内」。升级路径是给 PR 加一个标签或让 `todo-check` 类脚本在合并前跑一次；若这条路径被滥用，就上机器检查（记为 deferred）。
- 与并行任务（`2026-11-04-skip-guard`）无关，互不改同一文件。

## Open Questions

无阻塞项。
