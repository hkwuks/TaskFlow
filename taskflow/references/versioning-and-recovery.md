# Task versioning and recovery

Read this reference when a design/requirement boundary changes, when design documents are not stored in Git, or when an old proposal must be inspected or restored.

## Version levels

- **Work revision:** typo, link, checkbox, progress, test result, or evidence that does not change a decision. Keep the current Task version.
- **Task version:** a material change to goal, scope, acceptance, architecture, contract, compatibility, risk decision, or implementation path. Increment `vN` and archive the superseded version.
- **Git history:** mechanical history within a Task version. It is not a replacement for the semantic Task version.

`plan.md` owns the Task version; existing `prd.md` and `spec.md` repeat it for readability. A small task without `spec.md` does not create one just for synchronization. Work revisions should update `Last updated` and, when useful, append a line to Plan's change log without incrementing the Task version.

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

1. The first superseded version gets a complete `old/v1/snapshot/`.
2. Later superseded versions get an adjacent unified patch, named `changes/from-v<base>-to-vN.patch`.
3. Every patch states source version, target version, base path, creation time, restore root, apply order, and verification method.
4. Create another full snapshot at an important milestone, after roughly five logical versions, or when the patch chain is costly to recover.
5. Patch only task-maintained Markdown (`prd.md`, `spec.md`, `plan.md`, and team notes/indexes under `reference/`). Do not rewrite or patch external PDFs, web captures, images, archives, or binaries.

Apply patches only in a new temporary restore root. Verify with `diff --exit-code` or an equivalent comparison and, when available, checksums. Never restore an old version by overwriting the current task directory.

## Atomic version transition

Treat a Task version change as one operation:

1. Capture the old version's status and archive metadata.
2. Write `old/vN/` and its snapshot/patch.
3. Update every existing core document to `vN+1` in one pass; absent optional documents remain absent.
4. Update `plan.md` state and Version History.
5. Check that all existing core documents agree on the new version.
6. Return to `ready` and obtain user approval before implementation.

If interrupted, retain the old version and mark the task `blocked`; do not leave mixed `v1`/`v2` documents.

## Safe completion and reopening

Before moving a task to `TaskFlowDocs/achieved/`, confirm no agent is writing core documents, external references are known, and the move is authorized. The achieved directory is read-only history. Create a new related task only for a new independently releasable outcome with independent acceptance criteria, or different owner/accountability; reopening an incomplete task requires user confirmation and a `reopen` reason in `plan.md`.

After moving the directory, update known cross-task references and the task artifact path in `sessions.md`. Keep the code working directory separate from the task artifact directory because only the latter changes during archive.
