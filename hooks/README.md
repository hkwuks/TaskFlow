# TaskFlow hooks

Lifecycle hooks for TaskFlow, arranged the way `obra/superpowers/hooks` is:
a flat `hooks/` directory with extensionless bash scripts, one hook JSON per
host, and a cross-platform launcher.

```text
taskflow/hooks/
├── README.md
├── hooks.json          # Claude Code wiring
├── hooks-codex.json    # Codex CLI wiring
├── hooks-codebuddy.json # CodeBuddy wiring
├── hooks-dsh.json      # dsh wiring
├── session-start       # SessionStart entry (extensionless bash)
├── session-record      # records the host session id in the selected task
├── install-merge-driver # configures the repo-local Todo merge driver
├── merge-todo          # the driver: merges TaskFlowDocs/todo.md by entry
├── summarize-state     # derives the state summary (shared logic)
├── repository-docs-context # syncs index metadata and derives routes
├── task                # explicit intake/promote/state/progress/complete edits
├── archive             # full archive transaction (incl. Todo update)
├── version             # atomic version transition (changed docs only)
├── reopen              # retrieve an achieved task
├── release-version     # write the eight mechanical release version literals
├── release-check       # version literals + marketplace pin agree
├── todo-check          # no merge in a commit or rev range dropped a Todo entry
├── run-hook.cmd        # cross-platform launcher (polyglot batch/bash)
├── smoke-test-windows.ps1 # Windows PowerShell/cmd lifecycle regression
└── smoke-test          # assert-style smoke tests
```

## Why this shape

- **Extensionless bash** so Claude Code's Windows auto-detection (prepends
  `bash` to any command containing `.sh`) never interferes.
- **`run-hook.cmd`** is a polyglot file: on Windows, `cmd.exe` runs the batch
  half and finds Git Bash from the active Git for Windows installation without
  falling through to WSL Bash; on Unix the `:` no-op makes it a bash no-op. One
  `command` value works on every OS for Claude Code. Windows requires Git for
  Windows Bash; the launcher fails visibly when it is unavailable.
- **No language runtime.** Every hook is POSIX shell using only `awk` and
  `sed`, at the bash 3.2 + BSD userland level that stock macOS ships. There is
  no interpreter to locate, validate, or fall back from: an interpreter that is
  missing, shimmed, or a different major version is a failure mode the plugin
  does not have. Hooks are written to the POSIX subset deliberately — no
  `declare -A`, no `mapfile`, no GNU-only `sed -i`.
- **One JSON per host** (`hooks.json` for Claude Code, `hooks-codex.json` for
  Codex CLI, `hooks-codebuddy.json` for CodeBuddy, `hooks-dsh.json` for dsh);
  Codex's `commandWindows` lets the codex file point at the same launcher on
  Windows. CodeBuddy substitutes `${CODEBUDDY_PLUGIN_ROOT}` and
  `${CLAUDE_PLUGIN_ROOT}` alike, so its file calls `bash` on `session-start`
  directly and skips the launcher. dsh runs the hook through its own Claude Code
  bridge and does *not* put `${CLAUDE_PLUGIN_ROOT}` in the environment, so its
  file sets the variable on the command line — see the dsh note under Install.

## Install

Install TaskFlow as a plugin from the repository marketplace — no file copying:

```bash
# Claude Code
claude plugin marketplace add hkwuks/TaskFlow     # or a local path
claude plugin install taskflow@taskflow

# Codex CLI
codex plugin marketplace add hkwuks/TaskFlow      # or a local path
codex plugin add taskflow@taskflow

# CodeBuddy Code CLI (not the CodeBuddy IDE client)
codebuddy plugin marketplace add hkwuks/TaskFlow  # or a local path
codebuddy plugin install taskflow@taskflow

# dsh (no marketplace; the repository root is the plugin package)
dsh plugin --profile web add dsh-taskflow         # or a local path
```

