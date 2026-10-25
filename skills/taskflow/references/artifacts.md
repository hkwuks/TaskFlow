# Task artifacts and routing

Use this reference when creating or reviewing task documents. The task directory is `TaskFlowDocs/<YYYY-MM-DD-short-slug>/`.

`TaskFlowDocs/repository-docs/index.md` is the authoritative routing and check record for repository rules, repository guidance, and personal rules. Maintain or read it first, route by phase, load the listed authoritative sources, then record selected paths and incorporated conclusions in `plan.md`. Repository documents prevail over scoped personal rules.

If a task needs a rule the repository does not supply, first classify it as shared governance or a personal habit. For non-trivial development, derive missing `CONTRIBUTING.md` and `CODE_STYLE.md` from repository evidence, ask at most three dependency-ordered questions per turn for undecidable policy, and require explicit approval before either becomes binding. Draft `ROADMAP.md` only from confirmed product direction and other repository documents only when task-dependent. Put only stricter or orthogonal personal habits as sections of `repository-docs/personal.md`; personal rules never replace repository-owned policy and are never committed — the shared alternative is a repository-owned document. That exclusion is written per clone by `hooks/install-git-hygiene` into `.git/info/exclude`, not into a tracked `.gitignore`, and it hides only an untracked copy. Stop for any conflict.

`TaskFlowDocs/todo.md` is the mandatory first record only after a request passes the Skill's applicability gate: a repository development request or an explicit `$taskflow` invocation. Read-only explanation, translation, status, research, review, and diagnosis do not create Todo or task documents. Each qualifying batch import creates or updates one Todo item per source requirement, retaining source plus external identifier/link when available; the batch itself is metadata only. Todo retains triage metadata and a task link after promotion; PRD, Spec, Plan, and verification remain authoritative in that task directory.

A **live** entry carries every field `hooks/task intake` writes. A **closed** entry — one whose status is `done`, rewritten by `hooks/archive` at the moment of archiving — keeps only `- ID:`, `- Status:`, `- Goal:`, `- Task:` and `- Next action:`. The rest are intake facts nothing reads once the work is finished, and the free-form prose under them is carried verbatim into the achieved `plan.md` under `## Todo Record` before it is removed, because that prose is the analysis behind the task and is not duplicated by the Plan. `Goal` stays for two reasons: the heading is a byte-truncated copy of it, and `hooks/task`'s duplicate-goal check reads the field on every entry regardless of status. `Updated` is the one field a later `hooks/reopen` has to insert, since a closed entry no longer carries it.

Each index entry records document class, repository-relative source path, applicable phases, existence, and status. The personal-rule row is the one exception to `existence`: it names a routing location and reads `Exists: local`, because the file it names is never committed while the index is, so a per-clone answer there would leave the committed file permanently modified on the clones that have one. That index contains routing metadata only; repository-owned documents remain authoritative at conventional source locations. When authorized to create a missing document, reuse an established conventional filename or use `README.md`, `CONTRIBUTING.md`, `CODE_STYLE.md`, or `ROADMAP.md` for those classes. Never copy or symbolically link repository-owned documents into `repository-docs/`, which contains `index.md` plus optional local personal rules in `personal.md` (never committed).

When a user changes an approved task fact, classify it before editing artifacts. The classification (work revision vs Task-version material change) and the required action for each are defined in `SKILL.md` under User-change trigger; this reference does not restate them. Never update only one core document after a material user change.

## Artifact language

Write `prd.md`, `spec.md`, `plan.md`, and `reference/` prose in the user's working language, including every section heading the list below does not name.

The rule binds the document, not whoever drafts it: prose that arrives from a capability and is folded in obeys it exactly as prose you write yourself does. A capability supplies a shape to fill, and the language of its template is not a policy adopted along with it.

Hooks parse task documents by exact text, so the lines they match stay English verbatim:

- Section headings a hook matches by name: `## Approval`, `## Skills / Tools Used`, `## Verification / Review`, `## Change Log`, `## Items`, `## Removed`, `## Active / Resumable`, `## Closed / Reference Only`, `## Reference Pointers`
- The reinforce bullet inside `## Reference Pointers`: `- [Reinforce] \`<path>\` — <reason>`, matched at column 0. The marker, the backticks and the `—` separator are text a hook reads; translating or re-indenting any of them turns the declaration off without an error. The reason after the separator is prose and follows the user's language.
- The `## Todo Record` heading: not matched by any hook, but it is written by `hooks/archive` and must stay at column 0 in `plan.md` — the same rule that keeps it out of a Todo entry, where a column-0 `## ` line is a section boundary to every hook that splits the file.
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
## Requirements
## Acceptance Criteria
## In Scope
## Out of Scope
## Risks / Deferred Items
## Open Questions
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
- [PRD] `<name>` — purpose: `<why it was invoked>`; outcome: `succeeded | failed | unavailable`; incorporated: `<reviewed conclusion or None>`
- [PRD] `Unaided — no capability applied to this phase; considered: <concept classes inspected>`
- [Test] `<name>` — purpose: `<why it was invoked>`; outcome: `succeeded | failed | unavailable`; incorporated: `<reviewed conclusion or None>`
- [Test] `Unaided — no capability applied to this phase; considered: testing strategy`
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

