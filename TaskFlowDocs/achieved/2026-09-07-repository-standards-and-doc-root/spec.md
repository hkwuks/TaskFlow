# Spec — Repository standards and TaskFlowDocs root
> Task version: v3

## Objective and Success Criteria

TaskFlow has one repository-local documentation root. Standards are indexed in one file, loaded selectively, and applied to task planning, implementation, commits, and PR preparation. If a relevant rule does not exist, the Agent guides the user to establish or waive it before implementation.

## Architecture Boundaries and Responsibilities

- `TaskFlowDocs/standards/index.md`: manifest, applicability, precedence, and sync metadata.
- Linked standards files: repository-owned rules grouped by concern (`code.md`, `commits.md`, `design.md`, `development.md`, or repository-specific names).
- `taskflow/SKILL.md`: lifecycle instructions that discover and apply standards.
- README/reference files: user-facing explanation and path examples.

## Interfaces, Data Flow, and Contracts

1. At triage, inspect `TaskFlowDocs/standards/index.md` if present; an absent index means no repository-specific standards are declared.
2. Determine applicable categories from the task: development process for non-trivial work; code for code changes; commits and PR rules for commit/remote work; design for architecture, UX, API, or data-contract decisions.
3. If an applicable category is missing, incomplete, or unwaived, pause planning or implementation and guide the user in batches of at most three dependency-ordered questions. Give a recommended answer for each. The default order is development process, code, commits/PR, then design.
4. After confirmation, create only the selected files and add their links to the index. Every file states scope, rules, verification, and exceptions/change control; `commits.md` also states commit format and PR checks.
5. Load only standards marked applicable to the current task and phase.
6. Local repository standards take precedence over generic TaskFlow guidance when they do not conflict with safety or explicit user requirements; conflicts are surfaced rather than guessed.
7. For remote PR work, identify the host from `git remote -v`, inspect available PR templates, contribution guides, CODEOWNERS, branch/CI rules, and host metadata when accessible. Treat findings as candidate until reviewed, then record the source and incorporated conclusion in the index or linked note.
8. Never copy secrets, tokens, private data, or opaque remote payloads into standards files.
9. A user message that corrects, rejects, adds to, or materially changes an approved requirement, design, standard, scope, compatibility decision, risk, or implementation path is a change event. Stop the current phase, archive the current version, update all existing core documents atomically, set the task to `ready`, and obtain approval before resuming.

## Validation and Error Semantics

- Missing standards index: continue with generic TaskFlow rules and record that no local standards were found.
- Missing applicable standard: ask the standards-bootstrap questions and wait for user decisions; an explicit user waiver is recorded in `index.md` and the task `plan.md`.
- Unavailable remote or insufficient permissions: continue without sync, record the limitation, and do not claim synchronization completed.
- Conflicting rules: pause the affected decision and ask the user; do not silently merge precedence.
- User material change: pause immediately; do not update just one named document or continue under stale PRD/Spec/Plan facts.

## Code and Test Constraints

This change is documentation-only. Validate with repository-wide searches for stale `tasks/` references and inspect all changed Markdown/SVG files.

## Design Decisions and Alternatives

- Use a Markdown index instead of a config schema: readable, diffable, and no parser required.
- Use discovery plus reviewed incorporation instead of provider API automation: works across hosts and avoids hidden writes.
- Do not keep a compatibility alias for `tasks/`: the user requested a complete migration.
