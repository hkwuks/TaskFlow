## Summary

Codex CLI had no pre-write gate. `hooks/hooks-codex.json` wired only `SessionStart`
and `UserPromptSubmit`, so on that host a TaskFlow run had no gate, no evidence
capture, and one reminder line per prompt — the flow was guidance there, not a
lifecycle. `skills/taskflow/references/runtime.md` recorded this as a limitation of
the host. It was not: Codex's own hooks documentation documents `PreToolUse` firing
on `apply_patch`, `hookSpecificOutput.permissionDecision: "deny"`, and
`additionalContext`. The distinction between **not wired** and **not supported** was
the defect, and `CONTRIBUTING.md` now states it as a rule.

This PR wires the gate, teaches it the input shape Codex sends, and closes two
holes in the existing gates that the same audit turned up.

## TaskFlow traceability

- Task: `TaskFlowDocs/2026-10-29-midturn-presence/`
- Scope:
  - `hooks/hooks-codex.json` — new `PreToolUse` on `apply_patch` → `capability-gate`.
  - `hooks/capability-gate` — reads a patch as well as a path; refuses a write whose
    recorded approval names a different Task version.
  - `hooks/approval-check` (new) — the one implementation of the approval decision,
    shared by `completion-gate` and `capability-gate`.
  - `hooks/completion-gate` — refuses a Step carrying two `- Status:` lines.
  - `hooks/smoke-test` — replaces the assertion that *forbade* wiring Codex with one
    that runs the wiring, plus the fixtures for each new condition.
  - `hooks/README.md`, `skills/taskflow/references/runtime.md`, `CHANGELOG.md`,
    `CONTRIBUTING.md` — the host-coverage rule, the Codex column and section, the
    inventory entries, the changelog.
  - `TaskFlowDocs/todo.md` — the promoted entry's status.
  - Also adds `TaskFlowDocs/todo.md` entry `TF-20261030-15b439`, an unrelated
    user request recorded during this task. It is a Todo entry only — no code.
- Base branch: `main`
- Target repository: `https://github.com/hkwuks/TaskFlow` — read with
  `git remote get-url origin`; one remote, no fork, no credentials in this body.

## Verification

- [x] `Hooks` workflow — CI is the authority per `CONTRIBUTING.md`; this branch is
  pushed and the run is read there rather than reproduced locally
- [x] `git diff --check` — clean
- [x] Relevant Skill/plugin validation — `quick_validate.py skills/taskflow`:
  `Skill is valid!`
- [x] Results recorded in the TaskFlow Plan — `## Verification / Review`, Steps 1–6

Measured locally before the push, and recorded in the Plan:

- `bash hooks/smoke-test` — `ALL SMOKE PASSED`.
- `hooks/completion-gate` gives the same verdict **and the same message** on all 93
  archived Plans before and after the approval decision moved out: 19 refused, 74
  passed, 0 disagreements. The refusal text every caller matches on is unchanged.
- `hooks/capability-gate`'s `file_path` path was compared against its previous self
  over 11 event shapes and matched byte for byte — the Codex work is additive.
- Every new condition was mutated and restored byte-identically (`diff -q`), each
  reddening its own named assertion. Two mutations found real gaps rather than
  confirming the code: the `move` fixture passed with the `Move to:` arm deleted,
  because the `Update File:` line named the gated document too — a
  `move-destination-only` case was added; and a review pass after the suite was
  already green found **four ways the patch gate allowed writes it exists to
  refuse**, listed below.
- Four fail-open defects, found by driving real events rather than reading the code:
  (1) `set -- $patch_paths` expanded unquoted, so a path containing a space split
  into two paths that were each judged and each allowed; (2) a CRLF patch — routine
  on Windows, the host this wiring is for — left a trailing `\r` on every path, so
  the basename matched no stage and the gate returned 0; (3) releases were written
  as each path was judged, so a refused two-path patch still spent an evidence line
  behind a write the host never applied; (4) `consumed` was recomputed per path, so
  two releases in one patch both claimed sequence 1. (3) and (4) are one defect —
  deciding and writing were interleaved — and are fixed by queuing releases and
  writing them once, after every path has been judged. Each has a fixture, and each
  fixture was verified to redden when its fix is reverted. **This is the reason the
  Codex path needs a real-machine run before its column says `measured`**: none of
  these shapes was in the original fixtures, and a real host may carry more.

## Review boundaries

- [x] No secrets or opaque remote payloads included
- [x] No unrelated task or user files changed — the Todo entry above is the one
  addition outside the task, and it is a record, not a change to any behaviour
- [x] Remote/base assumptions stated

## Known limitations and follow-ups

- **The Codex wiring is documented, not measured.** No real Codex has run it. The
  `runtime.md` column says `documented, not yet measured` and stays that way until a
  session on a real machine confirms the deny reaches the agent — including one
  `*** Move to:` case, since the destination's spelling is the part the docs leave
  least clear. Recorded as A14 in the Plan.
- **`PostToolUse` is deliberately not wired.** `capability-evidence`'s predicate is a
  capability class (`Skill`, `Agent|Task`, `mcp__*`) and `apply_patch` is an edit
  tool; wired, the hook would run, exit 0, and record nothing while `runtime.md`
  claimed evidence capture. Measured: feeding it that event changed no evidence line.
- **A proposed rule was measured, rejected, and removed from scope.** A per-Step
  evidence requirement (`done` requires a `## Verification / Review` line naming that
  Step) was implemented far enough to test: it was satisfied by three throwaway `ok`
  lines on a Plan where nothing was done, and it refused 73 of 93 archived Plans —
  including 7 of the 24 that really did use `hooks/task progress`. It measures
  whether verification was *documented per Step*, not whether it happened, so it was
  dropped. The evidence is in the task's `reject-a16.md` and
  `evidence-a16-fake-plan.md`, and A16 in the PRD records the reversal.
- **dsh remains ungated** — `not wired`, not `not supported`: its file tools register
  as lowercase `write`/`edit`, which no matcher arm matches. Left for its own task.
