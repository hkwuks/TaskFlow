# Plan — Task worktree teardown

> Task version: v1
> Status: checking

Small task, no spec.

## Reference Pointers

- `hooks/archive:115-121` — the trailing "Stage (commit on the current branch…)" block, the only machine-printed completion guidance.
- `hooks/task:1247-1248` — `complete` re-prints archive's stdout verbatim, so anything archive prints reaches the Agent after `complete`.
- `hooks/task:43-60` — `worktree_kind`, the existing `--absolute-git-dir` + `commondir` test for "linked worktree vs base checkout". Reused rather than reinvented.
- `hooks/repository-check:93-116` — the orphan-directory section, the pattern a read-only report section follows here: it accumulates a list, prints it, and only `needs=1` for integrity findings.
- `skills/taskflow/SKILL.md:299-311` — `### 7. Complete and archive`, the single definition of the archive transaction.
- `CONTRIBUTING.md:18-33` — `## Working branches`, where the isolation rule is stated for creation only.

## Related Tasks

- Related: `TaskFlowDocs/achieved/2026-10-18-single-history-owner/`, `TaskFlowDocs/achieved/2026-10-18-todo-template-repair/` — the two tasks whose merged worktrees are the live evidence for this one.
- Related: `TF-20260919-6b4e21` (Todo growth) — not a dependency; both are "bookkeeping nobody owns" findings from the same audit.

## Skills / Tools Used

- [PRD] `Explore` — purpose: enumerate every lifecycle exit point that could carry the teardown instruction; outcome: succeeded; incorporated: the three end points are `SKILL.md:299-311`, `hooks/archive:119-121`, and `CONTRIBUTING.md`'s landing sequence — and no hook anywhere currently mentions worktrees outside creation.
- [Plan] `general-purpose` — purpose: measure `git worktree remove` semantics in throwaway `/tmp` repositories (cancel-inside, dirty/untracked messages, whether the branch is deleted, whether merge status is checked); outcome: succeeded; incorporated: `worktree remove` succeeds from inside the tree being removed and leaves the shell in a deleted cwd; it deletes the directory only, never the branch; it does **not** check merge status, so the merged test has to be separate; a dirty tree needs `--force`, and `--force` on a clean tree is harmless.

## Preconditions

- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded — `CONTRIBUTING.md` (working branches, checks, PRs), `CODE_STYLE.md` (shell: exit 0/2/3, read-only unless a named transition), `RELEASE.md` (not applicable: this is not a release).
- [x] For remote/fork/PR work: remotes, target repository, base branch, local branch/base, freshness limits, and required checks recorded — `origin` = `hkwuks/TaskFlow`, base = `main` at `30562f7`, branch `chore/worktree-teardown` from `origin/main`.
- [x] For PR creation/update: applicable template path, every required-field mapping, and template verification recorded — `.github/pull_request_template.md`, mapped in the PR body once the work is pushed.
- [x] Missing governance drafts and explicit approvals recorded before they become binding — none needed.

## Approval

- Status: approved
- Approved by: hkwuks
- Approved at: 2026-10-19 20:52 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — State the teardown in the completion path

- Goal: make the end of a task's lifecycle say what happens to its working tree, with the condition that decides when.
- Dependencies: none.
- Files: `hooks/archive`, `hooks/task` (only if the base-checkout case needs suppressing), `skills/taskflow/SKILL.md`, `CONTRIBUTING.md`.
- Implementation checklist:
  - [x] `hooks/archive`'s trailing output gains a teardown paragraph naming `git worktree remove <path>` and stating the condition: after the branch is merged into the base and the tree is clean. The `Git is never invoked` boundary at `hooks/archive:9-10,116` is unchanged — it prints an instruction, it does not run one.
  - [x] The paragraph is printed only when the archive ran inside a linked worktree. Detected with the same `commondir` test `hooks/task:43-60` uses, so a repository that never made a worktree sees byte-identical output. `hooks/smoke-test:652` asserts on the stage lines and still passes.
  - [x] `skills/taskflow/SKILL.md` §7 states the teardown and its condition as part of the completion step, and says the branch's merge is what gates it.
  - [x] `CONTRIBUTING.md` §Working branches states where the working tree goes at the end, beside the rule that says where it comes from.
