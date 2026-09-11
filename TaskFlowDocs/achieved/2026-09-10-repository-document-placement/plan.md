# Plan — Repository document placement
> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md` — placement boundaries, catalog contract, legacy handling, and validation.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — applicable repository guidance catalog.
- `README.md` and `README.zh-CN.md` — current user-facing repository-document behavior.

## Related Tasks

None.

## Skills / Tools Used (Optional)

- `taskflow` — purpose: manage intake, requirements, design, approval, execution, and verification; incorporated: Todo-first workflow and required artifacts.
- `ponytail` — purpose: minimize the implementation; incorporated: documentation-only change with no migration script.
- `context-mode` — purpose: inspect repository-wide references without flooding context; incorporated: all relevant clauses and duplicate paths identified.

## Preconditions

- [x] Current date, platform, path, Git state, and CodeGraph availability checked.
- [x] Existing repository-document clauses and all callers/consumers inspected.
- [x] User decisions recorded for placement, filenames, personal supplements, non-Git use, and legacy handling.
- [x] User approves Task version v1 for implementation.

## Approval

- Status: approved
- Requested: 2026-09-10
- Approved: 2026-09-10 by user
- Scope: PRD v1 and Spec v1 in this task directory.

## Steps

### Step 1 — Update normative Skill contract
- Goal: Make path-only conventional placement the authoritative TaskFlow behavior.
- Dependencies: v1 approval.
- Files: `SKILL.md`, `skills/taskflow/SKILL.md`
- Implementation checklist:
  - [x] Remove symbolic-link and access-mode behavior.
  - [x] Add conventional creation, personal supplement, non-Git, and legacy handling rules.
  - [x] Keep both copies byte-identical.
- Acceptance: Normative guidance satisfies PRD requirements 1–8.
- Verification: Focused searches plus file-hash comparison.
- Rollback: Revert only these two documentation edits.
- Status: done

### Step 2 — Align compact reference and public documentation
- Goal: Keep supporting and user-facing descriptions consistent with the Skill.
- Dependencies: Step 1.
- Files: `references/artifacts.md`, `skills/taskflow/references/artifacts.md`, `README.md`, `README.zh-CN.md`
- Implementation checklist:
  - [x] Update the compact catalog contract in both references.
  - [x] Update equivalent English and Chinese README sections.
  - [x] Keep both reference copies byte-identical.
- Acceptance: No maintained public/reference text recommends repository-doc links or copies.
- Verification: Focused searches and hash comparison.
- Rollback: Revert only these four documentation edits.
- Status: done

### Step 3 — Verify and review
- Goal: Prove consistency and no lifecycle regression.
- Dependencies: Steps 1–2.
- Files: changed documentation and task artifacts.
- Implementation checklist:
  - [x] Run required/obsolete wording assertions.
  - [x] Compare duplicate file hashes.
  - [x] Run `hooks/smoke-test`.
  - [x] Review the final diff and working-tree scope.
  - [x] Record results here.
- Acceptance: All checks pass and only intended files changed.
- Verification: Command results recorded under Verification / Review.
- Rollback: Revert implementation documentation edits; retain task history.
- Status: done

## Checkpoints

- After Step 1: normative contract is internally consistent.
- After Step 2: all maintained descriptions agree.
- After Step 3: verification and scope review pass.

## Verification / Review

- Documentation contract assertions passed: required placement, non-Git, filename, personal-rule, and legacy-authorization wording is present; obsolete access-mode and relative-link guidance is absent.
- `SKILL.md` matches `skills/taskflow/SKILL.md` byte-for-byte.
- `references/artifacts.md` matches `skills/taskflow/references/artifacts.md` byte-for-byte.
- `bash hooks/smoke-test`: `ALL SMOKE PASSED`.
- `git diff --check`: passed with no whitespace errors.
- Final scope review: six approved maintained documentation files changed; TaskFlow artifacts added; no files moved, deleted, committed, pushed, or published.
- Test-command issue: two initial PowerShell assertions failed because nested command interpolation removed `$` variables; rerun as JavaScript file assertions and passed. This was a verification-command error, not a product failure.
- Task version consistency: PRD, Spec, and Plan are all v1; approval preceded implementation.

## Change Log

- 2026-09-10 v1 planning — captured dependency-ordered user decisions and promoted Todo to PRD/Spec/Plan; affects task artifacts and catalog.
- 2026-09-10 v1 approval — user approved implementation of PRD/Spec v1; affects Plan status.
- 2026-09-10 v1 implementation — updated normative, reference, and bilingual public documentation; affects six maintained files.
- 2026-09-10 v1 verification — all focused assertions, duplicate checks, smoke tests, and diff checks passed; task completed.

## Follow-ups

- Legacy copies or symbolic links found in downstream repositories require a separate explicit migration/deletion decision.

## Version History

- v1 — Approved, implemented, verified, and completed.
