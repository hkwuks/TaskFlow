# Plan — Run TaskFlow hooks without a Python interpreter
> Task version: v2
> Status: in_progress

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
- `TaskFlowDocs/2026-09-15-todo-merge-driver/` — the concurrent-Todo strategy
  task. Separate worktree; both touch `runtime.md`, so their PRs merge one at a
  time.

## Skills / Tools Used (Optional)

## Preconditions

- Approval of this Plan at Task version v2.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-15 14:49 +0800
- Approved version: v2
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
  - [x] Rewrite both hooks; keep each script's external interface, exit codes,
        and stderr diagnostics identical.
  - [x] Confirm the reference fixtures are reproduced byte for byte, including
        the no-op and unparseable-input paths.
- Acceptance: The two rewritten hooks reproduce the reference fixtures exactly,
  and the smoke sections covering them pass unmodified.
- Verification: `tools/fixture-compare /tmp/refcap/ref <fresh root>` reports
  `compared 43 fixture files` with 0 differences. The only differences it
  normalizes are the fixture root path, wall-clock stamps, and interpreter
  traceback framing — the last being the one intentional change, since the spec
  keeps the diagnostic message and drops the traceback text.
  `bash hooks/smoke-test` prints `ALL SMOKE PASSED`, and its stdout differs from
  the reference only by the one section added below.
- Rollback: `git checkout` the two hook files.
- Status: done

### Step 2 — Convert the remaining hooks and delete the runtime

- Goal: Convert `task`, `summarize-state`, `archive`, `reopen`, and
  `session-start`; delete `hooks/python-runtime` and every reference to it,
  including `TASKFLOW_PYTHON`.
- Dependencies: Step 1 (idiom proven).
- Files: `hooks/task`, `hooks/summarize-state`, `hooks/archive`, `hooks/reopen`,
  `hooks/session-start`, `hooks/python-runtime` (deleted), `hooks/smoke-test`.
- Implementation checklist:
  - [x] Convert each hook, preserving argument handling, exit codes, and output.
  - [x] Replace the `python-runtime` smoke section with a no-interpreter
        assertion: run the suite with a `PATH` that contains no `python*`.
  - [x] Confirm the Windows smoke path does not reference the deleted runtime.
- Acceptance: No hook invokes Python; the suite passes with no Python on `PATH`.
- Verification: The full suite passes twice over — once normally, and once with
  an outer `PATH` holding every `/usr/bin` tool except `python*`, where it prints
  `ALL SMOKE PASSED`. `grep -rn -i python hooks/` matches nothing outside the
  smoke test's own assertion.
- Rollback: `git checkout` the converted hooks and restore `python-runtime`.
- Status: done

### Step 3 — Align CI and documentation

- Goal: Remove Python from the hook CI job and correct the documentation that
  states an interpreter is required.
- Dependencies: Step 2.
- Files: `.github/workflows/hooks.yml`, `hooks/README.md`,
  `skills/taskflow/references/runtime.md`, `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [x] Drop `actions/setup-python` from the hook job if nothing else uses it;
        keep it if `evals/runner.py` still runs there, and say which in the Plan.
  - [x] Restate the runtime as: POSIX shell + `awk` + `sed`, bash 3.2 level, Git
        for Windows Bash on Windows.
  - [x] Remove `TASKFLOW_PYTHON` from user-facing guidance.
- Acceptance: No user-facing document instructs installing Python for TaskFlow.
- Verification: The `smoke` job installs no interpreter at all; `evals/runner.py`
  moved to its own `evals` job, which keeps `setup-python` because the eval runner
  is repository tooling rather than shipped plugin runtime. `grep -rn -i python`
  over the documented surfaces matches only that one workflow line.
- Rollback: Revert the documentation and workflow commit.
- Status: done

## Checkpoints

- After Step 1: the hardest conversion is proven before the rest is attempted.
- After Step 2: the dependency is gone; Step 3 is text only.
- Step 1 and Step 2 shipped as separate commits, so the two heaviest conversions
  were auditable against the reference before the remaining four were attempted.

## Verification / Review

- `tools/fixture-compare <reference> <candidate>` reports 0 differences over 41
  fixture files, and the smoke suite's stdout is identical apart from the two
  sections added by this task. The reference is captured from the Python
  implementation before it was removed.
- `bash hooks/smoke-test` with `PATH` containing no `python*`.
- `bash -n` on every hook; manual review of `awk`/`sed` for GNU-only constructs.
- CI: ubuntu, macos, windows.

## Change Log

- 2026-09-15 14:49 — Implementation verified: `bash hooks/smoke-test` prints
  `ALL SMOKE PASSED` both normally and with an outer `PATH` containing every
  `/usr/bin` tool except `python*`; `python3 evals/runner.py` prints
  `PASS (6 evals)`; `tools/fixture-compare` reports 0 differences over 41
  fixture files captured from the Python implementation.
- 2026-09-15 — Approval recorded at v2 after the version bump.

- 2026-09-15 — Task version bumped from v1 to v2 and re-approved: the PRD recorded
  a POSIX `awk`/`sed` direction but not the user's confirmed answers (Git for
  Windows Bash stays required; no PowerShell implementation; error diagnostics
  keep the message and may drop traceback text).
- 2026-09-15 — Captured the reference fixture set from the Python implementation
  and validated the comparator against a second unchanged run.
- 2026-09-15 — Converted `task`, `summarize-state`, `archive`, `reopen`, and
  `session-start`; deleted `python-runtime`. The comparison found six defects in
  the drafts, each listed in the implementation commit: an index-row column
  misread, a duplicate candidate row on re-run, a dropped heading on append, an
  `ls` of the current directory when no plan exists, a pipeline that truncated
  the target when awk rejected the input, and a `reopen` path that emitted the
  original text before deciding to append. Two more came from reading the
  result rather than the diff: `%c` double-encoding non-ASCII under a UTF-8
  locale, and a `command -v` that returned a shell-function name so the curated
  PATH had no real `grep`.

## Follow-ups

- If a future hook needs structured parsing beyond `awk`/`sed`, prefer the
  existing single-command transition scripts over reintroducing an interpreter.

## Version History

- v1 — planning.
- v2 — approved: records the confirmed POSIX-only direction and the fixture
  comparator; supersedes v1 (archived under `old/v1/`).
- v2 — implemented and verified: no hook invokes an interpreter, and the suite
  passes on a host where none is reachable.
