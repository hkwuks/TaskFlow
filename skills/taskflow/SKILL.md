---
name: taskflow
description: "Manage repository development requests through TaskFlow: features, fixes, refactors, tests, configuration/build/CI changes, and explicit $taskflow planning or research. Not for releases, which run RELEASE.md directly, and not for read-only explanation, translation, status, research, review, or diagnosis unless the user explicitly invokes $taskflow."
---

# TaskFlow

Use this skill as the single entry point for the project's task framework. It defines where task facts live and how work moves through the lifecycle. TaskFlow does not select tools: during clarification, PRD, Spec, Plan, research, and review work, first check the capabilities currently available to the Agent and use any that materially help. Review and route only incorporated task facts into the current task directory.

## Applicability gate

Apply TaskFlow automatically only when the request asks to modify a repository or deliver a development artifact, including a feature, bug fix, refactor, test, or configuration/build/CI change. Do not create or update Todo/task documents for read-only explanation, translation, status queries, research, review, or diagnosis. If such work later leads to an implementation request, begin TaskFlow with that new request. An explicit user request to use `$taskflow` opts any planning or research work into this workflow.

**A release is the exception: it does not pass through TaskFlow.** `RELEASE.md` is the procedure, and it runs from the base checkout with no TaskFlow task, no Todo item, no branch, and no PRD, Spec, or Plan. Its record is the `CHANGELOG.md` section and the GitHub Release body. An explicit `$taskflow` request, or a release that changes the plugin itself rather than shipping what is already merged, is ordinary development work and is handled as one.

Decide this applicability before Todo intake. If TaskFlow does not apply, answer or investigate directly and stop reading this workflow.

TaskFlow may coordinate with host/harness hooks (Claude Code and Codex CLI) for bounded bookkeeping and context. Host hooks are optional optimization, not a prerequisite: an environment without hooks runs the same flow. See [references/runtime.md](references/runtime.md) for what hooks may and may not do.

## Source of truth

For an active task, the task directory is:

```text
TaskFlowDocs/YYYY-MM-DD-short-slug/
```

`TaskFlowDocs/repository-docs/index.md` is the authoritative routing and check record for repository documents, repository rules, and personal rules. Maintain or read it first, route by phase, then load the listed source documents; those source documents remain authoritative for policy content. Record selected paths and incorporated conclusions in the active task Plan. If the task needs a rule that the repository does not provide, use the repository-document rules below before implementation.

`TaskFlowDocs/todo.md` is the mandatory intake record for every request that passes the applicability gate, including qualifying direct development requests, GitHub Issues, other development imports, and explicit `$taskflow` requests. Create or update its Todo item before task matching, clarification, promotion, planning, implementation, or import-specific processing. It is not a second source of task facts: after promotion, the linked `TaskFlowDocs/<task-id>/` directory is authoritative for requirements, design, plan, and verification.

Required artifacts:

- `prd.md` — goal, requirements, scope, and observable acceptance criteria.
- `plan.md` — current Task version, state, approval, steps, progress, verification, review, risks, rollback, and follow-ups.

Conditional artifacts:

- `spec.md` — required for a large task; optional for a small, self-contained task.
- `reference/` — optional research and evidence. Create `reference/index.md` only when the material is numerous enough to need navigation.
- `sessions.md` — optional session/resume index when work spans sessions or agents.
- `old/vN/` — only for a superseded logical version.

Never create a second task fact source such as a root `SPEC.md`, `TaskFlowDocs/plan.md`, or an automatic review file for the same task. `TaskFlowDocs/todo.md` is the sole repository Todo inbox; it contains triage metadata only and never duplicates promoted task facts.

Task documents are read by the user and parsed by hooks, so they carry two languages at once. Write the prose in the user's working language; keep the lines hooks match — `> Task version:`, `> Status:`, `## ` headings, the `## Approval` fields, `### Step N`, `- Status:` lines, Todo field names, and `- [ ]` / `- [x]` markers — in English exactly as the hooks expect. `references/artifacts.md` lists the boundary. Existing documents, including everything under `TaskFlowDocs/achieved/`, are not rewritten for language.

