# Plan — Index-driven repository document routing
> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `skills/taskflow/references/runtime.md`

## Related Tasks

- Related: `TaskFlowDocs/2026-09-10-repository-governed-development/`

## Skills / Tools Used (Optional)

- `taskflow` — Todo-first task creation and approval boundary; incorporated: separate approved v1 task.
- `using-agent-skills` — selected spec, implementation, test, and Git workflow.
- `ponytail` — kept the design to one helper composed by the existing SessionStart hook.

## Preconditions

- [x] Existing index, hook flow, Skill rules, and untracked user files inspected.
- [x] User confirmed index authority, deterministic maintenance, and compact phase-aware injection.
- [x] Source policies remain authoritative and PR/release actions retain explicit approval.
- [x] Dedicated branch `docs/index-hook-routing` created after Git metadata write approval.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-11 13:39 +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan and bounded hook implementation

## Steps

### Step 1 — Implement index synchronization and routing

- Goal: Maintain the routing record and emit compact applicable paths.
- Dependencies: approved v1 design.
- Files: `hooks/repository-docs-context`, `TaskFlowDocs/repository-docs/index.md`.
- Implementation checklist:
  - [x] Synchronize recognized source and personal supplement metadata atomically.
  - [x] Route by explicit phase or active task state.
- Acceptance: repeatable sync and concise routing output.
- Verification: focused fixture in `bash hooks/smoke-test`.
- Rollback: remove the helper and restore the prior index.
- Status: done

### Step 2 — Integrate and document

- Goal: Use the record from SessionStart and align workflow guidance.
- Dependencies: Step 1.
- Files: `hooks/session-start`, `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, hook docs.
- Implementation checklist:
  - [x] Compose repository routing with the existing task summary.
  - [x] Replace derived-navigation wording with index-first routing and source-authority rules.
- Acceptance: hook and manual workflow have the same authority boundary.
- Verification: focused text review and SessionStart JSON smoke check.
- Rollback: revert integration/documentation changes.
- Status: done

### Step 3 — Verify and prepare Git handoff

- Goal: Prove behavior and leave a scoped reviewable diff.
- Dependencies: Steps 1–2.
- Files: smoke tests and task Plan.
- Implementation checklist:
  - [x] Run hook smoke tests and Skill validation.
  - [x] Run shell syntax and whitespace checks.
  - [x] Confirm user-owned untracked files remain untouched.
- Acceptance: checks pass and diff is scoped.
- Verification: recorded commands under Verification / Review.
- Rollback: revert only task-specific fixes.
- Status: done

## Checkpoints

- [x] Index is a record, not a copy of policies.
- [x] Hook writes only deterministic index metadata.
- [x] No automatic governance creation, approval, or Git/hosting mutation.

## Verification / Review

- `bash hooks/smoke-test` — passed, including index sync, phase routing, candidate review, and idempotency.
- `python3 .../quick_validate.py skills/taskflow` — passed.
- `bash -n hooks/repository-docs-context hooks/session-start hooks/smoke-test` — passed.
- `git diff --check` — passed.
- Simulated Claude SessionStart `startup` with `TASKFLOW_PHASE=pr` — valid JSON; routed `LICENSE`, `CONTRIBUTING.md`, and `.github/pull_request_template.md`.
- Simulated Claude SessionStart `resume` with `TASKFLOW_PHASE=release` — valid JSON; routed available release-phase sources and reported missing sources, including `RELEASE.md` because PR #4 is not merged into this branch's `main` base.
- Index synchronization idempotency — first SessionStart corrected the stale `RELEASE.md` existence record; the next run preserved the same SHA-256 hash.
- Git branch preparation — initial sandbox attempt was blocked by read-only `.git`; approved elevated retry created `docs/index-hook-routing` without moving or discarding working-tree changes.
- Scope check — existing user-owned `TaskFlowDocs/2026-09-10-token-saving-lifecycle-scripts/` remains untracked and untouched.

## Change Log

- 2026-09-11 Task v1 — user approved index-first routing, automatic bounded index maintenance, and SessionStart context injection.

## Follow-ups

- Create and push a dedicated branch when `.git` write access is restored.

## Version History

- v1 — approved implementation contract.
