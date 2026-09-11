# Repository standards and TaskFlowDocs root
> Task version: v3
> Status: completed

## Goal

Give each repository a discoverable place for code, commit, design, and development-process rules, while making `TaskFlowDocs/` the single default root for TaskFlow artifacts. When rules are absent or inadequate, TaskFlow must guide the user to define them before implementation. When work targets a Git remote or pull request, let the Agent discover and incorporate repository-host PR rules into the same standards index.

## Background / Confirmed Facts

- The Skill and both READMEs currently use `tasks/` as the default root.
- This repository has no runtime implementation or provider-specific remote integration.
- The user approved a local standards index, optional standards files, remote PR-rule synchronization, and a complete `tasks` to `TaskFlowDocs` migration without compatibility aliases.
- The user found that v1 only discovered existing standards and did not guide creation of missing standards.
- The user identified that the v1 task was extended after completion without a Task-version transition.
- The user identified that a material requirement correction did not automatically trigger document synchronization and version transition.

## Requirements

1. Replace every documented TaskFlow path rooted at `tasks/` with `TaskFlowDocs/`.
2. Define `TaskFlowDocs/standards/index.md` as the required repository standards entry point.
3. Permit standards to be split into optional files such as code, commits, design, and development-process rules; only files linked as applicable need to exist.
4. Require the Agent to inspect the standards index before planning or implementing a non-trivial task and record applicable standards in `plan.md`.
5. Define remote PR-rule synchronization as a discovery step: inspect the configured Git remote and repository-host files/templates/workflows, then route reviewed conclusions into the local standards index or a linked note. Do not require provider APIs or silently overwrite local rules.
6. Update examples, archive paths, references, and workflow diagram labels consistently.
7. When an applicable standard is missing, incomplete, or not explicitly waived, require the Agent to guide the user to define it before implementation. Ask at most three dependency-ordered questions per turn and provide a recommendation for each.
8. Create only user-confirmed standard files and link them from `index.md`; every created file must state scope, rules, verification, and exceptions/change control. `commits.md` must additionally state commit format and PR checks.
9. Treat a material standards-contract change as a Task-version change: archive the prior version, update core documents atomically, return to `ready`, and obtain approval before implementation.
10. When a user corrects, rejects, adds to, or materially changes an approved requirement, design, standard, or scope, trigger archive, core-document synchronization, and re-approval before continuing.

## Acceptance Criteria

- No active documentation or Skill instruction presents `tasks/` as the default TaskFlow root.
- `TaskFlowDocs/standards/index.md` is documented as the standards entry point and gives applicability and precedence rules.
- The Skill describes local standards discovery and optional remote PR-rule synchronization, including review-before-incorporation and no-secret requirements.
- Both READMEs explain the new root and standards mechanism in their respective languages.
- All changed Markdown and SVG references are internally consistent.
- The Skill explicitly distinguishes: load existing rules, bootstrap missing rules with the user, and proceed only after standards are defined or explicitly waived.
- The v1 task state is recoverable under `old/v1/`, and v2 records this change and approval.
- The Skill and workflow draft explicitly describe how a user's material change triggers archive, synchronized document updates, and a new approval gate.

## In Scope

- Skill instructions, artifact references, versioning references, README files, and workflow diagram text.
- A minimal standards index template, standards-bootstrap guidance, and remote synchronization guidance.

## Out of Scope

- A provider-specific API client, webhook, CLI, or background synchronizer.
- Automatically creating or updating remote repository settings.
- Migrating external repositories or existing user task directories.

## Risks / Deferred Items

- Remote provider APIs and permissions vary; synchronization remains agent-assisted discovery until a provider integration is explicitly requested.
- Existing repositories using `tasks/` need a separate, user-authorized migration.

## Open Questions

- None blocking. The user approved the v2 behavior in the request that raised the omission.

## Version History

- v1 — initial approved scope: standards mechanism, remote PR-rule discovery, and complete documentation-root migration; superseded because missing standards bootstrap and version-transition enforcement.
- v2 — adds user-guided standards bootstrap and explicitly follows the Task-version transition; superseded because the user-change trigger was still implicit.
- v3 — adds an explicit user-change trigger and synchronization protocol.
