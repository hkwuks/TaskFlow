# Plan — Add Linux and Windows CI coverage for TaskFlow hooks
> Task version: v1
> Status: checking

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `CONTRIBUTING.md`
- `.github/pull_request_template.md`
- `hooks/README.md`

## Related Tasks

## Skills / Tools Used (Optional)

- TaskFlow — lifecycle and verification record.
- ci-cd-and-automation — minimal cross-platform quality gates.
- git-workflow-and-versioning — isolated worktree and atomic commit.

## Preconditions

- Dedicated worktree branch: `ci/hooks-matrix`.
- Integration baseline: `b9ad6ce`.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-11 (batch authorization)
- Approved version: v1
- Approved scope: PRD / Plan and implementation of the recorded optimization batch

## Steps

### Step 1 — Implement and verify

- Goal: Enforce existing TaskFlow hook checks on Linux and Windows in GitHub Actions.
- Dependencies: GitHub-hosted Ubuntu/Windows runners and Python 3.
- Files: `.github/workflows/` and only directly related documentation if needed.
- Implementation checklist:
  - [x] Add a least-privilege Ubuntu/Windows matrix workflow.
  - [x] Use the existing Bash and PowerShell smoke entrypoints.
  - [x] Provision Python 3 through `actions/setup-python`.
  - [x] Run local workflow parse, smoke, and diff checks.
- Acceptance: The workflow covers both supported operating systems without duplicating lifecycle logic.
- Verification: PyYAML parsed `.github/workflows/hooks.yml`; `bash hooks/smoke-test`; `git diff --check` — passed.
- Rollback: Revert `d9ad0c8`.
- Status: done

## Checkpoints

## Verification / Review

- Workflow grants only `contents: read`.
- `actions/checkout@v4` and `actions/setup-python@v5` are used; no new project dependency was added.
- Local Linux smoke suite passed. Hosted Windows execution will be verified by GitHub Actions after push.

## Change Log

- 2026-09-13 — Promoted the CI item and began isolated implementation.

## Follow-ups

- Inspect the GitHub Actions run after pushing; do not archive if either matrix job fails.

## Version History

- v1 — approved, implemented, awaiting hosted CI.
