# Personal rules live in repository-docs/ and are local-only
> Task version: v2
> Status: completed

## Goal

Make the personal-rule boundary explicit and structural: a person's own rules are plain files beside `TaskFlowDocs/repository-docs/index.md`, are never committed, and are always subordinate to repository documents; anything shared belongs in a repository-owned document instead.

## Background / Confirmed Facts

- `skills/taskflow/SKILL.md:102` and `skills/taskflow/references/artifacts.md:7,11` define personal supplements under `TaskFlowDocs/repository-docs/personal/`, subordinate to repository documents, but never state whether they enter Git.
- The repository contradicts the intended rule: `TaskFlowDocs/repository-docs/personal/README.md` is tracked (`git ls-files` confirms), and copies exist on other branches (`feat/event-aware-docs`, `perf/session-context`).
- `hooks/repository-docs-context:72-76` (v1) scanned `personal/*.md` and cataloged everything except that `README.md`, and the personal paths were merged into the same `Read authoritative sources:` line as repository-owned documents. Measured on 2026-09-14 by adding `personal/test-rule.md`: the route line read `Read authoritative sources: LICENSE, CONTRIBUTING.md, CODE_STYLE.md, TaskFlowDocs/repository-docs/personal/test-rule.md`, so the subordinate status was invisible.
- Repository-owned documents are never copied into `repository-docs/` (`SKILL.md:77`), so every other `*.md` beside `index.md` in that directory is by construction a personal rule. The `personal/` subdirectory carries no information the location does not already carry.
- `.gitignore` contains only `.sxng/` and `tasks/`; there is no ignore rule for personal content.
- The user's rules (2026-09-14, 2026-09-15): personal rules are not committed to Git and this must be stated in the Skill; the `personal/` directory is dropped and personal rules sit directly in `repository-docs/`; the placeholder README goes away with the directory; the personal route must still be injected.

## Requirements

- R1. `skills/taskflow/SKILL.md` states that a personal rule is a local-only working rule: not committed, not pushed, not part of a PR, and never the way to change shared or team policy.
- R2. The same section states the correct channel: anything that must be shared or survive a fresh clone becomes a repository-owned document at its conventional source path under the existing creation and approval rules.
- R3. A personal rule lives directly under `TaskFlowDocs/repository-docs/`; there is no `personal/` subdirectory, and the directory contains `index.md` plus those rules only.
- R4. `hooks/repository-docs-context` treats every `*.md` beside `index.md` in `repository-docs/` as a personal rule: it catalogs it with class `personal-rule`, phases `all`, and status `local-only`.
- R5. The hook injects personal rules on their own route line that states they are local-only, never committed, and cannot override the routed repository sources; a personal rule never appears in the `Read authoritative sources:` line.
- R6. A personal rule removed from disk disappears from the index on the next sync; the index never keeps a stale personal row.
- R7. The `personal/` directory and its placeholder `README.md` are removed from the repository.
- R8. This repository ignores personal-rule files while `index.md` stays tracked.
- R9. `skills/taskflow/references/artifacts.md` repeats only the actionable boundary and the new location; `README.md` and `README.zh-CN.md` state the same rule.
- R10. A personal rule stays excluded from Git even when a task uses it; using one must not create a commit requirement.

## Acceptance Criteria

- A1. `grep` finds the local-only statement in `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, `README.md`, and `README.zh-CN.md`, and each names the repository-owned document as the shared alternative.
- A2. `TaskFlowDocs/repository-docs/personal/` does not exist, and no tracked file references that path.
- A3. `git check-ignore -v TaskFlowDocs/repository-docs/example-rule.md` matches the ignore rule, while `git check-ignore TaskFlowDocs/repository-docs/index.md` does not.
- A4. With a `*.md` beside `index.md`, `hooks/repository-docs-context` catalogs it as `| personal-rule | ... | all | yes | <date> | local-only |` and prints one `- Local personal rules (...)` line naming it; the same file never appears in `Read authoritative sources:`.
- A5. Removing that file and re-running the hook drops its row and its route line, and a second run over the unchanged state is byte-identical (idempotent).
- A6. No personal rule appears in the `index.md` `Personal rules` section as a repository-owned class, and `index.md` itself is never cataloged as a personal rule.
- A7. `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow` passes, `bash hooks/smoke-test` passes, and `git diff --check` is clean.

## In Scope

- `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, `README.md`, `README.zh-CN.md`, `.gitignore`, `hooks/repository-docs-context`, `hooks/smoke-test`, `TaskFlowDocs/repository-docs/index.md`, and removal of `TaskFlowDocs/repository-docs/personal/`.

## Out of Scope

- Rewriting history or removing the placeholder from other branches and tags that already contain it.
- Any new hook, task-document, or versioning behavior.
- Enforcing the ignore rule for a clone that adds personal rules before the rule exists.

## Risks / Deferred Items

- Removing `personal/` needs the user's authorization for the tracked-file deletion; it is recorded in the Plan Approval record.
- Older branches and clones still carry the placeholder; the ignore rule and this change do not clean history. Deferred unless the user asks.
- A contributor who needs a personal rule on another machine must copy the file manually; the Skill states this rather than inventing a sync mechanism.
- `repository-docs/` now mixes routing metadata with personal content; the distinction is by filename (`index.md` vs the rest) and by the class column, which the smoke test pins.

## Open Questions

None — location, placeholder disposal, and route injection were decided by the user on 2026-09-15.

## Version History

- v2 — `personal/` subdirectory dropped; personal rules live directly in `repository-docs/` with their own injected route line and an ignore rule.
- v1 — approval was requested for the original statement-only change; superseded before implementation.
