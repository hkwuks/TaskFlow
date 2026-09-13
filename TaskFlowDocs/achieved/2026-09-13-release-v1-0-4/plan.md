# Plan — Prepare TaskFlow v1.0.4 release
> Task version: v2
> Status: completed

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
- git-workflow-and-versioning — exact-commit synchronization and annotated tag workflow.

## Preconditions

- Preparation branch: `release/v1.0.4`, synchronized with `origin/main` after PR #14.
- PR #14 is merged; Ubuntu/Windows CI passed.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-13 ("OK, sync and publish")
- Approved version: v2
- Approved scope: PRD / Spec / Plan, synchronization to main, annotated `v1.0.4` tag, and GitHub Release

## Steps

### Step 1 — Implement and verify

- Goal: Update release metadata/notes, synchronize the exact release commit to main, then publish by tag.
- Dependencies: Python 3, GitHub Actions, merged `origin/main`.
- Files: manifests, README examples, `CHANGELOG.md`, release task docs.
- Implementation checklist:
  - [x] Update both manifests, README examples, and release notes.
  - [x] Synchronize the new direct-tag governance from main.
  - [x] Run repository, smoke, Skill, diff, and version checks.
  - [x] Synchronize the final release commit to `origin/main`.
  - [x] Create/push annotated tag and GitHub Release.
- Acceptance: Exact `origin/main` commit has the approved versions and notes; tag and GitHub Release point to it.
- Verification: Full release checklist passed before final release record; rerun after synchronization.
- Rollback: Do not move/delete a published tag; stop distribution and use a corrective patch release.
- Status: done

## Checkpoints

## Verification / Review

- Release commit `2691453a40955a6f7353c3326dd44c58638f6608` matched `origin/main` before tagging.
- `bash hooks/repository-check .`, `bash hooks/smoke-test`, Skill validation, `git diff --check`, and manifest assertions passed.
- Annotated tag `v1.0.4` was pushed successfully.
- GitHub Release: `https://github.com/hkwuks/TaskFlow/releases/tag/v1.0.4`.

## Change Log

- 2026-09-13 — User approved v1.0.4; release preparation started from merged main.
- 2026-09-13 — v2 approved after direct-tag release governance replaced the mandatory Release PR path.

## Follow-ups

- None.

## Version History

- v1 — superseded mandatory-PR flow.
- v2 — approved direct-tag flow.
