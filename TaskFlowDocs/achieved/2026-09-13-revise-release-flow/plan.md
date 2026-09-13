# Plan — Revise release flow to support direct tag releases
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `RELEASE.md`
- `CONTRIBUTING.md`
- `.github/pull_request_template.md`

## Related Tasks

## Skills / Tools Used (Optional)

- TaskFlow — governance task traceability.
- shipping-and-launch — release gates and rollback.
- git-workflow-and-versioning — tags, branches, and release history.

## Preconditions

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-13 (explicit release-flow revision authorization)
- Approved version: v1
- Approved scope: PRD / Plan and `RELEASE.md` governance update

## Steps

### Step 1 — Implement and verify

- Goal: Change release governance to default direct tagging from verified main.
- Dependencies: merged main commit, passing checks, release-owner approval.
- Files: `RELEASE.md`, release task records.
- Implementation checklist:
  - [x] Make direct tagging from verified `main` the default release path.
  - [x] Retain Release PRs as an optional review/release-candidate path.
  - [x] Preserve explicit owner approval, validation, traceability, and rollback gates.
  - [x] Run repository, smoke, and diff checks.
- Acceptance: All PRD acceptance criteria pass.
- Verification: `bash hooks/repository-check .`; `bash hooks/smoke-test`; `git diff --check` — passed.
- Rollback: Revert the governance commit and restore the mandatory Release PR rule.
- Status: done

## Checkpoints

## Verification / Review

- Direct-tag prerequisites require merged base content, a clean exact commit, version/release-note validation, and explicit owner approval.
- Release PR wording is consistently optional throughout `RELEASE.md`.

## Change Log

- 2026-09-13 — User approved replacing mandatory Release PRs with a direct-tag default and optional PR path.

## Follow-ups

- Rebase the existing v1.0.4 release metadata onto the merged governance change, then publish by direct tag after final validation.

## Version History

- v1 — approved, implemented, and verified.
