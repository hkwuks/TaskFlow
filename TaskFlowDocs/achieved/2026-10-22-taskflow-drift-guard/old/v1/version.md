# Archived Version v1 — Plan — Keep a mid-implementation request inside the workflow
> Task: 2026-10-22-taskflow-drift-guard
> Version: v1
> Status: superseded
> Archived: 2026-10-22 22:48 +0800
> Superseded by: v2
> Archive mode: file

## Change Summary
Wiring widened from Claude Code alone to all five hosts this repository ships hook
wiring for. v1 justified the narrow scope by saying the prompt-submit contract was
established for Claude Code only; checking the other hosts' own references contradicted
that — CodeBuddy, Trae and Codex CLI all document `UserPromptSubmit` injecting
`hookSpecificOutput.additionalContext`, and dsh documents an `agent/prompt-submit`
waterfall carrying `additionalContext` that maps onto it. R7 now requires every shipped
host to get the reminder under its own event name with its own recorded standing, and the
new R1a states that the `SKILL.md` wording — not the hook — is the whole fix for a host
with no wiring at all. Per-host risks (Codex hook trust, Trae's `cwd`-less event) were
added to the PRD; the Spec's D3 was rewritten with the host table and three rejected
alternatives.

## Archived Materials
- prd.md
- spec.md

## Restore
Read the archived v1 core docs from a new temporary restore root. Do not overwrite the current task root.
