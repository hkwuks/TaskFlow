# Changelog

## [1.0.5] — 2026-09-15

### Added

- A Git merge driver for `TaskFlowDocs/todo.md`, installed into the clone by `SessionStart`, so two task branches merge Todo by entry instead of by line.
- Deterministic Todo IDs derived from the goal (`TF-<yyyymmdd>-<6 hex>`), replacing the `TF-<date>-<max+1>` counter that made two branches cut from one base allocate the same ID.
- Session ids recorded in the selected task's `sessions.md`, and the macOS CI runner added to the hooks matrix.
- `CONTRIBUTING.md` working-branch rules and repository-documents guidance for personal rules.
- CodeBuddy as a third host: `.codebuddy-plugin/plugin.json` and `.codebuddy-plugin/marketplace.json`, installable through the CodeBuddy Code CLI (`codebuddy plugin marketplace add` then `codebuddy plugin install`), and `hooks/hooks-codebuddy.json` wiring `SessionStart` through `${CODEBUDDY_PLUGIN_ROOT}`. The CodeBuddy IDE client does not implement these commands, so the plugin is exercised through the CLI.

### Fixed

- **Hooks no longer need a Python interpreter at all.** `hooks/python-runtime` and `TASKFLOW_PYTHON` are gone; every hook is POSIX shell with `awk` and `sed` at the bash 3.2 + BSD userland level.
- macOS portability: `sed`/`grep` patterns that relied on GNU-only `\|` and `\{n\}` no longer fail silently or vacuously, and the hooks parse under the bash 3.2 that macOS ships.
- `hooks/version` no longer archives a tracked document that has uncommitted changes, which had made `old/vN/` record the text that replaced the version instead of the version itself.
- `task progress` and `task complete` now require the same recorded approval as `task state in_progress`; previously an unapproved task could be completed step by step and archived.
- Windows launcher argument forwarding, and the repository-document index path and concurrency protections carried over from 1.0.4.
- `hooks/release-check` reads each catalog's pin from inside its `source` object instead of scanning the whole file, so a second entry carrying `ref`/`sha` can no longer displace the value being checked, and it validates the `X.Y.Z` shape of all three manifests rather than only the one without a cachebuster suffix.

### Compatibility

- **The runtime floor dropped.** No interpreter needs to be located, validated, or version-matched; a missing, shimmed, or wrong-major-version Python is no longer a failure mode. Windows still requires Git for Windows Bash, and there is still exactly one implementation of each hook.
- **Todo IDs change shape for new entries.** Existing entries keep their numeric suffix; only new intake uses the derived six-hex-digit form.
- **The Todo merge driver applies to local merges only.** A pull request merged in a hosting web UI runs server-side and does not run a custom driver, so that path still produces an ordinary content conflict. `skills/taskflow/references/runtime.md` states this.
- Updating an existing installation needs no migration or dependency installation.

### Verification

- `bash hooks/smoke-test` — passed on Ubuntu, macOS, and Windows GitHub Actions runners.
- `python3 evals/runner.py` — passed.
- TaskFlow Skill validator — passed.
- Every hook parses under a real `bash:3.2` container.

## [1.0.4] — 2026-09-13

### Added

- Current-task-first SessionStart context with explicit verbose mode.
- SessionStart event JSON routing using `cwd`, event filtering, and safe malformed-input diagnostics.
- Linux and Windows GitHub Actions coverage for TaskFlow hooks.

### Fixed

- Windows launcher forwarding for more than nine arguments, spaces, and Unicode values.
- Repository-document index path traversal validation, malformed-row preservation, and concurrent-write protection.
- Explicit Python 3 runtime discovery and Microsoft Store alias diagnostics.

### Compatibility

- Runtime behavior remains backward-compatible; hooks continue to use Git Bash on Windows and Python 3 for Markdown lifecycle operations.
- No migration or dependency installation is required for existing installations.

### Verification

- `bash hooks/smoke-test` — passed.
- Linux and Windows GitHub Actions matrix — passed.
- TaskFlow Skill validator — passed.
