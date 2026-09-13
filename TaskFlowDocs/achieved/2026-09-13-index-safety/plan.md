# Plan — Validate repository-document index paths and protect concurrent writes
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

- TaskFlow — lifecycle records and archive checks.
- security-and-hardening — path trust-boundary validation.
- git-workflow-and-versioning — isolated worktree and atomic commit.

## Preconditions

- Dedicated worktree branch: `fix/index-safety`.
- Integration baseline: `6412cbd`.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-11 (batch authorization)
- Approved version: v1
- Approved scope: PRD / Plan and implementation of the recorded optimization batch

## Steps

### Step 1 — Implement and verify

- Goal: Validate catalog paths at the repository boundary and serialize index refreshes.
- Dependencies: Python 3 and filesystem atomic rename support.
- Files: `hooks/repository-docs-context`, focused smoke tests.
- Implementation checklist:
  - [x] Reject absolute, drive-qualified, traversal, and repository-escaping paths.
  - [x] Serialize index writes with a repository-local lock while retaining atomic replacement.
  - [x] Preserve the old index when a catalog row is malformed.
  - [x] Run focused and complete verification.
- Acceptance: All PRD acceptance criteria passed.
- Verification: `bash -n hooks/repository-docs-context hooks/smoke-test`; `git diff --check`; `bash hooks/smoke-test` — all passed.
- Rollback: Revert `746b29a`.
- Status: done

## Checkpoints

## Verification / Review

- Unsafe `../` records are rejected before any write.
- Malformed table rows fail without changing the existing index hash.
- Existing lock directories produce an explicit busy failure; temporary-file replacement remains atomic.
- Full smoke suite passed on 2026-09-13.

## Change Log

- 2026-09-13 — Promoted the next optimization item and started isolated implementation.
- 2026-09-13 — Review added malformed-row preservation coverage before completion.

## Follow-ups

- None.

## Version History

- v1 — approved, implemented, and verified.
