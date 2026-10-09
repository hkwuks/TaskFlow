# PRD — Adapt TaskFlow to Trae IDE as a fifth host

> Task version: v1
> Status: completed

## Goal

Adapt TaskFlow to Trae IDE as a fifth supported host, so a Trae user runs the same
TaskFlow flow and gets the same SessionStart state summary the other hosts get.
The change is additive: one new per-host wiring file in the repository, the exact
steps a Trae user runs locally, and the host-list bookkeeping.

## Background / Confirmed Facts

**Trae has no plugin-install mechanism for a third-party repository.** Verified
against `docs.trae.cn` on 2026-10-09:

- Trae's plugin market (设置 > 插件市场) is a curated in-app catalog. No documented
  way exists for a repository to publish or self-register an entry, and there is no
  `trae plugin marketplace add <owner/repo>` command. The documented third-party
  precedent (`mnemon-dev/mnemon`) does not publish a Trae plugin either; it copies
  files into `.trae/`.
- Trae's repository-facing surface is project-scoped files:
  - `$PROJECT_FOLDER/.trae/skills/` — project skills, one folder per skill with a
    `SKILL.md`. `.agents/skills/` is also read, with `.trae/skills/` winning a
    name collision.
  - `$PROJECT_FOLDER/.trae/hooks.json` — project hooks. Global hooks are
    `~/.trae-cn/hooks.json` (macOS/Linux) or `%userprofile%/.trae-cn/hooks.json`
    (Windows).
- Trae **also reads Claude Code hook configs** when the user turns on
  "导入 CLAUDE 中的 Hooks 配置": `~/.claude/settings.json`, and
  `.claude/settings.json` / `.claude/settings.local.json`, merged with any Trae
  hooks. It is an opt-in switch in Trae, not something this repository controls,
  which is why it is documented as an alternative rather than the primary path.

**Trae's SessionStart contract matches what `hooks/session-start` already emits.**

- stdin carries `session_id`, `cwd`, `hook_event_name`, `workspace_roots`; the
  event-specific field is `source`, and Trae sends only `startup` — no `fork`, and
  no `resume|clear|compact`.
- stdout accepts the nested `hookSpecificOutput.additionalContext` envelope, which
  the hook already emits on its Claude Code branch.
- Trae injects `TRAE_PROJECT_DIR` **and** `CLAUDE_PROJECT_DIR` (both equal to stdin
  `cwd`), and does **not** inject any plugin-root variable — Trae has no plugin
  root for this file to resolve.
- `matcher` in `hooks.json` applies only to `PreToolUse`, `PostToolUse`, and
  `Notification`, never to `SessionStart`.
- Hooks run in the system shell: Bash on macOS/Linux, PowerShell on Windows; there
  is no `.sh` rewrite to dodge. Exit-code semantics match Claude Code's (0 read,
  2 blocking, anything else non-blocking); the hook already exits 0.

**Trae's tool-call contract is close enough to carry the same two gate hooks.**

- `PreToolUse` carries `hook_event_name`, `tool_name`, `tool_input`, `cwd`, and its
  deny shape is `hookSpecificOutput.permissionDecision: "deny"` with
  `permissionDecisionReason` — byte-identical to what `capability-gate` already
  prints, so the script is unchanged.
- `PostToolUse` carries the same fields plus `tool_response`, which is what
  `capability-evidence` reads its `tool_name` and `tool_input.*` from.
- `matcher` is a **regex** on the normalized `tool_name`, so `Write|Edit`,
  `Skill`, and `mcp__.*` all work as written in `hooks.json`.
- Trae's normalized tool names include `Write`, `Edit`, `Skill`, and
  `mcp__<server>__<tool>`, which is the set both hooks already branch on. Trae's
  list has **no** `Agent`/`Task` tool: its subagents are markdown-defined and are
  not documented as a tool call, so evidence from that path is not collected on
  Trae while `Skill` and MCP calls still are.

**Why the other hosts' install path does not carry over.** Claude Code, Codex, and
CodeBuddy install by command from the marketplace; dsh installs by `dsh plugin add`.
Trae has neither, so TaskFlow ships a wiring file plus copy commands, and says so
rather than implying an install command that does not exist.

## Requirements

1. Add `hooks/hooks-trae.json`: Trae's own `hooks.json` shape (`version`, event,
   hook group with `type`/`command`/`timeout`), wiring the same three events the
   Claude Code file wires — `SessionStart`, `PreToolUse` on `Write|Edit`,
   `PostToolUse` on `Skill` and `mcp__.*` — all through `hooks/run-hook.cmd`, with
   the repository root supplied the way Trae supplies it (`CLAUDE_PROJECT_DIR`; no
   plugin-root variable) and `SessionStart` matched on `startup` alone.
