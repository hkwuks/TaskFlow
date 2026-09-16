# Plan — Personal rules live in repository-docs/ and are local-only
> Task version: v2
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `CONTRIBUTING.md`
- `CODE_STYLE.md`
- `skills/taskflow/SKILL.md` (Repository document environment, Missing repository rules and personal rules)
- `hooks/repository-docs-context` (index sync + route output)

## Related Tasks

- Depends on: None
- Related: `TaskFlowDocs/2026-09-14-session-id-record/` (same user request, independent deliverable)
- Related: `TaskFlowDocs/2026-09-14-untrack-workflow-draft/` (same class of tracked-status change)
- Blocks: None

## Skills / Tools Used (Optional)

## Preconditions

- [x] Applicable repository documents and personal supplements inspected; precedence/conflicts recorded.
- [x] For remote/fork/PR work: not applicable.
- [x] For PR creation/update: not applicable.
- [x] Missing governance drafts and explicit approvals recorded before they become binding.
- [x] Work isolation: this task runs on `docs/personal-docs-git-boundary` inside its own worktree.
- [x] User authorization recorded for removing `TaskFlowDocs/repository-docs/personal/` (user decision, 2026-09-15).

## Approval

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

## Steps

### Step 1 — Implement and verify

- Goal: Move personal rules directly under `repository-docs/`, give them a first-class but clearly subordinate route line, and keep them out of Git.
- Dependencies: User authorization to delete `TaskFlowDocs/repository-docs/personal/`.
- Files: `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, `README.md`, `README.zh-CN.md`, `.gitignore`, `hooks/repository-docs-context`, `hooks/smoke-test`, `TaskFlowDocs/repository-docs/index.md`, `TaskFlowDocs/repository-docs/personal/` (removed).
- Implementation checklist:
  - [x] Scan `repository-docs/*.md` except `index.md` as class `personal-rule`, status `local-only` (R4).
  - [x] Print a dedicated `- Local personal rules (...)` route line and keep them out of `Read authoritative sources:` (R5).
  - [x] Drop the carried-over row for a personal rule that no longer exists, keeping the sync idempotent (R6).
  - [x] Replace `## Personal supplements` with `## Personal rules` in the generated index (R4).
  - [x] Update `SKILL.md`, `artifacts.md`, `README.md`, and `README.zh-CN.md` to the new location and boundary (R1–R3, R9, R10).
  - [x] Point `.gitignore` at the new location while keeping `index.md` tracked (R8).
  - [x] Extend `hooks/smoke-test` with the catalog, route-line, and staleness checks (R4–R6).
  - [x] Remove `TaskFlowDocs/repository-docs/personal/` and regenerate `index.md` (R7).
- Acceptance: PRD acceptance criteria A1–A7 pass.
- Verification: `git check-ignore -v`; `git ls-files`; `TASKFLOW_PHASE=code bash hooks/repository-docs-context` with and without a personal rule; `bash hooks/smoke-test`; `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow`; `git diff --check`.
- Rollback: Revert the Step 1 commit; `git checkout -- TaskFlowDocs/repository-docs/` restores the removed placeholder.
- Status: pending

## Checkpoints

## Verification / Review

## Change Log

- 2026-09-15 Task version — `personal/` subdirectory dropped: personal rules now sit directly in `repository-docs/` with their own injected route line, an ignore rule, and a staleness-aware index sync; affects `hooks/repository-docs-context`, `hooks/smoke-test`, `TaskFlowDocs/repository-docs/`, `skills/taskflow/`, `README*`, `.gitignore`.
- 2026-09-14 work revision — ignore `personal/` in Git and untrack the placeholder README; wording also added to `README.md` and `README.zh-CN.md`.
- 2026-09-15 work revision — Closed out: the work shipped as PR #19 (merged) and is on `main`. Archived with `## Approval` left at `Status: requested`: no commit in this repository's history records an approval for v2, so no approver is named. Recorded as a work revision because implementation is complete and the delivered contract is not being changed.

## Follow-ups

## Version History

- v2 — `personal/` subdirectory dropped; personal rules live directly in `repository-docs/` with their own injected route line and an ignore rule.
- v1 — approval was requested for the original statement-only change; superseded before implementation.
