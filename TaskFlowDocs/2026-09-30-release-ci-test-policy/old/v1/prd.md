# A release skips re-running tests that CI already ran green on the same revision,
> Task version: v1
> Status: in_progress

## Goal

Make CI the repository's test authority. A release must not re-run tests CI has already adjudicated, every pull request must prefer CI over a local run so local time and resources are not spent repeating the CI matrix, and because CI then carries that authority, CI has to be kept current and compatible rather than allowed to lag behind the surfaces it is supposed to cover.

## Background / Confirmed Facts

- `RELEASE.md:54` requires `bash hooks/smoke-test` in the Validation checklist, unconditionally and for every release.
- `CONTRIBUTING.md:41-49` asks for the same suite, plus `quick_validate.py` and `git diff --check`, before opening a pull request.
- A release commit changes only version literals and the `CHANGELOG.md` section; the second commit of the pair changes only the two marketplace catalogs. Neither touches `hooks/` or `skills/`, which is the surface the smoke suite exercises. Measured on the 1.1.2 release: `5d4fccf` touches neither path.
- CI runs the smoke suite on `ubuntu-latest`, `macos-latest`, and `windows-latest` for every push and pull request, so its verdict is already authoritative and three-OS wide — wider than any single local run.
- On this host the suite cannot complete at all: the no-interpreter section fails with `error while loading shared libraries` because MSYS symlinks its own binaries. The same section fails on unmodified `origin/main`, so it is not a property of any particular change. The 1.1.2 release recorded it as a limitation instead of a result, which is the shape of record this change is meant to remove.
- `hooks/release-check .` and `hooks/repository-check .` check version literals, catalog `ref`/`sha` pairs, and release-record freshness. Only a release commit produces those differences, so CI cannot cover them.
- `RELEASE.md:73` forbids recording an unavailable check as passed.
- The release owner widened the requirement on 2026-09-30: it applies to every pull request, not only to releases, and CI's own upkeep is part of it.

## Requirements

- R1. The `RELEASE.md` Validation checklist must not require re-running a test that CI has already run green.
- R2. The rule must state its predicate precisely. The tagged commit is a new commit, so "the same revision" is the wrong test. The right one is that everything the tagged commit changes relative to a CI-green commit falls outside the surface the suite exercises.
- R3. Checks whose differences only a release commit produces — `hooks/release-check`, `hooks/repository-check`, `quick_validate.py`, `git diff --check` — stay unconditional.
- R4. Skipping must stay distinguishable from passing: the release notes must still record which checks were not run, and why.
- R5. `CONTRIBUTING.md` must name CI as the preferred test authority for every pull request, not only for releases: a local run is for what CI structurally cannot cover — the host-specific, the private, the pre-push — and re-running the CI matrix locally is not required.
- R6. Because CI carries that authority, CI has to be kept current and compatible. A change that adds or alters a surface CI does not exercise must extend CI in the same change, rather than leaving that surface verified only by hand; and CI must keep running on the hosts it declares.

## Acceptance Criteria

- A1. RELEASE.md, as amended, permits a release to skip `bash hooks/smoke-test` when CI has run green on a revision the release commit does not diverge from outside the suite's surface — and requires the release notes to name that CI run.
- A2. No reading of the amended text permits skipping `hooks/release-check`, `hooks/repository-check`, `quick_validate.py`, or `git diff --check`.
- A3. The amended text cannot be read as "the suite passed" when it was not run.
- A4. CONTRIBUTING.md names CI as the preferred test authority for every pull request, and says plainly what a local run is still for.
- A5. `bash hooks/release-check .` still reports `pass`, and `git diff --check` is clean.
- A6. The amended text closes the loophole R6 exists to prevent: it does not let a contributor skip local verification of a surface CI does not exercise. It states that such a surface is added to CI in the same change, or that running it locally is the fallback.
- A7. The two documents do not contradict each other when read together: CONTRIBUTING carries the principle, RELEASE carries the procedure that applies it, and neither restates the other's content.

## In Scope

- `RELEASE.md` — the Validation checklist and the rules around it.
- `CONTRIBUTING.md` — the Checks section.

## Out of Scope

- `RELEASE.md:111` step 6, the manual three-host catalog validation. It is the same theme — release-time work CI never exercises — but it is tracked as `TF-20260928-3910fb` and is not folded in here.
- Any hook or Skill change.
- Changing what CI runs today. R6 is a rule about future changes, not a rewiring of the current workflow.
- Adding a new CI job. Whether the current matrix is sufficient is not questioned here.

## Risks / Deferred Items

- The predicate stays prose. Nothing enforces it mechanically, and no hook can: judging whether a diff falls outside the suite's surface needs a human reading. Accepting that is the point of the change, so the mitigation is disclosure — the record must state the comparison that was made, which keeps the decision auditable even though it is not automatic.
- R6 is the load-bearing half. Preferring CI only holds while CI covers the right things, so this change trades a repeated local cost for a maintenance obligation. The mitigation is A6's wording: the obligation is stated in the same rule that creates it, at the point of the change that creates the gap.
- The rule is stated in two documents. They can drift. Mitigated by A7: CONTRIBUTING states the principle, RELEASE states the procedure, and neither duplicates the other.

## Open Questions

- None blocking. The two boundary questions recorded on the Todo item are answered by A1 and A3.
