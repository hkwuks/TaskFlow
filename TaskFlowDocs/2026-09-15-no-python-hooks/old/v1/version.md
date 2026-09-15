# Archived Version v1 — Plan — Run TaskFlow hooks without a Python interpreter
> Task: 2026-09-15-no-python-hooks
> Version: v1
> Status: superseded
> Archived: 2026-09-15 13:23 +0800
> Superseded by: v2
> Archive mode: file
> Restore root: a new temporary directory (never overwrite the current task root)

## Change Summary

v1's Plan was approved, then superseded within the same session by two kinds of
change. The material ones reset the Approval record:

- The PRD did not record two decisions the user confirmed in the same review:
  Git for Windows Bash stays a required Windows runtime and no native PowerShell
  implementation is added; and error diagnostics keep their message while the
  interpreter's traceback text is not preserved. The second is why
  `malformed.err` and `unsafe.err` are the two fixture files this task changes on
  purpose.
- The Plan gained the fixture-comparator step: capture the Python
  implementation's fixtures, validate the comparator against an unchanged second
  run, then require 0 differences. v1 assumed a byte comparison without saying
  what it was measured against.

The remaining Plan edits are work revisions that would not have forced a bump on
their own (Step 1's wording, the `[x]` checkmarks, the recorded verification
commands). They are part of the v2 document because they were written before the
bump was taken, not because they changed the approved scope.

## Archived Materials

- `prd.md`, `plan.md`, `spec.md` as of commit `9c26465`, the last commit in which
  v1 was the current version.

`spec.md` carries no `> Status:` line, so `hooks/version` does not select it for
archival; the superseded copy is included here for a complete v1 record.

## Restore

Read the archived v1 core documents from a new temporary restore root. Do not
overwrite the current task root.

## Read This Version When

Checking what was approved before the fixture comparator existed, or whether the
POSIX-only direction was in scope from the first approved version (it was not —
v1 recorded the direction but not the two confirmed decisions above).
