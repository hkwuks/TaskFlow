# Todo intake and promotion workflow
> Task version: v1
> Status: completed

## Goal

Define a lightweight Todo list that captures ideas without becoming a second source of truth, then promotes a selected Todo item into a TaskFlow task with PRD, optional Spec, and Plan. Make Plan steps executable through explicit checklists.

## Background / Confirmed Facts

- TaskFlow currently routes generic todo/task-list output into a task's `plan.md` and discourages a global `TaskFlowDocs/todo.md`.
- The user requested a maintained Todo list that can evolve into PRD, Spec, and Plan.
- Plan steps already require an implementation checklist in the Skill, but the artifact template does not show one consistently enough.

## Requirements

1. Define one Todo inbox location and item schema with status, priority, source, owner, links, and promotion target.
2. Define promotion states: inbox → clarified → promoted → in_progress → done/cancelled, with no duplicate task fact source after promotion.
3. Define the trigger and gate for promotion: clarify goal, scope, acceptance, size, dependencies, and applicable standards before creating PRD/Spec/Plan.
4. Define when a Todo remains a Todo, when it gets a small task, and when it requires a large-task Spec.
5. Define how promoted items link back to the Todo and how completion archives or closes the Todo item.
6. Add a concrete checklist subsection to the Plan template and require checklist completion before a Step is done.
7. Synchronize the mechanism across Skill, artifact reference, workflow draft, and both READMEs.

## Acceptance Criteria

- A repository can create and maintain a single documented Todo inbox without duplicating task facts.
- A Todo item has a documented path to PRD, Spec decision, and Plan with explicit gates and statuses.
- The Plan template contains checklist items with completion semantics, not only prose fields.
- Promotion, linking, cancellation, and completion behavior are documented consistently.

## In Scope

- Markdown-based Todo inbox contract and promotion workflow.
- Plan checklist template and lifecycle documentation.

## Out of Scope

- A CLI, database, hosted issue tracker, background watcher, or automatic task creation.
- Requiring every Todo item to become a PRD.

## Risks / Deferred Items

- A single Markdown inbox can become noisy at high volume; split by repository or adopt an external tracker only when search/ownership becomes a measured problem.

## Open Questions

- None. User approved `TaskFlowDocs/todo.md`, the status flow, item fields, and mandatory Plan Step checklists.

## Version History

- v1 — initial Todo promotion and Plan checklist design task.
