# Plan — Land a task's documents with its pull request, and record its landing claim there
> Task version: v4
> Status: ready

No spec required — small, self-contained task.

## Reference Pointers

- `CONTRIBUTING.md` — § Where the commit lands（`:35-56`，v3 写的两根轴，以及本次要接着说清的第四条）。
- `hooks/smoke-test` — `:1391`、`:1304`（钉措辞的先例）、`:1395-1416`（v3 新增的 landing 钉段，本次加钉的邻位）。
- `skills/taskflow/SKILL.md` — `:121`（只做指向；本次预计不动）。
- `RELEASE.md` — `:161-166`（v3 改正过的判据引用；本次预计不动）。
- `TaskFlowDocs/achieved/2026-10-01-taskflow-commit-path/plan.md` — 那句不合当前规则的遗留原话。本次**不修**，理由见 PRD 的 Out of Scope。

## Related Tasks

- 本任务是 `TF-20261001-331f7c` 的 v4；v1/v2/v3 的完整文档见 `old/v1/`、`old/v2/`、`old/v3/`。
- `TF-20261001-da6047` — `hooks/reopen` 的 Todo 路径缺陷，已修复（`e603f2c`）。本任务取回与回滚都依赖它。
- `TF-20260919-6b4e21` — `todo.md` 无界增长，另一根轴，不并入。

## Skills / Tools Used

- [PRD] Unaided — 已按 pre-write gate 记录（`task unaided PRD --considered 'requirements elicitation and framing'`）。需求由用户在 v3 合并后当场给出（「别下次了，现在吧」）；PRD 的增量是把 v3 已经写下的两句推出它们的第四条并界定范围，其中关键事实（PR #66 的 Plan 承诺了回填）在仓库内可查，没有留给能力去发现的部分。considered: requirements elicitation and framing。
- [Plan] Unaided — 未调用能力：改动是一段规则文字加一条钉子，分解为「先写正文、再钉冻结后的措辞、最后按新规则自己落地」，步骤间的依赖由 v3 已立的同一模式决定。为这个规模调用分解能力会是表演而不是使用。considered: work breakdown and task decomposition。

## Preconditions

- Worktree `.worktrees/taskflow-commit-path`，分支 `docs/taskflow-commit-path-v4`，基于 `main` 的 `b370b62`。前三轮的提交（`cadee53`、`7d7a60d`、`b370b62`）已在 `main` 上，不重开。
- **本任务按 v3 写的落地规则走**：PR + draft→ready；文档提交与 archive 留在 PR 内，不合并后直推。
- **本 Plan 不得承诺任何合并后回写**（A6）。落地主张写进 PR 正文；核对用 `git merge-base --is-ancestor`，结果只说给用户，不落任务文档。
- 本机无法跑完整的 `bash hooks/smoke-test`：无解释器一节在 `:53-117` 中止，早于本次触碰的段落。本地只跑 `git diff --check`、`bash hooks/release-check .`、Skill 的 `quick_validate`；smoke 交 CI 三主机。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-01 22:31 +0800
- Approved version: v4
- Approved scope: PRD / Plan

## Steps

### Step 1 — State where a task's landing claim is recorded

- Goal: 在 § Where the commit lands 写明落地主张属于 PR、任务文档在合并之后不再回写，并把「核对」与「回写」分开。
- Dependencies: none.
- Files: `CONTRIBUTING.md`.
- Implementation checklist:
  - [ ] 在 v3 那两段之后接着说第四条：任务的落地主张记录在**它的 PR 里**——正文与提交（R1）。
  - [ ] 写明任务在合并之后**不再回写任务文档**，并给出理由：那是一次合并后的任务文档写入，规则已禁止（R2）。
  - [ ] 写明只有合并后才知道的事实按**核对**处理，不写成分解成回写的承诺；点明核对本身不需要文档（R3）。
  - [ ] 不与 v3 的措辞冲突：两根轴、draft→ready、隔离规则、发布例外都不动（R4）。
  - [ ] 逐处核对 `SKILL.md:121` 与 `RELEASE.md`，只在因此不准时才改（R5）。
- Acceptance: A1, A2, A4.
- Verification: 只读该节，回答两问——「本任务的落地记在哪」「合并后才知道的核对结果呢」。两个都答得出才算过（A2）；需要翻别的文档就是没写成。
- Rollback: `git restore --source=HEAD -- CONTRIBUTING.md skills/taskflow/SKILL.md RELEASE.md`（本步提交前）。
- Status: pending

### Step 2 — Pin the frozen wording