## Triage and lifecycle

After the request passes the applicability gate, first record or update its Todo item. Then inspect the repository, `TaskFlowDocs/repository-docs/index.md`, applicable project rules, active and achieved TaskFlowDocs tasks, tests, configuration, Git state, and uncommitted changes. Separate findings into confirmed facts, user decisions, technical unknowns, and explicit exclusions.

### Todo-first intake

Every request within TaskFlow's applicability boundary enters `TaskFlowDocs/todo.md` before task selection. Record its ID, source, goal, status, next action, update date, and external identifier/link when one exists. Deduplicate imported items by source plus external identifier; preserve distinct requirements even when imported as a batch. A batch may carry common source metadata, but it is never itself a task, PRD, or requirements source.

Prefer `hooks/task intake`, `promote`, `state`, `progress`, and `complete` for their bounded mechanical edits. Use Agent edits for semantic content and cases those commands do not cover. These commands are explicit Agent actions, not automatically bound hooks.

Do not create, reopen, modify, or select a task before the Todo record exists. After promotion, retain lifecycle metadata, source identity, and one task link in Todo; do not duplicate task facts. Update the Todo status as the linked task moves through `inbox → clarified → promoted → in_progress → done/cancelled`.

### Existing-task-first selection

Search active tasks before creating a task. Also compare against achieved tasks to identify a later request that belongs to an achieved deliverable. Compare the request with each task's goal, deliverable, owner, scope, acceptance criteria, open questions, and next Plan Step.

| Request relation | Required action |
| --- | --- |
| Advances an active deliverable, planned step, open question, verification, or follow-up | Maintain that task |
| Materially revises the same deliverable | Version that task and obtain re-approval |
| Belongs to an achieved task's deliverable | Retrieve that task, version it, and obtain re-approval |
| Has an independently releasable outcome **and** independent acceptance criteria | Create a related task |
| Has different owner or accountability | Create a related task |
| Mixes existing-task work with an independent deliverable | Present the split and await the user's choice before creating a second task |

A new session, new Agent, or a changed implementation detail is never by itself a new-task trigger. Before continuing an existing or retrieved task, read its current PRD, Spec when present, Plan, applicable repository documents, approval/version/status, next Step and checklist, and latest verification. Update the Plan after meaningful work, including progress, decisions, deviations, and verification; do this before starting unrelated work.

When work targets a pull request, fork, or Git remote, inspect the configured remotes, intended target repository, base branch, local branch/base relationship, and available repository-host guidance such as contribution guides, PR templates, CODEOWNERS, branch or CI rules, and host metadata. Remote names are conventions, not proof: never assume `origin` is the fork or `upstream` exists. Before creating or updating a PR, read the applicable PR template, treat unchecked fields as required unless explicitly optional, map every field to the PR title/body/checks/user decision, and record the template path, mapping, and verification in `plan.md`. A missing, ambiguous, or conflicting required item blocks PR mutation. Record URLs with credentials redacted, freshness limits of remote-tracking data, reviewed source paths, conclusions, and required pre-PR checks in the catalog or linked TaskFlow document. Do not silently add or rewrite remotes, fetch, rebase, merge, push, open a PR, claim synchronization when access fails, or copy secrets, tokens, private data, or opaque remote payloads. If target or base cannot be established from current evidence, stop and ask the user.

### Repository document environment

`TaskFlowDocs/repository-docs/index.md` is the routing/check record, not a copy of source policy. Before non-trivial work, maintain or read it first. Its deterministic SessionStart synchronizer records recognized repository-document and personal-rule paths with class, applicable phases, existence, and status. The hook may update only this routing metadata and inject applicable paths/status; it never edits source documents, task core documents, approval, or Git/hosting state. Add an unrecognized candidate only after user confirmation.

