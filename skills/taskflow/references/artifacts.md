# Task artifacts and routing

Use this reference when creating or reviewing task documents. The task directory is `TaskFlowDocs/<YYYY-MM-DD-short-slug>/`.

`TaskFlowDocs/repository-docs/index.md` is the authoritative routing and check record for repository rules, repository guidance, and personal rules. Maintain or read it first, route by phase, load the listed authoritative sources, then record selected paths and incorporated conclusions in `plan.md`. Repository documents prevail over scoped personal rules.

If a task needs a rule the repository does not supply, first classify it as shared governance or a personal habit. For non-trivial development, derive missing `CONTRIBUTING.md` and `CODE_STYLE.md` from repository evidence, ask at most three dependency-ordered questions per turn for undecidable policy, and require explicit approval before either becomes binding. Draft `ROADMAP.md` only from confirmed product direction and other repository documents only when task-dependent. Put only stricter or orthogonal personal habits as sections of `repository-docs/personal.md`; personal rules never replace repository-owned policy and are never committed — the shared alternative is a repository-owned document. Stop for any conflict.

`TaskFlowDocs/todo.md` is the mandatory first record only after a request passes the Skill's applicability gate: a repository development request or an explicit `$taskflow` invocation. Read-only explanation, translation, status, research, review, and diagnosis do not create Todo or task documents. Each qualifying batch import creates or updates one Todo item per source requirement, retaining source plus external identifier/link when available; the batch itself is metadata only. Todo retains triage metadata and a task link after promotion; PRD, Spec, Plan, and verification remain authoritative in that task directory.

Each index entry records document class, repository-relative source path, applicable phases, existence, and status. The personal-rule row is the one exception to `existence`: it names a routing location and reads `Exists: local`, because the file it names is never committed while the index is, so a per-clone answer there would leave the committed file permanently modified on the clones that have one. That index contains routing metadata only; repository-owned documents remain authoritative at conventional source locations. When authorized to create a missing document, reuse an established conventional filename or use `README.md`, `CONTRIBUTING.md`, `CODE_STYLE.md`, or `ROADMAP.md` for those classes. Never copy or symbolically link repository-owned documents into `repository-docs/`, which contains `index.md` plus optional local personal rules in `personal.md` (never committed).

When a user changes an approved task fact, classify it before editing artifacts. The classification (work revision vs Task-version material change) and the required action for each are defined in `SKILL.md` under User-change trigger; this reference does not restate them. Never update only one core document after a material user change.

## Artifact language

Write `prd.md`, `spec.md`, `plan.md`, and `reference/` prose in the user's working language, including every section heading the list below does not name.

The rule binds the document, not whoever drafts it: prose that arrives from a capability and is folded in obeys it exactly as prose you write yourself does. A capability supplies a shape to fill, and the language of its template is not a policy adopted along with it.

Hooks parse task documents by exact text, so the lines they match stay English verbatim:

- Section headings a hook matches by name: `## Approval`, `## Skills / Tools Used`, `## Verification / Review`, `## Change Log`, `## Items`, `## Removed`, `## Active / Resumable`, `## Closed / Reference Only`
- Entry headings a hook matches by name: `### Step N — <name>`, `### SN — <Agent>`
- The `## Approval` fields, in order: `- Status:`, `- Approved by:`, `- Approved at:`, `- Approved version:`, `- Approved scope:`
- Todo field names: `- ID:`, `- Goal:`, `- Task:`, `- Source:`, `- Status:`, `- Updated:`, `- Next action:`
- Blockquote and inline lines: `> Task version:`, `> Status:`, `> Current Task version:`, the `- Status:` lines inside Steps, session entries, and Todo entries, and the `- [ ]` / `- [x]` checklist markers.