2. Give the Trae install as commands in `hooks/README.md`, `README.md`, and
   `README.zh-CN.md`: copy `skills/taskflow` into `.trae/skills/taskflow`, and
   write `.trae/hooks.json` from the shipped `hooks-trae.json` with the repository
   root substituted. Document Trae's own "import Claude Code hooks" switch as the
   alternative. Do not commit a second skill tree.
3. Add Trae to every enumerated host list: `README.md` / `README.zh-CN.md`,
   `ROADMAP.md`, `skills/taskflow/SKILL.md`, `package.json`, and
   `skills/taskflow/references/runtime.md` (host table, event map, folder layout).
4. Add a "Trae specifics" subsection to `runtime.md` stating each fact with its
   source and stating separately what has not been measured on a live host.
5. Pin the new file with one `hooks/smoke-test` section, sized like the existing
   dsh section: the wiring parses as Trae config, its commands resolve the
   repository root, and each event's command produces the shape that event's
   consumer reads.
6. Keep the intake record in `TaskFlowDocs/todo.md` (written at intake) linked to
   this task.

## Acceptance Criteria

- `bash smoke-test` from `hooks/` (run from the task worktree) exits 0.
- `bash hooks/release-check .` exits 0.
- The new smoke section fails when `hooks-trae.json` is deleted, when its commands
  stop naming the repository root, and when SessionStart's output loses the nested
  `hookSpecificOutput.additionalContext` envelope.
- `grep -ri trae` finds Trae in every enumerated host list, and no file still says
  TaskFlow supports only four hosts.
- `git diff --check` is clean.

## In Scope

- `hooks/hooks-trae.json` (new).
- `hooks/README.md`, `README.md`, `README.zh-CN.md`, `ROADMAP.md`.
- `skills/taskflow/references/runtime.md`, `skills/taskflow/SKILL.md`,
  `package.json` (host lists only).
- `hooks/smoke-test` (one new section; no existing assertion weakened).

`capability-gate` and `capability-evidence` are **wired, not modified**: all three
of Trae's events reuse the existing scripts and the existing deny/evidence shapes,
so no hook script gains a host branch.

## Out of Scope

- Any `.trae-plugin/` directory or `~/.trae-cn/` global install. Trae documents no
  manifest for either, and inventing one would dress a guess as a convention.
- A `PostToolUse` matcher for `Agent|Task` in the Trae file. Trae's tool table has
  no such tool, so the entry would be dead config; `Skill` and `mcp__.*` are the
  capability paths Trae actually exposes.
- Committing `.trae/skills/`, `.trae/hooks.json`, or symlinks. This repository is
  not a Trae project; a committed copy is a second skill tree that drifts, and a
  symlink does not survive a Windows checkout.
- `.gitignore` changes. Nothing new is generated inside the repository.

## Risks / Deferred Items

- **The Trae wiring has never run on a live host.** Every Trae statement here is
  from `docs.trae.cn` as read on 2026-10-09, while the repository's practice is to
  write each host contract from a measurement (the CodeBuddy notes, the Claude Code
  2.1.282 note). Consequence specific to wiring the gate: Trae's `tool_input` field
  names inside `PreToolUse`/`PostToolUse` are not documented in the same detail as
  Claude Code's, and `json-field` reads a fixed field list (`tool_input.file_path`,
  `tool_input.skill`, `tool_input.subagent_type`). A denial that never fires, or an
  evidence line that never records, is silent by design in both hooks — so this is
  the one thing the live test must check first, and the runtime reference must send
  the tester there. The user has a Trae machine available for that follow-up.
- **`CLAUDE_PROJECT_DIR` is Trae's variable, not ours.** If Trae renames it, this
  wiring breaks silently, because nothing in this repository can run Trae. The
  smoke test pins only the spelling this repository wrote.
- **`.trae/skills/` is a copy.** A user who copies once does not pick up a later
  skill change; the install step must say to re-copy after an update.
- **Trae's `PreToolUse` can `ask`.** Trae documents a third decision Trae itself can
  interpose; the gate only ever denies, so the two cannot disagree, but a reader
  comparing the files should not expect the Trae file to mirror Claude Code's
  permission surface beyond `deny`.

## Open Questions

None.

## Version History

- v1 — planning.
