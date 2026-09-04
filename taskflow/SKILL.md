---
name: taskflow
description: "Manage a task through the project's task-directory workflow: clarify requirements, create PRD, decide whether a large task needs a Spec, plan implementation, verify results, record sessions, and archive completed work. Use for non-trivial feature, bug, refactor, research, or documentation tasks that need durable task artifacts."
---

# TaskFlow

Use this skill as the single entry point for the project's task framework. It defines where task facts live and how work moves through the lifecycle. Other Skills and tools are optional collaborators; when used, their task outputs should be routed into the current task directory.

## Source of truth

For an active task, the task directory is:

```text
tasks/YYYY-MM-DD-short-slug/
```

Required artifacts:

- `prd.md` — goal, requirements, scope, and observable acceptance criteria.
- `plan.md` — current Task version, state, approval, steps, progress, verification, review, risks, rollback, and follow-ups.

Conditional artifacts:

- `spec.md` — required for a large task; optional for a small, self-contained task.
- `reference/` — optional research and evidence. Create `reference/index.md` only when the material is numerous enough to need navigation.
- `sessions.md` — optional session/resume index when work spans sessions or agents.
- `old/vN/` — only for a superseded logical version.

Never create a second task fact source such as a root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, or an automatic review file for the same task unless the project explicitly defines one.

## Triage and lifecycle

First inspect the repository, applicable project rules, existing tasks, tests, configuration, Git state, and uncommitted changes. Separate findings into confirmed facts, user decisions, technical unknowns, and explicit exclusions.

Choose the lightest path that preserves traceability:

```text
small, obvious one-file change → direct change + minimal verification
non-trivial task              → planning workflow below
```

For a non-trivial task:

```text
planning → ready → in_progress → checking → completed
    │                         │
    └──────── blocked ◄────────┘
```

- `planning`: requirements, evidence, or design are still being clarified.
- `ready`: PRD, required Spec, and Plan are complete and awaiting user approval.
- `in_progress`: the user approved the current Task version; implementation is allowed.
- `checking`: implementation is done and acceptance/quality verification is running.
- `blocked`: a concrete blocker is recorded with reproduction, attempts, and needed input; resume the prior phase when cleared.
- `completed`: acceptance and verification passed. Then move the entire task directory to `tasks/achieved/<task-id>/`.

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

Create or update `plan.md`. Route generic planning outputs such as `tasks/plan.md` or `tasks/todo.md` into this task's `plan.md`. Each Step should include:

- goal;
- dependencies;
- files likely touched;
- implementation checklist;
- acceptance;
- focused verification command or manual check;
- rollback point;
- status: `pending | in_progress | done | blocked`.

Include checkpoints after meaningful groups of steps. Record risks, deviations, verification results, review findings, and unresolved follow-ups. If other Skills or tools were used, optionally record their names and role.

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

If another tool or Skill creates files, review and route them before treating them as task facts. Do not let automation skip approval, expand scope, delete history, or write secrets.

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

Before moving the task to `tasks/achieved/`, confirm all acceptance criteria pass, verification is recorded, the current Task version is consistent across existing core documents, unresolved items are explicit follow-ups, and no other agent is writing core documents. Mark the task `completed`, then move the entire directory. Keep `old/` history. Treat achieved tasks as read-only; create a related new task for new goals, or reopen only with user confirmation and a recorded reason.

After completion, promote only verified, cross-task rules into the project's shared specification/guides. Leave task-specific decisions, personal preferences, unverified ideas, and temporary workarounds in the task artifacts.

Publishing, merging, deployment, or delivery processes managed by other tools are external to this framework. They may be not applicable and do not replace `completed` or `tasks/achieved/`.

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
- [ ] Completion gates passed before moving to `tasks/achieved/`.
