# 归档时把任务目录里的本地专用文件带进 base 检出

> Task version: v1
> Status: completed

## Goal

`hooks/archive` 把任务目录从活动区搬到 `achieved/` 时，把目录里的**本地专用文件**（`sessions.md`，以及该任务路径下的 `personal.md` 若存在）一并复制到 **base 检出**的对应路径下，且它们保持不进入版本控制。今天它们要么随 worktree 一起消失，要么在 base 检出里留下一个 git 看不见的幽灵目录。

## Background / Confirmed Facts

`sessions.md` 与 `personal.md` 由 `hooks/install-git-hygiene` 写进本 clone 的 `.git/info/exclude`（`hooks/install-git-hygiene:78-79`），意图是「本地专用、永不提交」。`hooks/archive` 对这两个名字**零命中**——它对整个目录做一次 `mv`，然后再不做任何文件级处理。

三条实测（2026-11-03，探针仓库各建一次）：

**路径 A：worktree 里归档，记录随 worktree 一起消失。**

1. 在 worktree 的任务目录写 `sessions.md`；
2. `git status --porcelain` 全空——git 看不见被 exclude 的文件；
3. `hooks/archive` 做 `mv`，文件跟着进了 `achieved/`；
4. `git add -A` 不包含它；
5. 按 `CONTRIBUTING.md` 与 `archive` 自己打印的步骤执行 `git worktree remove`，**无任何警告地成功**（git 只拒绝「有未跟踪文件」的树，被 ignore 的文件不算）；
6. 全仓库再找 `sessions.md`：没了。

**路径 B：base 检出里留下幽灵目录。**

若记录写于 base 检出（会话 cwd 指向那里），分支上归档并合并回 base 之后，base 里只剩 `TaskFlowDocs/<task>/sessions.md` 一个文件，git 既不移走也不删除，因为它 untracked + ignored。本仓库现在就有一个：

```
TaskFlowDocs/2026-10-29-schema-check/sessions.md
```

该目录没有 `plan.md`，`git ls-files` 为空；归档提交 `73f5e82` 是 2026-10-31 00:23，文件时间戳 2026-10-30 22:48——先写的记录，后归档的目录。`achieved/2026-10-29-schema-check/` 里没有这份记录。

**为什么两套机制各自都对、放一起就丢**：隔离机制的目的就是让这些文件对 git 隐形；而搬家是纯文件系统操作，隐形意味着没有任何一步会报告它们没被带上。`hooks/repository-check` 的 worktree 清洁度判定读的也是 `git status --porcelain`，同样看不见它们，所以它也不会报。

## Requirements

### R1 — 归档把本地专用文件复制到 base 检出

`hooks/archive` 在 `mv` 成功之后，把源目录中（`mv` 之前）存在的本地专用文件逐个复制到 base 检出的 `TaskFlowDocs/achieved/<task>/` 下。

### R2 — 认哪些文件是本地专用的

名单与 `hooks/install-git-hygiene:78-79` 的两条 exclude 规则一致，但落在任务目录里的只有一条：

- `TaskFlowDocs/<task>/sessions.md` — 本次搬它；
- `TaskFlowDocs/repository-docs/personal.md` — 不在任务目录内，归档碰不到它，本次不涉及。

名单写成一个显式变量，便于将来扩展。不按「凡被 exclude 命中者」自动发现：那需要调用 `git check-ignore`，而它按 clone 的 exclude 文件作答，换个 clone 答案就不同。

### R3 — 不进入版本控制，且失败不致命

- 复制不是 `git add`，文件在 base 检出里同样被 exclude，`git status` 仍然看不见。
- 复制失败不得让归档失败：归档的事务性是目录移动 + Todo 重写，本地副本不是归档的一部分。失败时打印一行说明，退出码不变。

### R4 — 同时处理已存在的幽灵目录

提供一个可重复执行的清理动作（不自动执行），并清掉本仓库现存的 `TaskFlowDocs/2026-10-29-schema-check/`：先把 `sessions.md` 复制到 `achieved/2026-10-29-schema-check/`，再删除该空目录。

## Acceptance Criteria

- **A1**：在 worktree 的任务目录放 `sessions.md`，跑 `hooks/archive`，base 检出的 `achieved/<task>/` 下出现同内容文件，且 `git status --porcelain` 仍不显示它。
- **A2**：没有 `sessions.md` 的任务归档后行为与今天逐字节相同（不新增输出行）。
- **A3**：覆盖写入失败（base 不可写）时归档仍成功，`archive OK` 照常打印。
- **A4**：`hooks/smoke-test` 新增断言覆盖 A1–A3，全绿。
- **A5**：现存幽灵目录清理完毕：`TaskFlowDocs/2026-10-29-schema-check/` 不存在，其 `sessions.md` 位于 `achieved/2026-10-29-schema-check/`。

## External Facts

- Depends on external facts: no
- Why not: 全部结论来自 `hooks/archive`、`hooks/install-git-hygiene`、`CONTRIBUTING.md` 与本仓库现存目录，2026-11-03 逐一读过并在探针仓库复现。

## In Scope

- `hooks/archive`：复制步骤与输出。
- `hooks/smoke-test`：新断言。
- 现存幽灵目录的清理。
- 本任务的两份核心文档。

## Out of Scope

- 修改 exclude 规则本身，或让这些文件进入版本控制。
- 追溯修复其它 clone 上可能已经丢失的记录。
- `hooks/repository-check` 的清洁度判定（它语义上问的是「能否安全删除」，被 ignore 的文件确实不影响删除安全）。

## Risks / Deferred Items

- **R1 风险**：`archive` 在 worktree 里运行时，base 检出路径需要从 git 推出（`--absolute-git-dir` 的 `commondir`），而脚本目前只在结尾为了打印 teardown 才取它。若取不到（非 git 目录），跳过复制并说明。
- **Deferred**：把「本地专用文件」从一个显式名单升级为「凡被 exclude 规则命中者」，需先定义如何在不调用 `git check-ignore` 的前提下判定——属独立设计。
