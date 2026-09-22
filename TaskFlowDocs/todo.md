# Todo inbox

This is the repository's single lightweight intake list. It stores triage metadata only. After promotion, the linked TaskFlow directory is the sole source of requirements, design, plan, and verification facts.

## Status flow

`inbox → clarified → promoted → in_progress → done/cancelled`

## Items

<!-- Add new items at the top using the template below. -->
## Fix hooks/merge-todo so a Removed record matches its live entry by ID token

- ID: TF-20260918-985164
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-18
- Updated: 2026-09-22
- Goal: Fix hooks/merge-todo so a ## Removed record matches its live entry by ID token and deletion wins, then clear the duplicate IDs that resurrection left in todo.md.
- Task: `TaskFlowDocs/achieved/2026-09-22-merge-todo-removed/`
- Next action: None — completed and archived.
- Notes: **2026-09-19 复核（本条是同一 ID 的另一半，见文件末尾 `## Removed`）**：v1.0.7 已正常发布（tag `v1.0.7` = `c3c536d`），发布事务本身没有问题。真正发生的是**工作区/提交时序错乱**：本条目在 `3f683a5`（10:40）还是活条目，`86a0605`（10:41）被整个删掉，同一分钟 `9406720` 又在 `## Removed` 写下移除记录，声称「v1.0.7 已发布、目录已随 PR #42 删除」——而 PR #42 到 19:35 才合并，发布是 21:21。**移除记录先于它声称的事实写下。** 被删的活条目随后在 19 小时后由合并 `944d833`（`feature/dsh-host` 反向合并 main）复活，于是同一 ID 在文件里出现两次。

  **两处根因（都不在发布流程）**：(1) **闸门被前置改写绕过**——`hooks/task remove` 拒绝删除 `Task:` 不是 `Not promoted.` 的条目，而 `3f683a5` 先把该条目的 `Task:` 改成了 `Not promoted.`，闸门于是放行；「已交付但记录未生」的状态由此可以把一条活条目删掉。(2) **`hooks/merge-todo` 认不出 `## Removed`**——移除记录行以 `- ID: TF-20260918-985164 (removed …)` 开头，而 `key_of` 用 `substr($0, 7)` 取 ID，得到的是 ` TF-20260918-985164 (removed 2026-09-19: …`（整段含括号），与活条目的 key `id:TF-20260918-985164` 不相等。driver 的规则是「key 只在一侧存在就保留该侧」且注释明写 entry 永不被删除，所以被删的活条目被当成「我们加过、他们没动」保留下来。**`## Removed` 记录在 driver 眼里只是一条 ID 不同的新条目**，既不表示删除也不参与匹配。

  **修法方向（未开工）**：让 `key_of` 只取 ID 的首个空白分隔 token，并让 driver 在「某侧有 Removed 记录、另一侧有同名活条目」时按删除处理。**别只修 `task remove` 的闸门**——那只是让删除更难发生，没解决「删了也会被 merge 复活」。


## Windows worktree misjudgement: `hooks/task` reads a `D:/` git dir as relative.

- ID: TF-20260920-9f3c07
- Status: done
- Priority: high
- Owner: unassigned
- Source: user request
- Added: 2026-09-20
- Updated: 2026-09-21
- Goal: Fix the Windows worktree misjudgement so a drive-letter git dir is not read as relative to the root.
- Task: `TaskFlowDocs/achieved/2026-09-20-windows-git-path/`
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
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-17
- Updated: 2026-09-17
- Goal: Make the release atomic: push the marketplace pin and the release tag in one atomic push so the catalog never names a tag that is missing or stale
- Task: `TaskFlowDocs/achieved/2026-09-17-atomic-release-push/`
- Next action: None — completed and archived.

## Refresh both READMEs so they document the shipped surfaces: the hooks/tools/eval