- Acceptance: a `complete` inside a task worktree prints the teardown instruction; a `complete` in the base checkout does not; `bash hooks/smoke-test:652`'s stage assertion still passes.
- Verification: smoke section asserting both directions, mutation-checked.
- Rollback: revert the commit.
- Status: done

### Step 2 — Report worktrees that should have been torn down

- Goal: a leftover merged worktree becomes visible instead of accumulating silently.
- Dependencies: Step 1 (the instruction has to exist before reporting that it was skipped).
- Files: `hooks/repository-check`.
- Implementation checklist:
  - [x] New read-only section listing every linked worktree whose branch is an ancestor of the base branch **and** whose tree is clean, with the command that removes it.
  - [x] Silent for: the main working tree (the first `git worktree list --porcelain` record); the worktree the check is run from; a dirty or untracked-file-carrying tree; a branch with any commit not in the base; a detached record, which has no branch to compare.
  - [x] Reported worktrees do **not** set `needs`: the check stays `STATUS: pass` when a stale worktree is the only finding, so a real `needs-user-input` keeps meaning what it means. Stated in the section's comment.
  - [x] Dropped from the plan as written: the `commondir` test. It is redundant here — the first record is the main working tree by position, every later record is a linked tree by construction, and `git -C <path> rev-parse --absolute-git-dir` already rejects a directory that is gone. One condition fewer that can disagree with the rest of the suite.
  - [x] Added during implementation: the base is the **main working tree's** upstream, not the current checkout's. Read from the current checkout the section goes blind exactly where it is most useful, because a task worktree's own branch has no upstream. Caught by mutation M1 (see `## Verification / Review`).
- Acceptance: fixture with one merged-clean and one unmerged worktree names exactly the first and exits `0`; this repository names its two real ones.
- Verification: smoke assertions for each silence condition, each mutation-checked.
- Rollback: revert the commit.
- Status: done

## Checkpoints

## Verification / Review

Pushed as `0e7eb86` on `chore/worktree-teardown`, pull request #87 as a draft, per `CONTRIBUTING.md` — a task's documents land with the task inside its own pull request, and the PR body carries the landing claim.

Local checks, run in this worktree on 2026-10-19 before the commit.

| Check | Result |
| --- | --- |
| `bash hooks/smoke-test <dir>` | exit 0, `ALL SMOKE PASSED`, 75 `ok` sections (74 before; the two new sections are the archive teardown and the repository-check worktree report) |
| `bash hooks/todo-check .` | `STATUS: pass` |
| `bash hooks/repository-check .` | exit 0, `STATUS: pass`, and it names the two real stale worktrees — `.worktrees/single-history-owner` and `.worktrees/todo-template-repair` |
| `bash -n` on the three changed hooks | clean |
| `docker run --rm -i bash:3.2 bash -n` on the three changed hooks | clean — the floor is real here: the `?*)` case arm and the heredoc parser must both survive 3.2 |
| `git diff --check` | clean |
| `quick_validate.py skills/taskflow` | `Skill is valid!` |

The smoke suite is run locally here because the change is exactly a surface it exercises; `CONTRIBUTING.md` sanctions the local run for the pre-push, and CI is still the authority — its verdict is recorded below, not inferred.

### CI, and the macOS failure it caught

