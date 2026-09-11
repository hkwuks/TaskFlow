# Plan — Consolidate the packaged Skill layout
> Task version: v1
> Status: checking

No spec required — this is a bounded packaging cleanup with no runtime interface change.

## Reference Pointers

- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`
- `README.md`
- `README.zh-CN.md`

## Related Tasks

- Related: `TaskFlowDocs/2026-09-10-unblock-capability-invocation/`

## Skills / Tools Used (Optional)

- `taskflow` — purpose: intake and approved execution tracking; outcome: succeeded; incorporated: this v1 contract.
- `skill-creator` — purpose: validate canonical Skill package shape; outcome: succeeded; incorporated: `SKILL.md`, `agents/openai.yaml`, and `references/` belong together under the Skill directory.
- `git-workflow` — purpose: inspect migration history and scoped deletions; outcome: succeeded; incorporated: preserve only the manifest-consumed package and verify changed-file scope.
- `ponytail` — purpose: remove redundant synchronization; outcome: succeeded; incorporated: one canonical package instead of mirror tooling.

## Preconditions

- [x] Exact duplicate trees, manifests, references, and history inspected.
- [x] User authorized the stated move, deletions, and README repairs.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-10 20:05 +08:00
- Approved version: v1
- Approved scope: PRD / Plan and the explicitly listed consolidation.

## Steps

### Step 1 — Consolidate files and references
- Goal: Leave one complete packaged Skill.
- Dependencies: approval.
- Files: root Skill mirror, `skills/taskflow/`, README files, direct reference callers.
- Implementation checklist:
  - [x] Move Agent metadata into the packaged Skill.
  - [x] Remove the verified root duplicates.
  - [x] Repair links and structural checks.
- Acceptance: No duplicate Skill tree or broken direct reference remains.
- Verification: Path/reference scan and manifest resolution.
- Rollback: Restore deleted tracked files from the current Git revision and move metadata back.
- Status: done

### Step 2 — Verify and review
- Goal: Prove plugin packaging and existing behavior remain valid.
- Dependencies: Step 1.
- Files: changed files only.
- Implementation checklist:
  - [x] Run syntax and smoke checks.
  - [x] Run Skill metadata/link validation and `git diff --check`.
  - [x] Review deletion scope.
- Acceptance: All checks pass with only one Skill entrypoint.
- Verification: Recorded command results.
- Rollback: Revert this task's scoped changes.
- Status: done

## Verification / Review

- Both manifests resolve `./skills/` to exactly one entrypoint: `skills/taskflow/SKILL.md`.
- `skills/taskflow/` contains `SKILL.md`, `agents/openai.yaml`, and all three references; required metadata fields and `$taskflow` default prompt passed focused validation.
- README relative-link validation found zero broken links.
- Git Bash syntax checks and `hooks/smoke-test` passed: `ALL SMOKE PASSED`.
- `git diff --check` passed; stale-root-reference search found no obsolete target.
- The bundled `quick_validate.py` could not run because the available Python lacks its `PyYAML` dependency; no dependency was installed. Equivalent format/path checks passed locally.
- Deleted root items were confirmed exact duplicates or the old metadata location before removal and remain recoverable from Git.

## Change Log

- 2026-09-10 v1 — user approved removal of the stale root mirror and completion of `skills/taskflow/`.
- 2026-09-10 v1 implementation — consolidated the package and passed manifest, link, metadata, smoke, and diff checks; task is checking pending user acceptance and archive permission.

## Follow-ups

None.

## Version History

- v1 — approved and in progress.
