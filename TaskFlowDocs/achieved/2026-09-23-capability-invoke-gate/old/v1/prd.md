# Gate PRD/Spec/Plan on real capability invocation: large tasks need one real invo
> Task version: v1
> Status: checking

## Goal

Make professional capability use on PRD/Spec/Plan an auditable, gated choice: large tasks need one real invoke (or a qualified Unaided line with considered concept classes); `task approve` validates the `Skills / Tools Used` record; TaskFlow maps foreign skill outputs into `prd.md`/`spec.md`/`plan.md`; concept-class candidates are visible at document time.

## Background / Confirmed Facts

- Three prior tasks added layers without a call-quality gate: concept-class table (`2026-09-15-phase-concept-mapping`), required section + Unaided shape + smoke heading pins (`2026-09-16-capability-selection-enforcement`), selection≠invocation accounting (`2026-09-10-unblock-capability-invocation`).
- Smoke today pins headings/templates only; it does not require a non-empty plan section, a `considered:` list, or any invoke attempt on large tasks.
- Measured on 59 achieved plans (2026-09-23): empty/missing 34, Unaided-like 14, invoked-ish 11. Of tasks with `spec.md`: missing 12, unaided 1, invoked-ish 4 — large tasks are the worst offenders.
- Foreign skills conflict with TaskFlow paths/gates: `planning-and-task-breakdown` defaults to `tasks/plan.md`; `spec-driven-development` has its own SPECIFY→PLAN chain; TaskFlow forbids a second fact root and owns approve.
- The host capability set is environment-specific and must not enter the contract. Any installed Skills, tools, MCP servers, Agents, subagents, or search/codegraph utilities count if actually invoked; the gate never names a required product.
- User decisions 2026-09-23 (A/A/A + B): Q1-A large tasks require a real invoke attempt or qualified Unaided; Q2-A thin TaskFlow output mapping (generic: foreign skill outputs fold into prd/spec/plan); Q3-A primary gate at `task approve`, Q3-B secondary candidate injection at document time.
- Demonstration only (not product requirement): on this authoring host, three agent-skills were invoked for PRD/Spec/Plan framing so this plan itself satisfies the large-task rule.

## Requirements

- R1. Large task (Plan has `spec.md` / promote size `large`): `## Skills / Tools Used` before approve must contain **at least one** non-Unaided capability line for **any** actually invoked host capability (Skill, tool, MCP, Agent, …) **or** a single `Unaided — … considered: …` line that names ≥1 concept class drawn from the product-neutral phase table (e.g. requirements elicitation, architecture and design specification, work breakdown) and a one-sentence reason no available capability fit. No product name is required or preferred.
- R2. Small task: section must be non-empty; either invoke lines or qualified Unaided (same considered shape); empty section fails approve.
- R3. `hooks/task approve` enforces R1/R2 against the current plan version before writing Approval fields; failure exits non-zero with a clear message (no partial approval write).
- R4. Qualifying Unaided line matches `artifacts.md` shape: `Unaided — no capability applied to this phase; considered: <concept classes …>` (free-form suffix allowed after the classes).
- R5. Invoke lines remain real-invocation-only (existing rule): any capability id the host used, purpose/outcome/incorporated or equivalent; discovery does not count. Validation matches shape and non-Unaided form only — never an allowlist of skill names.
- R6. TaskFlow documents a **generic** fold rule for any foreign planning/spec/requirements capability: requirements material → `prd.md`, design material → `spec.md`, breakdown → `plan.md` Steps; never root `SPEC.md` / `tasks/plan.md` as fact sources; foreign gates defer to TaskFlow approve. Mapping keys on output kind, not vendor.
- R7. At PRD/Spec/Plan drafting time, the Agent inspects **whatever capabilities the current host exposes** for the active phase’s concept class, then either invokes one or lists the considered classes in the eventual Unaided line. Secondary aid only; R3 is the hard gate. No fixed candidate list ships in TaskFlow.
- R8. Smoke-test covers: approve rejects empty section; approve rejects large+empty-or-unqualified; approve accepts large+one invoke line; approve accepts small+qualified Unaided; existing heading pins stay.

## Acceptance Criteria

- A1. `hooks/task approve` on a large-task plan with empty Skills section fails and leaves Approval `pending`.
- A2. Same plan with one invoke line (`- \`skill\` — purpose: …; outcome: …`) succeeds.
- A3. Same plan with only `Unaided — … considered: requirements elicitation, work breakdown …` succeeds for large; Unaided without `considered:` fails.
- A4. Small task with non-empty qualified Unaided succeeds; empty still fails.
- A5. `skills/taskflow/SKILL.md` + `references/artifacts.md` state the large/small rule, approve gate, and generic foreign-output mapping (R1, R6); greps inside those rules find no mandatory product/skill allowlist.
- A6. `bash hooks/smoke-test` passes including new approve-gate cases; `quick_validate.py skills/taskflow` passes; `git diff --check` clean.
- A7. This task’s own plan records ≥1 real invoke line (large-task self-demo). The three agent-skills lines currently present are authoring-host examples only and are **not** the acceptance pattern for other machines.

## In Scope

- `hooks/task` (approve validation only)
- `hooks/smoke-test`
- `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`
- Optional light touch: document-time candidate mention in Preconditions template wording (R7) inside the same two Skill files — **not** a new SessionStart hook unless approve alone proves insufficient after A6
- Task docs + todo lifecycle for this task

## Out of Scope

- Forking or rewriting any third-party skill/plugin in its install cache
- Forcing or allowlisting a specific vendor skill, MCP, or Agent on every task
- Hook inference of model intent (still forbidden)
- Making SessionStart inject a full capability inventory (deferred; R7 is document-time only)
- Retroactive rewrite of historical achieved plans
- Release path (no TaskFlow docs)

## Risks / Deferred Items

- Approve gate can be satisfied by a token invoke line; mitigation: smoke uses a realistic line shape; deeper quality review stays human.
- R7 without a hook may still be under-applied between sessions; full candidate injection deferred.
- Agent-skills path defaults remain wrong in the plugin; only TaskFlow-side mapping text ships here.

## Open Questions

None — Q1/Q2/Q3 closed 2026-09-23 by user.

## Version History

- v1 — planning.
