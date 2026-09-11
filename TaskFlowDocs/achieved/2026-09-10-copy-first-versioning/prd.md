# Copy-first Task versioning
> Task version: v1
> Status: completed

## Goal

Reduce Task-version transition token use by preserving existing task documents mechanically and limiting Agent writing to genuine semantic changes.

## Background / Confirmed Facts

- `hooks/version` currently moves changed core documents into `old/vN/`; the root copies disappear and must then be recreated.
- The user requires a copy-first flow: use Hook/script transformations where deterministic, and use the Agent only where semantic judgment is necessary.
- The existing transition already has one runnable smoke test and a cross-platform launcher.
- Applicable repository guidance: `README.md`, `README.zh-CN.md`, `hooks/README.md`, `references/runtime.md`, and `references/versioning-and-recovery.md`.

## Requirements

- Copy each materially changed core document into `old/vN/` while retaining the root document for editing.
- Do not copy unaffected core documents.
- Let the script update deterministic version-transition metadata, including the new Task version, `ready` state, and removal of superseded approval values.
- Leave semantic requirement/design changes and the human-readable change summary to the Agent.
- Validate all inputs before the first archive or root-document mutation.
- Preserve the rule that a new version requires user approval before implementation resumes.

## Acceptance Criteria

- After versioning a task with `prd.md` as the only changed document, `old/vN/prd.md` and the root `prd.md` both exist.
- The archived copy retains the old approved content; the root copy reports the new version and `ready` state without a valid old approval.
- An unchanged `spec.md` is not duplicated into `old/vN/` but has consistent current-version metadata when required by the transition contract.
- A failed preflight leaves both the root task and `old/vN/` unchanged.
- The focused smoke test and syntax checks pass.

## In Scope

- `hooks/version` and its focused regression test.
- Project documentation that currently describes move/rewrite behavior.
- Mirrored project Skill/reference files when the same maintained text exists in both public and packaged locations.

## Out of Scope

- User-level installed Skill or plugin-cache edits.
- Git-based delta/snapshot redesign.
- Automatic semantic rewriting of PRD, Spec, Plan, or `version.md` change summaries.
- Archiving or deleting any existing task directory.

## Risks / Deferred Items

- Shell edits must work under the existing Git Bash path on Windows.
- Exact approval-field shapes vary; the script must only change fields defined by TaskFlow's own artifact contract.
- More elaborate patch generation remains deferred until a measured need exists.

## Open Questions

None.

## Version History

- v1 — copy-first version transition contract, ready for approval.