The list is the whole boundary. A heading outside it is prose and follows the user's language; translating one is safe because the hooks read the `## ` prefix as the section boundary and never the words after it. A skeleton arrives in English whatever the language — `hooks/task promote` writes one into every new document, and a capability invoked for a phase brings its own — and a skeleton is not prose this rule governs: an unedited scaffold heading may stay in the language it arrived in, and it follows the rule once you edit it. That exemption ends at the headings. The prose written underneath them is not the skeleton's and not the template's: it is yours, and it is in the user's working language however the words around it are phrased.

Field *values* written by a hook are fixed English tokens (`approved`, `done`, `in_progress`) and are not translated; prose inside a value you write yourself may be in either language.

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
## Product Decisions
## Requirements
## Acceptance Criteria
## In Scope
## Out of Scope
## Risks / Deferred Items
## Open Questions
### Blocking
### Non-blocking
## Version History
```

`## Product Decisions` exists because a product question has no reasonable
default. A technical question does: use ES modules or CommonJS, store the score
or recompute it — either answer keeps the work moving. A product question asks
what the thing should be like for whoever uses it, and the Agent cannot answer
it. Choosing one silently is worse than guessing, because the choice then
survives into the artifact as a fact the user never made.

Record each fork as options and a decision, and attribute the decision:

```markdown
## Product Decisions
| # | Decision | Options | Choice | Decided by |
|---|---|---|---|---|
| D1 | Target platform | web page / desktop / both | web page | user |
| D2 | Speed feel | fixed / accelerating / selectable | selectable | user |
| D3 | Visual style | dark / pixel / minimal | dark | agent, pending user confirmation |
```

Rules for this section:

- **Offer options, do not open-endedly ask.** Give two to four concrete choices
  with their consequence. "What style do you want?" makes the user do the design
  work; "A dark theme, B pixel, or C minimal?" asks for a decision.
- **`user` means the user actually chose.** Recording `user` without asking is
  the failure this section exists to prevent.
- **`agent` requires a stated reason and stays pending.** A default chosen to
  keep work moving is fine; presenting it as settled is not.
- **Only mark `agent` with a reason when the choice is reversible.** A
  reversible technical default is not a product decision, so it belongs under
  `### Non-blocking` with its assumption instead.
- **A product question does not belong under `### Non-blocking`.** Speed that
  rises with the score is a preference, not an assumption. Putting it there
  hides a decision inside a technical default.

When a task changes what the product *is* rather than how it is built — target
platform, interaction model, naming, visual identity, default behavior a user
would notice — this section is where those forks live. Record the option set even
when the user has already chosen, because the rejected options are what a later
reader needs to see were considered.

An open question is **blocking** when two answers would produce different work:
different requirements, a different scope, a different contract, or a different
validation. Everything else is **non-blocking** and moves forward with its
assumption written down.

Classifying by consequence rather than by importance is deliberate: an important
question is often non-blocking, and a small-sounding one can invalidate the whole
design. When an answer would change what is built, it blocks regardless of how
easy it seems.

A blocking question answers one of:

- Which concept is being used, when two readings give different behavior
- Which of two valid states the actor starts in
- What the boundary is, when the scope depends on it
- Which requirement wins, when two requirements conflict

Record the assumed answer and where it is verified when a question is
non-blocking. A non-blocking question without a recorded assumption is an
unanswered blocking question with extra steps.

```markdown
## Open Questions
### Blocking
- [ ] Q1 — Is "current session" a property of the Session, or the sidebar's
      selected row? The two give different behavior when a session is removed.
### Non-blocking
- [Q2] Does title generation use a small model? Assumption: yes, derived from
      the first message; verified in Step 3.
```

## Spec outline for large tasks

```markdown
# Spec — <Task title>
> Task version: v1

## Objective and Success Criteria
## Concepts and Terminology
## User Journey
## Interaction and Interface
## Architecture Boundaries and Responsibilities
## Project Structure / Affected Files
## Interfaces, Data Flow, and Contracts
## Invariants and Compatibility
## Validation and Error Semantics
## Code and Test Constraints
## Design Decisions and Alternatives
## Open Questions
```

