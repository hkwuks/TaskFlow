# Host / harness hooks and single-command transitions

Read this reference when configuring TaskFlow on a host that supports lifecycle hooks (Claude Code, Codex CLI, CodeBuddy, dsh, Trae), or when running a TaskFlow transition as one command.

## What a host/harness hook is

A **host/harness hook** is a script or MCP-tool call that the Agent's host runs automatically at a lifecycle event (session start, a tool call, a turn stop, compaction). The host hands the hook one JSON event on stdin and the hook may reply with JSON to add context, block/annotate an action, or (on permission events) approve or deny. Hooks are deterministic and host-side; they do not run a second LLM by default, and they never see the model's reasoning.

Hooks are **optional optimization, not a prerequisite**. A host without hooks runs the exact same TaskFlow flow; the Agent itself performs every step a hook would have automated.

## Supported hosts (additive)

TaskFlow ships reference hook configs for:

| Host | Config location | Reference file |
| --- | --- | --- |
| Claude Code | plugin root `hooks/hooks.json` (auto-loaded standard hooks file), or `.claude/settings.json` for a manual install | `hooks/hooks.json` |
| Codex CLI | `.codex-plugin/plugin.json` (`hooks` entry → `hooks/hooks-codex.json`), or `<repo>/.codex/hooks.json` for a manual install | `hooks/hooks-codex.json` |
| CodeBuddy | `.codebuddy-plugin/plugin.json` (`hooks` entry → `hooks/hooks-codebuddy.json`), or `.codebuddy/settings.json` for a manual install | `hooks/hooks-codebuddy.json` |
| dsh | the plugin package's `dsh/index.js` mounts `hooks-dsh.json` through dsh's Claude Code hook bridge; the bundle patch is what pulls the package in | `hooks/hooks-dsh.json` |
| Trae | `hooks/hooks-trae.json` is Trae's own `hooks.json` format, copied to `<project>/.trae/hooks.json` at install time (or `~/.trae-cn/hooks.json` for a global install). Trae has no plugin marketplace a repository can publish to | `hooks/hooks-trae.json` |

Install every host by command from the repository marketplace — no file copying:
`claude plugin marketplace add hkwuks/TaskFlow && claude plugin install taskflow@taskflow`;
`codex plugin marketplace add hkwuks/TaskFlow && codex plugin add taskflow@taskflow`;
`codebuddy plugin marketplace add hkwuks/TaskFlow && codebuddy plugin install taskflow@taskflow`
(a local directory path works in place of the GitHub owner/repo). dsh has no marketplace
and the package is on no registry: its command names the Git repository and pins the full
commit — `dsh plugin --profile <name> add github:hkwuks/TaskFlow#<40-character-sha>` — with
the sha taken from the release tag, which is the same commit the marketplace catalogs pin.
A local directory path works there too. Trae has neither a
marketplace nor a plugin command: its install is the copy above, described in
`hooks/README.md`, and Trae also reads Claude Code hook configs when the user turns on
**导入 CLAUDE 中的 Hooks 配置**.

The three marketplace hosts expose plugin management as shell subcommands of their own CLI. CodeBuddy
Code is a separate binary from the CodeBuddy IDE client; the IDE client does not implement
`plugin` commands, so the CLI is required to install or validate the plugin.

An environment running any other agent host needs no hooks: it continues with the base flow. Adding a new host later is additive — write one JSON plus (if needed) a launcher, reusing the extensionless bash scripts.

## Event map

