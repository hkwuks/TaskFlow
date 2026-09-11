# Reduce TaskFlow workflow token cost
> Task version: v1
> Status: completed

## Goal

Reduce the tokens an Agent spends running TaskFlow — across skill activation, task-document churn, and retrieval — while preserving traceability, approval gates, and recoverability. This task applies the four selected levers only; `old/vN/` snapshots stay as the recovery mechanism for users who keep design documents out of Git.

## Background / Confirmed Facts

- The skill bundle (`SKILL.md` + two references) is ~9.3k tokens per activation; the versioning rule and archive transaction are each stated in all three files.
- Version churn is high: the largest achieved task ran 5 version bumps and 6 re-approvals within ~16 hours, several bumps for wording-only refinements (v3→v4→v5 carry 82–85% of unchanged text forward).
- Each version bump rewrites all three core documents and archives full copies of the prior set into `old/vN/` (one achieved task holds ~14k tokens of snapshot copies vs ~5k current).
- Reopening/retrieving an achieved task re-reads its current docs plus `old/`.
- TaskFlow lifecycle is duplicated in README (EN and zh-CN), which the repository catalog lists as `repository-guidance`; README phrasing lags or repeats skill wording.
- Git tracks `TaskFlowDocs/`. The selected levers must not assume that: lever 3 (git-only `old/`) is explicitly out of scope because some users keep design documents out of Git.

## Requirements

1. Archive-transaction wording exists in exactly one file: `SKILL.md`. `artifacts.md` and `versioning-and-recovery.md` point to it instead of restating it.
2. The version-trigger test is tightened so that an "implementation path/approach change" or a wording-only clarification is a work revision (Plan change-log entry, no new Task version) unless it changes an approved goal, requirement, acceptance criterion, scope, or contract.
3. Versioning rules distinguish Task versions (`prd.md`/`spec.md` only) from Plan-internal revisions (Plan change log). A new Task version does not require regenerating a Plan whose steps, approval, and verification are unaffected.
4. A version bump archives only the changed core documents plus `version.md`, and snapshots only when the design document is not recoverable from an existing archive. Do not copy a Plan into `old/` when its content is unchanged.
5. Retrieval is staged: check `version.md` summaries and current `plan.md` before reading full archived document sets.
6. README (EN and zh-CN) states the workflow in a version-stable summary; the operational details stay in the skill.
7. No change forces design documents into Git. `old/vN/` remains a valid recovery store for users who do not commit design files.

## Acceptance Criteria

- Each of the duplicated procedure statements exists in exactly one of `SKILL.md`, `artifacts.md`, `versioning-and-recovery.md` (grep-checkable).
- The version-trigger wording no longer treats an implementation-path wording change as a Task-version trigger by default.
- `plan.md` change-log guidance permits work revisions without a new Task version, and a version bump does not require rewriting an unaffected Plan.
- The archive rule reduces `old/` copies to changed documents plus `version.md` unless a recoverability check requires a full snapshot.
- The retrieval step is staged before full archived reads.
- Both README files describe the workflow without restating full operational rules.
- No git-only requirement is introduced.

## In Scope

- Edits to `taskflow/SKILL.md`, `taskflow/references/artifacts.md`, `taskflow/references/versioning-and-recovery.md`, and `README.md` / `README.zh-CN.md` governing these workflow behaviors.
- Mirroring the edits to the installed skill copy at `~/.claude/skills/taskflow/` (symlinked from the LLMConfig store) so the running skill matches the repository.

## Out of Scope

- Reducing the absolute size of `SKILL.md` prose or templates (a separate lever; the skill itself is the source-of-truth carrier here).
- Changing `old/vN/` to git-only or removing file-mode archival (users may keep design docs out of Git).
- Any change to artifact locations, Todo intake, approval semantics, or the phase state machine.

## Risks / Deferred Items

- Rule-shrinking may blur a version boundary; mitigated by the tightened trigger test and by keeping contract changes on the Task-version path.
- If the user later wants git-only archives, that is a separate change event.

## Open Questions

- None blocking.

## Version History

- v1: Proposed four-lever workflow change (version triggers, archive granularity, plan revisions, retrieval staging); git-only archival excluded.
