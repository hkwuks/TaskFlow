# Plan — Gate PRD/Spec/Plan on real capability invocation
> Task version: v1
> Status: checking

## Spec Pointers

- `spec.md`

## Reference Pointers

- `TaskFlowDocs/achieved/2026-09-16-capability-selection-enforcement/prd.md`
- `TaskFlowDocs/achieved/2026-09-15-phase-concept-mapping/prd.md`
- `TaskFlowDocs/achieved/2026-09-10-unblock-capability-invocation/prd.md`

## Related Tasks

- Todo `TF-20260923-230f49` (this task)

## Skills / Tools Used

- `agent-skills:idea-refine` — purpose: requirements framing on this authoring host after user locked A/A/A+B (demonstration invoke, not a product allowlist); outcome: succeeded; incorporated: HMW = auditable capability use at approve; Not Doing = no vendor mandate, no SessionStart inventory in v1, no history rewrite.
- `agent-skills:spec` — purpose: structured spec on this host (demonstration invoke); outcome: succeeded; incorporated: approve-time contract, large/small rules, generic output-kind mapping, POSIX constraints in spec.md.
- `agent-skills:plan` — purpose: ordered steps on this host (demonstration invoke); outcome: succeeded; incorporated: Step 1 hook gate → Step 2 Skill mapping → Step 3 smoke prove with per-step rollback.
- Note: these three are whatever this machine had for the three concept classes. Other machines may invoke different Skills/MCP/Agents; A7 only requires ≥1 non-Unaided line on this task, not these names.

## Preconditions

- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded (CONTRIBUTING branch/PR rules; no personal rules).
- [x] Concept-class candidates inspected against **host inventory at authoring time** (not a fixed list): requirements elicitation / architecture / work breakdown — three different invokes on this host; other hosts may differ.
- [ ] For PR creation/update: template path and mapping recorded at PR time.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-24 00:01 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Approve-time validation in `hooks/task`

- Goal: Reject empty / unqualified Skills records before Approval is written; accept invoke lines or qualified Unaided.
- Dependencies: approval
- Files: `hooks/task`
- Implementation checklist:
  - [x] Detect large ( `spec.md` present ) vs small
  - [x] Fail on missing/empty `## Skills / Tools Used`
  - [x] Pass on non-Unaided invoke bullets
  - [x] Pass on Unaided line containing `considered:`; large requires ≥1 phase-table concept-class phrase (not a product name)
  - [x] Invoke acceptance is shape-only — must pass with a placeholder capability id in smoke
  - [x] Fail closed otherwise; no partial Approval write
- Acceptance: PRD A1–A4 behavior at function level
- Verification: focused shell cases in smoke (Step 3) + manual approve on fixture plan
- Rollback: `git checkout -- hooks/task`
- Status: done

### Step 2 — Skill + artifacts: large/small rule and foreign output mapping

- Goal: Agents know the gate and how to fold external skill output into TaskFlow files.
- Dependencies: Step 1 contract stable
- Files: `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`
- Implementation checklist:
  - [x] SKILL: large = one real invoke of **any** host capability or qualified Unaided; approve enforces it
  - [x] SKILL/artifacts: generic fold — requirements→prd, design→spec, breakdown→plan Steps by output kind; forbid second fact root; no vendor allowlist
  - [x] artifacts: point at Unaided shape (already present) + approve checklist line
  - [x] No product names in concept table (table unchanged)
- Acceptance: PRD A5
- Verification: grep for gate sentence + mapping; concept table still product-free
- Rollback: `git checkout --` the two skill files
- Status: done

### Step 3 — Smoke-test prove + full suite

- Goal: Mutation-prove A1–A4; keep existing pins green.
- Dependencies: Steps 1–2
- Files: `hooks/smoke-test`
- Implementation checklist:
  - [x] Fixture large plan: empty → approve fails, Approval still pending
  - [x] Add invoke line → approve succeeds
  - [x] Unaided without considered → fail; with considered classes → pass
  - [x] Small + qualified Unaided → pass
  - [x] Existing capability-record heading assertions still pass
  - [x] `bash hooks/smoke-test` green; kill stray processes; re-run once if needed
- Acceptance: PRD A6; A7 = this plan has ≥1 invoke line (currently three host examples; names not required)
- Verification: `bash hooks/smoke-test`; `python3 …/quick_validate.py skills/taskflow`; `git diff --check`
- Rollback: `git checkout -- hooks/smoke-test`
- Status: done

## Checkpoints

- After Step 1: gate logic existable without docs (manual fixture).
- After Step 2: wording and code agree.
- Before `checking`: all checkboxes + full smoke green.

## Verification / Review

- Scope: `hooks/task`, `hooks/smoke-test`, `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, task docs + todo — matches In Scope; no vendor skill/plugin files changed.
- PRD A1: empty Skills → approve fails, Approval stays `requested` — pass (focused fixture + smoke).
- PRD A2: placeholder invoke `some:requirements-skill` (shape-only, no allowlist) → approve OK — pass.
- PRD A3: large Unaided without `considered:` → fail; with `considered: requirements elicitation, work breakdown` → pass; `considered: vibes` (no concept class) → fail — pass.
- PRD A4: small + qualified Unaided / invoke — pass via small fixture path.
- PRD A5: SKILL + artifacts state gate + generic output-kind mapping; no product names in those gate sentences — pass.
- PRD A6: `bash hooks/smoke-test` → ALL SMOKE PASSED (exit 0, twice); `quick_validate.py skills/taskflow` → Skill is valid!; `git diff --check` clean.
- PRD A7: this plan has three `purpose:` invoke lines (host demos; names not required).
- Strategy effectiveness proof (user requirement): mutation-style gate cases in smoke + focused rejects above demonstrate empty/invalid blocked, valid accepted — **effective**.
- Conflicts: none.
- Debug leftovers: none.

## Change Log

- 2026-09-23 — v1 planning: worktree `feature/capability-invoke-gate`, promoted `TF-20260923-230f49`, A/A/A+B recorded; three host capabilities invoked for PRD/Spec/Plan (demo, not allowlist).
- 2026-09-23 — work revision: de-overfit contract from authoring-host skill names to capability-set-agnostic gate (user feedback); A7/knowledge mapping/R1/R5/R6/R7 updated; no Task-version bump.
- 2026-09-24 — Steps 1–3 implemented; focused gate fixtures + full smoke green; entered checking.

## Follow-ups

- Optional later: SessionStart/route injection of concept-class candidates (original Q3-B full form).
- Optional later: quality lint beyond shape (e.g. minimum purpose length).

## Version History

- v1 — planning.
