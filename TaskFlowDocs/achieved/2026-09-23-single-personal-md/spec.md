# Spec — Map the personal rule to a single personal.md: one file, each rule in its own se
> Task version: v1

## Objective and Success Criteria

One personal-rule file: `TaskFlowDocs/repository-docs/personal.md`, multi-section (one rule per section, each with its own Scope). Hook, Skill, READMEs, smoke-test, and the index Personal rules section all agree on that contract. Success = PRD A1–A8.

## Architecture Boundaries and Responsibilities

| Piece | Responsibility |
| --- | --- |
| `personal.md` (disk, untracked) | Authoritative personal-rule body; sections only; never committed |
| `hooks/repository-docs-context` | Detect only `personal.md`; one `personal-rule` row; standing Personal rules prose; one personal route line |
| `index.md` | Routing metadata only; table row when file exists; Personal rules prose always |
| Skill / references / READMEs | Creation and reading guidance: append a section to `personal.md` |
| `hooks/smoke-test` | Pins A1–A5, A7 |

Hook does not read section bodies. Skill readers apply Scope when loading rules for a task.

## Project Structure / Affected Files

- `hooks/repository-docs-context` — replace `for path in "$docs"/*.md` personal scan with a `personal.md` existence check; rewrite Personal rules render.
- `hooks/smoke-test` — replace `my-card.md` fixture with `personal.md`; add stray-sibling negative assertion; assert standing prose.
- `skills/taskflow/SKILL.md` — personal-rule creation → section in `personal.md`.
- `skills/taskflow/references/artifacts.md` — same, including “directory contains `index.md` plus optional `personal.md`”.
- `README.md`, `README.zh-CN.md` — location wording.
- Not changed: `.gitignore`, route-line prefix text, five-field rule schema, precedence rules.

## Interfaces, Data Flow, and Contracts

```text
disk: repository-docs/personal.md ?
  yes → add_entry personal-rule TaskFlowDocs/repository-docs/personal.md all local-only
         + route line “Local personal rules (…): …personal.md”
  no  → no personal-rule row, no personal route line
always → index ## Personal rules names personal.md + origin + purpose
         (+ not present when file absent)
```

Catalog row shape unchanged (five columns). Personal prose is renderer-owned, not a carried-over row.

### `personal.md` section shape (Skill contract, not parsed by hook)

```markdown
## <rule title>

- Scope: …
- Repository documents checked: …
- Rules: …
- Verification: …
- Exceptions / Change control: …
```

Commit/PR rules additionally: `Commit format`, `PR checks`.

## Invariants and Compatibility

- Personal rules never enter `Read authoritative sources:`.
- Personal rules never override repository documents (prose + existing Skill rule).
- `personal.md` remains gitignored; `index.md` remains tracked.
- Carry-over of non-personal rows unchanged.
- Idempotent index render preserved.

## Validation and Error Semantics

- Absent `personal.md` is normal (not an error).
- Stray sibling `*.md`: ignored for personal catalog (no fail, no route) — Q1-A.
- Existing path validation / lock / atomic replace untouched.

## Code and Test Constraints

- POSIX shell + awk only (plugin runtime).
- Smoke-test mutations one at a time; clean up fixtures; no leftover `hooks/smoke-test` processes (memory: smoke-test run discipline).
- Do not run smoke-test with `.` as a fixture root against the real repo (memory: clobbers repo).

## Design Decisions and Alternatives

| ID | Decision | Alternative rejected |
| --- | --- | --- |
| Q1-A | Only `personal.md` is a personal rule | B dual-shape; C docs-only |
| Q2-A | Five fields per section; hook injects one path | B parse Scope in hook; C drop fields |
| Q3-A | Standing index prose always names `personal.md` | B prose only when file exists; C prose in header only |

## Open Questions

None.
