# Plan — Token-saving lifecycle scripts
> Task version: v1
> Status: completed

## Skills / Tools Used

- `taskflow` — purpose: task lifecycle and approval; outcome: succeeded; incorporated: approved v1 artifacts.
- `skill-creator` — purpose: keep deterministic scripts scoped to repeated work; outcome: succeeded; incorporated: one dispatcher and existing resources, no new dependency.
- `ponytail` — purpose: minimize code and output; outcome: succeeded; incorporated: shared parser and one-line success messages.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-10 22:55 +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan and explicit-write/automatic-summary design.

## Steps

### Step 1 — Implement shared lifecycle command
- Implementation checklist:
  - [x] Implement intake and promote.
  - [x] Implement state and progress.
  - [x] Implement guarded complete using existing archive.
- Acceptance: all five operations are deterministic and concise.
- Verification: isolated command fixture.
- Rollback: remove `hooks/task` and revert docs/tests.
- Status: done

### Step 2 — Optimize resume summary and document commands
- Implementation checklist:
  - [x] Add only high-value next-step/approval context to the existing summary.
  - [x] Update runtime, artifact, Hook, and README command guidance.
- Acceptance: Agent can resume and perform mechanical updates without rereading full task documents.
- Verification: summary fixture and link/text checks.
- Rollback: revert summary/docs changes.
- Status: done

### Step 3 — Verify and review
- Implementation checklist:
  - [x] Run focused and full smoke tests.
  - [x] Run syntax, JSON, scope, and diff checks.
- Acceptance: all tests pass with no automatic write Hook.
- Verification: recorded command results.
- Rollback: revert this task's scoped changes.
- Status: done

## Verification / Review

- 2026-09-11: Complete lifecycle passed through Windows PowerShell 5.1, `cmd.exe`, Git Bash, Python, and archive.
- 2026-09-11: The Windows fixture preserved a Unicode goal and used a repository path containing spaces and Chinese characters.
- 2026-09-11: Rejected transitions returned nonzero through `run-hook.cmd`; fixed premature `%ERRORLEVEL%` expansion with delayed expansion.

## Change Log

- 2026-09-11 work revision — expanded Windows verification to the full lifecycle through PowerShell 5.1 and `cmd.exe`; affects launcher exit propagation, Windows smoke coverage, and runtime documentation.

## Version History

- v1 — approved and in progress.
