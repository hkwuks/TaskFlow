# Repository-governed fork development

- Task version: v2
- State: in_progress
- Owner: user / TaskFlow

## Goal

Make TaskFlow consistently discover, apply, and—when needed—help create repository governance before implementation, with explicit fork/upstream discipline and user approval for new or materially changed governance documents.

## User value

Developers get changes that follow the target repository's actual conventions instead of generic Agent defaults. Repositories missing basic discipline gain small, evidence-based governance documents without fabricated policy or silent Git/remote mutations.

## Background / Confirmed facts

- The TaskFlow plugin root contains Claude and Codex manifests, one TaskFlow Skill, lifecycle hooks, and bilingual README guidance.
- `TaskFlowDocs/repository-docs/index.md` already catalogs repository rules, guidance, and personal supplements.
- Existing rules make repository documents authoritative and prohibit personal supplements from weakening or overriding them.
- Existing rules inspect remote and PR guidance when work targets a remote, but do not define a complete fork/upstream decision flow.
- This repository currently has only `origin`, with `origin/main` as the available baseline; it has no configured `upstream`.
- This repository has no `CONTRIBUTING.md`, `CODE_STYLE.md`, or `ROADMAP.md`.
- The user confirmed that TaskFlow should help create missing governance documents to maintain sound development discipline.
- The current active `2026-09-07-tool-participation` task is in checking and has a different deliverable; this is an independently releasable task.

## Assumptions

1. “Fork development standard” means validating remote topology, intended target repository and base branch, local branch origin, applicable contribution rules, and pre-PR checks—not automatically creating remotes, fetching, rebasing, pushing, or opening a PR.
2. Governance discovery and drafting happen before implementation; a new or materially changed governance document becomes authoritative only after explicit user approval.
3. `CONTRIBUTING.md` and `CODE_STYLE.md` are baseline governance for non-trivial development. `ROADMAP.md` is created only after the user confirms product direction. Other governance documents are task-dependent.
4. Generated governance must be minimal and repository-specific; empty templates and invented policies do not satisfy the requirement.

## Requirements

13. Provide a read-only `hooks/repository-check` command that reports repository governance and fork/remote readiness as `pass`, `needs-user-input`, or `blocked`.
14. The command must inspect local files and Git metadata without creating documents, modifying remotes, fetching, rebasing, merging, pushing, or opening PRs.
15. Keep the command opt-in; do not attach it to `session-start` or other automatic hooks in v2.

1. Before planning or implementing non-trivial repository work, TaskFlow must discover applicable repository-owned documents and scoped personal supplements, including README, contributing, code style, roadmap, release, code of conduct, PR templates, CODEOWNERS, branch rules, and CI guidance.
2. TaskFlow must apply sources in this order: repository rules and guidance first; compatible, scope-matched personal supplements second. A conflict stops work for user resolution.
3. For Git remote, fork, or PR work, TaskFlow must identify configured remote topology, intended target repository, base branch, local branch/base relationship, available remote-host guidance, and the checks required before submission.
4. Remote discovery must not silently add or rewrite remotes, fetch, rebase, merge, push, or claim synchronization. When the target or baseline cannot be established from current evidence, TaskFlow asks the user before continuing.
5. When baseline governance is missing for non-trivial development, TaskFlow must help create `CONTRIBUTING.md` and `CODE_STYLE.md` at conventional repository locations before implementation.
6. TaskFlow creates `ROADMAP.md` only after the user confirms product direction. README, PR templates, CODEOWNERS, CI, release, code-of-conduct, or other governance is created only when the task needs it.
7. A governance draft must derive rules from verifiable repository evidence first: language and framework, manifests, build/test/lint scripts, CI, existing code patterns, Git history, and remote-host rules. Only undecidable policy is asked of the user, at most three dependency-ordered questions per turn with recommendations.
8. Every created governance document must be concise, actionable, repository-specific, and contain concrete commands or checks where evidence supports them. TaskFlow must not create an empty template or fabricate roadmap/product policy.
9. Creating or materially changing a repository governance document requires its own explicit user approval. The task Plan records its evidence and proposed effect before it governs implementation.
10. `TaskFlowDocs/repository-docs/personal/` remains limited to personal habits or stricter compatible preferences. It cannot substitute for missing repository-owned governance.
11. The document catalog must be refreshed after governance is created, moved, removed, or materially changed, and the current task Plan must record applicable sources and incorporated conclusions.
12. English and Chinese public documentation must describe the same behavior.

## Acceptance criteria

- `hooks/repository-check` runs on a repository and emits deterministic status plus actionable findings for missing governance, ambiguous remote/base, and applicable checks.
- The command has focused smoke coverage and is documented in both READMEs.
- No automatic hook invokes the command.

- The Skill provides one dependency-ordered workflow for repository-document discovery, precedence, missing-document creation, approval, and catalog refresh.
- The Skill provides an explicit fork/upstream workflow that works for direct clones and forks without assuming remote names or mutating remotes.
- A non-trivial task cannot enter implementation while required baseline governance is missing or an applicable governance draft awaits approval.
- `CONTRIBUTING.md` and `CODE_STYLE.md` creation rules are evidence-first and mandatory when absent for non-trivial development; `ROADMAP.md` remains direction-gated.
- Personal supplements remain scoped, compatible additions rather than substitutes for repository policy.
- Task artifacts record reviewed source paths, remote/base conclusions, missing governance, draft evidence, approval state, and required checks without storing secrets or opaque remote payloads.
- README English and Chinese descriptions remain aligned.
- Focused validation, hook smoke tests, whitespace checks, and review of the changed documentation all pass.

## In scope

- `skills/taskflow/SKILL.md` operational rules.
- Task artifact/template guidance needed to record governance and fork decisions.
- English and Chinese README documentation.
- Focused smoke-test assertions for durable textual contracts where appropriate.

## Out of scope

- Creating this repository's own missing `CONTRIBUTING.md`, `CODE_STYLE.md`, or `ROADMAP.md` as part of this plugin-rule task.
- Automatically adding or changing Git remotes, fetching, rebasing, merging, pushing, forking, or opening PRs.
- Calling hosting-provider APIs automatically or defining provider-specific recipes.
- Compatibility shims for previous behavior.
- Changing plugin manifests unless validation proves they must change.

## Risks and deferred items

- Over-prescription could block tiny changes; the governance gate applies to non-trivial work, while trivial changes still use applicable existing rules.
- Repository evidence may be inconsistent. Conflicts are surfaced rather than resolved by guessing.
- Remote-tracking refs may be stale. TaskFlow records that limitation and requests authorization when a freshness-changing operation is necessary.
- Governance quality cannot be guaranteed from filenames alone; approval and evidence recording are required.

## Repository documents inspected

- `README.md` — applicable repository guidance and current public contract.
- `README.zh-CN.md` — applicable bilingual public contract.
- `skills/taskflow/SKILL.md` — authoritative TaskFlow workflow rule.
- `TaskFlowDocs/repository-docs/index.md` — current catalog; missing contributing, code-style, release, roadmap, and code-of-conduct sources.
- `TaskFlowDocs/repository-docs/personal/README.md` — personal supplement boundary.
- Git remote, branch, tracked-file, and recent commit metadata — fork baseline and repository conventions.

## Open questions

None.

## Version history

- v1 — Initial contract from the user's six confirmed decisions on scope, remote safety, missing governance, evidence, and approval.
- v2 — Added approved read-only governance-check command; automatic hook integration explicitly deferred.