- ID: TF-20260918-13ff42
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-18
- Updated: 2026-09-18
- Goal: Refresh both READMEs so they document the shipped surfaces: the hooks/tools/evals trees, the verification and CI checks, and the release process link
- Task: `TaskFlowDocs/achieved/2026-09-18-readme-refresh/`
- Next action: None — completed and archived.

## The plugin's hook launcher installs without the executable bit, so every Unix Se

- ID: TF-20260918-b0f73a
- Status: done
- Priority: normal
- Owner: Codex
- Source: direct user request
- Added: 2026-09-18
- Updated: 2026-09-18
- Goal: The plugin's hook launcher installs without the executable bit, so every Unix SessionStart hook fails with Permission denied
- Task: `TaskFlowDocs/achieved/2026-09-18-hook-launcher-exec-bit/`
- Next action: None — completed and archived.

## Restore the zh-CN manifest count that a conflict resolution reverted, and rule on conflict-side review

- ID: TF-20260918-ad8348
- Status: done
- Priority: high
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-18
- Updated: 2026-09-18
- Goal: Restore the zh-CN manifest count that a conflict resolution reverted, and decide whether a resolved conflict needs a recorded side-by-side review before it is pushed.
- Task: `TaskFlowDocs/achieved/2026-09-18-conflict-side-review/`
- Next action: None — completed and archived.
- Notes: **2026-09-18 复核（推翻了先前「静默 auto-merge」的说法）**：`46131a1`（"Merge branch 'main' into chore/e-task-isolation-and-capability-record"）那次**确实是真冲突**，不是自动合并——重放三方合并（base `985b269`、ours `adfc5c1`、theirs `c083240`）得到 `git merge-file` exit 1，且 `46131a1` 里存在过冲突块。冲突行两侧都改过同一句：PR #37 把「两个插件 manifest」改成「三个」，PR #38 在同一句里加了「并列出该 checkout 里未提交的任务产物」。**解决时整块取了分支侧**，于是合入结果同时保留了 PR #38 的新句子和 PR #37 已被覆盖的旧计数。时间窗只有 2 分钟：`adfc5c1` 定稿于 20:08:19，PR #37 合并于 20:11:40，`46131a1` 于 20:13:42。窗口和"两侧都读得通"（同是合法中文、同讲一个检查）是它能逃过目视复核的原因。
- **`hooks/todo-check` 覆盖不到这一类**：它是纯 hook、无 LLM，对每个 merge commit 比较两个 parent 各自持有的 `- ID:` 集合与结果的集合（`sed` 提取 + `sort -u` + `comm -13`），只查 `TaskFlowDocs/todo.md` 一个文件的条目级丢失，不做三方比较，因此看不见"解决冲突时取错侧"。它由 `.github/workflows/hooks.yml` 的 `todo-merge-audit` 作业调用（非自动 hook），跑 `git rev-list --merges` 范围内的每个 merge。所以本条不能靠泛化 `todo-check` 解决——「取错侧」这个动作必然伴随一次冲突解决，应该做成"冲突解决后需记录取舍"的流程规则，而非内容比对。
- Updated: 2026-09-18

## Fold the deterministic Todo bookkeeping into hooks/task instead of Agent edits: 

