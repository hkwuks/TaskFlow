# Plan — Land a task's documents with its pull request, and route only standalone bookkeeping by push permission
> Task version: v3
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `CONTRIBUTING.md` — § Working branches（`:16-33` 隔离规则）、§ Where the commit lands（`:35-58`，规则本体，尤其 `:39-47` 的类目与判据）、§ Pull requests（`:97-99`，draft 那句的落点）。
- `skills/taskflow/SKILL.md` — `:121`（把路由复述成 `Todo 条目 / 任务状态与归档 / 发布` 的摘要，本次失效的正是它）。
- `RELEASE.md` — `:152`（发布直推的理由，含「one of the three classes it covers」这句引用）。
- `hooks/smoke-test` — `:1391`（钉 `CONTRIBUTING.md` 段首短句的先例）、`:1304`（钉 `SKILL.md` 的先例）、`:1240-1400` 一带（本次加钉的位置）。
- `TaskFlowDocs/repository-docs/index.md` — 路由记录；`CONTRIBUTING.md` 是分支与提交规则的权威来源。

## Related Tasks

- `TF-20260919-6b4e21` — `todo.md` 无界增长。本次会让每个任务多带两个文档提交，但不改变 `todo.md` 的条目数，故不并入。
- `TF-20261001-da6047` — `hooks/reopen` 的 Todo 路径缺陷，已修复（`e603f2c`）。本次的 Rollback 依赖它：若 PR 被拒，用它把归档的任务取回。
- `TF-20260928-3910fb` — 发布流程精简，另一根轴（发布时跑什么，不是提交落在哪）。

## Skills / Tools Used

- [PRD] Unaided — 未调用能力，已按 pre-write gate 记录（`task unaided PRD --considered 'requirements elicitation and framing'`）。需求由所有者直接给出，PRD 的增量是把它与 v1/v2 的权限判据对齐成两根轴；假设已在澄清轮用三个问题当面挖过（轴的分界、PR 何时可合、钉不钉），没有留给能力去发现的部分。considered: requirements elicitation and framing。
- [Plan] `agent-skills:planning-and-task-breakdown` — 调用，用途是分解与排序。采纳的结论：(1) 钉子必须依赖「措辞已冻结」这一步，故钉的位置排在其所引文本之后，而不是与之并行；(2) 三步的验收标准各自可观察，且每一步都留了独立的 `git restore` 回滚点；(3) 高风险项（钉子的脆性、draft 边界的可守性）排在 Step 3 的 push 上尽早由 CI 裁定，不等落地。

## Preconditions

- Worktree `.worktrees/taskflow-commit-path`，分支 `docs/taskflow-commit-path`，基于 `main` 的 `e603f2c`。前两轮的提交（`cadee53`、`7d7a60d`）已在 `main` 上，不重开；v1/v2 的完整文档见 `old/v1/`、`old/v2/`。
- **本任务按它自己写的规则落地。** 这是本次与 v1/v2 最大的差别：v1/v2 是直推，本次走 PR。因此 Step 3 之后不再有直接推到 `main` 的动作；若届时发现 PR 路径不可用（权限或托管故障），回退到直推，并在 Plan 里记下这次反转——这正是 PRD 记下的「两根轴」第一次同时被检验。
- 本机无法跑完整的 `bash hooks/smoke-test`：无解释器一节在 `:53-117` 就中止，早于 Step 3 触碰的 `:1240-1400`。本地只跑 `git diff --check`、`bash hooks/release-check .`、Skill 的 `quick_validate`；smoke 矩阵交由 CI 三主机。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-01 14:51 +0800
- Approved version: v3
- Approved scope: PRD / Plan

## Steps

### Step 1 — State both axes in `CONTRIBUTING.md`

