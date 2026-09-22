# Make hooks/version write the same five-field Approval block hooks/task generates

> Task version: v1
> Status: completed

## Goal

`hooks/version`’s Approval reset must emit the same five-field block
`hooks/task`’s promote template writes — so `require_approval` and the version
reset agree on shape, and a missing `- Status:` line cannot slip through.

Umbrella-free small fix. Prerequisite for `454ac4` (Approval automation);
that work stays out of scope here.

## Background / Confirmed Facts

Measured on `main` = `17556d2`, 2026-09-23, worktree
`.worktrees/fix-version-approval-shape`. Nothing inferred.

**`hooks/task` promote template (`hooks/task` ~651–657), exact:**

```
## Approval

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending
```

**`hooks/version` today (`hooks/version` 36–39, 96–114):**

1. Presence check requires all five fields already exist
   (`Status`, `Approved by`, `Approved at`, `Approved version`,
   `Approved scope`). Missing `Status` → `missing Approval field: Status`
   and exit 1 — **refuses rather than writes**.
2. Reset awk rewrites those five lines **in place** when present
   (`Status` → `requested`, the rest → `pending`). It never inserts a
   missing line and never reorders to the template order.
3. Post-check greps `- Status: requested` inside `-A8` of `## Approval`.

Reproduced: five-field plan → reset produces the template values (in the
source order). Four-field plan (no `Status`) → refuse, no mutation.

**`require_approval` (`hooks/task` 503–515)** greps
`- Status: approved`, `- Approved version: <v>`, and fails on
`- Approved by: pending`. It only works if someone wrote `- Status:` —
promote does; a plan that followed the skill’s four-field record shape does
not get a Status line from `version` either (version refuses first).

**Skill record shape (`skills/taskflow/SKILL.md` ~228–232)** documents the
*human* approval block as four fields starting at `Approved by` — no
`Status`. That is the documented write path for recording approval, not the
promote template. Divergence is real and is why Notes on `454ac4` call the
blocks disagreeing.

**Smoke (`hooks/smoke-test` ~607–619)** after `version` only asserts
`- Approved version: pending`. It does **not** assert `- Status: requested`
or the full five-line shape / order.

**Todo Notes on `b7821b` / `454ac4` (2026-09-19, v1.0.7):** claim version
“never writes Status” and left Status at the old value. Current code *does*
rewrite an existing Status line (added earlier); the residual bug is the
refuse-vs-write gap, the missing order guarantee, the skill four-field
record template, and the thin smoke assert — not a total absence of the
Status rewrite. Do not “fix” a fully broken reset that is not broken.

## Requirements

- **R1.** After a successful `hooks/version` reset, the plan’s `## Approval`
  body is **exactly** the five template lines, in order:

  ```
  - Status: requested
  - Approved by: pending
  - Approved at: pending
  - Approved version: pending
  - Approved scope: pending
  ```

  Values and order match `hooks/task` promote byte-for-byte. Blank line
  immediately under `## Approval` stays as promote writes it.

- **R2.** If any of the five lines is missing (including `Status`),
  `version` **writes the full block** instead of refusing on the presence
  check. Section header `## Approval` must still exist (missing section =
  hard fail, unchanged).

- **R3.** Presence check that currently requires all five before any mutation
  is removed or narrowed to “section exists”; it must not reject the
  missing-`Status` case R2 handles.

- **R4.** Post-reset verify asserts the full five lines (not only
  `Status: requested` under `-A8`).

- **R5.** `skills/taskflow/SKILL.md`’s “Record approval as” block lists all
  five fields (add `- Status: approved` as the recorded value, or document
  that Status is the fifth line the human sets alongside the others — match
  what the gate actually greps). One place only; no second template.

- **R6.** Smoke: (a) version on a five-field approved plan → exact five-line
  pending/requested block; (b) version on a four-field plan (no Status) →
  succeeds and emits the same five lines; (c) existing version section still
  green.

- **R7.** `bash hooks/smoke-test` → `ALL SMOKE PASSED`.

## Acceptance Criteria

- **A.** Fixture: plan with only four Approval fields (skill shape) →
  `hooks/version … v2` exits 0; resulting Approval body equals the R1 block.
- **B.** Fixture: normal five-field approved plan → after version, same R1
  block; `old/vN/` archive still holds the superseded docs.
- **C.** `require_approval` on a plan that was version-reset then hand-set to
  the approved five-field values still passes / fails as before (no gate
  behavior change).
- **D.** Skill approval snippet shows five fields; no duplicate template.
- **E.** Suite green; `bash -n` on changed hooks.

## In Scope

- `hooks/version` (presence check, reset write, post-check).
- `hooks/smoke-test` (R6).
- `skills/taskflow/SKILL.md` approval snippet (R5).

## Out of Scope

- `hooks/task` promote template (already the source of truth).
- `hooks/task` `require_approval` logic (no behavior change).
- `454ac4` — hook-driven approval write / `task approve`.
- Timestamp format / timezone for `Approved at` (454ac4 Notes; pending
  values only here).
- Changing what the human is allowed to approve.

## Risks / Deferred Items

- Rewriting the Approval body wholesale could drop a stray comment line a
  human put inside the section. **Mitigate:** replace only the five field
  lines / insert them if absent; do not delete unrelated non-field lines
  without recording that choice in the Change Log if one appears in smoke.
- Skill snippet change is docs-only; agents that already memorized four
  fields still hit R2 (version writes Status).

## Open Questions

1. Skill record shape: **`- Status: approved` fifth line** vs “Status set
   separately” — **Recommend: five lines, Status first, value `approved`**
   for the human record (same order as promote; value differs because this
   is the approved state). Gate already greps `- Status: approved`.
2. Extra non-field lines inside `## Approval` — **Recommend: leave them**;
   only ensure the five fields exist and match values/order among field
   lines. No comment-stripping.
3. Fold skill.md into this PR — **Recommend: yes, one snippet** (R5) so the
   documented record shape cannot reintroduce the four-field hole.

## Version History

- v1 — planning.
