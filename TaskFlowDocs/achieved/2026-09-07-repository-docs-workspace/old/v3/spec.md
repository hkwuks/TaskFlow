# Spec — Task selection, maintenance, and repository documents
> Task version: v3

## Existing-task-first decision

| Condition | Action |
| --- | --- |
| Advances an active task's deliverable or planned step | Maintain that task |
| Resolves its open question, verification, or follow-up | Maintain that task |
| Materially changes the same deliverable | Version the existing task, re-approve |
| Independently releasable outcome **and** independent acceptance | Create a related task |
| Different owner/accountability | Create a related task |
| Mixed request | Propose split; ask user before creating a second task |

On every existing-task continuation, read current PRD, Spec if present, Plan, applicable repository documents, and latest verification/checklist state. Update Plan progress and verification after meaningful work. New session is never a new-task trigger.

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
