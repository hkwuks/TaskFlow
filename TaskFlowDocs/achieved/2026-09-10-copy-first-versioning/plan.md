# Plan — Copy-first Task versioning
> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md` — transition responsibilities, invariants, and failure semantics.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `references/runtime.md`
- `references/versioning-and-recovery.md`
- `hooks/README.md`

## Related Tasks

- Related: `TaskFlowDocs/2026-09-10-unblock-capability-invocation/`

## Skills / Tools Used (Optional)

- `taskflow` — purpose: intake, task split, artifact routing, and approval gate; outcome: succeeded; incorporated: two independently releasable tasks and approved execution records.
- `skill-creator` — purpose: keep project Skill changes scoped and deterministic; outcome: succeeded; incorporated: reused the existing script and changed only project Skill/reference mirrors.
- `agent-skills:test-driven-development` — purpose: assess regression evidence; outcome: succeeded; incorporated: state-based archive/root assertions in the existing smoke test.
- `agent-skills:code-review-and-quality` — purpose: final five-axis review; outcome: succeeded; incorporated: input validation, mirror checks, scoped diff, and no new dependency.
- `ponytail` — purpose: minimize implementation; outcome: succeeded; incorporated: reused `hooks/version` and its single smoke test without dependencies or abstractions.

## Preconditions

- [x] Windows, PowerShell, date/time, project path, Git state, and CodeGraph absence checked.
- [x] Existing version command and regression coverage inspected.
- [x] Copy scope and script/Agent boundary confirmed by the user.
- [x] PRD / Spec / Plan v1 approved by the user.

## Approval

- Status: approved
- Requested at: 2026-09-10 19:53 +08:00
- Approved by: user
- Approved at: 2026-09-10 19:54 +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Make transition copy-first

- Goal: Preserve old content and retained roots in one preflighted script operation.
- Dependencies: v1 approval.
- Files: `hooks/version`.
- Implementation checklist:
  - [x] Validate the complete transition before mutation.
  - [x] Copy selected documents instead of moving them.
  - [x] Update retained root version, ready state, and approval metadata.
  - [x] Verify archive/root consistency before success.
- Acceptance: The command satisfies every Spec invariant without Agent full-file reconstruction.
- Verification: Focused temporary TaskFlowDocs invocation.
- Rollback: Revert `hooks/version` only; temporary test data is disposable.
- Status: done

### Step 2 — Update regression and contract text

- Goal: Lock in copy-first behavior and remove contradictory documentation.
- Dependencies: Step 1.
- Files: `hooks/smoke-test`, relevant project README/Skill/reference mirrors.
- Implementation checklist:
  - [x] Assert root preservation and archived old bytes.
  - [x] Assert ready state and invalidated prior approval.
  - [x] Update only text that contradicts the implemented transition.
- Acceptance: Documentation and tests describe the same command behavior.
- Verification: Bash syntax checks, `hooks/smoke-test`, and targeted text search.
- Rollback: Revert Step 2 files.
- Status: done

### Step 3 — Review

- Goal: Confirm minimal scope, safety, and no token-heavy fallback remains.
- Dependencies: Steps 1–2.
- Files: changed files only.
- Implementation checklist:
  - [x] Review diff and callers of `hooks/version`.
  - [x] Run `git diff --check` and focused regressions.
- Acceptance: No unrelated changes or new dependency; all checks pass.
- Verification: Diff scope plus recorded command results.
- Rollback: Revert this task's changed files only.
- Status: done

## Checkpoints

- After Step 1: focused transition behavior passes before documentation edits.
- After Step 2: full Hook smoke test passes.

## Verification / Review

- Git Bash syntax checks passed for `hooks/version` and `hooks/smoke-test`.
- `hooks/smoke-test`: `ALL SMOKE PASSED`, including copied old bytes, retained roots, unchanged-document exclusion, ready state, approval reset, invalid-input preflight, and capability-contract mirrors.
- Root/package mirror hashes agree; contradictory move/rewrite text search returned no matches.
- `git diff --check` passed; no dependency, user-level configuration, plugin cache, commit, push, delete, or task archive was introduced.
- Five-axis review found no blocking correctness, readability, architecture, security, or performance issue.

## Change Log

- 2026-09-10 v1 planning — recorded user-approved copy-first and deterministic-script boundaries; affects PRD / Spec / Plan.
- 2026-09-10 v1 implementation — implemented and verified copy-first versioning; task is checking pending user acceptance and archive permission.

## Follow-ups

None.

## Version History

- v1 — ready for approval.
