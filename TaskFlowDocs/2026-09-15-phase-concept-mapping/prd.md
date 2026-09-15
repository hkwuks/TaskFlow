# Map TaskFlow phases to the concept class each phase corresponds to
> Task version: v1
> Status: planning

## Goal

Make phase-appropriate capabilities discoverable at the moment a phase runs: a TaskFlow phase (`prd.md`, `spec.md`, `plan.md`, verification, review) names the class of external workflow concept it is equivalent to, so the Agent recognizes that an installed capability covering that concept should be invoked instead of producing the artifact unaided.

## Background / Confirmed Facts

- `skills/taskflow/SKILL.md:117` tells the Agent to "inspect the capabilities currently available … and freely determine whether any can materially improve the current task, artifact, or decision". It names no mapping from a TaskFlow phase to any capability class.
- Phases 1–6 (`SKILL.md:138-230`) describe only the artifact each one produces. They never say what that artifact is called elsewhere, so an Agent reading "PRD" has no reason to connect it to an installed capability whose own vocabulary is "requirements interview", "spec-driven development", or "task breakdown".
- `skills/taskflow/references/artifacts.md:104` covers only accounting ("list a capability only after an actual invocation attempt"); there is no selection aid before the attempt.
- The consequence observed on 2026-09-14: this repository's own `prd.md`, `spec.md`, and `plan.md` for several tasks were produced with no optional capability invoked, even though installed plugins cover exactly those concepts. The Plan `Skills / Tools Used` sections stayed empty, which is the documented signal of an unaided phase — the recording rule was never the problem.
- TaskFlow deliberately does not select tools or require any provider (`SKILL.md:117`), so the fix must add concept correspondence without naming a specific tool, vendor, or chain.
- TaskFlow's phase names are its own; parity with an external tool is not the goal. The goal is that an Agent which already holds a capability covering "requirements elicitation" recognizes that TaskFlow's "Define — PRD" phase is where it belongs.

## Requirements

- R1. A single concept table maps every TaskFlow phase (Define, Research, Design, Plan, Build, Verify, Complete) to the class of concept its output corresponds to in common engineering workflows, described by what the artifact *is*, not by a tool name.
- R2. The table names the capability class to consider for each phase and states the observable signal that the phase is running unaided, so an Agent can tell whether it skipped one.
- R3. The table is normative for selection but not for outcome: it states that the class is what to look for, while the Agent still decides whether an available capability fits and remains free to proceed unaided.
- R4. No requirement, no named tool, provider, plugin, or chain appears in the table; the correspondence must survive any capability set changing.
- R5. The table lives where a phase actually reads it: `skills/taskflow/SKILL.md` in the capability section, with `skills/taskflow/references/artifacts.md` keeping only its existing accounting rule and not restating the table.
- R6. The existing behaviour is unchanged: TaskFlow still requires no particular capability, an unavailable capability still falls back to the base flow, and `Skills / Tools Used` accounting still records only real invocations.
- R7. `README.md` and `README.zh-CN.md` reflect that phases correspond to capability classes, in one sentence each, so the two READMEs stay aligned per `CODE_STYLE.md`.

## Acceptance Criteria

- A1. `skills/taskflow/SKILL.md` contains one table whose rows are the TaskFlow phases and whose columns name the corresponding concept class and the class to consider.
- A2. Every phase listed in `## Phase routing` appears in the table, and the table's phase names match those headings.
- A3. The table names no specific tool, plugin, provider, or chain (`grep` for the installed plugin names returns nothing inside the table).
- A4. The section still states that TaskFlow requires no particular capability, that an unavailable one falls back to the base flow, and that only actual invocations are recorded.
- A5. `skills/taskflow/references/artifacts.md` states the accounting rule without duplicating the table.
- A6. `README.md` and `README.zh-CN.md` each state that phases map to capability classes.
- A7. `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow` passes, `bash hooks/smoke-test` passes, and `git diff --check` is clean.

## In Scope

- `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md` (accounting rule only), `README.md`, `README.zh-CN.md`, `hooks/smoke-test` (contract assertions), and the Todo entry for this task.

## Out of Scope

- Naming specific tools, vendors, plugins, or chains, or bundling one.
- Changing any phase's artifact set, the lifecycle states, or the approval gate.
- Auto-invoking a capability, or making a capability mandatory for any phase.
- Changing `implementation` behaviour: this is documentation plus its contract test.

## Risks / Deferred Items

- A concept table can age as external vocabulary shifts; it is deliberately written by artifact semantics rather than by tool names so it stays valid.
- An Agent may still judge that no available capability helps, which is allowed. Deferred: measuring whether phases actually invoke capabilities is a separate observability question.
- The table adds lines to a Skill that is loaded on every task; kept compact for that reason.

## Open Questions

None — the concept-only scope was decided by the user on 2026-09-15.

## Version History

- v1 — planning.
