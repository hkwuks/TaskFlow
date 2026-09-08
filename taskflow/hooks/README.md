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
  half and finds Git Bash; on Unix the `:` no-op makes it a bash no-op. One
  `command` value works on every OS for Claude Code.
- **One JSON per host** (`hooks.json` for Claude Code, `hooks-codex.json` for
  Codex CLI); Codex's `commandWindows` lets the codex file point at the same
  launcher on Windows.

## Install

Claude Code (project settings or plugin `hooks` entry):

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

Codex CLI — copy `hooks-codex.json` to `<repo>/.codex/hooks.json` (or its
`[hooks]` into `.codex/config.toml`) and set the absolute script path.

## Scope / safety

- `session-start` only prints a derived, non-authoritative summary; it writes
  nothing. `archive`, `version`, and `reopen` are run **explicitly** by the
  Agent at the lifecycle point and never touch an approval block.
- Rules and host event maps live in `../references/runtime.md`.
- Smoke: `bash smoke-test` (builds a temp TaskFlowDocs and exercises
  archive → reopen → version).

Hosts without hooks run the base flow unchanged; hooks are optional.
