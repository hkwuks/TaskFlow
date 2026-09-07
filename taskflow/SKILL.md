---
name: taskflow
description: "Manage a task through the project's task-directory workflow: clarify requirements, create PRD, decide whether a large task needs a Spec, plan implementation, verify results, record sessions, and archive completed work. Use for non-trivial feature, bug, refactor, research, or documentation tasks that need durable task artifacts."
---

# TaskFlow

Use this skill as the single entry point for the project's task framework. It defines where task facts live and how work moves through the lifecycle. TaskFlow does not select tools: during clarification, PRD, Spec, Plan, research, and review work, first check the capabilities currently available to the Agent and use any that materially help. Review and route only incorporated task facts into the current task directory.

## Source of truth

For an active task, the task directory is:

```text
TaskFlowDocs/YYYY-MM-DD-short-slug/
```

Repository documents are cataloged at `TaskFlowDocs/repository-docs/index.md`; repository standards live at `TaskFlowDocs/repository-docs/standards/index.md`. Before planning or implementing a non-trivial task, inspect the catalog and standards index, then load only linked standards applicable to the task or phase. If the catalog or an applicable standard is missing, incomplete, or not explicitly waived, use the document-environment and standards-bootstrap rules below before implementation.

The repository Todo inbox is `TaskFlowDocs/todo.md`. It is a triage source only, not a second source of task facts. Promoted items link to exactly one `TaskFlowDocs/<task-id>/` directory, where PRD, Spec, Plan, and verification become authoritative.

Required artifacts:

- `prd.md` — goal, requirements, scope, and observable acceptance criteria.
- `plan.md` — current Task version, state, approval, steps, progress, verification, review, risks, rollback, and follow-ups.

Conditional artifacts:

- `spec.md` — required for a large task; optional for a small, self-contained task.
- `reference/` — optional research and evidence. Create `reference/index.md` only when the material is numerous enough to need navigation.
- `sessions.md` — optional session/resume index when work spans sessions or agents.
- `old/vN/` — only for a superseded logical version.

Never create a second task fact source such as a root `SPEC.md`, `TaskFlowDocs/plan.md`, or an automatic review file for the same task. `TaskFlowDocs/todo.md` is the sole repository Todo inbox; it contains triage metadata only and never duplicates promoted task facts.

## Triage and lifecycle

First inspect the repository, `TaskFlowDocs/repository-docs/index.md`, `TaskFlowDocs/repository-docs/standards/index.md`, applicable project rules, existing TaskFlowDocs tasks, tests, configuration, Git state, and uncommitted changes. Separate findings into confirmed facts, user decisions, technical unknowns, and explicit exclusions.

When work targets a pull request or Git remote, inspect the configured remote and available repository-host guidance such as contribution guides, PR templates, CODEOWNERS, branch or CI rules, and host metadata. Route reviewed conclusions into `TaskFlowDocs/repository-docs/standards/index.md` or a linked standards note. Do not silently overwrite local rules, claim synchronization when access fails, or copy secrets, tokens, private data, or opaque remote payloads.

### Repository document environment

`TaskFlowDocs/repository-docs/index.md` is derived navigation, not a source of rules. Before non-trivial work, refresh its catalog only when it is absent, stale, or the task phase needs a document class not cataloged. Discover README, contributing, code style, release, roadmap, code of conduct, PR template, CODEOWNERS, branch/CI, and standards documents. Record each class, repository-relative source path, access mode (`symlink` or `index`), existence, and last-checked date. Add an unrecognized candidate document only after user confirmation.

Use a relative symbolic link only when its source exists inside the repository and both platform and Git support links. Otherwise, retain a usable repository-relative path in the catalog; never copy source contents or create a fake link. Source documents are authoritative. Refresh the catalog after their addition, removal, move, or relevant change. If a changed source rule affects approved work, apply the user-change trigger before continuing.

Select documents by phase: code work uses code style and contributing guidance; commits/PRs use contributing, commit rules, PR templates, CODEOWNERS, and branch/CI rules; design/API/UX work uses design standards, architecture guidance, and relevant README behavior; release work uses release/changelog guidance; roadmap work uses roadmap and README. Record applicable documents and incorporated conclusions in the task `plan.md`. Missing document classes are informational unless the task needs a repository rule that is absent, in which case use the standards bootstrap.

### User-change trigger

Treat a user message that corrects, rejects, adds to, or materially changes an approved goal, requirement, acceptance criterion, scope, design, standard, compatibility decision, risk, or implementation path as a change event. Stop the current phase immediately. Do not update only the document named by the user or continue under stale PRD, Spec, or Plan facts.

Classify the change. For a material change, archive the current Task version, update every existing core document atomically to `vN+1`, return the task to `ready`, and record a new approval before implementation resumes. For a work revision, synchronize only affected current documents and record the revision in `plan.md`. A completed task is read-only: create a related task unless the user explicitly authorizes reopening, then record the reason before changing it.

