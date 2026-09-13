# Plan — Model optional repository documents and consume SessionStart event input
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `CONTRIBUTING.md`
- `.github/pull_request_template.md`
- `skills/taskflow/references/runtime.md`

## Related Tasks

## Skills / Tools Used (Optional)

- TaskFlow — lifecycle record.
- source-driven-development — verify hook event input contract.
- git-workflow-and-versioning — isolated worktree and atomic commit.

## Preconditions

- Dedicated worktree branch: `feat/event-aware-docs`.
- Integration baseline: `996a1c7`.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-11 (batch authorization)
- Approved version: v1
- Approved scope: PRD / Plan and implementation of the recorded optimization batch

## Steps

### Step 1 — Implement and verify

- Goal: Consume SessionStart event data and distinguish optional repository documents.
- Dependencies: Python 3 and the host SessionStart JSON contract.
- Files: `hooks/session-start`, `hooks/repository-docs-context`, smoke tests, runtime docs.
- Implementation checklist:
  - [x] Parse and validate SessionStart stdin JSON.
  - [x] Route using event `cwd` and retain `session_id` safely.
  - [x] Ignore non-SessionStart events without output or index mutation.
  - [x] Mark absent optional repository documents as `optional`.
  - [x] Run syntax, diff, and full smoke checks.
- Acceptance: All PRD acceptance criteria passed locally.
- Verification: `bash -n hooks/session-start hooks/repository-docs-context hooks/smoke-test`; `git diff --check`; `bash hooks/smoke-test` — passed.
- Rollback: Revert `f3b68c1`.
- Status: done

## Checkpoints

## Verification / Review

- Valid SessionStart event cwd overrides an unrelated environment root.
- Non-SessionStart events emit nothing and do not create an index.
- Malformed JSON exits non-zero with an actionable diagnostic.
- Missing CODEOWNERS is cataloged as optional and omitted from blocking missing routes.
- GitHub Actions run `34758138507` passed: Ubuntu in 6 seconds and Windows in 24 seconds.

## Change Log

- 2026-09-13 — Promoted the final optimization item and started isolated implementation.
- 2026-09-13 — Completed event filtering, optional status modeling, review, and local verification.

## Follow-ups

## Version History

- v1 — approved, implemented, and verified on hosted Linux and Windows runners.
