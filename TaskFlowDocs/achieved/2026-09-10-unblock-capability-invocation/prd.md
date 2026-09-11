# Unblock autonomous capability invocation
> Task version: v1
> Status: completed

## Goal

Preserve the Agent's freedom to choose useful capabilities while removing TaskFlow wording or workflow obstacles that allow a selected Skill/tool to be recorded without actually being invoked.

## Background / Confirmed Facts

- TaskFlow currently tells the Agent to inspect available capabilities and invoke those that materially help.
- The user observed an Agent select an `agent-skills` Skill but not actually invoke/load it.
- A host Hook receives lifecycle events and cannot see private model reasoning; it cannot reliably infer which capability the Agent intended to select.
- `agent-skills:using-agent-skills` defines selected Skills as workflows to invoke and follow, not names to cite without loading.
- The user explicitly rejects mandatory selection or invocation of any particular tool.

## Requirements

- Keep capability choice autonomous, open-ended, and provider-neutral.
- Do not mandate a particular Skill, tool, Agent, provider, chain, category, or count.
- Remove any TaskFlow ambiguity or sequencing obstacle between selecting a capability and invoking it through the host-supported mechanism.
- Treat discovery, listing, mentioning, or planning to use a capability as distinct from successful invocation.
- Record a capability under `Skills / Tools Used` only after an actual invocation attempt; distinguish successful incorporated output from unavailable/failed invocation.
- When invocation is unavailable or fails, record the fact if relevant and continue the base TaskFlow flow unless that capability is genuinely required for correctness.
- Do not use Hook logic to guess model intent or force capability calls.

## Acceptance Criteria

- Project Skill text explicitly preserves free capability selection.
- The workflow makes a selected useful capability immediately actionable through the host mechanism, without a TaskFlow approval or documentation step blocking invocation.
- `Skills / Tools Used` cannot truthfully represent mere discovery or selection as successful use.
- A failed/unavailable optional capability does not block normal TaskFlow execution.
- A focused repository check covers the new invariants without testing model internals.

## In Scope

- Project `SKILL.md` and packaged `skills/taskflow/SKILL.md` capability-routing language.
- Artifact/runtime reference wording only where needed for consistent recording semantics.
- Minimal deterministic validation in the existing Hook smoke/check surface or a simpler existing repository check.

## Out of Scope

- User-level Agent configuration, installed plugin cache, or third-party `agent-skills` files.
- Requiring the Agent to select any capability.
- Host/model implementation changes or claims of deterministic model tool choice.
- Hook inference of private reasoning.

## Risks / Deferred Items

- Instructions can remove ambiguity but cannot guarantee a model will always make an optimal autonomous choice.
- Host-specific invocation syntax varies; TaskFlow must rely on the current host-supported mechanism rather than hard-code one provider.
- Telemetry beyond honest Plan records is deferred absent a reproduced host-level failure.

## Open Questions

None.

## Version History

- v1 — autonomous selection with unobstructed, truthful invocation contract, ready for approval.
