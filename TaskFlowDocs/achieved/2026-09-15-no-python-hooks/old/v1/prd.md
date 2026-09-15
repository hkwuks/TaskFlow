# Remove the Python runtime dependency from TaskFlow hooks
> Task version: v1
> Status: in_progress

## Goal

Run every TaskFlow hook with no Python interpreter available, using only POSIX
shell, `awk`, and `sed` at bash 3.2 level, without changing any hook's behavior,
output, or exit code.

## Background / Confirmed Facts

- Python is used only to edit and read Markdown/structured text. It is invoked
  through `hooks/python-runtime` by eight hooks:
  `task` (183 lines), `repository-docs-context` (166), `session-record` (121),
  `summarize-state` (56), `archive` (16), `reopen` (9), `session-start` (9),
  `session-record` via `session-start`.
- `hooks/python-runtime` exists solely to locate and validate an interpreter and
  to reject WindowsApps Microsoft Store aliases. Removing the dependency deletes
  the problem it was written for, along with `TASKFLOW_PYTHON`.
- `hooks/version`, `hooks/repository-check`, and `hooks/run-hook.cmd` are already
  Python-free; `hooks/version` already uses the temp-file + `mv` idiom and `awk`
  field rewriting, so the target idiom exists in this repository.
- Task `2026-09-14-macos-hook-portability` established the portability floor:
  bash 3.2 (`/bin/bash` on stock macOS) and BSD userland. It removed GNU-only
  bare `sed -i` and `sha256sum`. No associative arrays (`declare -A`) and no
  bash-4 substitutions may be introduced.
- The user's reason is compatibility risk: an interpreter that may be missing,
  shimmed, or a different major version is a failure mode the plugin does not
  need, and Python is currently a hard requirement for SessionStart to produce
  any context at all.
- Windows is not a separate implementation target: Git for Windows Bash is a
  required runtime, so one POSIX implementation serves every platform.

## Requirements

- No hook invokes Python, and no `python`, `python3`, `py`, or `TASKFLOW_PYTHON`
  lookup remains in `hooks/`.
- `hooks/python-runtime` is deleted.
- Behavior, stdout, stderr, and exit codes are unchanged for every hook; the
  existing smoke suite passes with no assertion weakened, skipped, or deleted.
- The implementation uses only POSIX `awk`/`sed` (no `gensub`, no `\b`, no
  `--posix`-only constructs, no `sed -i` without a backup-extension argument),
  bash 3.2-compatible syntax, and the temp-file + `mv` write idiom.
- The smoke suite passes with no Python on `PATH` at all.
- `.github/workflows/hooks.yml` no longer installs Python for the hook jobs, and
  the `setup-python` step is removed only if no remaining CI step needs it.
- Documentation that states Python is required is corrected: `hooks/README.md`,
  `skills/taskflow/references/runtime.md`, the plugin/README install guidance.

## Acceptance Criteria

- `PATH` restricted to a directory tree with no `python*` and no usable
  `TASKFLOW_PYTHON`: `bash hooks/smoke-test` prints `ALL SMOKE PASSED`.
- `grep -rn 'python' hooks/` matches nothing outside historical comments that the
  Plan explicitly lists.
- Identical behavior on the same fixtures: for the session-record, index-sync,
  and lifecycle fixtures, the produced files are byte-identical before and after
  the change (captured in the Plan's Verification section).
- bash 3.2 syntax check passes (`bash -n`), and `awk`/`sed` usage avoids the
  GNU-only constructs listed above.
- CI passes on ubuntu, macos, and windows runners.

## In Scope

- `hooks/task`, `hooks/repository-docs-context`, `hooks/session-record`,
  `hooks/summarize-state`, `hooks/archive`, `hooks/reopen`, `hooks/session-start`
- Deletion of `hooks/python-runtime`
- `hooks/smoke-test` (fixtures for the no-Python assertion only; no coverage
  removed), `hooks/smoke-test-windows.ps1` if it references the runtime
- `hooks/README.md`, `skills/taskflow/references/runtime.md`, `README.md`,
  `README.zh-CN.md`, `.github/workflows/hooks.yml`

## Out of Scope

- Hook behavior changes, new fields, new commands, or a changed context budget.
- A native PowerShell implementation: Git for Windows Bash stays a required
  runtime and is documented as such.
- `evals/runner.py`, which is a repository-side test harness and not part of the
  installed plugin's runtime.

## Risks / Deferred Items

- `awk`/`sed` are more error-prone than Python for structured edits. The guard is
  byte-identical output on the existing fixtures, not a rewritten expectation.
- Line-ending behavior on Windows: writes must stay in the same mode the Python
  implementation produced (`newline=""`), or diff churn appears on Windows.
- A host without any POSIX toolchain is already unsupported; this change removes
  one dependency without adding any.

## Open Questions

- None blocking.

## Version History

- v1 — planning.