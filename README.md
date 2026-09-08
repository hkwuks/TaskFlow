<div align="center">

# TaskFlow

### Durable task decisions for coding Agents.

**Local Markdown. Explicit approvals. Recoverable design history.**

[![Workflow: Skill](https://img.shields.io/badge/workflow-Skill-0f766e?style=for-the-badge)](taskflow/SKILL.md)
[![Storage: Local Markdown](https://img.shields.io/badge/storage-local%20Markdown-1d4ed8?style=for-the-badge)](taskflow/references/artifacts.md)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-e11d48?style=for-the-badge)](LICENSE)

[Get started](#get-started) · [Why TaskFlow](#the-problem) · [Compare tools](#where-taskflow-fits) · [中文](README.zh-CN.md)

<img src="assets/taskflow-workflow.svg" alt="TaskFlow workflow: planning, ready, in progress, checking, completed; material changes archive the old version and return to approval." width="100%" />

</div>

> [!IMPORTANT]
> **TaskFlow is a workflow convention, not an Agent runtime.** It does not intercept prompts, tool calls, or model behavior. It gives humans and Agents a shared, inspectable place to record what a task means and how it changed.

<br />

## The problem

When an Agent ships code, the code is visible. The decisions that made it safe are often not.

<table>
<tr>
<td width="50%" valign="top">

### Without a durable task record

```text
chat → draft → edit → new chat → overwrite
               ↑
         "Which design was approved?"
```

- Requirements and design notes live in scattered chats.
- A new session cannot recover the real state of work.
- A requirement change overwrites the original proposal.
- Git records line edits, but not necessarily the decision boundary.
- Handoffs become another round of discovery.

</td>
<td width="50%" valign="top">

### With TaskFlow

```text
task directory → approval → implementation
      │               │
      └ old/vN/ ◀─────┘  material change
```

- One directory holds requirements, design, plan, and verification.
- States make progress and blockers explicit.
- Material decisions create a recoverable Task version.
- Markdown stays reviewable by people, Agents, and Git.
- Handoffs resume from facts instead of memory.

</td>
</tr>
</table>

## The core idea

```text
TaskFlowDocs/YYYY-MM-DD-short-slug/
├── prd.md          # what / why / scope / acceptance
├── spec.md         # how / contracts / trade-offs       (large tasks only)
├── plan.md         # approval / steps / verification / rollback
├── sessions.md     # handoff and resume context         (optional)
├── reference/      # evidence and research              (optional)
└── old/vN/         # superseded logical versions         (optional)
```

TaskFlow deliberately uses plain files. A human can read them, an Agent can load them, Git can diff them, and your project does not need another service to keep its task history.

## Repository documents

`TaskFlowDocs/repository-docs/index.md` is one catalog for repository rules, repository guidance, and scoped personal supplements. It provides unified navigation to existing README, contributing, code-style, release, roadmap, PR, and CI guidance without copying source content.

Before a non-trivial task is planned or implemented, TaskFlow refreshes the catalog only when it is absent, stale, or the task needs an uncataloged class, then reads documents applicable to the task phase. It uses relative symbolic links when safely supported; otherwise the catalog's relative paths remain portable. For PR/remote work, it also discovers available contribution guides, PR templates, CODEOWNERS, branch/CI rules, and accessible host metadata. Findings are reviewed before being recorded locally; TaskFlow does not overwrite local rules, require a provider API, or copy secrets.

Repository documents are authoritative. If a needed rule is absent, TaskFlow pauses implementation and guides the user through up to three dependency-ordered questions at a time, with recommendations. Once confirmed, it creates only a scope-matched personal supplement under `repository-docs/personal/`; it cannot weaken, override, or conflict with repository guidance. A material applicable-document change follows the same version gate as any other task-contract change.

Any user correction or addition to an approved task is classified before documents change: wording or approach clarifications are work revisions that update only affected records and the Plan change log; changes to an approved goal, requirement, acceptance criterion, scope, or contract create a Task version and return to approval. TaskFlow never continues implementation using an outdated plan.

## Todo intake

`TaskFlowDocs/todo.md` is the mandatory first record for every direct request and imported requirement, including GitHub Issues. Batch imports retain one Todo item per source requirement, with source and external identifier/link when available. An item moves from `inbox` to `clarified`, then is promoted into a task directory with `prd.md`, optional `spec.md`, and `plan.md`; it enters `in_progress` after approval and closes as `done` or `cancelled`. The inbox retains source identity, lifecycle metadata, and the task link after promotion. Every Plan Step has a checkbox checklist, and cannot be `done` until required items and focused verification pass.

After verification, TaskFlow moves the whole task directory to `TaskFlowDocs/achieved/<task-id>/`, updates the Todo item's task path and status to `done`, and verifies the active path is absent. If later work belongs to that achieved deliverable, it retrieves the directory to the active root, records the Todo source and reopen reason, creates a new Task version, and returns to approval before changing implementation. Achieved tasks are read-only; their `old/vN/` history is read only when the current documents or a version summary require it.

<details>
<summary><strong>Why not just rely on Git?</strong></summary>
<br />

Git is excellent at mechanical history. TaskFlow adds **semantic history**: a task version changes only when an approved goal, requirement, acceptance criterion, scope, architecture/interface/data contract, compatibility decision, risk decision, or standard changes; wording or implementation-approach clarifications are work revisions that stay on the current version. The archived version answers what the previous proposal meant, not merely which lines changed.

</details>

## The non-invasive promise

| TaskFlow adds | TaskFlow deliberately avoids |
| --- | --- |
| A shared `clarify → approve → implement → verify → archive` protocol | Runtime hooks, proxies, daemons, or API gateways |
| Project-local Markdown as task facts | Hidden state in a hosted database or proprietary UI |
| Explicit state, approval, handoff, rollback, and recovery records | Replacing your editor, Git host, test runner, or other Skills |
| A semantic version boundary for material decisions | Forcing an Agent model, programming language, framework, or toolchain |

During clarification, PRD, Spec, Plan, research, and review work, the Agent checks its currently available capabilities and uses those that materially help. TaskFlow does not prescribe a tool, vendor, Skill family, or invocation mechanism; it makes reviewed, incorporated task facts and the surrounding agreement durable.

## The one rule that prevents lost designs

<div align="center">

```text
ordinary edit                 material decision change
─────────────                 ────────────────────────
keep current vN               archive vN → create vN+1 → return to ready → approve
```

</div>

| This is a work revision | This creates a Task version |
| --- | --- |
| Wording, approach clarification within the approved design, typo, progress, test result | Goal, requirement, acceptance criterion, scope, architecture/interface/data contract, compatibility, risk, standard |
| Update current files + one Plan change-log line | Preserve the old version under `old/vN/`, then update current files |
| Git shows the edit | Git plus TaskFlow explain the decision |

### A concrete recovery story

```diff
  TaskFlowDocs/2026-09-05-billing-export/
  ├── prd.md                       # current v2: CSV export added
  ├── spec.md                      # current v2 design
  ├── plan.md                      # v2 approval + verification
+ └── old/v1/
+     ├── version.md               # why v1 was superseded
+     └── snapshot/                # v1 PRD / Spec / Plan recovery point
```

Someone changes the export requirement midway through implementation. Instead of rewriting the only design document, TaskFlow preserves `v1`, records why `v2` exists, and requires a new approval before implementation continues.

## Lifecycle at a glance

```mermaid
stateDiagram-v2
    [*] --> planning
    planning --> ready: PRD / Spec / Plan complete
    ready --> in_progress: explicit approval
    in_progress --> checking: implementation complete
    checking --> completed: acceptance passes
    planning --> blocked
    in_progress --> blocked
    blocked --> planning: input or condition resolved
    in_progress --> ready: material change / new version
    completed --> [*]
```

| State | Meaning |
| --- | --- |
| `planning` | Requirements, evidence, or design are being clarified. |
| `ready` | The current task documents are complete and waiting for approval. |
| `in_progress` | The approved plan is being implemented. |
| `checking` | Acceptance and quality checks are running. |
| `completed` | Verification passed; archive as read-only history. |
| `blocked` | A specific blocker is recorded with the required next input. |

## Get started

```text
1. Add taskflow/ to your project's Agent Skills directory.

2. Tell your Agent:
   Use $taskflow to plan, execute, verify, and archive this task.

3. Add ideas to `TaskFlowDocs/todo.md`; promote clarified items into `prd.md`, `spec.md` (when needed), and `plan.md`.

4. Review the task documents, record approval, then implement one planned step at a time using its checklist.
```

> [!TIP]
> A small, obvious one-file change can still be a direct change with minimal verification. TaskFlow does not create documents merely to satisfy a process.

## Where TaskFlow fits

TaskFlow is not trying to replace specification-driven development, role-based multi-agent methods, or project management. It covers a specific missing layer: **durable task facts, state boundaries, and recoverable decision history inside the repository.**

| | TaskFlow | [Spec Kit](https://github.com/github/spec-kit) | [OpenSpec](https://github.com/Fission-AI/OpenSpec) | [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Issue tracker / PM tool |
| --- | --- | --- | --- | --- | --- |
| **Primary concern** | Task state and semantic history | Spec-driven workflow | Configurable spec/change workflow | Role-based Agent methodology | Ownership and coordination |
| **Core unit** | Local TaskFlowDocs directory | Specs and workflow artifacts | Specs and changes | Agents, roles, workflows | Tickets, cards, issues |
| **Design recovery** | Explicit `old/vN/` archive | Adoption/repository dependent | Project/Git practice dependent | Workflow/repository dependent | Usually activity history only |
| **Agent interaction** | Instructions only; no runtime interception | Tool/workflow conventions | Configurable workflow conventions | Role and orchestration patterns | Usually outside Agent context |
| **Infrastructure** | Markdown + filesystem + Git | Adopted repository tooling | Adopted repository tooling | Method assets + adopted tooling | Usually a hosted service |
| **Use it with TaskFlow?** | — | Generate specs, then route reviewed task facts into TaskFlow | Route reviewed specs/changes into TaskFlow | Keep role outputs as reviewed task references | Link a ticket to its task directory |

### Choose the right layer

<table>
<tr><td><strong>Choose TaskFlow</strong></td><td>You lose task context, overwrite designs, or struggle to resume work across sessions and Agents.</td></tr>
<tr><td><strong>Choose Spec Kit / OpenSpec</strong></td><td>You primarily need a broad or configurable spec-driven development workflow.</td></tr>
<tr><td><strong>Choose BMAD-METHOD</strong></td><td>You need a role-based multi-Agent delivery methodology.</td></tr>
<tr><td><strong>Choose an issue tracker</strong></td><td>You need prioritization, ownership, deadlines, and reports.</td></tr>
<tr><td><strong>Combine them</strong></td><td>Use external tools to coordinate work; use TaskFlow to preserve the decisions that make it recoverable.</td></tr>
</table>

> [!NOTE]
> This is a positioning comparison, not a benchmark or a claim of feature parity. Check each project's current documentation before adoption.

## Guardrails, not bureaucracy

| Principle | In practice |
| --- | --- |
| **One task, one source of truth** | Keep the active task facts in one task directory. |
| **Lightest useful artifact** | Omit `spec.md` for a small, self-contained task. |
| **Archive before replace** | Capture the old logical version before a material update. |
| **Approval is explicit** | `ready` never silently becomes `in_progress`. |
| **Verification is a fact** | Record what was checked and the result in `plan.md`. |
| **Tools stay optional** | Other Skills can contribute; reviewed task artifacts remain authoritative. |

## Project map

```text
taskflow/
├── SKILL.md                         # workflow entry point
├── agents/openai.yaml               # display metadata and default prompt
└── references/
    ├── artifacts.md                 # templates and output routing
    └── versioning-and-recovery.md   # semantic versions and safe restoration
```

## License

Distributed under [AGPL-3.0](LICENSE).
