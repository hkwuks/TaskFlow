# Plan — Run TaskFlow hooks without a Python interpreter
> Task version: v1
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

- v1 — planning.