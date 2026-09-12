# Add explicit cross-platform runtime preflight for Windows Python dependencies
> Task version: v1
> Status: completed

## Goal

Add explicit cross-platform runtime preflight for Windows Python dependencies

## Background / Confirmed Facts

- TaskFlow hooks use Python for bounded Markdown processing.
- Windows may expose unusable Microsoft Store aliases, and the former per-script fallback did not verify Python 3 consistently.
- The implementation commit is `d3970c1` and is merged into the integration branch.

## Requirements

- Use one shared preflight for every Python-backed hook.
- Honor `TASKFLOW_PYTHON`, otherwise try `python3`, `python`, then `py`.
- Accept only Python 3 and reject WindowsApps aliases.
- Exit with an actionable diagnostic when no usable interpreter exists.
- Preserve Linux and Git Bash behavior.

## Acceptance Criteria

- A valid override is selected and printed.
- An unusable WindowsApps-style shim is rejected with Python 3 installation guidance.
- All affected shell scripts pass syntax checks.
- The complete TaskFlow smoke suite passes.

## In Scope

- `hooks/python-runtime` and Python-backed hook callers.
- Runtime documentation and smoke-test coverage.

## Out of Scope

- Replacing Git Bash with a separate PowerShell implementation.
- Installing Python automatically.
- The remaining optimization Todo items TF-20260911-04 through TF-20260911-08.

## Risks / Deferred Items

- Native Windows execution remains dependent on Git Bash; launcher hardening and Windows CI are separate Todo items.

## Open Questions

- None.

## Version History

- v1 — approved, implemented, and verified.