- Goal: 让 § Where the commit lands 同时写出两根轴——任务自己的文档随该任务的 PR 落地；推送权限只路由不隶属任何任务的 bookkeeping。今天这个类目表里有「A task's status and archive」，正是要被移出的那一项。
- Dependencies: none.
- Files: `CONTRIBUTING.md`.
- Implementation checklist:
  - [x] 把 `:39-45` 的类目表改写：任务状态与归档**移出**权限判据，改为一条独立陈述——任务自己的文档（PRD、Spec、Plan、验证记录、archive 提交）在它自己的 PR 内落地（R1）。
  - [x] 明写权限判据保留的范围：纯 Todo 改动、reopen、发布执行、没有对应任务的文档维护（R2）。
  - [x] 明说两根轴互不推导——能否推送回答不了任务文档该放哪，反之亦然（R3）。
  - [x] § Pull requests 增加 draft→ready：以 `gh pr create --draft` 打开，文档提交推上去后 `gh pr ready` 转正；说明这是「还不能合」的可辨识标记（R4、A5）。
  - [x] 发布例外保持行为不变，措辞与新类目一致（R5）。隔离规则（R7）不动。
- Acceptance: A1, A2, A5.
- Verification: 只读该节，回答两个问题——「我任务的 Plan 记录与 archive 去哪」「纯 Todo 改动去哪」。两个都答得出才算过（A2）；需要翻别的文档就是没写成。
- Rollback: `git restore --source=HEAD -- CONTRIBUTING.md`（本步提交前）。
- Status: done

### Step 2 — Correct the two statements that cite it

- Goal: 让 `SKILL.md` 与 `RELEASE.md` 跟着新的类目走，使三份文档描述的是一条规则。
- Dependencies: Step 1 —— 它们是否还准确，是关于新文本的问题。
- Files: `skills/taskflow/SKILL.md`, `RELEASE.md`.
- Implementation checklist:
  - [x] `SKILL.md:121` 不再复述类目表，改为指向 `CONTRIBUTING.md`；现在这句把「任务状态与归档」列为直推项，是新规则下的错误陈述（A3）。
  - [x] `RELEASE.md:152` 把发布称作「one of the three classes it covers」；随新类目改正这句引用，发布本身仍是直推、理由不变（A4）。
  - [x] 两处都只指向，不复述（v2 的 A4 仍有效）。
- Acceptance: A3, A4.
- Verification: 三份文档合读，确认描述的是一个范围而不是两个。
- Rollback: `git restore --source=HEAD -- skills/taskflow/SKILL.md RELEASE.md`（本步提交前）。
- Status: done

### Step 3 — Pin the frozen wording, then let CI adjudicate

- Goal: 用字面串把两处新句子钉住，并把三主机的判决作为本步的验收。
- Dependencies: Steps 1-2。钉子引的是它们的**最终**措辞；措辞未定，钉出来的测试只会在下次改动时因错误的原因失败。
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] 措辞到此**冻结**：钉的字符串从 Step 1/2 改完的文本里复制，不凭记忆重打；只取足够独特的最短片段（先例 `:1391` 取的是段首短句，而不是整段）。
  - [x] 加钉位置放在现有的 skill / `CONTRIBUTING.md` 措辞钉那一段（`:1240-1400` 一带），沿用 `grep -q -F --` 的形态。
  - [x] push 分支、以 draft 开 PR、读 CI 三主机结果。
- Acceptance: A6；A7 的 CI 部分。
- Verification: CI 的 `smoke (ubuntu-latest)` / `smoke (macos-latest)` / `smoke (windows-latest)` 三项绿。本机跑不了整套，记录为未执行，不写成「已验证」。
- Rollback: 加钉这一步是本分支上的普通提交，`git restore` 后重新 push；措辞不改则回滚只涉及 `hooks/smoke-test`。
- Status: done

### Step 4 — Land by the rule being written

