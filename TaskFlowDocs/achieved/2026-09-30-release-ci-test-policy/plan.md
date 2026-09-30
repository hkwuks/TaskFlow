# Plan — A release skips re-running tests that CI already ran green on the same revision,
> Task version: v2
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `RELEASE.md` — the procedure being amended (Validation checklist; step 6 stays out of scope).
- `CONTRIBUTING.md` — the Checks section, and the Working-branches line about running the suite on the branch whose files changed.
- `.github/pull_request_template.md` — the verification checklist a PR carries.
- `README.md`, `README.zh-CN.md` — the sentences describing what CONTRIBUTING requires before a pull request.
- `.github/workflows/hooks.yml` — what CI actually runs, and when. Triggers are `pull_request` and `push` on `main` only (lines 3–7); jobs are `smoke` on ubuntu/macos/windows, `release`, `todo-merge-audit`, `evals`.
- `TaskFlowDocs/todo.md` — `TF-20260930-c4e4c8` (this task's origin) and `TF-20260928-3910fb` (same theme, not folded in).

## Related Tasks

- `TF-20260928-3910fb` — the manual three-host catalog validation. Same theme, separate task; the division of labour keeps it out.
- `TF-20260929-3fc4b8` — the live-session verification of the 1.1.2 pre-write gate. Unrelated to this change, but its evidence is captured during Step 4.

## Skills / Tools Used

- [PRD] Unaided — v2 未调用能力：需求增量是范围扩展（PR 模板 + 两份 README）与所有者当场给出的双向原则，两者都不需要需求获取；v1 已由 `agent-skills:spec-driven-development` 建立的需求框架未变，v2 沿用其六要素结构。considered: requirements elicitation and framing。
- [Plan] Unaided — v2 未调用能力：分解增量是把一处文档改动拆成同一形态的 Step 3，步骤数从 3 变 4，内部顺序不变；v1 已由 `agent-skills:planning-and-task-breakdown` 建立的 acceptance / verification / rollback 结构未变。considered: work breakdown and task decomposition。

## Preconditions

- Worktree `.worktrees/2026-09-30-todo-release-ci-policy`, branch `chore/todo-release-ci-policy`, based on `main` at `ff15458`.
- Plugin 1.1.2 installed, so the pre-write gate is active on this host. Observed here, not assumed: the first `prd.md` write was denied with the stage and the `task unaided` command in the message, and was allowed only after a capability invocation was recorded.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-01 00:06 +0800
- Approved version: v2
- Approved scope: PRD / Plan

## Steps

### Step 1 — Amend `RELEASE.md`

- Goal: stop requiring a re-run of the smoke suite when CI already adjudicated an equivalent revision, without weakening any check that only a release commit can produce, and state both directions of the rule.
- Dependencies: none.
- Files: `RELEASE.md`.
- Implementation checklist:
  - [x] Split the Validation checklist: the four CI-uncovered checks stay unconditional, the smoke suite becomes conditional.
  - [x] State the predicate (R2) and why "the same revision" is the wrong test: the tag names a new commit, and the tag and pin are pushed together, so CI has not seen it at checklist time.
  - [x] State R7 in both directions, so the skip cannot read as an exemption.
  - [x] Require the release notes to name the CI run relied on and the comparison made (R4).
  - [x] Leave step 6's catalog validation untouched.
- Acceptance: A1, A2, A3.
- Verification: read the amended section against A1–A3 line by line; `bash hooks/release-check .` still reports `pass`.
- Rollback: `git restore --source=HEAD -- RELEASE.md` before this step is committed; `git revert` after.
- Status: done

### Step 2 — Amend `CONTRIBUTING.md`

- Goal: name CI as the preferred test authority for every pull request, state the maintenance obligation that makes that safe, and remove the line that contradicts it.
- Dependencies: Step 1. The principle has to exist before the working-branches line can be checked against it, and A7 is a consistency claim about the set.
- Files: `CONTRIBUTING.md`.
- Implementation checklist:
  - [x] Rewrite the Checks section so CI is the authority, a local run is for what CI structurally cannot cover, and the local-only checks stay named.
  - [x] State that a surface CI does not exercise is added to CI in the same change, with a local run as the fallback (R6, A6).
  - [x] Reword the Working-branches line that required running the suite on the branch whose files changed, so it no longer contradicts the section above it.
  - [x] Do not restate RELEASE.md's predicate; point at it instead (A7).
- Acceptance: A4, A6, A7.
- Verification: read Steps 1 and 2 together against A7; confirm no rule is weakened.
- Rollback: same as Step 1, scoped to `CONTRIBUTING.md`.
- Status: done

### Step 3 — Remove the two remaining local-run requirements

- Goal: bring `.github/pull_request_template.md` and both READMEs into agreement with the rule, so nothing in the repository still asks for a local run of a CI-covered check.
- Dependencies: Step 2. The template and the READMEs describe what CONTRIBUTING requires, so they follow it.
- Files: `.github/pull_request_template.md`, `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [x] Replace the template's `bash hooks/smoke-test` checkbox with one that asks what CI ran, keeping the field required (A8).
  - [x] Update the English and Chinese sentences that name `hooks/smoke-test` among CONTRIBUTING's pre-pull-request checks, keeping the suite described accurately as something CI runs (A9).
  - [x] Keep the Chinese and English text saying the same thing.
- Acceptance: A8, A9.
- Verification: grep the repository for `smoke-test` in documents and check each hit against R8 by reading; no hit may require a local run of it.
- Rollback: same as Step 1, scoped to the three files.
- Status: done

### Step 4 — Verify, publish, and sync

- Goal: get CI's verdict on the change, then close the Todo item and record the gate evidence.
- Dependencies: Steps 1–3.
- Files: `TaskFlowDocs/2026-09-30-release-ci-test-policy/`, `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [x] Run `git diff --check`, `bash hooks/release-check .`, and `bash hooks/repository-check .`; record results and any unavailable check as unavailable.
  - [x] Push the branch and let CI's matrix give the verdict the change itself argues for (A5). Do not claim a local suite result that was not obtained — the change would be self-refuting.
  - [x] Record, against `TF-20260929-3fc4b8`, the live gate observation from Preconditions: the deny, its message, and the allow after invocation.
  - [x] Once CI is green and the owner merges, move `TF-20260930-c4e4c8` to `done` and archive this task.
- Acceptance: A5.
- Verification: `gh pr checks <n>` all green; the recorded evidence quoted from the observed message, not paraphrased.
- Rollback: the branch and PR are discardable before merge; nothing on `main` changes until the owner merges.
- Status: done

## Checkpoints

- After Step 2: `RELEASE.md` and `CONTRIBUTING.md` read together against A1–A7.
- After Step 3: the whole-repository grep against R8, before anything is pushed.
- After Step 4: CI green, and the Todo sync withheld until the merge actually happens.

## Verification / Review

- A1, A3, A4, A6, A7, A8, and A9 are prose claims checked by reading, not by a command. Stated here so the limitation is on the record; the change itself is about preferring CI, so it must not invent a local check to fill this gap.
- The command-level checks available are `hooks/release-check` (version literals, catalog pin), `git diff --check`, and the Step 3 grep. None inspects the amended prose. `hooks/smoke-test` exercises the hooks, which this change does not touch — running it here locally would contradict the rule being written.
- 已执行（2026-10-01，本工作树）：
  - `git diff --check` — clean。
  - `bash hooks/release-check .` — `STATUS: pass`；8 处版本字面量一致，两个 catalog pin 都解析到 `5d4fccf`。
  - `bash hooks/repository-check .` — `STATUS: needs-user-input`，唯一原因是既存孤儿目录 `TaskFlowDocs/achieved/2026-09-10-repository-document-placement`（早于本任务，本任务未触碰）；另有「工作树有未提交改动」的提示，提交后即消失。
  - R8 复查 — `grep -rn smoke-test --include=*.md` 后逐条比对：余下命中全部是**描述**套件（`README.md:354` 与 `README.zh-CN.md:315` 的表格、两份 README 的文件树、`hooks/README.md`、`references/runtime.md`）或**条件性**提及（`CONTRIBUTING.md:31`、`RELEASE.md:69`），无一处要求本地必须跑。
  - 未执行 `bash hooks/smoke-test`：本次改动不碰 `hooks/` 与 `skills/`，且该套件在本机跑不完（无解释器章节因 MSYS 软链二进制缺 DLL 而中止，未修改的 `origin/main` 在同一处同样失败）。本地不跑它**正是本次改动要立的规则**，不是回避；判定交给 CI 三平台矩阵，结果记在 PR 里。
  - CI（PR #62，run `36742917605`）— 六项全绿：`smoke (ubuntu-latest)` / `smoke (macos-latest)` / `smoke (windows-latest)` / `release` / `todo-merge-audit` / `evals`。这一步本身就是本改动主张的做法：本地不跑套件，判定由 CI 给出，而且给的是三台宿主而不是一台。
  - 合入 — PR #62 以 merge commit `3094f69` 进入 `main`（2026-09-30T16:20:52Z）。

## Change Log

- 2026-10-01 — 实现与验证完成并合入。PR #62 六项 CI 全绿（run `36742917605`）后以 merge commit `3094f69` 进入 `main`。本地**未**跑 `hooks/smoke-test`——这正是本改动所立的规则：CI 覆盖得到的交给 CI，此处 CI 还多给了两台宿主。实际改动的五处文档：`RELEASE.md`、`CONTRIBUTING.md`、`.github/pull_request_template.md`、`README.md`、`README.zh-CN.md`。
- 2026-10-01 — v2. Implementing v1 surfaced `.github/pull_request_template.md:14` and `README.md:361` / `README.zh-CN.md:322` as further local-run requirements; left alone they would have contradicted the rule on merge. Release owner approved the version bump and required R7: state both directions, so a preference for CI never reads as an exemption.
- 2026-09-30 — Plan written. Scope widened mid-PRD by the release owner: the CI-first rule covers every pull request, and CI's own upkeep is part of it. Recorded as R5/R6 rather than as a follow-up, because the preference is only safe while CI covers the right surfaces.
- 2026-09-30 — Recorded the live pre-write gate observation from this session (deny on the first `prd.md` write, allow after a capability invocation) as evidence for `TF-20260929-3fc4b8`.

## Follow-ups

- `TF-20260928-3910fb` — fold the three-host catalog validation into the same "what CI cannot cover" rule once this lands, so the release procedure has one principle instead of two exceptions.
- Drift among the five documents carrying this rule is now a named risk rather than a hypothetical; a future change should either reduce the count or state which document is authoritative for which half.

## Version History

- v1 — planning; superseded after implementation surfaced three further places to amend.
- v2 — scope extended to the pull-request template and both READMEs, and the rule stated in both directions.
