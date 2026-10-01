# Archived Version v2 — Plan — Commit Todo, release, and TaskFlowDocs changes straight to main when the author
> Task: 2026-10-01-taskflow-commit-path
> Version: v2
> Status: superseded
> Archived: 2026-10-01 14:42 +0800
> Superseded by: v3
> Archive mode: file

## Change Summary

v2 把 landing 规则的字面收紧到它一直以来的意图：先声明路由范围（bookkeeping 三类），再讲权限判据，并明写「其余一律走 PR、拿不准就走 PR」。v3 拆的正是那三类里的第二类。

权限判据在 v2 覆盖 Todo 条目、**任务状态与归档**、发布执行三类。v3 把「任务状态与归档」移出：任务自己的文档——PRD、Spec、Plan、Plan 的验证记录、archive 提交——随该任务的 PR 落地，不再是权限判据能决定去留的东西。权限判据保留的范围改为不隶属任何任务的 bookkeeping：纯 Todo 改动、reopen、发布执行、没有对应任务的文档维护。两根轴互相独立，任一都不能推出另一个。

新增 draft→ready：PR 以 draft 打开，任务文档提交推齐后才 `gh pr ready` 转正，使「还不能合」由 PR 自身可辨识，而不是靠正文的一句叮嘱。

起因是实测缺陷：2026-10-01 连续两个任务把文档落在了 PR 之外（`docs/artifact-language` 的 Plan 记录被 cherry-pick 成 `64ac50d`，两个任务的 archive 都是合并后直推——`35a4071`、`e603f2c`），两次形态还不一样。v3 把成因定为一根轴被当成了两根。

v2 未改动、v3 也未改动的部分：权限判据本身、隔离规则（worktree）、发布例外。

## Archived Materials
- prd.md
- plan.md

## Restore
Read the archived v2 core docs from a new temporary restore root. Do not overwrite the current task root.
