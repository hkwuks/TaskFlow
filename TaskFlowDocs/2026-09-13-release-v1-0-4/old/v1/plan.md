# Plan — Prepare TaskFlow v1.0.4 release
> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers

- `RELEASE.md`
- `CONTRIBUTING.md`
- `CODE_STYLE.md`
- `.github/pull_request_template.md`
- `ROADMAP.md`

## Related Tasks

## Skills / Tools Used (Optional)

- TaskFlow — release task lifecycle.
- shipping-and-launch — release gate and rollback discipline.
- git-workflow-and-versioning — release branch and PR workflow.

## Preconditions

- Branch: `release/v1.0.4` from `origin/main` at `864b36f`.
- PR #13 is merged; Ubuntu/Windows CI passed.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-13 (explicit v1.0.4 authorization)
- Approved version: v1
- Approved scope: PRD / Spec / Plan and release PR preparation

## Steps

### Step 1 — Implement and verify

- Goal: Update release metadata and notes, then verify before PR.
- Dependencies: Python 3, GitHub Actions, merged `origin/main`.
- Files: manifests, README examples, `CHANGELOG.md`, release task docs.
- Implementation checklist:
  - [ ] Implement the approved change.
  - [ ] Run focused verification.
- Acceptance:
- Verification:
- Rollback:
- Status: in_progress

## Checkpoints

## Verification / Review

## Change Log

- 2026-09-13 — User approved v1.0.4; release preparation started from merged main.

## Follow-ups

## Version History

- v1 — planning.
