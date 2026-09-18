# Todo inbox

This is the repository's single lightweight intake list. It stores triage metadata only. After promotion, the linked TaskFlow directory is the sole source of requirements, design, plan, and verification facts.

## Status flow

`inbox → clarified → promoted → in_progress → done/cancelled`

## Items

<!-- Add new items at the top using the template below. -->

## Record the host SessionStart session_id in the active task's sessions.md

- ID: TF-20260914-02
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-14
- Updated: 2026-09-14
- Goal: Record the host SessionStart session_id in the active task's sessions.md so a cross-session resume has a real, platform-specific identifier.
- Task: `TaskFlowDocs/achieved/2026-09-14-session-id-record/`
- Next action: None — completed and archived.

## State in the Skill that personal supplements are local-only

- ID: TF-20260914-03
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-14
- Updated: 2026-09-14
- Goal: State in the Skill that personal supplements are local-only and must not be committed to Git, and align this repository with that boundary.
- Task: `TaskFlowDocs/achieved/2026-09-14-personal-docs-git-boundary/`
- Next action: None — completed and archived.

## TF-20260913-03 — Pin stable marketplace installs to released revisions
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- External: None
- Goal: Keep the marketplace catalog on `main` while pinning stable TaskFlow plugin installs to the immutable `v1.0.4` release commit.
- Task: `TaskFlowDocs/achieved/2026-09-13-pin-marketplace-release/`
- Next action: None — completed and archived.
- Updated: 2026-09-13

## TF-20260911-02 — Allow appropriate tools to contribute to task documents
- Status: done
- Priority: normal
- Owner: Codex
- Source: historical TaskFlow task
- External: None
- Goal: Allow relevant tools and capabilities to contribute to task documents without forcing a tool chain.
- Task: `TaskFlowDocs/achieved/2026-09-07-tool-participation/`
- Next action: None — completed and archived.
- Updated: 2026-09-11

## TF-20260911-03 — Audit further Hook automation opportunities
- Status: done
- Priority: normal
- Owner: Codex
- Source: historical TaskFlow task
- External: None
- Goal: Audit additional Hook automation opportunities while preserving approval and mutation boundaries.
- Task: `TaskFlowDocs/achieved/2026-09-10-audit-hook-opportunities/`
- Next action: None — completed and archived; recommendations require separate approved tasks.
- Updated: 2026-09-11

## TF-20260911-04 — Consolidate the packaged Skill layout
- Status: done
- Priority: normal
- Owner: Codex
- Source: historical TaskFlow task
- External: None
- Goal: Consolidate the packaged Skill layout and remove stale duplicate entrypoints.
- Task: `TaskFlowDocs/achieved/2026-09-10-consolidate-skill-layout/`
- Next action: None — completed and archived.
- Updated: 2026-09-11

## TF-20260911-05 — Copy-first Task versioning
- Status: done
- Priority: high
- Owner: Codex
- Source: historical TaskFlow task
- External: None
- Goal: Preserve superseded Task documents while retaining current roots during version transitions.
- Task: `TaskFlowDocs/achieved/2026-09-10-copy-first-versioning/`
- Next action: None — completed and archived.
- Updated: 2026-09-11

## TF-20260911-06 — Limit TaskFlow to development requests
- Status: done
- Priority: normal
- Owner: Codex
- Source: historical TaskFlow task
- External: None
- Goal: Restrict automatic TaskFlow intake to development requests while preserving explicit opt-in.
- Task: `TaskFlowDocs/achieved/2026-09-10-limit-taskflow-scope/`
- Next action: None — completed and archived.
- Updated: 2026-09-11

## TF-20260911-07 — Unblock autonomous capability invocation
- Status: done
- Priority: normal
- Owner: Codex
- Source: historical TaskFlow task
- External: None
- Goal: Make capability selection, invocation, review, and recording explicit without forcing a provider or tool.
- Task: `TaskFlowDocs/achieved/2026-09-10-unblock-capability-invocation/`
- Next action: None — completed and archived.
- Updated: 2026-09-11

## TF-20260911-08 — Update and review TaskFlow plugin
- Status: done
- Priority: high
- Owner: Codex
- Source: historical TaskFlow task
- External: None
- Goal: Fix, publish, install, and verify the TaskFlow plugin and Windows Hook behavior.
- Task: `TaskFlowDocs/achieved/2026-09-10-update-review-plugin/`
- Next action: None — completed and archived.
- Updated: 2026-09-11

