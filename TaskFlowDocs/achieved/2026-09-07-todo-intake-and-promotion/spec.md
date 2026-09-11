# Spec — Todo intake and promotion workflow
> Task version: v1

## Objective and Success Criteria

Provide one low-friction inbox for uncommitted work and a deterministic promotion path into TaskFlow's authoritative task directory. Once promoted, PRD/Spec/Plan own the facts; the Todo keeps only a pointer and lifecycle status.

## Proposed Data Model

```markdown
## T-YYYYMMDD-001 — Short title
- Status: inbox | clarified | promoted | in_progress | done | cancelled
- Priority: low | normal | high | urgent
- Owner: <person or Agent>
- Source: <user / review / issue / remote>
- Goal: <one sentence>
- Task: <TaskFlowDocs/<task-id>/ or None>
- Next: <single next clarification or implementation action>
- Updated: YYYY-MM-DD
```

## Promotion Contract

1. `inbox`: capture only; no implementation assumptions.
2. `clarified`: goal, scope, acceptance, owner, and applicable standards are known; unresolved decisions are explicit.
3. `promoted`: create `TaskFlowDocs/<task-id>/prd.md` and `plan.md`; create `spec.md` when the large-task rule applies.
4. `in_progress`: enter only after Plan approval; update Todo with the task path.
5. `done` or `cancelled`: close the Todo item after task completion or explicit cancellation, retaining the task link and reason.

Promotion is not automatic merely because an item is old or high priority. The Agent asks the minimum clarifying questions needed, then applies the normal PRD/Spec/Plan approval gate.

## Plan Checklist Contract

Every Plan Step includes a checkbox list under `Implementation checklist`. A Step may become `done` only when every required checkbox is checked and its focused verification passes. Checklists may include implementation, docs, tests, review, and rollback confirmation.

## Boundaries

- Always: keep one Todo inbox; link promoted items to one task directory; preserve acceptance and verification.
- Ask first: deleting Todo history, changing item identity, splitting one item into multiple tasks, or promoting across repositories.
- Never: duplicate PRD/Spec/Plan facts in the inbox, mark a Todo done before task acceptance, or bypass approval.
