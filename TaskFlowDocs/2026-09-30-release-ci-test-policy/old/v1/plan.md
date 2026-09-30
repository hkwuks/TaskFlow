# Plan — A release skips re-running tests that CI already ran green on the same revision,
> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

- `RELEASE.md` — the procedure being amended (Validation checklist at lines 47–73; step 6 at 111 stays out of scope).
- `CONTRIBUTING.md` — the Checks section at lines 39–49 being amended.
- `.github/workflows/hooks.yml` — what CI actually runs, and when. Triggers are `pull_request` and `push` on `main` only (lines 3–7); jobs are `smoke` on ubuntu/macos/windows, `release`, `todo-merge-audit`, `evals`.
- `TaskFlowDocs/todo.md` — `TF-20260930-c4e4c8` (this task's origin) and `TF-20260928-3910fb` (same theme, not folded in).

## Related Tasks

- `TF-20260928-3910fb` — the manual three-host catalog validation. Same theme, separate task; A7's two-document split deliberately leaves it alone.
- `TF-20260929-3fc4b8` — the live-session verification of the 1.1.2 pre-write gate. Unrelated to this task's change, but its evidence is captured during Step 3.

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — 用于需求文档成形：它给出目标/成功判据/边界的六要素结构与「先亮假设」检查表。据此把发布所有者中途扩的范围（所有 PR 优先 CI、CI 须跟上）落成显式 R5/R6 与 A6/A7，而不是留在 Goal 里当隐含项；两条边界问题（判据用严格相等还是形态判断、跳过时记什么）也随之被 R2/R4 收口。
- [Plan] `agent-skills:planning-and-task-breakdown` — 用于分解：它给出每步 acceptance / verification / files / rollback 的结构，据此把「两篇文档」拆成 Step 1/2/3，并把 Step 2 排在 Step 1 之后——A7 是两篇一致性的断言，必须先有原则再谈程序。

## Preconditions

- Worktree `.worktrees/2026-09-30-todo-release-ci-policy`, branch `chore/todo-release-ci-policy`, based on `main` at `ff15458`.
- Plugin 1.1.2 installed, so the pre-write gate is active on this host. Observed here, not assumed: the first `prd.md` write was denied with the stage and the `task unaided` command in the message, and was allowed only after a capability invocation was recorded.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-30 23:59 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — Amend `RELEASE.md`

- Goal: stop requiring a re-run of the smoke suite when CI already adjudicated an equivalent revision, without weakening any check that only a release commit can produce.
- Dependencies: none.
- Files: `RELEASE.md`.
- Implementation checklist:
  - [ ] Replace the unconditional `bash hooks/smoke-test` line in the Validation checklist with a conditional rule.
  - [ ] State the predicate (R2) and why "the same revision" is the wrong test: the tag names a new commit, and the atomic push means CI has not run on it at checklist time.
  - [ ] Keep `hooks/release-check`, `hooks/repository-check`, `quick_validate.py`, and `git diff --check` unconditional, and say why (R3).
  - [ ] Require the release notes to name the CI run relied on and the comparison made (R4).
  - [ ] Leave step 6's catalog validation untouched.
- Acceptance: A1, A2, A3.
- Verification: read the amended section against A1–A3 line by line; `bash hooks/release-check .` still reports `pass`.
- Rollback: `git restore --source=HEAD -- RELEASE.md` before Step 1 is committed; `git revert` after.
- Status: pending

### Step 2 — Amend `CONTRIBUTING.md`

- Goal: name CI as the preferred test authority for every pull request, and state the maintenance obligation that makes that safe.
- Dependencies: Step 1. The principle has to be stated before the procedure that applies it can be checked against it, and A7 is a consistency claim about the pair.
- Files: `CONTRIBUTING.md`.
- Implementation checklist:
  - [ ] Rewrite the Checks section so CI is the authority and a local run is for what CI structurally cannot cover.
  - [ ] State that a surface CI does not exercise is added to CI in the same change, with a local run as the fallback (R6, A6).
  - [ ] Do not restate RELEASE.md's predicate; point at it instead (A7).
- Acceptance: A4, A6, A7.
- Verification: read Step 1's and Step 2's text together against A7; confirm no rule is weakened.
- Rollback: same as Step 1, scoped to `CONTRIBUTING.md`.
- Status: pending

### Step 3 — Verify, publish, and sync

- Goal: get CI's verdict on the change, then close the Todo item and record the gate evidence.
- Dependencies: Steps 1 and 2.
- Files: `TaskFlowDocs/2026-09-30-release-ci-test-policy/`, `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [ ] Run `git diff --check`, `bash hooks/release-check .`, and `bash hooks/repository-check .`; record results and any unavailable check as unavailable.
  - [ ] Push the branch and let CI's matrix give the verdict the change itself argues for (A5). Do not claim a local suite result that was not obtained.
  - [ ] Record, against `TF-20260929-3fc4b8`, the live gate observation from Preconditions — the deny, its message, and the allow after invocation.
  - [ ] Once CI is green and the owner merges, move `TF-20260930-c4e4c8` to `done` and archive this task.
- Acceptance: A5.
- Verification: `gh pr checks <n>` all green; the recorded evidence is quoted from the observed message, not paraphrased.
- Rollback: the branch and PR are discardable before merge; nothing on `main` changes until the owner merges.
- Status: pending

## Checkpoints

- After Step 2: both documents read together against A1–A7, before anything is pushed.
- After Step 3: CI green, and the Todo sync withheld until the merge actually happens.

## Verification / Review

- A4 and A7 are prose claims and are checked by reading, not by a command. Stated here so the limitation is on the record.
- The only command-level checks available are `hooks/release-check` (version literals, catalog pin) and `git diff --check`. Neither inspects the amended prose. `hooks/smoke-test` exercises the hooks, which this change does not touch.

## Change Log

- 2026-09-30 — Plan written. Scope widened mid-PRD by the release owner: the CI-first rule covers every pull request, and CI's own upkeep is part of it. Recorded as R5/R6 rather than as a follow-up, because the preference is only safe while CI covers the right surfaces.
- 2026-09-30 — Recorded the live pre-write gate observation from this session (deny on the first `prd.md` write, allow after a capability invocation) as evidence for `TF-20260929-3fc4b8`.

## Follow-ups

- `TF-20260928-3910fb` — fold the three-host catalog validation into the same "what CI cannot cover" rule once this lands, so the release procedure has one principle instead of two exceptions.

## Version History

- v1 — planning.
