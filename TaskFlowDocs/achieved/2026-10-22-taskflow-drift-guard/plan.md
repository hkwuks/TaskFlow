# Plan — Keep a mid-implementation request inside the workflow

> Task version: v2
> Status: completed

## Spec Pointers

- `spec.md` — decisions D1–D3, implemented in that order.

## Reference Pointers

- `TaskFlowDocs/todo.md` — `TF-20261022-d8db4d` (the report).
- Claude Code hooks reference, `UserPromptSubmit` section — fetched 2026-10-22; the
  quoted contract is in PRD fact 8.

## Related Tasks

- `TF-20261022-fda8d8` (inbox) — `hooks/archive` is looser than `task complete`.
  Separate defect, not touched here.
- `TF-20261009-8abbd6` (inbox) — the gate's false refusal. Unrelated mechanism.

## Skills / Tools Used

- [PRD] `mcp__exa__web_fetch_exa` — purpose: read the Claude Code hooks reference to
  establish the prompt-submit contract before designing a signal on it; outcome: the
  event fires before the prompt is processed, injects
  `hookSpecificOutput.additionalContext` on exit 0, and a timed-out hook's output is
  discarded while the prompt still arrives; incorporated as PRD fact 8.
- [Spec] `mcp__exa__web_search_exa` — purpose: establish whether the same event exists on
  CodeBuddy and Trae before widening D3; outcome: both document `UserPromptSubmit` with
  the same `hookSpecificOutput.additionalContext` field, at documented rather than
  measured standing; incorporated as the Spec D3 host table and its standing column.
- [Plan] `mcp__exa__web_search_exa` — purpose: establish the Codex CLI and dsh event
  shapes before rewriting the Step decomposition for five hosts; outcome: Codex
  documents `UserPromptSubmit` injecting `additionalContext` as developer context, and
  dsh's `agent/prompt-submit` waterfall carries `additionalContext` in a
  `PromptDecision` that its docs map onto Claude Code's event; incorporated into
  Step 1 (the per-host contract check) and Step 3 (five wiring files).

v1's capabilities (`claude-code-guide` for PRD and Spec, `agent-skills:planning-and-task-breakdown`
for Plan) are recorded with the archived v1 documents in `old/v1/` and are not claimed
here; the v2 documents were rewritten against the host references above.

## Preconditions

- Working tree is the task worktree `.worktrees/taskflow-drift-guard`, branch
  `fix/taskflow-drift-guard`.
- `main` is at `1897ffc` (1.1.7 released and pinned).

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-22 22:55 +0800
- Approved version: v2
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Confirm each host's prompt-submit contract before writing the hook

- Goal: for every host this repository ships wiring for, the event name, the input
  fields, the injection field and the timeout behaviour, checked rather than assumed —
  and the exact wording the rule needs so that a host with no hooks is not dependent on
  the reminder.
- Dependencies: none.
- Files: none — research only, recorded in `## Verification / Review`.
- Implementation checklist:
  - [x] Record, per host, the event name, whether it fires before the prompt is
        processed, the injection field, whether `cwd` is present, and the standing the
        finding rests on (measured / packaged CLI / docs).
  - [x] Confirm whether `dsh/index.js` mounts hook files by name, so a new file reaches
        the bridge without a config edit.
  - [x] Run `hooks/summarize-state` against a fixture worktree and record the exact line
        the hook will consume, including the `Multiple active tasks` case.
  - [x] List the existing smoke sections that will pick the new file up automatically
        (`bash -n` loop, curated `PATH`) and confirm both enumerate `hooks/*`.
- Acceptance: every finding carries a file:line or a documentation citation, and every
  host is labelled with the standing its wiring will rest on.
- Verification: the commands and their output go into `## Verification / Review`.
- Rollback: none — no file changes.
- Status: done

### Step 2 — D1: the rule names the mid-implementation case

- Goal: an agent reading either the User-change trigger or Phase 5 sees "fix this bug"
  as a change event, and has one question to answer — including an agent on a host with
  no hooks, for which this Step is the entire fix.
