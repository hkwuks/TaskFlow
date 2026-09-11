# Plan — Support host/harness hooks in TaskFlow
> Task version: v2
> Status: completed

## Spec Pointers

- `spec.md`

## Reference Pointers

- `TaskFlowDocs/achieved/2026-09-08-token-efficiency/` (T-006 foundation).
- Claude Code hooks reference (docs.anthropic.com) and Codex Hooks guide (learn.chatgpt.com/docs/hooks, plus openai/codex repo schemas) — verified event names, config locations, and output contract.
- `obra/superpowers/hooks` — the reference hook layout adopted in v2: flat `hooks/`, extensionless bash scripts, one hook JSON per host, polyglot `run-hook.cmd` cross-platform launcher (user-provided reference).

## Related Tasks

- Depends on: `TaskFlowDocs/achieved/2026-09-08-token-efficiency/`
- Blocks: None
- Related: `2026-09-07-repository-docs-workspace` (achieved), `2026-09-07-tool-participation` (achieved; tool-agnostic capability rule)

## Skills / Tools Used (Optional)

- `taskflow` — established artifact, approval, versioning, and safety constraints.
- Host hook references (Claude Code + Codex) — event names, config locations, output fields, and caps.

## Preconditions

- User approval of v1 PRD / Spec / Plan recorded below before implementation.

## Approval

- Approved by: user
- Approved at: 2026-09-08 23:20 +08:00
- Approved version: v2
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Replace the "non-runtime" claim with host-hook support
- Goal: README EN/zh and SKILL.md no longer claim no-interception; they state host/harness hooks (Claude Code + Codex, additive) may do bounded bookkeeping and context with explicit prohibitions.
- Dependencies: v1 approval.
- Files: `README.md`, `README.zh-CN.md`, `taskflow/SKILL.md` (intro, non-invasive table, comparison table, Safety and scope).
- Implementation checklist:
  - Rewrite the intro callout in both READMEs and SKILL opening to a positive bounded statement naming Claude Code and Codex CLI as supported hosts (additive).
  - Update non-invasive/comparison tables and Safety bullet that forbid hooks.
  - Add pointer to `runtime.md`.
- Acceptance: `rg` shows no remaining "does not intercept / no runtime hooks / not an Agent runtime" claim in the three files.
- Verification: `rg` scan + `git diff --check`.
- Rollback: revert the three files' claim edits.
- Status: done

### Step 2 — Write `taskflow/references/runtime.md`
- Goal: single owner of host-hook rules: definitions, event map (Claude Code | Codex), must/may-not list, single-command transitions.
- Dependencies: Step 1.
- Files: `taskflow/references/runtime.md` (new).
- Implementation checklist:
  - Define "host/harness hook" and the additive supported-host rule.
  - Event map table with Claude Code and Codex columns pinned to referenced docs.
  - Must/may-not list (Todo triage updates allowed; core-document writes and approval forbidden).
  - Single-command archive/version/reopen contracts with verification steps.
  - Hook folder layout and install snippets for both hosts.
- Acceptance: PRD acceptance criteria for runtime.md all covered.
- Verification: review against PRD Requirements list.
- Rollback: remove the new file.
- Status: done

### Step 3 — Add flat hook scripts + single-command transitions under the skill (v2)
- Goal: `taskflow/hooks/` in the `obra/superpowers/hooks` shape — extensionless bash scripts, one hook JSON per host, cross-platform `run-hook.cmd`; `archive` is a full transaction (move task → update Todo path/status → verify locations and root statuses).
- Dependencies: Step 2 (v2).
- Files: `taskflow/hooks/README.md`, `hooks.json`, `hooks-codex.json`, `run-hook.cmd`, `session-start`, `summarize-state`, `archive`, `version`, `reopen`, `smoke-test` (new).
- Implementation checklist:
  - `summarize-state` shared summary generator (extensionless bash) + `session-start` platform-shaped entry (Claude Code / Cursor / Copilot context JSON), mirroring superpowers.
  - `archive` full transaction + `version` (changed docs only) + `reopen` scripts.
  - `run-hook.cmd` polyglot launcher (finds Git Bash on Windows; no-op on Unix).
  - Per-host JSON: `hooks.json` (Claude Code), `hooks-codex.json` (Codex, with `commandWindows`).
  - `smoke-test` assert-style checks for all of the above.
