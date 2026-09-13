# Pin stable marketplace installs to released revisions

- Task version: v1
- Status: completed

## Goal

Keep the TaskFlow marketplace catalog current on `main` while making stable Claude Code and Codex installs resolve to an immutable released revision.

## Requirements

- Pin the shared marketplace plugin source to tag `v1.0.4` and commit `2691453a40955a6f7353c3326dd44c58638f6608`.
- Keep local-directory installation available for development.
- Document the same tag-plus-SHA publication rule for future releases.
- Do not move or recreate the published `v1.0.4` tag and do not bump the plugin version for this catalog-only correction.

## Acceptance criteria

- Claude Code and Codex can parse the shared marketplace entry and resolve the repository-root plugin source.
- Remote stable installs are insulated from later `main` changes.
- English and Chinese installation guidance distinguish stable remote installs from local development installs.
- Release guidance requires updating the catalog pin after creating a release tag.

## Scope

In scope: marketplace metadata, release/install documentation, and task records.

Out of scope: new plugin functionality, moving the existing tag, publishing `v1.0.5`, or changing local development behavior.

## Version history

- v1 — approved fixed-version marketplace distribution.
