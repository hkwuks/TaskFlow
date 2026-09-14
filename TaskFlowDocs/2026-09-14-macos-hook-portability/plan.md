# Plan — Restore macOS portability for hooks and smoke tests
> Task version: v1
> Status: ready

No spec required — small, self-contained task.

## Reference Pointers

- Reproduced failure: `hooks/version: line 27: selected[*]: unbound variable` under `/bin/bash` 3.2.57 (macOS).

## Related Tasks

- `TaskFlowDocs/achieved/2026-09-13-hooks-ci-matrix/` (added Linux + Windows CI; macOS was not covered).

## Skills / Tools Used (Optional)

- None beyond the repository's own hooks, smoke tests, and eval runner.

## Preconditions

- Fork `1692775560/TaskFlow`, branch `fix/macos-hook-portability`, base `hkwuks/TaskFlow:main`.

## Approval

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

External fork contribution: implementation and verification are complete; approval is requested from the maintainer via pull-request review. No approval is claimed or implied.

## Steps

### Step 1 — Fix bash 3.2 / BSD sed failures in `hooks/version`

- Goal: version transitions run on stock macOS.
- Dependencies: none.
- Files: `hooks/version`.
- Implementation checklist:
  - [x] Default the empty `selected` array expansion under `set -u` (`${selected[*]:-}`).
  - [x] Replace GNU-only bare `sed -i` with temp-file + `mv`, matching the existing awk rewrite idiom.
- Acceptance: version smoke sections pass on macOS.
- Verification: `== version bumps root + archives only changed docs == ok`; `== version rejects invalid input before mutation == ok`.
- Rollback: revert commit.
- Status: done

### Step 2 — Make `hooks/smoke-test` portable and stop deleting caller roots

- Goal: developers on stock macOS can run the full suite; a passed-in root is never removed.
- Dependencies: none.
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] Add a `digest` helper (`sha256sum`, falling back to `shasum -a 256`) and use it at all call sites.
  - [x] Replace GNU-only `sed -i` with temp-file + `mv`.
  - [x] Register the EXIT cleanup trap only when the script created the temp root itself.
- Acceptance: `ALL SMOKE PASSED` on macOS; caller root preserved.
- Verification: full suite `ALL SMOKE PASSED`; explicit caller-root run exits 0 and the root still exists.
- Rollback: revert commit.
- Status: done

### Step 3 — Cover macOS and the evals in CI

- Goal: the macOS breakage class is caught by CI; the eval runner is exercised.
- Dependencies: none.
- Files: `.github/workflows/hooks.yml`.
- Implementation checklist:
  - [x] Add `macos-latest` to the matrix; run bash smoke tests on every non-Windows runner.
  - [x] Add a `python3 evals/runner.py` step on non-Windows runners.
- Acceptance: workflow YAML parses; steps are OS-gated correctly.
- Verification: local `python3 evals/runner.py` → `PASS (6 evals)`; workflow syntax reviewed.
- Rollback: revert commit.
- Status: done

### Step 4 — Align license metadata and drop dead code

- Goal: plugin manifests agree with the AGPL-3.0 LICENSE; `repository-check` carries no unreachable branch.
- Dependencies: none.
- Files: `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `hooks/repository-check`.
- Implementation checklist:
  - [x] Set `"license": "AGPL-3.0-only"` in both plugin manifests.
  - [x] Remove the never-set `blocked` variable and its unreachable tail branch (exit 3 preflight unchanged).
- Acceptance: manifests parse; `repository-check` behavior unchanged.
- Verification: `python3 -m json.tool` on all manifests OK; `bash hooks/repository-check .` still reports `STATUS: needs-user-input` with exit 2.
- Rollback: revert commit.
- Status: done

### Step 5 — Record the task and open the fork pull request

- Goal: TaskFlow traceability for the change; PR satisfies `.github/pull_request_template.md`.
- Dependencies: Steps 1–4.
- Files: `TaskFlowDocs/todo.md`, `TaskFlowDocs/2026-09-14-macos-hook-portability/`.
- Implementation checklist:
  - [x] Add the Todo item and task records.
  - [ ] Push focused commits to the fork and open the PR against `hkwuks/TaskFlow:main`.
- Acceptance: PR opened with the template fields completed.
- Verification: PR URL recorded in the change log.
- Rollback: close the PR; delete the branch.
- Status: in_progress

## Checkpoints

- After Step 2: full smoke suite green on macOS (observed).

## Verification / Review

- `bash hooks/smoke-test` → `ALL SMOKE PASSED` (macOS 26, `/bin/bash` 3.2.57, BSD sed). Previously failed at the version section.
- Caller-root preservation: `bash hooks/smoke-test <dir>` exits 0 and `<dir>` still exists.
- `python3 evals/runner.py` → `PASS (6 evals)`.
- `python3 -m json.tool` on `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/marketplace.json` → OK.
- `bash hooks/repository-check .` → `STATUS: needs-user-input`, exit 2 (expected: branch has no upstream tracking branch).
- `git diff --check` → clean.
- Not run: the Skill validation script referenced in `CONTRIBUTING.md` (`/home/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py`) is maintainer-local and does not exist in this environment. Substitute: the smoke-test packaged-Skill contract assertions passed; no Skill content changed in this PR.

## Change Log

- 2026-09-14 — v1 records created by an external fork contributor; approval requested via pull request.

## Follow-ups

- Maintainer decides the final SPDX identifier (`AGPL-3.0-only` vs `AGPL-3.0-or-later`).
- Consider running the evals on Windows runners too (skipped here: `python3` invocation is only verified on non-Windows runners).

## Pull-request template mapping

- Summary → PRD Goal and Background.
- TaskFlow traceability → this directory; scope per PRD In Scope; base `main`; target repository `hkwuks/TaskFlow`.
- Verification → commands and results above; the maintainer-local Skill validator is recorded as unavailable with its substitute.
- Review boundaries → no secrets; no unrelated files; remotes (`origin` = upstream, `fork` = contributor fork) stated; limitations per Risks / Follow-ups.

## Version History

- v1 — planning.
