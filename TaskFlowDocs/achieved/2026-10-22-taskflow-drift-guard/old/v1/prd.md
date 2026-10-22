# PRD — Keep a mid-implementation request inside the workflow

> Task version: v1
> Status: in_progress

## Goal

A task that has an approved Plan and is being implemented keeps being *governed* while
it is implemented. Today the workflow is described once, when the session starts, and
then nothing speaks again until the next compaction — so the moment a user says "there
is a bug here, fix it", the agent has no reason to see that instruction as task work.
It absorbs the fix into whatever Step it was on and the Plan stops describing what is
actually being built.

The user's report, restated as the case this must fix: **plan finished and approved,
implementation begins, a bug is found in the code, the user asks for it to be fixed
because it affects this task's result — and the TaskFlow flow is abandoned.** It is
worst once the session is long.

## Background / Confirmed Facts

Measured on 1.1.7 (`1897ffc`), in this task's worktree:

1. **The rule exists and is correct.** `SKILL.md:105-110` classifies a user change into
   exactly two buckets: a work revision (default — update the affected documents, one
   change-log line, keep the version) and a Task-version material change (archive the
   version, bump every core document atomically, return to `ready`, re-approve).

2. **Phase 5 restates both buckets**, at `SKILL.md:280`. So the rule the agent needs is
   present in the phase it is in when this happens. This is not a missing-rule problem.

3. **The trigger is described only in the vocabulary of a requirement change.**
   `SKILL.md:103`: "a user message that **corrects, rejects, adds to, or materially
   changes an approved task fact**". A bug found during implementation does not arrive
   in that shape — it arrives as *new work from the user*, which reads as "part of the
   task, keep going". The classification is never entered, because nothing in the
   wording forces the reading.

4. **The case never appears as an example anywhere in the Skill.** `grep -i` for
   `bug`/`defect`/`discovered` over `SKILL.md` returns two unrelated hits:
   `:12` (a bug fix is TaskFlow-eligible work) and `:297` (debug code in the review
   checklist). No example anywhere says what to do with a bug found mid-implementation.

5. **Nothing speaks between the session start and the next compaction.**
   `hooks/hooks.json` wires `SessionStart`, `PreToolUse`, `PostToolUse` only. `grep -n
   '"Stop"\|UserPromptSubmit' hooks/*.json` matches nothing. `runtime.md:216` states
   the same in prose.

6. **Compaction already re-injects the summary.** `hooks/hooks.json:6` matches
   `startup|resume|clear|compact|fork`, so the state summary comes back after a
   compact. The uncovered window is the one between compactions, and for a long
   implementation that window is the whole task.

7. **The derivation the reminder needs already exists.** `summarize-state:203-205`
   prints `- <id> | <version> | <status> — <title> | approval: <a> | next: <Step>`.
   Nothing new has to be derived; a reminder only has to select and frame it.

8. **`UserPromptSubmit` can inject context without blocking.** Claude Code's hooks
   reference (fetched 2026-10-22): it fires "when a prompt is submitted, before Claude
   processes it" and "also fires on turns Claude Code starts on its own"; on exit 0,
   `hookSpecificOutput.additionalContext` "is added as context alongside the submitted
   prompt", and plain stdout is added too. `decision: "block"` is optional and this
   task does not use it. A hook that reaches its timeout is cancelled and its output,
   including the `additionalContext`, is discarded — the prompt itself still reaches
   Claude, so a slow hook degrades to no reminder rather than to a broken prompt.

9. **The injection point is the exact moment of the drift.** The user's instruction is
   what starts it ("用户要求开始修"). `UserPromptSubmit` runs before the agent decides
   what that instruction means; `Stop` runs after it has already decided.

## Requirements

R1. The User-change trigger and Phase 5 name the mid-implementation case explicitly: a
    request that arrives while a task is `in_progress`, including "fix this bug", is a
    change event, and the one question that decides the bucket is stated.

R2. Between the session start and the next compaction, a session implementing a task is
    told, on each turn, which task it is in and that an instruction other than the
    current Step must be classified before it is acted on.

R3. The reminder is derived from the task's actual state, never from fixed prose: it
    names the task, its version, its phase, its approval, and the next Step by using the
    existing derivation rather than restating it.