- ID: TF-20260918-e2317d
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-18
- Updated: 2026-09-18
- Goal: Fold the deterministic Todo bookkeeping into hooks/task instead of Agent edits: the Next action, Updated, and status fields are fixed writes with no semantic judgment, and writing them by hand spends tokens.
- Task: `TaskFlowDocs/achieved/2026-09-18-todo-field-writes/`
- Next action: None — completed and archived.
- Notes: 用户提出（2026-09-18，在 ad8348 的 PR 打开后）：上面那条 `Next action` 的改写就是例子——它没有任何语义判断，只是把「PR 已开、等合入」这个状态写成固定句式，却要 Agent 读整条条目、定位行、写回。类似动作还有 `Updated` 落日期、状态推进时同步 `Next action`、promote 时回填 `Task:` 路径。hook 做这件事的代价只是把内容固定化，省的是 token。需要先定的边界：哪些字段是**确定性**的（可由 hook 直接从命令参数推出）vs 哪些仍要 Agent 写（需要判断的 goal、notes）；以及 `hooks/task state` 推进状态时是否应当顺带更新 `Next action`，还是留一个独立的 `task action` 子命令。相关条目：`TF-20260918-88e04c`（归档流程开销）是同一条思路的另一半。
- **2026-09-18 范围复盘**：原 Notes 里「应该做成流程规则，而非内容比对」的论证，只对**冲突该取哪一侧**成立——那是真判断。而这次实际手写的 `Next action: PR open …; await review and merge.` 不是判断，是从已知状态套模板，Hook 完全可以做。所以本条的边界是「确定性写入」（Next action / Updated / promote 时回填 `Task:`）交给 Hook，「需要判断的内容」（goal / notes / 规则措辞）仍由 Agent 写。待决：`Next action` 搭 `task state` 的车，还是单独开 `task action`。
- 本条交付即为本条服务的第一个用例：这个 Next action 由新命令写入，不再手改。Step 1 在 `hooks/task` 加 `next` 子命令（复用 `findsec`/`setr`/`run_awk_to`），Step 2 在 `hooks/smoke-test` 补一节（含 Notes 落点与字段缺失补行两个边界，已做一次变异验证）。
- v2 追加读侧：`hooks/task get <todo-id>` 只打印该条目字段行（复用既有 awk 内部分支，另开 entry 分支以免动到 TASKFLOW_CMD=get 的三个内部调用点）。

## Make the task complete transaction fail-safe: it marks both core documents compl

- ID: TF-20260918-e7c041
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-18
- Updated: 2026-09-22
- Goal: Make the task complete transaction fail-safe: it marks both core documents completed before hooks/archive runs, so any archive failure leaves the task half-archived with no rollback.
- Task: `TaskFlowDocs/achieved/2026-09-22-archive-transaction/`
- Next action: None — completed and archived.
- Notes: **2026-09-18 实测观测到（不是推测）**：在 `2026-09-18-todo-field-writes` 上跑 `hooks/task complete` 时，调用**失败**了，但失败发生在 mutation 之后——`hooks/task:589-590` 先把 prd.md 与 plan.md 置为 `completed`（两次 `docstatus`），再调用 `hooks/archive`；而后续报错时目录已被移动、Todo 已改。工作区于是停在「已归档 + 文档状态已改」的半完成态，没有回滚。
  当天的实际触发：worktree 上跑 `complete` 成功落盘，但 base 检出落后 4 个提交；`git merge --ff-only origin/main` 把**合并进来的** `plan.md` 覆盖了工作区里已改好的那份，Approval 块回到 `pending`，于是第二次 `complete` 报 `current Task version is not approved`。也就是说事务的中间态被后续的合并撞了回去——纯属运气，不是设计。
  与 `TF-20260918-172455`（archive 往 todo.md 插空行）、`TF-20260918-88e04c`（archive 的 stage 步骤与分支选择）同属一个事务；三者一起做才不用重复设计同一个失败边界。
- Updated: 2026-09-18

## Record approval in the plan from a hook instead of hand-editing four fixed-forma

