# Archived Version v1 — Personal supplements are local-only (statement-only)
> Task: 2026-09-14-personal-docs-git-boundary
> Version: v1
> Status: superseded
> Created: 2026-09-14
> Archived: 2026-09-15 00:02 +0800
> Superseded by: v2
> Archive mode: file
> Restore root: any new temporary directory

## Change Summary

v1 planned a statement-only change: keep `TaskFlowDocs/repository-docs/personal/`, state in the Skill that personal supplements are local-only, ignore that directory in Git, and untrack the placeholder `README.md`. The plan was approved but never implemented.

v2 replaces the location as well: the `personal/` subdirectory is dropped, personal rules are plain `*.md` files directly beside `TaskFlowDocs/repository-docs/index.md`, the hook catalogs them as `personal-rule` with status `local-only`, and it injects them on a dedicated route line instead of merging them into `Read authoritative sources:`. The placeholder `README.md` is removed with the directory rather than untracked, the requirement that personal paths stay out of Git is kept, and the index sync must drop a removed personal row so the sync stays idempotent.

## Archived Materials

- `prd.md` — the v1 statement-only PRD.

## Restore

Read the archived v1 `prd.md` from a new temporary restore root only. Never restore by overwriting the current task directory; v2 supersedes it and the approved v2 documents are authoritative.

## Read This Version When

Inspecting why the original scope was statement-only, or when comparing the two candidate locations for personal rules.
