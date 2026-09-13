# Prepare TaskFlow v1.0.4 release
> Task version: v2
> Status: completed

## Goal

Prepare and document the TaskFlow v1.0.4 patch release from merged `origin/main`.

## Background / Confirmed Facts

- `origin/main` is at merged PR #13 and includes the completed optimization batch.
- Previous release is `v1.0.3`; repository history uses patch releases for compatible workflow and hook enhancements.
- Updated `RELEASE.md` allows direct tagging from an exact verified base commit with release-owner approval.

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
- Release metadata is synchronized to `main`; no tag/release is created before exact-commit verification and release-owner approval.

## In Scope

- Version metadata, release notes, and release TaskFlow records.

## Out of Scope

- Package-registry publication, signing, and provenance automation.

## Risks / Deferred Items

- A tag must never point to a commit that is not the verified `origin/main` release commit.

## Open Questions

## Version History

- v1 — superseded when repository release governance changed from mandatory PR to direct-tag default.
- v2 — approved direct-tag release from synchronized, verified `main`.
