# Plan — Ship a Todo merge driver so parallel task branches merge cleanly
> Task version: v1
> Status: completed

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

- Status: approved
- Approved by: user
- Approved at: 2026-09-15 13:14 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — Write and pin the merge driver

- Goal: A POSIX `awk` script that merges two `todo.md` revisions by entry, wired
  into the clone's attributes, and covered by a smoke section that merges real
  branches in a throwaway repository.
- Dependencies: None.
- Files: `hooks/merge-todo` (new), `hooks/smoke-test`.
- Implementation checklist:
  - [x] Implement: read the common ancestor, ours, and theirs; keep the preamble;
        emit entries in ours-then-theirs-new order; take an entry from either side
        when the other lacks it; leave an entry both sides changed differently
        unresolved so `git` still reports a conflict.
  - [x] Wire the driver into `.git/info/attributes` — see the Change Log for why
        this replaced the planned tracked `.gitattributes` line — and make the
        driver installable.
  - [x] Smoke: two branches appending different entries merge with both intact;
        the interleaving case that breaks `merge=union` is covered explicitly;
        same-entry field edit still conflicts.
- Acceptance: The three smoke scenarios behave as specified.
- Verification: `hooks/smoke-test` — "todo merge driver keeps both branches'
  entries", "…still conflicts on one entry changed twice", "…takes a one-sided
  edit without conflicting". The three-entry fixture is the `merge=union`
  interleaving shape: both entries end in the same two lines, so a union merge
  would drop one entry's `- Status:` while the driver keeps all three intact.
- Rollback: Remove `hooks/merge-todo`, the install line, and the smoke section.
- Status: done

### Step 2 — Make Todo IDs unique across parallel branches

- Goal: Two branches cut from the same base on the same day must not allocate the
  same Todo ID, so that a merge that keeps both entries leaves no duplicate ID
  for the ID lookup to resolve ambiguously.
- Dependencies: Step 1 (it is the case that exposes the collision).
- Files: `hooks/task` (the `intake` command's ID allocation), `hooks/smoke-test`,
  `hooks/smoke-test-windows.ps1`.
- Implementation checklist:
  - [x] Derive the ID deterministically from inputs that differ between tasks —
        date plus a digest of the goal — so every branch that creates the entry
        computes the same ID, and two different goals never collide.
  - [x] Keep the `TF-<date>-<suffix>` shape readable and grep-able; document the
        suffix's meaning where intake is documented.
  - [x] The deterministic scheme proved practical, so no merge-time renumbering
        fallback was needed.
- Acceptance: Two same-day intakes with different goals get different IDs from
  independent clones of the same base; no duplicate IDs after a merge.
- Verification: `hooks/smoke-test` — "Todo IDs are derived from the goal, not from
  a shared counter" asserts the shape, two distinct goals differing, one goal
  agreeing across two independent roots, and a two-branch merge of two same-day
  intakes landing as three intact entries with no conflict. ID lookup is checked
  by promoting the intake's own ID in the lifecycle section.
- Rollback: Revert the intake change; Step 1 still merges text correctly.
- Status: done

### Step 3 — Install the driver from a hook

- Goal: A fresh clone gets the driver configured without manual setup.
- Dependencies: Step 1.
- Files: `hooks/install-merge-driver` (new), `hooks/session-start`.
- Implementation checklist:
  - [x] Idempotent, `--local` only, silent on success, best-effort failure.
  - [x] Do not touch anything outside the *current repository's* config.
  - [x] A TaskFlow root that is not a Git repository is a silent no-op rather
        than a `git config` fatal error.
- Acceptance: Running SessionStart twice leaves the local config unchanged; a
  repository without TaskFlowDocs is unaffected.
- Verification: `hooks/smoke-test` — "merge driver installation is local,
  idempotent, and silent"; `hooks/smoke-test-windows.ps1` runs the real
  `session-start` through `run-hook.cmd` in a non-Git fixture root and passes.
- Rollback: Remove the call site and the script.
- Status: done

### Step 4 — Document the strategy and its limits

- Goal: An Agent or maintainer reading the Skill knows what happens when two
  branches touch Todo, and what to do about it.
- Dependencies: Step 3.
- Files: `skills/taskflow/references/runtime.md`, `skills/taskflow/SKILL.md`,
  `README.md`, `README.zh-CN.md`, `hooks/README.md`.
- Implementation checklist:
  - [x] State the strategy, the local-merge requirement, and the web-UI
        limitation.
  - [x] Keep both READMEs aligned per `CODE_STYLE.md`; `hooks/README.md` carries
        the hook-level scope note.
- Acceptance: No document implies the web UI will merge Todo automatically.
- Verification: Read-through; `grep -rn 'merge=taskflow-todo\|install-merge-driver|
  merge-todo' README.md README.zh-CN.md hooks/README.md skills/taskflow` returns
  the intended locations and nothing contradictory.
- Rollback: Revert the documentation commit.
- Status: done

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
- Git passes a merge driver `%O %A %B` — ancestor, ours, theirs. The first draft
  read them as `ours base theirs` and produced a merge that silently dropped one
  side's entry. Caught by running the driver through a real `git merge` in a
  throwaway repository rather than by calling the script directly; the smoke
  section now does the same.
- The driver takes three inputs, not two: an entry both sides have but only one
  side changed is taken from the side that changed it, so the ordinary
  "one branch archived its task while another added a new entry" merge does not
  conflict. Comparing ours against theirs alone would have reported a conflict
  for every one-sided edit.
- Entry identity falls back from `- ID:` to the heading, in both directions:
  a lookup by ID alone would append an entry a second time when only one side had
  written its ID yet.
- Step 1's plan named a tracked `.gitattributes` line. Changed to the untracked
  `.git/info/attributes`: the attribute is per-clone configuration for a tool
  that only some clones have, and writing it tracked would push one user's choice
  into every other user's `git status`. This is a work revision — same mechanism,
  different file — not a Task version change.
- Step 1's planned failure-mode note in §Risks said the install was part of Step 3.
  It is `hooks/install-merge-driver`, called best-effort from `session-start`.
- Todo ID suffix is `cksum` modulo 16777216 rendered as six hex digits. `cksum`
  is in POSIX, so it is present on macOS, Windows' Git Bash, and Linux; a
  `sha256sum`/`shasum` split would have needed a branch per platform.
- Intake retains a collision guard: a digest clash between two different goals is
  refused loudly rather than written, because a duplicate ID makes every later
  lookup ambiguous.

## Follow-ups

- If web-UI merging becomes a requirement, the only structural fix is one Todo
  file per entry, which is a separate, larger task.
- Todo IDs on this repository's existing entries keep their numeric suffix. The
  scheme is only applied to new intake; rewriting history is out of scope.

## Version History

- v1 — planning.