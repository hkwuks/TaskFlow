# Spec — Gate PRD/Spec/Plan on real capability invocation (v2 stage gate)
> Task version: v2

## Objective and Success Criteria

Per-document **pre-write** capability invocation, recorded as stage-tagged lines; approve rejects incomplete stages. Success = PRD A1–A7.

## Architecture Boundaries and Responsibilities

| Piece | Responsibility |
| --- | --- |
| Skill narrative | Invoke matching concept class **before** first drafting each of prd/spec/plan; append stage line immediately |
| `plan.md` Skills section | Source of truth: one or more lines per stage `[PRD]` / `[Spec]` / `[Plan]` |
| `hooks/task` approve | Compute required stages from `spec.md` presence; validate each stage line shape; write Approval only if all pass |
| `hooks/smoke-test` | Mutation-prove missing/bad stage fail, complete stage set pass |
| Foreign capabilities | Unchanged; Agent folds output by kind into the task files |

No filesystem watcher in v2.

## Project Structure / Affected Files

- `hooks/task` — replace/extend v1 Skills check with stage-aware validation
- `hooks/smoke-test` — stage matrix
- `skills/taskflow/SKILL.md`, `references/artifacts.md` — pre-write rule + tag shape + approve pointer
- Not changed: concept table neutrality, promote scaffold heading (body content gains tags when filled)

## Interfaces, Data Flow, and Contracts

```text
Before writing prd.md:
  inspect host capabilities for Define class → invoke OR decide Unaided
  append to plan ## Skills / Tools Used:
    - [PRD] `…` — purpose: …; outcome: …; incorporated: …
      or
    - [PRD] Unaided — …; considered: <concept class> …

Before writing spec.md (large only): same with [Spec] + Design class
Before writing plan.md body: same with [Plan] + work-breakdown class

task approve <id>:
  required = {PRD, Plan} ∪ ({Spec} if spec.md exists)
  for each stage in required:
    lines = bullets under Skills that start with [STAGE]
    if none → fail "approve blocked: missing stage [STAGE]"
    if any line lacks invoke-shape and (lacks considered: or
       (large/unaided stage lacks phase-table concept)) → fail naming stage
  else write Approval
```

**Stage tag:** line must match `^- \[PRD\] |^- \[Spec\] |^- \[Plan\] ` (ASCII brackets).

**Unaided + tag:** `- [PRD] Unaided — …; considered: …` (considered required; concept class required for large).

**Neutrality:** no product-name allowlist; smoke uses `some:tool` placeholders.

## Invariants and Compatibility

- Heading stays `## Skills / Tools Used`.
- Untagged freeform lines alone do **not** satisfy a stage (v1 shape without tag fails approve for that stage).
- Historical approved plans are not re-validated.
- Concept table still product-free.

## Validation and Error Semantics

| Case | Result |
| --- | --- |
| Large missing `[Spec]` | fail: missing stage [Spec] |
| Large all three stages invoke | pass |
| Stage Unaided no considered | fail: that stage |
| Large stage Unaided considered no concept class | fail: that stage |
| Small with PRD+Plan, no Spec file | pass |
| Small missing [PRD] | fail |
| Empty Skills | fail |

## Code and Test Constraints

- POSIX shell + awk; fail before Approval write; no blocking log I/O.
- Smoke: one mutation at a time; clean up; no real-repo fixture root; pkill discipline.

## Design Decisions and Alternatives

| ID | Decision | Rejected |
| --- | --- | --- |
| Q1-A | Stage tags in one Plan Skills section | per-file Skills sections; prose-only |
| Q2-A | Approve checks stages; Skill requires **pre-write** invoke | file-create hook (deferred); approve-only after full draft (v1, rejected by user) |
| Q3-A | Small = PRD+Plan; Large = +Spec | require Spec stage on small; status-quo single blob |

## Open Questions

None.
