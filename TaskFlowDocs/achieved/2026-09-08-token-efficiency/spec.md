# Spec — Reduce TaskFlow workflow token cost
> Task version: v1
> Status: completed

## Objective and Success Criteria

Each operational rule is stated once and referenced elsewhere; version bumps stop regenerating whole document sets for wording changes; Plan revisions do not force new Task versions; archived `old/` keeps only what is needed for recovery; retrieval is staged. No rule forces design documents into Git.

## Architecture Boundaries and Responsibilities

- `taskflow/SKILL.md` — single source for: archive transaction procedure, version-trigger test, retrieval staging, and revision-vs-version decision.
- `taskflow/references/artifacts.md` — templates + routing only; references SKILL.md for lifecycle rules instead of restating them.
- `taskflow/references/versioning-and-recovery.md` — how to archive/recover a version; references SKILL.md for the transaction and trigger.
- `README.md` / `README.zh-CN.md` — stable workflow summary; operational detail lives in the skill.
- Installed skill copy (`~/.claude/skills/taskflow/`) mirrors the repository copies; both are updated together.

## Project Structure / Affected Files

- `taskflow/SKILL.md`
- `taskflow/references/artifacts.md`
- `taskflow/references/versioning-and-recovery.md`
- `README.md`
- `README.zh-CN.md`
- Installed mirror of the three skill files.

## Interfaces, Data Flow, and Contracts

- Ownership table (document → owns which rules) is the contract that de-duplication must satisfy.
- The version-trigger decision procedure (inputs: change type → output: revision vs new version) is the contract for when a full re-approval cycle runs.
- The archive checklist defines what goes into a new `old/vN/`: `version.md` always; each core document whose content is materially changed; snapshots only when the source document is not recoverable from an existing archive.

## Invariants and Compatibility

- A change to an approved goal, requirement, acceptance criterion, scope, or contract always bumps the Task version and returns to approval.
- `old/vN/` remains a valid non-Git recovery store.
- Task directories, Todo intake, phase state machine, and approval semantics are unchanged.

## Validation and Error Semantics

- A document that is read after a session break must still show a consistent version/status even when `plan.md` alone carries recent work-revision notes.
- If a "work revision" is later judged material, the operator can still archive the current version before the next change; nothing is lost because the current docs remain the baseline.

## Code and Test Constraints

- No code changes. Verification is textual: grep for duplicated procedure sentences, and review each changed document.

## Design Decisions and Alternatives

- Rejected: splitting lifecycle rules into a new reference file (adds a file and a load cost).
- Rejected: removing `versioning-and-recovery.md` (it carries the archive mechanics the skill should not carry).
- Chosen: SKILL.md as the single rule owner; the two references and README defer.

## Open Questions

- None.