## T-20260910-001 — Enforce repository-governed fork development
- Status: done
- Priority: high
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Make the TaskFlow plugin follow fork/upstream development discipline and applicable repository, personal-supplement, code-style, contributing, and roadmap documents, creating missing governance documents with the user when needed.
- Task: `TaskFlowDocs/achieved/2026-09-10-repository-governed-development/`
- Next: None — completed and archived.
- Updated: 2026-09-11

## TF-20260910-08 — Reduce TaskFlow token use with lifecycle scripts
- Status: done
- Priority: high
- Owner: Codex
- Source: user request
- External: None
- Goal: Replace repetitive Agent reads and Markdown rewrites with bounded lifecycle commands where automation saves tokens.
- Task: `TaskFlowDocs/achieved/2026-09-10-token-saving-lifecycle-scripts/`
- Next: User acceptance after verified Windows full-lifecycle compatibility; archive only after explicit authorization.
- Updated: 2026-09-11

## T-20260909-002 — Restructure TaskFlow as repo-root plugin (superpowers-style)
- Status: done
- Priority: normal
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Restructure so the repo root is the plugin root (like superpowers/agent-skills): SKILL.md, hooks/, references/, agents/, and the plugin manifests move up out of the `taskflow/` subdir; marketplace `source` becomes `./`; skill loads with the plugin, no manual copy.
- Task: None — direct restructure in repo root (uncommitted; user said don't commit yet)
- Next: None — repo-root plugin validated (`claude plugin validate . --strict` PASS), locally installed from the working tree, hooks end-to-end tested (all PASS), full smoke-test suite PASS.
- Updated: 2026-09-09

## T-20260909-001 — Package TaskFlow as installable plugin (marketplace, Claude + Codex)
- Status: done
- Priority: normal
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Let users install TaskFlow by command (`claude plugin marketplace add + install`; `codex plugin add`) instead of copying skills/hooks config, following how superpowers ships per-host manifests.
- Task: None — direct change; first iteration added `.claude-plugin/` + `.codex-plugin/` under `taskflow/`, then superseded by T-20260909-002 (repo-root plugin)
- Next: None — superseded by T-20260909-002; install commands verified end-to-end on both Claude Code (`✔ enabled`) and Codex CLI (`installed, enabled`).
- Updated: 2026-09-09

## T-20260908-007 — Support host/harness hooks in TaskFlow (reverse non-runtime boundary)
- Status: done
- Priority: normal
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Allow TaskFlow to coordinate with host/harness hooks (Claude Code and Codex) via a flat `hooks/` of extensionless bash scripts + per-host JSON + `run-hook.cmd`, plus a SessionStart context summary, without automation writing core documents or skipping approval.
- Task: `TaskFlowDocs/achieved/2026-09-08-runtime-hooks/`
- Next: None — v2 completed, verified (smoke + mirror), and archived.
- Updated: 2026-09-08
- Updated: 2026-09-08
- Updated: 2026-09-08

## T-20260908-006 — Reduce TaskFlow workflow token cost
- Status: done
- Priority: high
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Reduce Agent token consumption in the TaskFlow workflow while preserving traceability and reliability.
- Task: `TaskFlowDocs/achieved/2026-09-08-token-efficiency/`
- Next: None — completed, verified, and archived.
- Updated: 2026-09-08
- Updated: 2026-09-08

## T-20260908-003 — Archive completed legacy TaskFlow tasks
- Status: done
- Priority: high
- Owner: user / TaskFlow
- Source: user-approved audit repair
- External: None
- Goal: Add Todo traceability and archive the completed standards-root and Todo-promotion tasks.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/`
- Next: None — completed and archived.
- Updated: 2026-09-08

## T-20260908-004 — Repository standards and TaskFlowDocs root
- Status: done
- Priority: normal
- Owner: user / TaskFlow
- Source: historical TaskFlow task
- External: None
- Goal: Preserve the completed repository-standards and TaskFlowDocs-root design as achieved history.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-standards-and-doc-root/`
- Next: None — completed and archived.
- Updated: 2026-09-08

## T-20260908-005 — Todo intake and promotion workflow
- Status: done
- Priority: normal
- Owner: user / TaskFlow
- Source: historical TaskFlow task
- External: None
- Goal: Preserve the completed Todo intake and promotion design as achieved history.
- Task: `TaskFlowDocs/achieved/2026-09-07-todo-intake-and-promotion/`
- Next: None — completed and archived.
- Updated: 2026-09-08

## T-20260908-002 — Repair TaskFlow activation and archival consistency
- Status: done
- Priority: high
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Ensure TaskFlow applies to every repository work request and keeps task, Todo, and achieved locations consistent.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/`
- Next: None — completed and archived.
- Updated: 2026-09-08

## T-20260908-001 — Todo-first intake and achieved-task retrieval
- Status: done
- Priority: high
- Owner: user / TaskFlow
- Source: user request
- External: None
- Goal: Make Todo mandatory for every direct or imported requirement and retrieve achieved tasks before material maintenance.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/`
- Next: None — completed and archived.
- Updated: 2026-09-08

## Item template

```markdown
## T-YYYYMMDD-001 — Short title
- Status: inbox | clarified | promoted | in_progress | done | cancelled
- Priority: low | normal | high | urgent
- Owner: <person or Agent>
- Source: <user / review / issue / remote>
- External: <issue number / URL / None>
- Goal: <one sentence>
- Task: <TaskFlowDocs/<task-id>/ or None>
- Next: <single next clarification or implementation action>
- Updated: YYYY-MM-DD
```

Every direct request or imported requireme

## Make repository-docs index the primary routing record and maintain/inject it thr

- ID: TF-20260911-01
- Status: done
- Priority: normal
- Owner: Codex
- Source: direct user request
- Added: 2026-09-11
- Updated: 2026-09-11
- Goal: Make repository-docs index the primary routing record and maintain/inject it through SessionStart hook
- Task: `TaskFlowDocs/achieved/2026-09-11-index-hook-routing/`
- Next action: None — completed and archived.

## Identify the current TaskFlow task before phase routing

- ID: TF-20260911-02
- Status: done
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-11
- Updated: 2026-09-12
- Goal: Identify the current TaskFlow task before phase routing
- Task: `TaskFlowDocs/achieved/2026-09-12-current-task-routing/`
- Next action: None — completed and archived.

## Add explicit cross-platform runtime preflight for Windows Python dependencies

- ID: TF-20260911-03
- Status: done
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-11
- Updated: 2026-09-12
- Goal: Add explicit cross-platform runtime preflight for Windows Python dependencies
- Task: `TaskFlowDocs/achieved/2026-09-12-windows-runtime-preflight/`
- Next action: None — completed and archived.

## Harden the Windows hook launcher argument forwarding and failure reporting

- ID: TF-20260911-04
- Status: done
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-11
- Updated: 2026-09-12
- Goal: Harden the Windows hook launcher argument forwarding and failure reporting
- Task: `TaskFlowDocs/achieved/2026-09-12-windows-launcher/`
- Next action: None — completed and archived.

## Validate repository-document index paths and protect concurrent writes

- ID: TF-20260911-05
- Status: done
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-11
- Updated: 2026-09-13
- Goal: Validate repository-document index paths and protect concurrent writes
- Task: `TaskFlowDocs/achieved/2026-09-13-index-safety/`
- Next action: None — completed and archived.

## Add Linux and Windows CI coverage for TaskFlow hooks

- ID: TF-20260911-06
- Status: done
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-11
- Updated: 2026-09-13
- Goal: Add Linux and Windows CI coverage for TaskFlow hooks
- Task: `TaskFlowDocs/achieved/2026-09-13-hooks-ci-matrix/`
- Next action: None — completed and archived.

## Reduce SessionStart context output to the active task by default

- ID: TF-20260911-07
- Status: done
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-11
- Updated: 2026-09-13
- Goal: Reduce SessionStart context output to the active task by default
- Task: `TaskFlowDocs/achieved/2026-09-13-session-context/`
- Next action: None — completed and archived.

## Model optional repository documents and consume SessionStart event input

- ID: TF-20260911-08
- Status: done
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-11
- Updated: 2026-09-13
- Goal: Model optional repository documents and consume SessionStart event input
- Task: `TaskFlowDocs/achieved/2026-09-13-event-aware-docs/`
- Next action: None — completed and archived.

## Prepare TaskFlow v1.0.4 release

- ID: TF-20260913-02
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-13
- Updated: 2026-09-13
- Goal: Prepare TaskFlow v1.0.4 release
- Task: `TaskFlowDocs/achieved/2026-09-13-release-v1-0-4/`
- Next action: None — completed and archived.

## Revise release flow to support direct tag releases

- ID: TF-20260913-01
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-13
- Updated: 2026-09-13
- Goal: Revise release flow to support direct tag releases
- Task: `TaskFlowDocs/achieved/2026-09-13-revise-release-flow/`
- Next action: None — completed and archived.

## Restore macOS portability for hooks and smoke tests

- ID: TF-20260914-01
- Status: done
- Priority: normal
- Owner: external contributor
- Source: external code review (fork pull request)
- Added: 2026-09-14
- Updated: 2026-09-14
- Goal: Make the hooks and smoke tests pass on stock macOS (bash 3.2 + BSD sed), cover macOS and the evals in CI, and align plugin license metadata with the AGPL-3.0 LICENSE.
- Task: `TaskFlowDocs/achieved/2026-09-14-macos-hook-portability/`
- Next action: None — completed and archived.

## Map TaskFlow phases to the concept class each one corresponds to in external wor

- ID: TF-20260915-01
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-15
- Updated: 2026-09-15
- Goal: Map TaskFlow phases to the concept class each one corresponds to in external workflows, so PRD/Spec/Plan work selects the right capability instead of working unaided.
- Task: `TaskFlowDocs/achieved/2026-09-15-phase-concept-mapping/`
- Next action: None — completed and archived.

## Stop tracking TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md: the workflow draft is not

- ID: TF-20260914-05
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-14
- Updated: 2026-09-14
- Goal: Stop tracking TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md: the workflow draft is not part of the TaskFlowDocs artifact system.
- Task: `TaskFlowDocs/achieved/2026-09-14-untrack-workflow-draft/`
- Next action: None — completed and archived.

## Require a short-lived branch or dedicated worktree before implementation starts,

- ID: TF-20260914-04
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-14
- Updated: 2026-09-14
- Goal: Require a short-lived branch or dedicated worktree before implementation starts, and route contribution rules to the design phase.
- Task: `TaskFlowDocs/achieved/2026-09-14-branch-and-worktree-gate/`
- Next action: None — completed and archived.

## Run TaskFlow hooks without a Python interpreter

- ID: TF-20260915-82ec4c
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-15
- Updated: 2026-09-17
- Goal: Run TaskFlow hooks without a Python interpreter
- Task: `TaskFlowDocs/achieved/2026-09-15-no-python-hooks/`
- Next action: None — completed and archived.

## Make concurrent Todo updates merge cleanly in parallel-task branches

- ID: TF-20260915-02
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-15
- Updated: 2026-09-15
- Goal: Make concurrent Todo updates merge cleanly in parallel-task branches
- Task: `TaskFlowDocs/achieved/2026-09-15-todo-merge-driver/`
- Next action: None — completed and archived.

## Fix hook integrity so archived versions are never polluted, unimplemented work c

- ID: TF-20260915-0f6dda
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-15
- Updated: 2026-09-15
- Goal: Fix hook integrity so archived versions are never polluted, unimplemented work cannot pass the approval gates, and task documents follow the user's language
- Task: `TaskFlowDocs/achieved/2026-09-15-hook-integrity/`
- Next action: Awaiting user acceptance of the implemented change; this task's Step 1 also shipped as PR #24 and Steps 2/3 as PR #25, both merged.

## Publish TaskFlow v1.0.5 with the no-runtime hooks, the Todo merge driver, and th

- ID: TF-20260915-a9cabf
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-15
- Updated: 2026-09-15
- Goal: Publish TaskFlow v1.0.5 with the no-runtime hooks, the Todo merge driver, and the hook-integrity fixes
- Task: `TaskFlowDocs/achieved/2026-09-15-release-v1-0-5/`
- Next action: None — completed and archived.

## Cut the mechanical overhead out of a release: one version-consistency check, a r

- ID: TF-20260915-1f0f66
- Status: done
- Priority: normal
- Owner: Codex
- Source: local fixture
- Added: 2026-09-15
- Updated: 2026-09-15
- Goal: Cut the mechanical overhead out of a release: one version-consistency check, a release document rule, and an archive that clears the Todo next action.
- Task: `TaskFlowDocs/achieved/2026-09-15-release-friction/`
- Next action: None — completed and archived.

## Detect a Todo entry that a merge dropped, so a silent loss cannot reach main unn

- ID: TF-20260916-2561e8
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-16
- Updated: 2026-09-16
- Goal: Detect a Todo entry that a merge dropped, so a silent loss cannot reach main unnoticed.
- Task: `TaskFlowDocs/achieved/2026-09-16-todo-entry-loss-detection/`
- Next action: None — completed and archived.

## Hold Todo protection on the web-UI merge path

- ID: TF-20260916-2a89e2
- Status: done
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-16
- Updated: 2026-09-17
- Goal: Make the Todo merge protection hold on the path where merges actually happen: a hosting web-UI pull-request merge.
- Task: `TaskFlowDocs/achieved/2026-09-16-web-ui-merge-loss-guard/`
- Next action: None — completed and archived.

## Repair the duplicate Todo ID that the old counter-derived scheme shipped: two li

- ID: TF-20260916-01bd1a
- Status: done
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-16
- Updated: 2026-09-17
- Goal: Repair the duplicate Todo ID that the old counter-derived scheme shipped: two live entries both carry TF-20260915-01, so an ID lookup can resolve to the wrong task.
- Task: `TaskFlowDocs/achieved/2026-09-16-duplicate-todo-id/`
- Next action: None — completed and archived.

## Isolate a task before its documents are written, and make the choice auditable

- ID: TF-20260916-ab381b
- Status: done
- Priority: normal
- Owner: Codex
- Source: user review
- Added: 2026-09-16
- Updated: 2026-09-17
- Goal: Isolate a task before its documents are written, and make the choice auditable: task documents are created in Phase 1 while the branch/worktree rule only applied from Phase 5, so documents landed in a shared checkout (usually another task's branch) and could not be checked out away; separately, the Plan's capability-selection section was marked optional, so "chose not to invoke" and "forgot the step" were indistinguishable.
- Task: `TaskFlowDocs/achieved/2026-09-16-capability-selection-enforcement/`
- Next action: None — completed and archived.

## Detect a task directory that no Todo entry references

- ID: TF-20260916-a357ee
- Status: inbox
- Priority: normal
- Owner: Codex
- Source: user review
- Added: 2026-09-16
- Updated: 2026-09-16
- Goal: Detect a task directory that no Todo entry references, so a lost Todo record cannot leave orphaned task documents behind.
- Task: Not promoted.
- Next action: Clarify whether this belongs in the existing `hooks/todo-check` or is a separate check; then promote.
- Notes: 发现于 2026-09-16 —— 提交 PR #28 时为让提交只含任务 A 而摘掉 B/C/D 的 Todo 条目，随后一次 `git checkout -- TaskFlowDocs/todo.md` 把工作区文件整体回退，三条条目一度丢失（同日已按原样补回），而三个任务目录始终在 `TaskFlowDocs/` 下，形成「目录存在、无 Todo 指向」的孤儿态（仅工作区，未进入任何提交）。同一形态在历史里也有一例：`TaskFlowDocs/achieved/2026-09-10-repository-document-placement/`，全部历史中从未有过对应的 Todo 条目。目前该缺口无自动检查兜住。注意：只查「任务目录 → Todo」这一个方向；反方向（Todo 条目指向不存在的目录）本轮已实测为空。2026-09-16 追问：本条与 `TF-20260916-ab381b` 是同一根因的两个方向——孤儿目录是「文档先于隔离产生」的结果，`ab381b` 修根因并在 `hooks/repository-check` 里报告错位产物；本条仍是更广的历史审计（含已提交、已归档的目录），是否仍要独立成检查待定。

## Publish TaskFlow v1.0.6 with the CodeBuddy host, the Todo merge-drop audit, and the release version check

- ID: TF-20260917-b7bc40
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-17
- Updated: 2026-09-17
- Goal: Publish TaskFlow v1.0.6 with the CodeBuddy host, the Todo merge-drop audit, and the release version check
- Task: `TaskFlowDocs/achieved/2026-09-17-release-v1-0-6/`
- Next action: None — completed and archived.

## Make the release atomic: push the marketplace pin and the release tag in one ato

- ID: TF-20260917-a608b7
- Status: in_progress
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-17
- Updated: 2026-09-17
- Goal: Make the release atomic: push the marketplace pin and the release tag in one atomic push so the catalog never names a tag that is missing or stale
- Task: `TaskFlowDocs/2026-09-17-atomic-release-push/`
- Next action: Complete PRD / Spec / Plan and request approval.

## Refresh both READMEs so they document the shipped surfaces: the hooks/tools/eval

- ID: TF-20260918-13ff42
- Status: in_progress
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-18
- Updated: 2026-09-18
- Goal: Refresh both READMEs so they document the shipped surfaces: the hooks/tools/evals trees, the verification and CI checks, and the release process link
- Task: `TaskFlowDocs/2026-09-18-readme-refresh/`
- Next action: Complete PRD / Spec / Plan and request approval.
