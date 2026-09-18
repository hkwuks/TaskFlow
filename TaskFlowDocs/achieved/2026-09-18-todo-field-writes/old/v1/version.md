# Archived Version v1 — Plan — Move the deterministic Todo field writes into hooks/task
> Task: 2026-09-18-todo-field-writes
> Version: v1
> Status: superseded
> Archived: 2026-09-18 22:38 +0800
> Superseded by: v2
> Archive mode: file

## Change Summary
(Agent: summarize what changed between v1 and v2.)

## Archived Materials
- prd.md
- plan.md

## Restore
Read the archived v1 core docs from a new temporary restore root. Do not overwrite the current task root.

## Correction (recorded 2026-09-18, after this archive was cut)

This archive was made with `hooks/version`, which copies the core documents as
they stand in the working tree. The v1 documents had **already been staged** for
an intended v1 commit, so `git diff` was quiet and the "commit the superseded
version first" guard did not fire — but neither prd.md nor plan.md had a commit
to be read from, so what is archived here is not v1 as it was written.

Concretely: v1/plan.md carries the Step 1-3 verification notes and status updates
made after v2's scope was decided, and v1/prd.md carries the v2 range note. The
accurate v1 documents are the ones this repository's history will show when the
v1 work is committed, not these copies.

Nothing is lost — the superseded facts (no `task get`, no follow-up promotion,
write-side scope only) are in the archived documents' own listed omissions and in
the v2 `## Version History` entry. But a reader should not trust this directory as
a byte-exact v1 snapshot.

This is a limitation of `hooks/version`'s file-mode default, not of this task:
it has no baseline to copy from for an uncommitted document. Filed for follow-up
in the v2 Plan.