Repository-owned documents live at their conventional repository locations, with the repository root preferred for README, contributing, code style, and roadmap documents and platform-standard directories used for PR templates, CODEOWNERS, CI, and similar files. Never copy or symbolically link them into `repository-docs/`; that directory contains `index.md` plus optional local personal rules in `personal.md`, which is never committed. Source documents are authoritative. Refresh the catalog after their addition, removal, move, or relevant change. If a changed source rule affects approved work, apply the user-change trigger before continuing.

When a non-trivial development task needs a missing repository-owned document, help the user create the smallest evidence-based document at its conventional source location. For missing `CONTRIBUTING.md` or `CODE_STYLE.md`, derive confirmed practice from repository files, scripts, tests, CI, code patterns, history, and host guidance, ask at most three dependency-ordered questions for undecidable policy, draft the document, record evidence and intended effect in the Plan, and obtain explicit user approval before it becomes binding. Create `ROADMAP.md` only after the user confirms product direction; create README, PR templates, CODEOWNERS, CI, release, code-of-conduct, or similar documents only when the task needs them. Never create an empty template, fabricate policy, or treat a personal rule as a substitute. If legacy copies or symbolic links exist under `repository-docs/`, report them, stop using them, and index the authoritative source path; do not migrate or delete them without explicit user authorization.

Select documents by phase: code work uses code style and contributing guidance; commits/PRs use contributing, commit rules, PR templates, CODEOWNERS, and branch/CI rules; design/API/UX work uses design and architecture guidance plus relevant README behavior; release work uses release/changelog guidance; roadmap work uses roadmap and README. Record applicable documents and incorporated conclusions in the task `plan.md`. Missing document classes are informational unless the task needs them; then resolve shared governance through an approved repository-owned document and personal habits through a scoped personal rule.

Repository documents prevail over personal rules. A personal rule may add stricter or orthogonal practices, but cannot weaken, override, or conflict with any applicable repository rule or guidance. A personal rule applies only if its declared scope matches the task. On a conflict, stop and ask the user; do not silently choose one.

### User-change trigger

Treat a user message that corrects, rejects, adds to, or materially changes an approved task fact as a change event. Stop the current phase immediately. Do not update only the document named by the user or continue under stale PRD, Spec, or Plan facts.

Classify the change into exactly one of two buckets before editing anything:

| Change | Examples | Required action |
| --- | --- | --- |
| Work revision (default) | wording, an implementation approach within the approved design, formatting, a progress/checklist update, a verification result, a correction that does not alter an approved contract | Update only affected current documents and record one line in the Plan's change log. Keep the current Task version. |
| Task-version material change | a change to an approved goal, requirement, acceptance criterion, scope, architecture/interface/data contract, compatibility decision, risk decision, or standard | Archive the current Task version, update every existing core document atomically to `vN+1`, return the task to `ready`, and record a new approval before implementation resumes. |

A completed task is read-only in `TaskFlowDocs/achieved/`: if the classified request belongs to its deliverable, retrieve its complete directory to the active TaskFlowDocs root, record the Todo source and reopen reason, then version and re-approve it before changing core documents or implementation. Create a related task only when the existing-task-first boundary requires one.

### Missing repository rules and personal rules

When a task needs a rule not supplied by the repository, first determine whether the gap belongs in repository-owned governance or a personal rule. Missing shared development discipline belongs in an evidence-based repository document as described above; personal rules are only for a person's stricter or orthogonal habits. Ask no more than three dependency-ordered questions per turn, with a recommendation for each; ask only applicable categories (development process, code, commits/PR, then design by default). A repository-owned source document may be created or changed only with explicit user authorization.

After confirmation, append only the selected personal rule as its own section in `TaskFlowDocs/repository-docs/personal.md` (create that file if absent) and let the catalog pick it up on the next sync. Each section must declare `Scope`, `Repository documents checked`, `Rules`, `Verification`, and `Exceptions / Change control`; commit-related sections also state `Commit format` and `PR checks`. Other `*.md` files beside `index.md` are not personal rules. Record any explicit waiver in the catalog and task Plan; never create an empty placeholder or fabricate repository-owned policy.

