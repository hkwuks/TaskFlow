# Spec — Unblock autonomous capability invocation
> Task version: v1

## Objective and Success Criteria

Clarify the TaskFlow lifecycle so capability discovery remains advisory, autonomous selection remains free, and a capability the Agent decides to use is actually invoked before its output is incorporated or recorded as used.

## Architecture Boundaries and Responsibilities

- TaskFlow Skill: define phase-independent selection/invocation/recording semantics without choosing tools.
- Host: expose capabilities and provide the supported invocation mechanism.
- Agent: decide relevance, perform the invocation, review the result, and incorporate only supported conclusions.
- Hook: provide bounded lifecycle context only; never infer or enforce model capability choice.

## Project Structure / Affected Files

- `SKILL.md`
- `skills/taskflow/SKILL.md`
- `references/artifacts.md` and its packaged mirror if recording language changes.
- `references/runtime.md` and its packaged mirror only if the Hook boundary needs clarification.
- Existing lightweight validation surface where practical.

## Interfaces, Data Flow, and Contracts

```text
discover available capabilities
  -> Agent freely decides whether any materially help
  -> selected capability is invoked through the current host mechanism
  -> Agent reviews success/failure and output
  -> incorporated conclusions are routed to task artifacts
  -> actual attempt/outcome is recorded when plan.md exists
```

Discovery alone has no recording side effect. No selection means the base flow continues. Failed optional invocation returns to the base flow with an honest outcome; a required capability failure becomes a normal concrete blocker.

## Invariants and Compatibility

- No fixed allowlist, provider, Skill chain, category, or numerical requirement.
- No mandatory capability selection.
- No Hook-based intent inference.
- Hosts without relevant capabilities continue the base TaskFlow workflow.
- The existing `Skills / Tools Used` section remains optional.

## Validation and Error Semantics

- “Used” means an actual invocation attempt occurred.
- Successful incorporation records purpose plus incorporated conclusion.
- Relevant failed/unavailable attempts may be recorded as failed/unavailable with no fabricated conclusion.
- Failure of an optional capability is non-blocking; correctness-critical failure follows the normal blocker contract.

## Code and Test Constraints

- Change instructions, not host configuration or third-party Skills.
- Keep root and packaged TaskFlow documents semantically identical where they are maintained mirrors.
- Prefer a focused text/structure invariant check over mocks of model behavior.

## Design Decisions and Alternatives

- Chosen: remove ambiguity at the Skill contract and record actual outcomes.
- Rejected: force a specific capability or lifecycle chain; this contradicts autonomous selection.
- Rejected: require at least one tool per phase; some tasks need none.
- Rejected: Hook enforcement; Hooks cannot observe private selection intent.

## Open Questions

None.
