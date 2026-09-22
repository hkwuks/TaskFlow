# Record Approval from a hook instead of hand-editing the five fixed fields

> Task version: v1
> Status: completed

## Goal

`hooks/task approve <task-id> [approver]` transcribes an already-given human
approval into the Plan’s `## Approval` block — Status, by, at, version,
scope — so the Agent does not hand-edit five fixed-format lines. The hook
never invents consent: it only writes what the user has already said.

Shape prerequisite (`b7821b` five-field block) landed in PR #52.

## Background / Confirmed Facts

Measured on `main` = `7f531a2`, 2026-09-23, worktree
`.worktrees/feat-task-approve`. Nothing inferred.

**Today’s approval path:** after the user approves, the Agent rewrites the
`## Approval` body by hand (smoke fixtures use `sed` on Status / by / version
only). Nothing in `hooks/task` writes those five lines except the promote
template (all `pending` / `requested`).

**`require_approval` (`hooks/task` 503–515)** needs:

1. `- Status: approved`
2. `- Approved version:` equal to plan `> Task version:`
3. `- Approved by:` not `pending`

`Approved at` / `Approved scope` are not read by the gate; they exist so the
block matches the skill template and is auditable.

**Field sources (from `454ac4` Notes + measured code):**

| Field | Source |
|---|---|
| `Status` | verb of this subcommand → `approved` |
| `Approved by` | human; CLI arg, default `user` |
| `Approved at` | now, skill form `YYYY-MM-DD HH:mm +08:00` (`date '+%Y-%m-%d %H:%M %z'` → `2026-09-23 00:39 +0800` on this host) |
| `Approved version` | plan `> Task version:` |
| `Approved scope` | which of `prd.md` / `spec.md` / `plan.md` exist → `PRD / Spec / Plan` subset, ` / `-joined |

**Boundary:** legal order is *user approves → hook records*. The command
must not be presented as self-service approval. Skill already forbids hooks
from creating approval without the user; this subcommand is the
transcription half only.

**`hooks/version` after #52** already emits the same five-line pending
block; `approve` writes the *approved* values into that same shape/order.

## Requirements

- **R1.** New subcommand: `task approve <task-id> [approver] [--root <path>]`.
  Default approver string: `user`.
- **R2.** Preconditions (fail non-zero, no write): plan exists; `## Approval`
  section exists; plan `> Task version:` present and `vN`. Core docs other
  than plan are optional for scope only.
- **R3.** On success, rewrite the five Approval field lines under
  `## Approval` to exactly:

  ```
  - Status: approved
  - Approved by: <approver>
  - Approved at: <YYYY-MM-DD HH:mm +ZZZZ>
  - Approved version: <plan Task version>
  - Approved scope: <PRD / Spec / Plan subset>
  ```

  Order matches promote. Non-field lines in the section are left alone
  (same rule as `version` reset). Missing field lines are inserted.
- **R4.** Scope = join of present cores among `PRD` (`prd.md`), `Spec`
  (`spec.md`), `Plan` (`plan.md`) in that order, ` / ` separated. Plan
  always present (R2) so scope is never empty.
- **R5.** `approve` does **not** change `> Status:` on prd/plan, does not
  call `require_approval` on itself (writing approval is not gated on
  already being approved), does not touch Todo or Git.
- **R6.** Skill: document that after the user approves, record with
  `task approve` (optional approver); hand-editing the five lines is the
  fallback only when the hook is unavailable. Keep the five-line snippet as
  the human-visible shape.
- **R7.** Smoke: (a) approve on a promoted pending plan → five lines exact,
  then `state in_progress` / a gated command succeeds via `require_approval`;
  (b) custom approver string appears; (c) missing plan version or missing
  Approval section → non-zero, plan bytes unchanged; (d) scope reflects
  prd+plan without spec vs all three.
- **R8.** `bash hooks/smoke-test` → `ALL SMOKE PASSED`.

## Acceptance Criteria

- **A.** Fixture pending five-field plan → `approve` → fields match R3;
  `require_approval` accepts the result.
- **B.** `approve <task> alice` → `- Approved by: alice`.
- **C.** Plan without `## Approval` or without `> Task version:` → exit ≠ 0,
  file unchanged (`digest` before/after).
- **D.** With only `prd.md`+`plan.md` → `- Approved scope: PRD / Plan`;
  with spec → `PRD / Spec / Plan`.
- **E.** Suite green; `bash -n` on `hooks/task`.

## In Scope

- `hooks/task` `approve` subcommand.
- `hooks/smoke-test`.
- `skills/taskflow/SKILL.md` (record-approval sentence only).

## Out of Scope

- Changing `require_approval` checks.
- Auto-approving, inferring consent, or calling approve from SessionStart.
- `Approved at` portability shims beyond `date '+%Y-%m-%d %H:%M %z'`
  (no compatibility fallback without separate permission).
- Reopening / re-approval flows; version bump still goes through
  `hooks/version`.

## Risks / Deferred Items

- Agent might call `approve` without a real user yes — process/skill
  rule, not enforceable in POSIX shell without a signed token (out of
  scope).
- `date +%z` shape varies (`+0800` vs `+08:00`); skill snippet shows
  `+08:00`. **Decision:** emit what `date` prints (`+0800`); gate does not
  parse `Approved at`. Note in Change Log if we later normalize.

## Open Questions

1. Approver argument — **Recommend: optional `[approver]`, default `user`**.
2. `Approved at` — **Recommend: `date '+%Y-%m-%d %H:%M %z'`** (skill shape,
   no fallback branch).
3. Scope order / labels — **Recommend: `PRD / Spec / Plan`, only existing
   files, fixed order**.

## Version History

- v1 — planning.
