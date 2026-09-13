# Revise release flow to support direct tag releases
> Task version: v1
> Status: completed

## Goal

Revise release flow to support direct tag releases from verified `main` commits.

## Background / Confirmed Facts

- The current `RELEASE.md` requires a release branch and merged Release PR before tagging.
- User explicitly requested direct tag-based publishing when the release content is already on merged `main`.

## Requirements

- Make direct tag release the default for releases whose content is already merged to `main` and passes required checks.
- Keep a Release PR as an optional path when release-only documentation or extra review is needed.
- Require explicit release-owner approval before pushing tags or creating GitHub Releases.
- Define rollback and traceability expectations for both paths.

## Acceptance Criteria

- `RELEASE.md` no longer mandates a release branch/PR for every release.
- Direct-tag prerequisites, commands, and approval gate are explicit.
- Optional Release PR use and release-task recording remain documented.
- Existing release safety controls are preserved.

## In Scope

## Out of Scope

## Risks / Deferred Items

## Open Questions

## Version History

- v1 — approved and in progress.
