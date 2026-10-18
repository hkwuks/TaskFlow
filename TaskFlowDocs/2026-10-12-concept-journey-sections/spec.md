# Spec — Concept and journey sections for the TaskFlow template
> Task version: v1

## Objective and Success Criteria
A task that changes what a term means, or which states an actor observes, cannot
reach `ready` with those two facts left implicit. Success is measured by the
generated scaffolds and the eval suite, not by prose volume.

## Concepts and Terminology
- Blocking question — one whose two answers would change requirements, scope,
  contract, or validation. `introduced`
- Non-blocking question — one that can proceed against a recorded assumption.
  `introduced`
- Concepts and Terminology — the Spec section holding one definition per noun
  with provenance. `introduced`
- User Journey — the Spec section holding actor-visible states and the
  transitions between them. `introduced`
- Rejected vocabulary — a plausible term deliberately not adopted, listed with its
  reason. `introduced`
- Existing / introduced — provenance marks on a concept, distinguishing a word
  the codebase already uses from one this task adds. `introduced`
- archive — `rejected` as a model for this change: it would add a second notion
  of hiding to a workflow whose current states are already sufficient.

## User Journey
The actor here is the Agent writing the task documents, with the user reviewing
at approval.

| from | to | trigger | guard |
|---|---|---|---|
| — | inbox | request passes the applicability gate | none |
| inbox | planning | task promoted | required documents exist |
| planning | ready | documents complete | no unchecked `### Blocking` item remains |
| ready | in_progress | approval recorded in `plan.md` | none |
| in_progress | checking | implementation complete | none |
| checking | completed | acceptance and verification pass | none |
| planning | blocked | a concrete blocker is recorded | none |
| blocked | planning | blocker cleared | none |
| in_progress | ready | material change to an approved decision | old version archived first |

- `ready` is reachable only with Blocking empty; the criterion is stated in prose
  rather than parsed.
- A material change during `in_progress` returns to `ready`, never straight to
  `in_progress` — the earlier approval no longer covers the new decision.

## Architecture Boundaries and Responsibilities
- `references/artifacts.md` owns the templates and the fill guidance.
- `SKILL.md` owns when each section is required and what `ready` means.
- `hooks/task` owns the generated scaffolds; it must not drift from
  `references/artifacts.md`.
- `evals/` owns the executable expectations for both routing and artifacts.

## Interfaces, Data Flow, and Contracts
`hooks/task promote <id> <task-id> large` writes the scaffolds; both templates
are shell literals inside that script. A change to a heading in
`references/artifacts.md` is incomplete until the matching literal in
`hooks/task` changes too.

## Invariants and Compatibility
- Existing task documents are not rewritten, matching the artifact-language rule.
- No lifecycle state, hook command, exit code, or path layout changes.
- Eval fixtures stay minimal: they assert headings, not filled content.

## Validation and Error Semantics
`evals/runner.py` fails on an unmet expectation. `hooks/smoke-test` must report
ALL SMOKE PASSED. A promote run against a scratch repository confirms the
generated documents, since the eval fixture and the generator are separate paths
to the same templates.

## Code and Test Constraints
- Shell: `#!/usr/bin/env bash`, `set -euo pipefail`, quoted expansions.
- Conventional Commits; mark a breaking change with `!`.
- One requirement per bullet; repository-relative paths in documentation.

## Design Decisions and Alternatives
- Classify blocking by consequence, not importance. Importance invites arguing
  about whether a question "feels" important; consequence is decidable.
- Record rejected vocabulary explicitly rather than omitting it, because an
  unmentioned word is treated as undefined rather than forbidden.
- Scope both new sections conditionally and require a recorded reason to skip,
  rather than requiring them always and pricing every small task for it.
- Keep enforcement in prose for this change. A parse in the state command is a
  behavior change and belongs to the maintainer's decision.

## Open Questions
### Blocking
### Non-blocking
- [Q1] Should `hooks/task` refuse `planning → ready` while `### Blocking` holds an
  unchecked item? Assumption: prose is sufficient for this change; raised in the
  PR body.