A personal rule is a local working rule, not a deliverable: it is excluded from Git, so never commit or push `personal.md`, never include it in a pull request, and never present it as team policy. Removing the file from disk removes it from the catalog on the next sync. Anything that must be shared, reviewed, or survive a fresh clone becomes a repository-owned document at its conventional source location under the rules above. Using a personal rule in a task does not make it commit material.

### Todo → PRD → Spec → Plan

**Isolate before the first document.** A task's artifacts are written in Phase 1, not Phase 5, so the isolation has to come first: before creating any `TaskFlowDocs/<slug>/` file or `todo.md` entry, give the task its own branch and its own working tree, and stay in it for the rest of the task.

```bash
git worktree add .worktrees/<slug> -b <type>/<slug> <base>
cd .worktrees/<slug>
```

One task, one working tree — not only when several tasks run at once. The base checkout then stays on `<base>` and clean, which is what makes the next task's branch startable at all: `git checkout` refuses to move while a shared file like `TaskFlowDocs/todo.md` carries uncommitted work from a task that belonged elsewhere. `<type>` follows the repository's branch prefixes (`CONTRIBUTING.md`); `.worktrees/` is ignored, so the worktrees themselves never appear as changes. `hooks/task promote` refuses to run outside a task working tree for this reason, and `hooks/task intake` warns when it has written `todo.md` in a shared one.

Use `TaskFlowDocs/todo.md` as the single intake for every idea, request, and imported requirement, whether or not it is ready for planning. Maintain each item with an ID, status, priority, owner, source, external identifier/link when available, one-sentence goal, task link, next action, and update date. Move it through `inbox → clarified → promoted → in_progress → done/cancelled`.

For batch imports, create or update one Todo item per source requirement before triage; deduplicate only source-identical requirements, retain source identity, and never promote a whole batch as one task. Keep an item in `inbox` while its intent is unknown. Move it to `clarified` only after goal, scope, acceptance, dependencies, size, and applicable repository documents are explicit. On promotion, create `prd.md`, decide whether `spec.md` is required, create `plan.md`, and link the task path back in the Todo item. Do not duplicate requirements or design in the inbox. Enter `in_progress` only after Plan approval; mark `done` only after task acceptance and verification, or `cancelled` with a reason.

Choose the lightest path that preserves traceability:

```text
small, obvious one-file change → direct change + minimal verification
non-trivial task              → planning workflow below
```

TaskFlow is the task-lifecycle and artifact layer, not the expert-capability layer. Before substantive work in any TaskFlow phase, inspect the capabilities currently available in the host environment, including Skills, tools, MCP servers, and Agents, and freely determine whether any can materially improve the current task, artifact, or decision. TaskFlow does not require the selection or use of any particular capability, provider, chain, category, or number of capabilities. When the Agent selects one for use, invoke or load it immediately through the host's supported mechanism before following its workflow or incorporating its output; discovery, listing, or selection alone is not invocation.

If none apply, continue with the base TaskFlow flow. If an optional invocation is unavailable or fails, continue with the base flow and record the failed or unavailable attempt only when it materially affects the task; block only when the capability is required for correctness and no safe alternative exists. Review successful outputs before incorporating them; raw outputs are not authoritative. When `plan.md` exists, record only actual invocation attempts: for success, record purpose and incorporated conclusions; for a relevant failure, record the failed or unavailable outcome without claiming incorporation. Do not record discovery, selection, or an uninvoked capability as used.

A phase's artifact has an equivalent outside TaskFlow. TaskFlow names these itself, so an available capability rarely advertises "PRD"; match on the concept instead, and consider the class below before writing the artifact unaided. The class says what to look for, never what to use: availability, fit, and the decision to proceed unaided stay yours.

