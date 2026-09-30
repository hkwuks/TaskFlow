# A release skips re-running tests that CI already ran green on the same revision,
> Task version: v2
> Status: checking

## Goal

Make CI the repository's test authority, and hold the rule in **both** directions: what CI can test is tested by CI, and what CI cannot test is still tested locally. A release must not re-run tests CI has already adjudicated; every pull request must prefer CI over a local run, so local time and resources are not spent repeating the CI matrix; and because CI then carries that authority, CI has to be kept current and compatible rather than allowed to lag behind the surfaces it is supposed to cover.

## What v2 changes

v1 named two documents, `RELEASE.md` and `CONTRIBUTING.md`. Implementing v1 surfaced three more places that demand a local smoke run and would contradict the rule as written:

- `.github/pull_request_template.md:14` — a required pull-request checkbox for `bash hooks/smoke-test`. Left alone, every PR would have to tick "I re-ran the CI matrix locally", which is the practice this change removes.
- `README.md:361` and `README.zh-CN.md:322` — both state that CONTRIBUTING's pre-pull-request checks include `hooks/smoke-test`. Left alone, both become false statements.

v2 brings those three into scope, and states the principle in both directions as the release owner required, so that preferring CI can never be read as making a local check optional. v1's requirements, acceptance criteria, and exclusions are otherwise carried forward unchanged.

## Background / Confirmed Facts

- `RELEASE.md:54` requires `bash hooks/smoke-test` in the Validation checklist, unconditionally and for every release.
- `CONTRIBUTING.md:41-49` asks for the same suite, plus `quick_validate.py` and `git diff --check`, before opening a pull request.
- A release commit changes only version literals and the `CHANGELOG.md` section; the second commit of the pair changes only the two marketplace catalogs. Neither touches `hooks/` or `skills/`, which is the surface the smoke suite exercises. Measured on the 1.1.2 release: `5d4fccf` touches neither path.
- CI runs the smoke suite on `ubuntu-latest`, `macos-latest`, and `windows-latest` for every pull request and every push to `main` (`.github/workflows/hooks.yml:3-7`), so its verdict is already authoritative and three-OS wide — wider than any single local run.
- CI does **not** run `quick_validate.py`, `git diff --check`, or `hooks/repository-check`; the `release` job does run `hooks/release-check`. Those are the local-only side of the rule.
- On this host the suite cannot complete at all: the no-interpreter section fails with `error while loading shared libraries` because MSYS symlinks its own binaries. The same section fails on unmodified `origin/main`, so it is not a property of any particular change. The 1.1.2 release recorded it as a limitation instead of a result, which is the shape of record this change is meant to remove.
- `RELEASE.md:73` forbids recording an unavailable check as passed.
- The release owner widened the requirement on 2026-09-30: it applies to every pull request, not only to releases; CI's own upkeep is part of it; and the two directions are to be stated together.

## Requirements

- R1. The `RELEASE.md` Validation checklist must not require re-running a test that CI has already run green.
- R2. The rule must state its predicate precisely. The tagged commit is a new commit, so "the same revision" is the wrong test. The right one is that everything the tagged commit changes relative to a CI-green commit falls outside the surface the suite exercises.
- R3. Checks whose differences only a release commit produces — `hooks/release-check`, `hooks/repository-check`, `quick_validate.py`, `git diff --check` — stay unconditional.
- R4. Skipping must stay distinguishable from passing: the release notes must still record which checks were not run, and why.
- R5. `CONTRIBUTING.md` must name CI as the preferred test authority for every pull request, not only for releases: a local run is for what CI structurally cannot cover, and re-running the CI matrix locally is not required.
- R6. Because CI carries that authority, CI has to be kept current and compatible. A change that adds or alters a surface CI does not exercise must extend CI in the same change, rather than leaving that surface verified only by hand; and CI must keep running on the hosts it declares.
- R7. The rule is stated in both directions, and preference never reads as exemption: a check CI can run belongs to CI, and a check CI cannot run remains a local requirement that no part of this change relaxes.
- R8. No document in the repository may require a local run of a check that CI covers, and none may describe CONTRIBUTING's pre-pull-request checks as including one.

## Acceptance Criteria

- A1. RELEASE.md, as amended, permits a release to skip `bash hooks/smoke-test` when CI has run green on a revision the release commit does not diverge from outside the suite's surface — and requires the release notes to name that CI run.
- A2. No reading of the amended text permits skipping `hooks/release-check`, `hooks/repository-check`, `quick_validate.py`, or `git diff --check`.
- A3. The amended text cannot be read as "the suite passed" when it was not run.
- A4. CONTRIBUTING.md names CI as the preferred test authority for every pull request, and says plainly what a local run is still for.
- A5. `bash hooks/release-check .` still reports `pass`, and `git diff --check` is clean.
- A6. The amended text closes the loophole R6 exists to prevent: it does not let a contributor skip local verification of a surface CI does not exercise. It states that such a surface is added to CI in the same change, or that running it locally is the fallback.
- A7. The documents do not contradict each other when read together: CONTRIBUTING carries the principle, RELEASE carries the procedure that applies it, and neither restates the other's content.
- A8. `.github/pull_request_template.md` no longer requires a local `bash hooks/smoke-test`, and its verification section still asks a contributor to report what CI ran.
- A9. Neither README claims that CONTRIBUTING's pre-pull-request checks include `hooks/smoke-test`, and both still describe the suite accurately as something the repository has and CI runs.

## In Scope

- `RELEASE.md` — the Validation checklist and the rules around it.
- `CONTRIBUTING.md` — the Checks section, and the one line in Working branches that requires running the suite on the branch whose files changed.
- `.github/pull_request_template.md` — the verification checklist.
- `README.md` and `README.zh-CN.md` — the sentences describing what CONTRIBUTING requires before a pull request.

## Out of Scope

- `RELEASE.md` step 6, the manual three-host catalog validation. Same theme — release-time work CI never exercises — but tracked as `TF-20260928-3910fb` and not folded in here.
- Any hook or Skill change.
- Changing what CI runs, adding a CI job, or rewiring the workflow. R6 is a rule about future changes.
- `hooks/README.md`, which documents the suite rather than requiring a run of it.

## Risks / Deferred Items

- The predicate stays prose. Nothing enforces it mechanically, and no hook can: judging whether a diff falls outside the suite's surface needs a human reading. Accepting that is the point of the change, so the mitigation is disclosure — the record must state the comparison that was made, which keeps the decision auditable even though it is not automatic.
- R6 is the load-bearing half. Preferring CI only holds while CI covers the right things, so this change trades a repeated local cost for a maintenance obligation. The mitigation is A6's wording: the obligation is stated in the same rule that creates it, at the point of the change that creates the gap.
- The rule now lives in five documents. They can drift, and v1 underestimated this by counting two. Mitigated by A7's division of labour — CONTRIBUTING states the principle, RELEASE states the procedure, the PR template states what a PR reports, and the READMEs state where the rules are — but the count is a real maintenance cost, recorded as one rather than argued away.

## Open Questions

- None blocking. The two boundary questions recorded on the Todo item are answered by A1 and A3.