R4. The reminder is confined to the window where drift happens. It says nothing when
    there is no active task, when the task is not `in_progress` or `checking`, and when
    the working directory is not the task's working tree.

R5. The reminder never writes, never approves, never blocks, and never fails the turn it
    observes. Every error path exits 0, the way `capability-evidence` does.

R6. No new runtime dependency: POSIX shell, `awk`, `sed`, at the bash 3.2 + BSD floor.

R7. A host is wired only where the event's contract is established, and `runtime.md`
    says which hosts those are and why the others are not.

## Acceptance Criteria

A1. `SKILL.md` names the mid-implementation case in the User-change trigger and in
    Phase 5, and gives the deciding question. Pinned by smoke with `grep -q -F`,
    in the style of the existing clause pins.

A2. Fixture: a worktree holding an `in_progress` task produces a `UserPromptSubmit`
    event whose `additionalContext` names that task, its version, its phase, its
    approval state, and its next Step.

A3. The same fixture produces nothing when the task is `planning` or `ready`, nothing
    when the worktree holds no task, and nothing when the event's `cwd` is elsewhere.

A4. The hook exits 0 and emits nothing on unusable input: empty stdin, truncated JSON,
    a non-`UserPromptSubmit` event, and a `cwd` that does not exist.

A5. The existing suite stays green on the three-platform matrix, and the hook passes
    `bash -n` under bash 3.2 and runs under the curated no-interpreter `PATH`.

A6. `runtime.md`'s event map carries a `UserPromptSubmit` row, and its "what is wired"
    paragraph agrees with `hooks/hooks.json`.

## In Scope

- `skills/taskflow/SKILL.md` — the User-change trigger and Phase 5 (R1).
- `hooks/prompt-reminder` (new) and its wiring in `hooks/hooks.json` (R2–R5).
- `skills/taskflow/references/runtime.md` and `hooks/README.md` — the wiring record (R7).
- `hooks/smoke-test` — one section per behaviour above.

## Out of Scope

- **An `Stop` hook.** It fires after the agent has already decided what the instruction
  means, which is the wrong side of the moment described in fact 9. Adding it would also
  need turn-scoped file tracking to say anything useful. Dropped, not deferred.
- **A once-per-session marker.** The reminder writes nothing at all, so it needs no
  store. Removing the write is what removes the whole test surface a marker would need.
- **Wiring `UserPromptSubmit` on CodeBuddy, Trae, dsh or Codex.** Fact 8 establishes the
  contract for Claude Code only; `runtime.md:54` already takes the line that a silent
  no-op is worse than an absent hook.
- **Any hook that edits `plan.md`, records a change-log line, or bumps a version.** The
  classification is a judgement about approved facts; hooks never decide
  (`SKILL.md:325`).
- **`TF-20261022-fda8d8`** — `hooks/archive` is looser than `task complete`. A separate
  defect with its own inbox item; this task does not touch it.
- **`TF-20261009-8abbd6`** — the gate's false refusal. Unrelated mechanism.

## Risks / Deferred Items

- **A reminder on every turn becomes wallpaper and gets ignored** — the same outcome as
  no reminder. Two things bound it: the phase gate (R4) means it only appears while a
  task is actually being implemented, and the content is three lines that state a fact
  the agent cannot otherwise recover mid-session. If it still reads as noise, the honest
  next step is to drop it rather than to add more.
- **A per-turn `git` call.** `summarize-state` runs `git branch --show-current` and
  reads one `plan.md`; the cost is milliseconds and it is the same work `SessionStart`
  already does. The host's timeout discards output rather than blocking the prompt
  (fact 8), so a slow disk degrades to a missing reminder.
- **`summarize-state`'s selection can go ambiguous.** Two active tasks in one worktree
  print "Multiple active tasks" instead of a line; the reminder then says nothing, which
  is the safe direction. One task, one worktree is already the repository's rule.
- **Deferred:** whether a request that is a *new* task rather than task work should also
  be flagged. The two-bucket classification covers recording it; deciding that it needs
  separate intake is the agent's call and not decidable from the document.

## Open Questions

None blocking.
