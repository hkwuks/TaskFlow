# Spec — Keep a mid-implementation request inside the workflow

> Task version: v1

## Objective and Success Criteria

Make the mid-implementation instruction land inside the workflow rather than beside it,
using the two levers the PRD measured as available: the rule already exists but is
worded for a requirement change (PRD fact 3), and the only moment the workflow speaks
is the session start (PRD facts 5–6), while the host will inject context at the moment
a prompt is submitted (PRD fact 8).

Success is PRD A1–A6, each exercised by `hooks/smoke-test`.

## Architecture Boundaries and Responsibilities

| Layer | Owns | Never does |
| --- | --- | --- |
| `SKILL.md` | What the agent is told to do with an instruction that arrives mid-task | Restate the lifecycle commands; that is `runtime.md` |
| `hooks/prompt-reminder` | Saying which task is in flight, and that the instruction needs classifying | Decide the bucket, write a document, approve, block |
| `hooks/summarize-state` | The one derivation of a task's line | Gain a second caller-specific format |
| `hooks/hooks.json` | The wiring | Carry behaviour |

The hook is a *reporter*, not a gate. Every existing TaskFlow hook that decides is a
deny on a write (`capability-gate`); this one decides nothing and produces one string.
That is deliberate: the classification it asks for is a judgement about approved facts,
and a hook that guessed it would be the fourth opinion on a two-bucket rule.

## Project Structure / Affected Files

- `hooks/prompt-reminder` (new) — the `UserPromptSubmit` hook.
- `hooks/hooks.json` — wire `UserPromptSubmit`.
- `skills/taskflow/SKILL.md` — the User-change trigger (`:101-112`) and Phase 5
  (`:278-282`).
- `skills/taskflow/references/runtime.md` — event map row, the "what is wired"
  paragraph (`:216`), and the hook inventory.
- `hooks/README.md` — the file tree and the boundary list.
- `hooks/smoke-test` — one section per acceptance criterion, plus the clause pins.

## Interfaces, Data Flow, and Contracts

### D1 — The rule names the case, in two places

The User-change trigger's opening sentence (`SKILL.md:103`) currently reads as being
about a requirement. It gains the case the user reported, in the same breath:

- an instruction that arrives while a task is `in_progress` and is not the current Step
  — "fix this bug", "this is wrong", "do this instead" — **is** a change event;
- the question that decides the bucket: does it change what the task promised to
  deliver, or only how it is delivered? Not promised-vs-not: that reading is what makes
  a legitimately discovered bug look like "part of the task".
- the default when the answer is not obvious is the work revision, because it is
  reversible in one line, while a version bump returns the task to `ready` and stops
  implementation.

Phase 5 (`:280`) gains one sentence pointing back, so the phase an agent is actually in
carries the instruction rather than requiring it to recall a section from the top of the
document. This is the same relationship `:272`'s isolation reminder already has.

**Rejected: restating the two buckets in Phase 5.** Two copies of a rule that must agree
is the divergence a shared spelling would have to keep in sync by hand; Phase 5 already
points rather than restates for the isolation rule (`:272`), and the same shape holds
here. Phase 5 points; the trigger defines.

### D2 — The reminder is `UserPromptSubmit`, and it only reports

`hooks/prompt-reminder`:

- Reads the event with `hooks/json-field` (`hook_event_name`, `cwd`, `prompt` — the last
  one is received but not used; see "Rejected" below).
- Exits 0 silently unless the event is `UserPromptSubmit`.
- Resolves the repository from the event `cwd`, exactly as `capability-evidence` does
  (`:58-64`), so a stale shell `PWD` cannot point it at another repository. Outside a
  repository, or outside `TaskFlowDocs/`, it is a no-op.
- Selects the active task by running `hooks/summarize-state` with
  `TASKFLOW_REPO_ROOT=<worktree>` and reusing its `- <id> | <version> | <status> — … |
  approval: … | next: …` line verbatim. It parses nothing out of `plan.md` itself.
- Emits only when the selected line's status field is `in_progress` or `checking`, and
  the line is a single task line. `Multiple active tasks` and `no active task` both
  produce nothing.
