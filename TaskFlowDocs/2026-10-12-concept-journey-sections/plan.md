# Plan — Concept and journey sections for the TaskFlow template
> Task version: v1
> Status: completed

## Spec Pointers
- `spec.md`

## Reference Pointers
- `skills/taskflow/references/artifacts.md`
- `skills/taskflow/SKILL.md`
- `hooks/task`
- `evals/cases/taskflow.json`

## Related Tasks
- None.

## Skills / Tools Used
- `WebFetch` / `WebSearch` — upstream structure and conventions; outcome: succeeded; incorporated: template layout, eval runner semantics, fixture immutability.
- `shell` — scratch-repository promote run; outcome: succeeded; incorporated: the generated scaffolds were verified directly.

## Preconditions
- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded.
- [x] For remote/fork/PR work: remotes, target repository, base branch, local branch/base, freshness limits, and required checks recorded.
- [x] For PR creation/update: applicable template path, every required-field mapping, and template verification recorded.
- [x] Missing governance drafts and explicit approvals recorded before they become binding.

## Approval
- approved — user directed "直接改，提交 PR", and fixed the deletion/second-confirmation and two-layer project/session scope for the motivating case.

## Steps
### Step 1 — Split open questions and name the ready criterion
- Goal: give leaving `planning` a stated precondition.
- Files: `references/artifacts.md`, `SKILL.md`, `hooks/task`.
- Implementation checklist:
  - [x] Add `### Blocking` / `### Non-blocking` to both templates.
  - [x] Define blocking by consequence, not importance.
  - [x] Name the criterion in the `ready` state definition.
  - [x] Require a recorded assumption per non-blocking question.
  - [x] Update the `hooks/task` promote scaffold to match.

### Step 2 — Add the two conditional Spec sections
- Goal: make vocabulary and actor-visible states first-class.
- Files: `references/artifacts.md`, `SKILL.md`, `hooks/task`.
- Implementation checklist:
  - [x] Add both headings to the Spec template.
  - [x] Write fill guidance, including rejected vocabulary and recovery paths.
  - [x] Scope both sections and require a recorded reason to skip.
  - [x] Update the `hooks/task` promote scaffold to match.

### Step 3 — Complete the host list
- Goal: name every supported host in the Skill.
- Files: `SKILL.md`.
- Implementation checklist:
  - [x] Correct both occurrences left behind by CodeBuddy support.

### Step 4 — Cover the change with evals
- Goal: make the new rules executable.
- Files: `evals/cases/taskflow.json`, `evals/fixtures/...`.
- Implementation checklist:
  - [x] Add positive routing cases for product-design and concept-definition work.
  - [x] Add a negative case keeping pure explanation out of scope.
  - [x] Add artifact expectations for all four new headings.
  - [x] Extend the fixture task tree minimally.

## Checkpoints
- [x] Template edits and the `hooks/task` scaffolds changed together, verified by a real promote run rather than by reading the diff.

## Verification / Review
- `python3 evals/runner.py` → `PASS (9 evals)`
- `bash hooks/smoke-test` → `ALL SMOKE PASSED`
- `git diff --check origin/main..HEAD` → clean
- `bash -n` on the modified hook → syntax OK
- `hooks/task promote <id> <task-id> large` in a scratch repository → the
  generated `prd.md` carries the Blocking split and the generated `spec.md`
  carries both new sections.
- Review note: the eval fixture and the promote generator are two independent
  paths to the same templates, so both were exercised.

## Change Log
- v1 — initial change.

## Follow-ups
- Consider mechanical enforcement of the Blocking criterion in the state
  command. Left to the maintainer; raised in the PR body.

## Version History
- v1 — completed.
