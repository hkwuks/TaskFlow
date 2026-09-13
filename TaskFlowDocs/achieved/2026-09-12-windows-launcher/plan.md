# Plan — Harden the Windows hook launcher argument forwarding and failure reporting
> Task version: v1
> Status: completed

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
- Acceptance: All PRD acceptance criteria pass.
- Verification: Native Windows launcher check — `WINDOWS LAUNCHER ARGS PASSED`; hosted `smoke-test-windows.ps1` — passed on GitHub Actions Windows runner; `bash hooks/smoke-test` — passed; `git diff --check` — passed.
- Rollback: Revert the focused launcher commit.
- Status: done

## Checkpoints

## Verification / Review

- Native Windows launcher argument check passed.
- The original local Windows host lacked Python 3; hosted Windows verification supersedes that environment-only blocker.
- GitHub Actions run `34758209208` passed on `windows-latest` in 22 seconds, including Python 3 setup and the full lifecycle.
- `conda run -n torch python --version` — Python 3.12.12.
- `conda run -n torch bash hooks/smoke-test` — all Linux/WSL smoke checks passed; this does not replace native Windows validation.

## Change Log

- 2026-09-12 — Promoted the approved batch item and began the isolated launcher fix.

## Follow-ups

- No follow-up required; hosted Windows Python 3 verification cleared the previous environment blocker.
- The WSL `torch` environment remains Linux-only evidence; hosted Windows CI provides the native validation.

## Version History

- v1 — approved, implemented, and verified.