- ID: TF-20260918-454ac4
- Status: inbox
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-18
- Updated: 2026-09-18
- Goal: Record approval in the plan from a hook instead of hand-editing four fixed-format fields, and fix hooks/version writing an Approval block that disagrees with hooks/task's template.
- Task: Not promoted.
- Next action: 先修 `hooks/version` 与 `hooks/task` 对 Approval 块形状的分歧（缺 `- Status:`、时间不带时区），再决定是否加 `hooks/task approve`。
- Notes: **2026-09-18 用户提出**：手改 Approval 块能否自动化。判定——`## Approval` 的字段里只有 `Approved by` 是语义的（必须由人表态），其余都可推导：`Status` 是该子命令的动词，`Approved at` 是当天日期（hook 已有 `today`），`Approved version` 直接读 plan 自己的 `> Task version:` 行，`Approved scope` 由存在的核心文档推出。`skills/taskflow/SKILL.md` 已把模板钉成「`- Approved by:` 起的四行」，格式无需 Agent 判断。
  **先修一个现成的自相矛盾**：`hooks/version` 的重置只写 `- Approved by/at/version/scope: pending` 四条，**不写 `- Status:`**；而 `hooks/task` 的模板是**五**行、带 `- Status: requested`。于是经 `version` 迁移过的任务，Approval 块是 version 的字段集加上一条滞留在旧值的 `- Status:` 行——两个 hook 对同一块内容的形状意见不一致。**本任务就是实例**：v1→v2 后 `- Status:` 留在 `checking` 一路没人管，直到 `complete` 读它才发现对不上（`require_approval` 用的是 `grep -qx -- "- Status: approved"`）。
  **时间格式也打架**：模板写 `YYYY-MM-DD HH:mm +08:00`，`version` 复位只写 `pending`。若自动化，`today` 目前只有 `+%Y-%m-%d`，要扩出分钟与时区。
  **门禁必须在写入之前**：合法顺序是「人先批准 → hook 记录」，不是「hook 写入 → 门禁通过」，否则 `require_approval` 变成自我认证。自动化只应删掉**转录**（把已表态的事实落成固定格式），不能生成或推断批准本身。
  **与 `TF-20260918-88e04c`、`TF-20260918-e7c041` 同族**：本次归档时 `complete` 在 base 检出上失败，正是因为 main 落后导致合并把 `Approval` 块覆盖回 `pending`，手工补批准后重跑才过。真正的修法在 `complete` 的**事务原子性**上（`e7c041`），不在让批准好写。
- Updated: 2026-09-18

## Fix task get silently dropping indented Notes continuation lines: it prints only

- ID: TF-20260918-9acf57
- Status: done
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-18
- Updated: 2026-09-22
- Goal: Fix task get silently dropping indented Notes continuation lines: it prints only lines starting with '- ', so a second Notes bullet written with the repo's two-space indent is absent from the output with no warning.
- Task: `TaskFlowDocs/achieved/2026-09-22-task-get-notes/`
- Next action: None — completed and archived.
- Notes: 本缺陷在归档 2026-09-18-todo-field-writes 时发现：`task get` 只打印 `^- ` 开头的行（`hooks/task` 的 `entry` 分支），而 Notes 的第二条及以后按仓库既有习惯写成**两空格缩进的 `- ` 行**，于是它们不出现在输出里，**且没有提示**。危害不是报错，是**静默**：调用方拿到一份看似完整、实则缺段的条目，据此决策。判据：本次取证用 `bash hooks/task get TF-20260918-454ac4` 只回出 Notes 的第一行，而文件里它下面还有三条缩进续行。修法二选一：(a) 把条目正文的缩进行也算正文一并打印；(b) 至少 stderr 提示该条目有 N 行未显示。v2 已合并，本缺陷未修。同族：`task next` 写 Notes 时用的是同一套字段边界（`isfield`），那边的续行判定虽已覆盖缩进，但输出侧没跟上。

## Make hooks/version write the same five-field Approval block hooks/task generates

- ID: TF-20260919-b7821b
- Status: in_progress
- Priority: normal
- Owner: Codex
- Source: audit follow-up
- Added: 2026-09-19
- Updated: 2026-09-23
- Goal: Make hooks/version write the same five-field Approval block hooks/task generates, so the plan gate and the version reset agree.
- Task: `TaskFlowDocs/2026-09-23-version-approval-shape/`
- Next action: Complete PRD / Spec / Plan and request approval.
- Notes: **2026-09-19 发布 v1.0.7 时确认**：`hooks/version` 的复位只写 `- Approved by/at/version/scope: pending` 四条，**不写 `- Status:`**；而 `hooks/task` 生成的模板是**五**行、带 `- Status: requested`。于是经 `version` 迁移过的任务，Approval 块是 version 的字段集加上一条滞留在旧值的 `- Status:` 行。`require_approval` 判定的却是 `grep -qx -- "- Status: approved"`——它在检查一个 `version` 从不写入的字段，之所以通常还能工作，只因 `hooks/task` 生成模板时写了一次。`TF-20260918-454ac4`（Approval 自动化）已记同一处矛盾，本条是它的前提条件：两个 hook 对同一块内容的形状不先对齐，自动写出来的块会继承同样的分歧。

