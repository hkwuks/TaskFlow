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
- maintain the selected task's `sessions.md` session index from the host event: one entry per session, limited to the session id, agent/platform, availability, started/last-active timestamps, code working directory, task artifact directory, and Task version/phase. `Last completed`, `Next step`, and `Notes` stay Agent-owned; the hook never creates the entry in another task, never touches `TaskFlowDocs/achieved/`, and never marks a session `closed`;
- run one of the single-command transition scripts below.

A hook MUST NOT:
- create, rewrite, or delete `prd.md`, `spec.md`, `plan.md`, `reference/index.md`, or move anything under `TaskFlowDocs/achieved/` on its own;
- create or alter an `## Approval` block, or otherwise approve;
- duplicate promoted task facts into Todo, `sessions.md`, or any hook output;
- read secrets or carry sensitive payloads in hook output (both hosts spill oversized output to disk).

If a hook fails (nonzero exit or stderr), it must fail safe: no partial core writes. The host surfaces the error as a reminder; the Agent recovers.

## SessionStart state summary

Purpose: on session start or resume, maintain the repository-document routing record and give the Agent compact derived routes/state. The index is authoritative for routing/check metadata; routed source documents remain authoritative for policy content.

Reference scripts:
- `hooks/summarize-state` — prints the selected active task and its next Plan Step by default. Set `TASKFLOW_TASK_ID` for explicit selection or `TASKFLOW_VERBOSE=1` to include the full Todo and active-task inventory. Ambiguous state is reported without guessing. Prints nothing when no TaskFlowDocs exists.
- `hooks/repository-docs-context` — atomically synchronizes deterministic index metadata for recognized sources and prints phase-filtered paths/status. It never edits source policies or core task documents.
- `hooks/session-start` — consumes the host event JSON, processes only `SessionStart`, uses its `cwd` for repository routing, and wraps the summary into the platform's context field (Claude Code → `hookSpecificOutput.additionalContext`; Cursor → `additional_context`; Copilot/other → top-level `additionalContext`).
- `hooks/session-record` — called by `session-start`; records the host `session_id` in the selected task's `sessions.md` (see the must/may-not list for the field boundary). Selection is the same as `summarize-state`: explicit `TASKFLOW_TASK_ID`, else the single active task; otherwise it writes nothing. It is best-effort — a failure never changes the SessionStart exit code or context output — and reports skipped or unparseable input on stderr only.

Keep summaries short; both hosts cap oversized hook context (Claude Code caps at 10,000 chars and Codex spills past ~2,500 tokens). If nothing is present, print nothing.

Scripts are extensionless bash so Claude Code's Windows auto-detection (prepends `bash` to any command containing `.sh`) never interferes. On Windows, `hooks/run-hook.cmd` is a polyglot batch/bash wrapper that locates Git Bash; the same `command` value works on every OS for Claude Code, and Codex `hooks-codex.json` uses `commandWindows` where desired.

Hooks carry no language runtime. Text work is done with `awk` and `sed` at the bash 3.2 + BSD userland level, which is the floor `2026-09-14-macos-hook-portability` established and which `tools/fixture-compare` protects: no `declare -A`, no `mapfile`, and no GNU-only `sed -i` may appear in a hook. The smoke suite runs the hooks against a curated `PATH` containing no interpreter, so a reintroduced runtime dependency fails CI rather than a user's session.

Windows uses the same Bash implementation through `run-hook.cmd`; PowerShell and `cmd.exe` do not maintain separate lifecycle logic. `hooks/smoke-test-windows.ps1` exercises the complete lifecycle through that launcher, including a repository path with spaces and Chinese characters.

## Single-command transitions

Run explicitly by the Agent as one operation. Only SessionStart summary injection is automatically wired; write commands never bind to `UserPromptSubmit`, `PostToolUse`, or `Stop`.

| Command | Action | Verify after |
| --- | --- | --- |
| `hooks/task intake <goal> [source] [--root <path>]` | Add one deduplicated Todo entry and allocate its ID. | Prints the Todo ID; duplicate goals fail before mutation. |
| `hooks/task promote <todo-id> <task-id> <small\|large> [--root <path>]` | Create minimal PRD/Plan and optional Spec scaffolds, then link the Todo. | Existing destinations and already-promoted items fail before mutation. |
| `hooks/task state <task-id> <state> [--root <path>]` | Update PRD/Plan state and Todo triage state. | `in_progress` requires approval for the current Task version. |
| `hooks/task progress <task-id> <step> <status> [verification] [--root <path>]` | Update one Plan Step and optionally append a verification line. | `done` rejects unchecked checklist items. |
| `hooks/task complete <task-id> --user-accepted [--root <path>]` | Validate completion gates, set core statuses, and invoke archive. | Requires explicit acceptance and leaves no active task on success. |
| `hooks/archive <task-id>` | Move `TaskFlowDocs/<task-id>` → `TaskFlowDocs/achieved/<task-id>`, update the linked Todo item's `Task:` path and status to `done`, then verify the active path is absent, the achieved path exists, and the achieved root PRD and Plan both say `completed`. | Prints a check report; on any failure leaves the Todo not `done` and exits nonzero. |
| `hooks/reopen <task-id>` | Move `TaskFlowDocs/achieved/<task-id>` → `TaskFlowDocs/<task-id>`, record the Todo source/reopen reason in the Plan change log. | Prints a check report; exit nonzero on mismatch. |
| `hooks/version <task-id> <new-v>` | Copy only changed core documents plus `version.md` into `old/v<old>/`, retain root docs, bump them to `<new-v>`, and reset state/approval for review. | Prints archived paths + root version/state agreement; exit nonzero before mutation on invalid input. |

