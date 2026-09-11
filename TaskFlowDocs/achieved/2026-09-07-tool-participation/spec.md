# Spec — Allow appropriate tools to contribute to task documents
> Task version: v1

## Objective and Success Criteria

Turn optional collaborator compatibility into an explicit, tool-agnostic collaboration decision without adding runtime behavior. At relevant planning stages, an Agent first checks available capabilities and uses those that materially help; reviewed conclusions are then routed into the existing TaskFlow artifacts.

## Architecture Boundaries and Responsibilities

| Concern | Owner |
| --- | --- |
| Selecting and invoking suitable available capabilities | Agent |
| Reviewing outputs and incorporating conclusions | Core-document owner |
| Artifact paths, document shape, state, approval, versions, archive | TaskFlow |
| Runtime interception, installation, scheduling, or tool choice | Out of scope |

## Project Structure / Affected Files

- `taskflow/SKILL.md`: phase instruction, routing/authority boundaries, and tool-use recording rule.
- `taskflow/references/artifacts.md`: concise template/routing support for actual tool use.
- `README.md` and `README.zh-CN.md`: aligned user-facing position.

## Interfaces, Data Flow, and Contracts

```text
phase work → assess available capabilities → use suitable capability (when helpful)
                                              ↓
                                      review conclusions
                                              ↓
                         route merged facts to prd.md/spec.md/plan.md/reference/
                                              ↓
                           record actual use and incorporated conclusion in plan.md
```

The output of a capability is not authoritative until reviewed and merged. TaskFlow does not supply an invocation API or mandate a named capability.

## Invariants and Compatibility

- Keep one task-directory source of truth; do not create parallel PRD, Spec, or Plan artifacts.
- Preserve the single core-document writer rule and Primary/user authority for confirmation, versioning, approval, and phase changes.
- Preserve direct handling for small obvious changes.
- Checking available capabilities does not imply that a tool must be invoked or that an unused-capability record is required.

## Validation and Error Semantics

- Inspect the resulting rule text for all required phases and absence of named-tool requirements.
- Verify template and README consistency by searching the changed wording and reviewing the diff.
- A missing optional tool is not an error; continue with normal TaskFlow work after assessment.

## Code and Test Constraints

- Documentation-only change; no runtime code or automated test required.
- Use focused text searches and Git diff as verification.

## Design Decisions and Alternatives

- Chosen: phase-level assessment requirement plus post-use traceability.
- Rejected: an enumerated approved-tool list, because available capabilities vary by environment and this project is not a tool registry.
- Rejected: automatic invocation, hooks, or a fixed workflow, because they conflict with TaskFlow’s non-invasive scope.

## Open Questions

- None blocking.
