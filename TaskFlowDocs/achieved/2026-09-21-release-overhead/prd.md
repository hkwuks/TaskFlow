# Cut the mechanical overhead out of a release without adding any authority to it

> Task version: v1
> Status: completed

## Goal

Write every version literal a release moves from one command, make the tagged
commit's completeness a stated rule instead of an accident, and make a stale
release record fail CI instead of passing.

## Background / Confirmed Facts

All of the following was executed on `main` = `2f6ae43` (PR #46 merged),
2026-09-21. Nothing here is inferred.

**The release transaction as it actually shipped:**

- v1.0.8: the tagged commit `620c6a7` carries **all seven** files — four
  manifests, the `CHANGELOG.md` section, and both READMEs. The pin commit
  `c1147ab` differs only in the two marketplace catalogs.
- v1.0.7: the tagged commit `c3c536d` carries the `CHANGELOG.md` section too. Its
  pin window additionally carries `TaskFlowDocs/2026-09-18-release-v1-0-7/plan.md`
  (`6b71b2d`) — from the era when a release still ran the TaskFlow flow.
- The annotated tag body and the `CHANGELOG.md` section are separate and both
  present on `v1.0.8`. Neither is missing.

**Corrections to the filed item — this is why the scope below differs from it:**

1. **Its item (2) has no defect to fix.** The claim was that release notes live in
   a commit *after* the tag, so the tag is missing the release body and rewriting
   it would need owner authorization. Measured: the notes are already in the
   tagged commit for both v1.0.7 and v1.0.8. The annotation body that
   `git tag -a` writes is a second copy on the tag object, not a replacement for
   the first. **What is actually missing is narrower**: `RELEASE.md` never states
   the ordering, so nothing stops a later release from writing the section after
   the tag. That is a rule to state, not code to write.
2. **Its item (1) miscounts.** It says six fixed literals in seven files. The
   mechanical literals are **eight in six files**: four manifests, plus two
   plugin-list samples in each README (`README.md:207,261`,
   `README.zh-CN.md:173,226`). The seventh file, `CHANGELOG.md`, is prose and
   stays with the Agent — that part of the item is right.
3. **`hooks/release-check` half-checks each README.** It reads
   `sed -n 's/^#.*Version:.*//p' … | head -1`, so only the first of the two
   literals per README is compared. Mutating `README.md:261` from `1.0.8` to
   `1.0.7` and running the check on the real repository prints `STATUS: pass`.
   Two literals that a release has to move are unguarded, which is the same
   failure the item's (3) is about.

**What the item's (3) window rule would do to history:** the v1.0.8 window is
exactly the two marketplace files, so the rule passes it. The v1.0.7 window
contains a task `plan.md`, so the rule would have failed that release. That file
was a side effect of the now-removed TaskFlow release flow, not of the pin step.

## Requirements

- **R1** `hooks/release-version <x.y.z> [root]` writes, in a single call, every
  mechanical version literal: the four manifests and every plugin-list sample
  line in both READMEs. `bash hooks/release-check .` reports `pass` immediately
  after, with no further edits.
- **R2** The command checks before it writes. Every refusal exits non-zero and
  leaves all six files byte-identical.
- **R3** The `CHANGELOG.md` prose stays with the Agent, and its `## [x.y.z]`
  section must already exist when the command runs. The command refuses
  otherwise, which is what binds the prose to the same commit as the literals.
- **R4** `RELEASE.md` states that the release-notes section is written before the
  tag, so the tagged commit carries it. No procedure step changes; only the
  reason is written down.
- **R5** `release-check` fails when the commit range from the tag-named commit to
  the pinned commit contains a change other than the two marketplace catalogs'
  `ref`/`sha` literals and paths under `TaskFlowDocs/`, and names the offending
  paths. Task documents are exempt because they are not distributed with the
  release, so a task document in the window cannot make a pin ship unpublished
  code.
- **R6** `release-check` compares **every** README version literal, not the first
  one per file.
- **R7** The command writes nothing that decides anything. It transcribes a
  version the release owner approved; it never tags, pushes, publishes, or
  approves. It must not touch `RELEASE.md`'s step 5 boundary — no automatic tag
  and no automatic GitHub Release.

## Acceptance Criteria

- **A** On a fixture at version `1.0.8`, `bash hooks/release-version 1.0.9 .`
  then `bash hooks/release-check .` prints `STATUS: pass`.
- **B** On a fixture whose `README.md` second literal is stale, `release-check`
  exits `2` and names `README.md`.
- **C** On a fixture whose pin window contains an unrelated file outside
  `TaskFlowDocs/`, `release-check` exits `2` and names that path; a fixture whose
  window contains only a `TaskFlowDocs/` file still passes.
- **D** Each refusal — malformed version, missing file, no `## [x.y.z]` section in
  `CHANGELOG.md`, or a version not greater than the current one — exits non-zero
  and leaves the tree unchanged, verified by digest before and after.
- **E** `bash hooks/smoke-test` passes, and each new assertion fails when its
  check is reverted (one mutation at a time).

## In Scope

- New `hooks/release-version`.
- `hooks/release-check`: every README literal (R6), the pin-window rule (R5).
- `RELEASE.md`: the ordering rule (R4), and the scope list gains the new command.
- `hooks/smoke-test`: assertions for A–D and for the reverted checks under E.

## Out of Scope

- Any change to the atomic push, the tag, or the GitHub Release steps.
- Inserting the `CHANGELOG.md` prose. The section heading is checked, never
  generated.
- Rewriting any existing tag or its annotation.
- The `cachebuster` date format, which stays `+<host>.<yyyymmdd>`.

## Risks / Deferred Items

- **Risk: R5 turns a future legitimate window into a red CI.** Mitigated by the
  `TaskFlowDocs/` exemption, which is what the v1.0.7 window needed. Anything
  else between the tag and the pin now blocks, and the escape is to move that
  change before the tag.
- **Deferred: `TF-20260919-b7821b`** (`hooks/version` writes a different Approval
  block shape than `hooks/task` generates). Untouched here; that hook is the
  Task-version archiver, not the release path.

## Open Questions

None outstanding. Both questions raised in the first draft of this PRD were
settled by the user before approval:

- the item's (2) is corrected to a stating rule (R4), not a procedure change;
- `TaskFlowDocs/` is exempt from the pin-window rule (R5).

## Version History

- v1 — planning.
