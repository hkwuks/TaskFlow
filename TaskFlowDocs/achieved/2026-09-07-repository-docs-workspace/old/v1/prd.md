# Repository documentation workspace
> Task version: v1
> Status: in_progress

## Goal

Provide one TaskFlowDocs workspace for existing repository documents and repository standards, using relative symbolic links when safe and a portable index when symbolic links are unavailable.

## Background / Confirmed Facts

- The repository contains `README.md` and `README.zh-CN.md`; no CONTRIBUTING, code-style, releasing, roadmap, or similar document was found.
- Git reports `core.symlinks=false`, so checked-in symbolic links are not portable in this workspace.
- The user approved `TaskFlowDocs/repository-docs/` as the unified location, moving standards into it, index fallback, and no automatic creation of missing source documents.

## Requirements

1. Move repository standards to `TaskFlowDocs/repository-docs/standards/`.
2. Add `repository-docs/index.md` as the unified document environment and cross-platform fallback.
3. Discover existing README, contributing, code-style, release, roadmap, and related files; create relative symbolic links only when platform and Git support them.
4. When symbolic links are unavailable, index the source path and status without creating a fake link or copying content.
5. Do not create source-document templates for files not present in the repository.
6. Update TaskFlow instructions, artifact routing, workflow draft, and both READMEs to use the new standards path and workspace behavior.

## Acceptance Criteria

- Standards resolve from `TaskFlowDocs/repository-docs/standards/index.md`.
- `repository-docs/index.md` lists discovered README files and records missing document classes.
- No symbolic link is created while `core.symlinks=false`; the index remains usable through relative paths.
- All active references use the new standards path.

## In Scope

- Documentation workspace directory, index, standards move, and workflow documentation.

## Out of Scope

- Editing, copying, generating, or publishing source documentation.
- A remote Git-host API, background synchronizer, or cross-repository aggregation.

## Open Questions

- None. User approved the workspace, fallback behavior, and missing-document policy.

## Version History

- v1 — initial implementation.
