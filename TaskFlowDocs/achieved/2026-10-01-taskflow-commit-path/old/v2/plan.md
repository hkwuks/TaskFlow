# Plan — Commit Todo, release, and TaskFlowDocs changes straight to main when the author
> Task version: v2
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `CONTRIBUTING.md` — Working branches (lines 16–33), the section that states the branch rule this change qualifies; and the release exception at line 14.
- `RELEASE.md` — line 5 (runs on the base checkout, no branch), lines 101–106 and 127–134 (the atomic push to `main` and why it is a direct push).
- `skills/taskflow/SKILL.md` — line 75 (the PR paragraph), lines 112–119 (Isolate before the first document).
- `skills/taskflow/references/runtime.md` — lines 134, 139 (`promote` refuses outside a task worktree), line 163 (the Todo merge driver runs only on local merges).
- `TaskFlowDocs/repository-docs/index.md` — routing record; `CONTRIBUTING.md` is the authoritative source for branch and commit rules.

## Related Tasks

- `TF-20261001-51d9c8` — the artifact-language question from the same message. Separate concern, same origin; deliberately not folded in.
- `TF-20260928-3910fb` — release-process reduction, a different axis (what runs at release time, not where the commit lands).

## Skills / Tools Used

- [PRD] Unaided — 未调用能力：需求是发布所有者直接给出的三句话（Todo 改动、发版、处理 TaskFlowDocs 的落地路径），PRD 的增量是把它与仓库既有的隔离规则对齐并界定范围，属仓库策略判断而非需求获取。已考虑 `agent-skills:idea-refine`（对规则做假设压力测试），但它的产出是发散选项，而本条的待解问题是两条既有规则的关系，PRD 的 Risks 已逐条列出未解项，故不调用。considered: requirements elicitation and framing。
- [Plan] Unaided — 未调用能力：分解是把一份规则拆到三处文档，每处的改动都是同一形态（陈述规则 / 指过去），步骤顺序由「先有规则文本，再让别处指向它」决定。considered: work breakdown and task decomposition。

## Preconditions

- Worktree `.worktrees/2026-10-01-taskflow-commit-path`, branch `chore/taskflow-commit-path-v2`, based on `main` at `1c23f0d` — the commit that recorded the reopen. v1's branch and its commit `cadee53` are already on `main` and are not reopened.
- The landing path this task writes is the one it will use: `main` is unprotected and this identity is admin, so Step 3 pushes directly rather than opening a pull request. If that stops being true before Step 3, the fallback is the ordinary PR path, and this Plan is where that deviation gets recorded.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-01 12:01 +0800
- Approved version: v2
- Approved scope: PRD / Plan

## Steps

### Step 1 — State the rule's scope in `CONTRIBUTING.md`

- Goal: make the section say which changes it routes, so the sentence at `CONTRIBUTING.md:37` cannot be read as covering every change.
- Dependencies: none.
- Files: `CONTRIBUTING.md`.
- Implementation checklist:
  - [x] Open the section by naming what it routes — bookkeeping-class commits — instead of asking a general landing question (R6).
  - [x] Say plainly that an ordinary code, hook, Skill, or review-needing documentation change keeps its pull request (A7).
  - [x] Leave the permission criterion, the worktree/isolation separation, and the checkable facts as they are; v1 got those right.
- Acceptance: A1, A2, A5, A7.
- Verification: read the section **alone** against A7 — a contributor must be able to answer "how does a code change land?" from it, without any other document.
- Rollback: `git restore --source=HEAD -- CONTRIBUTING.md` before this step is committed.
- Status: done

### Step 2 — Check the two documents that point at it