### Concepts and Terminology

Name what exists before describing what it does. An implementation cannot be
correct against a term nobody defined.

- One entry per noun the task introduces or reuses. Give each exactly one
  definition, then use that word unchanged in every later section, code
  comment, and UI string for this task.
- State what the concept is *not*, when a neighboring concept would fit. A
  definition that only says what it includes leaves room for a second word to
  claim the same meaning.
- Mark provenance: `existing` (the codebase already uses this word) or
  `introduced` (this task adds it). `introduced` terms must be adopted verbatim
  in code and UI; do not paraphrase them per screen or per language.
- **Record rejected vocabulary explicitly.** When a plausible term was
  considered and deliberately not adopted, list it under `Rejected` with the
  reason. This is not padding: an unmentioned word is treated as undefined
  rather than forbidden, and is the main source of invented synonymous concepts.
- Mixed-language products pick one term per concept here and forbid the
  alternates. Write down which forms are allowed, because per-surface translation
  is how one concept ends up with two names.

```markdown
## Concepts and Terminology
- Session — one continuous conversation between a user and the Agent. `existing`
- active session — the Session currently accepting input. A property of the
  Session, not the sidebar's selected row. `introduced`
- Archive — `rejected`: the product has no such state. Removing a Session is
  `delete`; no reversible hiding state exists in this version.

### User Journey

Model the path the actor takes before modelling the code that runs beside it.
Every transition that can strand a user in an inconsistent state belongs here.

- List the states an actor can observe, then the transitions between them. Mark
  each transition with its trigger and its guard — the condition that must hold
  for the transition to be legal.
- Name the initial and terminal state. A state an actor can reach but cannot
  leave is a defect, and so is a transition with no reachable trigger.
- Include the recovery path for each blocking or error state. A journey that
  only covers the happy path does not describe the product.
- When an actor has multiple roles or the actor is not always the user, say so
  and give each role its own journey or state subset.
- Where a state lives in the persisted data, name that field. A visible state
  that no field can represent will be re-invented in code per screen.

### Interaction and Interface

Required when the task has a surface a person looks at: a screen, a command, a
message, a document layout. It fixes what they see before code fixes what
functions do.

Cover, in this order:

- **Layout.** The regions and their order. A plain-text diagram is enough, and
  it must show real proportions rather than a decorative box.
- **Each observable state of the surface**, drawn separately. If a banner says
  one thing while idle and something else while running, that is two surfaces,
  not one with a footnote.
- **Input.** Every key, control, or gesture, and what each one does when it is
  not applicable.
- **Feedback.** What changes visibly in response, and how long it stays.

Two rules that decide whether the diagram is worth writing:

- **Draw it at the real size.** A 20-column grid drawn as 12 cells is a wrong
  specification, not a rough sketch. Check the rows line up.
- **A diagram is specification.** It fixes decisions that otherwise surface after
  implementation: whether an element is removed or padded when its state
  changes, whether a board freezes or clears on game over, whether a view opens
  still or already active. Anything the picture settles must not be re-decided
  in code.

When the surface is a CLI or a notification, "diagram" means the output shape:
the columns, the order of lines, and what appears per state.

Skip the section only when the task produces no surface — a library, a data
transform, a migration. Then say so in `plan.md`.

## Plan outline

```markdown
# Plan — <Task title>
> Task version: v1
> Status: planning

## Spec Pointers
## Reference Pointers
## Related Tasks
## Skills / Tools Used
- [PRD] `<name>` — purpose: `<why it was invoked>`; outcome: `succeeded | failed | unavailable`; incorporated: `<reviewed conclusion or None>`
- [PRD] `Unaided — no capability applied to this phase; considered: <concept classes inspected>`
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