## Measure whether delegating exploration to subagents actually reduces main-thread

- ID: TF-20260919-90797c
- Status: inbox
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-19
- Updated: 2026-09-19
- Goal: Measure whether delegating exploration to subagents actually reduces main-thread context, before adopting it as guidance.
- Task: Not promoted.
- Next action: Design the measurement, then run it on one real exploration.
- Notes: **2026-09-19 用户提出**：subagent 委派能不能省 token，要**实测**才知道，别先写进指引。

  **为什么值得测而不是直接采纳**：我给的论证是「读 `todo.md` 22k、整读 `SKILL.md`、反复读 `plan.md` 都在主线里做，丢给 subagent 就只回结论」。这条论证**在我这个会话里是空的**——我一次 subagent 都没用，所以那是推断不是观测。

  **反方向的可能（必须先承认）**：subagent 有 setup 成本（重建 prompt、加载工具、自己走一遍检索），一次小读取委派出去可能**比直接读更贵**；它的结论还要回主线，如果结论本身很长，省的就不多。所以「委派总是更省」很可能是错的，**该测的是阈值**：多大的读取/搜索开始值得委派。

  **测法（草案）**：同一件事（例如「找出 v1.0.6 到 main 之间哪些改动属于用户可见」）分别用「主线直接做」与「委派 subagent」各跑一次，记两边的：(a) 主线上下文增量，(b) 总 token（含 subagent 自身），(c) 结论质量是否够用。判据要**同时**看 (a) 与 (b)——只看主线增量会把成本藏进 subagent 里。

  **可用的观测手段**：`/context` 看占用；会话 jsonl 在 `~/.claude/projects/<path>/` 下可解析每轮的输入 token；`ctx stats` 若可用。选一个能复现的，别靠感觉。

  **落地条件**：只有实测显示某类探索稳定更省，才写进 `SKILL.md` 的 Phase 2/6（探索与复核）或 `CLAUDE.md` 的工作方式；否则结论就是「不采纳」，那也是有效结论。相关：本条与 `TF-20260919-76e7fb` 无关，属会话成本治理。

## Adapt TaskFlow to the DeepSeek Harness (dsh) as a fourth host: ship a dsh plugin

- ID: TF-20260919-55110d
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-19
- Updated: 2026-09-19
- Goal: Adapt TaskFlow to the DeepSeek Harness (dsh) as a fourth host: ship a dsh plugin bundle that self-wires the existing skill and hooks with no manual config
- Task: `TaskFlowDocs/achieved/2026-09-19-dsh-host/`
- Next action: None — completed and archived.

## Take a release out of the TaskFlow task workflow: RELEASE.md runs directly on th

- ID: TF-20260919-40eca2
- Status: done
- Priority: normal
- Owner: Codex
- Source: direct user request
- Added: 2026-09-19
- Updated: 2026-09-19
- Goal: Take a release out of the TaskFlow task workflow: RELEASE.md runs directly on the base checkout with no Todo item, task directory, branch, or PRD/Plan, and its record is the CHANGELOG section and the GitHub Release body.
- Task: `TaskFlowDocs/achieved/2026-09-19-release-flow-exception/`
- Next action: None — completed and archived.
- Notes: **2026-09-19 用户确认**：发布彻底不走 TaskFlow（不创建任务目录与 Todo 条目），记录形态取「只在 CHANGELOG 段落 + GitHub Release 正文」，写入方式取「纯文档规则、Agent 手写」，分支取「豁免——发布不从 base 检出切分支」，批准门禁改为「用户授权先行、写入 RELEASE.md 与发布正文」。本条即该决定的规则改动，已落在 RELEASE.md、CONTRIBUTING.md、SKILL.md、references/artifacts.md 与两份 README（分支问题由用户当场追问确认：『发布要切分支吗？不需要吧』，结论是不切）。

