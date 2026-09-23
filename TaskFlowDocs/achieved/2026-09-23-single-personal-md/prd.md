# Map the personal rule to a single personal.md: one file, each rule in its own se
> Task version: v1
> Status: completed

## Goal

Map the personal rule to a single personal.md: one file, each rule in its own section with its own scope etc. The repository-docs index names personal.md and explains its origin (local-only, never committed) and purpose (personal rules that cannot override repository documents).

## Background / Confirmed Facts

- Personal rules currently live as zero or more independent `*.md` files directly beside `TaskFlowDocs/repository-docs/index.md`. `hooks/repository-docs-context` scans that directory, skips `index.md`, and catalogs every other `*.md` as class `personal-rule`, phases `all`, status `local-only`.
- On 2026-09-23 the worktree has only `index.md`; its `## Personal rules` section reads `None.` when no personal row is cataloged, or a single generic sentence when one is.
- Route injection prints personal rules on their own line: `- Local personal rules (local-only, never committed; they cannot override the sources above): …`. They never enter `Read authoritative sources:`.
- Creating a personal rule is specified in `skills/taskflow/SKILL.md` (`*.md` beside `index.md`, five mandatory fields, optional commit/PR fields) and repeated in `skills/taskflow/references/artifacts.md` and both READMEs.
- `.gitignore` already ignores `TaskFlowDocs/repository-docs/*` and re-includes `index.md`, so any new `personal.md` stays uncommitted without a gitignore change.
- `hooks/smoke-test` pins the multi-file shape: it writes `my-card.md` and asserts the catalog row and route line for that path.
- Prior decision (2026-09-14, task `2026-09-14-personal-docs-git-boundary`): drop the `personal/` subdirectory; personal rules sit directly in `repository-docs/`; local-only and never committed; subordinate to repository documents. That boundary is unchanged.

## Requirements

- R1. The sole personal-rule file is `TaskFlowDocs/repository-docs/personal.md`. Other `*.md` files beside `index.md` are not cataloged as `personal-rule` and do not appear on the personal route line.
- R2. When `personal.md` exists, `hooks/repository-docs-context` catalogs exactly one `personal-rule` row for that path (class `personal-rule`, phases `all`, exists per disk, status `local-only`) and injects it on the existing personal route line only.
- R3. When `personal.md` is absent, no `personal-rule` row is derived and no personal route line is printed; the index still carries the standing Personal rules explanation (R5).
- R4. Each rule inside `personal.md` is its own section (heading) with its own `Scope` and the existing mandatory fields: `Scope`, `Repository documents checked`, `Rules`, `Verification`, `Exceptions / Change control`; commit-related rules also state `Commit format` and `PR checks`.
- R5. The index `## Personal rules` section always names `personal.md` and states origin (local-only, never committed) and purpose (personal rules cannot override repository documents), whether or not the file is present; when absent it also says the file is not present. Cataloged rows remain in the main table as today.
- R6. The hook does not parse sections or filter by `Scope`; scope applicability stays a Skill reading step (user decision Q2-A).
- R7. `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, `README.md`, and `README.zh-CN.md` describe creating/reading rules as sections of `personal.md`, not as new sibling `*.md` files, and keep the local-only / never-commit / subordinate boundary.
- R8. `hooks/smoke-test` asserts the single-file contract: `personal.md` is cataloged and routed alone; a stray sibling `*.md` is not cataloged as `personal-rule` and does not appear on the personal route line; index Personal rules prose names `personal.md` with origin and purpose; idempotent resync still holds.
- R9. No `personal.md` content is invented as placeholder; an absent file is a valid state.

## Acceptance Criteria

- A1. Creating `TaskFlowDocs/repository-docs/personal.md` yields one `| personal-rule | \`TaskFlowDocs/repository-docs/personal.md\` | all | yes | local-only |` row and a personal route line naming only that path; it never appears in `Read authoritative sources:`.
- A2. Creating only a sibling `my-card.md` (no `personal.md`) yields no `personal-rule` row and no personal route line naming `my-card.md`.
- A3. With no `personal.md`, `## Personal rules` still names `personal.md`, local-only / never committed, and that personal rules cannot override repository documents, and marks the file not present.
- A4. With `personal.md` present, the same standing explanation remains; existence is reflected by the catalog row / exists column, not by dropping the explanation.
- A5. A second sync over unchanged state is byte-identical (idempotent), and removing `personal.md` drops its row on the next run.
- A6. Grep in `SKILL.md`, `artifacts.md`, `README.md`, and `README.zh-CN.md` shows `personal.md` as the personal-rule location and keeps `never committed` / subordinate wording; no guidance tells the user to create a new sibling rule file as the normal path.
- A7. `bash hooks/smoke-test` passes on the task branch.
- A8. `.gitignore` still keeps `personal.md` out of Git (`git check-ignore` matches) while `index.md` stays tracked.

## In Scope

- `hooks/repository-docs-context` (scan + Personal rules render)
- `hooks/smoke-test` (personal-rule assertions)
- `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`
- `README.md`, `README.zh-CN.md`
- Task documents under `TaskFlowDocs/2026-09-23-single-personal-md/` and the linked `todo.md` entry lifecycle

## Out of Scope

- Changing the gitignore pattern set (already correct).
- Parsing `Scope` inside sections, phase-filtering personal rules, or multi-section route lines.
- Creating an actual `personal.md` or authoring any personal rule content.
- Migrating other branches/history that may still mention multi-file personal rules beyond this branch’s docs.
- Todo.md archival/growth (separate inbox item `TF-20260919-6b4e21`).
- Release/version tagging (not requested).

## Risks / Deferred Items

- Stray sibling `*.md` files are silently uncataloged (Q1-A). Deferred: optional warning — not required for acceptance.
- Older prose outside this branch may still say `*.md`; fixed on this branch only.
- Smoke-test is the executable contract; if it is run from another checkout, results do not apply (CONTRIBUTING rule).

## Open Questions

None — Q1/Q2/Q3 decided by the user on 2026-09-23 (A/A/A).

## Version History

- v1 — planning.