`## Skills / Tools Used` is required, not optional, and it is a report of what happened rather than a declaration: the first body write of `prd.md`, `spec.md`, or `plan.md` is refused by a `PreToolUse` hook until a capability was really invoked for that stage, and each stage document spends one record from the version's evidence queue. The queue is consumed oldest first and the gate attaches the stage when it releases a document, so **which record a stage spends depends on which document was written first, not on when the call was made** — a call made while drafting one document can back a later one, and a phase that invokes more than once leaves its extra record to the next phase. Record a stage-tagged line in that section once the stage document is under way: `- [PRD] …`, `- [Spec] …`, `- [Plan] …`. Each line is either the invocation that was made (capability, purpose, outcome) or `Unaided — …; considered: <concept classes>` for that stage. A phase with no capability worth invoking is declared with `hooks/task unaided <stage> --considered "<concept class>"` — that command is the only place a concept class is validated. Untagged lines do not count toward a stage.

`task approve` gates stages before Approval fields: required = `[PRD]`+`[Plan]`, plus `[Spec]` when `spec.md` exists. A missing stage line fails naming that stage; so does a stage with no release record, a line naming a capability this Task version never released as an invocation, and an invocation-shaped line standing over an unaided record. The name is checked against the version's released invocations, not against the stage's own record, because the store records no stage: writing the stages in a different order legitimately moves which stage a call's record lands on, and requiring that record's name would force the section to misreport itself. What it cannot do is invent a name — a capability in no released record of the version is refused, and one that exists only as an `unaided` declaration cannot be claimed as an invocation. The `Unaided` class is the exception: it is typed into `hooks/task unaided` and written back by that same command, so it reconciles exactly. It prints how many stages were released by an invocation and how many unaided, so a task that declared every phase unaided is visible rather than silent; the invoked count is stages, not distinct capabilities. A task promoted before this gate existed has no release record for any stage, and `approve` fails closed for it: declare each stage with `hooks/task unaided`, or re-run the phase with a capability invoked. Fold foreign capability output by kind: requirements → `prd.md`, design → `spec.md`, breakdown → `plan.md` Steps; never a second fact root.

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

If there is no research, do not create `reference/`. If `reference/` is small, `index.md` is optional. If a tool emits a default root-level artifact, move or rewrite its content into the current task destination before accepting it as authoritative. Rewriting it covers the language as well as the structure: what folds in is the shape, and the prose is rewritten in the user's working language rather than carried over from whoever produced the draft.

A new Task version or a user change is governed by the lifecycle rules in `SKILL.md` (User-change trigger, Phase 5 Build, Complete and archive); this reference does not restate them. Archive a completed task as one transaction per `SKILL.md`. Tool output is candidate material until the core-document owner reviews and merges it.

When a Skill or tool is used, add one concise entry to `plan.md` with its name, purpose, and incorporated conclusion. Do not record checks that led to no tool use. Tool output is candidate material until the core-document owner reviews and merges it.

## Related tasks

Put lightweight dependency links in `plan.md`:

```markdown
## Related Tasks
- Parent: `<task path> (Task version: vN) or None`
- Children: `<task path or None>`
- Depends on: `<task path or None>`
- Blocks: `<task path or None>`
- Related: `<task path or None>`
```

`Parent` and `Children` carry direction; `Related` is symmetric and covers tasks with neither. `Parent` names the Task version the link was planned against, because that is the version the relationship was reasoned from — the coordination rules that use it are in `SKILL.md` (Existing-task-first selection). Do not create a global task index solely for these links.

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

`TaskFlowDocs/<task>/sessions.md` is the resume index. Whether an entry must exist is a condition rather than a judgement — a session that ends while its task is not `completed` writes one — and `SKILL.md` under **Sessions and collaboration** states that condition and the fields to record; this reference does not restate it. Hook and Agent own different fields: the SessionStart hook writes the session id, agent, availability, started/last-active timestamps, code working directory, task artifact directory, and Task version/phase; the Agent owns `Last completed`, `Next step`, and `Notes`, and is the only writer that may mark an entry `closed`. Never restate progress or next-step detail here that belongs in `plan.md`.

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
