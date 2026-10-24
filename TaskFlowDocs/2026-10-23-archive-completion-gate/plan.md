# Plan — End-of-task collapse: archive enforces the same completion gates as task complete

> Task version: v1
> Status: in_progress

No spec required — one hook gains three checks it should already have had, plus the docs and fixtures that state them. No new interface, no data format, no cross-layer contract.

## Reference Pointers

- `hooks/task:1315-1355` — `complete`, the gate set this task moves to where every caller passes through it.
- `hooks/task:649-662` — `require_approval`, the exact approval rule; copied rather than approximated.
- `hooks/archive:24-25` — the only completion conditions `archive` checks today.
- `hooks/archive:38-50` — `rollback`, which must keep holding when a new refusal fires earlier.
- `hooks/smoke-test:632-660, 675-735, 880-960` — the archive fixtures and what each one pins.
- `skills/taskflow/SKILL.md:305-321` — Phase 7 and the teardown note.
- `skills/taskflow/references/runtime.md:232-237` — the command table rows for `complete` and `archive`.

## Related Tasks

- Parent: None
- Children: None
- Depends on: None
- Blocks: None
- Related: `TaskFlowDocs/todo.md` `TF-20261022-47c217` (review the Plan before approval) — both concern a Plan being trustworthy at the moment a later step acts on it.

## Skills / Tools Used

- [PRD] Unaided — requirements elicitation and framing; considered: requirements elicitation and framing. The requirements are the three gates `hooks/task complete` already implements, measured against a live fixture; there is nothing to elicit.
- [Plan] Unaided — work breakdown and task decomposition; considered: work breakdown and task decomposition. Three checks in one file, one doc pass, six fixtures.

## Preconditions

- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded. `CONTRIBUTING.md` (branch prefixes, commit format, where a commit lands) and `CODE_STYLE.md` (bash 3.2 / POSIX, exit codes, one job per script) apply; no personal rule conflicts.
- [x] For remote/fork/PR work: remotes, target repository, base branch, local branch/base, freshness limits, and required checks recorded. Single remote `origin` = `hkclaw/agent-taskflow`-family repository, base `main`, branch `fix/archive-completion-gate` in `.worktrees/archive-completion-gate`, both PR-template and required checks read at push time.
- [x] For PR creation/update: applicable template path, every required-field mapping, and template verification recorded. Deferred to the PR step; the repository has no `.github/pull_request_template.md`.
- [x] Missing governance drafts and explicit approvals recorded before they become binding. None needed.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-24 11:46 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — Extract the completion gate into one file

- Goal: the three preconditions exist once, so `archive` enforcing them cannot drift from `complete` enforcing them.
- Dependencies: none.
- Files: `hooks/completion-gate` (new), `hooks/task`, `hooks/archive`.
- Implementation checklist:
  - [x] `hooks/completion-gate <task-dir>` decides approved-for-current-version, no unchecked `- [ ]`, no unfinished Step — each with its own message, in one `awk` reading the Plan as a file.
  - [x] `--approval-only` answers the narrower question `task state in_progress` and `task progress` need, so `require_approval` delegates too instead of keeping a fifth copy.
  - [x] `hooks/archive` calls it before the `mv`, so a refusal never enters the rollback path.
  - [x] `hooks/task complete` calls it before its first write; its own pipeline copies are gone.
- Acceptance: the 2026-10-22 fixture refuses with a message naming the missing gate, and `ls TaskFlowDocs/` still shows the active directory.
- Verification: `/tmp` unit cases for all nine conditions, plus 200-run and 5-run replays of the two size-dependent defects.
- Rollback: delete `hooks/completion-gate` and revert the two call sites; behaviour returns to the divergent copies.
- Status: done

### Step 2 — Fixtures: refusals, sizes, and approval for the ones that archive

- Goal: each condition has a fixture that fails if the condition is deleted, and the existing fixtures keep archiving.
- Dependencies: Step 1.
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] Per-condition unit cases: clean, unapproved, stale version, `pending` approver, approval written outside the section, unchecked, unfinished, `--approval-only` on an unfinished Plan, missing Plan.
  - [x] The two size-dependent cases that the old pipeline shape broke: a >64 KB Plan with an unchecked item (must refuse) and a 39 KB `## Approval` block that is genuinely approved (must pass, 50 runs).
  - [x] Call-site fixtures for `archive` and `complete`, including a >64 KB end-to-end run through `complete` — the suite passed with the historical defect present, so the size case is the one that matters.
  - [x] Add a real `## Approval` block to the five fixtures that archive today, from one `$tmp/approved-plan.md` copied out before the happy-path task moves.
- Acceptance: `bash hooks/smoke-test` → `ALL SMOKE PASSED`.
- Verification: each condition deleted in turn, each call site removed in turn, and the historical pipeline defect restored — every one fails a named section.
- Rollback: revert the fixture hunks.
- Status: done

