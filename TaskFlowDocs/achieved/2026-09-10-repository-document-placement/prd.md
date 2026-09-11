# Repository document placement
> Task version: v1
> Status: completed

## Goal

Keep repository-owned documentation in conventional repository locations and make `TaskFlowDocs/repository-docs/index.md` path-only navigation rather than duplicate storage.

## Background / Confirmed Facts

- Repository documents commonly live at the repository root or in platform-standard directories.
- Current TaskFlow text already calls the index derived navigation but still permits symbolic links and records an access mode.
- The repository has duplicate source trees for the root and packaged TaskFlow skill; their checked files currently have matching hashes.
- The rule applies even before a directory is initialized as a Git repository because it may be published later.
- Personal supplements mean a person's development rules and work habits.

## Requirements

1. Existing repository-owned documents remain in their conventional locations and are referenced by repository-relative path in the index.
2. When an authorized repository-owned document is missing, create it in its conventional location, preferring the root where appropriate; use platform-standard directories for PR, CI, CODEOWNERS, and similar files.
3. Reuse an existing conventional filename; otherwise default to `README.md`, `CONTRIBUTING.md`, `CODE_STYLE.md`, or `ROADMAP.md` for those document classes.
4. Do not copy or symbolically link repository-owned documents into `TaskFlowDocs/repository-docs/`.
5. `TaskFlowDocs/repository-docs/` contains only `index.md` and personal supplements under `personal/`.
6. The index records document class, repository-relative source path, existence, and last-checked date; it has no access-mode field.
7. Personal supplements contain personal development rules or work habits, apply only within their declared scope, and cannot weaken, override, or conflict with repository rules.
8. Legacy copies or symbolic links are reported and no longer used; migration or deletion requires explicit user authorization.

## Acceptance Criteria

- No maintained TaskFlow guidance recommends copies or symbolic links for repository-owned documents.
- Skill guidance states where authorized missing repository documents are created, including non-Git directories.
- The catalog contract omits access mode and limits `repository-docs/` contents to the index and `personal/`.
- Personal supplements are explicitly defined and subordinate to repository rules.
- English and Chinese README descriptions agree.
- Root and packaged duplicate Skill/reference files remain byte-identical.
- Verification searches find no obsolete symbolic-link/access-mode guidance in maintained documentation.

## In Scope

- `SKILL.md` and `skills/taskflow/SKILL.md`
- `references/artifacts.md` and `skills/taskflow/references/artifacts.md`
- `README.md` and `README.zh-CN.md`
- TaskFlow planning and catalog artifacts for this change

## Out of Scope

- Moving or deleting legacy repository documents
- Adding migration automation
- Creating currently absent repository documents unrelated to this change
- Committing, pushing, or publishing

## Risks / Deferred Items

- Downstream repositories may already contain legacy duplicates or links; TaskFlow will report them and wait for explicit authorization.

## Open Questions

None.

## Version History

- v1 — Initial approved-scope candidate based on user decisions from 2026-09-10.