## Map the personal rule to a single personal.md: one file, each rule in its own se

- ID: TF-20260919-495145
- Status: inbox
- Priority: normal
- Owner: Codex
- Source: user decision
- Added: 2026-09-19
- Updated: 2026-09-19
- Goal: Map the personal rule to a single personal.md: one file, each rule in its own section with its own scope etc. The repository-docs index names personal.md and explains its origin (local-only, never committed) and purpose (personal rules that cannot override repository documents).
- Task: Not promoted.
- Next action: Clarify and promote when ready.

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

## Stop `TaskFlowDocs/todo.md` from growing without bound: it is at 877 lines, 45%

- ID: TF-20260919-6b4e21
- Status: inbox
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-19
- Updated: 2026-09-19
- Goal: Stop `TaskFlowDocs/todo.md` from growing without bound: it is at 877 lines / 50 KB, of which the 47 `done` entries are 45% (22.6 KB) and the 18 live entries (`inbox` 12, `promoted` 2, `in_progress` 4) are under a third — the file is a growing archive that every task still has to read.
- Task: Not promoted.
- Next action: User studies the fix and decides; do not start.
- Notes: **2026-09-19 用户提出，明确排除在本次修复范围外**（「先立一个 todo，我后面研究修复」）。
  **实测分布**（HEAD `c1147ab`，877 行 / 50,427 字节，按条目正文统计）：`done` 47 条 / 22,661 字节（45%）；`inbox` 12 条 / 14,194 字节；`in_progress` 4 条 / 3,422 字节；`promoted` 2 条 / 991 字节；模板与无法解析的 4 段 / 384 字节。**待每天打交道的 live 条目只有 18 条、不到三分之一。**
  **两个已观测到的结构损伤**（不只是「长」）：(1) `## Item template` 模板块停在第 251 行，**在条目中间**，其下还有条目，随后第 267 行是一句被截断的半句 `Every direct request or imported requireme`；(2) 条目顺序是三个时代的堆叠，不是严格新在前——`TF-20260919-*` 的若干条排在 `TF-20260918-*` 之下。
  **已排除的选项**：本文件的定义是 intake 清单（`SKILL.md:30`、`references/artifacts.md:9` 都写 triage metadata only），历史事实在 `TaskFlowDocs/achieved/`，且 `SKILL.md:44` 禁止第二份事实源——所以往 todo.md 里做归档是反方向的。按日期分片/换后端会把整套 hook（`hooks/archive`、`hooks/summarize-state`、`hooks/todo-check`、`hooks/merge-todo`、`hooks/task`）都改一遍。
  **读取代价已被 v1.0.7 砍掉一半**：`hooks/task get <todo-id>` 只回一条条目，`task next` / `task intake` 只写一条，所以「查/改」不再需要读全文；剩下的整读场景只有「新增条目」。（本条由 `hooks/task next` 写入，未手改。）

## Cut the mechanical overhead out of a release without adding any authority to it

