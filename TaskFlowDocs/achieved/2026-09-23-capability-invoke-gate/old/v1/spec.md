# Spec — Gate PRD/Spec/Plan on real capability invocation
> Task version: v1

## Objective and Success Criteria

Approve-time, deterministic validation of `Skills / Tools Used` so large tasks cannot ship unaided without a considered decision, using only product-neutral shape/concept-class checks; TaskFlow documents how **any** foreign requirements/design/planning capability folds into its three artifacts. Success = PRD A1–A7.

## Architecture Boundaries and Responsibilities

| Piece | Responsibility |
| --- | --- |
| `hooks/task` `approve` | Read plan; classify large vs small; validate Skills section; write Approval only if pass |
| `skills/taskflow/SKILL.md` | Phase rules: large invoke-or-qualified; foreign output mapping |
| `references/artifacts.md` | Exact Unaided/invoke line shapes; approve checklist pointer |
| `hooks/smoke-test` | Mutation-prove accept/reject cases |
| Foreign capabilities of any vendor (unchanged) | Produce content Agent routes into prd/spec/plan by output kind |

No new MCP, no SessionStart capability scanner in v1.

## Project Structure / Affected Files

- `hooks/task` — `approve)` branch: validation before `run_awk_to` Approval write
- `hooks/smoke-test` — new `== approve gates the capability record ==` block
- `skills/taskflow/SKILL.md` — capability section + approve gate sentence
- `skills/taskflow/references/artifacts.md` — record shapes + mapping table row
- Not changed: promote scaffold heading, concept table neutrality, release flow

## Interfaces, Data Flow, and Contracts

```text
task approve <id> [approver]
  → require-shaped plan
  → read ## Skills / Tools Used body
  → size = large if plan.md contains "## Spec Pointers" with `spec.md`
       or file spec.md exists; else small   # match promote size signal
  → if body empty → FAIL
  → if body has invoke lines (non-Unaided bullets; any capability id) → PASS
       (no allowlist of skill/MCP/agent names)
  → else must be single Unaided line containing "considered:"
       → large: considered non-empty and includes ≥1 concept-class phrase
                aligned to the SKILL phase table (requirements elicitation,
                architecture and design, work breakdown, …) — table vocabulary,
                not product names
       → small: considered present is enough
  → PASS → existing approval write
```

**Size detection:** prefer presence of `spec.md` beside plan (promote `large` always writes it). Fallback: grep plan for `` - `spec.md` `` under Spec Pointers.

**Capability neutrality:** validation never greps for `agent-skills`, `idea-refine`, MCP tool names, or any other product token. Smoke fixtures may use placeholder ids like `some:requirements-skill` to prove neutrality.

**Failure:** stderr message `approve blocked: Skills / Tools Used …`; exit non-zero; Approval block unchanged.

## Invariants and Compatibility

- Existing approved plans: gate runs on future approves only; no re-validation of history.
- Heading remains `## Skills / Tools Used` (no `(Optional)`).
- Concept table still names no products.
- Unaided fill pattern string in artifacts.md stays the documented shape (smoke already pins it).

## Validation and Error Semantics

| Input | Result |
| --- | --- |
| Empty section | fail all sizes |
| Large + only Unaided without `considered:` | fail |
| Large + Unaided with considered classes | pass |
| Large + one invoke line | pass |
| Small + qualified Unaided | pass |
| Malformed plan (no section) | fail |

## Code and Test Constraints

- POSIX shell + awk only in `hooks/task`.
- No blocking I/O for logging.
- Smoke: one mutation at a time; clean fixtures; no real-repo root as fixture; `pkill` discipline if suite leaves processes.

## Design Decisions and Alternatives

| ID | Decision | Rejected |
| --- | --- | --- |
| Q1-A | Large needs invoke or qualified Unaided | always-invoke (too rigid); record-only (status quo failure) |
| Q2-A | Generic text mapping by output kind in SKILL/artifacts only | forking any vendor skills; writing TaskFlow-native PRD skills; vendor-specific fold rules |
| Q3-A | Gate at approve | promote (too early, empty plan); complete (too late) |
| Q3-B | Document-time considered note, no new hook | SessionStart inventory (deferred; R7 lightweight) |

## Design Decisions and Alternatives — alternatives detail

Token invoke risk accepted (PRD Risks). SessionStart injection deferred to keep approve the single hard gate.

## Open Questions

None.
