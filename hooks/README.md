# TaskFlow hooks

Lifecycle hooks for TaskFlow, arranged the way `obra/superpowers/hooks` is:
a flat `hooks/` directory with extensionless bash scripts, one hook JSON per
host, and a cross-platform launcher.

```text
taskflow/hooks/
├── README.md
├── hooks.json          # Claude Code wiring
├── hooks-codex.json    # Codex CLI wiring
├── session-start       # SessionStart entry (extensionless bash)
├── summarize-state     # derives the state summary (shared logic)
├── archive             # full archive transaction (incl. Todo update)
├── version             # atomic version transition (changed docs only)
├── reopen              # retrieve an achieved task
├── run-hook.cmd        # cross-platform launcher (polyglot batch/bash)
└── smoke-test          # assert-style smoke tests
```

## Why this shape

- **Extensionless bash** so Claude Code's Windows auto-detection (prepends
  `bash` to any command containing `.sh`) never interferes.
- **`run-hook.cmd`** is a polyglot file: on Windows, `cmd.exe` runs the batch
  half and finds Git Bash from the active Git for Windows installation without
  falling through to WSL Bash; on Unix the `:` no-op makes it a bash no-op. One
  `command` value works on every OS for Claude Code.
- **Python** is used only for small Markdown edits. Scripts prefer `python3`
  and fall back to `python` when the WindowsApps `python3` shim is not runnable.
- **One JSON per host** (`hooks.json` for Claude Code, `hooks-codex.json` for
  Codex CLI); Codex's `commandWindows` lets the codex file point at the same
  launcher on Windows.

## Install

Install TaskFlow as a plugin from the repository marketplace — no file copying:

```bash
# Claude Code
claude plugin marketplace add hkwuks/TaskFlow     # or a local path
claude plugin install taskflow@taskflow

# Codex CLI
codex plugin marketplace add hkwuks/TaskFlow      # or a local path
codex plugin add taskflow@taskflow
```

The plugin manifests (`.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`,
and the repo-root marketplace) wire the SessionStart hook automatically:
- Claude Code auto-loads `hooks/hooks.json` (standard hooks file at the plugin
  root) and runs `run-hook.cmd session-start`.
- Codex loads the manifest's `hooks` → `hooks/hooks-codex.json`, which points
  at `session-start` via `${PLUGIN_ROOT}`.

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

## Scope / safety

- `session-start` only prints a derived, non-authoritative summary; it writes
  nothing. `archive`, `version`, and `reopen` are run **explicitly** by the
  Agent at the lifecycle point. `version` copies changed documents, retains
  their roots, and resets the Plan approval block for the new review cycle;
  it never grants approval.
- Rules and host event maps live in `../references/runtime.md`.
- Smoke: `bash smoke-test` (builds a temp TaskFlowDocs and exercises
  archive → reopen → version).

Hosts without hooks run the base flow unchanged; hooks are optional.
