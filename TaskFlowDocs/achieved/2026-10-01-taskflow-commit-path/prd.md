# Land a task's documents with its pull request, and record its landing claim there
> Task version: v4
> Status: completed

## Goal

v3 的目标不变——任务自己的文档随该任务的 PR 落地，推送权限只路由不隶属任何任务的 bookkeeping。v4 补上它带来的一条推论：**任务的落地主张写在它的 PR 里，任务文档在合并之后不再回写**。于是「只有合并后才知道的事实」没有、也不需要「回填」这一步——它作为一次核对表述，或干脆留在 PR 正文里。

## What v4 changes

v3 把任务文档——含「写进 Plan 的验证记录」——收进任务自己的 PR，并禁止把它们推上目标分支。这两句合起来就推出第四条，而 v3 没有把它写出来：**一个只存在于合并之后的事实，在任务文档里没有位置**。写它，就是把任务文档在合并后推上目标分支，正是规则禁止的动作。

v3 合并后的**首次实战立刻撞上**。PR #66 的 Plan 里我写了「合入后按 A8 核对并回填本处」，而 A8（archive 是否落在合并之内）只能在合并后判定。旧流程确实有这一格——v1/v2 的 Plan 记着「落地 — `git push origin HEAD:main`，`1c23f0d..7d7a60d`，CI run `36813488643` success」，因为直推能预先写下自己的记录。归档进 PR 之后，这一格消失了。

v4 把这条推论写进规则，并把「核对」与「回写」分开：核对不需要文档，合并拓扑本身就是证据。

## Background / Confirmed Facts

- `CONTRIBUTING.md:39`（v3 所写）把「the verification record written into the Plan」列为随 PR 落地的一项，同一段又禁止把任务文档推上目标分支。两句合起来即是这条推论；v4 是把它说出来，不是加新约束。
- `CONTRIBUTING.md:43` 的类目表列出权限判据覆盖的 bookkeeping：纯 Todo 改动、reopen、发布执行、无对应任务的文档维护。**已归档任务的事后回写不属于其中任何一项**，所以它没有合法路径，而不是路径不明。
- 实例（2026-10-01）：`TaskFlowDocs/achieved/2026-10-01-taskflow-commit-path/plan.md` 里那句「合入后按 A8 核对并回填本处」。该文件是合并 `b370b62` 的产物，按规则不得再写。用户裁定取消这个期待。
- 同日的对比事实：`git merge-base --is-ancestor 1f23f82 b370b62` 成立——archive 提交在合并之内，A8 已按拓扑核对通过，全程没有写任何文档。核对与回写确实是两件事。
- 用户指示（2026-10-01）：「别下次了，现在吧」——把这条写进规则，不推迟到下一次相关改动。

## Requirements

- R1. 写明任务的落地主张记录在**它的 PR 里**（正文与提交），不记录在任务文档里。
- R2. 写明任务**在合并之后不再回写任务文档**，并给出理由：那是一次合并后的任务文档写入，规则已禁止。
- R3. 说明「只有合并后才知道的事实」怎么处理：作为**核对**表述（如「合入后按合并拓扑核对」），不合成分解成回写的承诺。核对本身不需要文档。
- R4. 不改 v3 的两根轴、draft→ready、隔离规则与发布例外。v4 只补这条推论，且不得与 v3 的措辞冲突。
- R5. 逐处核对 `skills/taskflow/SKILL.md:121` 与 `RELEASE.md`，只在它们因此变得不准时才改；本次预计两处都不需要动（它们讲的是提交落在哪，不是合并后写什么）。

## Acceptance Criteria

- A1. `CONTRIBUTING.md` § Where the commit lands 明写「落地主张在 PR 里」「任务文档合并后不再回写」，理由与 R2 一致。
- A2. 只读该节即可答出两问——「本任务的落地记在哪」（PR 正文与提交，不是 Plan）与「合并后才知道的核对结果呢」（不需要写，合并拓扑即证据）。需要翻别的文档即未写成。
- A3. `hooks/smoke-test` 按 `:1391`、`:1304` 与 v3 新增段的先例，用字面串钉住新句子。
- A4. 三份文档合读仍只有一条规则；不得出现与 v3 相冲突的措辞。
- A5. `git diff --check` 干净；`bash hooks/release-check .` 报 `pass`；Skill 的 `quick_validate` 通过。
- A6. 本任务按它写的规则落地：文档提交与 archive 在本任务的 PR 之内；**且本 Plan 自身不得出现任何「合并后回写」的承诺**——那正是本次要修的东西。

## In Scope

- `CONTRIBUTING.md` — § Where the commit lands。
- `hooks/smoke-test` — 新句子的字面串钉。
- `skills/taskflow/SKILL.md`、`RELEASE.md` — 仅在措辞因此不准时改动。

## Out of Scope

- v3 的两根轴、draft→ready、隔离规则、发布例外，以及任何 hook 行为。
- **不修正已归档的那句遗留。** `achieved/2026-10-01-taskflow-commit-path/plan.md` 里的「合入后回填本处」按本规则不得更正——更正它本身就是被禁止的合并后写入。它作为已知遗留留在原处。
- 分支保护与仓库角色。

## Risks / Deferred Items

- **归档文档里的遗留无法更正。** 上述那句会永久留着，与当前规则不符。这是规则的直接后果而非疏漏；接受，不绕。
- **这条推论仍只是散文，靠阅读遵守。** 没有任何机制阻止一个 Agent 下次又在 Plan 里写下回写承诺——钉子只能钉住规则文本，钉不住 Plan 的措辞。真要强制，得在 `hooks/task approve` / `complete` 上检查 Plan 里是否出现此类句子，那是另一个改动，本次不做。
- **v4 自身也可能再生同类缺口。** 它的 A6 只能检查「本 Plan 没写回写承诺」，检查不了「规则已把该说的说全」。若合并后才发现还缺一句，那就是 v5——本次不预先为它设计。

## Open Questions

无。v3 的 Open Question 已裁定；本次的起因、结论与处理方式都由用户直接给出。
