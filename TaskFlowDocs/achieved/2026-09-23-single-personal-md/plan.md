# Plan — Map the personal rule to a single personal.md: one file, each rule in its own se
> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md`

## Reference Pointers

- Prior boundary task: `TaskFlowDocs/achieved/2026-09-14-personal-docs-git-boundary/prd.md`

## Related Tasks

- Todo `TF-20260919-495145` (this task)
- Unrelated: `TF-20260919-6b4e21` (todo.md growth) — out of scope

## Skills / Tools Used

- Unaided — PRD/Spec/Plan drafted from codebase inspection and the user’s A/A/A answers; no requirements/design capability invoked beyond `taskflow:taskflow` (lifecycle only).

## Preconditions

- Worktree: `.worktrees/2026-09-23-single-personal-md`
- Branch: `feature/single-personal-md`
- Base: `main` @ `fd58de9`
- User decisions 2026-09-23: Q1-A / Q2-A / Q3-A

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-23 23:12 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Hook scan + index Personal rules render

- Goal: Catalog only `personal.md`; standing Personal rules prose always names it with origin and purpose.
- Dependencies: approval
- Files: `hooks/repository-docs-context`
- Implementation checklist:
  - [x] Replace sibling `*.md` personal scan with `personal.md` existence check → one `personal-rule` entry
  - [x] Always render `## Personal rules` prose: path `personal.md`, local-only, never committed, cannot override repository documents; mark not present when absent
  - [x] Keep personal route line and “not in authoritative sources” behavior
- Acceptance: A1, A3, A4 (hook behavior)
- Verification: temp-root run — present: one personal-rule row + route line only for `personal.md`, standing prose + `Status: present`; absent: no row, no personal route line, standing prose + `Status: not present`; stray `stray.md` not routed
- Rollback: `git checkout -- hooks/repository-docs-context` on the task branch
- Status: done

### Step 2 — Skill, references, README wording

- Goal: Creation/read path is “section in `personal.md`”, boundary unchanged.
- Dependencies: Step 1 contract stable
- Files: `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, `README.md`, `README.zh-CN.md`
- Implementation checklist:
  - [x] SKILL personal-rule creation → append section to `personal.md` with five (+optional) fields
  - [x] artifacts.md location sentences → `index.md` plus optional `personal.md`
  - [x] Both READMEs: single-file location; keep never-committed / subordinate
  - [x] No residual guidance to add a new sibling rule file as the normal path
- Acceptance: A6
- Verification: residual grep (`repository-docs/*.md` / “file directly in”) → none; `personal.md` present in all four files; `never committed` kept in SKILL + artifacts; `python3 …/quick_validate.py skills/taskflow` → Skill is valid!
- Rollback: `git checkout --` those four paths
- Status: done

### Step 3 — Smoke-test + full verification

- Goal: Executable pin of the contract; full suite green.
- Dependencies: Steps 1–2
- Files: `hooks/smoke-test`
- Implementation checklist:
  - [x] Fixture uses `personal.md` for positive catalog/route assertions
  - [x] Stray sibling `*.md` → no `personal-rule` row, not on personal route line
  - [x] Assert standing Personal rules prose (names `personal.md`, never committed, cannot override)
  - [x] Idempotency / remove-file still asserted
  - [x] `bash hooks/smoke-test` passes
  - [x] Kill any stray smoke-test processes; re-run once if prior runs left zombies
- Acceptance: A1–A5, A7, A8 (`git check-ignore TaskFlowDocs/repository-docs/personal.md`)
- Verification:
  - `bash hooks/smoke-test` → `ALL SMOKE PASSED` (exit 0)
  - `git check-ignore -v TaskFlowDocs/repository-docs/personal.md` → matches `.gitignore:15`
  - `git check-ignore TaskFlowDocs/repository-docs/index.md` → not ignored; `git ls-files` tracks `index.md`
  - `git diff --check` → clean
- Rollback: `git checkout -- hooks/smoke-test`
- Status: done

## Checkpoints

- After Step 2: docs and hook agree; ready to pin in smoke-test.
- Before `checking`: all checkboxes + smoke-test green.

## Verification / Review

- 2026-09-23 Step 1: smoke-test ALL SMOKE PASSED; A1-A8 verified

- Scope: `README.md`, `README.zh-CN.md`, `TaskFlowDocs/todo.md`, `hooks/repository-docs-context`, `hooks/smoke-test`, `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, plus untracked `TaskFlowDocs/2026-09-23-single-personal-md/` — matches In Scope; no unrelated edits.
- PRD A1–A8: pass (live temp-root checks + smoke-test + greps + gitignore).
- Spec contracts: single-file catalog, standing index prose, no section parsing, POSIX-only — pass.
- Plan steps: all checkboxes done; no deviations.
- Conflicts: none (no merge/rebase).
- `bash hooks/smoke-test`: pass (2026-09-23, this branch).
- `python3 …/skill-creator/scripts/quick_validate.py skills/taskflow`: Skill is valid!
- `git diff --check`: clean.
- Debug/temp leftovers: none (`smoke.out` removed; no fixture files in `repository-docs/`).

## Change Log

- 2026-09-23 — v1 planning: isolated worktree, promoted `TF-20260919-495145`, A/A/A recorded.
- 2026-09-23 — Steps 1–3 implemented; smoke-test and focused checks green; entered `checking`.

## PR template mapping (`.github/pull_request_template.md`)

- Summary → PR body first section (goal: single personal.md contract).
- TaskFlow traceability → Task: `TaskFlowDocs/achieved/2026-09-23-single-personal-md/`; Scope: In Scope in prd.md; Base branch: `main`; Target repository: `https://github.com/hkwuks/TaskFlow` (origin, no credentials).
- Verification checkboxes → smoke-test / git diff --check / skill validate / this Plan’s Verification section (all checked in PR body where true).
- Review boundaries → no secrets; only In Scope files; remote/base stated; orphan-dir note under limitations (pre-existing).

## Follow-ups

- None required. Optional deferred: warn on stray sibling `*.md` in `repository-docs/`.

## Version History

- v1 — planning → in_progress → checking (same version; work revisions only).
