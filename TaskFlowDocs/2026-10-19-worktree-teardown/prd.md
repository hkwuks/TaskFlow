# Removing a task worktree is nobody's job

> Task version: v1
> Status: checking

## Goal

Make tearing down a task's working tree part of the lifecycle, and make a leftover one visible. Today `hooks/task complete` archives the directory and closes the Todo entry, and then nothing — not the command's output, not `CONTRIBUTING.md`, not `SKILL.md` — ever tells the Agent to remove the worktree, and nothing notices when it has not been. `.worktrees/` therefore keeps every merged task forever, and the local branch keeps pointing at its merge commit.

## Background / Confirmed Facts

Measured on `30562f7` (1.1.6) in this worktree:

- `grep -rn 'worktree remove\|worktree prune' hooks/` → no matches. No hook removes or prunes a worktree.
- `grep -c -i 'worktree' hooks/repository-check` → `0`. The readiness check says nothing about worktrees at all. The Todo entry's claim that it "reports stale worktrees only when their branch no longer exists" is **wrong** and is corrected here: it never reports them.
- `hooks/archive` ends by printing a three-line `Stage (commit on the current branch; …)` block. It does not mention the worktree, and it cannot: at archive time the branch has not been pushed or merged yet.
- `hooks/task:1211-1250` (`complete`) archives, prints whatever `hooks/archive` printed, and stops.
- `skills/taskflow/SKILL.md:299-305` (`### 7. Complete and archive`) is the single definition of the archive transaction. It states the move, the Todo update, and the verification, and stops there. `SKILL.md:129` states "One task, one working tree" for *creation* only.
- `CONTRIBUTING.md:18-31` states the worktree-isolation rule for creation only; "worktree" appears nowhere else.
- `.gitignore:7` ignores `.worktrees/`, so the trees never appear as changes — which is also why nothing ever complains about them.
- Live evidence in this repository: `git worktree list` shows `.worktrees/single-history-owner` and `.worktrees/todo-template-repair`, both fully merged into `origin/main` (`git merge-base --is-ancestor` → yes), both still present with their local branches.

The distinction that decides the design: **a worktree is removable when the work is on the base branch, not when the task is archived.** `complete` runs before the push and the merge, so the teardown instruction belongs at the end of the lifecycle but cannot be acted on immediately — which is exactly why it needs to be stated as a step with a condition, and why a check is needed to catch the ones that were skipped rather than a single line of advice.

## Requirements

1. `hooks/archive`'s trailing output names the worktree teardown as the step after the branch is merged, without implying it can be done now.
2. `SKILL.md`'s `### 7. Complete and archive` states the teardown and its condition. `CONTRIBUTING.md` states it where the isolation rule already lives, so the two documents that define task isolation also define its end.
3. `hooks/repository-check` reports every linked worktree whose branch is fully merged into the base branch and whose tree is clean, naming the command that removes it. It stays read-only and never removes anything.
4. The check is silent for the base checkout itself, for the worktree it is run from, and for any worktree whose branch carries work not yet in the base.
5. Smoke covers both directions: a merged-and-clean worktree is reported; an unmerged one, a dirty one, the base checkout, and the current worktree are not.

## Acceptance Criteria

- In a fixture repository with one merged, clean task worktree and one branch with an unmerged commit, `hooks/repository-check` names exactly the first, and its exit code is unchanged by the finding (read-only; it must not turn `STATUS: pass` into a pass-with-repairs that callers cannot distinguish).
- `hooks/archive`'s output, on a task completed inside a linked worktree, contains the teardown instruction; run on a task completed in the base checkout, it does not.
- `bash hooks/smoke-test` passes, and each new assertion is red under its own mutation.
- `bash hooks/repository-check .` on this repository reports the two real stale worktrees and still exits `0`.

## In Scope

- `hooks/archive` trailing output.
- `hooks/repository-check`'s stale-worktree section.
- `hooks/smoke-test` assertions for both.
- `skills/taskflow/SKILL.md` §7 and `CONTRIBUTING.md`'s isolation section.

## Out of Scope

- Removing any worktree automatically. The hooks do not touch Git state; `hooks/archive`'s existing comment states that boundary and it is unchanged.
- Removing the two worktrees currently in this repository. That is a bookkeeping action on the author's machine, taken after this lands, not part of the change.
- Deleting the branch. `git worktree remove` does not, and whether the branch should go is a separate question from whether the directory should.
- Any change to how worktrees are *created*.

## Risks / Deferred Items

- **The merged test can be wrong on a squash-merged branch.** `git merge-base --is-ancestor <branch> <base>` is true only for a branch whose commits are literally in the base. A squash or rebase merge leaves the branch's own commits outside, so the check under-reports. Under-reporting is the safe direction — a false positive would invite removing a worktree that still holds the only copy of a commit — and it matches the existing branch-report heuristic in `hooks/summarize-state`, which prefers silence to noise. Recorded as a limitation rather than solved.
- **A clean-worktree test needs untracked files counted as dirty.** A worktree with an untracked scratch file may hold work `git status` calls dirty anyway, so `git status --porcelain` empty is the right condition; this is stated so the implementation does not fall back to `git diff --quiet`.

## Open Questions

None blocking.
