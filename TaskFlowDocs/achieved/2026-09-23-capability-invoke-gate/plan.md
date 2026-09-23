# Plan — Gate PRD/Spec/Plan on real capability invocation (v2 stage gate)
> Task version: v2
> Status: completed

## Spec Pointers

- `spec.md`

## Reference Pointers

- `old/v1/` — superseded single-blob approve gate
- `TaskFlowDocs/achieved/2026-09-16-capability-selection-enforcement/prd.md`
- `TaskFlowDocs/achieved/2026-09-15-phase-concept-mapping/prd.md`
- `TaskFlowDocs/achieved/2026-09-10-unblock-capability-invocation/prd.md`

## Related Tasks

- Todo `TF-20260923-230f49` (this task)

## Skills / Tools Used

- [PRD] `agent-skills:idea-refine` — purpose: started v2 PRD framing with Define-class invoke before rewriting requirements after material change; outcome: succeeded; incorporated: pre-write stage model, Not Doing = no file-watch hook in v2.
- [Spec] `agent-skills:spec` — purpose: started v2 Spec with Design-class invoke before writing spec.md; outcome: succeeded; incorporated: stage-tag grammar, approve algorithm, neutrality constraints.
- [Plan] `agent-skills:plan` — purpose: started v2 Plan with work-breakdown invoke before writing plan.md body; outcome: succeeded; incorporated: three-step rework sequence with per-step rollback.
- Note: tags demonstrate [PRD]/[Spec]/[Plan]; capability ids are this host only (not an allowlist).

## Preconditions

- [x] Applicable repository documents and personal rules inspected (CONTRIBUTING; no personal rules).
- [x] v1 archived to `old/v1/` before v2 core-doc rewrite (material change).
- [x] For PR creation/update: template path and mapping recorded at PR time.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-24 00:50 +0800
- Approved version: v2
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Approve stage validation in `hooks/task`

- Goal: Reject plans missing required stages or with invalid stage lines; pass complete sets; fail before Approval write.
- Dependencies: v2 approval
- Files: `hooks/task`
- Implementation checklist:
  - [x] Parse stage-tagged bullets under Skills
  - [x] required stages from `spec.md` presence (large vs small)
  - [x] missing stage → fail naming stage
  - [x] stage line shape: invoke OR Unaided+considered(+concept class when unaided stage)
  - [x] no product allowlist; placeholder ids pass
  - [x] replace/extend any v1 untagged-only gate so untagged alone fails stages
- Acceptance: PRD A1–A4
- Verification: focused fixtures (matrix) + smoke
- Rollback: `git checkout -- hooks/task`
- Status: done

### Step 2 — Skill + artifacts: pre-write rule and stage tags

- Goal: Agents invoke when **starting** each document; record stage tags; fold foreign output by kind.
- Dependencies: Step 1 contract stable
- Files: `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`
- Implementation checklist:
  - [x] Pre-write ordering for prd/spec/plan documented
  - [x] Stage tag shape documented with example lines
  - [x] Approve stage gate described; output-kind fold kept; no vendor allowlist
  - [x] Concept table unchanged
- Acceptance: PRD A5
- Verification: grep pre-write + stage-tag + no product names in gate text
- Rollback: `git checkout --` skill files
- Status: done

### Step 3 — Smoke stage matrix + full suite

- Goal: Prove strategy; full green.
- Dependencies: Steps 1–2
- Files: `hooks/smoke-test`
- Implementation checklist:
  - [x] Large missing [Spec] → fail
  - [x] Large three invoke stages → pass
  - [x] Stage Unaided invalid → fail naming stage
  - [x] Small PRD+Plan pass; small missing [PRD] fail
  - [x] Existing heading/concept-table pins still pass
  - [x] `bash hooks/smoke-test` green; pkill; re-run once if needed
- Acceptance: PRD A6; A7 = this plan’s three tagged lines
- Verification: smoke; `quick_validate.py skills/taskflow`; `git diff --check`
- Rollback: `git checkout -- hooks/smoke-test`
- Status: done

## Checkpoints

- After Step 1: stage matrix passes on fixtures without docs change.
- After Step 2: wording matches code.
- Before `checking`: all boxes + full smoke.

## Verification / Review

- Scope: `hooks/task`, `hooks/smoke-test`, `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, task docs + todo — matches In Scope.
- Stage matrix (focused, product-neutral placeholders): 8/8 expected outcomes — large missing Spec fail; large 3 unaided concept pass; stage Unaided no considered fail naming stage; large 3 invoke pass; small PRD+Plan pass; small missing PRD fail; untagged-only fail; empty fail.
- PRD A1–A4: covered by matrix + smoke approve section.
- PRD A5: SKILL/artifacts state pre-write + stage tags + approve stages; no product names in gate text.
- PRD A6: `bash hooks/smoke-test` → ALL SMOKE PASSED (exit 0); `quick_validate.py skills/taskflow` → Skill is valid!; `git diff --check` clean.
- PRD A7: plan Skills has [PRD]/[Spec]/[Plan] tagged invoke lines used when starting v2 docs.
- Strategy proof: missing/invalid stage rejected with Approval left pending; complete stage set accepted — **effective**.
- Conflicts: none. Leftovers: none.

## Change Log

- 2026-09-23 — v1 planning: untagged approve-time Skills gate; three host invokes.
- 2026-09-23 — v1 work revision: de-overfit to capability-set-agnostic contract.
- 2026-09-24 — **v2 material change** (user): invoke must start with each document write; stage-tagged records; approve verifies stages; v1 docs → `old/v1/`; return to planning for re-approval.
- 2026-09-24 — v2 approved (user); Steps 1–3 implemented; stage matrix 8/8 + full smoke green; entered checking.

## PR template mapping (`.github/pull_request_template.md`)

- Summary → PR body: pre-write stage gate for PRD/Spec/Plan capability invocation.
- TaskFlow traceability → Task: `TaskFlowDocs/achieved/2026-09-23-capability-invoke-gate/`; Scope: In Scope in prd.md; Base: `main`; Target: `https://github.com/hkwuks/TaskFlow` (origin, no credentials).
- Verification checkboxes → smoke / diff --check / skill validate / this Plan.
- Review boundaries → no secrets; In Scope only; remote/base stated; limitations in PR body.

## Follow-ups

- Optional: hook that refuses first write to `prd.md` without a [PRD] line (temporal enforcement).
- Optional: SessionStart concept-class candidate injection.

## Version History

- v2 — pre-write per-document invoke + stage gate (awaiting approval).
- v1 — single approve-time untagged gate; superseded.
