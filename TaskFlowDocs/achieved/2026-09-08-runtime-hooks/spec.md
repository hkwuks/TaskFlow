# Spec — Support host/harness hooks in TaskFlow
> Task version: v2
> Status: completed

## Objective and Success Criteria

Host/harness hooks are bounded helpers: they do mechanical bookkeeping on Todo triage metadata and inject derived context, but never write core documents or manufacture approval. The public claim flips from "no runtime interception" to "may coordinate with Claude Code and Codex host hooks under explicit rules". Hooks are an optimization, not a prerequisite: an unknown host without hooks still runs the original flow.

## Architecture Boundaries and Responsibilities

- `README.md` / `README.zh-CN.md`: positive bounded statement (host hooks allowed for bookkeeping + context with prohibitions) in the intro box, non-invasive table, comparison table, and project map.
- `taskflow/SKILL.md`: single pointer to `runtime.md`; remove "no hooks" implications; add "Host / harness hooks" near Supporting references and a Safety bullet.
- `taskflow/references/runtime.md` (new): the single owner of host-hook rules — definitions, supported-host event map, must/may-not list, single-command transitions, and folder layout.
- `taskflow/hooks/` (new, flat): extensionless bash scripts + per-host hook JSON + a cross-platform launcher, mirroring `obra/superpowers/hooks`.
  - `hooks.json` — Claude Code wiring; `hooks-codex.json` — Codex CLI wiring.
  - `session-start`, `summarize-state` — SessionStart entry + shared summary generator (extensionless bash).
  - `archive`, `version`, `reopen` — single-command transition scripts.
  - `run-hook.cmd` — polyglot batch/bash launcher that finds Git Bash on Windows (native on Unix).
  - `smoke-test` — assert-style smoke tests.
- Installed skill mirror updated together with the repo copies.

## Project Structure / Affected Files

- `README.md`, `README.zh-CN.md`
- `taskflow/SKILL.md`
- `taskflow/references/runtime.md` (new)
- `taskflow/hooks/README.md`
- `taskflow/hooks/hooks.json`, `taskflow/hooks/hooks-codex.json`
- `taskflow/hooks/run-hook.cmd`
- `taskflow/hooks/session-start`, `taskflow/hooks/summarize-state`
- `taskflow/hooks/archive`, `taskflow/hooks/version`, `taskflow/hooks/reopen`
- `taskflow/hooks/smoke-test`
- Installed mirror of the skill files.

## Interfaces, Data Flow, and Contracts

- Supported-host event map contract (two columns: Claude Code | Codex): SessionStart summary (both, `additionalContext`), PostToolUse guardrail (both), Stop/SubagentStop and PreCompact feedback (both), PermissionRequest guardrail (both, optional; never approves core writes).
- Script contract: extensionless bash; `session-start` reads the summary from `summarize-state` and emits the platform-appropriate context JSON field (Claude Code nested `hookSpecificOutput.additionalContext`, Cursor `additional_context`, Copilot/other top-level `additionalContext`), exactly like `obra/superpowers/hooks/session-start`.
- Cross-platform contract: Unix runs bash natively; Windows runs the same scripts through the polyglot `run-hook.cmd` which locates Git Bash. Codex `hooks-codex.json` uses `commandWindows` where desired. No Python or per-host runtimes are required for the hooks.
- Single-command transitions contract (in `runtime.md`): `archive`, `version`, and `reopen` are one shell command each under `taskflow/hooks/`. `archive` performs the full transaction — move the task directory to achieved, update the Todo item's `Task:` path and status to `done`, then verify both locations and root statuses — so the whole transaction is a single operation. Approval stays with the user; the commands never touch an `## Approval` block.

## Invariants and Compatibility

- Todo stays triage metadata only; a hook may update status/date/next but never duplicate task facts.
- Core documents (`prd.md`, `spec.md`, `plan.md`, `reference/index.md`) are Agent-written only under the approved Task version.
- Approval is never automated; `ready` still is not approval.
- Achieved tasks stay read-only; commands respect archive/reopen boundaries from T-006.
- Host event names are documented per the referenced Claude Code and Codex docs and marked version-sensitive.

## Validation and Error Semantics

- A hook that fails (nonzero exit, stderr) fails safe: no partial core writes; the Agent sees the error as a system reminder and recovers.
- A single-command archive that is interrupted leaves the task active and the Todo not `done`; the command's verify step reports the mismatch.

## Code and Test Constraints

- No change to core document formats. Verification is textual (grep removed claims) plus one runnable assert-style `smoke-test` that exercises `summarize-state` (empty), `session-start` (platform JSON), `archive` (happy path incl. Todo), `reopen`, and `version` (changed docs only).

## Design Decisions and Alternatives

- Chosen: flat `obra/superpowers/hooks` shape (extensionless bash + one JSON per host + `run-hook.cmd`), per the user's reference and the bash + Windows-variant selection.
- Rejected: per-host subfolders with python entry scripts (not the reference layout; python not selected).
- Chosen: core writes stay Agent-only even though a PermissionRequest hook could technically approve them.
- Chosen: shared logic in the scripts themselves; each host JSON only wires events.

## Open Questions

- None.