- Acceptance: scripts are extensionless bash; `smoke-test` passes; `session-start` emits platform JSON; `archive` updates Todo; mirror identical.
- Verification: `bash smoke-test <tmp>`; host entry JSON check; `diff -q` mirrors.
- Rollback: remove `taskflow/hooks/` additions.
- Status: done

### Step 4 — SKILL pointers and mirror installed skill
- Goal: SKILL references runtime.md and hooks/; installed skill matches repo copies.
- Dependencies: Steps 1–3.
- Files: `taskflow/SKILL.md` (Supporting references), mirrors.
- Implementation checklist:
  - Add `runtime.md` and `hooks/` to Supporting references.
  - Ensure Safety and scope says hooks never write core documents or approve.
  - Mirror all skill files + hooks dir to the installed copy.
- Acceptance: repo and installed skill files identical.
- Verification: `diff -q` recursive.
- Rollback: revert SKILL pointers and re-mirror.
- Status: done

## Checkpoints

- Before editing: user approval of v1 PRD / Spec / Plan.
- Before completion: no stale no-runtime claims; runtime.md + hooks folders present; mirror identical; verification recorded.

## Verification / Review

### Acceptance checklist (from PRD v2)

- [x] README EN/zh and SKILL no longer claim "non-runtime"/"no hooks"; each states hooks are allowed for bounded bookkeeping + context with prohibitions, names Claude Code + Codex CLI, and is additive. `rg` across README/zh/SKILL for `does not intercept|not an Agent runtime|no runtime hooks` → clean.
- [x] `taskflow/references/runtime.md` exists: host-hook definition, additive supported-host rule, event map (Claude Code | Codex), must/may-not list, single-command transitions, folder layout (flat superpowers shape).
- [x] `taskflow/hooks/` exists in the `obra/superpowers/hooks` shape: flat dir, extensionless bash scripts (`session-start`, `summarize-state`, `archive`, `version`, `reopen`), one JSON per host (`hooks.json`, `hooks-codex.json`), `run-hook.cmd` cross-platform launcher.
- [x] Cross-platform: bash through polyglot `run-hook.cmd` on Windows (Git Bash), native on Unix; no python runtimes required (matches the user's bash + Windows-variant selection, not Python).
- [x] Single-command transitions landed: `archive` performs the full transaction incl. Todo path/status update + verify; `version` archives only changed core docs; `reopen` restores + change-log line.
- [x] Hooks never write core documents or approve: SKILL Safety bullet states it; `session-start`/`summarize-state` write nothing; transitions run explicitly and never touch approval.
- [x] Todo item T-20260908-007 promoted and linked.

### Checks run (v2)

- `bash taskflow/hooks/smoke-test <tmp>` → ALL SMOKE PASSED (summarize-state empty, session-start platform JSON, archive happy path incl. Todo, reopen, version changed-docs-only).
- Real-repo host entry: `CLAUDE_PLUGIN_ROOT=… bash taskflow/hooks/session-start` → valid `hookSpecificOutput.additionalContext` JSON with inbox + active tasks.
- `diff -qr` repo `taskflow/hooks` + `references/runtime.md` vs installed skill copy → identical; installed-copy `smoke-test` also passes.
- `git diff --check` clean.

## Follow-ups

- Hook installation for this repository remains a deployment decision outside this task (per PRD Out of Scope).

## Version History

- v1: Support host/harness hooks (Claude Code + Codex), per-host hook folders, SessionStart summary, single-command archive/version/reopen transactions (archive includes the Todo update); reverse the non-runtime claim.
- v2: Replaced per-host subfolders + python with the flat `obra/superpowers/hooks` shape (extensionless bash, `hooks.json` + `hooks-codex.json`, `run-hook.cmd`), per user reference and bash+Windows selection.

## Change Log
- 2026-09-08 reopen — retrieved achieved task `2026-09-08-runtime-hooks` for new work; re-approval required before core changes
- 2026-09-08 v2 — per user reference, replaced per-host python folders with the flat `obra/superpowers/hooks` bash layout; re-approved v2 PRD/Spec/Plan.