- Goal: 让本任务的 Plan 记录与 archive 成为本分支上的提交、留在本 PR 之内——这正是本次要立的规则，也是它与 v1/v2 的唯一差别。
- Dependencies: Step 3.
- Files: `TaskFlowDocs/2026-10-01-taskflow-commit-path/`, `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [x] 把 CI run、PR 模板字段映射与本步的验证结果写进本 Plan，提交并推送（仍在同一 PR）。
  - [x] **先切断那个环**：PR body 的 Task 字段一次写成两份都覆盖的形态——评审期间任务在活动根，最后一个提交把它归档到 `achieved/`。一次写完，避免 archive 之后再改 body。
  - [x] `hooks/task complete --user-accepted`，再 `hooks/archive`；提交并推送（仍在同一 PR）。archive 之后不再有直推 `main` 的动作。
  - [x] `gh pr ready` 转正，交用户合并。
- Acceptance: A8.
- Verification: 合入后 `git log --oneline main` 显示 archive 提交在 PR 的合并之内、而不是合并之后的直推；`git ls-remote origin main` 指向该合并。
- Rollback: PR 被拒则用 `hooks/reopen 2026-10-01-taskflow-commit-path` 取回（`TF-20261001-da6047` 已修复此路径），并按 PRD 的 Risks 记录这次配对的首次实战结果。
- Status: done

## Checkpoints

- After Step 2：三份文档合读，确认只有一条规则，再动测试。
- After Step 3：CI 三主机绿。这一步同时是措辞的最后一次改动——之后只允许追加文档提交。
- After Step 4：PR 内含 archive，且已合入 `main`。

## Verification / Review

- 2026-10-01 Step 4: PR #66 于 2026-10-01 由用户验收；archive 提交与 CI 记录同在该 PR 内，不另开 PR、不合并后直推

- 2026-10-01 Step 3: CI run 36827790066 六项全绿（含 smoke 三主机）；本机未跑整套，见 Preconditions

- 2026-10-01 Step 2: 三份文档合读，描述同一条规则；SKILL 改为指向而不复述类目

- 2026-10-01 Step 1: 只读该节即可答出两个问题；钉子与 git diff 佐证措辞确已改变

- A1–A5 是散文主张，靠阅读判定。本仓库没有能检查规则措辞的命令，本次也不发明一个——与 `2026-09-30-release-ci-test-policy` 和本任务 v2 记录的同一限制一致。
- A6 由 CI 裁定：钉子本身是 smoke 套件的一部分。
- A7 本机执行：`git diff --check`、`bash hooks/release-check .`、Skill 的 `quick_validate`（本机需 `PYTHONUTF8=1`，否则 GBK 解码报错）。
- A8 在合入后按提交拓扑核对，不靠推断。
- 未执行：`bash hooks/smoke-test` 整套。原因见 Preconditions，与 `2026-10-01-artifact-language` 和 `2026-10-01-reopen-todo-path` 记录的是同一件事。
- 已执行（**v3**，2026-10-01，分支 `docs/taskflow-commit-path`，PR #66，draft）：
  - `git diff --check` — clean。`bash hooks/release-check .` — `STATUS: pass`（版本字面量 1.1.2 一致；marketplace pin `5d4fccf6`）。
  - `quick_validate.py skills/taskflow` — `Skill is valid!`。本机须带 `PYTHONUTF8=1`：默认 GBK 解码在该文件上抛 `UnicodeDecodeError`，与 `2026-10-01-artifact-language` 记录的是同一处宿主问题。
  - 新增钉子单独跑过：整套在本机到不了那一段，故把 `:1295-1416` 抽出、配 `HERE` 后以 `sh` 执行，输出 `== a task's documents land with its pull request, not by push permission ==` / `ok`。（同次抽出的相邻段落里 `digest: command not found` 报错来自后文依赖前面定义的工具函数，与本段无关。）
  - 钉子的**非空过**核对：`git diff` 显示四条被钉句子与两处引用的新句子全部是新增行，故对改前文本必然失败；负向钉（`A task's status and archive` 必须消失）指向的正是被删掉的那行。
  - CI（run `36827790066`，sha `5b4cbfc`）— `success`，六项全绿：`smoke (ubuntu-latest)` / `smoke (macos-latest)` / `smoke (windows-latest)` / `release` / `todo-merge-audit` / `evals`。**三个宿主都跑了新增的钉子段**，这是在无解释器一节中止的本机上做不到的。
  - 未执行 `bash hooks/smoke-test` 整套，理由同上。
