# Plan — Repository standards and TaskFlowDocs root
> Task version: v3
> Status: completed

## Spec Pointers
- `spec.md` — standards index contract, bootstrap behavior, user-change trigger, remote discovery behavior, and migration scope.

## Related Tasks
- Depends on: None
- Blocks: None
- Related: None

## Skills / Tools Used
- `taskflow` — routed this non-trivial documentation change through PRD, Spec, and Plan; incorporated the `TaskFlowDocs/` root and standards-index decisions.
- `incremental-implementation` — split edits into standards contract, then documentation migration; incorporated focused searches after each slice.

## Preconditions
- User approved v1 scope in chat on 2026-09-07.
- No existing `tasks/` directory is present in this repository.
- v1 was archived to `old/v1/` before this material contract change.
- v2 was archived to `old/v2/` before this material contract change.

## Approval
- Approved by: user
- Approved at: 2026-09-07 21:25 +08:00
- Approved version: v3
- Approved scope: PRD / Spec / Plan

## Steps
### Step 1 — Define standards mechanism
- Goal: Add the standards index contract and remote PR-rule discovery guidance.
- Dependencies: User approval.
- Files: `taskflow/SKILL.md`, `taskflow/references/artifacts.md`, `TaskFlowDocs/standards/index.md`.
- Acceptance: Index format, applicability, precedence, and remote sync review rules are explicit.
- Verification: Search changed files for `standards`, `remote`, `PR`, and secret-handling guidance.
- Rollback: Revert Step 1 files.
- Status: done (v1)

### Step 2 — Migrate documentation root
- Goal: Replace all default `tasks/` paths with `TaskFlowDocs/`.
- Dependencies: Step 1.
- Files: `README.md`, `README.zh-CN.md`, `taskflow/references/versioning-and-recovery.md`, `assets/taskflow-workflow.svg`.
- Acceptance: No stale active `tasks/` examples remain.
- Verification: `rg -n 'tasks/' .` returns no active references except this task's historical notes, if any.
- Rollback: Revert Step 2 files.
- Status: done (v1)

### Step 3 — Final consistency check
- Goal: Verify all acceptance criteria and changed-file scope.
- Dependencies: Steps 1–2.
- Files: none expected.
- Acceptance: Markdown/SVG references and standards instructions are consistent.
- Verification: repository-wide `rg` checks and `git diff --check`.
- Rollback: Reopen the affected step.
- Status: done (v1)

### Step 4 — Add standards bootstrap and version-transition guard
- Goal: Guide users to define missing applicable standards and ensure future material changes follow Task versioning.
- Dependencies: v2 approval.
- Files: `taskflow/SKILL.md`, `taskflow/references/artifacts.md`, `TaskFlowDocs/standards/index.md`, `README.md`, `README.zh-CN.md`.
- Acceptance: The bootstrap questions, selective creation rules, file minima, explicit waivers, and version-transition behavior are documented consistently.
- Verification: Search for bootstrap and Task-version terms; inspect linked templates and README descriptions.
- Rollback: Revert Step 4 files and retain `old/v1/`.
- Status: done

### Step 5 — Add explicit user-change trigger
- Goal: Ensure a material user correction automatically starts archive, document synchronization, and re-approval.
- Dependencies: v3 approval.
- Files: `taskflow/SKILL.md`, `taskflow/references/artifacts.md`, `README.md`, `README.zh-CN.md`, `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md`.
- Acceptance: Trigger examples, material-change classification, atomic synchronization, and approval gate are explicit.
- Verification: Search all workflow documents for change-trigger and synchronization rules.
- Rollback: Revert Step 5 files and retain `old/v2/`.
- Status: done

## Checkpoints
- After Step 1: standards contract is independently readable.
- After Step 2: root migration is complete before final review.

## Verification / Review
- `rg -n 'User-change trigger|Standards bootstrap|用户.*修正|用户.*新增|实质.*变化' taskflow README.md README.zh-CN.md taskflow/references TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` — passed; trigger and bootstrap rules are present across the workflow documentation.
- `rg -n 'archive.*current|同步.*全部|synchronize.*every|outdated plan|过期 Plan' taskflow README.md README.zh-CN.md taskflow/references TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` — passed; material user changes require archive, synchronization, and re-approval.
- `test -f old/v1/version.md && test -f old/v2/version.md` plus v3 core artifacts — passed; prior versions remain recoverable and current PRD/Spec/Plan agree on v3.
- `git diff --check` — passed; only the existing CRLF normalization warning remains for `versioning-and-recovery.md`.

## Follow-ups
- A provider-specific API synchronizer can be a separate task if a target host and write permissions are specified.

## Version History
- v1 — completed scope; superseded because standards bootstrap and a version-transition correction were needed.
- v2 — adds standards bootstrap and version-transition enforcement; superseded because the user-change trigger remained implicit.
- v3 — adds explicit user-change trigger and synchronization enforcement.
