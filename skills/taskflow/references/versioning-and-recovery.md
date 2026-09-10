# Task versioning and recovery

Read this reference when a design/requirement boundary changes, when design documents are not stored in Git, or when an old proposal must be inspected or restored.

## Version levels

- **Work revision:** wording, an implementation approach within the approved design, progress, a checklist or verification-result update, or any other change that does not alter an approved goal, requirement, acceptance criterion, scope, or contract. Record it in the Plan's change log. Keep the current Task version.
- **Task version:** a material change to an approved goal, scope, acceptance, architecture, interface/data contract, compatibility decision, risk decision, or standard. Increment `vN` and archive the superseded version.
- **Git history:** mechanical history within a Task version. It is not a replacement for the semantic Task version.

The classification decision belongs to `SKILL.md` (User-change trigger and Phase 5 Build). `plan.md` owns the Task version; existing `prd.md` and `spec.md` repeat it for readability. A small task without `spec.md` does not create one just for synchronization. Work revisions should update `Last updated` and append a line to the Plan's change log without incrementing the Task version.

## Supersession order

`old/vN/` means “how to recover the already superseded Task version vN.” The current version remains at the task root.

```text
current v1 → v2: archive v1 in old/v1/, then make root v2
current v2 → v3: archive v2 in old/v2/, then make root v3
```

Create `old/vN/version.md` with:

```markdown
# Archived Version vN — <title>
> Task: YYYY-MM-DD-short-slug
> Version: vN
> Status: superseded
> Created: YYYY-MM-DD HH:mm +08:00
> Archived: YYYY-MM-DD HH:mm +08:00
> Superseded by: vN+1
> Archive mode: git | file
> Restore root: <new temporary directory>

## Change Summary
## Archived Materials
## Restore
## Read This Version When
```

## Git mode

When task documents may be committed, record the exact start and end commits or commit range in `version.md`. Use Git diff/history to inspect mechanical edits. `old/vN/` only needs the semantic archive entry; do not duplicate the repository history.

## File mode

When design documents must not enter Git:

1. The first superseded core document set gets a complete `old/v1/snapshot/` when no other recoverable baseline exists.
2. Later superseded versions get an adjacent unified patch, named `changes/from-v<base>-to-vN.patch`, when their design documents stay out of Git.
3. Every patch states source version, target version, base path, creation time, restore root, apply order, and verification method.
4. Create another full snapshot at an important milestone, after roughly five logical versions, or when the patch chain is costly to recover.
5. Patch only task-maintained Markdown (`prd.md`, `spec.md`, `plan.md`, and team notes/indexes under `reference/`). Do not rewrite or patch external PDFs, web captures, images, archives, or binaries.

In either archive mode, `old/vN/version.md` is the semantic archive entry and always written. When the changed core document is also recoverable from an existing archive or Git, do not duplicate its full content in `old/vN/`; the `version.md` change summary plus the existing baseline is sufficient. Apply patches only in a new temporary restore root. Verify with `diff --exit-code` or an equivalent comparison and, when available, checksums. Never restore an old version by overwriting the current task directory.

## Atomic version transition

Treat a Task version change as one operation. Archive only the core documents whose approved content materially changed, plus `version.md`. Do not copy an unaffected Plan into `old/`; the current `plan.md` remains the baseline and its change log records the transition.

1. Capture the old version's status and archive metadata.
2. Write `old/vN/version.md`.
3. For each core document whose approved content materially changed, copy its prior version into `old/vN/`; do not duplicate unaffected core documents.
4. Update the retained root documents to `vN+1` in one pass; absent optional documents remain absent.
5. Set the root PRD and Plan to `ready`, invalidate the prior Approval record, then let the Agent edit only semantic changes and the `version.md` change summary.
6. Check that all existing core documents agree on the new version.
7. Return to `ready` and obtain user approval before implementation.

Design documents may stay out of Git: file-mode archival remains a valid recovery store. When a prior core document is not recoverable from an existing archive (for example, no baseline snapshot exists and the design must not be committed), keep a full `snapshot/` under `old/vN/`. Apply file-mode patches only in a new temporary restore root and verify with `diff --exit-code` or checksums; never restore by overwriting the current task directory.

If interrupted, retain the old version and mark the task `blocked`; do not leave mixed `v1`/`v2` documents.

## Safe completion and reopening

The archive transaction is defined in `SKILL.md` (Complete and archive); this reference covers recovery and the reopen path. Before reading a full archived document set, stage the retrieval: read `old/vN/version.md` change summaries and the current `plan.md` first, then read the full set only when the current documents or a version summary require it.

The achieved directory is read-only history. When a later Todo item belongs to an achieved deliverable, move the complete directory back to `TaskFlowDocs/<task-id>/` and follow the `SKILL.md` reopen path (record the Todo source/reopen reason, then the atomic version transition and approval gate) before changing it. Create a new related task only for a new independently releasable outcome with independent acceptance criteria, or different owner/accountability.

After moving the directory, update known cross-task references and the task artifact path in `sessions.md`. Keep the code working directory separate from the task artifact directory because only the latter changes during archive.