| Phase | Artifact | Equivalent concept class | Consider a capability for |
| --- | --- | --- | --- |
| 1. Define — PRD | `prd.md` | requirements elicitation and framing | interviewing the user, refining a vague idea into testable requirements, writing a requirements document |
| 2. Research — Reference | `reference/` | literature and evidence review | searching external sources, assessing evidence quality, annotating findings |
| 3. Design — Spec decision | `spec.md`, or the recorded `No spec required` | architecture and design specification | methodology or architecture design, interface/contract definition |
| 4. Plan — execution contract | `plan.md` | work breakdown and task decomposition | decomposing work into verifiable steps, sequencing dependencies, estimating |
| 5. Build — implement by Plan | the change itself | incremental implementation | language and framework conventions, pattern guidance for the code being written |
| 6. Verify and review | acceptance and findings | testing strategy and code review | designing or writing tests, adversarial review, security or performance review |
| 7. Complete and archive | archived directory, promoted rules | documentation and decision records | writing durable documentation or an ADR, recording the decision trail |

A phase ran unaided when its artifact exists but nothing was invoked for its concept class; that is a legitimate outcome, but it must be a choice, not an oversight. Record it as one — `## Skills / Tools Used` in `plan.md` is required, and a phase that ran unaided says so in one `Unaided — …` line rather than staying empty.

**Invoke when each document starts, not after it is written.** Before the first body of `prd.md`, invoke (or decide qualified Unaided for) the Define class and append a `[PRD]` line to the Plan’s Skills section; do the same with `[Spec]` before drafting `spec.md` and `[Plan]` before drafting `plan.md`. Stage lines look like `- [PRD] \`some:cap\` — purpose: …; outcome: …; incorporated: …` or `- [PRD] Unaided — …; considered: <concept class>`. `task approve` requires `[PRD]` and `[Plan]` always, and `[Spec]` when `spec.md` exists; each required stage line is shape-only invoke or qualified Unaided (large Unaided stages name a phase-table concept class) — never a product allowlist. Untagged bullets do not satisfy a stage. Fold external requirements/design/planning output by kind: requirements → `prd.md`, design → `spec.md`, breakdown → `plan.md` Steps; never a foreign root `SPEC.md` or `tasks/plan.md` as a second fact source.

For a non-trivial task:

```text
planning → ready → in_progress → checking → completed
    │                         │
    └──────── blocked ◄────────┘
```

- `planning`: requirements, evidence, design, or applicable repository documents are still being clarified.
- `ready`: PRD, required Spec, and Plan are complete and awaiting user approval.
- `in_progress`: the user approved the current Task version; implementation is allowed.
- `checking`: implementation is done and acceptance/quality verification is running.
- `blocked`: a concrete blocker is recorded with reproduction, attempts, and needed input; resume the prior phase when cleared.
- `completed`: acceptance and verification passed. Execute the archive transaction defined in **Complete and archive** below: move the entire task directory to `TaskFlowDocs/achieved/<task-id>/`, update the linked Todo item's `Task:` path to that achieved path and its status to `done`, then verify the active path is absent, the achieved path exists, and the achieved root PRD and Plan both say `completed`. If any part fails, leave the Todo item not `done`, record the blocker, and do not claim archival completion.

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

Record which repository documents were inspected and which apply. If remote PR-rule discovery was attempted, record its sources, result, and incorporated conclusions without storing sensitive payloads.

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

A `## Change Log` in `plan.md` records work revisions — wording or approach changes, progress, results, and other updates that do not alter an approved contract. Append one line per revision and keep the current Task version. Only a Task-version material change bumps `vN`, updates every core document atomically, and returns to approval. Do not treat a wording or approach clarification as a Task-version event.

Include checkpoints after meaningful groups of steps. Record risks, deviations, verification results, review findings, and unresolved follow-ups. `Skills / Tools Used` is required: stage-tagged invoke or Unaided lines as each document starts (see the capability section); do not leave the section blank. `task approve` rejects missing stages and unqualified stage Unaided lines.

