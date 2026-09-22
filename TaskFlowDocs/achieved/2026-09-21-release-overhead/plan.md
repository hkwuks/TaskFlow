# Plan — Cut the mechanical overhead out of a release without adding any authority to it

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `RELEASE.md` — the release procedure this bounds.
- `hooks/release-check` — the read-only check extended here.
- `CONTRIBUTING.md` `## Checks` — where `hooks/smoke-test` is required.
- Task-level evidence for the corrected scope: `prd.md` `## Background / Confirmed
  Facts`, taken from `620c6a7`, `c3c536d`, `c1147ab`, and a live mutation run of
  `release-check`.

## Related Tasks

- `TF-20260919-c41f8a` — this task's Todo item.
- `TF-20260919-76e7fb` — delivered: a release no longer runs the TaskFlow flow.
  That change is why the v1.0.7 pin window's extra `plan.md` is historical.
- `TF-20260919-b7821b` — deferred, out of scope here.

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell/awk text
  processing, POSIX-portability references, and the repository's own hook
  conventions, all read directly.`

## Preconditions

- [x] Applicable repository documents and personal rules inspected;
  precedence/conflicts recorded. — `RELEASE.md`, `CONTRIBUTING.md`,
  `CODE_STYLE.md`, and `TaskFlowDocs/repository-docs/index.md` read.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-21
- Approved version: v1
- Approved scope: R1–R7; the corrected item (2) as a stating rule (R4), and the
  `TaskFlowDocs/` exemption in the pin-window rule (R5).

## Steps

### Step 1 — `hooks/release-version`, the one-call literal writer

- Goal: one command writes all eight mechanical literals in six files, and
  refuses before writing anything when it cannot.
- Dependencies: none.
- Files: `hooks/release-version` (new).
- Implementation checklist:
  - [x] Accept `<x.y.z> [root]`; validate the shape and that it is greater than
        the current `.claude-plugin/plugin.json` version.
  - [x] Require every target file to exist and `CHANGELOG.md` to already carry a
        `## [x.y.z]` section (R3). Refuse otherwise.
  - [x] Stage all rewrites in a temp dir under the same filesystem, then move
        them into place only after every check passed (R2).
  - [x] Write the four manifests, each README's **every** plugin-list sample
        line, and the Codex/CodeBuddy cachebuster date from the hook's `today`.
  - [x] Write nothing else: no tag, no push, no procedure step (R7).
- Acceptance: A and D.
- Verification: `bash hooks/release-check .` on a fixture prints `pass`; each
  refusal case diffed by digest.
- Rollback: delete `hooks/release-version`; no other file depends on it.
- Status: done

### Step 2 — `hooks/release-check`: every README literal, and the pin window

- Goal: close the two measured gaps — a stale second README literal passing, and
  a pin window carrying an unexplained change.
- Dependencies: Step 1 (its acceptance runs through this check).
- Files: `hooks/release-check`.
- Implementation checklist:
  - [x] Replace the `head -1` README reads with a loop over every match, and
        report each one (R6).  - [x] Add the pin-window rule: resolve `ref` to its commit, walk
        `tag..sha` with `git diff --name-only`, and fail with the paths named
        when anything other than the two marketplace catalogs or a
        `TaskFlowDocs/` path appears (R5).
  - [x] Keep every existing exit code and `STATUS:` line — CI and `RELEASE.md`
        read them.
- Acceptance: B and C.
- Verification: mutate each check in turn and confirm the suite fails.
- Rollback: `git checkout -- hooks/release-check`.
- Status: done

### Step 3 — `RELEASE.md` states the ordering, and names the new command

- Goal: the tagged commit carrying the release section becomes a stated rule.
- Dependencies: none.
- Files: `RELEASE.md`.
- Implementation checklist:
  - [x] State that the `CHANGELOG.md` section is written before the tag, and why
        (R4) — the tag is the immutable artifact, so what it points at has to be
        complete.
  - [x] Add `hooks/release-version` to the scope list and to the pre-tag steps.
  - [x] Leave the atomic-push step, the rollback section, and the
        "does not push tags or create GitHub Releases automatically" boundary
        untouched.
- Acceptance: the file reads as one consistent procedure.
- Verification: `git diff --check`; re-read the tag/pin steps for contradiction.
- Rollback: `git checkout -- RELEASE.md`.
- Status: done

### Step 4 — smoke assertions and the mutation pass

- Goal: each new check fails when it is reverted.
- Dependencies: Steps 1–3.
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] Assert A–D against a fixture, in the fixture style the release-check
        section already uses.
  - [x] Mutate one check at a time; record what each mutation made fail.
- Acceptance: E.
- Verification: `bash hooks/smoke-test` — ALL SMOKE PASSED.
- Rollback: `git checkout -- hooks/smoke-test`.
- Status: done

## Checkpoints

- After Step 2: run `bash hooks/release-check .` on the real repository and
  confirm it still prints `STATUS: pass`.

## Verification / Review

Run in this worktree on 2026-09-21, all four green:

- `bash hooks/smoke-test` — ALL SMOKE PASSED
- `bash hooks/release-check .` — `STATUS: pass` on the unmodified repository, and
  it reports all nine literal lines (four manifests, the CHANGELOG section, and
  both samples in each README)
- `bash hooks/repository-check .` — `needs-user-input`, for the expected reason:
  this branch's task directory is still untracked, and the check reports an
  uncommitted task artifact rather than a governance defect. It clears when the
  task documents are committed to this branch.
- `git diff --check` — clean

Mutated once per check, each restored after:

| Mutation | Suite result |
|---|---|
| `readme_versions` restricted to the first match, as the old code did | `FAIL stale second README sample accepted` |
| the pin-window rule's guard forced false | `FAIL a stray file in the pin window was accepted` |
| `release-version`'s "exactly one version key" relaxed to "at least one" | `FAIL a manifest with two version keys was rewritten` |
| `release-version`'s CHANGELOG-section precondition removed | `FAIL release-version ran without a CHANGELOG section` |
| `release-version`'s already-at-target refusal removed | `FAIL a file already at the target version was overwritten silently` |

## Change Log

- 2026-09-21 — item (2) of the Todo entry is corrected to a stating rule; the
  measurement is in `prd.md`. Item (1) was an undercount, not a defect: eight
  literals in six files. Item (3)'s window rule gains a `TaskFlowDocs/` exemption.

## Follow-ups

- `TF-20260919-b7821b` — `hooks/version`'s Approval block shape. Still open.

## Version History

- v1 — planning.