`task complete` performs the validated completion plus the existing archive transaction. The Agent still owns semantic document content and every Approval record.

## Parallel branches and the Todo merge driver

`TaskFlowDocs/todo.md` is one file every task appends to, so two task branches merge-conflict there even when they touched nothing in common. TaskFlow ships a Git merge driver for it, so the two ordinary cases resolve without a human:

- two branches each added an entry — both entries survive;
- two branches changed different entries — both changes survive.

Two branches changing *the same* entry differently is still a real conflict and is left for review with ordinary conflict markers.

The wiring is per-clone and untracked: `merge.taskflow-todo.driver` in the repository's own Git config, plus a `TaskFlowDocs/todo.md merge=taskflow-todo` line in `.git/info/attributes`. `hooks/install-merge-driver` writes both, `hooks/session-start` calls it on every session start, and it is idempotent, `--local`-only, silent on success, and best-effort. Nothing tracked is edited, so a repository that has not adopted TaskFlow is unaffected; `hooks/merge-todo` is the driver itself.

Two limits are worth stating plainly:

- **Only local merges.** A hosted-platform merge (a pull request merged in the web UI) runs server-side and does not run a custom driver — Git does not ship the driver command to the server. It degrades to an ordinary content conflict, which is resolvable but manual. Merging the branches locally and pushing is what uses the driver.
- **Text, not semantics.** The driver matches entries by `- ID:` and falls back to the heading. Tasks that intentionally reuse an ID for different items are not detected as a conflict.

Because the web UI path has no driver, the driver's own invariant — a Todo entry is never deleted — is not enforced there by anything. `hooks/todo-check [repo-root] [commit]` is the read-only check for it: every `- ID:` a merge's parent commits held must still be present in the result, or the dropped entry is named along with the parent that held it (`0` pass, `2` dropped, `3` cannot tell). Run it explicitly, or once per merge commit to audit a range. Only the named commit's own parents are compared, so a push whose tip is clean passes even when an earlier merge in the same push dropped an entry.

Todo IDs are derived from the goal (`TF-<yyyymmdd>-<6 hex>` from a `cksum` digest), not from the highest existing ID. A shared counter makes two branches cut from the same base both allocate the day's first ID, and a merge that keeps both entries then leaves two entries claiming one ID — no merge strategy can repair that, because the ambiguity is in the content. Deriving the ID makes the branches agree instead.

## Folder layout

```text
repo-root/
├── .claude-plugin/marketplace.json      # marketplace catalog (both hosts read it)
└── taskflow/
    ├── .claude-plugin/plugin.json       # Claude Code manifest (skills: ./skills/)
    ├── .codex-plugin/plugin.json        # Codex CLI manifest (skills: ./skills/)
    ├── skills/taskflow/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/                  # runtime.md, artifacts.md, versioning-and-recovery.md
    └── hooks/
        ├── README.md                    # install + run instructions for both hosts
        ├── hooks.json                   # Claude Code wiring (SessionStart; auto-loaded)
        ├── hooks-codex.json             # Codex CLI wiring (SessionStart)
        ├── run-hook.cmd                 # cross-platform launcher (polyglot batch/bash)
        ├── session-start                # SessionStart entry (extensionless bash)
        ├── session-record               # records the host session id in the task index
        ├── install-merge-driver         # configures the repo-local Todo merge driver
        ├── merge-todo                   # the driver: merges todo.md by entry
        ├── repository-docs-context      # syncs index metadata + derives routes
        ├── task                         # explicit intake/promote/state/progress/complete
        ├── summarize-state              # shared state-summary generator
        ├── archive                      # full archive transaction (incl. Todo update)
        ├── version                      # archive changed docs + version bump
        ├── reopen                       # retrieve an achieved task
        ├── release-check                # version literals + marketplace pin agree
        ├── todo-check                   # no parent commit's Todo entry is missing from a merge
        ├── smoke-test-windows.ps1       # PowerShell/cmd full lifecycle regression
        └── smoke-test                   # assert-style smoke tests
```

This mirrors the `obra/superpowers/hooks` convention: flat directory, extensionless bash scripts, one hook JSON per host, and a cross-platform launcher — no per-host subfolders or non-bash runtimes. Shared logic lives in the scripts themselves; each host JSON only wires events to them.