| TaskFlow need | Claude Code | Codex CLI | CodeBuddy | dsh | Trae |
| --- | --- | --- | --- | --- | --- |
| Session-start state summary (derived, non-authoritative) | `SessionStart` → `additionalContext` | `SessionStart` → `additionalContext` | `SessionStart` → `hookSpecificOutput.additionalContext` | `agent/session-start` → `hookSpecificOutput.additionalContext` | `SessionStart` → `hookSpecificOutput.additionalContext` |
| Per-prompt in-flight task reminder (derived, non-authoritative) | `UserPromptSubmit` → `hookSpecificOutput.additionalContext` | `UserPromptSubmit` → `hookSpecificOutput.additionalContext` (added as developer context) | `UserPromptSubmit` → `hookSpecificOutput.additionalContext` | `agent/pre-step` → the bridge runs the configured `UserPromptSubmit` command, so the same event name and envelope | `UserPromptSubmit` → `hookSpecificOutput.additionalContext` |
| Cross-platform launcher | `run-hook.cmd` (polyglot, finds Git Bash on Windows) | `commandWindows` in `hooks-codex.json` | `run-hook.cmd` is not needed; `hooks-codebuddy.json` calls `bash` directly | `run-hook.cmd`, reached through dsh's `bash -c` seam | `run-hook.cmd` behind an explicit `bash`; no `commandWindows` equivalent, so Windows uses `& '<path>\hooks\run-hook.cmd'` |
| Bookkeeping guardrail (never decides) | `PostToolUse` / `PostToolBatch` | `PostToolUse` | `PostToolUse` | `tools/post-execute` | `PostToolUse` |
| End-of-turn feedback | `Stop` / `SubagentStop` | `Stop` / `SubagentStop` | `Stop` / `SubagentStop` | `agent/turn-stopping` / `subagent/end` | `Stop` (with `loop_limit`); no subagent tool event |
| Pre-compaction summary | `PreCompact` | `PreCompact` | `PreCompact` | none (dsh emits `compact` as a SessionStart source) | none (Trae's SessionStart source is only `startup`) |
| Optional permission guardrail (never approves core writes) | `PermissionRequest` | `PermissionRequest` | `PreToolUse` | `tools/pre-execute` | `PreToolUse` |
| Pre-write capability gate on a stage document (deny only) | `PreToolUse` (`Write`, `Edit`) → deny | `PreToolUse` (`apply_patch`) → deny; real host unverified | `PreToolUse` (`Write|Edit`) → deny | `PreToolUse` (`write|edit|apply_patch`) → deny; real host unverified | `PreToolUse` (`Write|Edit`) → deny |
| Capability-call capture (feeds the gate) | `PostToolUse` (`Skill`, `Agent|Task`, `mcp__.*`) | `PreToolUse` / `PostToolUse` (`mcp__.*`); session and call IDs unverified | `PostToolUse` (`Skill`, `Agent|Task`, `mcp__.*`) | `PostToolUse` (`skill`, `mcp__.*`); real host unverified | `PostToolUse` (`Skill`, `mcp__.*`) — Trae has no `Agent`/`Task` tool |
| External-lookup capture (never releases a stage) | `PostToolBatch` (no matcher) | `PostToolUse` (no matcher) — real host unverified | `PostToolUse` (no matcher) — `tool_response` not confirmed | `PostToolUse` (no matcher) — real host unverified | `PostToolUse` (no matcher) — `tool_response` not confirmed |

Host event names and output fields are version-sensitive; check each host's current hooks reference when wiring a new release. The gate's contract was measured against **Claude Code 2.1.282** on 2026-09-27 rather than assumed: `Skill` fires both `PreToolUse` and `PostToolUse`, its `tool_input.skill` carries the capability name, and `PreToolUse` fires for `Edit`. That measurement covers `Skill` only — that `Agent`/`Task` and `mcp__.*` reach `PostToolUse` the same way is inferred from the same tool-call lifecycle, not measured. The Trae column is documented, not measured — see **Trae specifics** below. The CodeBuddy columns come from the packaged CLI rather than from a running session, and the Codex and dsh columns from Codex's own hook documentation (read 2026-10-29) and measured payloads respectively — **CodeBuddy specifics**, **Codex specifics** and **dsh specifics** below each state which standing they hold.

An event that is not wired is an outstanding integration gap. Mark a capability not supported only when host evidence establishes the missing mechanism; an untested host is neither proof of support nor proof of absence.

**External-lookup capture is recorded by URL, not by tool name, and is documented
rather than measured.** The predicate is "did this event carry an absolute
`http(s)` URL", scanned over the whole event text — both `tool_input` and
`tool_response` — so it covers `WebSearch`, `WebFetch`, any MCP server, and any
CLI a Skill runs through `Bash` (`dg`, `tvly`, `sxng`, `curl`) without naming a
tool. That is deliberate: the host exposes no "this tool searches" class, and
the 1.1.10 wiring — a `WebSearch|WebFetch` matcher — was a product list, which
R3 of the pre-write gate forbids and which measurably missed every lookup that
went through a redirected or MCP path.

The Claude Code wiring uses `PostToolBatch`, whose reference (read 2026-11-02,
level: documented, not measured) describes it as firing once after every tool
call in a batch resolves, with no matcher, carrying `tool_calls[]` where each
entry has `tool_name`, `tool_input` and `tool_response`. The other hosts wired
above have no batch event, so they use `PostToolUse` with no matcher (omit the
matcher or set `"*"` to match every tool). On CodeBuddy and Trae the `tool_input`
fields are the documented Claude Code ones but `tool_response` has not been
confirmed; if it is absent there, the recorder still sees URLs in the arguments
and misses URLs that appear only in results. Codex's own hooks documentation
(read 2026-11-02) gives `tool_name` as `Bash`, `apply_patch` or `mcp__fs__read`
with a `tool_response` per tool, and lists no batch event. The dsh bridge also
forwards `PostToolUse` arguments and response text; its tool name does not affect
the URL scanner. The new wiring has not been measured in a real dsh session.

The gate reads `tool_input.file_path` for edits and `tool_input.command` or `tool_input.input` for patches. A host whose events have another shape must not be reported as protected until that shape has been verified and handled.

The recorder accepts `Skill`, dsh's `skill`, `Agent`/`Task`, and `mcp__*`. Trae has no `Agent`/`Task` tool, so that evidence path exists only where the host does.

## Base checkout edit guard

An explicit user-issued `base-document-permit` can authorize one observable edit of named document paths in the base checkout; see `hooks/README.md` for supported paths, cancellation and limitations. The permit cannot prove who issued it and does not replace user authorization.

`base-write-gate` checks the target Git worktree before observable file edits: the base checkout of a repository containing `TaskFlowDocs/todo.md` is denied, while a linked worktree and direct Todo intake are allowed. The guard runs first inside `capability-gate`, preventing a denied edit from spending stage evidence. dsh uses lowercase `write`/`edit` and `apply_patch` (`tool_input.input`); its wiring has not been tested in a real dsh session. Existing host caveats about trusted hooks and event shapes still apply.

The check is a guardrail, not a filesystem boundary: shell commands, interactive input, specialized tools that do not emit these events, symlink and hardlink targets and untrusted or disabled hooks can bypass it. On Windows, a test of an MXC profile with the base read-only and the nested worktree writable still allowed a write through a worktree hardlink to change the base file. This is one local fixture result, not a cross-platform claim. A release editing the base checkout through these file tools may be refused; release exceptions are tracked in TF-20261109-ccbb96. It never rolls back another process's writes.

Codex and Claude Code run `base-status-reminder` asynchronously after shell calls. It reports a dirty base checkout outside Todo without attributing changes to the command or Agent. It stores no snapshot and may repeat warnings for pre-existing changes; ignored files and changes gone before the check are missed. A failed status check is reported as unknown. Claude Code's official hooks reference says async output is delivered to the Agent on a later turn, not displayed directly to the user (https://code.claude.com/docs/en/hooks#run-hooks-in-the-background); this wiring has not been tested in a real Claude Code session. Other hosts are not wired for this reminder until their asynchronous event and output behavior is verified. Codex requires a trusted, enabled hook.

## Pre-write capability gate

Before a phase invocation, select the task, stage and session using `bash <installed-taskflow>/hooks/capability-context stage <worktree> <task-id> <PRD|Spec|Plan|Test> <session-id>`. SessionStart supplies the current session ID when the host provides it. The PreToolUse hook captures the phase at call start; PostToolUse records a successful call against that snapshot. Evidence rows include capability, task, version, stage and session. A gate release must match all of them and cannot reuse a line already spent. Older unbound evidence is preserved and cannot release a new stage. The Test stage has no document gate; release its matching invocation with `capability-context release-test <worktree> <task-id> <session-id>`.

A host that does not expose a matching session ID and tool-call ID cannot supply independently observed evidence through this path. If a capability was actually used but could not be observed, use `hooks/task declared <stage> --capability <name>`; if no capability applies, `hooks/task unaided <stage> --considered "<concept class>"` records that decision. These are explicit statements, not independent proof of a call. Worktree handoff snapshots the evidence, release, declaration, context and pending-call ledgers. Existing ledgers are retained; do not delete them to satisfy a gate.

The gate only sees supported file-edit events, not shell writes. It resolves paths from the event and denies rather than grants access. On Windows it normalizes path separators. A release ledger whose highest sequence exceeds the evidence length is refused; `hooks/task recover` preserves recoverable rows and records discarded rows. A length check cannot prove that unconsumed rows were not altered. Events reporting a subagent `agent_id` are not attributed, because the selected context belongs to the parent session; a real unobservable use can be declared explicitly. The ledger lock is nonblocking: a concurrent hook may fail to record a call rather than delay it; use `declared` only when the call actually happened. Host event shapes and real-session behavior still need verification; synthetic tests alone do not establish it.

### Codex specifics

Codex edits files with `apply_patch`, so the gate's input there is the patch text
under `tool_input.command` and there is no `file_path` field at all. Three
properties of that shape are load-bearing, all from Codex's own hooks
documentation read on 2026-10-29:

- **The matcher takes `Edit`/`Write` as aliases, but the event does not.** Aliasing
  chooses which hook runs; the hook input still reports
  `tool_name: "apply_patch"`. `capability-gate` therefore compares the name
  exactly and has no alias arm — one would be a branch nothing can reach.
- **The patch text is the only place the paths are.** `capability-gate` reads the
  four directives that name a target — `*** Update File:`, `*** Add File:`,
  `*** Delete File:`, `*** Move to:` — and judges each path with the same rule
  the `file_path` shape uses. A move is `Update File: <old>` plus `Move to: <new>`,
  so both ends are judged: the document really does leave one task and arrive at
  another, and reading only the destination would leave the departure unchecked.
- **A patch with no recognizable directive is refused, not allowed.** An empty
  command is the one exception — no edit happened. Everything else is a gate that
  cannot read its host, and allowing it would be the failure this wiring exists to
  fix. The refusal names the format as the problem.

**This host is documented, not measured.** No real Codex has run this wiring, so
the column above says so, and it stays that way until a session on a real machine
confirms the deny reaches the agent — including one `*** Move to:` case, because
the destination's spelling is the part the documentation leaves least clear.

Codex MCP `PreToolUse` and `PostToolUse` are wired to the capability recorder; real event identity fields remain unverified. `SubagentStart` alone cannot provide the paired tool-call snapshot and is not attributed. A file read or edit
does not prove a Skill invocation; use the explicit declaration for actual Skill
use when no independent host event is observable. Real-host delivery remains
to be verified.

### dsh specifics

dsh runs the hook through its own first-party Claude Code bridge
(`@deepseek-ai/dsh-hooks-claude-code`), which translates each Claude Code event
onto a dsh interception seam. Four details differ, and each was measured against
an installed dsh rather than assumed:

- **Plugin root is not exported.** The bridge substitutes `${CLAUDE_PLUGIN_ROOT}`
  inside the `command` string at config-parse time and exports only
  `CLAUDE_PROJECT_DIR`. `hooks-dsh.json` therefore sets `CLAUDE_PLUGIN_ROOT` on
  the command line (`CLAUDE_PLUGIN_ROOT='${CLAUDE_PLUGIN_ROOT}' bash ...`), because
  dsh's shell seam runs `bash -c` and honours a `VAR=value` prefix. Without it
  `session-start` takes its fallback branch, emits a top-level
  `additionalContext`, and the bridge's codec discards it silently.
- **SessionStart sources.** dsh emits `startup`, `resume`, `clear`, or `compact`.
  There is no `fork`, so the dsh matcher omits it; the other four match the shared
  script unchanged.
- **No plugin manifest.** dsh has no per-host manifest file. The repository root
  is the plugin package, and `dsh/index.js` mounts `hooks-dsh.json` on the bridge
  at load time. The file name is therefore a TaskFlow choice, not a host
  convention, and nothing outside `dsh/index.js` reads it.
- **Tool names are lowercase, and the bridge does not translate them.** The
  gate and recorder now recognize dsh's `write`, `edit`, `apply_patch` and
  `skill` forms, and the bridge forwards tool arguments. The current wiring has
  synthetic-event coverage but has not been measured in a real dsh session;
  explicit Skill injection need not produce a `skill` tool event.

### CodeBuddy specifics

CodeBuddy follows the Claude Code hook contract closely enough that `session-start` needs no host branch, but three details differ from the table above. The first two were executed against the packaged CLI, on 2026-10-11, by unpacking `@tencent-ai/codebuddy-code@2.137.0` and reading the shipped bundle; the third is from the docs alone, and is labelled as such below:

- **Tool names are the PascalCase ones.** The hook manager filters a tool's descriptors with `ToolNames.SKILL`, and the tool-name enum carries `READ="Read"`, `WRITE="Write"`, `EDIT="Edit"`, `MULTI_EDIT="MultiEdit"`, so `Write`/`Edit` are the names `PreToolUse` sees and the `Write|Edit` matcher is a correct pattern. The lowercase vocabulary that appears in a second, older documentation surface (`write_to_file`, `replace_in_file`, `execute_command`) is a different family's naming: those strings reach the bundle only as **telemetry aliases** (`case "Write": case "write-to-file": case "WriteToFile":` all collapse to the same metric key), never as an event's `tool_name`. A build that emitted them would have to send a name the host itself never matches against a tool.
- **The write path is `tool_input.file_path`.** `PermissionUtils` reads `ed.file_path` for `Read`, `Write`, `Edit` and `MultiEdit`, and the code that builds a file event does `el.file_path && (ec["file.path"] = el.file_path)` for both `Write` and the aliases above. The camelCase `filePath` in the SDK page is likewise a parameter name inside a hook callback, not a wire field.
- **Plugin root.** CodeBuddy injects both `${CODEBUDDY_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_ROOT}` with the same value, and substitutes both spellings in a hook command. `hooks-codebuddy.json` uses the `CODEBUDDY_` spelling, which is what every bundled plugin in the official marketplace writes.
- **Context field.** `session-start` chooses its output shape from the environment: with `CLAUDE_PLUGIN_ROOT` set it emits the `hookSpecificOutput` envelope, and without it the bare `additionalContext` object. That branch is this repository's own code and either arm can be run locally; since CodeBuddy injects both root variables, the plugin takes the envelope arm.

Two further facts about this host belong here because they change what "installed" means, and both are documented rather than measured:

- **SessionStart source.** CodeBuddy runs SessionStart with `source` fixed to `startup`. The shared `startup|resume|clear|compact` matcher lists `startup` among its alternatives, so it matches a host that only ever sends that one value.
- **The panel is the gate.** Hooks the user did not register through `/hooks` are not trusted — the docs call the panel "the authoritative entry point" and say external file edits need confirming there before taking effect. A plugin's `hooks/hooks.json` is exempt from the frontmatter gate that guards Agent/Skill-declared hooks, but not from that review. So wiring the gate pair here does not mean it runs: the install notes carry the confirmation step.

`.codebuddy-plugin/` names the host's own manifest and catalog explicitly, so the two entry points are visible in the tree rather than inferred from `.claude-plugin/`.

### Trae specifics

**Nothing in this subsection has been run on a live Trae host.** Every statement is
from `docs.trae.cn` as read on 2026-10-09, which is a different standing from the
Claude Code 2.1.282 measurement and the dsh notes above — those were executed
against an installed host, this was read. It is written down anyway because the
wiring ships, and shipping it unlabelled would be worse than shipping it labelled.
The first run on Trae either confirms it or corrects it.

- **No plugin mechanism.** Trae's marketplace is a curated in-app catalog with no
  documented way for a repository to publish an entry, and there is no
  `trae plugin …` command. What a project gets is `$PROJECT_FOLDER/.trae/skills/`
  and `$PROJECT_FOLDER/.trae/hooks.json`; the global pair is `~/.trae-cn/hooks.json`
  and `~/.trae-cn/skills/`. TaskFlow's install is therefore a copy
  (`hooks/README.md` has the commands), which is also what the other Trae
  integrations do — `mnemon` and ARIS both deploy by copying into `.trae/`.
- **Identifier.** Trae substitutes nothing into a hook command, so the file must
  carry a resolved path. `<TASKFLOW_ROOT>` is TaskFlow's own placeholder, replaced
  at install time, not a Trae variable.
- **Plugin root.** Trae injects `TRAE_PROJECT_DIR` and `CLAUDE_PROJECT_DIR`, and no
  plugin-root variable — it has no plugin root to inject. `session-start` picks its
  output shape from the environment, so `hooks-trae.json` sets `CLAUDE_PLUGIN_ROOT`
  on the SessionStart command line, the way `hooks-dsh.json` does; without it the
  hook emits a top-level `additionalContext` that Trae discards, silently.
- **SessionStart source.** Trae runs SessionStart with `source` fixed to `startup`
  and supports no other value. There is no `fork` and no resume/clear/compact
  source, so the file's matcher is `startup` alone. The shared script does not read
  `source` at all, so only the matcher depends on this.
- **Shell.** Bash on macOS/Linux, PowerShell on Windows. That is why the commands
  spell `bash` explicitly, and why a Windows user replaces them with
  `& '<path>\hooks\run-hook.cmd' <script>` rather than relying on one spelling
  working everywhere.
- **Tool names.** `Write`, `Edit`, `Skill`, and `mcp__<server>__<tool>` are the ones
  the gate and the recorder read, and Trae's normalized tool list contains all four.
  It has no `Agent`/`Task`. What has **not** been confirmed is the interior of
  `tool_input` on Trae's `PreToolUse`/`PostToolUse` events: the field names
  `json-field` reads (`file_path`, `skill`) are documented for Claude Code, not for
  Trae, and both hooks fail open — a denial that never fires and an evidence line
  that never records look exactly like a phase where nothing happened. That is the
  first thing to check when someone runs this on Trae.
- **Claude Code config import.** Trae can read `~/.claude/settings.json` and the
  project `.claude/settings.json` files instead, behind the
  **导入 CLAUDE 中的 Hooks 配置** switch, merging them with any Trae hooks. It is
  opt-in and host-side, so it cannot be shipped from here; the `.trae/` path is the
  one this repository documents.

## Must / may-not

A hook MAY:
- update a `TaskFlowDocs/todo.md` item's triage metadata (status, priority, date, `Next`) — Todo is triage metadata only;
- inject a derived, clearly non-authoritative context summary (e.g. the SessionStart state summary, or the per-prompt in-flight task reminder, which names the task, its phase, approval and next Step and asks the Agent to classify the incoming instruction — it never classifies, records, or edits anything);
- maintain the selected task's `sessions.md` session index from the host event: one entry per session, limited to the session id, agent/platform, availability, started/last-active timestamps, code working directory, task artifact directory, and Task version/phase. `Last completed`, `Next step`, and `Notes` stay Agent-owned; the hook never creates the entry in another task, never touches `TaskFlowDocs/achieved/`, and never marks a session `closed`;
- record a real capability invocation in the task worktree's evidence store, and refuse a stage document's first body write until one was recorded for that stage (`capability-evidence`, `capability-gate`);
- run one of the single-command transition scripts below.

A hook MUST NOT:
- create, rewrite, or delete `prd.md`, `spec.md`, `plan.md`, `reference/index.md`, or move anything under `TaskFlowDocs/achieved/` on its own;
- grant a permission or approve: the pre-write gate can only deny, and every other permission surface keeps its own say;
- create or alter an `## Approval` block, or otherwise approve;
- duplicate promoted task facts into Todo, `sessions.md`, or any hook output;
- read secrets or carry sensitive payloads in hook output (both hosts spill oversized output to disk).

If a hook fails (nonzero exit or stderr), it must fail safe: no partial core writes. The host surfaces the error as a reminder; the Agent recovers.

## SessionStart state summary

Purpose: on session start or resume, maintain the repository-document routing record and give the Agent compact derived routes/state. The index is authoritative for routing/check metadata; routed source documents remain authoritative for policy content.

Reference scripts:
- `hooks/summarize-state` — prints the selected active task and its next Plan Step by default. Set `TASKFLOW_TASK_ID` for explicit selection or `TASKFLOW_VERBOSE=1` to include the full Todo and active-task inventory. Ambiguous state is reported without guessing. It goes silent only where there is nothing to say: no `TaskFlowDocs` at all, or the directory present with nothing recorded in it, each states the applicability boundary in one block instead — see below.
- `hooks/repository-docs-context` — atomically synchronizes deterministic index metadata for recognized sources and prints phase-filtered paths/status. It never edits source policies or core task documents.
- `hooks/session-start` — consumes the host event JSON, processes only `SessionStart`, uses its `cwd` for repository routing, and wraps the summary into the platform's context field (Claude Code → `hookSpecificOutput.additionalContext`; Cursor → `additional_context`; Copilot/other → top-level `additionalContext`).
- `hooks/session-record` — called by `session-start`; records the host `session_id` in the selected task's `sessions.md` (see the must/may-not list for the field boundary). Selection is the same as `summarize-state`: explicit `TASKFLOW_TASK_ID`, else the single active task; otherwise it writes nothing. It is best-effort — a failure never changes the SessionStart exit code or context output — and reports skipped or unparseable input on stderr only.

Keep summaries short; both hosts cap oversized hook context (Claude Code caps at 10,000 chars and Codex spills past ~2,500 tokens). If nothing is present, print nothing.

The one exception is an entry point, where this hook is the only TaskFlow output a session gets before an Agent has read anything. A repository with no `TaskFlowDocs/`, and one that has the directory but has never recorded anything in it, are the two states where every other signal is absent at once — no task list, no Todo entry, and no branch report to raise — so both print the applicability boundary instead of nothing. The sentence states the rule; it creates nothing, and it is suppressed entirely once `todo.md` exists, which is the point at which intake has run at least once and the obligation has been seen.

A branch no task directory matches is reported in one line, also at the end of the summary. It locates the work and leaves the judgement alone: work that was registered and then archived counts as registered, so `achieved/` matches, and a base branch, a detached HEAD, and a non-repository directory say nothing at all.

Scripts are extensionless bash so Claude Code's Windows auto-detection (prepends `bash` to any command containing `.sh`) never interferes. On Windows, `hooks/run-hook.cmd` is a polyglot batch/bash wrapper that locates Git Bash; the same `command` value works on every OS for Claude Code, and Codex `hooks-codex.json` uses `commandWindows` where desired.

Hooks carry no language runtime. Text work is done with `awk` and `sed` at the bash 3.2 + BSD userland level, which is the floor `2026-09-14-macos-hook-portability` established: no `declare -A`, no `mapfile`, and no GNU-only `sed -i` may appear in a hook. Two smoke sections carry that floor rather than a linter — every hook must `bash -n` clean under the shell on the runner, which on macOS is a real 3.2 parser check, and every hook must run against a curated `PATH` holding no interpreter, so a reintroduced runtime dependency fails CI rather than a user's session. `tools/fixture-compare` is a different tool: it byte-compares the fixtures one run produced against a reference run, normalizing paths and timestamps, which is how a hook rewrite is proven equivalent.

Windows uses the same Bash implementation through `run-hook.cmd`; PowerShell and `cmd.exe` do not maintain separate lifecycle logic. `hooks/smoke-test-windows.ps1` exercises the complete lifecycle through that launcher, including a repository path with spaces and Chinese characters.

## Single-command transitions

Run explicitly by the Agent as one operation. Only SessionStart summary injection, the per-prompt reminder, the sessions index, and the pre-write gate (Claude Code, Codex CLI, CodeBuddy, and Trae) are automatically wired; no write command binds to `UserPromptSubmit`, `PostToolUse`, or `Stop`. `UserPromptSubmit` is bound, but only to `prompt-reminder`, which reads state and emits context — it is not a write command and it changes nothing.

`prompt-reminder` derives task state from `summarize-state`. In a TaskFlow repository with no active task, its entrance context guides intake and capability selection for development requests; a single `planning` task gets a short phase-specific capability reminder. `in_progress` and `checking` retain the existing change-event reminder. A `ready` task, multiple active tasks, a cwd outside a repository, or invalid input produces no task reminder. Successful `task promote` also prints one short capability-selection hint in its normal command output. No tool-call watcher or new state is added; if the agent bypasses `promote` and ignores the entrance hint, this does not guarantee a mid-turn correction.

The one exception to "reads `plan.md` only through `summarize-state`" is the reinforce line: the routed document list reaches the session once, at SessionStart, so a Plan that names material it must keep consulting has no other per-prompt carrier. The hook reads that Plan's `## Reference Pointers` for `- [Reinforce] \`path\` — reason` bullets and prints the resolved paths on one line between the task line and the classification question. Admission needs the marker, a backticked path, the `—` separator and a non-empty reason after it; a line missing any of them is dropped rather than parsed as far as it goes, because a malformed bullet reported as a pointer says a document is missing when the bullet is what is wrong. The path has to be a POSIX repository-relative one — a leading `/` or `~`, a backslash, a colon, or a `..` segment each name something unresolvable, so each is dropped. Fenced blocks are skipped, because the Plan outline in `artifacts.md` is itself fenced and carries this heading verbatim. A path that no longer resolves prints as `MISSING: <path>` in that same line instead of disappearing — material going missing is the failure the line exists to surface, and filtering it would make the reminder quietest exactly when it had most to say. A Plan that marks nothing produces the same output it always did. `artifacts.md` states who marks an entry, the three tests an entry must pass, and which change-event bucket a wrong pointer falls into. It is wired on all five hosts, under one event name on four of them: Claude Code, CodeBuddy, Trae and Codex CLI all call the event `UserPromptSubmit` and read `hookSpecificOutput.additionalContext`, and dsh's bridge subscribes to `agent/pre-step`, runs the command configured under `UserPromptSubmit` with a payload whose `hook_event_name` is that same string, and decodes the same envelope — measured against `@deepseek-ai/dsh-hooks-claude-code` 0.2.0-rc.2 and `@deepseek-ai/dsh-hook-protocol`, which discards a `hookSpecificOutput` whose `hookEventName` differs from the firing event. The per-host standing is the table's: Claude Code measured, CodeBuddy from its packaged CLI and docs, Trae, Codex and dsh from documentation. Trae's documented input carries no `cwd`, so the hook falls back to the process working directory, the same fallback `capability-evidence` takes.

A host with no hook wiring gets none of this, and that is not a gap to be filled by adding more hosts: `SKILL.md`'s User-change trigger is the rule, and the reminder only keeps it in view across a long session. The wording there therefore names the case on its own — an instruction that arrives mid-Step, a reported defect, a different approach — so an Agent on a host with no hooks at all still has the rule; see the trigger's section and Phase 5.

`intake` and `promote` both care whether the working tree they write into is the base one: a task's first documents are written in Phase 1, so writing them in the base tree puts them on whatever branch happens to be checked out. `promote` refuses there; `intake` only notes it, because triage should stay cheap. Both read the same signal — a linked worktree's git directory contains `commondir`, which is Git's own answer and needs no branch-name parsing — and neither applies where `--root` is not a repository at all.

### Which task a command acts on

The commands that record something — `unaided`, `external` — have to name a task, and one task per working tree is the rule that normally makes the question trivial. It stops being trivial when one tree holds several task directories, which happens when a parent and a child run together or documents are carried in from another branch, and the answer matters because `released` is keyed by task name: record against the wrong one and `approve` reconciles a stage against evidence another task earned.

So the name is resolved from evidence, in this order, and never from directory order:

1. **`TASKFLOW_TASK_ID`**, the same variable and meaning `summarize-state` and `session-record` already read. A caller naming a task is not something to second-guess.
2. **The task directory the caller is standing in**, including any subdirectory of it. This is the only source that cannot disagree with intent, because it is where the caller is.
3. **The only active task**, when exactly one exists.

Anything else is refused with exit `2` — needs-user-input, per `CODE_STYLE.md` — and the refusal lists the candidates and prints both remedies. Refusing rather than picking is the whole point: the failure being repaired is a silent wrong answer, so the one branch that must not exist is the one that guesses. `external` is deliberately not on this list: its store is keyed to the git directory rather than to a task, so it only asks whether any active task exists, and several of them are not ambiguous for a question it never puts.

| Command | Action | Verify after |
| --- | --- | --- |
| `hooks/task intake <goal> [source] [--local] [--kind <defect\|capability\|internal>] [--root <path>]` | Add one deduplicated Todo entry and allocate its ID. | Prints the Todo ID; duplicate goals fail before mutation. `--kind` defaults to `capability` here and is written to the entry as `- Kind:`; `promote` requires it explicitly, because that is where it starts deciding anything. In the base working tree it additionally notes that `todo.md` is now uncommitted there (exit code unchanged). |
| `hooks/task item-state <todo-id> <inbox\|clarified\|in_progress\|done> <next-action> [--root <path>]` | Update one unpromoted local Todo by ID, retaining its prose. | Refuses ambiguous IDs, promoted items and remote-associated records; use remote operations for remote Issues. |
| `hooks/task promote <todo-id> <task-id> <small\|large> --kind <defect\|capability\|internal> [--root <path>]` | Create minimal PRD/Plan and optional Spec scaffolds, then link the Todo. | Existing destinations and already-promoted items fail before mutation. `--kind` is required here and optional at intake: it is written into the PRD's `## Task Kind`, and `approve` reads it to decide whether this task's `[PRD]` line must name something that investigates a cause. Refuses with `STATUS: blocked` (exit `3`) outside a task worktree — the first task documents are written in Phase 1, so they would otherwise land in the base tree on whatever branch is checked out. The message prints the `git worktree add` command with everything but `<type>` filled in. |
| `hooks/task state <task-id> <state> [--root <path>]` | Update PRD/Plan state and Todo triage state. | `in_progress` requires approval for the current Task version. |
| `hooks/task progress <task-id> <step> <status> [verification] [--root <path>]` | Update one Plan Step and optionally append a verification line. | `done` rejects unchecked checklist items. |
| `hooks/task unaided <PRD\|Spec\|Plan\|Test> --considered "<concept class>" [--root <path>]` | Record a deliberate unaided decision for a stage, which is what lets the pre-write gate release it and `approve` reconcile it. For `Test` it is also the stage's only carrier, so it spends the next unreleased evidence line when one is standing and reports which kind it wrote. | Exit `2` on a stage that is none of the four, a missing `--considered`, or a class outside the phase vocabulary, which it prints. It validates a class against the vocabulary and nothing else — it cannot judge whether the decision was right. Also exit `2` when it cannot tell which task the record belongs to; see **Which task a command acts on**. |
| `hooks/task complete <task-id> --user-accepted [--root <path>]` | Run `completion-gate`, set core statuses, and invoke archive. | Requires explicit acceptance and leaves no active task on success. Refuses before the first write, so nothing has to be rolled back. |
| `hooks/archive <task-id>` | Run `completion-gate` — the Plan is approved for its current Task version, has no unchecked item and no unclosed Step — then move `TaskFlowDocs/<task-id>` → `TaskFlowDocs/achieved/<task-id>`, update the linked Todo item's `Task:` path and status to `done`, and verify the active path is absent, the achieved path exists, and the achieved root PRD and Plan both say `completed`. | Prints a check report; on any failure leaves the task active, the Todo unchanged, and exits nonzero. Both entry points into `achieved/` run the same file, so neither is a weaker way in. |
| `hooks/completion-gate <task-dir>` | Decide whether the Plan may be treated as finished: approved for its current Task version, no unchecked item, no unclosed Step. A Step is closed only when it says `- Status: done` in column 0 — a whitelist, so an unrecognized or missing value counts as unfinished rather than as finished. A block is located by its `### Step <number>` heading anywhere in the Plan, not only under `## Steps`, because that is how `task progress` finds the block it edits. `--approval-only` asks the narrower question `task state in_progress` and `task progress` need. | Exit `1` with one line naming the failing condition. Reads the Plan as a file in one `awk`; a `printf | grep -q` shape is silently disabled by `pipefail` on any Plan larger than the pipe buffer. A Plan with no `### Step` block at all is not refused — that is a question about whether a Plan must have Steps, which this command does not answer. |
| `hooks/reopen <task-id>` | Move `TaskFlowDocs/achieved/<task-id>` → `TaskFlowDocs/<task-id>`, record the Todo source/reopen reason in the Plan change log. | Prints a check report; exit nonzero on mismatch. |
| `hooks/version <task-id> <new-v>` | Copy only changed core documents plus `version.md` into `old/v<old>/`, retain root docs, bump them to `<new-v>`, and reset state/approval for review. | Prints archived paths + root version/state agreement; exit nonzero before mutation on invalid input. |

`task complete` performs the validated completion plus the existing archive transaction. The Agent still owns semantic document content and every Approval record.

## Parallel branches and the Todo merge driver

Local Todo entries and promoted remote task references share `TaskFlowDocs/todo.md`, so two task branches can merge-conflict there even when they touched nothing in common. TaskFlow ships a Git merge driver for it, so the two ordinary cases resolve without a human:

- two branches each added an entry — both entries survive;
- two branches changed different entries — both changes survive.

Two branches changing *the same* entry differently is still a real conflict and is left for review with ordinary conflict markers.

The wiring is per-clone and untracked: `merge.taskflow-todo.driver` in the repository's own Git config, a `TaskFlowDocs/todo.md merge=taskflow-todo` line in `.git/info/attributes`, and local-only exclude rules in `.git/info/exclude` (`TaskFlowDocs/repository-docs/personal.md`, `TaskFlowDocs/**/sessions.md`, and the remote Todo recovery directories). `hooks/install-git-hygiene` writes all three, `hooks/session-start` calls it on every session start, and it is idempotent, `--local`-only, silent on success, and best-effort. Nothing tracked is edited, so a repository that has not adopted TaskFlow is unaffected; `hooks/merge-todo` is the driver itself.

The two exclude rules are there because those files belong to one clone rather than to the repository — a personal rule is not team policy, and `sessions.md` carries a session id, a working directory and `Session availability: local-only`. They are written per clone for exactly that reason: a `.gitignore` line would be a tracked file, which changes the view of every clone including the ones that want to commit the same paths. Two limits follow. Git applies no ignore rule to a **tracked** path, so a copy that was forced in once keeps appearing in `git status` — deliberately, because a rule that hid real changes to a tracked file would be worse than the stale file; clearing those copies is a decision about tracked history, not a configuration change. And the installation is done by SessionStart, so a host that does not run the hooks leaves the repository unconfigured until someone runs `bash hooks/install-git-hygiene` there.

Two limits are worth stating plainly:

- **Only local merges.** A hosted-platform merge (a pull request merged in the web UI) runs server-side and does not run a custom driver — Git does not ship the driver command to the server. It degrades to an ordinary content conflict, which is resolvable but manual. Merging the branches locally and pushing is what uses the driver, and `hooks/todo-check` (below) is what catches a hosted merge that resolved the conflict badly.
- **Text, not semantics.** The driver matches entries by `- ID:` and falls back to the heading. Tasks that intentionally reuse an ID for different items are not detected as a conflict.

Because the web UI path has no driver, the driver's own invariant — a Todo entry is never deleted — is not enforced there by anything. `hooks/todo-check [repo-root] [commit | <before>..<after>]` is the read-only check for it: every `- ID:` a merge's parent commits held must still be present in the result, or the dropped entry is named along with the parent that held it and the merge that lost it (`0` pass, `2` dropped, `3` cannot tell). Run it explicitly, or give it a rev range to audit every merge commit inside it — the range form is what CI runs.

A hosted-platform merge only becomes visible here after it has landed, so the protection is a pair: merge locally so the driver runs, and audit the result. The `.github/workflows/hooks.yml` `todo-merge-audit` job runs `todo-check` over the pushed range on every push to `main`, and over the tip on a pull request, so a drop introduced by a web-UI merge is named within the same push that carried it. Recovery is still manual and reviewed: `git show <parent-that-held-it>:TaskFlowDocs/todo.md` gives the entry back, and the entry is re-added to `todo.md` in a normal commit.

Only merge commits' own parents are compared, so a single commit whose tip is a clean merge passes even when an earlier merge in the same push dropped an entry — the range form is what closes that. A range with no merge commits passes; a range that cannot be resolved is `blocked`, not `pass`, because an unusable argument and a clean push are not the same answer.

Todo IDs are derived from the goal (`TF-<yyyymmdd>-<6 hex>` from a `cksum` digest), not from the highest existing ID. A shared counter makes two branches cut from the same base both allocate the day's first ID, and a merge that keeps both entries then leaves two entries claiming one ID — no merge strategy can repair that, because the ambiguity is in the content. Deriving the ID makes the branches agree instead.

## Folder layout

```text
repo-root/
├── .claude-plugin/marketplace.json      # marketplace catalog (all hosts read it)
├── .codebuddy-plugin/marketplace.json   # CodeBuddy catalog (same pin as the above)
└── taskflow/
    ├── .claude-plugin/plugin.json       # Claude Code manifest (skills: ./skills/)
    ├── .codex-plugin/plugin.json        # Codex CLI manifest (skills: ./skills/)
    ├── .codebuddy-plugin/plugin.json    # CodeBuddy manifest (skills: ./skills/taskflow)
    # Trae has no manifest directory: its hooks.json is copied, not installed
    ├── package.json                     # dsh plugin package (dsh.bundle.patch)
    ├── dsh/
    │   ├── index.js                     # mounts the skill provider and the hook bridge
    │   └── cordis.patch.yml             # bundle layer: one insert of the plugin row
    ├── skills/taskflow/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/                  # runtime.md, artifacts.md, versioning-and-recovery.md
    └── hooks/
        ├── README.md                    # install + run instructions for every host
        ├── hooks.json                   # Claude Code wiring (SessionStart + UserPromptSubmit + PreToolUse gate + PostToolUse/PostToolBatch evidence; auto-loaded)
        ├── hooks-codex.json             # Codex CLI wiring (SessionStart + UserPromptSubmit + PreToolUse apply_patch gate + PostToolUse external-evidence)
        ├── hooks-codebuddy.json         # CodeBuddy wiring (SessionStart + UserPromptSubmit + PreToolUse gate + PostToolUse evidence)
        ├── hooks-dsh.json               # dsh wiring (SessionStart + UserPromptSubmit + base edit guard)
        ├── hooks-trae.json              # Trae wiring (SessionStart + UserPromptSubmit + PreToolUse gate + PostToolUse evidence)
        ├── run-hook.cmd                 # cross-platform launcher (polyglot batch/bash)
        ├── session-start                # SessionStart entry (extensionless bash)
        ├── prompt-reminder              # UserPromptSubmit: in-flight task + reinforce pointers + classification question
        ├── session-record               # records the host session id in the task index
        ├── install-git-hygiene          # per-clone Git config: Todo merge driver + local-file excludes
        ├── merge-todo                   # the driver: merges todo.md by entry
        ├── repository-docs-context      # syncs index metadata + derives routes
        ├── diagnostic-event             # asynchronous allowlisted event recording
        ├── diagnostic-log               # user-controlled enable, disable, export
        ├── test-diagnostic-log          # privacy and nonblocking fixture
        ├── ledger-lock                 # nonblocking guard for task evidence and handoff
        ├── reuse-worktree             # journaled reuse and evidence restoration
        ├── test-ledger-lock           # concurrent handoff guard fixture
        ├── test-worktree-candidates    # archived worktree discovery fixture
        ├── test-reuse-worktree        # archived worktree reuse fixture
        ├── capability-evidence          # records real invocations in the worktree store
        ├── external-evidence            # records outside URLs from any tool event, in a separate store
        ├── capability-gate              # refuses a stage document's first body write
        ├── test-base-document-permit    # scoped permit regression
        ├── base-document-permit         # one-edit document permit
        ├── base-write-gate              # refuses observable base checkout edits
        ├── base-status-reminder         # asynchronously reports base checkout changes
        ├── json-field                   # shared one-level JSON reader
        ├── task-id                      # the one rule for a legal task name
        ├── approval-check               # the one rule for whether a Plan's version is approved
        ├── completion-gate              # the one rule for an approved, finished Plan
        ├── markdown-field      # read task metadata outside fenced examples
        ├── version-baseline             # verify each task version has a Git rollback point
        ├── task                         # explicit intake/promote/state/progress/unaided/complete
        ├── summarize-state              # shared state-summary generator
        ├── archive                      # full archive transaction (incl. Todo update)
        ├── version                      # archive changed docs + version bump
        ├── reopen                       # retrieve an achieved task
        ├── release-version              # write the mechanical release version literals
        ├── release-check                # version literals + marketplace pin agree
        ├── repository-check             # governance and fork readiness check (read-only)
        ├── remote-topology              # per-remote fork topology + push permission (networked, opt-in)
        ├── repo-rules                   # show / install / check default repository rules
        ├── templates                    # the default CONTRIBUTING.md and CODE_STYLE.md
        ├── todo-check                   # no merge in a commit or rev range dropped a Todo entry
        ├── test-host-parity             # synthetic host event and declaration fixture
        ├── smoke-test-windows.ps1       # PowerShell/cmd full lifecycle regression
        ├── test-multi-todo              # shared task and per-item lifecycle regression
        ├── test-version-baseline        # real Git lifecycle regression fixture
        ├── remote-todo                      # explicit remote Issue Todo commands
        ├── remote-todo-local-list           # list and deduplicate retained local Todos
        ├── remote-todo-migrate              # migrate one local Todo to an Issue
        ├── remote-todo-promote              # promote an Issue into a TaskFlow task
        ├── remote-todo-reattach             # reconnect a detached task after checking phases
        ├── remote-todo-reattach-todo        # reconnect an unpromoted local Issue copy
        ├── remote-todo-to-local             # copy an Issue locally and optionally detach
        ├── test-json-field-arrays           # JSON string array membership regression
        ├── test-json-field-numbers          # JSON number parsing regression
        ├── test-remote-todo                 # remote Todo  regression
        ├── test-remote-todo-archive         # remote Todo archive regression
        ├── test-remote-todo-concurrency     # remote Todo concurrency regression
        ├── test-remote-todo-configure       # remote Todo configure regression
        ├── test-remote-todo-create          # remote Todo create regression
        ├── test-remote-todo-detach          # remote Todo detach regression
        ├── test-remote-todo-detach-archived # remote Todo detach archived regression
        ├── test-remote-todo-detach-task     # remote Todo detach task regression
        ├── test-remote-todo-edit            # remote Todo edit regression
        ├── test-remote-todo-intake          # remote Todo intake regression
        ├── test-remote-todo-label           # remote Todo label regression
        ├── test-remote-todo-link            # remote Todo link regression
        ├── test-remote-todo-list            # remote Todo list regression
        ├── test-remote-todo-migrate         # remote Todo migrate regression
        ├── test-remote-todo-migrate-dedup   # remote Todo migrate dedup regression
        ├── test-remote-todo-migrate-stage   # remote Todo migrate stage regression
        ├── test-remote-todo-mixed-list      # remote Todo mixed list regression
        ├── test-remote-todo-private         # remote Todo private regression
        ├── test-remote-todo-promote         # remote Todo promote regression
        ├── test-remote-todo-recover         # remote Todo recover regression
        ├── test-remote-todo-reminders       # remote Todo reminders regression
        ├── test-remote-todo-snapshot        # remote Todo snapshot regression
        ├── test-remote-todo-stage           # remote Todo stage regression
        ├── test-remote-todo-task-state      # remote Todo task state regression
        ├── test-remote-todo-to-local        # remote Todo to local regression
        └── smoke-test                   # assert-style smoke tests
```

This mirrors the `obra/superpowers/hooks` convention: flat directory, extensionless bash scripts, one hook JSON per host, and a cross-platform launcher — no per-host subfolders or non-bash runtimes. Shared logic lives in the scripts themselves; each host JSON only wires events to them.

The tree is the inventory, and `hooks/smoke-test` asserts it against the directory in this file and in `hooks/README.md` alike: a script added, renamed, or removed without its line here is a suite failure.

Not every script in the tree is a lifecycle command, and the two are documented in different places. `hooks/task` and the four it drives (`task-id`, `completion-gate`, `archive`, `version`, `reopen`) are the lifecycle, and their rows are above. `hooks/release-version` and `hooks/repository-check` belong to the release procedure instead — `release-version` writes the mechanical version literals across the eight files that carry them, and `repository-check` performs a read-only governance and fork-readiness check that also names every worktree whose branch is already merged. Both are documented in `RELEASE.md`, which is where their ordering and preconditions live; they are listed here so that a reader routed to the hooks layout knows they exist, not so that a second copy of the procedure lives here.

**`hooks/remote-topology` is a read-only network command and is not wired to an event.** The explicit `remote-todo` commands also use the network when invoked. It answers what `git remote -v` cannot: which repository each remote names, whether this clone can push to it, and which base a pull request should target. `CONTRIBUTING.md` requires the receiving repository be established rather than inferred from a remote named `origin` or `upstream`, and remote names carry no role — a fork's `origin` may be the author's own fork or the upstream. Every fact it prints is read from `GET /repos/{owner}/{repo}`: `fork`, `parent.full_name`, `source.full_name`, `default_branch`, and `permissions.push`. The base is not inferred — a fork targets the repository it was forked from and a non-fork targets itself, both read from `parent`.

Three boundaries keep it from changing what the rest of the runtime is. It is **never** added to any `hooks-*.json`: a network round trip in `SessionStart` would make every session wait on GitHub, and the smoke suite asserts the absence rather than trusting it. It writes no file and issues no request other than `GET /repos/*`. And it **always exits 0** — `repository-check`'s `2` and `3` are verdicts about the repository, and "`gh` is not installed" is not one.

The four ways the lookup can fail are reported apart because each calls for a different action: `gh not found` (install it), `gh not logged in` (authenticate it), `cannot reach the GitHub API` (wait for the network), `API rate limit` (wait for the window to reset). They cannot be told apart by exit code — an unauthenticated `gh` and an unreachable network both exit `1`, measured 2026-11-02 — so the authentication question is asked first and the response body distinguishes the rest. The timeout budget is for the whole run rather than each request, so the command is bounded at ten seconds however many remotes a clone has; without `timeout` or `gtimeout` on `PATH` the script says so instead of leaving the absence silent.

`hooks.json` is named without a host suffix because Claude Code auto-loads that exact filename at the plugin root. Every other host points at its file some other way — a manifest `hooks` entry for Codex and CodeBuddy, `dsh/index.js` for dsh, a copy to `.trae/hooks.json` for Trae — so only Claude Code depends on the name.

## Remote Todo backend

`hooks/remote-todo mode-set local|remote` selects the project default; `connect <alias> github|gitlab <host> <project>` adds a source without changing the mode. `mode` and `validate` are local, and `list` explicitly reads remote sources alongside retained local entries. GitHub's issue endpoint can include pull requests; those are filtered. Source failures make the result incomplete. A user's explicit `hooks/task intake ... --local` can still make one local entry in remote mode.

`promote`, `stage`, `edit`, `label`, `create`, `migrate-to-remote`, and `migrate-to-local` require explicit invocation. A remote task keeps `remote-issue` as an execution association; `task state`, `archive`, and `reopen` synchronize its phase before the local transition. The two sides cannot be committed atomically. Existing remote labels outside `taskflow:` are preserved by targeted additions/removals. Missing TaskFlow stage labels are created as needed; repository label creation requires permission. `migrate-to-local ... --detach` keeps the original local record and remote Issue; for a task it retains the approved task documents and saves an untrusted local reference copy. Local detached tasks no longer contact the remote source. `reattach-todo <todo-id> <alias> --remote-authoritative` reconnects an unpromoted remote copy without writing the Issue; retain the local content. `reattach-task <task-id>` reads the original Issue, refuses if the phase differs or another task is linked, and preserves detach history without changing remote content. A later detachment retains the earlier local copy and fetches a fresh one. Migration checks all Issues for a stable Todo marker before creation; never migrate the same Todo concurrently from multiple worktrees or machines. Editing or removing the marker outside TaskFlow can defeat later checks.

`gh` and `glab` use the host's existing authentication for the selected hostname; missing tools or permissions fail visibly. No credential is saved in project config or recovery records. Before a remote write, the local recovery directories must be excluded from Git and must contain no tracked files; `hooks/install-git-hygiene` installs the per-clone exclusions. Explicit snapshots contain only source order and validated Issue numbers, states and update times; titles, bodies and labels are excluded. Metadata can still reveal activity; source numbers refer to configuration order at export time. The user selects a new path, and the snapshot is historical, not an editing source. No automatic network polling occurs.

A write timeout can mean success or failure. Inspect the recorded operation before retrying: use `resolve <id> <number>` to verify a creation marker, `resolve-absent <id> --checked` only after confirming no Issue was created, and `ack-update <id> --checked` only after reviewing an uncertain update. A stale lock may require user inspection. Local locks do not coordinate independent worktrees or machines. Platforms without conditional writes leave an accepted concurrent-update window; a read-before/write/read-after sequence cannot prove no overwrite occurred.

### Archived worktree handoff

`reuse-worktree start` verifies a committed archive and snapshots the current worktree's evidence before detaching at a verified base commit and creating a new branch there. `resume` restores a retained task snapshot; `recover` restores the original state after an interrupted handoff. The caller must establish that all users of the worktree are idle. Evidence hooks skip events rather than wait on the shared ledger lock; task commands and the document gate refuse work while it is held or a handoff is pending. Abrupt termination can leave a lock requiring inspection; ordinary Git checkout does not transfer evidence. Version baselines remain in place. Submodules and nonstandard Git metadata layouts require manual isolation. See the skill for commands and authorized cleanup.
