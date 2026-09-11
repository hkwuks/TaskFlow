# Spec — Task selection, maintenance, and repository documents
> Task version: v4

## Existing-task-first decision

| Condition | Action |
| --- | --- |
| Advances an active task's deliverable or planned step | Maintain that task |
| Resolves its open question, verification, or follow-up | Maintain that task |
| Materially changes the same deliverable | Version the existing task, re-approve |
| Independently releasable outcome **and** independent acceptance | Create a related task |
| Different owner/accountability | Create a related task |
| Mixed request | Propose split; ask user before creating a second task |

Every request first creates or updates a Todo item. Task selection then searches active tasks and achieved tasks. On every existing-task continuation, read current PRD, Spec if present, Plan, applicable repository documents, and latest verification/checklist state. Update Plan progress and verification after meaningful work. New session is never a new-task trigger.

## Todo-first intake and achieved retrieval

```text
direct request / GitHub Issue / other source
  → create or update one Todo item per requirement
  → deduplicate and clarify
  → match active task or achieved task
  → promote / maintain / retrieve-and-version
  → complete → TaskFlowDocs/achieved/<task-id>/
```

Todo is the sole intake record, not a duplicate PRD or Plan. A Todo item retains source, external identifier or link when available, task link, state, and next action. For a batch import, each source requirement has its own Todo item; the import batch may be recorded as source metadata only.

An achieved task is immutable in its achieved location. If a new request belongs to its deliverable, move the complete directory back to `TaskFlowDocs/<task-id>/`, record the reopen reason and source Todo item, archive the prior Task version, make the new version `ready`, and obtain approval before implementation. After the revised task passes completion checks, move the entire directory back to `achieved/`.

## Unified repository document model

```text
TaskFlowDocs/repository-docs/
├── index.md
├── personal/
│   └── <topic>.md
└── links or indexed source paths
```

Each index entry has a class: `repository-rule`, `repository-guidance`, or `personal-supplement`. Source repository documents are authoritative over personal supplements. A personal supplement declares scope, source documents checked, rules, verification, and exceptions/change control. It applies only when its scope matches the task and may add stricter or orthogonal practices, never conflict with or relax repository rules.

## Missing-rule behavior

When a task needs a rule not supplied by the repository, guide the user to create a scoped personal supplement. Creating or changing a repository-owned document needs explicit user authorization. A detected conflict pauses the task for user resolution.
