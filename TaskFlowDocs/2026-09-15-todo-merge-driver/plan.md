# Plan — Ship a Todo merge driver so parallel task branches merge cleanly
> Task version: v1
> Status: ready

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/repository-docs-context` — the existing precedent for a hook that
  performs repository-local setup, including its lock and failure handling.
- `hooks/version` — the local, temp-file + `mv`, POSIX-only idiom.

## Related Tasks

- `TaskFlowDocs/2026-09-15-no-python-hooks/` — separate task, separate worktree.
  Both edit `skills/taskflow/references/runtime.md`; merge them one at a time.

## Skills / Tools Used (Optional)

## Preconditions

- Approval of this Plan at Task version v1.

## Approval

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

## Steps

### Step 1 — Write and pin the merge driver

- Goal: A POSIX `awk` script that merges two `todo.md` revisions by entry, wired
  into `.gitattributes`, and covered by a smoke section that merges real
  branches in a throwaway repository.
- Dependencies: None.
- Files: `hooks/merge-todo` (new), `.gitattributes`, `hooks/smoke-test`.
- Implementation checklist:
  - [ ] Implement: read the common ancestor, ours, and theirs; keep the preamble;
        emit entries in ours-then-theirs-new order; take an entry from either side
        when the other lacks it; leave an entry both sides changed differently
        unresolved so `git` still reports a conflict.
  - [ ] Add the `.gitattributes` line and make the driver installable.
  - [ ] Smoke: two branches appending different entries merge with both intact;
        the interleaving case that breaks `merge=union` is covered explicitly;
        same-entry field edit still conflicts.
- Acceptance: The three smoke scenarios behave as specified.
- Verification: The smoke section itself, plus a manual `merge=union` comparison
  recorded in the Change Log.
- Rollback: Remove `hooks/merge-todo`, the `.gitattributes` line, and the smoke
  section.
- Status: pending

### Step 2 — Make Todo IDs unique across parallel branches

- Goal: Two branches cut from the same base on the same day must not allocate the
  same Todo ID, so that a merge that keeps both entries leaves no duplicate ID
  for `todo_part` to resolve ambiguously.
- Dependencies: Step 1 (it is the case that exposes the collision).
- Files: `hooks/task` (the `intake` command's ID allocation), `hooks/smoke-test`.
- Implementation checklist:
  - [ ] Derive the ID deterministically from inputs that differ between tasks —
        date plus a digest of the goal — so every branch that creates the entry
        computes the same ID, and two different goals never collide.
  - [ ] Keep the `TF-<date>-<suffix>` shape readable and grep-able; document the
        suffix's meaning where intake is documented.
  - [ ] If a deterministic scheme proves impractical, fall back to repairing
        collisions inside the merge driver (renumber the later entry and say so
        on stderr) and record why in the Change Log.
- Acceptance: Two same-day intakes with different goals get different IDs from
  independent clones of the same base; no duplicate IDs after a merge.
- Verification: Smoke assertion creating two same-base, same-day intakes and
  merging them; `todo_part` resolution checked by ID.
- Rollback: Revert the intake change; Step 1 still merges text correctly.
- Status: pending

### Step 3 — Install the driver from a hook

- Goal: A fresh clone gets the driver configured without manual setup.
- Dependencies: Step 1.
- Files: `hooks/session-start`, or a new `hooks/install-merge-driver` it calls.
- Implementation checklist:
  - [ ] Idempotent, `--local` only, silent on success, best-effort failure.
  - [ ] Do not touch anything outside the *current repository's* config.
- Acceptance: Running SessionStart twice leaves the local config unchanged; a
  repository without TaskFlowDocs is unaffected.
- Verification: Smoke assertion on the config value and on the no-op case.
- Rollback: Remove the call site.
- Status: pending

### Step 4 — Document the strategy and its limits

- Goal: An Agent or maintainer reading the Skill knows what happens when two
  branches touch Todo, and what to do about it.
- Dependencies: Step 3.
- Files: `skills/taskflow/references/runtime.md`, `skills/taskflow/SKILL.md`,
  `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [ ] State the strategy, the local-merge requirement, and the web-UI
        limitation.
  - [ ] Keep both READMEs aligned per `CODE_STYLE.md`.
- Acceptance: No document implies the web UI will merge Todo automatically.
- Verification: Read-through; `grep` for the merge driver name across docs.
- Rollback: Revert the documentation commit.
- Status: pending

## Checkpoints

- After Step 1: the mechanism is proven against real branches before it is wired
  into a hook.
- After Step 2: a merge that keeps both entries cannot leave an ambiguous ID
  behind.

## Verification / Review

- Smoke merges in a throwaway repository, so the assertion exercises real `git`
  behavior rather than a simulated one.
- `merge=union` is documented as rejected with the measured failure, so the
  choice is not re-litigated later.

## Change Log

- Measured `merge=union` interleaving two top-inserted entries and dropping the
  shared trailing `- Status` / `- Next action` lines. Rejected for that reason.

## Follow-ups

- If web-UI merging becomes a requirement, the only structural fix is one Todo
  file per entry, which is a separate, larger task.

## Version History

- v1 — planning.