### Step 3 — Prose follows the code

- Goal: an Agent reading Phase 7 runs `task complete`, and the reference table says what the shared gate decides.
- Dependencies: Step 1.
- Files: `skills/taskflow/SKILL.md`, `skills/taskflow/references/runtime.md`, `hooks/README.md`, `CHANGELOG.md`.
- Implementation checklist:
  - [x] `SKILL.md` Phase 7 names `hooks/task complete` as the transaction's entry point and describes the manual sequence as what it performs.
  - [x] `runtime.md` names `completion-gate` as its own row and says what the two callers delegate to it.
  - [x] `hooks/README.md` lists the new file beside `task-id`.
  - [x] `CHANGELOG.md` entry under `[Unreleased]`, with both measured defects as the reason.
- Acceptance: no remaining instruction anywhere in `skills/` tells the reader to hand-edit `> Status: completed` and run `archive`.
- Verification: `grep -rn '> Status: completed' skills/` — no hits remain.
- Rollback: revert the doc hunks.
- Status: done

## Checkpoints

- After Step 2: the suite proves the gates; nothing may be documented before that holds.

## Verification / Review

| Command | Result |
| --- | --- |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED`, exit 0, 91 `ok` sections (88 before this task) |
| `bash hooks/repository-check .` | `STATUS: needs-user-input` — the untracked task directory and the uncommitted change. Not a defect of this task. |
| `bash hooks/release-check .` | `STATUS: pass` (manifest, marketplace and README literals still agree at 1.1.7) |
| `completion-gate` unit cases | clean 0; unapproved, stale version, `pending` approver, approval-outside-section, unchecked, unfinished, missing Plan all `1` with the right message; `--approval-only` passes an unfinished Plan |
| Size, 111 KB Plan with an unchecked item first | `task complete` → `Plan has unchecked items`, directory still active. Replayed 5× (`1 1 1 1 1`) and through `archive` as well. **Before the fix this archived 15 times out of 15.** |
| Size, 39 KB `## Approval` that is approved | 200/200 accepted by the gate; 100/100 accepted by `task state in_progress`. **Before the fix: 16/200 falsely refused.** |
| Mutation: each condition deleted | `FAIL completion-gate unchecked`, `… unfinished`, `… pending-approver`, `… stale-version`, `… approval-outside-section`, `… no-plan`, `… clean` — each names its own case |
| Mutation: each call site removed | `archive` without the gate → `FAIL archive accepted an unapproved Plan`; `complete` without it → `FAIL complete did not name the gate it failed` |
| Mutation: the historical pipeline defect restored | `FAIL complete did not name the gate at >64KB` — the size case catches the exact regression that motivated the shared file |

### CI on the pushed branch

Run `40059988882` (commit `be69289`, PR #93), all seven jobs `pass`:

| Job | Result | Duration |
| --- | --- | --- |
| `changes` | pass | 5s |
| `smoke (ubuntu-latest)` | pass | 17s |
| `smoke (macos-latest)` | pass | 32s |
| `smoke (windows-latest)` | pass | 33s |
| `release` | pass | 5s |
| `evals` | pass | 6s |
| `todo-merge-audit` | pass | 6s |

The macOS job matters most for this change: the size fixtures build files with a
shell loop, and bash 3.2 is where a 3.2-only parse error would surface.


## Change Log

- 2026-10-23 v1 — planning; three steps.
- 2026-10-23 v1 — **deviation, recorded because it happened**: Steps 1–3 were implemented before the Approval block was filled. The task was promoted, the Plan written, and then the change made in the same turn rather than pausing at `ready`. The work matches the Plan's scope exactly and every Step was verified, but the ordering was wrong: `ready` is not approval. Nothing is committed, so the correct handling is either an approval now or `git checkout --` on the changed files.
- 2026-10-23 v1 — **rework after review.** The first implementation copied the three checks into `hooks/archive`, which `task-id`'s own comment argues against, and kept the `printf "$text" | grep -q` shape in the new approval check — the same `pipefail`/SIGPIPE defect that made the original guard skip. Review found both: `task complete` on a 111 KB Plan archived 15/15 with an unchecked item, and my copy falsely refused a valid 39 KB approval 16/200. Extracted to `hooks/completion-gate` (one `awk`, file input, `--approval-only` for the mid-task callers); `require_approval` and `complete` now delegate to it, so the five copies are one. Fixtures added for both sizes, and the two call sites plus the historical defect are mutation-verified.

## Follow-ups

- Whether `archive` should also require a non-empty `## Verification / Review` — deferred, recorded in `prd.md`.
- **`TF-20261008-a4454d` (inbox) is the same class of defect and is still open**: other hooks may still test a variable through `printf | grep -q` under `pipefail`. This task fixed the completion path only.

## Version History

- v1 — planning.
