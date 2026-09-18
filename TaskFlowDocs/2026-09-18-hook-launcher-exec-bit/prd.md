# Hook launcher exec bit
> Task version: v1
> Status: in_progress

## Goal

Every hook script in the plugin — the launcher above all — is recorded in Git
without the executable bit, so a Unix plugin install cannot execute it and the
SessionStart hook fails with `Permission denied`.

## Background / Confirmed Facts

- Claude Code runs a plugin `command` hook through the platform shell
  (`sh -c` on macOS and Linux), so the command's first token has to be an
  executable *file*. Nothing in the install path adds the bit: the docs tell an
  author to `chmod +x` a hook script themselves, and never state that the plugin
  installer chmods anything.
- The plugin cache is populated from a Git checkout of the marketplace
  `source`, so the mode recorded in the Git tree is the mode a user's install
  gets. `hooks/run-hook.cmd` is `100644` in every commit in this repository's
  history, and every other hook script with it.
- Reproduced on this host: `/bin/sh -c '"<cache>/hooks/run-hook.cmd" session-start'`
  exits `126` with `Permission denied`; the same file invoked as
  `bash "<cache>/hooks/run-hook.cmd" session-start` prints the SessionStart
  context normally. The failure is a mode, not a script defect.
- The pattern this launcher is modelled on — `obra/superpowers` — records
  `hooks/run-hook.cmd` as `100755`.
- The existing suite never caught it because every section invokes hooks as
  `bash "$HERE/<hook>"`. That explicit interpreter is the one form the harness
  does not use, so a launcher nothing can execute left a fully green suite.

## Requirements

- R1: Every hook script that a host executes as a program is recorded as
  `100755` in the Git tree: `hooks/run-hook.cmd` first, then the rest of
  `hooks/` for consistency.
- R2: The same treatment for `tools/fixture-compare`, which carries a shebang,
  is invoked as a path, and is in the same class.
- R3: The suite fails when the launcher cannot be executed the way the harness
  executes it, and when the Git tree records it non-executable.

## Acceptance Criteria

- `git ls-files -s` reports `100755` for `hooks/run-hook.cmd` and for every
  other non-JSON, non-Markdown file under `hooks/`, and for
  `tools/fixture-compare`.
- `bash hooks/smoke-test` passes.
- Reverting the mode, or chmod-ing the launcher to `644` outside a Git
  checkout, makes the new section fail with a message naming the cause.
- No hook's content changes.

## In Scope

- File modes in the Git index for `hooks/` and `tools/fixture-compare`.
- One new assertion section in `hooks/smoke-test`.

## Out of Scope

- The `hooks.json` / `hooks-codex.json` / `hooks-codebuddy.json` command
  strings. Adding a `bash` prefix would also work on Unix but changes the
  Windows polyglot path, which is not the defect.
- Any claim that the plugin installer normalizes modes. That is undocumented,
  so the fix does not depend on it.
- The local plugin cache in `~/.claude/plugins/cache`. It is regenerated on
  every plugin update, so patching it fixes one session and not the plugin.

## Risks / Deferred Items

- `tools/fixture-compare` is non-idempotent on this host: two runs of the
  unmodified suite differ in three captured files, two of which embed a fresh
  Git SHA per run. Pre-existing and unrelated to this change, confirmed by
  running the comparison against an unmodified checkout. Not fixed here.
- `hooks/smoke-test-windows.ps1` gets the bit for consistency although
  `cmd.exe` and PowerShell do not read it. Harmless, and it keeps the "no
  script under `hooks/` is 644" rule checkable by one glance.

## Open Questions

None.

## Version History

- v1 — planning.