### Standards bootstrap

When applicable repository standards are missing or incomplete, pause implementation and guide the user to define them. Ask no more than three dependency-ordered questions per turn, with a recommendation for each. Use this order unless the task makes another order necessary: development process, code, commits/PR, then design. Ask only for categories applicable to the task.

After the user confirms, create only the selected files under `TaskFlowDocs/repository-docs/standards/` and link them from its `index.md`. Each file must define its scope, rules, verification method, and exceptions/change control. `commits.md` must additionally define commit format and PR checks. If the user explicitly waives an applicable category, record the waiver in `index.md` and the task `plan.md`; do not create an empty file.

### Todo → PRD → Spec → Plan

Use `TaskFlowDocs/todo.md` for ideas and requests that are not ready for planning. Maintain each item with an ID, status, priority, owner, source, one-sentence goal, task link, next action, and update date. Move it through `inbox → clarified → promoted → in_progress → done/cancelled`.

Keep an item in `inbox` while its intent is unknown. Move it to `clarified` only after goal, scope, acceptance, dependencies, size, and applicable standards are explicit. On promotion, create `prd.md`, decide whether `spec.md` is required, create `plan.md`, and link the task path back in the Todo item. Do not duplicate requirements or design in the inbox. Enter `in_progress` only after Plan approval; mark `done` only after task acceptance and verification, or `cancelled` with a reason.

Choose the lightest path that preserves traceability:

```text
small, obvious one-file change → direct change + minimal verification
non-trivial task              → planning workflow below
```

Checking available capabilities does not require invoking one or recording an empty result. TaskFlow does not name a required tool, vendor, Skill family, or invocation mechanism.

For a non-trivial task:

```text
planning → ready → in_progress → checking → completed
    │                         │
    └──────── blocked ◄────────┘
```

- `planning`: requirements, evidence, design, or applicable standards are still being clarified.
- `ready`: PRD, required Spec, and Plan are complete and awaiting user approval.
- `in_progress`: the user approved the current Task version; implementation is allowed.
- `checking`: implementation is done and acceptance/quality verification is running.
- `blocked`: a concrete blocker is recorded with reproduction, attempts, and needed input; resume the prior phase when cleared.
- `completed`: acceptance and verification passed. Then move the entire task directory to `TaskFlowDocs/achieved/<task-id>/`.

`ready` is not approval. Do not implement until approval is recorded in `plan.md`.

## Phase routing

### 1. Define — PRD

Create `prd.md` before implementation for a non-trivial task. It must state:

- Goal and user value;
- confirmed background facts;
- requirements;
- observable acceptance criteria;
- in-scope and out-of-scope work;
- risks, deferred items, and only blocking open questions;
- current Task version and version history.

Record which repository standards were inspected and which apply. If remote PR-rule discovery was attempted, record its sources, result, and incorporated conclusions without storing sensitive payloads.

Expose assumptions and turn vague requests into testable criteria using the approach that best fits the task. Do not silently decide product, compatibility, or risk questions owned by the user.

### 2. Research — Reference (optional)

Use `reference/` only when external evidence, codebase investigation, experiments, or papers materially affect the decision. Preserve external originals; write conclusions, source status, and links in team-maintained notes. If `reference/index.md` exists, treat it as navigation, not a second requirements source.

Agent suggestions may mark evidence as candidate. Only the Primary Agent or user confirms `verified`, `rejected`, or `superseded` status.

### 3. Design — Spec decision

Classify the task before planning:

- Large: multiple modules/files, architecture/API/data-flow/compatibility/error-contract changes, multiple sessions, or roughly more than 30 minutes. `spec.md` is required.
- Small: one file, clear boundaries, one short session, and no cross-layer contract. `spec.md` may be omitted.

When omitted, put this exact decision in `plan.md`:

```text
No spec required — <brief reason>
```

For a large task, `spec.md` records architecture boundaries, responsibilities, data flow, interfaces/events/database contracts, invariants, compatibility, error semantics, design trade-offs, code patterns, and testing constraints. A multi-capability task may place a Capability Map in `prd.md` scope/overview or `spec.md` module boundaries; do not create multiple root-level Specs by default.

### 4. Plan — execution contract

Create or update `plan.md`. Route generic planning outputs such as `TaskFlowDocs/plan.md` into this task's `plan.md`; retain unpromoted Todo intake in `TaskFlowDocs/todo.md`. Each Step should include:

- goal;
- dependencies;
- files likely touched;
- implementation checklist;
- acceptance;
- focused verification command or manual check;
- rollback point;
- status: `pending | in_progress | done | blocked`.

The `Implementation checklist` is a checkbox list, not prose. A Step cannot be marked `done` until every required checkbox is checked and focused verification passes.

