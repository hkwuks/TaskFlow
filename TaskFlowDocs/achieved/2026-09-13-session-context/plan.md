# Plan — Reduce SessionStart context output to the active task by default
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `CONTRIBUTING.md`
- `CODE_STYLE.md`
- `skills/taskflow/references/runtime.md`

## Related Tasks

## Skills / Tools Used (Optional)

- TaskFlow — lifecycle and verification record.
- context-engineering — minimize injected context while retaining actionable state.
- git-workflow-and-versioning — isolated worktree and atomic commit.

## Preconditions

- Dedicated worktree branch: `perf/session-context`.
- Integration baseline: `b8e3ff1`.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-11 (batch authorization)
- Approved version: v1
- Approved scope: PRD / Plan and implementation of the recorded optimization batch

## Steps

### Step 1 — Implement and verify

- Goal: Make SessionStart context current-task-first and verbose only on request.
- Dependencies: Existing TaskFlow Todo and Plan formats.
- Files: `hooks/summarize-state`, focused smoke tests, runtime documentation.
- Implementation checklist:
  - [x] Select one explicit or uniquely active task by default.
  - [x] Report invalid IDs and ambiguous multi-task state without guessing.
  - [x] Add `TASKFLOW_VERBOSE=1` full-inventory escape hatch.
  - [x] Add default/verbose/explicit-ID regression coverage.
  - [x] Run syntax, diff, and full smoke checks.
- Acceptance: All PRD acceptance criteria passed.
- Verification: `bash -n hooks/summarize-state hooks/smoke-test`; `git diff --check`; `bash hooks/smoke-test` — all passed.
- Rollback: Revert `8b128b5`.
- Status: done

## Checkpoints

## Verification / Review

- Default output remains compact and preserves repository-document routing.
- Verbose mode retains full Todo/active-task inventory.
- Invalid explicit IDs and ambiguous active-task sets produce safe diagnostics.

## Change Log

- 2026-09-13 — Promoted the context-reduction item and started isolated implementation.
- 2026-09-13 — Completed implementation and smoke verification.

## Follow-ups

## Version History

- v1 — approved, implemented, and verified.
