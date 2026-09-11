# Task artifacts and routing

Use this reference when creating or reviewing task documents. The task directory is `TaskFlowDocs/<YYYY-MM-DD-short-slug>/`.

`TaskFlowDocs/repository-docs/index.md` is the path-only catalog for repository rules, repository guidance, and personal supplements. Refresh it when absent, stale, or needed by the task phase; load only applicable entries and record the files plus incorporated conclusions in `plan.md`. Repository documents prevail over scoped personal supplements, which are a person's development rules or work habits rather than repository-owned policy.

If a task needs a rule the repository does not supply, first classify it as shared governance or a personal habit. For non-trivial development, derive missing `CONTRIBUTING.md` and `CODE_STYLE.md` from repository evidence, ask at most three dependency-ordered questions per turn for undecidable policy, and require explicit approval before either becomes binding. Draft `ROADMAP.md` only from confirmed product direction and other repository documents only when task-dependent. Put only stricter or orthogonal personal habits under `repository-docs/personal/`; supplements never replace repository-owned policy. Stop for any conflict.

`TaskFlowDocs/todo.md` is the mandatory first record only after a request passes the Skill's applicability gate: a repository development request or an explicit `$taskflow` invocation. Read-only explanation, translation, status, research, review, and diagnosis do not create Todo or task documents. Each qualifying batch import creates or updates one Todo item per source requirement, retaining source plus external identifier/link when available; the batch itself is metadata only. Todo retains triage metadata and a task link after promotion; PRD, Spec, Plan, and verification remain authoritative in that task directory.

The catalog is derived navigation: each entry records document class, repository-relative source path, existence, and last-checked date. Repository-owned documents remain at conventional source locations whether or not Git is initialized; prefer the root for README, contributing, code style, and roadmap documents, and platform-standard directories for PR, CODEOWNERS, CI, and similar files. When authorized to create a missing document, reuse an established conventional filename or use `README.md`, `CONTRIBUTING.md`, `CODE_STYLE.md`, or `ROADMAP.md` for those classes. Never copy or symbolically link repository-owned documents into `repository-docs/`, which contains only `index.md` and optional `personal/`. Report legacy copies or links and do not migrate or delete them without explicit authorization.

When a user changes an approved task fact, classify it before editing artifacts. The classification (work revision vs Task-version material change) and the required action for each are defined in `SKILL.md` under User-change trigger; this reference does not restate them. Never update only one core document after a material user change.

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
## Skills / Tools Used (Optional)
- `<name>` — purpose: `<why it was invoked>`; outcome: `succeeded | failed | unavailable`; incorporated: `<reviewed conclusion or None>`
## Preconditions
- [ ] Applicable repository documents and personal supplements inspected; precedence/conflicts recorded.
- [ ] For remote/fork/PR work: remotes, target repository, base branch, local branch/base, freshness limits, and required checks recorded.
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

List a capability only after an actual invocation attempt. Discovery or selection is not use. A failed or unavailable optional invocation may be recorded when relevant, but it has no incorporated conclusion and does not block the base flow unless it is required for correctness.

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

```markdown
# Sessions — <Task title>
> Current Task version: v1

## Active / Resumable
### S1 — <Agent>
- Status: resumable | closed | unavailable
- Primary: yes | no
- Session availability: local-only | account-scoped | shared | expired
- Session ID:
- Started / Last active:
- Code working directory:
- Task artifact directory:
- Task version / phase:
- Last completed:
- Next step:
- Resume:
- Notes:

## Closed / Reference Only
```

Record a platform's actual resume command only; do not assume one Agent's session ID or command works in another Agent.