- Dependencies: Step 1.
- Files: `skills/taskflow/SKILL.md`, `hooks/smoke-test`.
- Implementation checklist:
  - [x] Extend the trigger's opening sentence (`:103`) with the in-flight instruction,
        and add the deciding question plus the default.
  - [x] Add one pointer sentence in Phase 5 (`:280`), not a second copy of the buckets.
  - [x] Read both additions back with the hook disabled in mind: no sentence may rely on
        a reminder having been injected.
  - [x] Pin both with `grep -q -F` in smoke, in the style of `smoke-test:2160-2166`.
- Acceptance: PRD A1 and R1a.
- Verification: the new pins red-line when each sentence is reverted.
- Rollback: `git checkout -- skills/taskflow/SKILL.md hooks/smoke-test`.
- Status: done

### Step 3 — D2: the per-prompt reminder

- Goal: while a task is in flight, every prompt arrives with the task's real state and
  the classification question beside it, on every host this repository wires.
- Dependencies: Step 1.
- Files: `hooks/prompt-reminder` (new), `hooks/hooks.json`, `hooks-codebuddy.json`,
  `hooks-trae.json`, `hooks-codex.json`, `hooks-dsh.json`, `hooks/smoke-test`.
- Implementation checklist:
  - [x] Read the event with `hooks/json-field`; exit 0 on an event name it does not
        serve, or on unusable input.
  - [x] Select the task by running `hooks/summarize-state` with `TASKFLOW_REPO_ROOT` set
        from the event `cwd`, falling back to the process working directory; reuse its
        line verbatim.
  - [x] Emit only for a single line whose status is `in_progress` or `checking`.
  - [x] Accept each wired host's event name in one predicate, and print the envelope
        that host reads — chosen from the plugin-root variable, the way `session-start`
        already chooses it.
  - [x] Wire all five hosts' files; write nothing; every error path exits 0.
- Acceptance: PRD A2, A3, A4.
- Verification: `bash hooks/smoke-test`; `bash -n` under `docker run --rm -i bash:3.2`;
  mutations per spec's test constraints, one at a time.
- Rollback: delete `hooks/prompt-reminder` and revert the five wiring files and the
  smoke section.
- Status: done

### Step 4 — D3: the wiring record matches what shipped

- Goal: the event map and the "what is wired" paragraph agree with every `hooks/*.json`,
  states each host's standing, and says what reaches a host with no wiring at all.
- Dependencies: Step 3.
- Files: `skills/taskflow/references/runtime.md`, `hooks/README.md`, `hooks/smoke-test`.
- Implementation checklist:
  - [x] Add the row for all five hosts; correct the `:216` paragraph.
  - [x] Add `prompt-reminder` to both inventories and to the must/may-not boundary list.
  - [x] Name the fallback for a host with no hook wiring: the rule in `SKILL.md` is the
        only signal there, and the document says so rather than implying the reminder
        is universal.
  - [x] Assert in smoke that every host named as wired carries the event in its JSON,
        and that the row count matches the wiring files.
- Acceptance: PRD A6.
- Verification: `bash hooks/smoke-test`; `bash hooks/release-check .` unaffected.
- Rollback: `git checkout -- skills/taskflow/references/runtime.md hooks/README.md`.
- Status: done

### Step 5 — Full verification and record

- Goal: the change is verified the way this repository verifies changes.
- Dependencies: Steps 2–4.
- Files: `plan.md` only.
- Implementation checklist:
  - [x] `bash hooks/smoke-test` green locally, then on the three-platform CI.
  - [x] Record the mutation table: each guard removed in turn, one at a time, with the
        observed red line.
  - [x] Run the bash 3.2 + BSD syntax check on every touched hook.
  - [x] Write the verification record into this Plan.
- Acceptance: every PRD acceptance criterion has a recorded command and result.
- Verification: as listed.
- Rollback: none — this Step writes only the Plan.
- Status: done

## Checkpoints

- After Step 1: the contract is confirmed or the design is amended **before** the hook
  is written. If `summarize-state`'s line cannot be consumed without parsing it, the
  Spec is amended first — not the code.