Include checkpoints after meaningful groups of steps. Record risks, deviations, verification results, review findings, and unresolved follow-ups. If a Skill or tool was used, record its name, purpose, and incorporated conclusion in `Skills / Tools Used`. Do not record unused-capability checks.

Record approval as:

```markdown
## Approval
- Approved by: <user / role>
- Approved at: YYYY-MM-DD HH:mm +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan
```

### 5. Build — implement by Plan

After approval, read `prd.md`, `spec.md` if present, `reference/` if present, and `plan.md`. Implement one focused Step at a time. Keep changes within the PRD scope and current Spec contracts. Update `plan.md` after each meaningful Step and run its smallest useful check.

If a requirement, design, contract, or risk changes materially, stop implementation, archive the old logical version, create the next Task version, update all existing core documents atomically, and return to `ready` for approval.

The same rule applies when the standards contract changes materially: archive the prior Task version first, update `prd.md`, `spec.md`, and `plan.md` atomically, return to `ready`, and obtain approval before implementation. Never extend a `completed` task in place.

If another tool or Skill creates files or conclusions, review and route only incorporated facts before treating them as task facts. Do not let automation skip approval, expand scope, delete history, or write secrets.

### 6. Verify and review

Enter `checking` only after implementation is complete. Verify in this order:

1. changed-file scope and Git/file archive state;
2. every PRD acceptance criterion;
3. Spec contracts when `spec.md` exists, or the `No spec required` rationale;
4. Plan steps, deviations, rollback points, and follow-ups;
5. relevant evidence in `reference/`;
6. project lint, type checks, unit/integration/end-to-end tests as applicable;
7. debug code, temporary bypasses, uncovered branches, and unrelated changes.

Record each command and result in `plan.md`. Distinguish pre-existing failures, newly introduced failures, and environment failures. A test pass does not replace product acceptance.

### 7. Complete and archive

Before moving the task to `TaskFlowDocs/achieved/`, confirm all acceptance criteria pass, verification is recorded, the current Task version is consistent across existing core documents, unresolved items are explicit follow-ups, and no other agent is writing core documents. Mark the task `completed`, then move the entire directory. Keep `old/` history. Treat achieved tasks as read-only; create a related new task for new goals, or reopen only with user confirmation and a recorded reason.

After completion, promote only verified, cross-task rules into the project's shared specification/guides. Leave task-specific decisions, personal preferences, unverified ideas, and temporary workarounds in the task artifacts.

Publishing, merging, deployment, or delivery processes managed by other tools are external to this framework. They may be not applicable and do not replace `completed` or `TaskFlowDocs/achieved/`.

## Sessions and collaboration

Use `sessions.md` only when cross-session or cross-agent continuation is useful. Record platform, session ID, availability, code working directory, task artifact directory, Task version, phase, last completed Step, next Step, status, and resume command. Do not store chat transcripts, model reasoning, full logs, secrets, or tokens.

Only one named owner may write `prd.md`, `spec.md`, `plan.md`, or `reference/index.md` at a time. Agents may read in parallel and produce independent research/review notes. The Primary Agent or user merges conclusions, changes Task version, records approval, and changes the phase. On handoff, the old owner updates `sessions.md` and `plan.md`; the new owner reads the current artifacts before writing. If a task has multiple agents, designate at most one `Primary` session.

## Safety and scope

- Do not delete, overwrite, commit, push, or archive user files unless the task and user authorization allow it.
- Do not put secrets, tokens, private data, or unauthorized sensitive material in any task artifact, snapshot, or patch; use redacted placeholders.
- Restore historical file versions only in a new temporary restore root; never overwrite the current task directory.
- Other tools are allowed to manage their own configuration and lifecycle. This skill only specifies how their task-related outputs integrate with this framework.
- A task ID is `YYYY-MM-DD-short-slug`; keep it stable after creation. Resolve same-day slug collisions with a suffix or a more specific slug. Use a new related task when the goal, deliverable, or ownership boundary materially changes.

## Supporting references

Read these only when needed:

- [artifacts.md](references/artifacts.md) for compact templates and output routing.
- [versioning-and-recovery.md](references/versioning-and-recovery.md) for Task versions, `old/`, Git/file archives, and safe restoration.

## Verification

Before declaring a task complete, confirm:

- [ ] Required artifacts exist (`prd.md`, `plan.md`; `spec.md` when large).
- [ ] Current Task version and state are consistent.
- [ ] User approval is recorded before implementation.
- [ ] Every Step has acceptance, verification, and rollback information.
- [ ] Validation results and failure classification are in `plan.md`.
- [ ] Scope, sensitive-data, and concurrent-write checks passed.
- [ ] Completion gates passed before moving to `TaskFlowDocs/achieved/`.
