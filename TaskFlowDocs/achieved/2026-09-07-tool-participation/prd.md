# Allow appropriate tools to contribute to task documents
> Task version: v1
> Status: completed

## Goal

Make TaskFlow require an Agent to consider currently available capabilities while clarifying requirements, preparing PRD/Spec/Plan documents, researching, and reviewing. Preserve TaskFlow as the authority for task-document paths, formats, approvals, state, and history—not as a tool selector or orchestrator.

## Background / Confirmed Facts

- The current wording calls other Skills and tools “optional collaborators”, but provides no decision point or phase-level instruction to consider them.
- TaskFlow intentionally does not intercept prompts, tool calls, or model behavior.
- The current plan template has an optional `Skills / Tools Used` section.
- The user wants no named or restricted tool set; an Agent may use any suitable capability available in its environment.

## Requirements

1. In requirements clarification, PRD, Spec, Plan, research, and review work, an Agent first checks whether currently available tools or Skills would materially help.
2. When a suitable capability is available and useful, the Agent uses it; TaskFlow must not prescribe a tool, vendor, Skill family, or invocation mechanism.
3. TaskFlow remains the owner of final artifact locations, document structure, version/state transitions, approval, and archival rules.
4. Only reviewed and merged conclusions become task facts; raw outputs remain non-authoritative.
5. When tools or Skills are used, `plan.md` records their names, purpose, and the conclusion incorporated. No assessment record is required when none is used.
6. README guidance must match the operational rule without claiming runtime interception or automatic invocation.

## Acceptance Criteria

- `SKILL.md` gives a clear, phase-level instruction to evaluate available capabilities and use suitable ones without naming a required tool.
- The instruction covers clarification, PRD, Spec, Plan, research, and review.
- Routing, review, authority, and approval boundaries remain explicit.
- The Plan template supports concise records of actual tool use and incorporated conclusions.
- English and Chinese README wording stays consistent with the non-runtime, tool-agnostic position.

## In Scope

- Documentation and templates governing TaskFlow collaboration with external capabilities.

## Out of Scope

- Runtime hooks, automatic tool invocation, tool installation, provider integrations, or tool-specific recipes.
- Changes to TaskFlow artifact paths, lifecycle, approval, versioning, or archival behavior.

## Risks / Deferred Items

- “Materially help” is necessarily contextual; checking available capabilities does not require invoking one or leaving an empty record in every phase.
- The later wording must avoid making TaskFlow a general orchestration framework.

## Open Questions

- None blocking.

## Version History

- v1: Initial proposal.
