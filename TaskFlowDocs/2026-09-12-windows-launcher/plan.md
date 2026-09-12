# Plan — Harden the Windows hook launcher argument forwarding and failure reporting
> Task version: v1
> Status: checking

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `CONTRIBUTING.md`
- `CODE_STYLE.md`
- `.github/pull_request_template.md`
- `skills/taskflow/references/runtime.md`

## Related Tasks

## Skills / Tools Used (Optional)

- TaskFlow — lifecycle and acceptance records.
- incremental implementation — one launcher slice with focused verification.
- git-workflow-and-versioning — dedicated worktree and atomic commit.

## Preconditions

- Dedicated worktree branch: `fix/windows-launcher`.
- Integration baseline: `d05a5ec`.
- Native `cmd.exe` and Windows PowerShell are available from WSL for launcher verification.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-11 (batch authorization; exact time not retained)
- Approved version: v1
- Approved scope: PRD / Plan and implementation of the recorded optimization batch

## Steps

### Step 1 — Implement and verify

- Goal: Forward all launcher arguments safely and retain actionable failure behavior.
- Dependencies: Git Bash on Windows.
- Files: `hooks/run-hook.cmd`, launcher tests, and directly related documentation if needed.
- Implementation checklist:
  - [x] Replace the fixed `%2` through `%9` forwarding path.
  - [x] Add focused regression coverage for count, spaces, Unicode, and quoted values.
  - [x] Verify the missing-Bash diagnostic remains non-zero and clear by preserving the existing branch.
  - [x] Run the Linux smoke suite and diff checks.
- Acceptance: Launcher argument acceptance passes. Full Windows lifecycle is pending a usable Windows Python 3 runtime.
- Verification: Native Windows launcher check — `WINDOWS LAUNCHER ARGS PASSED`; `bash hooks/smoke-test` — passed; `git diff --check` — passed. Full `smoke-test-windows.ps1` reached lifecycle and failed with explicit Python 3 required/exit 127 because Windows Python is unavailable.
- Rollback: Revert the focused launcher commit.
- Status: blocked

## Checkpoints

## Verification / Review

- Native Windows launcher argument check passed.
- Full Windows lifecycle is blocked by missing Windows Python 3; this is an environment prerequisite, not claimed as passed.

## Change Log

- 2026-09-12 — Promoted the approved batch item and began the isolated launcher fix.

## Follow-ups

- Install Python 3 on the Windows host (or set `TASKFLOW_PYTHON` to a Windows Python 3 executable), then rerun `powershell.exe -NoProfile -ExecutionPolicy Bypass -File hooks/smoke-test-windows.ps1` before archiving this task.

## Version History

- v1 — approved and in progress.