Record approval as:

```markdown
## Approval
- Status: approved
- Approved by: <user / role>
- Approved at: YYYY-MM-DD HH:mm +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan
```

After the user has approved, write those five fields with `task approve <task-id> [approver]` (default approver `user`). The hook only transcribes the decision you already have; it does not approve on its own. Hand-edit the block only when the hook is unavailable.

### 5. Build — implement by Plan

Before the first edit, confirm the task's working tree is still the one you are in — isolation was established in Phase 1, before the first document, and this phase only carries it forward. If it was skipped, do it now before editing: `git worktree add .worktrees/<slug> -b <type>/<slug> <base>`, then move the work there. Read the applicable repository guidance first — `CONTRIBUTING.md` names the branch prefixes and the base-branch rule; follow it when the repository states one, and otherwise branch as `<type>/<description>` off the intended base. Record the branch and worktree in `plan.md` when they are not obvious from the task directory.

Every task appends to the one `TaskFlowDocs/todo.md`, so merging parallel branches touches that file even when the branches share nothing else. TaskFlow installs a per-entry Git merge driver for it (see [runtime.md](references/runtime.md)); merge the branches locally so it runs, and expect an ordinary content conflict when a pull request is merged in a hosting web UI.

When a merge or rebase you run hits a conflict, stop and put both sides in front of the user, who decides what to keep; do not silently choose one. Record that decision in the task `plan.md` before continuing. An automatic merge needs no action. A conflict on a pull request merged in a hosting web UI is outside this rule — that path is resolved on the platform, not by the Agent.

After approval, read `prd.md`, `spec.md` if present, `reference/` if present, and `plan.md`. Implement one focused Step at a time. Keep changes within the PRD scope and current Spec contracts. Update `plan.md` after each meaningful Step and run its smallest useful check.

If an approved goal, requirement, acceptance criterion, scope, or Spec/architecture contract changes materially, stop implementation, archive the old logical version, create the next Task version, update all existing core documents atomically, and return to `ready` for approval. A change to implementation wording or approach within the approved design is a work revision: update the affected documents and add one change-log line, without a new Task version.

The same rule applies when the applicable repository-document contract changes materially: archive the prior Task version first, update `prd.md`, `spec.md`, and `plan.md` atomically, return to `ready`, and obtain approval before implementation. Never extend a `completed` task in place.

If another tool or Skill creates files or conclusions, review and route only incorporated facts before treating them as task facts. Do not let automation skip approval, expand scope, delete history, or write secrets.

### 6. Verify and review

Enter `checking` only after implementation is complete. Verify in this order:

1. changed-file scope and Git/file archive state;
2. any conflict raised by a merge or rebase in this task: resolved as the user decided and recorded in `plan.md`;
3. every PRD acceptance criterion;
4. Spec contracts when `spec.md` exists, or the `No spec required` rationale;
5. Plan steps, deviations, rollback points, change-log entries, and follow-ups;
6. relevant evidence in `reference/`;
7. project lint, type checks, unit/integration/end-to-end tests as applicable;
8. debug code, temporary bypasses, uncovered branches, and unrelated changes.

Record each command and result in `plan.md`. Distinguish pre-existing failures, newly introduced failures, and environment failures. A test pass does not replace product acceptance.

### 7. Complete and archive

The archive transaction below is the single definition; `artifacts.md` and `versioning-and-recovery.md` reference it rather than restate it.

Before moving the task to `TaskFlowDocs/achieved/`, confirm all acceptance criteria pass, verification is recorded, the current Task version is consistent across existing core documents, unresolved items are explicit follow-ups, and no other agent is writing core documents. Mark the task `completed`, move the entire directory, update the linked Todo item's `Task:` path to `TaskFlowDocs/achieved/<task-id>/` and status to `done`, then verify the active path is absent, the achieved path exists, and the achieved root PRD and Plan both say `completed`. If any part fails, record the blocker and do not claim archival completion.

