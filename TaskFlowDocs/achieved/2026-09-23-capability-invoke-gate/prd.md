# Gate PRD/Spec/Plan on real capability invocation: large tasks need one real invo
> Task version: v2
> Status: completed

## Goal

Capability invocation must start **when each document starts being written** (PRD, Spec, Plan), not after the draft and not skipped: stage-tagged records in `Skills / Tools Used`; `task approve` verifies every required stage; TaskFlow documents the pre-write invoke rule and foreign-output fold; concept-class candidates are considered against the live host inventory at that moment.

## Background / Confirmed Facts

- v1 (superseded, see `old/v1/`) gated only once at approve on a single untagged Skills section — after PRD/Spec were already written. User feedback 2026-09-24: that is too late; tools must be invoked **as each document starts**, not retroactively to patch the record.
- Prior layers still apply: concept-class table (`2026-09-15-phase-concept-mapping`), required section (`2026-09-16-capability-selection-enforcement`), selection≠invocation (`2026-09-10-unblock-capability-invocation`).
- Measured 59 achieved plans (2026-09-23): empty/missing 34, Unaided-like 14, invoked-ish 11; large tasks (with `spec.md`) were worst (12 missing / 1 unaided / 4 invoked).
- Host capability sets differ by machine; contract must stay product-neutral (any Skill/tool/MCP/Agent).
- Partial v1 code may remain on the branch until v2 is approved and re-implemented; it is not accepted as the final contract.
- User decisions 2026-09-23 (A/A/A+B) plus 2026-09-24 material clarification: invoke **when starting** each of prd/spec/plan; stage records; approve checks stages.

## Requirements

- R1. **Pre-write rule:** Before drafting `prd.md`, invoke (or record a qualified Unaided decision for) the Define concept class. Same for `spec.md` (Design) and `plan.md` (Plan) when that file is first written in the task — not after the body is complete.
- R2. Stage-tagged lines in plan `## Skills / Tools Used`: each required stage has at least one line prefixed `[PRD]`, `[Spec]`, or `[Plan]` (invoke line or `Unaided — … considered: …` for that stage).
- R3. Large task ( `spec.md` present at approve ): required stages = PRD, Spec, Plan. Small: required stages = PRD, Plan (no Spec file → no Spec stage required).
- R4. Each stage line meets shape rules: non-Unaided invoke (any capability id, purpose/outcome) **or** Unaided with `considered:` naming ≥1 phase-table concept class (for Unaided stages).
- R5. `hooks/task approve` enforces R2–R4 before writing Approval; fail closed with a message naming the missing/invalid stage; no partial Approval write.
- R6. Capability-set agnostic: never allowlist product names in validation or required text.
- R7. SKILL + artifacts: document pre-write invoke ordering, stage-tag shape, foreign fold by output kind (requirements→prd, design→spec, breakdown→plan Steps), no second fact root.
- R8. Smoke proves: missing stage fails; stage with bad Unaided fails; all required stages pass for large and small; placeholder capability ids pass.

## Acceptance Criteria

- A1. Large plan missing `[Spec]` stage (even if PRD/Plan present) → approve fails, Approval stays pending.
- A2. Large plan with `[PRD]`/`[Spec]`/`[Plan]` each an invoke line (placeholder ids OK) → approve succeeds.
- A3. Large plan with all three stages but one Unaided without `considered:` concept class → fails naming that stage.
- A4. Small plan with `[PRD]`+`[Plan]` only → succeeds; missing `[PRD]` → fails; no Spec stage required.
- A5. Skill/docs state: invoke when starting each document; stage-tag shape; approve checks stages; no product allowlist.
- A6. `bash hooks/smoke-test` green including new stage-gate cases; skill validate; `git diff --check` clean.
- A7. This task’s v2 plan records stage-tagged invokes for PRD/Spec/Plan that were used when **starting** those three documents in v2 (demonstration on this host; names not required elsewhere).

## In Scope

- `hooks/task` (approve stage validation — rework any v1 gate)
- `hooks/smoke-test`
- `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`
- Task docs v2 + `old/v1/` + todo lifecycle

## Out of Scope

- Filesystem hooks that block `prd.md` create before a call (deferred; Skill + approve is the v2 mechanism)
- Vendor allowlists; SessionStart full inventory; history rewrite; release path

## Risks / Deferred Items

- Temporal order (invoke truly before first byte of prd) is Skill discipline + stage record, not mtime enforcement — file-watching gate deferred.
- Three stage lines can still be tokenized at approve time.

## Open Questions

None — Q1/Q2/Q3 A/A/A + 2026-09-24 pre-write clarification accepted by user.

## Version History

- v2 — pre-write per-document invoke; stage-tagged Skills; approve verifies stages. Material change from v1.
- v1 — single approve-time untagged Skills gate; superseded (see `old/v1/`).
