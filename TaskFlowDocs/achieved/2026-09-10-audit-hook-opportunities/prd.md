# Audit further Hook automation opportunities
> Task version: v1
> Status: completed

## Goal

Identify TaskFlow operations that can be made deterministic and cheaper without moving semantic decisions, approvals, or destructive actions into Hooks.

## Requirements

- Compare current TaskFlow mechanics with current Claude Code and Codex Hook events.
- Separate automatic Hooks from explicit deterministic lifecycle scripts.
- Rank candidates by token savings, correctness benefit, cross-host feasibility, and false-positive risk.
- Do not implement or configure new Hooks.

## Acceptance Criteria

- Each recommendation names its trigger, behavior, mutation boundary, and reason.
- Unsafe or low-value candidates are explicitly rejected.
- Recommendations preserve Agent tool choice and user approval boundaries.

## Scope

- In scope: `hooks/`, TaskFlow lifecycle rules, Claude Code Hooks, Codex Hooks.
- Out of scope: implementation, installation, trust approval, user-level configuration, commit, and push.

## Version History

- v1 — read-only Hook opportunity audit.