Run [`39259125010`](https://github.com/hkwuks/TaskFlow/actions/runs/39259125010) on `0e7eb86`, the first push: `evals`, `release`, `todo-merge-audit`, `smoke (ubuntu-latest)` and `smoke (windows-latest)` passed, and **`smoke (macos-latest)` failed** at `FAIL merged worktree not named with its branch`. Run [`39259315368`](https://github.com/hkwuks/TaskFlow/actions/runs/39259315368) on `5bfa4c0` repeated it, unchanged.

The cause is a host difference no local run on Linux could show. macOS sets `$TMPDIR` to `/var/folders/…`, and `/var` is a symlink to `/private/var`; `git worktree list --porcelain` reports **resolved** paths, so the fixture registered `/private/var/…/repository-check-worktrees/.worktrees/merged` while the assertion looked for `/var/…/…`. The fixture root is now put through `pwd -P` before any path is compared. That is an identity transform on Linux and Windows, and it is the same class of defect as `taskflow`'s earlier `--git-dir` drive-letter bug: a path that the tool and the test spell differently.

Verified by reproducing it on Linux with a symlinked root: a fixture built through `/tmp/wtlink -> /tmp/wtreal` is registered by Git as `/tmp/wtreal/…`, and only the `pwd -P` form matches. Note that the full suite already fails from a symlinked root for an **unrelated, pre-existing** reason (`the denial does not name the store holding them`), confirmed against the tree at `HEAD` before this branch — so the reproduction for this fix is the section, not the whole suite.

**Verdict: run [`39260080438`](https://github.com/hkwuks/TaskFlow/actions/runs/39260080438) on `ed609fb` — `success`, all six jobs green:** `evals`, `release`, `todo-merge-audit`, and `smoke` on `ubuntu-latest`, `macos-latest`, and `windows-latest`. The macOS job is the one that had failed, so it is also the one that confirms the fix.

Mutation-checked on a copy of the tree under `/tmp`; the real worktree was never mutated, and each mutation was restored from a backup taken immediately before it.

| # | Mutation | Red at |
| --- | --- | --- |
| 1 | read the base from the current checkout instead of the main working tree | `FAIL the section went blind when run from a task worktree` |
| 2 | drop the clean-tree test | `FAIL a worktree with untracked work was reported for removal` |
| 3 | drop the merge test | `FAIL an unmerged branch was reported for removal` |
| 4 | never skip the worktree the check runs from | `FAIL the current worktree was reported for removal` |
| 5 | print the teardown from the main working tree too | `FAIL archive told a main working tree to remove itself` |
| 6 | drop the merge condition from the printed sentence | `FAIL teardown instruction did not name the branch that gates it` |
| 7 | drop the teardown block entirely | `FAIL archive did not name the worktree to remove` |
| 8 | make a stale worktree set `needs` | `FAIL stale worktree changed the verdict: 2` |

Three of these found gaps in the assertions rather than in the code, and the assertions were fixed before the mutation was rerun:

- **M1 passed on the first attempt.** The obvious assertion — that the worktree the check runs from is not named — is also satisfied by a section that names nothing at all, and the fixture's base was the current checkout's upstream, so it was satisfied for the wrong reason. The assertion now also requires a merged sibling to still be named, which is what fails when the base is read from the wrong place. A second problem surfaced with it: the silence assertions matched the path anywhere in the output, and the printed instruction line contains the placeholder `<path>` — every one of them now anchors on `- `, the one shape a report line has.
- **M5 passed on the first attempt.** The plain archive fixture is a bare directory, not a Git repository, so the git-dir lookup failed for a reason unrelated to the linked-worktree test, and a mutation that widened that test still printed nothing. A second archive now runs from a real Git repository's main working tree.
- **The fixture's base had to move with the merge.** `git merge` in the fixture updates `refs/heads/main` but not `refs/remotes/origin/main`, which is what `@{upstream}` resolves to, so the "now merged" assertion was testing a ref that never moved.

## Change Log

- 2026-10-19 v1 planning — both documents written from the audit entry, with the `complete`-runs-before-the-merge distinction that decides the design.
- 2026-10-19 v1 work revision — implementation: `commondir` dropped from `repository-check` as redundant; the base corrected to the main working tree's upstream; three assertions strengthened after M1 and M5 passed; `SKILL.md` §7 and `CONTRIBUTING.md` §Working branches touched in Step 1.

## Follow-ups

- The squash-merge blind spot in the merged test (PRD `## Risks / Deferred Items`) is recorded, not solved: an ancestry test cannot see a squash merge.
- Removing the two worktrees this repository already carries is an operator action after this lands, not part of the change.

## Version History

- v1 — planning.
