# Host / harness hooks and single-command transitions

Read this reference when configuring TaskFlow on a host that supports lifecycle hooks (Claude Code, Codex CLI), or when running a TaskFlow transition as one command.

## What a host/harness hook is

A **host/harness hook** is a script or MCP-tool call that the Agent's host runs automatically at a lifecycle event (session start, a tool call, a turn stop, compaction). The host hands the hook one JSON event on stdin and the hook may reply with JSON to add context, block/annotate an action, or (on permission events) approve or deny. Hooks are deterministic and host-side; they do not run a second LLM by default, and they never see the model's reasoning.

Hooks are **optional optimization, not a prerequisite**. A host without hooks runs the exact same TaskFlow flow; the Agent itself performs every step a hook would have automated.

## Supported hosts (additive)

TaskFlow ships reference hook configs for:

| Host | Config location | Reference file |
| --- | --- | --- |
| Claude Code | plugin root `hooks/hooks.json` (auto-loaded standard hooks file), or `.claude/settings.json` for a manual install | `hooks/hooks.json` |
| Codex CLI | `.codex-plugin/plugin.json` (`hooks` entry → `hooks/hooks-codex.json`), or `<repo>/.codex/hooks.json` for a manual install | `hooks/hooks-codex.json` |

Install both hosts by command from the repository marketplace — no file copying:
`claude plugin marketplace add hkwuks/TaskFlow && claude plugin install taskflow@taskflow`;
`codex plugin marketplace add hkwuks/TaskFlow && codex plugin add taskflow@taskflow`
(a local directory path works in place of the GitHub owner/repo).

An environment running any other agent host needs no hooks: it continues with the base flow. Adding a new host later is additive — write one JSON plus (if needed) a launcher, reusing the extensionless bash scripts.

## Event map

| TaskFlow need | Claude Code | Codex CLI |
| --- | --- | --- |
| Session-start state summary (derived, non-authoritative) | `SessionStart` → `additionalContext` | `SessionStart` → `additionalContext` |
| Cross-platform launcher | `run-hook.cmd` (polyglot, finds Git Bash on Windows) | `commandWindows` in `hooks-codex.json` |
| Bookkeeping guardrail (never decides) | `PostToolUse` / `PostToolBatch` | `PostToolUse` |
| End-of-turn feedback | `Stop` / `SubagentStop` | `Stop` / `SubagentStop` |
| Pre-compaction summary | `PreCompact` | `PreCompact` |
| Optional permission guardrail (never approves core writes) | `PermissionRequest` | `PermissionRequest` |

Host event names and output fields are version-sensitive; check each host's current hooks reference when wiring a new release.

## Must / may-not

A hook MAY:
- update a `TaskFlowDocs/todo.md` item's triage metadata (status, priority, date, `Next`) — Todo is triage metadata only;
- inject a derived, clearly non-authoritative context summary (e.g. the SessionStart state summary);
- run one of the single-command transition scripts below.

A hook MUST NOT:
- create, rewrite, or delete `prd.md`, `spec.md`, `plan.md`, `reference/index.md`, or move anything under `TaskFlowDocs/achieved/` on its own;
- create or alter an `## Approval` block, or otherwise approve;
- duplicate promoted task facts into Todo or into any hook output;
- read secrets or carry sensitive payloads in hook output (both hosts spill oversized output to disk).

If a hook fails (nonzero exit or stderr), it must fail safe: no partial core writes. The host surfaces the error as a reminder; the Agent recovers.

## SessionStart state summary

Purpose: on session start or resume, give the Agent a compact, derived snapshot so it does not need to re-read the whole tree. The summary is **derived navigation** — never a source of task facts.

Reference scripts:
- `hooks/summarize-state` — reads `TaskFlowDocs/todo.md` and the active task dirs, prints a short summary (inbox items, active status, next Plan Step). Prints nothing when no TaskFlowDocs exists.
- `hooks/session-start` — SessionStart entry that wraps the summary into the platform's context field (Claude Code → `hookSpecificOutput.additionalContext`; Cursor → `additional_context`; Copilot/other → top-level `additionalContext`), mirroring the `obra/superpowers` session-start pattern.

Keep summaries short; both hosts cap oversized hook context (Claude Code caps at 10,000 chars and Codex spills past ~2,500 tokens). If nothing is present, print nothing.

Scripts are extensionless bash so Claude Code's Windows auto-detection (prepends `bash` to any command containing `.sh`) never interferes. On Windows, `hooks/run-hook.cmd` is a polyglot batch/bash wrapper that locates Git Bash; the same `command` value works on every OS for Claude Code, and Codex `hooks-codex.json` uses `commandWindows` where desired.

## Single-command transitions

Run by the Agent (or invoked by a hook) as one operation. They never touch approval.

| Command | Action | Verify after |
| --- | --- | --- |
| `hooks/archive <task-id>` | Move `TaskFlowDocs/<task-id>` → `TaskFlowDocs/achieved/<task-id>`, update the linked Todo item's `Task:` path and status to `done`, then verify the active path is absent, the achieved path exists, and the achieved root PRD and Plan both say `completed`. | Prints a check report; on any failure leaves the Todo not `done` and exits nonzero. |
| `hooks/reopen <task-id>` | Move `TaskFlowDocs/achieved/<task-id>` → `TaskFlowDocs/<task-id>`, record the Todo source/reopen reason in the Plan change log. | Prints a check report; exit nonzero on mismatch. |
| `hooks/version <task-id> <new-v>` | Archive only the changed core documents plus `version.md` into `old/v<old>/`, leave an unaffected Plan at the root, bump root docs to `<new-v>`. | Prints archived paths + root version agreement; exit nonzero on mixed versions. |

`archive` is a full transaction — it includes the Todo path/status update, so completing a task is truly one command. The Agent still records the `completed` status in the root PRD/Plan before invoking it and still owns every Approval record.

## Folder layout

```text
repo-root/
├── .claude-plugin/marketplace.json      # marketplace catalog (both hosts read it)
└── taskflow/
    ├── .claude-plugin/plugin.json       # Claude Code manifest (skills: ./)
    ├── .codex-plugin/plugin.json        # Codex CLI manifest (skills: ./)
    ├── SKILL.md
    ├── hooks/
    │   ├── README.md                    # install + run instructions for both hosts
    │   ├── hooks.json                   # Claude Code wiring (SessionStart; auto-loaded)
    │   ├── hooks-codex.json             # Codex CLI wiring (SessionStart)
    │   ├── run-hook.cmd                 # cross-platform launcher (polyglot batch/bash)
    │   ├── session-start                # SessionStart entry (extensionless bash)
    │   ├── summarize-state              # shared state-summary generator
    │   ├── archive                      # full archive transaction (incl. Todo update)
    │   ├── version                      # archive changed docs + version bump
    │   ├── reopen                       # retrieve an achieved task
    │   └── smoke-test                   # assert-style smoke tests
    └── references/                      # runtime.md, artifacts.md, versioning-and-recovery.md
```

This mirrors the `obra/superpowers/hooks` convention: flat directory, extensionless bash scripts, one hook JSON per host, and a cross-platform launcher — no per-host subfolders or non-bash runtimes. Shared logic lives in the scripts themselves; each host JSON only wires events to them.
