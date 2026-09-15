# Plan — Run TaskFlow hooks without a Python interpreter
> Task version: v1
> Status: ready

## Spec Pointers

- `spec.md`

## Reference Pointers

- `hooks/version` and `hooks/repository-check` — existing Python-free hooks; the
  temp-file + `mv` write idiom and the `awk` field-rewrite style to match.
- `TaskFlowDocs/achieved/2026-09-14-macos-hook-portability/` — the portability
  floor this change must not regress.

## Related Tasks

- `TaskFlowDocs/2026-09-14-macos-hook-portability/` (achieved) — established bash
  3.2 + BSD userland as the supported floor.
- Todo `TF-20260915-02` — concurrent-Todo strategy; separate task, separate
  worktree. Both touch `runtime.md`, so their PRs merge one at a time.

## Skills / Tools Used (Optional)

## Preconditions

- Approval of this Plan at Task version v1.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-15 13:14 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Prove byte-identical output on the two heaviest hooks

- Goal: Rewrite `hooks/repository-docs-context` and `hooks/session-record` with
  POSIX `awk`/`sed` and confirm byte-identical output on the existing smoke
  fixtures. These two carry the most structured logic (index sync, session
  upsert) and exercise every construct the other hooks need.
- Dependencies: None.
- Files: `hooks/repository-docs-context`, `hooks/session-record`,
  `hooks/smoke-test` (new equivalence section), `tools/fixture-compare` (new).
- Implementation checklist:
  - [x] Capture the Python implementation's output as the reference: run
        `bash hooks/smoke-test <dir>` against the unmodified hooks and keep the
        produced fixture files.
  - [x] Add a fixture comparator that byte-compares two smoke roots, normalizing
        only the root path and excluding `.git/` and the WindowsApps shim.
  - [x] Confirm the comparator itself is safe: it reports no differences when run
        against an unchanged second run, so it measures equality rather than the
        absence of a smoke failure.
  - [ ] Rewrite both hooks; keep each script's external interface, exit codes,
        and stderr diagnostics identical.
  - [ ] Confirm the reference fixtures are reproduced byte for byte, including
        the no-op and unparseable-input paths.
- Acceptance: The two rewritten hooks reproduce the reference fixtures exactly,
  and the smoke sections covering them pass unmodified.
- Verification: `tools/fixture-compare` reports 0 differences over the captured
  fixture set; the Python-runtime error fixture is the one intentional
  difference (the message stays, the traceback text does not).
- Rollback: `git checkout` the two hook files.
- Status: pending

### Step 2 — Convert the remaining hooks and delete the runtime

- Goal: Convert `task`, `summarize-state`, `archive`, `reopen`, and
  `session-start`; delete `hooks/python-runtime` and every reference to it,
  including `TASKFLOW_PYTHON`.
- Dependencies: Step 1 (idiom proven).
- Files: `hooks/task`, `hooks/summarize-state`, `hooks/archive`, `hooks/reopen`,
  `hooks/session-start`, `hooks/python-runtime` (deleted), `hooks/smoke-test`.
- Implementation checklist:
  - [ ] Convert each hook, preserving argument handling, exit codes, and output.
  - [ ] Replace the `python-runtime` smoke section with a no-interpreter
        assertion: run the suite with a `PATH` that contains no `python*`.
  - [ ] Confirm the Windows smoke path does not reference the deleted runtime.
- Acceptance: No hook invokes Python; the suite passes with no Python on `PATH`.
- Verification: Full smoke suite under a Python-free `PATH`; `grep -rn python
  hooks/` reviewed against the Plan's explicit allowlist.
- Rollback: `git checkout` the converted hooks and restore `python-runtime`.
- Status: pending

### Step 3 — Align CI and documentation

- Goal: Remove Python from the hook CI job and correct the documentation that
  states an interpreter is required.
- Dependencies: Step 2.
- Files: `.github/workflows/hooks.yml`, `hooks/README.md`,
  `skills/taskflow/references/runtime.md`, `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [ ] Drop `actions/setup-python` from the hook job if nothing else uses it;
        keep it if `evals/runner.py` still runs there, and say which in the Plan.
  - [ ] Restate the runtime as: POSIX shell + `awk` + `sed`, bash 3.2 level, Git
        for Windows Bash on Windows.
  - [ ] Remove `TASKFLOW_PYTHON` from user-facing guidance.
- Acceptance: No user-facing document instructs installing Python for TaskFlow.
- Verification: `grep -rn -i python` over the documented surfaces; CI green on
  all three runners.
- Rollback: Revert the documentation and workflow commit.
- Status: pending

## Checkpoints

- After Step 1: the hardest conversion is proven before the rest is attempted.
- After Step 2: the dependency is gone; Step 3 is text only.

## Verification / Review

- `tools/fixture-compare <reference> <candidate>` reports 0 differences. The
  reference is captured from the Python implementation before it is removed.
- `bash hooks/smoke-test` with `PATH` containing no `python*`.
- `bash -n` on every hook; manual review of `awk`/`sed` for GNU-only constructs.
- CI: ubuntu, macos, windows.

## Change Log

- 2026-09-15 — Task version bumped from v1 to v2 and re-approved: the PRD recorded
  a POSIX `awk`/`sed` direction but not the user's confirmed answers (Git for
  Windows Bash stays required; no PowerShell implementation; error diagnostics
  keep the message and may drop traceback text).
- 2026-09-15 — Captured the reference fixture set from the Python implementation
  and validated the comparator against a second unchanged run.

## Follow-ups

- If a future hook needs structured parsing beyond `awk`/`sed`, prefer the
  existing single-command transition scripts over reintroducing an interpreter.

## Version History

- v1 — planning.