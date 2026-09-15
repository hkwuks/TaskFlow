# Archived Version v1 — Plan — Run TaskFlow hooks without a Python interpreter
> Task: 2026-09-15-no-python-hooks
> Version: v1
> Status: superseded
> Archived: 2026-09-15 13:23 +0800
> Superseded by: v2
> Archive mode: file

## Change Summary
v1 was approved before the Plan's fixture-comparator step existed and before the
PRD recorded the two decisions the user confirmed in the same review:

- Git for Windows Bash stays a required Windows runtime; no native PowerShell
  implementation is added.
- Error diagnostics keep their message and drop the interpreter's traceback text,
  so `malformed.err` and `unsafe.err` are the two fixture files this task changes
  on purpose.

The Plan also gained the comparator step (capture the Python implementation's
fixtures, validate the comparator itself, then require 0 differences) and the
reopen/`complete` blank-line case found while implementing it.

## Archived Materials
- prd.md
- plan.md
- spec.md

`spec.md` carries no `> Status:` line, so `hooks/version` did not select or
archive it; the superseded copy is restored here from the pre-bump commit so the
v1 record is complete.

## Restore
Read the archived v1 core docs from a new temporary restore root. Do not overwrite the current task root.
