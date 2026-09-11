# Plan — Reduce TaskFlow workflow token cost
> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md`

## Reference Pointers

- Evidence: analysis of the 5-version achieved task and repository history (reported to the user before this task was created).

## Related Tasks

- Depends on: None
- Blocks: None
- Related: `2026-09-07-repository-docs-workspace` (rules being revised), `2026-09-07-tool-participation` (source of the tool-agnostic rule)

## Skills / Tools Used (Optional)

- `taskflow` — established artifact, approval, and versioning constraints for this task.

## Preconditions

- User approval of v1 PRD / Spec / Plan recorded below before implementation.

## Approval

- Approved by: user
- Approved at: 2026-09-08 21:34 +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Tighten version-trigger wording in SKILL.md
- Goal: wording-only and implementation-path-only changes become work revisions by default; contract changes still bump the Task version.
- Dependencies: v1 approval.
- Files: `taskflow/SKILL.md` (and mirror).
- Implementation checklist:
  - Replace the "implementation path" trigger with the tighter test (goal/requirement/acceptance/scope/contract changes bump; wording and approach clarifications are work revisions).
  - Add the revision-vs-version decision to the User-change trigger section.
- Acceptance: the trigger test is explicit and grep-checkable.
- Verification: `rg` the changed section; confirm no other doc still lists "implementation path" as a bump trigger.
- Rollback: revert only this step's edits before any version/approval change.
- Status: pending

### Step 2 — Add work-revision change log to Plan guidance
- Goal: a wording/approach revision updates `plan.md`'s change log without a new Task version.
- Dependencies: Step 1.
- Files: `taskflow/SKILL.md`, `taskflow/references/artifacts.md` (Plan outline gains a `## Change Log` section), mirrors.
- Implementation checklist:
  - Add `## Change Log` to the Plan template.
  - State that work revisions append here without incrementing the Task version.
- Acceptance: plan revision path is documented and does not require a Task-version bump.
- Verification: inspect the Plan template; cross-check SKILL.md's revision-vs-version rule.
- Rollback: revert the template/guidance edits.
- Status: pending

### Step 3 — Version bumps archive only changed documents
- Goal: `old/vN/` contains `version.md` plus changed core documents; snapshots only when the prior version is not recoverable from an existing archive.
- Dependencies: Step 1.
- Files: `taskflow/references/versioning-and-recovery.md`, `taskflow/SKILL.md` (atomic transition + archive), mirrors.
- Implementation checklist:
  - Rewrite the atomic version transition to archive only changed documents plus `version.md`.
  - Keep file-mode snapshots available when no archive baseline exists.
  - Remove the instruction to copy an unaffected Plan into `old/`.
- Acceptance: the transition no longer requires full-set copies; non-Git recovery remains possible.
- Verification: review the transition checklist; confirm recovery instructions still describe file-mode restore.
- Rollback: revert transition edits.
- Status: pending

### Step 4 — Stage retrieval before full archived reads
- Goal: check `version.md` summaries and current `plan.md` before reading full archived document sets.
- Dependencies: Step 3.
- Files: `taskflow/SKILL.md` (achieved-task retrieval), `taskflow/references/versioning-and-recovery.md`, mirrors.
- Implementation checklist:
  - Add a "staged retrieval" step to the reopen flow: read version summaries + current plan first; only read full archived sets when needed.
- Acceptance: retrieval guidance names the staged order.
- Verification: inspect the reopen/retrieval section.
- Rollback: revert the retrieval edit.
- Status: pending

### Step 5 — De-duplicate lifecycle statements and align READMEs
- Goal: archive transaction and version-trigger rules exist once (SKILL.md); README EN/zh-CN give a stable summary.
- Dependencies: Steps 1–4.
- Files: all five skill/README files and mirrors.
- Implementation checklist:
  - Remove duplicated archive-transaction/version-trigger statements from `artifacts.md` and `versioning-and-recovery.md`; replace with pointers to SKILL.md.
  - Align README EN/zh-CN wording to the revised rules without restating full procedure.
- Acceptance: grep shows each key procedure sentence once across the three skill files.
- Verification: `rg` for the transaction sentences; compare README EN/zh sections.
- Rollback: revert de-dup/README edits.
- Status: pending

## Checkpoints

- Before editing: user approval of v1 PRD / Spec / Plan.
- Before completion: all acceptance criteria pass, mirrored skill copy matches, README EN/zh agree.

## Verification / Review

### Acceptance checklist (from PRD)

- [x] Archive transaction + version trigger are single-sourced in `SKILL.md`; `artifacts.md` and `versioning-and-recovery.md` reference it. `rg "verify the active path is absent"` → 1 file; trigger table lives only in SKILL.md.
- [x] Version-trigger wording no longer treats "implementation path" as a Task-version trigger by default; wording/approach clarifications are work revisions (table in SKILL.md User-change trigger; Phase 5 Build; README EN/zh aligned).
- [x] Plan `## Change Log` documented (SKILL.md §4 + artifacts.md Plan outline); work revisions keep the Task version.
- [x] Version bump archives only changed core docs + `version.md`; full snapshots only when no recoverable baseline (versioning-and-recovery.md Atomic version transition / File mode).
- [x] Retrieval staged: version summaries + current plan read before full archives (SKILL.md §7 + versioning-and-recovery.md Safe completion and reopening).
- [x] README EN/zh describe the workflow as a stable summary and match the new classification without restating full operational procedure.
- [x] No git-only requirement introduced; file-mode `old/vN/` recovery retained (SKILL.md Safety and scope).

### Checks run

- `git diff --check` clean (only CRLF→LF notice).
- `diff -q` repo `taskflow/` vs installed skill copy → identical after mirroring all three files.
- `rg "implementation path"` across all 5 docs → no remaining version-trigger phrasing.
- Diff footprint: 5 files, +54/−31 lines.

## Follow-ups

- None. Apply the tightened version trigger to the two active-related tasks only when their own change events occur; no retroactive migration.

## Version History

- v1: Proposed four-lever workflow change (version triggers, plan revisions, archive granularity, retrieval staging); git-only archival excluded.