- After Step 3: the behaviour is delivered and green; Step 4 is documentation.
- After Step 5: everything verified and recorded.

## Verification / Review

- 2026-10-22 Step 5: CI run 39805143538: smoke ubuntu pass, windows pass, macos pending at time of writing; changes/evals/todo-merge-audit pass; release skipped by classifier

- 2026-10-22 Step 5: bash hooks/smoke-test ALL SMOKE PASSED; 3 mutations caught; bash:3.2 clean; release-check pass

### Step 1 — per-host contract

| Host | Event | Injection field | `cwd` in input | Standing |
| --- | --- | --- | --- | --- |
| Claude Code | `UserPromptSubmit` | `hookSpecificOutput.additionalContext` | yes | measured — hooks reference, 2026-10-22 |
| CodeBuddy | `UserPromptSubmit` | same | yes | docs (`codebuddy.ai/docs/cli/hooks`, v1.16.0+) + packaged-CLI reading |
| Trae | `UserPromptSubmit` | same | **no** — input is `session_id`, `hook_event_name`, `prompt` | docs only (`docs.trae.cn` hook configuration reference) |
| Codex CLI | `UserPromptSubmit` | same, added as developer context | yes | docs (`developers.openai.com/codex/hooks`) |
| dsh | `agent/pre-step` seam | same envelope | yes — bridge fills from `session.header.cwd` | measured against the installed bridge source |

dsh is the one that needed reading rather than trusting the summary: the bridge
(`@deepseek-ai/dsh-hooks-claude-code` 0.2.0-rc.2) subscribes to `agent/pre-step`
(`lib/index.js:234`) and runs the command configured under `UserPromptSubmit` with a
payload whose own `hook_event_name` is `"UserPromptSubmit"` (`lib/index.js:340-364`).
The codec (`@deepseek-ai/dsh-hook-protocol` `lib/index.js:144-154`) reads
`hookSpecificOutput.additionalContext` and **discards the block when `hookEventName`
differs from the firing event**. So dsh takes the same event name and the same envelope
as the other four — no arm of its own. Its `CLAUDE_EVENTS` list (`lib/index.js:13-21`)
carries `UserPromptSubmit` and discards a matcher on it, matching the matcher-less entry
this task writes.

`dsh/index.js` mounts `hooks-dsh.json` by fixed path, so a new file reaches the bridge
with no config edit; only the JSON needed a new event. Confirmed: nothing in
`dsh/index.js` enumerates hook scripts.

`summarize-state` output shapes the hook consumes:

```
- 2026-10-22-demo | v1 | in_progress — Demo task | approval: approved | next: Step 1 First [in_progress]
- Multiple active tasks (2); set TASKFLOW_TASK_ID to select one.
# Active tasks            (no task at all — heading only)
```

With `TASKFLOW_VERBOSE=1` the multi-task case prints one line per task instead of the
notice; both shapes are covered by the silence section.

Auto-picked-up by the suite, verified by reading the section: the `bash -n` loop
(`smoke-test:38`) and the curated-`PATH` section (`smoke-test:174`) both enumerate
`hooks/*`, so the new file is parsed and run without a new entry.

### Verification record

