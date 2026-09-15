# State in the Skill that personal supplements are local-only and must not be committed to Git
> Task version: v1
> Status: in_progress

## Goal

Make the personal-supplement boundary explicit: `TaskFlowDocs/repository-docs/personal/` holds one person's local rules, must not be committed, and anything meant to be shared belongs in a repository-owned document instead.

## Background / Confirmed Facts

- `skills/taskflow/SKILL.md:102` and `skills/taskflow/references/artifacts.md:7,11` define personal supplements under `TaskFlowDocs/repository-docs/personal/`, subordinate to repository documents, but never state whether they enter Git.
- The repository currently contradicts the intended rule: `TaskFlowDocs/repository-docs/personal/README.md` is tracked (`git ls-files` confirms), and copies exist on other branches (`feat/event-aware-docs`, `perf/session-context`).
- `hooks/repository-docs-context` catalogs every `personal/*.md` except that `README.md` into `index.md` (`hooks/repository-docs-context:72-76`), so the placeholder README is currently not indexed.
- `.gitignore` contains only `.sxng/` and `tasks/`; there is no ignore rule for personal content.
- The user's standing rule (2026-09-14): personal rules are not committed to Git and this must be stated in the Skill.
- `TaskFlowDocs/repository-docs/index.md` still carries a `Personal supplements` section pointing at "Cataloged above when present", which stays valid under the new boundary.

## Requirements

- R1. `skills/taskflow/SKILL.md` states that personal supplements are local-only working rules: not committed, not pushed, not part of a PR, and never the way to change shared or team policy.
- R2. The same section states the correct channel: anything that must be shared or survive a fresh clone becomes a repository-owned document at its conventional source path under the existing creation and approval rules.
- R3. `skills/taskflow/references/artifacts.md` repeats only the actionable boundary in its repository-docs paragraph, without restating the SKILL lifecycle rules.
- R4. This repository ignores `TaskFlowDocs/repository-docs/personal/` content while keeping the directory's purpose documented.
- R5. The tracked `TaskFlowDocs/repository-docs/personal/README.md` stops being tracked, with the local file preserved.
- R6. A personal supplement remains excluded from Git even when a task uses it; using a supplement must not create a commit requirement.

## Acceptance Criteria

- A1. `grep` for the local-only statement finds it in `skills/taskflow/SKILL.md` and `skills/taskflow/references/artifacts.md`, and both describe the repository-owned document as the shared alternative.
- A2. `git check-ignore -v TaskFlowDocs/repository-docs/personal/example.md` matches the new ignore rule.
- A3. `git ls-files TaskFlowDocs/repository-docs/personal/` returns nothing, while `TaskFlowDocs/repository-docs/personal/README.md` still exists in the working tree with unchanged content.
- A4. `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow` passes.
- A5. `bash hooks/smoke-test` passes and `git diff --check` is clean.
- A6. No other tracked personal supplement exists; if any other than `README.md` is found, it is reported rather than silently untracked.

## In Scope

- `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, `.gitignore`, and the tracked-status change for the existing `personal/README.md`.
- README / README.zh-CN wording only if an existing statement would contradict the new rule.

## Out of Scope

- Removing or rewriting the placeholder README's purpose.
- Changing `hooks/repository-docs-context` cataloging behavior, or the `index.md` `Personal supplements` section.
- Rewriting history on other branches that already contain the personal placeholder.
- Any new hook, task-document, or versioning behavior.

## Risks / Deferred Items

- Untracking `personal/README.md` is a Git state change in a shared repository; it requires the user's explicit authorization for the `git rm --cached` step before execution.
- Older branches and clones still carry the placeholder; the ignore rule stops new tracking but does not clean history. Deferred unless the user asks.
- A contributor who needs a personal rule on another machine must copy the file manually; the Skill states this rather than inventing a sync mechanism.

## Open Questions

None — scope, wording depth, and the in-repository fix were decided by the user on 2026-09-14. The `git rm --cached` authorization is tracked in the Plan Approval record.

## Version History

- v1 — planning.