- Prints `hookSpecificOutput.additionalContext` with `hookEventName:
  "UserPromptSubmit"`, three lines: the state line, one sentence naming both buckets,
  and one sentence saying which is the default. It writes nothing, anywhere.

Using `summarize-state` rather than re-deriving is the load-bearing choice: the selection
rules (which directories count, what "active" means, which Step is next, how approval is
read) already exist in one place and are covered by smoke. A second reader of `plan.md`
would be a second set of answers to the same question.

**Rejected: matching the prompt's wording** ("fix", "bug") to decide whether to remind.
It is a keyword classifier over free text, it is wrong in both directions (a bug report
phrased as "why does this return null?" is the same case), and it would make the
reminder's behaviour depend on English phrasing. The reminder fires on state, not on
words: while a task is in flight, *every* instruction is a candidate for classification.

**Rejected: `Stop`.** It fires after the agent has already acted on the instruction, so
it can only report a drift that already happened, and to say which file was edited it
would need turn-scoped tool tracking. `UserPromptSubmit` is on the correct side of the
decision and needs nothing tracked.

**Rejected: injecting at `SessionStart` only.** That is what exists, and the task was
abandoned with it in place. More of a signal that has already failed is not a fix.

**Rejected: a once-per-session marker.** Bounding a reminder by count makes the second
and third instructions — where drift actually accumulates over a long session — the
unreminded ones. The phase gate is the correct bound: outside `in_progress`/`checking`
there is nothing to remind about, and the reminder is three lines.

### D3 — Wiring is Claude Code only, and the docs say so

`hooks/hooks.json` gains a `UserPromptSubmit` entry with no matcher (the event has no
tool to match). `hooks-codebuddy.json`, `hooks-trae.json`, `hooks-codex.json` and
`hooks-dsh.json` are unchanged: the contract in PRD fact 8 is Claude Code's reference,
and this repository does not wire an event it has not established for that host. The
`runtime.md` row says "Claude Code" for the wired column and "not wired — contract not
established" for the others, in the form the gate's rows already use.

## Invariants and Compatibility

- **The hook writes nothing and decides nothing.** No store, no marker, no document.
- **It never fails the prompt.** Every path exits 0; the empty-output path is the
  normal path in every repository without an in-flight task.
- **It does not change `summarize-state`.** The hook consumes the existing line. If a
  later change wants a different format it adds a consumer, not a variant.
- **The phase gate is the rate limit.** No counter, no timer, no session id.
- **No new runtime dependency.** `json-field`, `awk`, `sed`, and the same curated `PATH`
  the interpreter section pins (`smoke-test:174`).
- **Bash 3.2 + BSD floor.** No `declare -A`, no `mapfile`, no process substitution.

## Validation and Error Semantics

Silence is the contract for every non-applicable case, and the tests assert it rather
than asserting an empty string: no active task, task not in flight, cwd elsewhere,
temporary directory, unparseable JSON, wrong event name. A hook that printed a diagnostic
here would put it in front of the model on every prompt, which is worse than the drift.

The one message it does print names facts, not rules: the task, the version, the phase,
the approval, the next Step, then what the two buckets are. A reader can act on it
without opening `SKILL.md`.

## Code and Test Constraints

- `hooks/smoke-test` gains one section per acceptance criterion: the injected context
  for an in-flight task (A2), the four silent cases (A3), the four unusable inputs (A4),
  and the clause pins on `SKILL.md` (A1).
- The `bash -n` loop (`smoke-test:38`) and the curated-`PATH` section pick the new file
  up automatically, because both enumerate `hooks/*`; the suite asserts rather than
  assumes that.
- Assertions on the emitted JSON read one field with `hooks/json-field` rather than
  `grep`, so an escaped newline cannot pass a substring check while the field is empty.
- Mutations, one at a time: remove the phase gate, remove the single-task guard, remove
  the event-name guard, and confirm each red-lines.

## Design Decisions and Alternatives

See D1–D3 above; each carries its rejected alternatives beside it. The one decision
worth isolating: **the reminder asks a question rather than answering it.** The two
buckets differ in cost, not in correctness — a work revision is a line in the change log,
a material change returns the task to `ready` — and the evidence needed to choose is in
the PRD, which the hook does not read. Asking is the only honest thing a non-deciding
hook can do.

## Open Questions

None blocking.
