# Restore macOS portability for hooks and smoke tests
> Task version: v1
> Status: ready

## Goal

Make the TaskFlow hooks and smoke tests pass on stock macOS (bash 3.2 + BSD userland) so the plugin's claimed cross-platform support actually holds, and close the small consistency findings from the same review.

## Background / Confirmed Facts

- External review, reproduced on macOS 26 with `/bin/bash` 3.2.57 and BSD sed: `bash hooks/smoke-test` fails at `== version bumps root + archives only changed docs ==` with `hooks/version: line 27: selected[*]: unbound variable`.
- `hooks/version` references an empty array under `set -u` (fails on bash < 4.4) and uses GNU-only bare `sed -i` (BSD sed treats the script as a backup extension).
- `hooks/smoke-test` uses `sha256sum`, which is absent on stock macOS (`shasum -a 256` is the built-in equivalent), and uses the same GNU `sed -i`.
- `hooks/smoke-test [tmp-root]` deletes a caller-provided root via its EXIT trap.
- CI (`.github/workflows/hooks.yml`) covers ubuntu + windows only, so the macOS breakage was invisible; `evals/runner.py` is never exercised in CI.
- `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` declare `"license": "MIT"` while `LICENSE` and both READMEs state AGPL-3.0.
- `hooks/repository-check` initializes `blocked=0` but never sets it, so the `STATUS: blocked` tail branch is unreachable (exit 3 remains in use for the not-a-git-repository preflight).

## Requirements

- `bash hooks/smoke-test` passes on stock macOS (`/bin/bash` 3.2, BSD sed) and keeps passing on Linux.
- `hooks/version` works under bash 3.2 with BSD sed.
- `hooks/smoke-test` never deletes a caller-supplied root.
- CI runs the bash smoke tests on macOS and runs the evals.
- Plugin license metadata matches the repository LICENSE.
- No behavior change on the Linux/Windows paths beyond the above.

## Acceptance Criteria

- `bash hooks/smoke-test` prints `ALL SMOKE PASSED` on macOS.
- A caller-provided smoke-test root still exists after the run.
- `python3 evals/runner.py` prints `PASS`.
- All plugin manifests parse as JSON and declare AGPL-3.0.
- `git diff --check` is clean.

## In Scope

- `hooks/version`, `hooks/smoke-test`, `hooks/repository-check`
- `.github/workflows/hooks.yml`
- `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`
- TaskFlow task records for this change

## Out of Scope

- SKILL.md workflow semantics and reference documents
- `hooks/smoke-test-windows.ps1` (unchanged; Windows path already covered)
- Version bumps, tags, releases, and marketplace pin updates (maintainer release flow)

## Risks / Deferred Items

- The temp-file + `mv` rewrite replaces file inodes, matching the existing awk rewrite already used in `hooks/version`; permissions follow the process umask.
- SPDX identifier chosen as `AGPL-3.0-only` (LICENSE carries no "or later" grant); maintainer may prefer `AGPL-3.0-or-later` — flagged in the PR.

## Open Questions

- None blocking. License identifier wording is left to maintainer review.

## Version History

- v1 — planning.