| Check | Command | Result |
| --- | --- | --- |
| Full suite | `bash hooks/smoke-test` | `ALL SMOKE PASSED`, rc=0 |
| bash 3.2 parse | `docker run --rm -i bash:3.2 bash -n < hooks/prompt-reminder` | clean |
| bash 3.2 parse (suite) | same, `< hooks/smoke-test` | clean |
| No interpreter | hook run with a curated `PATH` holding no python | emitted normally, rc=0 |
| Wiring JSON | all five files parsed | 5/5 valid |
| Release literals | `bash hooks/release-check .` | `STATUS: pass` |
| Skill validation | `quick_validate.py skills/taskflow` | `Skill is valid!` |
| `git diff --check` | whitespace/conflict markers | clean |
| CI, run 39805143538 (PR #92) | `gh pr checks 92` | `changes`, `evals`, `todo-merge-audit`, `smoke` ubuntu, `smoke` macOS, `smoke` windows all pass; `release` skipped by the path classifier — 6 passing, 0 failing |

Mutations, one at a time, each against the focused sections and then restored:

| Mutation | Result |
| --- | --- |
| remove the phase gate | CAUGHT — `FAIL prompt-reminder spoke on a planning task` |
| remove the single-task guard | CAUGHT — `FAIL prompt-reminder spoke on two active tasks with TASKFLOW_VERBOSE=1` |
| remove the event-name arm | CAUGHT — `FAIL prompt-reminder spoke on a SessionStart event` |

The single-task mutation was **not** caught on the first run: with the default
environment `summarize-state` prints the "Multiple active tasks" notice, which fails the
line split whether or not the count guard exists, so the guard was untested. The
`TASKFLOW_VERBOSE=1` fixture was added for that reason — a user may legitimately export
it, and in that shape the count guard is the only protection. Re-run: caught.

Also corrected while wiring: two existing smoke assertions pinned the hook-command count
for `hooks-codebuddy.json` (4) and `hooks-trae.json` (4). Both now expect 5, and both
fail loudly rather than silently under-counting.

## Change Log

- v1 — re-scoped. The PRD, Spec and Plan were first written against a different reading
  of the report (drift in this repository's own development, guarded by tightening
  `archive`/`state` and adding a `Stop` hook). The user's correction — the plugin while
  it is *used*, triggered by "a bug is found mid-implementation and the user asks to fix
  it" — makes that reading the wrong problem; the three documents were rewritten rather
  than amended. The `archive`-looseness finding it had collected is now
  `TF-20261022-fda8d8`, so it is not lost.
- v2 — wiring widened from Claude Code to all five shipped hosts, after the user asked
  whether only Claude Code was covered. The v1 draft's own justification for
  Claude-only ("the contract is established for Claude Code only") did not survive
  checking: `UserPromptSubmit` with the same `hookSpecificOutput.additionalContext`
  injection is documented by CodeBuddy, Trae and Codex CLI, and dsh's `agent/prompt-submit`
  waterfall with a `PromptDecision` is documented as mapping onto it. The material
  change is the R7 rule plus the "other agents" requirement (R1a), which states that the
  wording in `SKILL.md` — not the hook — is the whole fix for a host with no wiring at
  all. Recorded as a Task-version change rather than a work revision because it changes
  the approved compatibility decision.

## Follow-ups

- `TF-20261022-fda8d8` — `hooks/archive` accepts what `task complete` refuses. Its own
  item, its own fix.
- `TF-20261009-8abbd6` — the gate's false refusal; unchanged.
- If the per-turn reminder proves to be noise in use, the honest response is to remove
  it rather than to enlarge it. Recorded so the next session does not "fix" it by adding
  more.
- Each host's wiring carries the standing it rests on. The first real session on Trae,
  CodeBuddy, Codex or dsh either confirms it or corrects it; a silent no-op there is a
  wiring bug to fix against that host, not a reason to widen this task now.

## Version History

- v1 — planning; documents rewritten against the corrected reading.
- v2 — planning; wiring widened to every shipped host, and the no-hook fallback stated
  as a requirement rather than left implicit.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- Severity case (measured 2026-10-22 on 1.1.7): every state transition is an explicit command. runtime.md:216 states 'Only SessionStart summary injection, the sessions index, and the Claude Code pre-write gate are automatically wired; the write commands never bind to UserPromptSubmit, PostToolUse, or Stop.' capability-gate:126-131 returns exit 0 once (version, stage) is released, so after the FIRST write of prd/spec/plan nothing observes the task again; its path dispatch only matches prd.md/spec.md/plan.md one level under TaskFlowDocs, so every implementation edit is unguarded. PostToolUse runs capability-evidence only, which records invocations and checks nothing. summarize-state reports active tasks at SessionStart only. The one hard backstop is task complete, which fails on unchecked Plan items (hooks/task:1324) and unfinished Steps — but it only fires if the agent chooses to call it. So the failure is silent: the task directory still reads in_progress while nothing is enforcing it.
