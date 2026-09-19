# Task artifacts and routing

Use this reference when creating or reviewing task documents. The task directory is `TaskFlowDocs/<YYYY-MM-DD-short-slug>/`.

`TaskFlowDocs/repository-docs/index.md` is the authoritative routing and check record for repository rules, repository guidance, and personal rules. Maintain or read it first, route by phase, load the listed authoritative sources, then record selected paths and incorporated conclusions in `plan.md`. Repository documents prevail over scoped personal rules.

If a task needs a rule the repository does not supply, first classify it as shared governance or a personal habit. For non-trivial development, derive missing `CONTRIBUTING.md` and `CODE_STYLE.md` from repository evidence, ask at most three dependency-ordered questions per turn for undecidable policy, and require explicit approval before either becomes binding. Draft `ROADMAP.md` only from confirmed product direction and other repository documents only when task-dependent. Put only stricter or orthogonal personal habits as `repository-docs/*.md`; personal rules never replace repository-owned policy and are never committed — the shared alternative is a repository-owned document. Stop for any conflict.

`TaskFlowDocs/todo.md` is the mandatory first record only after a request passes the Skill's applicability gate: a repository development request or an explicit `$taskflow` invocation. Read-only explanation, translation, status, research, review, and diagnosis do not create Todo or task documents. Each qualifying batch import creates or updates one Todo item per source requirement, retaining source plus external identifier/link when available; the batch itself is metadata only. Todo retains triage metadata and a task link after promotion; PRD, Spec, Plan, and verification remain authoritative in that task directory.

Each index entry records document class, repository-relative source path, applicable phases, existence, last-checked date, and status. The index contains routing metadata only; repository-owned documents remain authoritative at conventional source locations. When authorized to create a missing document, reuse an established conventional filename or use `README.md`, `CONTRIBUTING.md`, `CODE_STYLE.md`, or `ROADMAP.md` for those classes. Never copy or symbolically link repository-owned documents into `repository-docs/`, which contains `index.md` plus optional local personal rules named `*.md` (never committed).

When a user changes an approved task fact, classify it before editing artifacts. The classification (work revision vs Task-version material change) and the required action for each are defined in `SKILL.md` under User-change trigger; this reference does not restate them. Never update only one core document after a material user change.

## Artifact language

Write `prd.md`, `spec.md`, `plan.md`, and `reference/` prose in the user's working language. Hooks parse task documents, so the lines they match stay English verbatim: `> Task version:`, `> Status:`, `## ` section headings, the `## Approval` fields, `### Step N`, the `- Status:` lines inside Steps and Todo entries, Todo field names (`- ID:`, `- Goal:`, `- Task:`, …), and the `- [ ]` / `- [x]` checklist markers. Field *values* written by a hook are fixed English tokens (`approved`, `done`, `in_progress`) and are not translated; prose inside a value you write yourself may be in either language.

This applies to documents created from now on. Existing documents are not rewritten for language, in particular not under `TaskFlowDocs/achieved/`, which is read-only history.

## Minimal layout

```text
TaskFlowDocs/
└── YYYY-MM-DD-short-slug/
    ├── prd.md
    ├── spec.md       # large tasks only
    ├── plan.md
    ├── sessions.md   # optional
    ├── reference/    # optional
    │   └── index.md  # optional when materials are numerous
    └── old/          # optional, superseded versions only
```

## PRD outline

```markdown
# <Task title>
> Task version: v1
> Status: planning

## Goal
## Background / Confirmed Facts
## Requirements
## Acceptance Criteria
## In Scope
## Out of Scope
## Risks / Deferred Items
## Open Questions
## Version History
```

## Spec outline for large tasks

```markdown
# Spec — <Task title>
> Task version: v1

## Objective and Success Criteria
## Architecture Boundaries and Responsibilities
## Project Structure / Affected Files
## Interfaces, Data Flow, and Contracts
## Invariants and Compatibility
## Validation and Error Semantics
## Code and Test Constraints
## Design Decisions and Alternatives
## Open Questions
```

## Plan outline

```markdown
# Plan — <Task title>
> Task version: v1
> Status: planning

## Spec Pointers
## Reference Pointers
## Related Tasks
## Skills / Tools Used
- `<name>` — purpose: `<why it was invoked>`; outcome: `succeeded | failed | unavailable`; incorporated: `<reviewed conclusion or None>`
- `Unaided — no capability applied to this phase; considered: <concept classes inspected>`
## Preconditions
- [ ] Applicable repository documents and personal rules inspected; precedence/conflicts recorded.
- [ ] For remote/fork/PR work: remotes, target repository, base branch, local branch/base, freshness limits, and required checks recorded.
- [ ] For PR creation/update: applicable template path, every required-field mapping, and template verification recorded.
- [ ] Missing governance drafts and explicit approvals recorded before they become binding.
## Approval
## Steps
### Step N — <name>
- Goal:
- Dependencies:
- Files:
- Implementation checklist:
  - [ ] <implementation item>
  - [ ] <documentation / test / review item>
- Acceptance:
- Verification:
- Rollback:
- Status: pending | in_progress | done | blocked
## Checkpoints
## Verification / Review
## Change Log
- <YYYY-MM-DD> <work revision or Task version> — <one-line reason>; affects <files>
## Follow-ups
## Version History
```

