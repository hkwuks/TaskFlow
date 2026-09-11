# Task selection, maintenance, and repository documents
> Task version: v4
> Status: completed

## Goal

Redesign TaskFlow so every requirement first enters the Todo inbox, completed tasks live in `TaskFlowDocs/achieved/`, and later requests that belong to an achieved task retrieve and version that task before its documents change.

## Confirmed Facts

- Current new-task wording treats changes to goal, deliverable, or ownership boundary as a new task too broadly.
- Existing task maintenance is not sufficiently enforced at task intake and resumption.
- `repository-docs/standards/` preserves a separate standards layer contrary to the user's requested single document environment.
- User confirmed on 2026-09-08: an independently releasable outcome **and** independent acceptance criteria are both required for a related task unless ownership/accountability differs; mixed requests require a proposed split and user choice; personal supplements apply only when their scope matches.
- User requires that every requested item, whether directly stated, imported from GitHub Issues, or received from another source, is first created or updated in `TaskFlowDocs/todo.md`; bulk imports must maintain a distinct Todo item for every imported requirement.
- User requires completed tasks to be moved to `TaskFlowDocs/achieved/`; when a new requirement belongs to an achieved task, TaskFlow must retrieve it before versioning and editing its documents.

## Requirements

1. Before creating a task, search active TaskFlowDocs tasks and classify the request against their goal, deliverable, owner, scope, and acceptance criteria.
2. Maintain the existing task when the request advances its approved deliverable, resolves an open question, implements or verifies a planned step, or makes a material revision of the same deliverable; use Task versioning and re-approval when required.
3. Create a new task only when the request has both an independently releasable deliverable and independent acceptance criteria, or has different owner/accountability. Record a related-task link.
4. Existing tasks must be read and updated before work: confirm status, current version, approval, next step, checklist, relevant repository documents, and verification record. Do not create a parallel task merely because a session is new.
5. Replace the separate `repository-docs/standards/` layer with one repository-documents catalog that classifies entries as repository rule, repository guidance, or personal supplement.
6. Repository rules are authoritative. Personal supplements may be created only in `repository-docs/personal/`, must declare their scope and source, and cannot weaken, override, or conflict with repository rules. If conflict is detected, stop and ask the user.
7. If a repository lacks needed rules, guide the user to add a personal supplement or, with explicit authorization, a repository rule source; do not fabricate repository-owned policy.
8. Record every work request in the Todo inbox before task matching, clarification, promotion, implementation, or import-specific processing. Preserve source and external identifier/link where available.
9. Batch imports must deduplicate by source and external identifier, then create or update one Todo item per imported requirement before any item can be promoted. A batch is an intake convenience, not a task or requirements source.
10. On completion, move the whole task directory to `TaskFlowDocs/achieved/<task-id>/`. When a new requirement is classified as a material change to an achieved deliverable, move that directory back to the active TaskFlowDocs root, record the reopen reason, create a new Task version, and obtain approval before changing implementation.

## Acceptance Criteria

- The Skill provides an explicit existing-task-first decision table and mandatory maintenance checks.
- New-task creation has a higher, outcome-based threshold and requires related-task linkage where applicable.
- No active `standards/` path remains; repository documents have one catalog and personal supplements have a defined location and precedence.
- The Skill prevents personal supplements from overriding repository guidance.
- Every direct or imported requirement is traceable to a Todo item before task handling; batch imports preserve one item per source requirement.
- Completed tasks are in `achieved/`, and an achieved task is retrieved, versioned, and re-approved rather than edited in place.

## Confirmed Decisions

- Require both independent acceptance criteria and an independently releasable outcome for a related task, unless ownership/accountability differs.
- For mixed requests, propose the boundary and ask the user before creating another task.
- Apply a personal supplement only when its declared scope matches the task.
- Treat every work request and import as Todo-first; preserve each imported requirement individually during bulk intake.
- Retrieve an achieved task to the active root before modifying a requirement that belongs to it; do not edit achieved history in place.

## Version History

- v1 — directory-centric approach; superseded.
- v2 — repository document behavior; superseded for incomplete task selection and separate standards layer.
- v3 — existing-task-first and unified repository-documents model.
- v4 — Todo-first intake and achieved-task retrieval.
