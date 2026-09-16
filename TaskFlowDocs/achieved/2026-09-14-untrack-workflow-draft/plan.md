# Plan — Stop tracking the workflow draft in TaskFlowDocs
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `CONTRIBUTING.md`
- `skills/taskflow/SKILL.md` (Source of truth — `TaskFlowDocs/` contents)

## Related Tasks

- Depends on: None
- Related: `TaskFlowDocs/2026-09-14-personal-docs-git-boundary/` (same class of tracked-status fix, different file)
- Blocks: None

## Skills / Tools Used (Optional)

## Preconditions

- [x] Applicable repository documents and personal supplements inspected; precedence/conflicts recorded.
- [x] For remote/fork/PR work: not applicable.
- [x] For PR creation/update: not applicable — no PR is created by this task.
- [x] Missing governance drafts and explicit approvals recorded before they become binding.
- [x] Work isolation: this task runs on `chore/untrack-workflow-draft` inside its own worktree.
- [x] User authorization recorded for the tracked-status change (`git rm --cached`, file preserved).

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-14
- Approved version: v1
- Approved scope: PRD / Plan and the `git rm --cached` tracked-status change for `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md`, authorized in the user request "把删除这个文档单独commit并提交"; the work is committed as its own commit.

## Steps

### Step 1 — Untrack and verify

- Goal: Drop the draft from Git tracking without touching the file, history, or any task-discovery logic.
- Dependencies: User authorization for the tracked-status change.
- Files: `TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` (tracked status), `.git/info/exclude` (local leftover exclusion), `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [x] Record the pre-change SHA-256 of the draft.
  - [x] `git rm --cached TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md`.
  - [x] Add the local exclude rule in `.git/info/exclude` so the leftover copy stays out of `git status`.
  - [x] Confirm the SHA-256 is unchanged and no other tracked content moved.
- Acceptance: PRD acceptance criteria A1–A6 pass.
- Verification: `git ls-files` (empty); `sha256sum` unchanged at `079012a8778e3e7b3e4b51e7f0f68a584aa0e2d9d9ce7bd32fa9a0afa9f14e3f`; `git check-ignore -v` matched `.git/info/exclude:8`; `git status --short` showed only the deletion and the Todo change; `bash hooks/smoke-test` — ALL SMOKE PASSED; `git diff --check` — clean.
- Rollback: `git add TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` restores tracking; remove the `.git/info/exclude` line.
- Status: done

## Checkpoints

## Verification / Review

- 2026-09-14 Step 1: `git ls-files TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` empty; SHA-256 unchanged; `git check-ignore -v` matches; `bash hooks/smoke-test` ALL SMOKE PASSED; `git diff --check` clean.

## Change Log

- 2026-09-14 work revision — untrack the draft via `git rm --cached` plus a local `.git/info/exclude` entry; no content or history change.
- 2026-09-15 work revision — Closed out: the work shipped as PR #17 (merged) and is on `main`; `git ls-files TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md` is empty there. Recorded as a work revision rather than a Task version bump because implementation is complete and no approved contract is being changed.

## Follow-ups

- If the draft is ever wanted as durable documentation, place it at a documented repository path outside `TaskFlowDocs/` under the normal document-creation rules.

## Version History

- v1 — planning.