- ID: TF-20260919-c41f8a
- Status: done
- Priority: high
- Owner: Codex
- Source: user request
- Added: 2026-09-19
- Updated: 2026-09-21
- Goal: Cut the mechanical overhead out of a release without adding any authority to it: write the six fixed version literals from one command, move the CHANGELOG section into the tagged commit so the tag is immutable, and make a stale release record fail CI instead of passing.
- Task: `TaskFlowDocs/achieved/2026-09-21-release-overhead/`
- Next action: None — completed and archived.
- Notes: **2026-09-19 用户指定三条一起做，作为本条**（依据是 v1.0.8 的实测产物，不是设想）。
- **2026-09-21 已 promote，三条经实测修正为**：(1) 机械字面量不是 6 处而是 **8 处 / 6 个文件**（4 个 manifest + 两份 README 各两处 `Version:` 示例），`hooks/release-version` 一次写掉；(2) **tag 缺正文不是真的**——实测 v1.0.7 (`c3c536d`) 与 v1.0.8 (`620c6a7`) 的 CHANGELOG 段落**都在被 tag 的 commit 里**，tag 注释是 tag 对象上的第二份正文，不替代第一份；真正缺的只是 `RELEASE.md` 没写下「段落先于 tag」这条顺序规则，改为补规则（R4）；(3) 新增两条已实测的检查——`release-check` 对每份 README **只用 head -1 比第一处**，把 `README.md:261` 改成 1.0.7 仍报 pass；以及 tag→pin 窗口内除 marketplace 两文件与 `TaskFlowDocs/` 外任何改动均应判红。用户已裁定：第 (2) 条只补规则、窗口豁免 `TaskFlowDocs/`。
  **三条内容**：
  (1) **`hooks/release-version <x.y.z>`（只做格值写入）**——当前一次发布要手改 **7 个文件**（`620c6a7` 的 stat）：4 个 manifest 的 `version`、两份 README 的插件列表示例、`CHANGELOG.md` 新段落。**前六处是格值**（4 个 manifest + 2 处 README 示例输出，`README.md:207,261`、`README.zh-CN.md:173,226`），完全可以一条命令写掉；**第七处是散文，留给 Agent**。Codex/CodeBuddy 的 cachebuster 形如 `1.0.8+codex.20260919`，日期用 hook 已有的 `today`。**必须一次调用写完，不要做成 preflight + write 两次**——一次调用就先检查后写，失败不留半成品。
  (2) **把 CHANGELOG 段落搬进 base tree 的 release commit，让 tag 不可变**。现状（`RELEASE.md:86-92` + 实测 `620c6a7`）：**release notes 活在 tag 指向的 commit 之后的第二个 commit 里**，所以 `git tag -a` 只能把正文写进 tag，**tag 本身缺发布正文**；后来补写正文是重写 tag 对象，而 tag 是 claude 的 `sha` pin 引用的东西，重写需要「显式 owner 授权 + 记录理由」（`RELEASE.md:126`，且改的是 `620c6a7`/`2a89e2` 那类 commit）。把 CHANGELOG 段落移进 release commit 之后：tag 指向的 commit 自带发布正文，下一个 tag 可以带正文且先于 pin 创建、此后不再改。`RELEASE.md` 的步骤顺序要同步（正文写入在打标签之前），并记录为什么。
  (3) **让过期的发布记录在 CI 里失败**：给 `hooks/release-check` 加一条——**tag 指向的 commit 之后、被 pin 的 commit 之前**，只允许存在 marketplace 的 `ref`/`sha` 字面量差异；一旦出现别的差异（CHANGELOG 段落、README、manifest 版本、代码），就退出非零。v1.0.8 顺带发现：`README.md:261` 的 `claude plugin list` 示例还停在 1.0.8，而发布前的文档版本是 1.0.9——这条同时就是防这个的。
  **三条的公共红线（不是可选项）**：新增的工具**不得做判断**。`RELEASE.md` 的批准门禁是「用户先批准，写入是转录」；格值写入与记录校验都是转录，所以可以做；**「允许发布」必须永远留在人手里**，任何一条都不得演变成自动发布或自动批准。另：`RELEASE.md:122` 明确「不做自动 tag / 自动 GitHub Release」，三条都不得触碰这条边界。
  **边界已核**：Hook 的 JSON 目前只有 `SessionStart`（`hooks/hooks.json`），三条都不需要新增 hook 事件，也都不需要 `hooks/task` / `hooks/archive` 的现有事务。`hooks/release-check` 已被 `hooks/smoke-test:1172-1231` 覆盖（漂移、坏 pin、cachebuster、缺 manifest），新增的检查要按同法补断言。相关：`TF-20260919-76e7fb`（发布不走 TaskFlow，已交付）、`TF-20260919-b7821b`（`hooks/version` 的 Approval 形状）。

