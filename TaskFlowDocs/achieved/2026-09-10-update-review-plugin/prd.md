# Update and review TaskFlow plugin
> Task version: v1
> Status: completed

## Goal

Fix the confirmed TaskFlow plugin defects, publish a uniquely versioned release, update the installed Codex plugin, and verify the installed behavior and cache contents end to end.

## Background / Confirmed Facts

- The project and installed Codex plugin both report `1.0.0+codex.20260909145457`, but the project is at commit `91807ef` while the marketplace snapshot and installed cache are at `6a1c349`.
- `hooks/run-hook.cmd session-start` fails on this Windows host because its fixed Git Bash paths omit the actual `D:\Program Files\Git\bin\bash.exe`, then its PATH fallback selects WSL Bash and passes a Windows path unchanged.
- `hooks/summarize-state` recognizes only Todo headings beginning `## T-`, while the Skill contract requires an `ID` field and does not require that heading shape; current valid Todo items are omitted.
- `hooks/archive` moves the task before checking `todo.md`; an isolated reproduction returned failure after the active task had already moved to `achieved`.
- JSON and Bash syntax checks pass, so these are behavioral/contract defects rather than parse errors.
- The user authorized the three fixes, version bump, scoped commit/push, marketplace refresh, reinstall, and verification.

## Requirements

1. Make the Windows launcher use the Git for Windows installation associated with `git.exe` before considering PATH Bash, and never silently select WSL Bash for a Windows script path.
2. Make Todo summary parsing follow the documented `ID` field contract while continuing to exclude `done` items.
3. Make archive preflight validate the Todo file and matching task entry before moving the task directory.
4. Add the smallest regression checks that fail for each confirmed defect.
5. Change Claude plugin version from `1.0.0` to `1.0.1` and Codex plugin version to a unique `1.0.1+codex.<timestamp>` value, keeping manifests coherent.
6. Preserve the previously completed repository-document-placement changes already present at commit `91807ef`.
7. Commit and push only the plugin files required by this task; exclude `TaskFlowDocs/`.
8. Refresh only the `taskflow` marketplace, reinstall/update only `taskflow@taskflow`, and verify installed/enabled state, revision/version, cache parity, and Windows SessionStart execution.

## Acceptance Criteria

- `cmd.exe /d /c hooks\\run-hook.cmd session-start` succeeds on the current Windows host and invokes Git Bash rather than WSL Bash.
- Todo summary includes a non-done entry whose display heading is arbitrary but whose `ID` field is valid.
- Archive with a missing Todo or missing linked task entry fails before moving the active task.
- Existing lifecycle smoke checks and new regression checks pass.
- Both plugin manifests report the agreed `1.0.1` release family with a unique Codex build version.
- The scoped commit is present on `origin/main`; no TaskFlow task artifacts are committed.
- `codex plugin list --json` reports TaskFlow installed and enabled at the new Codex version.
- Installed metadata points to the pushed revision and maintained cache files match that revision.

## In Scope

- Confirmed fixes in `hooks/run-hook.cmd`, `hooks/summarize-state`, and `hooks/archive`
- Minimal regression additions to `hooks/smoke-test`
- Necessary Hook documentation corrections
- `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` version bumps
- Scoped commit/push and TaskFlow-only Codex marketplace/cache refresh

## Out of Scope

- Updating other plugins
- Broad Hook rewrites or new runtime dependencies
- Changing TaskFlow workflow semantics unrelated to confirmed defects
- Committing `TaskFlowDocs/`
- Creating a pull request or release tag

## Risks / Deferred Items

- Marketplace refresh requires network access and writes outside the project; the user explicitly authorized both.
- Claude Code installation is not being changed because the request concerns the installed TaskFlow plugin visible to Codex.
- Other lifecycle scripts may deserve future transactional hardening, but no unverified redesign is included.

## Open Questions

None.

## Version History

- v1 — Three confirmed fixes, version bump, scoped publication, and Codex reinstall/update.
