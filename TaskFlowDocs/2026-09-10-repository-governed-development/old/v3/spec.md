# Spec — Repository-governed fork development

- Task version: v3
- State: checking

## Objective and success criteria

Extend the TaskFlow documentation contract so an Agent follows the target repository's governance and fork topology before implementation, and helps the user establish missing governance through evidence-based, explicitly approved repository documents.

Success means the workflow is deterministic about discovery, precedence, remote safety, missing-document policy, approval, and task-record fields while remaining host- and provider-agnostic.

## Architecture boundaries and responsibilities

### TaskFlow Skill

- Owns discovery order, source precedence, governance-gap classification, fork checks, question limits, approval gates, catalog refresh, and task-artifact routing.
- Does not own Git hosting, remote mutation, PR creation, or enforcement outside the documented workflow.

### Repository-owned governance

- Lives at conventional repository locations and is authoritative after user/repository approval.
- Describes shared project policy derived from repository evidence and explicit maintainer decisions.

### Personal supplements

- Live only under `TaskFlowDocs/repository-docs/personal/`.
- Add scope-matched personal discipline without replacing or weakening shared repository policy.

### Task artifacts

- `prd.md` records product requirements and applicable-document conclusions.
- `spec.md` records contracts and invariants when required.
- `plan.md` records reviewed source paths, remote/base facts, governance gaps/drafts/approvals, implementation checks, and verification.
- `repository-docs/index.md` remains derived navigation, never a policy source.

## Decision flow

```text
qualifying task
  → inspect repository and catalog
  → discover conventional and host-provided governance
  → classify applicable sources and precedence
  → inspect configured remote/base topology when Git or PR work applies
  → identify governance gaps
      → CONTRIBUTING/CODE_STYLE missing for non-trivial development: derive and draft
      → ROADMAP missing: ask for product direction before drafting
      → other document missing: draft only when task-dependent
  → ask only evidence-undecidable questions (maximum three per turn)
  → record evidence and proposed governing effect in Plan
  → obtain explicit approval for new/materially changed governance
  → refresh catalog and re-evaluate task contract
  → approve task Plan
  → implement on an appropriate branch
```

## Source precedence and conflict contract

1. Applicable repository rule.
2. Applicable repository guidance.
3. Scope-matched personal supplement that is stricter or orthogonal.
4. Task-specific approved decision where the repository leaves discretion.

Lower-priority sources cannot weaken or contradict higher-priority sources. Any contradiction pauses planning or implementation and names both sources plus the conflicting rule for user resolution.

## Governance discovery contract

The workflow checks conventional filenames and platform locations without assuming every repository has every class:

- README/project overview;
- contributing and development workflow;
- code style and language conventions;
- roadmap/product direction;
- release and changelog policy;
- code of conduct;
- PR/issue templates and CODEOWNERS;
- branch protection and CI guidance available from local or authorized host metadata;
- scoped personal supplements.

The catalog records class, repository-relative source, existence, and last-checked date. Discovery does not copy or symlink repository-owned sources into `repository-docs/`.

## Missing-governance contract

### Baseline documents

For non-trivial development, missing `CONTRIBUTING.md` or `CODE_STYLE.md` is a planning blocker. TaskFlow:

1. gathers repository evidence;
2. distinguishes confirmed practice from policy choices;
3. asks only unresolved choices;
4. drafts the smallest useful document at the repository root (or established conventional location);
5. lists evidence and intended governing effect in the Plan;
6. obtains explicit user approval;
7. refreshes the catalog before task implementation.

### Direction-dependent document

`ROADMAP.md` is never inferred solely from code or commit history. TaskFlow first obtains confirmed product direction, then drafts it for explicit approval.

### Task-dependent documents

README, PR templates, CODEOWNERS, CI, release, code-of-conduct, and similar sources are proposed only when the current task or repository lifecycle needs them. Security, ownership, and CI policy are never fabricated.

### Minimum quality

A created document must:

- identify its scope and intended audience;
- state only evidence-backed or user-approved rules;
- give runnable commands/checks where the repository exposes them;
- identify approval-sensitive exceptions;
- avoid placeholders, generic boilerplate, secrets, and unverifiable claims.

## Fork and remote contract

For work involving Git remotes, forks, or PRs, record:

- configured remotes and their URLs with credentials redacted;
- inferred repository role only when supported by evidence;
- intended PR target repository and base branch;
- local working branch and known base relationship;
- whether local remote-tracking information may be stale;
- applicable contribution, branch, CODEOWNERS, PR-template, and CI rules;
- pre-PR verification commands/checks.

Remote names are conventions, not truth: `origin` is not automatically treated as the fork and `upstream` is not required to exist. Discovery never silently mutates remote configuration or repository history. Fetch/rebase/merge/push/PR operations require ordinary workflow authorization; ambiguous target or base facts require user resolution.

## Task state and approval invariants

- Governance discovery and gap resolution happen before `in_progress` for non-trivial tasks.
- A draft governance document does not govern implementation until explicitly approved.
- A material governance change affecting an already approved task triggers the existing Task-version gate.
- Governance-document approval and task Plan approval are recorded separately when both occur.
- Existing unrelated active tasks are not modified.

## Project structure / affected files

- `skills/taskflow/SKILL.md` — authoritative operational workflow.
- `skills/taskflow/references/artifacts.md` — compact Plan/catalog recording fields if necessary.
- `README.md` — English user-facing behavior.
- `README.zh-CN.md` — Chinese user-facing behavior.
- `hooks/smoke-test` — focused durable assertions only if existing test structure supports them.
- `hooks/repository-check` — opt-in read-only governance and fork/remote readiness command.

Plugin manifests are excluded unless their declared metadata becomes inaccurate.

## Repository-check command contract

`hooks/repository-check [repo-root]` exits non-zero when review requires user input or is blocked, and zero only when no blocking finding is present. It reports:

- repository root and current branch;
- configured remote names and credential-redacted URLs;
- whether `CONTRIBUTING.md`, `CODE_STYLE.md`, and `ROADMAP.md` exist;
- whether `TaskFlowDocs/repository-docs/index.md` exists;
- base/target ambiguity and stale-data caveats;
- a concise remediation list.

The command is read-only, has no network dependency, does not infer remote roles from names, and is not registered with `session-start` in v2.

## Validation and error semantics

- Missing baseline governance: keep task before implementation and name the required draft/decision.
- Source conflict: stop and present the exact competing sources and rules.
- Ambiguous remote/target/base: do not infer; request user direction.
- Unavailable remote-host metadata: record the attempted source and limitation; do not claim synchronization.
- Unsupported or absent build/test command: do not invent one; document the evidence gap.

## Code and test constraints

- Prefer the smallest documentation diff that centralizes the rules in the Skill and summarizes them in READMEs.
- Reuse existing artifact and smoke-test structures; add no dependency or new runtime component.
- Keep English and Chinese semantics aligned rather than requiring sentence-level translation identity.
- Do not add compatibility code.

## Design alternatives rejected

- Always generate every conventional governance file: rejected because roadmap, ownership, security, release, and CI policy require repository-specific authority.
- Keep all missing policy in `personal/`: rejected because shared repository governance belongs in repository-owned documents.
- Assume `origin` is the contributor fork and `upstream` is authoritative: rejected because remote names are not reliable evidence.
- Automatically repair remote topology or synchronize branches: rejected because it mutates Git state beyond discovery and may target the wrong repository.

## Open questions

None.
