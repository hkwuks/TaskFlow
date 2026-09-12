# Plan — Add explicit cross-platform runtime preflight for Windows Python dependencies
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `CONTRIBUTING.md`
- `CODE_STYLE.md`
- `.github/pull_request_template.md`

## Related Tasks

- `TF-20260911-02` — current-task routing, completed separately.
- `TF-20260911-04` and `TF-20260911-06` — launcher and Windows CI follow-ups.

## Skills / Tools Used (Optional)

- TaskFlow — lifecycle records and completion checks.
- code-review-and-quality — correctness, simplicity, security, and regression review.
- git-workflow-and-versioning — focused worktree commit and integration merge.

## Preconditions

- Worktree branch: `fix/windows-runtime-preflight`.
- Integration branch: `feat/taskflow-optimization-batch` based on `origin/main` at `f50b5b7`.
- Target repository/base: `hkwuks/TaskFlow`, `main`.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-11 (batch authorization; exact time not retained)
- Approved version: v1
- Approved scope: PRD / Plan and implementation of all recorded optimization Todo items

## Steps

### Step 1 — Implement and verify

- Goal: Centralize and validate Python 3 runtime selection for TaskFlow hooks.
- Dependencies: Git Bash and a real Python 3 interpreter.
- Files: `hooks/python-runtime`, Python-backed hooks, `hooks/smoke-test`, `hooks/README.md`.
- Implementation checklist:
  - [x] Implement the approved change.
  - [x] Add a regression check for valid overrides and WindowsApps-style shims.
  - [x] Run focused and full verification.
- Acceptance: All PRD acceptance criteria pass.
- Verification: `git diff --check 1291a0d..d3970c1`; `bash -n` on changed scripts; `bash hooks/smoke-test` — passed on 2026-09-12.
- Rollback: Revert merge commit and `d3970c1` together; callers return to their former local fallback.
- Status: done

## Checkpoints

- Implementation committed as `d3970c1` and merged after full smoke verification.

## Verification / Review

- `git diff --check 1291a0d..d3970c1` — passed.
- `bash -n hooks/python-runtime hooks/task hooks/archive hooks/reopen hooks/summarize-state hooks/repository-docs-context hooks/smoke-test` — passed.
- `TASKFLOW_PYTHON=/does/not/exist bash hooks/python-runtime` — exited 127 with explicit Python 3 guidance.
- `bash hooks/smoke-test` — all checks passed on Linux/WSL2, including the WindowsApps-style shim regression.
- Review found no secret, unrelated-file, security, or performance blocker.
- Native Windows validation is not claimed here; it remains tracked by TF-20260911-06.

## Change Log

- 2026-09-12 — Recorded the already-approved batch slice, implementation commit, review, and verification before archival.

## Follow-ups

- TF-20260911-04 through TF-20260911-08 remain independent Todo items and are not claimed complete by this task.
- PR template mapping: Summary = shared Python 3 preflight; TaskFlow traceability = this achieved task plus the achieved current-task-routing task; Verification = commands above; Review boundaries = no secrets/unrelated files, target `hkwuks/TaskFlow:main`, native Windows CI deferred and disclosed.

## Version History

- v1 — approved, implemented, and verified.
