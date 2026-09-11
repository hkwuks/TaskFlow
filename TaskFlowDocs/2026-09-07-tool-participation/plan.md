# Plan — Allow appropriate tools to contribute to task documents
> Task version: v1
> Status: checking

## Spec Pointers

- `spec.md`

## Reference Pointers

- None. Repository inspection supplied the confirmed facts.

## Related Tasks

- Depends on: None
- Blocks: None
- Related: None

## Skills / Tools Used (Optional)

- `taskflow`: established artifact, approval, and collaboration constraints.
- `context-mode`: performed focused repository and history analysis.

## Preconditions

- User approval of v1 PRD / Spec / Plan is recorded below before implementation.

## Approval

- Approved by: user
- Approved at: 2026-09-07 15:04 +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Add a tool-agnostic collaboration decision
- Goal: In relevant planning phases, require checking available capabilities and use of suitable ones without naming or forcing a tool.
- Dependencies: User approval of the proposed PRD / Spec / Plan.
- Files: `taskflow/SKILL.md`
- Implementation checklist:
  - Add phase-level wording to check available capabilities during clarification, PRD, Spec, Plan, research, and review.
  - Require no record when no capability is used.
  - Preserve non-runtime and tool-agnostic boundaries.
  - Keep routing and final-authority rules explicit.
- Acceptance: All PRD collaboration requirements are represented without a mandated tool list or invocation mechanism.
- Verification: Search the changed sections and review `git diff --check` plus the focused diff.
- Rollback: Revert only this step’s documentation edits before any version/approval change.
- Status: done

### Step 2 — Make actual tool-use traceability actionable
- Goal: Adjust the artifact reference so actual use is recorded with purpose and incorporated conclusion.
- Dependencies: Step 1.
- Files: `taskflow/references/artifacts.md`
- Implementation checklist:
  - Keep tool-use records optional when no capability is used.
  - Define the minimal record content.
  - Preserve existing output routing.
- Acceptance: A document owner can record actual contribution without treating raw output as task fact.
- Verification: Inspect template/routing sections and cross-check against `SKILL.md`.
- Rollback: Revert only the template/reference edit.
- Status: done

### Step 3 — Align public guidance
- Goal: Update both README languages to accurately describe this collaboration model.
- Dependencies: Steps 1–2.
- Files: `README.md`, `README.zh-CN.md`
- Implementation checklist:
  - Explain tool-agnostic evaluation and reviewed routing.
  - Retain the no-interception/no-automatic-invocation claim.
- Acceptance: Both README files match the core rule and do not name a required tool family.
- Verification: Compare the relevant English/Chinese sections and review the focused diff.
- Rollback: Revert only the README edits.
- Status: done

## Checkpoints

- Before editing: User approval of v1 PRD / Spec / Plan.
- Before completion: all acceptance criteria and focused documentation checks pass.

## Verification / Review

- `rg` confirmed phase-level capability-check wording in `taskflow/SKILL.md`.
- `rg` confirmed the optional tool-use record template and candidate-material boundary in `taskflow/references/artifacts.md`.
- Focused English/Chinese README review confirmed matching tool-agnostic, non-runtime guidance.
- `git diff --check` passed.

## Follow-ups

- None.

## Version History

- v1: Proposed tool-agnostic collaboration rule.