Treat achieved tasks as read-only in place. A later request that belongs to one must first retrieve the entire directory to the active root, record the Todo source and reopen reason, create a new Task version, and obtain approval. Stage the retrieval before reading full archives: read `old/vN/version.md` change summaries and the achieved `plan.md` first, then read a full archived document set only when the current documents or the version summary require it. Create a related task only for a new independent outcome or different owner/accountability.

After completion, promote only verified, cross-task rules into the project's shared specification/guides. Leave task-specific decisions, personal preferences, unverified ideas, and temporary workarounds in the task artifacts.

Host/harness hooks may run as side effects during the flow but are bounded by [runtime.md](references/runtime.md): they never write core documents, never approve, and only update Todo triage metadata or inject derived context. Do not let a hook's presence skip the approval gate or expand scope.

Publishing, merging, deployment, or delivery processes managed by other tools are external to this framework. They may be not applicable and do not replace `completed` or `TaskFlowDocs/achieved/`.

## Sessions and collaboration

Use `sessions.md` only when cross-session or cross-agent continuation is useful. Record platform, session ID, availability, code working directory, task artifact directory, Task version, phase, last completed Step, next Step, status, and resume command. Do not store chat transcripts, model reasoning, full logs, secrets, or tokens. The SessionStart hook maintains the mechanical fields of the selected task's session entry — session id, agent, availability, timestamps, directories, Task version/phase — so normally you only add `Last completed`, `Next step`, and `Notes`, and you remain the only writer that closes an entry. Never treat the hook's entry as progress: `plan.md` stays authoritative for steps and verification.

Only one named owner may write `prd.md`, `spec.md`, `plan.md`, or `reference/index.md` at a time. Agents may read in parallel and produce independent research/review notes. The Primary Agent or user merges conclusions, changes Task version, records approval, and changes the phase. On handoff, the old owner updates `sessions.md` and `plan.md`; the new owner reads the current artifacts before writing. If a task has multiple agents, designate at most one `Primary` session.

## Safety and scope

- Do not delete, overwrite, commit, push, or archive user files unless the task and user authorization allow it.
- Do not put secrets, tokens, private data, or unauthorized sensitive material in any task artifact, snapshot, or patch; use redacted placeholders.
- Restore historical file versions only in a new temporary restore root; never overwrite the current task directory.
- Design documents may stay out of Git: file-mode `old/vN/` archival remains a valid recovery store. See [versioning-and-recovery.md](references/versioning-and-recovery.md).
- Host/harness hooks may update Todo triage metadata, deterministically maintain repository-document index metadata, and inject derived session-start routing/state context, but never create, rewrite, or delete core task documents or source policies, and never approve. See [runtime.md](references/runtime.md).
- Other tools are allowed to manage their own configuration and lifecycle. This skill only specifies how their task-related outputs integrate with this framework.
- A task ID is `YYYY-MM-DD-short-slug`; keep it stable after creation. Resolve same-day slug collisions with a suffix or a more specific slug. Create a new related task only at the outcome/ownership boundary defined in Existing-task-first selection.

## Supporting references

Read these only when needed:

- [artifacts.md](references/artifacts.md) for compact templates and output routing.
- [versioning-and-recovery.md](references/versioning-and-recovery.md) for Task versions, `old/`, Git/file archives, and safe restoration.
- [runtime.md](references/runtime.md) for host/harness hooks (Claude Code, Codex), single-command transitions, and `hooks/` layout.

## Verification

Before declaring a task complete, confirm:

- [ ] Required artifacts exist (`prd.md`, `plan.md`; `spec.md` when large).
- [ ] Current Task version and state are consistent.
- [ ] User approval is recorded before implementation.
- [ ] Every Step has acceptance, verification, and rollback information.
- [ ] Validation results and failure classification are in `plan.md`.
- [ ] Scope, sensitive-data, and concurrent-write checks passed.
- [ ] Completion gates passed before moving to `TaskFlowDocs/achieved/`.