`## Skills / Tools Used` is required, not optional, and it is a report of what happened rather than a declaration: the first body write of `prd.md`, `spec.md`, or `plan.md` is refused by a `PreToolUse` hook until a capability was really invoked for that stage, and each stage document spends one record from the version's evidence queue. The queue is consumed oldest first and the gate attaches the stage when it releases a document, so **which record a stage spends depends on which document was written first, not on when the call was made** — a call made while drafting one document can back a later one, and a phase that invokes more than once leaves its extra record to the next phase. Record a stage-tagged line in that section once the stage document is under way: `- [PRD] …`, `- [Spec] …`, `- [Plan] …`, `- [Test] …`. Each line is either the invocation that was made (capability, purpose, outcome) or `Unaided — …; considered: <concept classes>` for that stage. A phase with no capability worth invoking is declared with `hooks/task unaided <stage> --considered "<concept class>"` — that command is the only place a concept class is validated. Untagged lines do not count toward a stage. **`Test` is written the same way and recorded differently**, because it has no stage document: writing tests spans many files over several Steps, so there is no first body write to gate and the declaration does the gate's work, spending a standing evidence record when it finds one. What it records as an invocation depends on whether such a record existed, not on what the caller asked for — so read the command's output, which names the kind it wrote and the capability if it was one.

`task approve` gates stages before Approval fields: required = `[PRD]`+`[Plan]`+`[Test]`, plus `[Spec]` when `spec.md` exists. `[Test]` is required of every task and not only of ones whose Plan has a testing Step: a test document does not exist, so there is nothing whose existence could decide it, and inferring one from a Step's wording would be a second standard for what counts. A task that wrote no tests says so in one line — `bash hooks/task unaided Test --considered 'testing strategy'` — which is also what its refusal names. A missing stage line fails naming that stage; so does a stage with no release record, a line naming a capability this Task version never released as an invocation, and an invocation-shaped line standing over an unaided record. The name is checked against the version's released invocations, not against the stage's own record, because the store records no stage: writing the stages in a different order legitimately moves which stage a call's record lands on, and requiring that record's name would force the section to misreport itself. What it cannot do is invent a name — a capability in no released record of the version is refused, and one that exists only as an `unaided` declaration cannot be claimed as an invocation. The `Unaided` class is the exception: it is typed into `hooks/task unaided` and written back by that same command, so it reconciles exactly. It prints how many stages were released by an invocation and how many unaided, so a task that declared every phase unaided is visible rather than silent; the invoked count is stages, not distinct capabilities. A task promoted before this gate existed has no release record for any stage, and `approve` fails closed for it: declare each stage with `hooks/task unaided`, or re-run the phase with a capability invoked. Fold foreign capability output by kind: requirements → `prd.md`, design → `spec.md`, breakdown → `plan.md` Steps; never a second fact root.

`## Reference Pointers` lists what this task's work is read against. A plain bullet there is material already consulted; the line below is a declaration that it must come back while the task runs:

```markdown
- [Reinforce] `<repository-relative path>` — <why this task cannot do without it>
```

`hooks/prompt-reminder` prints those paths once per prompt, between the in-flight task line and the classification question, and prints nothing for a Plan that declares none. The list follows Plan order and a pointer declared twice prints once. The marker, a backticked path, the `—` separator, and a non-empty reason after it are all required; a line missing any of them is dropped rather than read as far as it parses, because a malformed entry reported as a pointer is worse than an ignored one — it claims a document is missing when what is actually wrong is the bullet. The bullet has to start at column 0: an indented one is not matched, so keep it flush left under the heading.

The path has to be a POSIX repository-relative one. A leading `/` or `~`, a backslash, a colon, and any `..` segment each name something the hook cannot resolve — an absolute path, a Windows drive or UNC share, a URL scheme, or a directory outside the worktree — so each is dropped rather than printed. A fenced block is skipped, which matters because this file's own Plan outline is fenced and contains the heading: pasting the outline before filling it in declares nothing.

**Who marks it, and by what test.** The Agent writing the Plan marks it; the user reviews the list when approving that Plan. Both questions are settled here because nothing else can settle them: the hook cannot read a document and decide whether it matters, and a second judge would be a second standard. An entry earns the marker when all three hold, each answerable while the Plan is being written rather than guessed at:

1. **It spans Steps.** Something one Step alone consults belongs in that Step, not in a list printed every prompt.
2. **Violating it is silent.** Nothing turns red when it is ignored — no assertion, no lint, no review checklist item.
3. **No code states it.** A rule the suite already enforces needs no reminder; the failure is already loud.

The second is the one that does the work. Mark what breaks quietly and forgets itself; do not mark `CODE_STYLE.md`, because a violation there is caught, or a rule `hooks/smoke-test` asserts, because the reminder would duplicate a louder signal.

**When the material goes wrong.** A path that no longer resolves prints as `MISSING: <path>` in the same line rather than disappearing — material vanishing is exactly what this list exists to surface. A pointer whose content contradicts the implementation is a work revision: fix the affected documents and add one change-log line, keeping the Task version. Only if the material overturns an approved requirement does it become a Task-version material change, per the User-change trigger in `SKILL.md`. Whether a *repository* document is wrong is a separate deliverable, not something this list judges.

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

`TaskFlowDocs/<task>/sessions.md` is the resume index. Whether an entry must exist is a condition rather than a judgement — a session that ends while its task is not `completed` writes one — and `SKILL.md` under **Sessions and collaboration** states that condition and the fields to record; this reference does not restate it. Hook and Agent own different fields: the SessionStart hook writes the session id, agent, availability, started/last-active timestamps, code working directory, task artifact directory, and Task version/phase; the Agent owns `Last completed`, `Next step`, and `Notes`, and is the only writer that may mark an entry `closed`. The file stays out of Git — machine-local resume data, excluded by `hooks/install-git-hygiene` in the clone's own `.git/info/exclude` — and a copy committed before that rule existed stays tracked and visible rather than being hidden. Never restate progress or next-step detail here that belongs in `plan.md`.

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
