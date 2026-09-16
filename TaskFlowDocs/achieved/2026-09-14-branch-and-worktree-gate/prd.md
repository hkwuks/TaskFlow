# Require a working branch or dedicated worktree before implementation starts
> Task version: v1
> Status: completed

## Goal

Make work isolation an explicit, repository-stated rule: implementation starts on a short-lived branch off the intended base, parallel tasks get separate worktrees, and the base working tree is never the place implementation happens.

## Background / Confirmed Facts

- `CONTRIBUTING.md:5` already says "Work from a short-lived feature, fix, docs, or chore branch based on the intended base branch", and `CONTRIBUTING.md:16` names the branch prefixes. Both are one-line assertions with no operational detail.
- Neither `CONTRIBUTING.md`, `README.md`, `skills/taskflow/SKILL.md`, nor any TaskFlow reference mentions `git worktree`; the plugin's own recent tasks were implemented directly in the `main` working tree.
- `hooks/repository-check` prints the current branch and reports `Base: ambiguous` when no upstream is set, so a branch check is already observable but not enforced or explained.
- TaskFlow's phase routing does not cover branch/worktree setup: `SKILL.md:81` routes "commits/PRs" to contributing/PR-template/CODEOWNERS, and `hooks/repository-docs-context` maps `CONTRIBUTING.md` to `code,commit,pr,release`. There is no `design` route that would surface contribution rules before implementation begins.
- GitHub's own convention is that contribution rules live in `CONTRIBUTING.md` at the repository root (or `.github/`, or `docs/`), with `.github/` taking precedence. Branching policy is ordinary contribution guidance; GitHub has no separate conventional all-caps file for it.
- Upstream practice confirms the split: fetching the contribution guides of kubernetes, rust, git, pytorch, vscode, go, node, and angular, "create a branch" appears as standard guidance (angular gives a full `git checkout -b my-fix-branch main` example), while `git worktree` appears zero times. Worktree isolation is therefore Agent-side execution detail, not contributor-facing convention.
- The user's rule (2026-09-14): the workflow must start on a branch, and parallel tasks must be separated with `git worktree`. The user then chose the placement: the branch rule goes to `CONTRIBUTING.md`, the worktree rule to `SKILL.md`.

## Requirements

- R1. `CONTRIBUTING.md` states the contributor-facing isolation rule: never implement in the base working tree, one TaskFlow task maps to one short-lived branch created before the first edit, and the branch name uses the existing `<type>/<description>` prefixes.
- R2. `CONTRIBUTING.md` gives one runnable branch-creation command and points at the existing observability (`git branch --show-current`, `bash hooks/repository-check .`) instead of inventing a second check.
- R3. `CONTRIBUTING.md` does not document `git worktree`: worktree isolation is Agent execution detail, and upstream contribution guides do not carry it.
- R4. `skills/taskflow/SKILL.md` Phase 5 (Build) states the worktree rule: read the repository's branch guidance before the first edit, branch as `<type>/<description>` off the intended base when the repository states no rule, and give each concurrent task its own working tree rather than switching branches in a shared checkout.
- R5. `TaskFlowDocs/repository-docs/index.md` routes `CONTRIBUTING.md` to the `design` phase as well, so contribution rules — including this one — are surfaced before implementation rather than only at commit time.
- R6. `hooks/repository-docs-context` lists `CONTRIBUTING.md` with the matching phase set, and the routing regression in `hooks/smoke-test` follows.
- R7. No hook enforces the rule automatically; branch/worktree choice stays an Agent and user decision, and `hooks/repository-check` behavior is unchanged.
- R8. `README.md` and `README.zh-CN.md` state the same isolation rule in one sentence each, keeping the two READMEs behaviorally aligned per `CODE_STYLE.md`.

## Acceptance Criteria

- A1. `CONTRIBUTING.md` contains an explicit branch rule covering the base tree, one-task-one-branch, naming, and the pre-edit check; it contains no `git worktree` guidance.
- A2. The commands given in `CONTRIBUTING.md` are runnable as written for this repository (no placeholder remote or path beyond the documented conventions).
- A3. `skills/taskflow/SKILL.md` Phase 5 states the worktree rule for concurrent tasks and defers branch naming to the repository guidance.
- A4. `TaskFlowDocs/repository-docs/index.md` and `hooks/repository-docs-context` both list `CONTRIBUTING.md` with `design` in its phases, and a regenerated index matches.
- A5. `TASKFLOW_PHASE=design bash hooks/repository-docs-context` lists `CONTRIBUTING.md` among the authoritative sources.
- A6. `README.md` and `README.zh-CN.md` each state the isolation rule.
- A7. `bash hooks/smoke-test` passes, `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow` passes, and `git diff --check` is clean.

## In Scope

- `CONTRIBUTING.md`, `skills/taskflow/SKILL.md` (Phase 5), `TaskFlowDocs/repository-docs/index.md`, `hooks/repository-docs-context`, `hooks/smoke-test`, `README.md`, `README.zh-CN.md`, and the Todo entry for this task.

## Out of Scope

- Any hook that blocks, warns on, or auto-creates a branch or worktree.
- Changing `hooks/repository-check` output, exit codes, or its `needs-user-input` status.
- Per-task branch naming enforcement in `hooks/task` or in the TaskFlow lifecycle commands.
- Documenting `git worktree` in `CONTRIBUTING.md`.
- Editing `CODE_STYLE.md`, `RELEASE.md`, or CI workflows.

## Risks / Deferred Items

- A rule in `CONTRIBUTING.md` is guidance, not enforcement; a session that ignores it still succeeds. Deferred: enforcement is a lifecycle change and needs its own approved task.
- Adding `design` to `CONTRIBUTING.md`'s phases widens the routed-document set for every design-phase task; the check is cheap, but the index row is shared with `code`, `commit`, `pr`, and `release`.
- Worktree cleanup after a merge is manual; the Skill states the rule rather than relying on a tool.

## Open Questions

None — placement (repository guidance plus routing record) was decided by the user on 2026-09-14.

## Version History

- v1 — planning.
