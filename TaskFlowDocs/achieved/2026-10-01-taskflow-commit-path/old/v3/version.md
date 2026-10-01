# Archived Version v3 — Plan — Land a task's documents with its pull request, and route only standalone bookkeeping by push permission
> Task: 2026-10-01-taskflow-commit-path
> Version: v3
> Status: superseded
> Archived: 2026-10-01 22:17 +0800
> Superseded by: v4
> Archive mode: file

## Change Summary

v3 把 landing 规则拆成两根独立的轴：任务自己的文档——PRD、Spec、Plan、Plan 里的验证记录、archive——随该任务的 PR 落地，与作者能否推送无关；推送权限只路由不隶属任何任务的 bookkeeping（纯 Todo 改动、reopen、发布执行、无对应任务的文档维护）。并新增 draft→ready，使「还不能合」由 PR 自身可辨识。

v4 补上 v3 蕴含却未写出的第四条：**任务的落地主张记录在它的 PR 里，任务文档在合并之后不再回写。** v3 既然把「写进 Plan 的验证记录」收进 PR、又禁止把任务文档推上目标分支，那么一个只存在于合并之后的事实就没有位置可写——写它就是那条被禁止的合并后推送。v3 把这件事留在了暗处。

触发它的是 v3 合并后的首次实战：PR #66 的 Plan 里写了「合入后按 A8 核对并回填本处」，而 A8 只在合并后判定。旧流程有这一格——v1/v2 的 Plan 记着「落地 — `git push origin HEAD:main`，`1c23f0d..7d7a60d`」——直推能预先写下自己的记录，进 PR 之后不能。v4 把「核对」与「回写」分开：核对不需要文档，合并拓扑即证据。

一条同日的核对事实：`git merge-base --is-ancestor 1f23f82 b370b62` 成立，archive 提交在合并之内，该核对全程没有写任何文档。

v3 未改动、v4 也未改动的部分：两根轴本身、draft→ready、隔离规则（worktree）、发布例外，以及任何 hook 行为。已归档 Plan 里那句不合规则的遗留按新规则**不得**更正——更正它本身即是被禁止的合并后写入。

## Archived Materials
- prd.md
- plan.md

## Restore
Read the archived v3 core docs from a new temporary restore root. Do not overwrite the current task root.