- Goal: 用字面串钉住新句子，并以 CI 三主机的判决作为本步验收。
- Dependencies: Step 1 —— 钉子引的是它的**最终**措辞。
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [ ] 措辞到此冻结：钉的字符串从改完的文本里复制，只取足够独特的最短片段（先例 `:1391` 取的是段首短句，不取整段），沿用 `grep -q -F --`。
  - [ ] 加钉位置接在 v3 的 landing 钉段（`:1395-1416`）之后，同属「陈述点」那一族。
  - [ ] push 分支、以 draft 开 PR、读 CI 三主机结果。
- Acceptance: A3；A5 的 CI 部分。
- Verification: CI 的 `smoke (ubuntu-latest)` / `smoke (macos-latest)` / `smoke (windows-latest)` 三项绿。本机跑不了整套，记录为未执行，不写成「已验证」。
- Rollback: 分支上的普通提交，`git restore` 后重新 push；措辞不改则回滚只涉及 `hooks/smoke-test`。
- Status: pending

### Step 3 — Land by the rule, and record the claim in the PR

- Goal: 文档提交与 archive 留在本 PR 之内，且本 Plan 不出现任何合并后回写的承诺——那正是本次要修的东西，本任务是它第一个应当遵守者。
- Dependencies: Step 2.
- Files: `TaskFlowDocs/2026-10-01-taskflow-commit-path/`, `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [ ] 把 CI run 与 PR 模板字段映射写进本 Plan，提交并推送（仍在同一 PR）。
  - [ ] PR 正文的 Task 字段一次写成覆盖两种状态的形态（评审期间在活动根，末次提交归档到 `achieved/`）——避免 archive 之后再改 body。
  - [ ] `hooks/task complete --user-accepted`（需用户验收），再 archive；提交并推送（仍在同一 PR）。
  - [ ] `gh pr ready` 转正，交用户合并。
  - [ ] 落地主张写进 PR 正文，**不写回本 Plan**（A6）。
- Acceptance: A6；A5.
- Verification: 合入后用**核对**确认 archive 提交在合并之内——`git merge-base --is-ancestor <archive-sha> <merge-sha>`。这是核对不是回写，不产生新的文档提交。
- Rollback: PR 被拒则 `hooks/reopen 2026-10-01-taskflow-commit-path` 取回（`TF-20261001-da6047` 已修复此路径）。
- Status: pending

## Checkpoints

- After Step 1：只读该节答出两问，再动测试。
- After Step 2：CI 三主机绿。这一步是措辞的最后一次改动——之后只允许追加文档提交。
- After Step 3：PR 内含 archive 且已合入。

## Verification / Review

- A1、A2、A4 是散文主张，靠阅读判定——与 `2026-09-30-release-ci-test-policy` 及本任务 v2/v3 记录的同一限制一致。
- A3 由 CI 裁定：钉子本身是 smoke 套件的一部分。
- A5 本机执行三项：`git diff --check`、`bash hooks/release-check .`、Skill 的 `quick_validate`（本机须 `PYTHONUTF8=1`，否则 GBK 解码报错）。
- A6 的落地部分在合入后**核对**（`git merge-base --is-ancestor`），结果只说给用户，不写回本 Plan——见 Preconditions。本 Plan 自身不含任何回写承诺，这可由阅读直接确认。
- 未执行：`bash hooks/smoke-test` 整套，原因见 Preconditions。

## Change Log
- 2026-10-01 reopen — retrieved achieved task `2026-10-01-taskflow-commit-path` for new work; re-approval required before core changes
- 2026-10-01 — **v4**。v3 合并后首次实战暴露一条缺口：任务文档里没有位置安放「只有合并后才知道」的事实，而 v3 自身的措辞已经蕴含这一点（验证记录随 PR 落地 ＋ 禁止合并后推任务文档）。工作区里还有一处铁证——PR #66 的 Plan 恰好写了「合入后按 A8 核对并回填本处」。本次补上第四条：落地主张写在 PR 里，任务文档在合并之后不再回写；并把「核对」与「回写」分开。

## Follow-ups

- 这条推论目前只由散文承载：没有机制阻止下一次又在 Plan 里写下回写承诺。若要在 `hooks/task approve` / `complete` 上加检查（例如拒绝含回写承诺的 Plan），那是另一个改动，本次不做。
- v3 的 Follow-ups 仍然有效：`RELEASE.md` 与 `CONTRIBUTING.md` 对同一判据的两处陈述，应在下一次发布时再互校一次——那是两者第一次被同时使用。

## Version History

- v1 — the rule stated and landed as `cadee53`; superseded because its text did not carry its own scope.
- v2 — the rule text tightened to state the scope it always had; landed as `7d7a60d`.
- v3 — 拆开两根轴：任务自己的文档随任务的 PR 落地，推送权限只路由不隶属任何任务的 bookkeeping；并新增 draft→ready。经 PR #66 合入 `b370b62`。
- v4 — 补上 v3 蕴含却未写出的第四条：落地主张写在 PR 里，任务文档在合并之后不再回写。
