# Plan — Make hooks/version write the same five-field Approval block hooks/task generates

> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/version` — presence check (36–39), reset awk (96–106), post-check
  (114).
- `hooks/task` — promote Approval template (~651–657); `require_approval`
  (503–515) — read-only for this task.
- `hooks/smoke-test` — `== version bumps root + archives only changed docs ==`
  (~607–619).
- `skills/taskflow/SKILL.md` — “Record approval as” (~228–232).
- Sibling: `TF-20260918-454ac4` (out of scope; this is its prerequisite).

## Related Tasks

- `TF-20260919-b7821b` — this task’s ID.
- `TF-20260918-454ac4` — Approval automation; do not implement here.

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell text
  processing and the repository's own hook templates, all read directly.`

## Preconditions

- [x] Docs/rules inspected; worktree `.worktrees/fix-version-approval-shape`
  on `fix/version-approval-shape` from `main` = `17556d2`.
- [x] Measured template vs version reset vs skill snippet; refuse-vs-write
  gap and thin smoke assert recorded in PRD Background.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-23
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — version: write the five-field block

- Goal: R1–R4.
- Files: `hooks/version`.
- Checklist:
  - [x] Keep hard-fail when `## Approval` is missing (R2).
  - [x] Drop/replace the all-five presence gate so a missing `Status` (or
        any one of the five) does not refuse (R3).
  - [x] Reset path: ensure the five field lines exist under `## Approval`
        and carry the R1 values, in template order (insert missing; rewrite
        existing; leave non-field lines — Q2).
  - [x] Post-check: assert all five lines exact (R4).
  - [x] `bash -n hooks/version`.
- Acceptance: A, B, C.
- Status: done

### Step 2 — skill snippet

- Goal: R5 / Q1.
- Files: `skills/taskflow/SKILL.md`.
- Checklist:
  - [x] “Record approval as” shows five lines, same order as promote;
        Status value `approved` for the human record.
  - [x] No second Approval template elsewhere in the skill (Q3: one place).
- Acceptance: D.
- Status: done

### Step 3 — smoke

- Goal: R6/R7.
- Files: `hooks/smoke-test`.
- Checklist:
  - [x] Four-field fixture (no Status): version succeeds; body equals R1
        five lines.
  - [x] Five-field approved fixture: after version, same R1 block (strengthen
        the existing assert beyond `Approved version: pending`).
  - [x] Existing version section still green.
- Acceptance: E.
- Status: done

## Checkpoints

- After Step 1: `bash -n` + targeted fixtures (A/B) before touching skill/smoke.
- After Step 3: one full suite; no chained mutations; pkill if killed.

## Verification / Review

| Check | Result |
|---|---|
| `bash -n hooks/version` | pass |
| `bash -n hooks/smoke-test` | pass |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` |
| `git diff --check` | clean |
| Four-field → five-field write (A) | pass (suite) |
| Five-field reset exact (B) | pass (suite) |
| Skill five-line snippet (D) | pass (suite) |

## Change Log

- v1 — planning; scope version shape + skill snippet + smoke; Q1 Status
  first/`approved` for human record, Q2 leave non-field lines, Q3 skill in
  this PR.
- v1 — approved (user, 2026-09-23); Steps 1–3 done; suite green.

## Follow-ups

- `454ac4` after this lands (hook-driven approve write).
- Housekeeping commit `17556d2` is on local main only (not pushed).

## Version History

- v1 — planning.
- v1 — approved (user, 2026-09-23); Steps 1–3 done; suite green.