- 待记（Step 4）：本 PR 的提交拓扑——archive 是否落在合并之内。合入后按 A8 核对并回填本处，不提前写成结论。
- PR 模板字段映射（`.github/pull_request_template.md`，逐字段，PR #66）：
  - `Summary` — 写缺陷与两根轴的新分法：两个任务的文档落在 PR 外（`64ac50d`、`35a4071`、`e603f2c`），以及任务文档 / 不隶属任务的 bookkeeping 的分野。
  - `TaskFlow traceability` 四项 — `Task` 一处，写成覆盖两种状态的形态（评审期间在活动根，本分支末次提交归档到 `achieved/`），这是 Step 4 为切断路径环而定的写法；`Scope`、`Base branch`、`Target repository` 各按实际填写。
  - `Verification` 四项 — 「`git diff --check`」与「Relevant Skill/plugin validation」在首次 push 前即可判，已勾；「Hooks workflow pass」与「Results recorded in the TaskFlow Plan」要等 push 之后，故 PR 开出时留空，本提交补上后者。
  - `Review boundaries` 四项 — 全部勾选；「Known limitations」指向本 Plan 的 Follow-ups 与 PRD 的 Risks，不另起一套说法。
  - 模板未要求的字段一律不加。

## Change Log
- 2026-10-01 reopen — retrieved achieved task `2026-10-01-taskflow-commit-path` for new work; re-approval required before core changes
- 2026-10-01 — **v3**。起因是所有者提出：PR 里的文档操作应当随同一个 PR 提交，不要为文档操作另开 PR。裁定把 landing 规则拆成两根独立的轴——「作者能否推送」路由**不隶属任何任务**的 bookkeeping；任务自己的文档随该任务的 PR 落地。类目表里的「A task's status and archive」因此移出权限判据。v1/v2 的权限判据、隔离规则与发布例外均不变，v3 只改这一项的归属并新增 draft→ready 的机制。
- 2026-10-01 — v3 实现完成并推送（`5b4cbfc`，PR #66 开为 draft）。三处文档改动落定，`hooks/smoke-test` 加六条字面串钉（含一条负向钉：`A task's status and archive` 不得回来）。CI run `36827790066` 六项全绿。
- 2026-10-01 — **一处相对 Plan 的偏离**：Plan 把加钉位置写成「`:1240-1400` 一带的既有措辞钉段」。实际落点是**新起一节**（`:1395-1416`），紧接「a release runs RELEASE.md…」那节之后，而不是并入既有的 artifact-language 钉段——因为本次钉的是 landing 规则，与语言规则不是同一件事，合在一起会让那一节的标题说谎。`:1395` 仍在所写带内，但该带因此变长；记下以免日后再按 `:1240-1400` 去找。

## Follow-ups

- PRD 的 Open Question **已裁定**（2026-10-01，批准轮）：archive 进 PR，与 Plan 记录一起。依据与代价见 PRD 的 Risks 第一条。Step 4 据此执行。
- draft 是平台状态，不是本仓库的机制：没有任何 CI 会因提前合并而失败。若日后给 `main` 开分支保护，应把「必须走 PR」与 draft 的关系一并写清，否则两者的边界仍只靠人守。
- 本任务落地后，`RELEASE.md` 与 `CONTRIBUTING.md` 对同一判据的两处陈述应在下一次发布时再互校一次——那是两者第一次被同时使用。

## Version History

- v1 — the rule stated and landed as `cadee53`; superseded because its text did not carry its own scope.
- v2 — the rule text tightened to state the scope it always had (R6, A7); landed as `7d7a60d`.
- v3 — 拆开两根轴：任务自己的文档随任务的 PR 落地，推送权限只路由不隶属任何任务的 bookkeeping。