## `task intake` inserts a new entry into the previous section instead of `## Items`

- ID: TF-20260921-337ab8
- Status: done
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-21
- Updated: 2026-09-22
- Goal: Fix task intake inserting a new entry into the previous section instead of the Items section, and its insertion point landing inside the Removed section.
- Task: `TaskFlowDocs/achieved/2026-09-22-todo-intake-insert/`
- Next action: None — completed and archived.
- Notes: **2026-09-21 用户指定：单独开一条。**
  **问题**：`hooks/task intake` 把新条目写进文件里的上一个 `## ` 节，而不是插到 `## Items` 下。新条目因此挂到别人的标题下——那次它挂在了「Stop `TaskFlowDocs/todo.md` from growing without bound…」节里，`promote` 又拿那行当标题生出 task 文档（本轮我用假标题「State in the Skill…」跑出了 plan/prd 的首行）。
  **另一半**：`intake` 的插入点固定在文件末尾，所以它落在 `## Removed` 之后；如果 `## Removed` 不是最后一节，新条目会插进 `## Removed` 节内，`todo-check` 读 `## Removed` 时会把在途条目当成已删除记录（该节与 `TF-20260918-985164` 的删除语义直接冲突）。
  **根因**：`hooks/task` 的 `intake` 分支（约 `:206-216`）是「rstrip 尾部空行 → 整文件原样输出 → 再追加 `## <title>` 块」，没有定位 `## Items` 边界，也没有插入点概念。
  **违反的既有约定**：`TaskFlowDocs/todo.md` 自己的 `## Items` 节里写着 `<!-- Add new items at the top using the template below. -->`——实现与文档约定相反。
  **判定依据**：`hooks/task get <todo-id>` 与 `hooks/task next <todo-id> … [notes]` 能只读/只改一条条目（`next` 的第三个位置参数就是 Notes），所以本次是「用 hook 写 Notes」而非手改——这正是 `task next` 存在的理由。
  **验收**：新条目落在 `## Items` 节内、位于任何其他 `## ` 节之前；`## Removed` 之后插入新条目不再可能污染删除记录；`todo-check` 的 removed 判定不受影响；smoke 增加一条断言（新条目不得出现在 `## Removed` 与文件末尾之间）。相关：本轮 PR #45 里我被这个 bug 误导，绕过后才 promote 成功。
  **同因的另一现象**：`## ` 标题与 Goal 对不齐是既有习惯，不是个别错误——本文件的 `## ` 节数比 `- ID:` 行数多 23，多出来的全是模板块（`## T-YYYYMMDD-001` 等），另有约 30 条已交付条目的标题是手写摘要、与 Goal 前缀不一致。`hooks/task get` 按 ID、`findsec` 按 `TaskFlowDocs/<task>/` 解析条目，都不看标题，所以目前只是可读性问题；唯一出错的是 `promote`——它用标题去派生任务目录名。口径待定：标题由 Goal 派生（与 intake 一致、可校验），还是保留人写标题但 `promote` 一并更新它。

## Removed

- ID: TF-20260921-4d8ae2 (removed 2026-09-22: stale: fix merged on main in PR 46 (02c1441); entry still said awaiting review)
- ID: TF-20260919-76e7fb (removed 2026-09-22: stale: delivered by release-flow-exception; merged in PR 42 (caad35b))
- ID: TF-20260919-2877ca (removed 2026-09-22: stale: delivered by release-flow-exception; merged in PR 42 (caad35b))
- ID: TF-20260918-88e04c (removed 2026-09-23: Covered by umbrella e7c041 / 2026-09-22-archive-transaction (R3 stage print + branch rule).)
- ID: TF-20260918-172455 (removed 2026-09-23: Covered by umbrella e7c041 / 2026-09-22-archive-transaction (R4 three-field rewrite lock).)