The plugin manifests (`.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`,
`.codebuddy-plugin/plugin.json`, and the two marketplace catalogs) wire the
SessionStart hook automatically:
- Claude Code auto-loads `hooks/hooks.json` (standard hooks file at the plugin
  root) and runs `run-hook.cmd session-start`.
- Codex loads the manifest's `hooks` → `hooks/hooks-codex.json`, which points
  at `session-start` via `${PLUGIN_ROOT}`.
- CodeBuddy loads the manifest's `hooks` → `hooks/hooks-codebuddy.json`, which
  runs `bash "${CODEBUDDY_PLUGIN_ROOT}/hooks/session-start"`. CodeBuddy's own
  bundled plugins use the `CODEBUDDY_` spelling, and it substitutes the
  `CLAUDE_` spelling too, so either resolves.
- dsh has no manifest and no marketplace entry. The package's `dsh/index.js`
  mounts `hooks/hooks-dsh.json` on dsh's Claude Code hook bridge at load time,
  and the command sets `CLAUDE_PLUGIN_ROOT` itself: the bridge substitutes that
  variable inside the command string but never exports it, and `session-start`
  chooses its output shape from the environment. Without the prefix the hook
  emits a top-level `additionalContext`, which the bridge's codec discards.

For a non-plugin (manual) install — e.g. running hooks from a checked-out copy
outside a plugin — the old wiring still works:

```jsonc
// .claude/settings.json  →  "hooks" key
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"<skill>/hooks/run-hook.cmd\" session-start",
            "shell": "bash"
          }
        ]
      }
    ]
  }
}
```

Codex CLI manual install — copy `hooks-codex.json` to `<repo>/.codex/hooks.json`
(or its `[hooks]` into `.codex/config.toml`) and set the absolute script path.

CodeBuddy manual install — put the same shape in `.codebuddy/settings.json`
(project) or `~/.codebuddy/settings.json` (user) and replace the plugin-root
variable with an absolute path. CodeBuddy runs SessionStart with `source` fixed
to `startup`; the shared matcher lists `startup` among its alternatives, so it
matches whatever the host sends.

dsh manual install — there is none to speak of: mounting the hook means mounting
a plugin. Add the repository as a bundle and let `dsh/index.js` do it.

## Scope / safety

- `session-start` synchronizes only deterministic routing metadata in
  `TaskFlowDocs/repository-docs/index.md` and, through `session-record`, writes
  one entry in the selected task's `sessions.md` session index, then injects
  derived routes/state. Both writes are append/update-only: `session-record`
  owns the session id, availability, timestamps, directories, and Task
  version/phase, while `Last completed`, `Next step`, and `Notes` stay
  Agent-owned. It never edits source policies, any other core task document,
  `TaskFlowDocs/achieved/`, or approval state.
  `task`, `archive`, `version`, and `reopen` are run **explicitly** by the
  Agent at the lifecycle point. `version` copies changed documents, retains
  their roots, and resets the Plan approval block for the new review cycle;
  it never grants approval.
- Rules and host event maps live in `../skills/taskflow/references/runtime.md`.
- `install-merge-driver` writes only repository-local, untracked Git state:
  `merge.taskflow-todo.driver` in the repository's own config and a
  `TaskFlowDocs/todo.md merge=taskflow-todo` line in `.git/info/attributes`. It
  never edits a tracked file or global config, is idempotent and silent, and is
  best-effort — a failure leaves the session unaffected. It is what makes two
  task branches merge `todo.md` by entry instead of by line; see
  `../skills/taskflow/references/runtime.md` for the two cases it resolves and
  the web-UI limit it does not.
- Lifecycle: `run-hook.cmd task intake <goal> [source]`, then `task promote`,
  `task state`, `task progress`, and `task complete`; append `--root <path>`
  when operating outside the current repository.
- Smoke: `bash smoke-test` (builds temporary TaskFlowDocs fixtures and, on
  Windows, runs the full lifecycle through PowerShell 5.1 + `run-hook.cmd` in
  a path containing spaces and Chinese characters).

Hosts without hooks run the base flow unchanged; hooks are optional.
