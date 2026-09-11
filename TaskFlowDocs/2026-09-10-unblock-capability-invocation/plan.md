# Plan — Unblock autonomous capability invocation
> Task version: v1
> Status: checking

## Spec Pointers

- `spec.md` — capability lifecycle and Host/Agent/Hook boundaries.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `references/artifacts.md`
- `references/runtime.md`

## Related Tasks

- Related: `TaskFlowDocs/2026-09-10-copy-first-versioning/`

## Skills / Tools Used (Optional)

- `taskflow` — purpose: intake, independent task selection, artifact routing, and approval; outcome: succeeded; incorporated: this approved v1 task contract.
- `agent-skills:using-agent-skills` — purpose: verify selection/invocation semantics; outcome: succeeded; incorporated: a selected Skill is actually invoked while selection remains autonomous.
- `skill-creator` — purpose: constrain project Skill edits; outcome: succeeded; incorporated: preserved autonomy and updated only non-obvious routing/recording rules.
- `agent-skills:test-driven-development` — purpose: assess regression evidence; outcome: succeeded; incorporated: deterministic contract assertions without mocking model behavior.
- `agent-skills:code-review-and-quality` — purpose: final five-axis review; outcome: succeeded; incorporated: mirror, scope, simplicity, and failure-semantics checks.
- `ponytail` — purpose: avoid an enforcement subsystem; outcome: succeeded; incorporated: narrow instruction fix plus deterministic invariant checks.

## Preconditions

- [x] Existing TaskFlow capability and Hook contracts inspected.
- [x] The relevant `agent-skills` invocation contract loaded and reviewed.
- [x] User confirmed autonomous selection, no forced tool, no Hook intent inference, and truthful invocation evidence.
- [x] PRD / Spec / Plan v1 approved by the user.

## Approval

- Status: approved
- Requested at: 2026-09-10 19:53 +08:00
- Approved by: user
- Approved at: 2026-09-10 19:54 +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Clarify the capability lifecycle

- Goal: Remove the gap between autonomous selection and actual invocation.
- Dependencies: v1 approval.
- Files: `SKILL.md`, `skills/taskflow/SKILL.md`.
- Implementation checklist:
  - [x] Preserve free, relevance-based selection.
  - [x] Define selection, invocation, review, incorporation, and recording in order.
  - [x] Define non-blocking behavior for failed optional capabilities.
  - [x] Keep Hook/model responsibilities separate.
- Acceptance: The Skill neither forces a tool nor permits selected-but-uninvoked capabilities to be presented as used.
- Verification: Targeted contract review and root/package comparison.
- Rollback: Revert the two Skill files.
- Status: done

### Step 2 — Align recording guidance and checks

- Goal: Make Plan evidence truthful and leave a runnable regression guard.
- Dependencies: Step 1.
- Files: minimal relevant reference mirror(s) and existing validation surface.
- Implementation checklist:
  - [x] Define successful and failed/unavailable invocation records.
  - [x] Add the smallest deterministic invariant check that guards the contract.
  - [x] Avoid model mocks and mandatory tool lists.
- Acceptance: Mere discovery/selection cannot be documented as incorporated tool use under the project contract.
- Verification: Focused check plus mirror comparison.
- Rollback: Revert Step 2 files.
- Status: done

### Step 3 — Review

- Goal: Confirm the change removes obstacles without reducing Agent autonomy.
- Dependencies: Steps 1–2.
- Files: changed files only.
- Implementation checklist:
  - [x] Search for contradictory fixed-chain or discovery-as-use language.
  - [x] Run repository checks and `git diff --check`.
- Acceptance: No fixed tool requirement, user-config edit, or Hook enforcement is introduced.
- Verification: Diff review and recorded checks.
- Rollback: Revert this task's changed files only.
- Status: done

## Checkpoints

- After Step 1: manually verify all four responsibility boundaries.
- After Step 2: focused invariant check passes.

## Verification / Review

- TaskFlow preserves autonomous capability selection and introduces no fixed tool/provider/chain/count requirement.
- Root/package Skill and reference mirrors are byte-identical.
- The existing smoke test asserts that selection is not invocation and that no capability is mandatory.
- Targeted contradictory-language search returned no matches; `git diff --check` passed.
- Review confirmed Hooks do not infer intent, optional failures remain non-blocking, and only actual invocation attempts may be recorded.

## Change Log

- 2026-09-10 v1 planning — clarified free selection, unobstructed invocation, and truthful evidence requirements; affects PRD / Spec / Plan.
- 2026-09-10 v1 implementation — implemented and verified the invocation contract; task is checking pending user acceptance and archive permission.

## Follow-ups

Host-level telemetry only if a separate reproduced host invocation failure remains after this contract fix.

## Version History

- v1 — ready for approval.
