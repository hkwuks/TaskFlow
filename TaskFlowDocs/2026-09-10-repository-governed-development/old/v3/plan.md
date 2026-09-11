# Plan — Repository-governed fork development

- Task version: v3
- State: checking
- Branch: `feature/repository-governed-development`

## Spec pointers

- `prd.md`
- `spec.md`

## Applicable repository documents

- `README.md`: public behavior and repository structure.
- `README.zh-CN.md`: Chinese public behavior must remain aligned.
- `skills/taskflow/SKILL.md`: authoritative workflow contract.
- `TaskFlowDocs/repository-docs/index.md`: catalog; currently reports contributing, code style, release, roadmap, and code of conduct as missing.
- `TaskFlowDocs/repository-docs/personal/README.md`: personal supplements cannot replace or conflict with repository governance.

## Skills / tools used

- `taskflow`: selected the independent task, Todo-first intake, required artifacts, version, state, and approval gate.
- `git-workflow-and-versioning`: created a short-lived feature branch from `main` and scoped commit/PR discipline.
- `plugin-creator`: confirmed plugin manifest and validation boundaries; no personal Agent configuration will be changed.
- `context-mode`: inspected repository documents, active tasks, manifests, Git metadata, and relevant rules with bounded output.
- `spec-driven-development`: converted the confirmed decisions into testable requirements and explicit boundaries.
- `planning-and-task-breakdown`: ordered focused implementation and verification steps.

## Preconditions

- [x] Todo intake recorded before task promotion.
- [x] Existing active task checked and kept separate.
- [x] Repository catalog and applicable current documents inspected.
- [x] Fork baseline inspected without remote mutation.
- [x] User decisions recorded for scope, remote safety, missing-document policy, evidence, and approval.
  - [x] User approves v1 PRD / Spec / Plan.

## Approval

- Approved by: user
- Approved at: 2026-09-11 10:40 +08:00
- Approved version: v2
- Approved scope: PRD / Spec / Plan

## Steps

### Step 0 — Refresh after upstream update

- Goal: Preserve the approved task while incorporating upstream `1.0.2`.
- Dependencies: User approval of v2.
- Files likely touched: task artifacts only.
- Implementation checklist:
  - [x] Refresh configured TaskFlow marketplace and reinstall plugin.
  - [x] Fast-forward from `origin/main` to `660679a` / `v1.0.2`.
  - [x] Preserve and report stash/untracked recovery boundaries.
- Acceptance: Work continues from the latest upstream baseline without data loss.
- Verification: `codex plugin list`, `git log`, `git status`, and retained stash inspection.
- Rollback: Revert task-only notes; do not rewrite upstream history.
- Status: done

### Step 1 — Centralize governance and fork rules

- Goal: Make the TaskFlow Skill deterministically govern discovery, precedence, missing documents, fork topology, and approvals.
- Dependencies: v1 approval.
- Files likely touched: `skills/taskflow/SKILL.md`.
- Implementation checklist:
  - [x] Add the dependency-ordered governance discovery and source-precedence flow.
  - [x] Add evidence-first creation rules for missing `CONTRIBUTING.md` and `CODE_STYLE.md`.
  - [x] Keep `ROADMAP.md` direction-gated and other documents task-dependent.
  - [x] Add separate governance-document approval and catalog-refresh gates.
  - [x] Add remote/fork/base discovery without assuming names or mutating Git state.
  - [x] Define Plan recording and failure/conflict behavior.
- Acceptance: Every PRD requirement has one authoritative operational rule without duplicate competing workflows.
- Verification: `rg -n -i 'fork|upstream|CONTRIBUTING|CODE_STYLE|ROADMAP|personal supplement|approval|remote' skills/taskflow/SKILL.md` and focused diff review.
- Rollback: Revert the Skill-only patch before Step 2.
- Status: done

### Step 1b — Add repository-check command

- Goal: Provide an opt-in, read-only machine check for governance and fork readiness.
- Dependencies: Step 1.
- Files likely touched: `hooks/repository-check`, `hooks/smoke-test`.
- Implementation checklist:
  - [x] Implement local document and Git metadata checks.
  - [x] Redact credentials in displayed URLs.
  - [x] Return `pass`, `needs-user-input`, or `blocked` with actionable output.
  - [x] Keep the command off automatic hooks.
  - [x] Add focused smoke coverage.
- Acceptance: Command is deterministic, read-only, and useful before planning/PR work.
- Verification: `bash hooks/repository-check <fixture>` and `bash hooks/smoke-test`.
- Rollback: Remove only the new command and its smoke assertions.
- Status: done

### Step 2 — Align artifact guidance and durable checks

- Goal: Ensure generated task artifacts can concisely record the new decisions and existing smoke tests guard stable contracts.
- Dependencies: Step 1.
- Files likely touched: `skills/taskflow/references/artifacts.md`, `hooks/smoke-test` only when necessary.
- Implementation checklist:
  - [x] Reuse existing Plan sections where sufficient; add only missing governance/fork fields.
  - [x] Add focused smoke assertions only for stable, machine-checkable wording or structure.
  - [x] Avoid a new template, runtime component, or dependency.
- Acceptance: A future task can record sources, topology, gaps, draft approval, and checks without inventing a second fact source.
- Verification: `bash hooks/smoke-test` and focused diff review.
- Rollback: Revert Step 2 files without disturbing the central Skill rule.
- Status: done

### Checkpoint — Operational contract

- [ ] Skill and artifact guidance agree.
- [ ] No remote mutation or provider-specific behavior was introduced.
- [ ] No personal supplement is allowed to replace repository governance.
- [ ] Smoke tests pass.

