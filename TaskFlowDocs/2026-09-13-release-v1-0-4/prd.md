# Prepare TaskFlow v1.0.4 release
> Task version: v1
> Status: in_progress

## Goal

Prepare and document the TaskFlow v1.0.4 patch release from merged `origin/main`.

## Background / Confirmed Facts

- `origin/main` is at merged PR #13 and includes the completed optimization batch.
- Previous release is `v1.0.3`; repository history uses patch releases for compatible workflow and hook enhancements.
- `RELEASE.md` requires a release PR before tagging or creating a GitHub Release.

## Requirements

- Update Claude manifest to `1.0.4`.
- Update Codex manifest to `1.0.4+codex.20260913`.
- Update user-facing installed-version examples.
- Add release notes with date, changes, compatibility impact, verification, and known limitations.

## Acceptance Criteria

- Both manifests contain the intended versions and valid JSON.
- README examples show `1.0.4`.
- Release notes accurately summarize merged changes and checks.
- Required smoke, repository, Skill, diff, and hosted CI checks are recorded.
- Release PR is opened; no tag/release is created before post-merge approval.

## In Scope

- Version metadata, release notes, and release TaskFlow records.

## Out of Scope

- Tagging, GitHub Release creation, package publishing, signing, and provenance automation before release PR merge and explicit owner approval.

## Risks / Deferred Items

- A GitHub Release cannot be created until this release PR is merged and the release owner confirms the final commit.

## Open Questions

## Version History

- v1 — approved and in progress.
