# Spec — Repository document placement
> Task version: v1

## Objective and Success Criteria

Replace the mixed index/symlink model with one rule: repository-owned documents live at conventional source paths; the catalog only indexes those paths. Preserve `personal/` solely for scoped personal development rules and work habits.

## Architecture Boundaries and Responsibilities

- Repository root or platform-standard directories own repository documents.
- `TaskFlowDocs/repository-docs/index.md` owns derived navigation metadata only.
- `TaskFlowDocs/repository-docs/personal/` owns optional personal supplements only.
- Task directories continue to own task-specific PRD, Spec, Plan, and verification facts.

## Project Structure / Affected Files

- Update both copies of `SKILL.md` with the normative placement and legacy handling rules.
- Update both copies of `references/artifacts.md` with the compact catalog contract.
- Update both READMEs with equivalent user-facing explanations.
- Do not change hooks because they neither create nor link repository documents.

## Interfaces, Data Flow, and Contracts

1. Discover conventional repository documents whether or not Git is initialized.
2. Index each source by class, repository-relative path, existence, and last-checked date.
3. For an absent needed document, obtain explicit authorization, reuse an established conventional filename when present, or use the agreed default name/location.
4. For a legacy copy or link inside `repository-docs`, report it and await explicit migration/deletion authorization.
5. Load applicable source documents by indexed path; never treat the index as authoritative content.

## Invariants and Compatibility

- Repository rules prevail over personal supplements.
- Personal supplements cannot redefine repository-owned policy.
- No compatibility path retains symlink or access-mode behavior.
- Existing legacy material is not deleted or moved automatically.
- Root and packaged duplicate files must remain byte-identical.

## Validation and Error Semantics

- Missing documents are informational unless a task requires them.
- Unauthorized creation, migration, or deletion stops before filesystem mutation.
- A conflict between personal and repository rules stops work and requires user resolution.

## Code and Test Constraints

- Documentation-only change; no new dependency or migration script.
- Run focused text assertions for obsolete and required wording.
- Compare hashes for duplicated Skill/reference files.
- Run the existing hook smoke test to ensure unrelated lifecycle behavior remains intact.

## Design Decisions and Alternatives

- Chosen: path-only index and conventional source locations.
- Rejected: relative symbolic links; they duplicate navigation mechanisms and add platform/Git behavior.
- Rejected: copying content; it creates competing sources of truth.
- Rejected: automated legacy migration; deletion/moves require explicit authorization and are unnecessary for enforcing future behavior.

## Open Questions

None.
