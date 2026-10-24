# End-of-task collapse: archive enforces the same completion gates as task complete

> Task version: v1
> Status: completed

## Goal

A task cannot reach `TaskFlowDocs/achieved/` unless it was approved for its current version and its Plan is actually finished. Today two commands write the same end-of-task record and only one of them checks anything.

## Background / Confirmed Facts

Measured 2026-10-22 on an isolated fixture (one task directory, one Todo entry):

```text
> Status: completed  (hand-edited into prd.md and plan.md)
## Approval          (empty — every field deleted)
### Step 1 …         - Status: pending    - [ ] not done
### Step 2 …         - Status: in_progress
$ bash hooks/archive <task>
archive OK: … -> achieved, Todo done
EXIT=0
```

`hooks/task complete` refuses all three before it writes anything:

- `hooks/task:1323` `require_approval` — `## Approval` must say `- Status: approved`, `- Approved version:` must equal the current `> Task version:`, and `- Approved by:` must not be `pending`;
- `hooks/task:1324` — no unchecked `- [ ]` anywhere in the Plan;
- `hooks/task:1325` — no `- Status: pending|in_progress|blocked` line, i.e. no unfinished Step.

`hooks/archive` checks only `> Status: completed` in `prd.md` and `plan.md` (`hooks/archive:24-25`) plus the Todo link. The guards are therefore only as strong as the Agent's choice of entry point, and the path that skips them is two hand-edited `> Status:` lines followed by one command.

`hooks/task:1329-1331` states the intent that makes this a defect rather than a design choice:

```sh
# Every archive precondition that does not depend on the docs already being
# `completed` runs before the first write. archive re-checks them; failing
# here means no docstatus mutation to roll back.
```

`archive` does not re-check them. The comment describes a contract nobody implemented.

**And `complete`'s own checks did not reliably run.** `hooks/task:1324-1325` read the Plan into `$plan_text` and tested it through `printf '%s\n' "$plan_text" | grep -q …` under `set -o pipefail`. `grep -q` exits on the first match, `printf` takes SIGPIPE and dies with 141, and `pipefail` reports the whole pipeline as failed — so an early match on a Plan larger than the pipe buffer *skips* the check. Measured on the pre-existing code: a 111 KB Plan with an unchecked item first in the file was archived 15 times out of 15, and the same shape falsely refused a genuinely approved 39 KB `## Approval` block 16 times out of 200. The guard is therefore not merely missing from `archive`; the one place it existed silently stopped working past a size nobody had reached yet.

`skills/taskflow/SKILL.md` matches the hole: Phase 7 (`:305-309`) writes the manual sequence — "mark the task `completed`, move the entire directory, update the linked Todo item … then verify" — as *the* procedure, and `task complete` appears only in the preferred-command list at `:60` and the teardown note at `:321`. An Agent following Phase 7 literally reproduces the fixture.

**One rule, asked in one place.** Four commands need this answer: `archive` and `complete` need all three conditions, `task state in_progress` and `task progress` need the approval half. `hooks/task-id` establishes the pattern the repository already follows — one file, called by each entry point, because two copies of a rule are two chances to disagree and the one that disagreed would be the one that lets bad work through. The completion gate had grown five partial copies across two scripts.

## Requirements

1. One file, `hooks/completion-gate <task-dir>`, decides whether a Plan is approved for its current Task version, free of unchecked checklist items, and free of Steps still `pending`, `in_progress`, or `blocked`. `--approval-only` answers just the approval question.
2. `hooks/archive` runs it before moving anything; a refusal leaves the active directory in place, the Todo untouched, and the achieved path absent.
3. `hooks/task complete`, `task state in_progress` and `task progress` reach the same rule through it rather than restating it.
4. No check reads the Plan through a pipeline of a shell variable: a `printf | grep -q` test under `pipefail` is disabled by its own early match on a Plan larger than the pipe buffer, at any size the repository has not yet reached.
5. Phase 7 of `SKILL.md` names `hooks/task complete` as the archive transaction's entry point and describes the manual sequence as what that command performs, not as the procedure to run by hand. `runtime.md` and `hooks/README.md` name the shared file.
6. Every condition, every call site, and both defects the change is about are covered by `hooks/smoke-test`, so a later edit that drops one fails the suite.

## Acceptance Criteria

- On the fixture above, `hooks/archive` exits nonzero and names the missing condition; the active directory still exists and the achieved path does not.
- Each condition — unapproved, stale version, `pending` approver, unchecked item, unfinished Step, approval written outside the section, missing Plan — fails independently, so one cannot mask another.
- An approved, fully finished Plan still archives, and `hooks/task complete` still succeeds on it.
- A Plan larger than the pipe buffer with an unchecked item first in the file is refused by both entry points, and a genuinely approved 39 KB `## Approval` block is never falsely refused.
- `bash hooks/smoke-test` passes.
- `bash hooks/repository-check .` and `bash hooks/release-check .` report `STATUS: pass`.

## In Scope

- A new `hooks/completion-gate` holding the one rule.
- `hooks/archive`, `hooks/task` (`require_approval`, `complete`): call sites only.
- `hooks/smoke-test`: per-condition fixtures, call-site fixtures, and the two size fixtures; plus an `## Approval` block in the fixtures that only ever exercised the Todo rewrite.
- `skills/taskflow/SKILL.md` Phase 7, `skills/taskflow/references/runtime.md`, `hooks/README.md`, `CHANGELOG.md`.

## Out of Scope

- The other inbox items about end-of-task behaviour; this task changes one rule and its call sites.
- The same `pipefail` defect in other hooks that test a variable through a pipe. `TF-20261008-a4454d` is the inbox item for hook/document reconciliation and this task records the shape there instead of re-scoping itself.
- Rewriting anything under `TaskFlowDocs/achieved/`. Seventeen of 82 archived Plans fail the rule — two carry an unchecked item, two a `pending` Step, and fifteen fail the approval rule (thirteen have no `- Status: approved` at all; two have one that is stale or carries a `pending` approver). They predate it and are read-only history, so the rule applies from now on and never retroactively.

## Risks / Deferred Items

- **Every smoke fixture that archives is currently unapproved.** Five write a two-line Plan and archive it (`tear`, `tear-base`, `r4`, `idf`, `pr`). They gain a real `## Approval` block. This is the cost of the rule and is in scope.
- **The suite passed with both defects present**, which is why the size fixtures matter more than the condition ones: a condition fixture proves a check exists, and only a size fixture proves it runs. Both are kept for that reason.
- **The manual sequence survives in prose** as a description of what `complete` does. A later edit could turn it back into an instruction; the smoke fixtures catch the command's behaviour, not the prose.
- **Deferred:** the gate could also require a non-empty `## Verification / Review`. Not done here — that is a different claim (verification was recorded) from the three the Goal names, and no measurement exists for what a recorded verification looks like.

## Open Questions

None blocking.
