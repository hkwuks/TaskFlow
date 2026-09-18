# Changelog

## [1.0.7] — 2026-09-19

### Added

- `hooks/task next <todo-id> <next-action> [notes]` — writes a Todo entry's `- Next action:` and `- Updated:` in one call, and appends `notes` at the end of the entry's Notes block. The fields it writes are templated from state the Agent already has, so writing them by hand only bought a full read of `TaskFlowDocs/todo.md` to change two lines. Missing fields are added rather than failing the write, matching `hooks/archive`.
- `hooks/task get <todo-id>` — prints one entry's field lines verbatim, so confirming an entry's state no longer means reading every entry. It is the read half of the same trade `task next` makes on the write side.
- `hooks/repository-check` — a read-only readiness summary: missing baseline governance documents and ambiguous branch/remote information are reported as `needs-user-input`, and any task artifact left uncommitted in the checkout is named. Opt-in; it is not attached to automatic hooks.
- A conflict rule in `skills/taskflow/SKILL.md`: when a merge or rebase the Agent runs hits a conflict, stop and put both sides in front of the user, who decides what to keep; the decision is recorded in the task `plan.md` before continuing. An automatic merge needs no action, and a conflict on a pull request merged in a hosting web UI is explicitly outside the rule.

### Fixed

- **The Claude Code SessionStart hook failed on every Unix installation.** `hooks/hooks.json` invokes `hooks/run-hook.cmd` as a bare path, but the file was recorded in Git without its executable bit, so the host failed each session with `Permission denied` (exit 126) — a configured hook that could not run, and no plugin feature behind it. `hooks/*` and `tools/fixture-compare` now carry the executable bit in the index. **This is the reason to update from 1.0.6.**
- `README.zh-CN.md` said the release check compares "two plugin manifests" where `hooks/release-check` compares three. The count had been corrected once before, and a later conflict resolution reverted it — two sides that both read as valid Chinese, differing only in the number.
- The awk program in `hooks/task` could be broken by an apostrophe in a comment: macOS ships bash 3.2, whose parser rejects that shape inside a heredoc that is itself inside a command substitution, and it reports the failure against the end of the substitution rather than the comment.

### Compatibility

- **No runtime or installation change.** The hook set, the plugin wiring, and the POSIX-shell-plus-awk floor are unchanged from 1.0.6; updating an existing installation needs no migration and no dependency installation.
- **`task next` and `task get` are additions, not changes.** They are new explicit subcommands; the existing `intake` / `promote` / `state` / `progress` / `complete` lifecycle is unchanged, and a task that never calls them behaves exactly as before.
- **The conflict rule hands control back to the user.** On a conflict you decide which side to keep, so a merge that hits one stops and waits. Only merges the Agent runs are covered; a pull request resolved in a hosting web UI is not.
- **A release is two commits by construction.** The marketplace pin names a commit that cannot exist before the tag does, so the pin lands as a second commit after the tag. Claude Code verifies the pin at install time and refuses a mismatch as `sha_pin_mismatch`; it clones by the pinned commit rather than by the tag, which is what keeps an installation on the reviewed release if the tag is ever moved.

### Verification

- `bash hooks/smoke-test` — passed on Ubuntu, macOS, and Windows GitHub Actions runners.
- `bash hooks/release-check .` — passed.
- `python3 evals/runner.py` — passed.
- TaskFlow Skill validator — passed.

## [1.0.6] — 2026-09-17

### Added

- CodeBuddy as a third host: `.codebuddy-plugin/plugin.json` and `.codebuddy-plugin/marketplace.json`, installable through the CodeBuddy Code CLI (`codebuddy plugin marketplace add` then `codebuddy plugin install`), and `hooks/hooks-codebuddy.json` wiring `SessionStart` through `${CODEBUDDY_PLUGIN_ROOT}`. The CodeBuddy IDE client does not implement these commands, so the plugin is exercised through the CLI.
- `hooks/todo-check` — reports a Todo entry a merge dropped, by comparing every `- ID:` a merge commit's parents held against the result. A hosted-platform merge runs server-side where the merge driver cannot go, so the check runs after the fact; its range form audits every merge in a push, and the `todo-merge-audit` CI job runs it on every push to `main` and on every pull request.
- `hooks/release-check` — compares the version literals a release has to move (both plugin manifests, the newest `CHANGELOG.md` section, the `claude plugin list` sample in each README) and confirms each marketplace `ref` resolves to the commit its `sha` names. The `release` CI job runs it on every change, so a README sample or CHANGELOG section left on the previous version is caught at the commit that left it rather than at the next release.
- `RELEASE.md` records why a release is two commits, and its validation checklist now carries `hooks/release-check` in place of the inline Python manifest dump.

### Fixed

- `hooks/release-check` reads each catalog's pin from inside its `source` object instead of scanning the whole file, so a second entry carrying `ref`/`sha` can no longer displace the value being checked, and it validates the `X.Y.Z` shape of all three manifests rather than only the one without a cachebuster suffix.
- `hooks/archive` clears the Todo item's `Next action` to `None — completed and archived.` instead of leaving the pre-completion action in place. `promote` writes an action that is only true before completion, so every archived entry claimed outstanding work; the archive transaction now asserts the field was cleared.

### Compatibility

- **No runtime or installation change.** The runtime floor, the hook set, and the plugin wiring are unchanged from 1.0.5; updating an existing installation needs no migration or dependency installation.
- **CodeBuddy is CLI-only.** The CodeBuddy IDE client does not implement `plugin` subcommands, so the plugin is installed and validated through the CodeBuddy Code CLI.
- **A release is two commits by construction.** The marketplace pin names a commit that cannot exist before the tag does, so the pin lands as a second commit after the tag. Claude Code verifies the pin at install time and refuses a mismatch as `sha_pin_mismatch`; it clones by the pinned commit rather than by the tag, which is what keeps an installation on the reviewed release if the tag is ever moved.
- This is the first release that carries `hooks/release-check` and the archive `Next action` rule, so it is the first release either one governs.

### Verification

- `bash hooks/smoke-test` — passed on Ubuntu, macOS, and Windows GitHub Actions runners.
- `bash hooks/release-check .` — passed.
- `python3 evals/runner.py` — passed.
- TaskFlow Skill validator — passed.

## [1.0.5] — 2026-09-15

### Added

- A Git merge driver for `TaskFlowDocs/todo.md`, installed into the clone by `SessionStart`, so two task branches merge Todo by entry instead of by line.
- Deterministic Todo IDs derived from the goal (`TF-<yyyymmdd>-<6 hex>`), replacing the `TF-<date>-<max+1>` counter that made two branches cut from one base allocate the same ID.
- Session ids recorded in the selected task's `sessions.md`, and the macOS CI runner added to the hooks matrix.
- `CONTRIBUTING.md` working-branch rules and repository-documents guidance for personal rules.

### Fixed

- **Hooks no longer need a Python interpreter at all.** `hooks/python-runtime` and `TASKFLOW_PYTHON` are gone; every hook is POSIX shell with `awk` and `sed` at the bash 3.2 + BSD userland level.
- macOS portability: `sed`/`grep` patterns that relied on GNU-only `\|` and `\{n\}` no longer fail silently or vacuously, and the hooks parse under the bash 3.2 that macOS ships.
- `hooks/version` no longer archives a tracked document that has uncommitted changes, which had made `old/vN/` record the text that replaced the version instead of the version itself.
- `task progress` and `task complete` now require the same recorded approval as `task state in_progress`; previously an unapproved task could be completed step by step and archived.
- Windows launcher argument forwarding, and the repository-document index path and concurrency protections carried over from 1.0.4.

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
