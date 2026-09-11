# Plan — Limit TaskFlow to development requests
> Task version: v1
> Status: checking

No spec required — this is a focused Skill routing correction with no runtime API change.

## Skills / Tools Used

- `taskflow` — purpose: track this development change; outcome: succeeded; incorporated: the approved v1 boundary.
- `skill-creator` — purpose: correct Skill discovery scope; outcome: succeeded; incorporated: make the description discriminating and avoid constraining unrelated work.
- `ponytail` — purpose: keep the fix narrow; outcome: succeeded; incorporated: instruction and assertion changes only, no classifier Hook.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-10 22:43 +08:00
- Approved version: v1
- Approved scope: PRD / Plan and the three recommended routing boundaries.

## Steps

### Step 1 — Correct discovery and intake scope
- Implementation checklist:
  - [x] Restrict automatic invocation to development requests.
  - [x] Exclude read-only explanation/research/review/diagnosis.
  - [x] Preserve explicit `$taskflow` opt-in.
- Acceptance: applicability is decided before Todo intake.
- Verification: targeted text review.
- Rollback: revert Skill/reference/README edits.
- Status: done

### Step 2 — Verify routing contract
- Implementation checklist:
  - [x] Add focused smoke assertions.
  - [x] Run smoke test and `git diff --check`.
- Acceptance: exclusions and override remain explicit and consistent.
- Verification: existing smoke suite and contradiction search.
- Rollback: revert smoke assertions.
- Status: done

## Verification / Review

- Skill frontmatter now limits automatic discovery to development requests and explicit `$taskflow` planning/research.
- The applicability gate runs before Todo intake and excludes read-only explanation, translation, status, research, review, and diagnosis.
- README and artifact guidance use the same boundary.
- Contradictory universal-intake search returned no matches; relative-link validation found zero broken links.
- Git Bash `hooks/smoke-test`: `ALL SMOKE PASSED`; `git diff --check` passed.
- `TF-20260910-06` was marked `cancelled` as a historical example of incorrect intake; its files were retained and nothing was deleted.

## Version History

- v1 — approved and in progress.