`plan.md`'s `## Change Log` records work revisions — wording or approach changes, progress, results, and other updates that do not alter an approved contract. Append one line per revision and keep the current Task version. Only a Task-version material change bumps `vN`, updates every core document atomically, and returns to approval; never treat a wording or approach clarification as a Task-version event.

List a capability only after an actual invocation attempt. Discovery or selection is not use. A failed or unavailable optional invocation may be recorded when relevant, but it has no incorporated conclusion and does not block the base flow unless it is required for correctness. The phase-to-concept table in `SKILL.md` says what class to look for; this rule says what may be recorded afterwards.

`## Skills / Tools Used` is required, not optional. Write exactly one of two shapes: one line per capability actually invoked, or a single `Unaided — no capability applied to this phase; considered: <concept classes inspected>` line. The unaided line names the classes that were inspected, so a considered decision stays distinguishable from an overlooked section. The requirement is not retroactive — a Plan written before it keeps the section it has.

## Release task documents

A release does not use task documents at all. It runs `RELEASE.md` directly, on the base checkout, with no Todo item, no task directory, no branch, and no PRD, Spec, or Plan — so there is nothing here to restate a procedure or to drift from one. The record of a release is its `CHANGELOG.md` section and its GitHub Release body; `RELEASE.md` names what they carry, and this reference does not repeat it.

The approval a Plan's `## Approval` block normally records comes with the procedure instead: the release owner approves the release commit before `RELEASE.md`'s step 5 pushes. A release that also changes the plugin is ordinary development work and takes the full path above; only shipping what is already merged is the exception.

## Output routing

| Generic output | Task destination |
|---|---|
| requirements / PRD | `prd.md` |
| design / specification | `spec.md` when required |
| plan / task list / checkpoint / review | `plan.md` |
| applicable development request / explicit `$taskflow` request | `TaskFlowDocs/todo.md` before task selection |
| research / evidence | `reference/` |
| resume index | `sessions.md` |

If there is no research, do not create `reference/`. If `reference/` is small, `index.md` is optional. If a tool emits a default root-level artifact, move or rewrite its content into the current task destination before accepting it as authoritative.

A new Task version or a user change is governed by the lifecycle rules in `SKILL.md` (User-change trigger, Phase 5 Build, Complete and archive); this reference does not restate them. Archive a completed task as one transaction per `SKILL.md`. Tool output is candidate material until the core-document owner reviews and merges it.

When a Skill or tool is used, add one concise entry to `plan.md` with its name, purpose, and incorporated conclusion. Do not record checks that led to no tool use. Tool output is candidate material until the core-document owner reviews and merges it.

## Related tasks

Put lightweight dependency links in `plan.md`:

```markdown
## Related Tasks
- Depends on: `<task path or None>`
- Blocks: `<task path or None>`
- Related: `<task path or None>`
```

Do not create a global task index solely for these links.

## Reference index when needed

When `reference/` is large enough to need navigation, add `reference/index.md` and list each item with:

```markdown
- Status: candidate | verified | rejected | superseded | archived
- Source: URL, DOI, code path, or experiment identifier
- Collected: YYYY-MM-DD
- Conclusion: what this source supports or contradicts
- Used by: PRD / Spec / Plan section
- Integrity: file hash or access date when useful
```

Do not alter external source files to add status metadata. Update the index or a team-authored note instead.

## Session outline

`TaskFlowDocs/<task>/sessions.md` is the optional resume index. Hook and Agent own different fields: the SessionStart hook writes the session id, agent, availability, started/last-active timestamps, code working directory, task artifact directory, and Task version/phase; the Agent owns `Last completed`, `Next step`, and `Notes`, and is the only writer that may mark an entry `closed`. Never restate progress or next-step detail here that belongs in `plan.md`.

```markdown
# Sessions — <Task title>
> Current Task version: v1

## Active / Resumable
### S1 — <Agent>
- Status: resumable | closed | unavailable
- Primary: yes | no
- Session availability: local-only | account-scoped | shared | expired
- Session ID:
- Started:            # hook-owned
- Last active:        # hook-owned
- Code working directory:
- Task artifact directory:
- Task version / phase:
- Last completed:     # Agent-owned
- Next step:          # Agent-owned
- Resume:
- Notes:              # Agent-owned

## Closed / Reference Only
```

Record a platform's actual resume command only; do not assume one Agent's session ID or command works in another Agent.
