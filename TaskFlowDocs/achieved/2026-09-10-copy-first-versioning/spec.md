# Spec — Copy-first Task versioning
> Task version: v1

## Objective and Success Criteria

Make `hooks/version` preserve superseded content with filesystem copies and prepare retained root documents mechanically for the next approval cycle.

## Architecture Boundaries and Responsibilities

- `hooks/version`: preflight, copy selected changed documents, create the deterministic `version.md` shell, update root version/state/approval metadata, and verify consistency.
- Agent: choose changed documents, edit new semantic content, replace the placeholder change summary, and request approval.
- User: approve the new Task version.

## Project Structure / Affected Files

- `hooks/version`
- `hooks/smoke-test`
- `hooks/README.md`
- `references/versioning-and-recovery.md`
- `skills/taskflow/references/versioning-and-recovery.md`
- Contract text in `SKILL.md` / `skills/taskflow/SKILL.md` only if needed for consistency.

## Interfaces, Data Flow, and Contracts

1. The Agent invokes `hooks/version <task-id> <new-v> [root] [file...]` with only materially changed core filenames.
2. The script validates task paths, required files, version progression, selected filenames, archive destination, and parseable metadata.
3. The script creates `old/<old-v>/`, writes `version.md`, and copies selected root documents there.
4. The script updates retained root core documents to the new version, sets the task state to `ready`, and invalidates the old Approval record deterministically.
5. The Agent edits only new semantic differences and the change summary, then obtains approval.

## Invariants and Compatibility

- The command interface remains unchanged.
- Only `prd.md`, `spec.md`, and `plan.md` are accepted as selected core documents.
- Existing root documents are never removed during versioning.
- Unselected documents are never placed in `old/vN/`.
- No compatibility fallback or second implementation path is added.

## Validation and Error Semantics

- All preflight failures exit nonzero before filesystem mutation.
- Existing archive destinations are rejected rather than overwritten.
- Post-transition checks require archived selected files, retained root files, consistent new versions, `ready` state, and no active old approval.

## Code and Test Constraints

- Reuse the existing Bash script and smoke test; add no dependency.
- Use `cp` and the smallest deterministic text transformations that satisfy the artifact format.
- Extend the existing version smoke section to assert preservation, archive content, new state, and approval invalidation.

## Design Decisions and Alternatives

- Chosen: copy selected old documents and edit retained roots.
- Rejected: move then have the Agent rewrite full documents, because it consumes tokens and risks accidental drift.
- Rejected: copy every core document, because unchanged content has no semantic archive value.
- Deferred: generated semantic diffs; the Agent still owns meaning.

## Open Questions

None.