- Goal: confirm `RELEASE.md` and `SKILL.md` still describe the narrowed rule, and correct them only if Step 1 makes their wording wrong.
- Dependencies: Step 1. Whether they are still accurate is a question about the new text.
- Files: `RELEASE.md`, `skills/taskflow/SKILL.md`.
- Implementation checklist:
  - [x] Read `RELEASE.md` against the new wording. A release is one of the covered classes, so it should need nothing; change it only if that turns out false.
  - [x] `SKILL.md` summarises the coverage as "the changes with nothing to review" — check that still matches the stated scope, and correct it if not.
  - [x] Do not restate the scope in either; they point at `CONTRIBUTING.md` (v1's A7, still in force).
- Acceptance: A3, A4.
- Verification: read all three together and confirm they describe one scope, not two.
- Rollback: `git restore --source=HEAD -- RELEASE.md skills/taskflow/SKILL.md` before this step is committed.
- Status: done

### Step 3 — Verify and land

- Goal: run the checks, then land the wording fix by direct push.
- Dependencies: Steps 1 and 2.
- Files: `TaskFlowDocs/2026-10-01-taskflow-commit-path/`, `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [x] Run `git diff --check` and `bash hooks/release-check .`; record results, and any unavailable check as unavailable.
  - [x] Re-check the permission facts before choosing the path, and record the command output that decided it.
  - [x] Push the commit stack to `main` directly. Open a pull request instead if the permission check fails, and record the reversal here.
  - [x] Move `TF-20261001-331f7c` to `done` and archive this task.
- Acceptance: A6.
- Verification: `git ls-remote origin main` names the landed commit; `hooks/release-check .` `pass`; `git diff --check` clean; CI green on the push. `hooks/smoke-test` is left to CI — the change touches no hook, and that is the rule this task landed.
- Rollback: `git revert` the landed commit and push that, per the same rule.
- Status: done

## Checkpoints

- After Step 2: the three documents read together, before anything is pushed.
- After Step 3: the landed commit verified on the remote, and the Todo sync applied.

## Verification / Review

- A1–A5 are prose claims checked by reading. There is no command that inspects rule wording, and this change does not invent one — the same limitation `2026-09-30-release-ci-test-policy` recorded. Stated here so it is on the record.
- A6 is mechanical: `bash hooks/release-check .` and `git diff --check`. `hooks/smoke-test` covers the hooks, and this change touches none, so per the landing rule now in force it is left to CI on the push to `main`.
- The permission facts in Preconditions are re-checked in Step 3 rather than trusted from the day this Plan was written; branch protection and roles are configuration, and configuration changes.
- 已执行（**v1**，2026-10-01，当时的 `chore/taskflow-commit-path` 工作树与 `main`）——保留在此以延续记录，v1 的完整文档见 `old/v1/`：
  - `git diff --check` — clean；`bash hooks/release-check .` — `STATUS: pass`。
  - 权限复核（落地前重查，未沿用 Preconditions）：`gh api repos/hkwuks/TaskFlow --jq .permissions` → `{"admin":true,"maintain":true,"pull":true,"push":true,"triage":true}`；`.../branches/main/protection` → `404 Branch not protected`。据这两个事实选直推。
  - 落地 — `git push origin HEAD:main`，`f3d893a..cadee53`，未开 PR。**这是改动第一次以它自己定义的路径落地。**
  - CI（run `36811386566`，sha `cadee53`）— `success`，六项全绿：`smoke (ubuntu-latest)` / `smoke (macos-latest)` / `smoke (windows-latest)` / `release` / `todo-merge-audit` / `evals`。
  - 未执行 `bash hooks/smoke-test`：改动不碰 hook，且按本次立下的规则（本地不重跑 CI 已覆盖的检查）交由 CI 裁定。
- 已执行（**v2**，2026-10-01）：
  - A7 —— 单独读 `CONTRIBUTING.md` § Where the commit lands 即可答出「代码改动怎么落地 = PR」，依据是这一节自己写的 `Everything else keeps its pull request. Code, hooks, the Skill, and any document whose wording is worth reviewing... If you are unsure which side a change falls on, it is a pull request.` v1 做不到这一点，那时范围只由末句隐含。
  - 顺带发现并修正：`RELEASE.md` 把判据写成「the criterion `CONTRIBUTING.md` states for **every commit**」，而发布只是三类之一——措辞同样越界；`SKILL.md` 的指引同病。两处随本次改正。
  - `git diff --check` — clean；`bash hooks/release-check .` — `STATUS: pass`。
  - 权限复核（落地前重查，未沿用 Preconditions）：`permissions` 含 `push: true`；`.../branches/main/protection` → `404 Branch not protected`。
  - 落地 — `git push origin HEAD:main`，`1c23f0d..7d7a60d`，未开 PR。CI（run `36813488643`，sha `7d7a60d`）— `success`。
  - **过程中撞到一个真实缺陷**（已记为 `TF-20261001-da6047`，本次不修）：`hooks/reopen` 把目录搬回活动根后，没有把 Todo 的 `Task:` 从 `achieved/...` 改回活动路径，而 `hooks/archive` 是会改的。于是 `hooks/task state` 报 `Todo entry not found: 2026-10-01-taskflow-commit-path`。本次手工改正那一行才继续；修法属于那条 todo。

## Change Log
- 2026-10-01 reopen — retrieved achieved task `2026-10-01-taskflow-commit-path` for new work; re-approval required before core changes
- 2026-10-01 — v2 实现、验证、落地完成。`CONTRIBUTING.md` 改为**先声明路由范围**（bookkeeping 三类）再讲判据，并明写「其余一律走 PR、拿不准就走 PR」；`RELEASE.md` 与 `SKILL.md` 中把范围写成「every commit」的两处随本次改正。落地仍为直推 `main`（`7d7a60d`），CI run `36813488643` `success`。
- 2026-10-01 — **v2**。把规则的字面收紧到它一直以来的意图。起因是用户追问这条规则的范围（「所有开发都优先直推，还是只有维护走直推」）；答复是窄范围，而落地的 `CONTRIBUTING.md:37` 写成了普适句、`:39` 的三类沦为例子，只有 `:51` 末尾一句隐含地把范围拉回。PRD 的 R6 与 A7 即为此而加。v1 的改动内容与落地方式不变。
- 2026-10-01 reopen — retrieved achieved task `2026-10-01-taskflow-commit-path` for new work; re-approval required before core changes

- 2026-10-01 — 实现、验证、落地完成。改动落在 `CONTRIBUTING.md`（规则本体）、`RELEASE.md`（补上它本就依赖的权限判据）、`skills/taskflow/SKILL.md`（指向规则，不复述）。落地方式为直推 `main`（`cadee53`），CI run `36811386566` 全绿。**记一处过程事实**：本次改动本身仍按原流程走了 worktree + PRD/Plan + 批准，只有「落盘」这一步用了新规则——这正是批准时确认的「走流程，只是落盘直推」。若新规则日后要把任务文档的写作也纳入 base 检出，这条记录就是下一次改动的起点。
- 2026-10-01 — Plan written. The release owner's instruction covered three change classes; the open question about whether `TaskFlowDocs` handling extends to authoring the task documents was answered at the approval round as the narrow reading — bookkeeping only.

## Follow-ups

- The Todo merge driver only runs on local merges (`references/runtime.md:163`). Direct pushes change which merge path is used, and parallel task branches are the case the driver exists for. A future change should either confirm the driver still catches what it was built to catch, or record that hosting-side merges are no longer in the path.
- Once this lands, `RELEASE.md`'s and `CONTRIBUTING.md`'s statements of the same criterion should be checked against each other again in the next release, since that is the first time both are exercised together.

## Version History

- v1 — the rule stated and landed as `cadee53`; superseded because its text did not carry its own scope.
- v2 — the rule text tightened to state the scope it always had (R6, A7).
