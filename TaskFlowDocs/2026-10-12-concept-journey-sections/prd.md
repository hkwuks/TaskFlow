# Concept and journey sections for the TaskFlow template
> Task version: v1
> Status: completed

## Goal
Make the concepts a task relies on, and the states an actor can observe, into
artifacts that must be written before implementation rather than decided during
it.

## Background / Confirmed Facts
- `spec.md` already exists as a required artifact for large tasks.
- No existing section forces the underlying vocabulary to be defined.
- No existing section enumerates actor-visible states or their transitions.
- An implementation could satisfy every current section while resting on an
  undefined term, and artifact review does not catch this because each document
  reads as complete on its own.
- `hooks/task promote` scaffolds the PRD and Spec templates in shell; both must
  change together with `references/artifacts.md`.

## Requirements
- `prd.md` and `spec.md` carry `### Blocking` and `### Non-blocking` under Open
  Questions.
- Blocking is classified by consequence: two answers would change requirements,
  scope, contract, or validation.
- `ready` states the Blocking criterion, so leaving `planning` has a stated
  precondition.
- Every non-blocking question carries a recorded assumption.
- `spec.md` gains conditional `## Concepts and Terminology` and `## User Journey`
  sections, with fill guidance in `references/artifacts.md`.
- Rejected vocabulary is recorded, since an unmentioned word reads as undefined
  rather than forbidden.
- Skipping either new section requires recording the reason in `plan.md`.
- The Skill host list names every supported host.

## Acceptance Criteria
- `hooks/task promote --size large` emits both new Spec sections and the Open
  Questions split in the generated `prd.md`.
- `python3 evals/runner.py` passes.
- `bash hooks/smoke-test` passes.
- Eval cases cover the new routing and the new artifact headings.

## In Scope
`skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`,
`hooks/task` scaffold templates, `evals/`.

## Out of Scope
- Changing a lifecycle state, hook command, exit code, or file layout.
- Rewriting existing task documents.
- Mechanical enforcement of the Blocking criterion in `hooks/task`.

## Risks / Deferred Items
- The Blocking criterion is reviewer-checked, not machine-checked. Mechanical
  enforcement would parse the state command; deferred to the maintainer.

## Open Questions
### Blocking
### Non-blocking
- [Q1] Should `hooks/task` refuse `planning → ready` while `### Blocking` holds an
  unchecked item? Assumption: left as prose for now; raised in the PR.

## Version History
- v1 — completed.
