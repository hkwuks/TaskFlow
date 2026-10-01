# Plan — Commit Todo, release, and TaskFlowDocs changes straight to main when the author
> Task version: v1
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

- Worktree `.worktrees/2026-10-01-taskflow-commit-path`, branch `chore/taskflow-commit-path`, based on `main` at `f3d893a`.
- The landing path this task writes is the one it will use: `main` is unprotected and this identity is admin, so Step 3 pushes directly rather than opening a pull request. If that stops being true before Step 3, the fallback is the ordinary PR path, and this Plan is where that deviation gets recorded.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-01 11:35 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — State the landing rule in `CONTRIBUTING.md`

- Goal: put the rule where the branch rule already lives, so a reader meets both at once and cannot take one for the other.
- Dependencies: none.
- Files: `CONTRIBUTING.md`.
- Implementation checklist:
  - [x] State the rule: land by pushing the target branch when the author can push it; open a pull request when they cannot (R1).
  - [x] Name its coverage — Todo entries, a task's status and archive, release execution (R2).
  - [x] Name how "can push" is decided: branch protection and the author's repository role, both checkable (R3).
  - [x] Separate the two mechanisms explicitly: a worktree isolates, the landing rule routes. Say the isolation rule is unchanged (A2).
  - [x] Keep "needs review" a live reason to use a pull request, so the rule does not read as direct-push-by-default (R4).
- Acceptance: A1, A2, A5.
- Verification: read the amended section against A1, A2, A5; confirm the sentence at line 18 still holds with the new text beside it.
- Rollback: `git restore --source=HEAD -- CONTRIBUTING.md` before this step is committed.
- Status: done

### Step 2 — Point the other two documents at it

- Goal: remove the places that imply PR-only, without restating the rule and creating a second source.
- Dependencies: Step 1. The rule has to exist before anything can point at it.
- Files: `RELEASE.md`, `skills/taskflow/SKILL.md`.
- Implementation checklist:
  - [x] `RELEASE.md`: name the permission criterion the direct push already relies on, changing nothing it does (R5, A3).
  - [x] `SKILL.md`: make the PR paragraph and the isolation paragraph distinguish routing from isolation, and point at `CONTRIBUTING.md` rather than restating (A4).
- Acceptance: A3, A4.
- Verification: read Steps 1 and 2 together; confirm no document states the rule twice and none contradicts it.
- Rollback: same as Step 1, scoped to the two files.
- Status: done

### Step 3 — Verify and land

- Goal: run the checks, then land the way the rule says.
- Dependencies: Steps 1 and 2.
- Files: `TaskFlowDocs/2026-10-01-taskflow-commit-path/`, `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [x] Run `git diff --check` and `bash hooks/release-check .`; record results, and any unavailable check as unavailable.
  - [x] Confirm the permission facts still hold before choosing the path — unprotected `main` and a role with `push` — and record the command output that decided it.
  - [x] Push the commit stack to `main` directly, then fast-forward the base checkout. Open a pull request instead if the permission check fails, and record the reversal here.
  - [x] Move `TF-20261001-331f7c` to `done` and archive the task.
- Acceptance: A6.
- Verification: `git ls-remote origin main` names the landed commit; `hooks/release-check .` `pass`; `git diff --check` clean. CI runs on the push to `main` as usual — the rule changes the review path, not the test path.
- Rollback: `git revert` the landed commit and push that, per the same rule. The branch and worktree are discardable before landing.
- Status: done

## Checkpoints

- After Step 2: the three documents read together, before anything is pushed.
- After Step 3: the landed commit verified on the remote, and the Todo sync applied.

## Verification / Review

- A1–A5 are prose claims checked by reading. There is no command that inspects rule wording, and this change does not invent one — the same limitation `2026-09-30-release-ci-test-policy` recorded. Stated here so it is on the record.
- A6 is mechanical: `bash hooks/release-check .` and `git diff --check`. `hooks/smoke-test` covers the hooks, and this change touches none, so per the landing rule now in force it is left to CI on the push to `main`.
- The permission facts in Preconditions are re-checked in Step 3 rather than trusted from the day this Plan was written; branch protection and roles are configuration, and configuration changes.
- 已执行（2026-10-01，本工作树与 `main`）：
  - `git diff --check` — clean；`bash hooks/release-check .` — `STATUS: pass`。
  - 权限复核（落地前重查，未沿用 Preconditions）：`gh api repos/hkwuks/TaskFlow --jq .permissions` → `{"admin":true,"maintain":true,"pull":true,"push":true,"triage":true}`；`.../branches/main/protection` → `404 Branch not protected`。据这两个事实选直推。
  - 落地 — `git push origin HEAD:main`，`f3d893a..cadee53`，未开 PR。**这是改动第一次以它自己定义的路径落地。**
  - CI（run `36811386566`，sha `cadee53`）— `success`，六项全绿：`smoke (ubuntu-latest)` / `smoke (macos-latest)` / `smoke (windows-latest)` / `release` / `todo-merge-audit` / `evals`。
  - 未执行 `bash hooks/smoke-test`：改动不碰 hook，且按本次立下的规则（本地不重跑 CI 已覆盖的检查）交由 CI 裁定。

## Change Log

- 2026-10-01 — 实现、验证、落地完成。改动落在 `CONTRIBUTING.md`（规则本体）、`RELEASE.md`（补上它本就依赖的权限判据）、`skills/taskflow/SKILL.md`（指向规则，不复述）。落地方式为直推 `main`（`cadee53`），CI run `36811386566` 全绿。**记一处过程事实**：本次改动本身仍按原流程走了 worktree + PRD/Plan + 批准，只有「落盘」这一步用了新规则——这正是批准时确认的「走流程，只是落盘直推」。若新规则日后要把任务文档的写作也纳入 base 检出，这条记录就是下一次改动的起点。
- 2026-10-01 — Plan written. The release owner's instruction covered three change classes; the open question about whether `TaskFlowDocs` handling extends to authoring the task documents was answered at the approval round as the narrow reading — bookkeeping only.

## Follow-ups

- The Todo merge driver only runs on local merges (`references/runtime.md:163`). Direct pushes change which merge path is used, and parallel task branches are the case the driver exists for. A future change should either confirm the driver still catches what it was built to catch, or record that hosting-side merges are no longer in the path.
- Once this lands, `RELEASE.md`'s and `CONTRIBUTING.md`'s statements of the same criterion should be checked against each other again in the next release, since that is the first time both are exercised together.

## Version History

- v1 — planning.
