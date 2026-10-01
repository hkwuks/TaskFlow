# Commit Todo, release, and TaskFlowDocs changes straight to main when the author
> Task version: v2
> Status: in_progress

## Goal

Let a change land by pushing the target branch directly when its author can push there, and reserve the pull request for when they cannot. TaskFlow's bookkeeping — a Todo entry, a task's status or archive, and a release — currently goes through the same branch-and-PR path as code, which costs a review round for content that has nothing to review.

## What v2 changes

v1 landed the rule, but the text does not carry its own scope. `CONTRIBUTING.md:37` states the landing question generally — "Landing is a separate question, and one fact decides it: **can the author push the target branch?**" — while the three covered classes appear under it as a list. A reader can therefore take the general sentence as the rule and the classes as examples of it, which would make the rule cover every change. The only sentence pulling the scope back is the closing one, and it does so by implication rather than by statement.

The scope itself was never in doubt: the Todo this task came from named Todo changes, releases, and TaskFlowDocs handling; R2 named the same three; and the approval round chose the narrow reading over extending it to authoring the task documents. What v2 changes is the text, so that it states that scope instead of leaving it to be inferred. The goal, the covered classes, and the permission criterion are unchanged.

## Background / Confirmed Facts

- `main` in this repository is not protected (`gh api repos/hkwuks/TaskFlow/branches/main/protection` → `404 Branch not protected`), and the session identity holds `admin` (its `permissions` include `push: true`). A direct push to `main` therefore works today.
- `CONTRIBUTING.md:18` states the rule this change qualifies: "Never implement in the base working tree. One task, one short-lived branch, created before the first edit — and before the first task document".
- `CONTRIBUTING.md:14` and `skills/taskflow/SKILL.md:14` already carve out one exception: a release runs from the base checkout with no branch, task, or PRD.
- `RELEASE.md:101-106` already pushes to `main` directly, atomically with the tag, and says why: the pin commit carries four mechanically derived literals, so "there is nothing in it to review".
- `skills/taskflow/SKILL.md:112-119` states the isolation rule and its reason: a task's documents are written in Phase 1, so without a worktree they land on whatever branch happens to be checked out, and the base checkout stops being startable for the next task.
- `skills/taskflow/references/runtime.md:134,139` — `hooks/task promote` refuses outside a task worktree; `intake` only warns. The refusal is a mechanism, not a convention.
- The release owner's instruction, 2026-10-01: Todo changes, releases, and TaskFlowDocs handling commit straight to `main` when the author has permission, and open a pull request only when they do not. Asked whether the policy should apply to itself, the answer was yes.

## Requirements

- R1. State one landing rule: when the author can push the target branch, the change is committed directly to it; when they cannot, a pull request is opened. The criterion is permission on the target branch, not the author's identity or the size of the diff.
- R2. Name what the rule covers — Todo entries, a task's status and archive, and release execution — and say plainly that it is about the landing path, not about isolation. The worktree rule is a different mechanism and is unchanged by this.
- R3. Say how "can push" is established, so the rule is decidable rather than aspirational: the target branch's protection and the author's role on the repository. Both are checkable facts; `gh api repos/<owner>/<repo> --jq .permissions` and `.../branches/<base>/protection` answer them.
- R4. Keep the review the direct path skips from being lost silently: a change that needs review is a change that keeps its pull request, so the rule must not read as "direct push by default for everything".
- R5. Do not weaken the existing release exception, which already lands this way; instead state the permission criterion it depends on.
- R6. The rule must state its own scope, so a reader can tell from the rule itself whether a code change, a hook change, or a Skill change is covered. A general sentence with a list of examples under it does not do that, and neither does a scope that only a trailing sentence implies.

## Acceptance Criteria

- A1. `CONTRIBUTING.md` carries the landing rule, its coverage, and the permission criterion, in the section that already states the branch rule — not as a second, competing rule elsewhere.
- A2. The amended text distinguishes the two mechanisms explicitly: a worktree isolates a task's work; the landing rule decides where its commits go. A reader cannot conclude that the worktree rule is abolished.
- A3. `RELEASE.md` names the permission criterion it already relies on, without changing what it does.
- A4. A reader looking for "how do I land this?" in `skills/taskflow/SKILL.md` is pointed at the rule rather than left with the PR-only text that is there now.
- A5. The rule is decidable from the text alone: it says which facts determine the path, and it names no identity-based shortcut ("the owner pushes, contributors PR").
- A6. `bash hooks/release-check .` still reports `pass`, and `git diff --check` is clean.
- A7. Reading only the `CONTRIBUTING.md` section that states the rule, a contributor can say how an ordinary code change lands — and the answer is a pull request — without consulting the PRD, the Plan, or any other document.

## In Scope

- `CONTRIBUTING.md` — the Working branches section.
- `RELEASE.md` — the release-scope narration around the direct push.
- `skills/taskflow/SKILL.md` — the PR paragraph and the isolation paragraph, so the two do not read as one rule.

## Out of Scope

- Removing or relaxing `hooks/task promote`'s refusal outside a task worktree, and any other hook change. Isolation behaviour stays exactly as it is; only the landing text changes.
- Changing branch protection, repository roles, or CI.
- The artifact-language question raised in the same message, tracked separately as `TF-20261001-51d9c8`.
- Any claim about repositories other than this one. The rule is stated as a general criterion; the measured facts are this repository's.

## Risks / Deferred Items

- **The Todo merge driver stops running.** `references/runtime.md:163` records that the per-entry driver only runs on local merges; a hosted pull-request merge degrades to a content conflict. Direct pushes to `main` change which of those paths is used, and parallel task branches are exactly the case the driver exists for. This is not resolvable in this change and is recorded as a follow-up rather than argued away.
- **Review disappears where it was doing something.** The rule's justification is that bookkeeping has nothing to review. That holds for an archive and a release pin; it holds less obviously for a Todo entry whose wording carries triage judgement. The mitigation is that R4 keeps "needs review" as a live reason to use a pull request.
- **A direct push cannot be reviewed after the fact as cheaply as a PR.** Reverting a bad commit on a shared branch is a second direct push. Accepted; the covered classes are small and reversible.

## Open Questions

- Whether `TaskFlowDocs` handling extends to authoring `prd.md`/`spec.md`/`plan.md`, or only to the bookkeeping around them. This PRD takes the narrow reading — bookkeeping only — because the wide reading would abolish the isolation rule by the back door and `promote` refuses outside a task worktree, so it would not work without a hook change that is out of scope here. Flagged for the approval round rather than assumed silently.
