# Consolidate the packaged Skill layout
> Task version: v1
> Status: completed

## Goal

Remove the duplicated root-level Skill mirror and make `skills/taskflow/` the single complete Skill package loaded by both plugin manifests.

## Background / Confirmed Facts

- Both plugin manifests point their Skill source at `./skills/`.
- Root `SKILL.md` and `references/` predate the plugin layout; the later `skills/taskflow/` copies are byte-identical mirrors.
- `agents/openai.yaml` exists only at the root, leaving the packaged Skill incomplete.
- README badge links still point to the obsolete `taskflow/` path.
- The user explicitly authorized the proposed move, deletion, and link repair.

## Requirements

- Keep exactly one Skill at `skills/taskflow/`.
- Move `agents/openai.yaml` to `skills/taskflow/agents/openai.yaml`.
- Delete root `SKILL.md`, `agents/`, and `references/` after verifying their exact contents.
- Update documentation and tests to reference the single packaged Skill.
- Do not change user-level configuration, installed caches, or unrelated files.

## Acceptance Criteria

- Both plugin manifests resolve `skills/taskflow/SKILL.md` and no root Skill mirror remains.
- The packaged Skill contains its metadata and references.
- README links resolve to existing files.
- Hook smoke tests and `git diff --check` pass.

## In Scope

- Root duplicate Skill files, packaged Skill metadata placement, direct references, and structural regression assertions.

## Out of Scope

- Plugin installation/update, version bump, commit, push, and unrelated task archival.

## Risks / Deferred Items

- Removing a legacy direct-install layout is intentional; the documented distribution mechanism is the plugin manifests.

## Open Questions

None.

## Version History

- v1 — approved consolidation scope.
