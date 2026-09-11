# Repository document environment behavior
> Task version: v2
> Status: completed

## Goal

Design TaskFlow behavior so an Agent maintains and uses a unified repository-document environment: it discovers existing repository guidance, exposes it under `TaskFlowDocs/repository-docs/`, refreshes the catalog when relevant files change, and applies relevant rules during task work.

## Confirmed Facts

- v1 created a directory and index but did not define the complete workflow behavior.
- The user wants a TaskFlow design, not merely documentation maintenance.
- `core.symlinks=false` in the current repository, so a portable index is required when links cannot work.

## Required Behavior

1. At TaskFlow triage and before PR/remote work, discover recognized repository documents and refresh the unified catalog when stale or absent.
2. Recognize README, contributing, code style, release, roadmap, code of conduct, PR templates, CODEOWNERS, branch/CI guidance, and repository standards.
3. Use relative symbolic links only if supported and safe; otherwise provide a portable path catalog with equivalent navigation.
4. Treat linked source files as authoritative; do not copy their contents into TaskFlowDocs.
5. Load applicable source documents by task phase: code changes, commits/PRs, architecture/design, release, and roadmap work.
6. On source-document addition, removal, move, or relevant content change, update the catalog as a work revision; on a rule change affecting an approved task, trigger the existing material-change workflow.
7. Keep task-specific facts in the task directory; the repository document environment is shared context only.

## Acceptance Criteria

- The Skill has explicit discovery, refresh, selection, and source-authority behavior.
- The workspace index contains machine-checkable source paths, link mode, document class, and last checked date.
- A TaskFlow task identifies which repository documents were applicable and used.
- Symlink fallback works without copying or fake links.

## Open Questions

- None. The user approved refresh only when absent, stale, or task-phase-relevant; confirmation before adding unrecognized candidates; and informational handling for missing document classes unless a needed repository rule is absent.

## Version History

- v1 — directory-centric approach; superseded because Agent workflow behavior was incomplete.
- v2 — behavior-first repository document environment.
