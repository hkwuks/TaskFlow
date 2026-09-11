# Support host/harness hooks in TaskFlow
> Task version: v2
> Status: completed

## Goal

Allow TaskFlow to coordinate with host/harness hooks — Claude Code and Codex CLI — so routine bookkeeping and transitions become fewer, cheaper operations, while keeping every decision record and approval gate intact. Reversing the earlier "non-runtime, no interception" claim is an explicit, user-selected decision, and TaskFlow now names the host hook surfaces it supports instead of promising none.

## Background / Confirmed Facts

- TaskFlow's README (EN/zh), skill, and comparison table currently claim "not an Agent runtime", "does not intercept prompts, tool calls, or model behavior", and "no runtime hooks".
- Claude Code and Codex CLI each ship an extensibility-hook mechanism. Both are host-side, deterministic scripts (or MCP tool calls) that receive a JSON event on stdin and can add context, block/annotate a tool call, or approve/deny a permission prompt. Neither hook runs another LLM in the loop by default; they are bookkeeping + guardrail + context-injection surfaces.
- Host hooks fire on lifecycle events (SessionStart/SessionEnd, PreToolUse/PostToolUse, PermissionRequest, Stop/SubagentStop, PreCompact). A SessionStart hook's stdout (Claude Code) or `additionalContext` (both) is injected at conversation start, which is the right place for a cheap TaskFlow state summary.
- Host hooks cannot see or edit the model's reasoning; they operate on tool-call metadata and files.
- Claude Code bundles hooks via `.claude-plugin/plugin.json` (`hooks` entry, hook files under `claude-hooks/` or `hooks/`); Codex bundles hooks via `.codex-plugin/plugin.json` and defaults to `hooks/hooks.json`, and also discovers repo-level `<repo>/.codex/hooks.json` or `[hooks]` in `<repo>/.codex/config.toml`. Plugins commonly ship per-host hook folders (`.claude-plugin/` vs `.codex-plugin/`) plus shared `scripts/`.
- T-006 (achieved 2026-09-08) already made lifecycle rules single-sourced, added Plan change-log revisions, tightened version triggers, and reduced `old/` archival. This task builds on that foundation.

## Requirements

1. Reverse the "non-runtime / no interception" claim in README EN, README zh-CN, and the skill; state that TaskFlow may coordinate with host/harness hooks under explicit rules.
2. Name the two supported hosts and their hook-config locations, and keep the host list additive: an unknown host that has no hooks simply runs the original flow (hooks are optional optimization, not a prerequisite).
3. Provide hook scripts and per-host wiring under the skill following the `obra/superpowers/hooks` convention: a flat `hooks/` directory of extensionless bash scripts, one hook JSON per host, and a cross-platform launcher (`run-hook.cmd`), so the same scripts run on macOS/Linux/Windows.
4. Document a SessionStart state-summary hook for each host: scans `TaskFlowDocs/todo.md` + active task dirs and injects a short, derived, non-authoritative summary.
5. Hooks may update `TaskFlowDocs/todo.md` triage metadata (an item's status/date/next) because Todo is triage metadata only.
6. Hooks must NOT create, rewrite, or delete `prd.md`, `spec.md`, `plan.md`, `reference/index.md`, or their `old/`/`achieved/` transitions on their own. Core-document writes stay with the Agent under the approved Task version and recorded approval.
7. A hook may append non-authoritative context to a turn as long as it is clearly derived navigation, not a source of task facts.
8. Land single-command transitions (one archive command, one version command, one reopen command) that an Agent runs to move a task; `archive` is a full transaction that also updates the linked Todo path/status.
9. Keep every approval gate: a hook must not bypass or fabricate an approval record.
10. Keep Todo as triage metadata only; hooks updating Todo must not duplicate promoted task facts.

## Acceptance Criteria

- README EN/zh and the skill no longer claim "non-runtime" or "no hooks"; each says hooks are allowed for bounded bookkeeping and context with explicit prohibitions, and names Claude Code + Codex CLI as supported hosts with an additive rule for others.
- `taskflow/references/runtime.md` exists and defines: what a host/harness hook is, the supported-host event map (Claude Code and Codex columns), and a must/may-not list.
- `taskflow/hooks/` exists in the `obra/superpowers/hooks` shape: flat directory, extensionless bash scripts, one hook JSON per host (`hooks.json`, `hooks-codex.json`), `run-hook.cmd` cross-platform launcher, and `session-start` + `summarize-state`.
- Cross-platform: the hooks are bash run through the polyglot `run-hook.cmd` on Windows (Git Bash) and natively on Unix; no per-OS python runtimes required. (User selection: bash + Windows variant, not Python.)
- Single-command archive/version/reopen transitions are delivered as scripts with an assert-style `smoke-test`.
- No wording anywhere permits a hook to write core documents or fabricate approval.
- The task's own Todo item T-20260908-007 is promoted and linked.

## In Scope

- Documentation edits across README EN/zh, `taskflow/SKILL.md`, and new `taskflow/references/runtime.md`.
- Reference hook scripts under `taskflow/hooks/` (flat, extensionless bash + `run-hook.cmd` + per-host JSON) with a runnable SessionStart summary and single-command transitions, plus an assert-style smoke test.
- Mirroring edited skill files to the installed skill copy.

## Out of Scope

- Actually installing hooks in `.claude/settings.json` / `.codex/config.toml` for this repository (a deployment decision; documented, not executed).
- Changes to core document formats, Todo intake, approval semantics, phase state machine, or task directory locations.
- Any mechanism that lets a hook auto-approve, auto-version, or auto-archive.
- Full Codex prompt/agent hook handlers (Codex parses but skips them in the current release); only `command` and `mcp_tool` handlers are documented.

## Risks / Deferred Items

- Reversing the boundary could invite over-automation; mitigated by the explicit prohibitions and by keeping core writes Agent-only.
- `additionalContext` injection adds tokens (a summary); this is the accepted trade for cheap resume context, and both hosts cap large hook output.
- Host hook schemas drift between releases; the reference pins event names to the current Claude Code and Codex docs and marks them as version-sensitive.

## Open Questions

- None blocking.

## Version History

- v1: Support host/harness hooks (Claude Code + Codex), per-host hook folders, SessionStart summary, single-command transitions; reverse the non-runtime claim; hooks never write core documents or approve.
- v2: Per-host subfolders and python scripts replaced by the flat `obra/superpowers/hooks` shape (extensionless bash, one JSON per host, `run-hook.cmd`), per user reference and the user's bash+Windows selection; `archive` includes the Todo update.
