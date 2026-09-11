# Archived Version v1 — Support host/harness hooks in TaskFlow
> Task: 2026-09-08-runtime-hooks
> Version: v1
> Status: superseded
> Archived: 2026-09-08 23:20 +08:00
> Superseded by: v2
> Archive mode: file
> Restore root: a new temporary directory

## Change Summary

v1 proposed per-host hook subfolders (`hooks/claude/`, `hooks/codex/`, `hooks/shared/`) with thin entry scripts, after the user approved reversing the "non-runtime" claim. Review feedback changed the deliverable shape before implementation was finalized: the user pointed at `obra/superpowers/hooks` as the reference layout and confirmed a bash + Windows-variant choice (not Python). v2 therefore replaces per-host subfolders and python with the flat superpowers shape (extensionless bash scripts, one hook JSON per host, `run-hook.cmd` polyglot launcher), and makes `archive` a full transaction that also updates the linked Todo item.

## Archived Materials

- `prd.md` (v1: per-host folders, SessionStart summary per host, single-command transitions)
- `spec.md` (v1: per-host folder contract, thin entry scripts, python-tolerant wording)
- `plan.md` (v1 steps ran against the per-host design; superseded in place — v2 plan re-specifies Step 3)

## Restore

Read the archived v1 prd/spec from a new temporary restore root if the per-host/python direction is ever revisited. Do not overwrite the current task root.

## Read This Version When

You need the pre-review per-host/python hook design that preceded the `obra/superpowers/hooks` flat layout.
