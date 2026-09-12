# Plan — Identify the current TaskFlow task before phase routing
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

## Related Tasks

## Skills / Tools Used (Optional)

## Preconditions

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-12 10:00 +08:00
- Approved version: v1
- Approved scope: PRD / Plan / implementation / verification

## Steps

### Step 1 — Implement and verify

- Goal: Select an explicit current task for automatic phase inference.
- Dependencies: approved v1.
- Files: `hooks/repository-docs-context`, `hooks/smoke-test`.
- Implementation checklist:
  - [x] Implement the approved change.
  - [x] Run focused verification.
- Acceptance: explicit task routes correctly; ambiguity remains unclassified.
- Verification: recorded below.
- Rollback: revert commit `1a4b366`.
- Status: done

## Verification / Review

- `bash -n hooks/repository-docs-context hooks/smoke-test` — passed.
- `bash hooks/smoke-test` — passed, including explicit task routing and ambiguity fallback.
- Commit: `1a4b366 fix: select the current task for auto routing`.

## Checkpoints

- [x] Explicit task routing tested.
- [x] Ambiguous fallback tested.

## Change Log

## Follow-ups

## Version History

- v1 — completed.