### Step 3 — Align bilingual public guidance

- Goal: Explain the resulting behavior to users in both supported READMEs.
- Dependencies: Steps 1–2.
- Files likely touched: `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [x] Summarize repository precedence and missing baseline governance.
  - [x] Explain direction-gated roadmap and task-dependent documents.
  - [x] Explain fork/remote discovery and non-mutation boundaries.
  - [x] Explain explicit approval before governance becomes binding.
- Acceptance: English and Chinese readers receive the same operational promise without copying the entire Skill.
- Verification: focused side-by-side review and keyword search.
- Rollback: Revert README changes without changing the operational Skill.
- Status: done

### Step 4 — Verify, review, and prepare the branch

- Goal: Prove acceptance, minimize the diff, and leave a reviewable branch.
- Dependencies: Steps 1–3.
- Files likely touched: `TaskFlowDocs/2026-09-10-repository-governed-development/plan.md`; implementation files only for review fixes.
- Implementation checklist:
  - [x] Run plugin/Skill validation available in the repository environment.
  - [x] Run `bash hooks/smoke-test`.
  - [x] Run `git diff --check`.
  - [x] Map every PRD acceptance criterion to evidence.
  - [x] Review for contradictory, duplicated, fabricated, or compatibility rules.
  - [x] Confirm no unrelated active task or user file changed.
  - [x] Record results and remaining follow-ups.
- Acceptance: All criteria and checks pass; the diff is scoped and ready for user review.
- Verification: validation commands above plus `git status --short` and focused `git diff` review.
- Rollback: Revert only review-fix edits; retain task records until disposition is decided.
- Status: done

## Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Governance gate blocks trivial work | Medium | Apply mandatory baseline creation only to non-trivial development. |
| Agent fabricates repository policy | High | Evidence-first derivation, unresolved-decision questions, explicit approval. |
| Wrong remote or base inferred | High | Treat remote names as non-authoritative and stop on ambiguity. |
| Rules become duplicated across files | Medium | Keep operational detail in the Skill and concise summaries elsewhere. |
| Existing checking task is disturbed | Medium | Do not edit its documents or reuse its deliverable. |

## Verification / review

- `bash hooks/smoke-test` — passed all lifecycle, dispatcher, and packaged Skill checks.
- `python3 .../skill-creator/scripts/quick_validate.py skills/taskflow` — Skill is valid.
- `git diff --check` — passed.
- `python3 .../plugin-creator/scripts/validate_plugin.py .` — failed on pre-existing upstream `.codex-plugin/plugin.json` `hooks` field; not changed because removing it would break declared Codex hook integration and is outside this task.
- `codex plugin marketplace upgrade taskflow && codex plugin add taskflow@taskflow` — installed `1.0.2+codex.20260911` successfully.
- `git pull --rebase origin main` — fast-forwarded branch base to `660679a` / `v1.0.2`; current work restored without losing the retained stash.
- Review result: no correctness, security, duplication, or scope findings in the governance/fork documentation changes.
- v2 command review: fixed Git worktree detection to accept both `.git` directories and worktree indirection files.
- `bash -n hooks/repository-check` — passed.
- `bash hooks/repository-check .` — returned `STATUS: needs-user-input`, exit `2`, identifying missing baseline governance and ambiguous tracking base.
- Hook registration audit — no `repository-check` registration in `hooks/hooks.json`, `hooks/hooks-codex.json`, or `hooks/session-start`.

## Change log

- 2026-09-10: Created v1 from six user-approved decisions; task remains ready pending approval of PRD / Spec / Plan.
- 2026-09-11: User approved v1; refreshed plugin to `1.0.2+codex.20260911`, fast-forwarded from `origin/main`, implemented Steps 1–4, and entered checking.
- 2026-09-11: User approved v2; archived v1, incorporated upstream `1.0.2`, and added the opt-in command scope; automatic hook integration deferred.
- 2026-09-11: User approved v3; added repository governance documents and PR template, refreshed the catalog, and kept automatic hook integration deferred.

### Step 1c — Add repository governance documents

- Goal: Establish approved repository-level contribution, style, roadmap, and PR rules.
- Dependencies: Step 1b; user-approved v3 direction.
- Files likely touched: `CONTRIBUTING.md`, `CODE_STYLE.md`, `ROADMAP.md`, `.github/pull_request_template.md`, `TaskFlowDocs/repository-docs/index.md`.
- Implementation checklist:
  - [x] Derive commands and conventions from existing scripts, history, and docs.
  - [x] Create concise actionable `CONTRIBUTING.md` and `CODE_STYLE.md`.
  - [x] Create direction-approved `ROADMAP.md` without dates or invented commitments.
  - [x] Create a PR template covering TaskFlow traceability and checks.
  - [x] Refresh the repository document catalog.
- Acceptance: The repository has usable governance documents at conventional locations and no personal supplement is used as a substitute.
- Verification: inspect all four files, run smoke tests, and run `git diff --check`.
- Rollback: Revert only the v3 governance-document commit.
- Status: done

## Verification / review

- `bash hooks/smoke-test` — passed.
- `python3 /home/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/taskflow` — passed.
- `git diff --check` — passed.
- Governance files and PR template are non-empty, evidence-based, and cataloged.
- No automatic hook registration was added.

## Follow-ups

- Whether this repository itself should adopt new `CONTRIBUTING.md`, `CODE_STYLE.md`, and `ROADMAP.md` is intentionally separate from defining plugin behavior.

## Version history

- v1 — Initial approved-decision plan; implementation not yet approved.
