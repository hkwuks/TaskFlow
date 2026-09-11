# Todo inbox

This is the repository's single lightweight intake list. It stores triage metadata only. After promotion, the linked TaskFlow directory is the sole source of requirements, design, plan, and verification facts.

## Status flow

`inbox → clarified → promoted → in_progress → done/cancelled`

## Items

<!-- Add new items at the top using the template below. -->

## T-20260910-001 — Enforce repository-governed fork development
- Status: in_progress
- Priority: high
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Make the TaskFlow plugin follow fork/upstream development discipline and applicable repository, personal-supplement, code-style, contributing, and roadmap documents, creating missing governance documents with the user when needed.
- Task: `TaskFlowDocs/2026-09-10-repository-governed-development/`
- Next: Implement the approved Skill, artifact, smoke-test, and README updates.
- Updated: 2026-09-11

## TF-20260910-08 — Reduce TaskFlow token use with lifecycle scripts
- Status: done
- Priority: high
- Owner: Codex
- Source: user request
- External: None
- Goal: Replace repetitive Agent reads and Markdown rewrites with bounded lifecycle commands where automation saves tokens.
- Task: `TaskFlowDocs/achieved/2026-09-10-token-saving-lifecycle-scripts/`
- Next: User acceptance after verified Windows full-lifecycle compatibility; archive only after explicit authorization.
- Updated: 2026-09-11

## T-20260909-002 — Restructure TaskFlow as repo-root plugin (superpowers-style)
- Status: done
- Priority: normal
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Restructure so the repo root is the plugin root (like superpowers/agent-skills): SKILL.md, hooks/, references/, agents/, and the plugin manifests move up out of the `taskflow/` subdir; marketplace `source` becomes `./`; skill loads with the plugin, no manual copy.
- Task: None — direct restructure in repo root (uncommitted; user said don't commit yet)
- Next: None — repo-root plugin validated (`claude plugin validate . --strict` PASS), locally installed from the working tree, hooks end-to-end tested (all PASS), full smoke-test suite PASS.
- Updated: 2026-09-09

## T-20260909-001 — Package TaskFlow as installable plugin (marketplace, Claude + Codex)
- Status: done
- Priority: normal
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Let users install TaskFlow by command (`claude plugin marketplace add + install`; `codex plugin add`) instead of copying skills/hooks config, following how superpowers ships per-host manifests.
- Task: None — direct change; first iteration added `.claude-plugin/` + `.codex-plugin/` under `taskflow/`, then superseded by T-20260909-002 (repo-root plugin)
- Next: None — superseded by T-20260909-002; install commands verified end-to-end on both Claude Code (`✔ enabled`) and Codex CLI (`installed, enabled`).
- Updated: 2026-09-09

## T-20260908-007 — Support host/harness hooks in TaskFlow (reverse non-runtime boundary)
- Status: done
- Priority: normal
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Allow TaskFlow to coordinate with host/harness hooks (Claude Code and Codex) via a flat `hooks/` of extensionless bash scripts + per-host JSON + `run-hook.cmd`, plus a SessionStart context summary, without automation writing core documents or skipping approval.
- Task: `TaskFlowDocs/achieved/2026-09-08-runtime-hooks/`
- Next: None — v2 completed, verified (smoke + mirror), and archived.
- Updated: 2026-09-08
- Updated: 2026-09-08
- Updated: 2026-09-08

## T-20260908-006 — Reduce TaskFlow workflow token cost
- Status: done
- Priority: high
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Reduce Agent token consumption in the TaskFlow workflow while preserving traceability and reliability.
- Task: `TaskFlowDocs/achieved/2026-09-08-token-efficiency/`
- Next: None — completed, verified, and archived.
- Updated: 2026-09-08
- Updated: 2026-09-08

## T-20260908-003 — Archive completed legacy TaskFlow tasks
- Status: done
- Priority: high
- Owner: user / TaskFlow
- Source: user-approved audit repair
- External: None
- Goal: Add Todo traceability and archive the completed standards-root and Todo-promotion tasks.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/`
- Next: None — completed and archived.
- Updated: 2026-09-08

## T-20260908-004 — Repository standards and TaskFlowDocs root
- Status: done
- Priority: normal
- Owner: user / TaskFlow
- Source: historical TaskFlow task
- External: None
- Goal: Preserve the completed repository-standards and TaskFlowDocs-root design as achieved history.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-standards-and-doc-root/`
- Next: None — completed and archived.
- Updated: 2026-09-08

## T-20260908-005 — Todo intake and promotion workflow
- Status: done
- Priority: normal
- Owner: user / TaskFlow
- Source: historical TaskFlow task
- External: None
- Goal: Preserve the completed Todo intake and promotion design as achieved history.
- Task: `TaskFlowDocs/achieved/2026-09-07-todo-intake-and-promotion/`
- Next: None — completed and archived.
- Updated: 2026-09-08

## T-20260908-002 — Repair TaskFlow activation and archival consistency
- Status: done
- Priority: high
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Ensure TaskFlow applies to every repository work request and keeps task, Todo, and achieved locations consistent.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/`
- Next: None — completed and archived.
- Updated: 2026-09-08

## T-20260908-001 — Todo-first intake and achieved-task retrieval
- Status: done
- Priority: high
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Make Todo mandatory for every direct or imported requirement and retrieve achieved tasks before material maintenance.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/`
- Next: None — completed and archived.
- Updated: 2026-09-08

## Item template

```markdown
## T-YYYYMMDD-001 — Short title
- Status: inbox | clarified | promoted | in_progress | done | cancelled
- Priority: low | normal | high | urgent
- Owner: <person or Agent>
- Source: <user / review / issue / remote>
- External: <issue number / URL / None>
- Goal: <one sentence>
- Task: <TaskFlowDocs/<task-id>/ or None>
- Next: <single next clarification or implementation action>
- Updated: YYYY-MM-DD
```

Every direct request or imported requireme
