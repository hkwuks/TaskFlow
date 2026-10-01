# Land a task's documents with its pull request, and route only standalone bookkeeping by push permission
> Task version: v3
> Status: ready

## Goal

开发任务自己的文档——PRD、Spec、Plan、Plan 里的验证记录、以及它的 archive——属于该任务的交付物，因此随该任务一起落地：在自己的分支上，进它自己的 PR。推送权限只决定**不隶属任何任务的 bookkeeping** 落在哪（纯 Todo 改动、reopen、发布、没有对应任务的文档维护）；它不授权把一个任务的文档从该任务自己的 PR 里拆出去。这是两个独立的问题，规则要同时写出两条。

## What v3 changes

v1 与 v2 定下的是**一根轴**：哪些提交直推目标分支、哪些走 PR，判据是作者能否推送。那套路由列了三类：Todo 条目、任务状态与归档、发布执行。v3 拆的正是其中第二类。

本仓库 2026-10-01 实测到的代价：连续两个任务，代码经 PR 落地，文档落在 PR 之外，而且两次形态还不一样。`docs/artifact-language` 合并为 `e4ce70f`，它的 Plan 记录（`b64dc26`）还留在分支上，只能 cherry-pick 成 `64ac50d`，archive 随后直推（`35a4071`）。`fix/reopen-todo-path` 合并为 `10caff1`，Plan 记录在里面（`b64f155`），但 archive 仍在合并后直推（`e603f2c`）。两种形态都不是刻意选的——差异来自「作者能否推送」回答的并不是「这个任务的记录该放哪」。

v3 把两根轴分开：权限判据保留自己的范围（不隶属任务的 bookkeeping），任务文档不再属于该范围。

## Background / Confirmed Facts

- `CONTRIBUTING.md:39-45` 把 bookkeeping 直推，并列出三类：Todo 条目、「A task's status and archive」、发布执行。`:45` 写的是「None of those has anything to review, so each goes straight to the target branch when the author can push it」。
- `CONTRIBUTING.md:12` 要求任务在实现前有 PRD、Spec、Plan，且只有**验收之后**才归档——所以任务文档全程都在它自己的分支上，archive 是其中最后一件。
- `skills/taskflow/SKILL.md:121` 把同一组三类复述成摘要并指向 `CONTRIBUTING.md`。类目一变，这句就错。
- `RELEASE.md:152` 说明发布为何直推：PR 带不了 tag，而 tag 与它的 pin 必须同时可见；同段还把发布称作「one of the three classes it covers」。发布没有可搭乘的 PR，故 v3 不改它的行为，只可能改这句引用。
- `hooks/smoke-test:1391` 用字面串钉住 `CONTRIBUTING.md` 的一句，`:1304` 钉住 `SKILL.md` 的一句。两份文件都有钉措辞的先例。
- 实测（2026-10-01）：`git merge-base --is-ancestor b64dc26 e4ce70f` 失败；`b64f155` 在 `10caff1` 之内；`e603f2c`、`35a4071` 都是合并后直推。
- 所有者指示（2026-10-01）：「所有的pr，应当在最后把文档操作都放同一个pr提交，不要新开pr单独提交文档操作」——能同时提交的保持同时提交，不能的可以单独开 PR；这与作者能否推送不冲突，因为开发任务与文档维护是两件事。

## Requirements

- R1. 写明任务自己的文档随该任务的 PR 落地：它实现时所用的 PRD、Spec、Plan、Plan 的验证记录、以及 archive 提交。它们不直推目标分支，也不单独开 PR。
- R2. 推送权限只管**不隶属任何任务**的 bookkeeping：纯 Todo 改动、reopen、发布执行、以及没有对应任务的文档维护。它不再决定任务自身文档的落点。
- R3. 明说两个问题是分开的，读者无法从一个推出另一个。权限判据对它仍然覆盖的部分不变，只是不再覆盖任务的 archive。
- R4. PR 在任务文档齐备之前不算可合，而且是 PR 自己说出来的、不需要读者去问：以 draft 打开，文档提交推上去之后才转 ready。
- R5. 发布例外不变。发布不取分支、不开 PR，没有可搭乘的东西，仍是直推；规则不得读成禁止它。
- R6. 修正**每一处**路由陈述，不只规则本体，使 `CONTRIBUTING.md` 与 `skills/taskflow/SKILL.md` 描述的是一条规则而不是两条。
- R7. 隔离规则不动：worktree 仍然隔离任务的工作，本条只决定这份工作的提交落在哪。

## Acceptance Criteria

- A1. `CONTRIBUTING.md` § Where the commit lands 同时写出两根轴，并列出权限判据现在覆盖的类目，其中已不含任务状态与归档。
- A2. 只读该节，贡献者能同时答出「我任务的 Plan 记录与 archive 去哪」（进它自己的 PR）与「纯 Todo 改动去哪」（能推就直推），无需任何别的文档。
- A3. `skills/taskflow/SKILL.md` 不再把类目复述为 Todo / 状态与归档 / 发布，而是指向 `CONTRIBUTING.md`（v2 的 A4 仍有效，正是它现在的文本失效了）。
- A4. `RELEASE.md` 的直推行为不变；它把发布称作「三类之一」的那句随新的类目改正，改正的是措辞而非范围。
- A5. draft→ready 的机制写在 `CONTRIBUTING.md` 的 Pull requests 一节并给出命令，使其可判定而非口号。
- A6. `hooks/smoke-test` 按 `:1391` 与 `:1304` 的先例，用字面串钉住两处的新句子。
- A7. `git diff --check` 干净；`bash hooks/release-check .` 报 `pass`；Skill 的 `quick_validate` 通过。
- A8. 本任务按它自己写的规则落地：Plan 记录与 archive 是 `docs/taskflow-commit-path` 上的提交，在本任务的 PR 之内，archive 不是合并后直推。

## In Scope

- `CONTRIBUTING.md` — § Where the commit lands；§ Pull requests（draft→ready 那句）。
- `skills/taskflow/SKILL.md` — `:121` 的路由摘要。
- `hooks/smoke-test` — 两处新句子的字面串钉。

## Out of Scope

- 任何 hook 行为。`hooks/archive`、`hooks/reopen`、`hooks/task` 都不改：本条讲提交落在哪，不讲 hook 写什么。
- `RELEASE.md` 的动作；只在措辞与新的范围不一致时才改措辞。
- 分支保护、仓库角色、CI 配置。
- 对本仓库以外仓库的任何主张。

## Risks / Deferred Items

- **任务的 archive 将先于它的代码出现在目标分支上。** archive 断言任务已完成，而目标分支此时还没有这项改动。若 PR 被拒，归档下来的任务描述的是一份从未落地的工作。恢复手段是 `hooks/reopen`（`e603f2c` 落地，现已是 archive 的逆操作），但这条配对没有被「PR 被拒」这一情形检验过——记录在案，不当它已被解决。
- **draft 边界靠人守，不是机制。** 提前合并不会让任何 CI 失败；把 `b64dc26` 落在分支外的那次提前合并，同样能落在它的后继者身上。缓解是 draft 状态本身在 GitHub 上可见，但本仓库没有分支保护来强制它。
- **类目缩到几乎为空。** 任务状态与归档移出后，权限判据只剩纯 Todo 改动、reopen、文档维护。它仍然真实，但已接近「一切没有自己任务的改动」，日后可能发现两根轴又并回一根。

## Open Questions

- **已裁定（2026-10-01，批准轮）：archive 进 PR，与 Plan 记录一起。** 争点是 `CONTRIBUTING.md:12` 的「只在验收之后归档」——若「验收」指结果已在目标分支上，archive 就属于「不能同时提交」那一类，该走它自己的路径。裁定取「两件都进」：archive 是同一个任务的最后一件文档，把它拆出来正是 `e603f2c` 的成因；「验收」按任务自身的审批与验证理解，不按代码是否已在目标分支上。代价与恢复手段见 Risks 第一条——若 PR 被拒，用 `hooks/reopen` 取回，这次是该配对首次实战。
