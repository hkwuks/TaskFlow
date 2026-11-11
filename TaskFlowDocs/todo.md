## Item template

An entry is written by `hooks/task intake` in this shape. The sample is indented so the hooks that parse this file do not read it as an entry — every field a hook matches sits at column 0 in a real entry:

    ## <goal, cut to 80 bytes>

    - ID: TF-yyyymmdd-xxxxxx
    - Status: inbox
    - Priority: normal
    - Owner: <person or Agent>
    - Source: <user / review / issue / remote>
    - Kind: <defect / capability / internal>
    - Added: YYYY-MM-DD
    - Updated: YYYY-MM-DD
    - Goal: <one sentence>
    - Task: Not promoted.
    - Next action: <single next clarification or implementation action>

`- External:` is not written by `intake`; add it by hand only for a source that
has an issue number or URL.

## Status flow

`inbox → clarified → promoted → in_progress → done/cancelled`

## Items

<!-- Add new items at the top using the template below. -->

## 在真实 GitHub PR 中验证已合并的文档跟进 CI 复用及失败回退

- ID: TF-20261110-8c4e24
- Status: inbox
- Priority: normal
- Owner: Unknown
- Source: follow-up:2026-11-10-ci-docs-followup
- Kind: capability
- Added: 2026-11-10
- Updated: 2026-11-10
- Goal: 在真实 GitHub PR 中验证已合并的文档跟进 CI 复用及失败回退
- Task: Not promoted.
- Next action: Clarify and promote when ready.

## 在可用的真实宿主会话中验证 TaskFlow 能力对齐及基础工作区

- ID: TF-20261110-0c7346
- Status: in_progress
- Priority: normal
- Owner: Unknown
- Source: follow-up:2026-11-10-host-capability-parity
- Kind: defect
- Added: 2026-11-10
- Updated: 2026-11-10
- Goal: 在可用的真实宿主会话中验证 TaskFlow 能力对齐及基础工作区异步提醒，逐项记录事件与提示是否实际到达
- Task: `TaskFlowDocs/2026-11-10-host-validation/`
- Next action: Complete PRD / Spec / Plan and request approval.
- Notes: 同一真实宿主验证时一并观察工具引导提示、实际能力选择和计划质量；区分提示送达与模型采纳，未经对照不声称因果改善。关联 TF-20261110-a56e72。另：合成 `PreToolUse` 事件显示新 `taskflow/declarations` 文件未纳入 evidence/released 的直接编辑流程护栏；需检查并补齐，该护栏不覆盖任意 shell 写入。

## 审视 TaskFlow 流程中的不合理环节和 Token 开销

- ID: TF-20261110-84d1a9
- Status: in_progress
- Goal: 排查 TaskFlow 流程、工具引导及相关记录中不合理或浪费 Token 的环节，并在验证有效后修复或精简
- Task: `TaskFlowDocs/2026-11-10-token-review/`
- Next action: Re-approve the new Task version before core changes.
- Updated: 2026-11-11

## 避免已通过 CI 后的文档跟进重复运行重型测试

- ID: TF-20261110-b73d49
- Status: done
- Goal: 让代码已通过 CI 后仅补充验证结果等任务文档的后续提交安全跳过不必要的重型测试，同时保留必要状态检查
- Task: `TaskFlowDocs/achieved/2026-11-10-ci-docs-followup/`
- Next action: None — completed and archived.

## 调查 Codex 中工具引用机制的引导效果

- ID: TF-20261110-a56e72
- Status: done
- Goal: 调查 digdig 新会话中工具引用机制对 Codex 的引导效果不佳的问题，并确定可验证的改进方式
- Task: `TaskFlowDocs/achieved/2026-11-10-codex-tool-guidance/`
- Next action: None — completed and archived.

## 检查并修复已支持 Agent 宿主的 TaskFlow 能力对齐：逐项核实实

- ID: TF-20261109-293987
- Status: done
- Goal: 检查并修复已支持 Agent 宿主的 TaskFlow 能力对齐：逐项核实实际接线、宿主事件与运行效果，补齐可支持能力和持续验证，区分未接线、未验证与确实不支持；关联 TF-20261109-e2df6d 和 TF-20261104-d3ac3c
- Task: `TaskFlowDocs/achieved/2026-11-10-host-capability-parity/`
- Next action: None — completed and archived.

## 让插件和桌面应用中的用户能够清楚获知 Agent 创建的 worktree

- ID: TF-20261109-3c1409
- Status: done
- Goal: 让插件和桌面应用中的用户能够清楚获知 Agent 创建的 worktree 所在路径及对应分支，并研究宿主可见性与展示方式
- Task: `TaskFlowDocs/achieved/2026-11-10-worktree-visibility/`
- Next action: None — completed and archived.

## 在 README 中展示 TaskFlow 架构与计划审核

- ID: TF-20261110-62fd8e
- Status: done
- Goal: 在中英文 README 添加 TaskFlow 架构图，展示流程、工具引导和计划审核及其边界
- Task: `TaskFlowDocs/achieved/2026-11-10-architecture-readme/`
- Next action: None — completed and archived.

## 为 TaskFlow 基础工作区写前防护设计可验证的发布例外，避免

- ID: TF-20261109-ccbb96
- Status: inbox
- Priority: normal
- Owner: Unknown
- Source: user:2026-11-09-release-guard-exception
- Kind: capability
- Added: 2026-11-09
- Updated: 2026-11-09
- Goal: 为 TaskFlow 基础工作区写前防护设计可验证的发布例外，避免阻止合法发布文档编辑，同时防止通过自报发布绕过防护
- Task: Not promoted.
- Next action: Clarify and promote when ready.

## 防止 TaskFlow 开发任务跳过独立 worktree，在 main 基础工作区直

- ID: TF-20261109-e2df6d
- Status: done
- Goal: 防止 TaskFlow 开发任务跳过独立 worktree，在 main 基础工作区直接修改文件；覆盖 digdig 事故并验证宿主写入限制
- Task: `TaskFlowDocs/achieved/2026-11-09-main-write-guard/`
- Next action: None — completed and archived.

## 插件引导下模型去做标记类周边工作而非实现真正功能

- ID: TF-20261107-5c5ee2
- Status: done
- Goal: 在插件引导下执行 todo 时，模型倾向于去做增加文件写入标记等周边工作，而不去实现真正需要修复或实现的功能；需要查清根本原因，判断是发散探索流程没发现问题的本质，还是其他机制导致的
- Task: `TaskFlowDocs/achieved/2026-11-07-repro-requirement/`
- Next action: None — completed and archived.

## 审批辅助命令按目录顺序识别活跃任务，无法为当前任务准

- ID: TF-20261106-3efcd7
- Status: done
- Goal: 审批辅助命令按目录顺序识别活跃任务，无法为当前任务准确补录阶段记录：一个任务树里存在多个 TaskFlowDocs/<slug>/ 时，task unaided/approve 取的是字母序第一个含 plan.md 的目录，而不是调用者所在的这个任务
- Task: `TaskFlowDocs/achieved/2026-11-06-active-task-detection/`
- Next action: None — completed and archived.

## 开发本仓库前先判定改动目标属于哪一类：插件自身能力（sk

- ID: TF-20261105-77051f
- Status: done
- Goal: 开发本仓库前先判定改动目标属于哪一类：插件自身能力（skills/、hooks/）、插件发给用户仓库的默认规则模板（hooks/templates/）、还是本仓库自己的规则文件，并据此选择正确的落点
- Task: `TaskFlowDocs/achieved/2026-11-05-change-target-rule/`
- Next action: None — completed and archived.

## 复杂框架项目中，引导模型关注整体效果与每一层的功能设

- ID: TF-20261105-f322be
- Status: done
- Goal: 复杂框架项目中，引导模型先建立整架构与各层职责的理解，从而在粗粒度需求下能定位问题所属的层；并禁止为了表面上的好结果去修改某一层的中间输出（这属于目标欺骗）——两个要求是一体两面：找不对层，就只能从症状处凑答案
- Task: `TaskFlowDocs/achieved/2026-11-05-layered-integrity/`
- Next action: None — completed and archived.

## README.md and README.zh-CN.md both still say Codex's wiring is SessionStart only

- ID: TF-20261104-d3ac3c
- Status: done
- Goal: README.md and README.zh-CN.md both still say Codex's wiring is SessionStart only and the pre-write gate cannot be wired there, which stopped being true at af8719a (2026-10-30, shipped in v1.1.10)
- Task: `TaskFlowDocs/achieved/2026-11-04-readme-codex-gate/`
- Next action: None — completed and archived.

## Ship TaskFlow's dsh plugin over the Git install path: make dsh plugin add github

- ID: TF-20261104-e151e6
- Status: done
- Goal: Ship TaskFlow's dsh plugin over the Git install path: make dsh plugin add github:hkwuks/TaskFlow#<sha> the documented main path, add the npm files whitelist so a pack is not 3.8MB, and record the commit pin the install needs
- Task: `TaskFlowDocs/achieved/2026-11-07-dsh-git-install/`
- Next action: None — completed and archived.

## Task archive should delete the local branch once it is merged: today archive rem

- ID: TF-20261104-d535ae
- Status: done
- Goal: Task archive should delete the local branch once it is merged: today archive removes the worktree and explicitly leaves the branch, so merged branches accumulate and nothing reports them
- Task: `TaskFlowDocs/achieved/2026-11-04-teardown-branch/`
- Next action: None — completed and archived.

## The Todo merge driver takes 180s on a 125-entry todo.md and silently loses a mer

- ID: TF-20261104-b1681b
- Status: done
- Goal: The Todo merge driver takes 180s on a 125-entry todo.md and silently loses a merge when its caller times out: the interrupted run leaves %A as ours, so the merge commits one side's file with no driver result and no error
- Task: `TaskFlowDocs/achieved/2026-11-04-merge-todo-speed/`
- Next action: None — completed and archived.

## PR 流程可以少一次提交：CI 已过、PR body 已改完、只差合并时

- ID: TF-20261103-af456a
- Status: done
- Goal: PR 流程可以少一次提交：CI 已过、PR body 已改完、只差合并时，允许先归档再一并合并，避免为归档记录再推一次触发一整轮 CI
- Task: `TaskFlowDocs/achieved/2026-11-04-ci-skip-archive/`
- Next action: None — completed and archived.

## 收到「修D1」后跳过全部 TaskFlow 阶段直接改产品代码，且改在 base checkout

- ID: TF-20261103-fa9090
- Status: done
- Goal: 用户下「修D1」后，Agent 跳过整个 TaskFlow 阶段直接改产品代码，且改在 main 的 base checkout 上；TaskFlow 对此没有任何拦截。要查的是：规则送达了、违反也发生了，为什么中间没有一道门
- Task: `TaskFlowDocs/achieved/2026-11-04-skip-guard/`
- Next action: None — completed and archived.

## Bind external-fact evidence to any tool class, not the WebSearch|WebFetch produc

- ID: TF-20261102-7a9caa
- Status: done
- Goal: Bind external-fact evidence to any tool class, not the WebSearch|WebFetch product list
- Task: `TaskFlowDocs/achieved/2026-11-02-external-tool-binding/`
- Next action: None — completed and archived.

## 个人配置文件（personal.md、sessions.md 等）若出现在 worktree 中

- ID: TF-20261030-15b439
- Status: done
- Goal: 个人配置文件（personal.md、sessions.md 等）若出现在 worktree 中，归档时可同步到 main 的对应任务路径下，且保持不纳入版本控制。
- Task: `TaskFlowDocs/achieved/2026-11-03-archive-local-files/`
- Next action: None — completed and archived.

## Assert the $schema a plugin manifest declares, so a schema URL that stops resolv

- ID: TF-20261029-218fdf
- Status: done
- Goal: Assert the $schema a plugin manifest declares, so a schema URL that stops resolving or a manifest that drops one fails a check instead of shipping
- Task: `TaskFlowDocs/achieved/2026-10-29-schema-check/`
- Next action: None — completed and archived.

## task approve requires the first [Plan] line to name exactly the capability relea

- ID: TF-20261026-726ec4
- Status: done
- Goal: task approve requires the first [Plan] line to name exactly the capability released for that stage, so a phase that invoked a different capability in a later version cannot be approved without hand-editing the shared released file
- Task: `TaskFlowDocs/achieved/2026-10-26-capability-task-identity/`
- Next action: None — completed and archived.

## A throw in hooks/smoke-test-windows.ps1 after the launcher section hangs the sui

- ID: TF-20261025-645ef4
- Status: done
- Goal: Give hooks/smoke-test-windows.ps1 a stdin for the SessionStart call it makes, so the suite cannot block on an open one: measured 2026-10-28, the hang is line 96's `Invoke-SessionStart 'pr'`, not any throw — `run-hook.cmd session-start` has no stdin of its own, so it inherits the runner's, and `session-start` reads its event with `cat`. A throw is never the cause: injected at eight positions, every one before line 96 exits 1 in under 14s with its message, every one after it hangs.
- Task: `TaskFlowDocs/achieved/2026-10-28-windows-smoke-stdin/`
- Next action: None — completed and archived.

## Ignore personal.md and sessions.md without the user editing .gitignore: the plug

- ID: TF-20261025-7c5897
- Status: done
- Goal: Ignore personal.md and sessions.md without asking the user to edit .gitignore: the plugin writes its own per-clone exclude lines, because a tracked .gitignore only ever governs the repository it lives in
- Task: `TaskFlowDocs/achieved/2026-10-25-git-hygiene/`
- Next action: None — completed and archived.

## Keep sessions.md out of Git: it carries a machine-local session id, working dire

- ID: TF-20261025-24d06c
- Status: done
- Goal: Keep sessions.md out of Git: it carries a machine-local session id, working directory and timestamps, so a committed copy is stale on every other clone
- Task: `TaskFlowDocs/achieved/2026-10-25-untrack-sessions/`
- Next action: None — completed and archived.

## Make the capability store recoverable instead of delete-and-restart: a truncated

- ID: TF-20261025-ef6c18
- Status: done
- Goal: Make the capability store recoverable instead of delete-and-restart: a truncated evidence file loses records the released lines still point at
- Task: `TaskFlowDocs/achieved/2026-10-25-capability-store-recover/`
- Next action: None — completed and archived.

## Give the pre-write gate the same out-of-step diagnosis that unaided now has: it

- ID: TF-20261025-537a8a
- Status: done
- Goal: Give the pre-write gate the same out-of-step diagnosis that unaided now has: it keeps denying a desynced store but never says why
- Task: `TaskFlowDocs/achieved/2026-10-25-gate-desync-diagnosis/`
- Next action: None — completed and archived.

## When a phase has no capability worth invoking, the fallback is the model's own a

- ID: TF-20261024-b48e56
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: user request 2026-10-24
- Added: 2026-10-24
- Updated: 2026-10-24
- Goal: When a phase has no capability worth invoking, the fallback is the model's own ability, and the docs should say so in those words instead of only describing it as nothing having been invoked
- Task: Not promoted.
- Next action: Read the three places that define the fallback -- skills/taskflow/SKILL.md:179, references/artifacts.md:99 and :130, references/runtime.md:63 -- and decide what the wording should say. Today all of them describe Unaided as the absence of a capability ('no capability applied to this phase', 'nothing was invoked'), which reads as a gap rather than as a choice. The requested framing is that the fallback when no tool is worth introducing is the model's own ability, so the phase still runs, and the record says which ability was brought to bear. Decide whether that is an edit to those three paragraphs, a fourth field in the recorded line, or a rename -- and whether the 'considered:' field already carries it (it names the concept class the model was asked to supply). Keep the mechanical contract unchanged: the class still validates against the phase vocabulary and approve still reconciles it exactly.
- Notes: Reported by the user 2026-10-24 while defining TF-20261024-310937. The user's wording: 这类引入工具的策略，当没有工具可以引入的时候，就用模型自己的能力。Related to TF-20261024-310937 (the Test stage's carrier): that task adds a fourth stage to the same set, so its line shape has to say what the model supplied for a stage no tool covers. Not the same gap as TF-20261009-8abbd6 (give a phase a way to record a selection that is not a tool-call artifact) -- this one is about what the fallback IS, not about how to record it.

## Test generation and test writing should draw in tools through the same mechanism

- ID: TF-20261024-310937
- Status: done
- Goal: Test generation and test writing should draw in tools through the same mechanism that writing the Plan does, instead of being only one row in the phase-concept table with nothing that makes the consideration happen or records that it did
- Task: `TaskFlowDocs/achieved/2026-10-24-test-phase-capability/`
- Next action: None — completed and archived.

## Reference-material reinforcement: some materials must be brought back to attenti

- ID: TF-20261023-c7540c
- Status: done
- Goal: Reference-material reinforcement: some materials must be brought back to attention while a task is running, not only read once at session start. Today the routed document list is produced by hooks/repository-docs-context and injected only from session-start, so in a long implementation the Agent works from whatever it read at the beginning. Decide what makes a document task-running material rather than phase material, where that is recorded, and whether the existing per-prompt reminder carries it.
- Task: `TaskFlowDocs/achieved/2026-10-24-reference-reinforce/`
- Next action: None — completed and archived.

## Review the Plan once before approval while TaskFlow is in use: after plan.md is

- ID: TF-20261022-47c217
- Status: done
- Goal: Review the Plan once before approval while TaskFlow is in use: after plan.md is written and before the user approves it, review the Plan itself rather than the code. If a capability covers plan review, invoke it the way the other phases invoke theirs (the [Plan] capability line in Skills / Tools Used, recorded through the same evidence path); if none is available, decide between reviewing unaided and reminding during implementation instead. Scope: TaskFlow while it is being used on a project, not development of TaskFlow itself.
- Task: `TaskFlowDocs/achieved/2026-11-07-plan-review/`
- Next action: None — completed and archived.

## End-of-task collapse: hooks/archive checks only that prd/plan say completed, whi

- ID: TF-20261022-fda8d8
- Status: done
- Goal: End-of-task collapse: hooks/archive checks only that prd/plan say completed, while task complete checks approval, unchecked items and unfinished Steps — so hand-editing the status and running archive skips all three (measured 2026-10-22: approval section deleted, 2 pending Steps, archive still exit 0). SKILL.md:305 also documents the manual sequence as the procedure and mentions task complete only at :60
- Task: `TaskFlowDocs/achieved/2026-10-23-archive-completion-gate/`
- Next action: None — completed and archived.

## Agent drifts out of TaskFlow mid-task: after starting under the workflow it sile

- ID: TF-20261022-d8db4d
- Status: done
- Goal: Agent drifts out of TaskFlow mid-task: after starting under the workflow it silently stops following it and just runs on its own — no state/progress updates, no approval gate, no verification record — while the task directory still looks in-progress
- Task: `TaskFlowDocs/achieved/2026-10-22-taskflow-drift-guard/`
- Next action: None — completed and archived.

## Before pushing a PR, establish which repository receives it: a fork's branch is

- ID: TF-20261021-d5c738
- Status: done
- Goal: Before pushing a PR, establish which repository receives it: a fork's branch is pushed to the writable fork (head), while the PR targets the original author's repository (base) — cannot push to upstream without write permission. Record the checkable facts (isFork/parent/source via gh api, .permissions.push per candidate, branch protection) instead of inferring repo role from a remote named origin/upstream
- Task: `TaskFlowDocs/achieved/2026-11-02-fork-topology/`
- Next action: None — completed and archived.

## Refine the worktree rules: changes the author does not want to commit (local edi

- ID: TF-20261021-0f066f
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: user request 2026-10-21
- Added: 2026-10-21
- Updated: 2026-10-21
- Goal: Refine the worktree rules: changes the author does not want to commit (local edits, not a requirement) and actions the author is authorized to perform directly on the base checkout (tagging, releasing) must not open a worktree
- Task: Not promoted.
- Next action: Clarify and promote when ready.

## Extract a set of default working rules from CODE_STYLE.md / CONTRIBUTING.md and

- ID: TF-20261021-4950fc
- Status: done
- Goal: Extract a set of default working rules from CODE_STYLE.md / CONTRIBUTING.md and similar docs, and make sure the defaults never override or violate the user's own habits
- Task: `TaskFlowDocs/achieved/2026-11-02-default-working-rules/`
- Next action: None — completed and archived.

## Make the Hooks workflow skip the jobs a change cannot affect, so a task archive

- ID: TF-20261020-a46573
- Status: done
- Goal: Make the Hooks workflow skip the jobs a change cannot affect, so a task archive or a docs-only commit does not queue a three-OS smoke matrix and an eleven-minute macOS runner, and add a concurrency group so a new push cancels the run it superseded. Today every pull request runs all four jobs: smoke on ubuntu, macos and windows, release-check, todo-merge-audit, and evals. Measured 2026-10-20 on PR #90, which only moved one task directory into achieved and updated its Todo entry: the macOS job queued eleven minutes and ran forty-two seconds, and the same thing happened on each of the three pushes that preceded it. The dependency is not 'a markdown file changed' but which job reads which path: release-check reads CHANGELOG.md, README.md, README.zh-CN.md and the manifests, so a docs-only skip has to keep running it when those move, while hooks/smoke-test also reads active TaskFlowDocs task directory names, which is why the mapping has to be recorded and checked rather than guessed.
- Task: `TaskFlowDocs/achieved/2026-10-20-ci-path-filter/`
- Next action: None — completed and archived.

## Validate the task id that promote joins into a filesystem path, and give a wrong

- ID: TF-20261020-cd02f5
- Status: done
- Goal: Validate the task id that promote joins into a filesystem path, and give a wrongly promoted entry a CLI way back: promote takes the id as task and runs mkdir -p on TaskFlowDocs/<task> with no shape check, so a misplaced flag makes --size the directory name and ../ escapes the docs tree entirely; because the command then succeeds, the Todo entry reads promoted and task remove refuses to undo it, leaving no CLI recovery. The same unvalidated value reaches state, progress, approve, complete, archive and reopen, and archive can move a directory from outside the repo into achieved/.
- Task: `TaskFlowDocs/achieved/2026-10-20-task-id-validation/`
- Next action: None — completed and archived.

## Stop stating the Task version history twice: prd.md and plan.md each keep their

- ID: TF-20261018-0f2f6a
- Status: done
- Goal: Stop stating the Task version history twice: prd.md and plan.md each keep their own Version History, and the two hand-maintained statements drift
- Task: `TaskFlowDocs/achieved/2026-10-18-single-history-owner/`
- Next action: None — completed and archived.

## Repair the todo.md template block and the leftover headings: the Item template s

- ID: TF-20261018-3f6686
- Status: done
- Goal: Repair the todo.md template block and the leftover headings: the Item template sits between entries with a truncated sentence, and its field names no longer match what intake writes
- Task: `TaskFlowDocs/achieved/2026-10-18-todo-template-repair/`
- Next action: None — completed and archived.

## Backfill the missing Todo record for a task whose documents landed without one:

- ID: TF-20261018-bfc718
- Status: done
- Goal: Backfill the missing Todo record for a task whose documents landed without one: TaskFlowDocs/achieved/2026-09-10-repository-document-placement entered the repository inside a release commit (660679a, release 1.0.2) instead of through a task branch, so it never had a Todo entry; the orphan-task-directory check added later by 2026-09-23-orphan-task-dirs has flagged it ever since. The directory and its documents are kept exactly as they are. Only the missing record is restored, so the check reports green again and its green carries information.
- Task: `TaskFlowDocs/achieved/2026-09-10-repository-document-placement/`
- Next action: None — completed and archived.

## Removing a task worktree is nobody's job: nothing in the lifecycle tells the Age

- ID: TF-20261018-66f814
- Status: done
- Goal: Removing a task worktree is nobody's job: `complete` archives the directory and closes the Todo entry, but nothing in the lifecycle, in `CONTRIBUTING.md`, or in `SKILL.md` ever tells the Agent to tear the worktree down, and nothing checks whether it has gone. The result is that `.worktrees/` keeps every merged task forever and the local branch keeps pointing at its merge commit. Verified 2026-10-18: the word `worktree` appears in `CONTRIBUTING.md` only for creating one, and `grep -rn 'worktree remove\|worktree prune' hooks/` finds nothing, so `repository-check` reports stale worktrees only when their branch no longer exists — not when the task merged and was archived. Nine such worktrees had accumulated before this was noticed.
- Task: `TaskFlowDocs/achieved/2026-10-19-worktree-teardown/`
- Next action: None — completed and archived.

## The stage ledger pairs each release to a capability record by queue position rat

- ID: TF-20261012-c79e31
- Status: done
- Goal: The stage ledger pairs each release to a capability record by queue position rather than by stage, so which capability a phase is credited with depends on the order its document happened to be written, and hooks/task approve then requires the Skills / Tools Used bullet to name that exact capability: a phase that really invokes several capabilities overflows into the next phase, writing plan.md first credits the Plan stage with the PRD stage call, and an honest Skills / Tools Used section is refused while a reordered one passes, so the section becomes a value back-filled to satisfy the gate rather than a report of what happened
- Task: `TaskFlowDocs/achieved/2026-10-17-stage-capability-pairing/`
- Next action: None — completed and archived.

## Bookkeeping the stage ledger by a globally monotonic evidence queue makes a Task

- ID: TF-20261012-c66ad3
- Status: done
- Goal: Bookkeeping the stage ledger by a globally monotonic evidence queue makes a Task version bump repeat the capability bookkeeping: hooks/task approve requires every stage to appear in <absolute-git-dir>/taskflow/released, and a stage is released only while evidence lines > max(seq), so each new Task version needs one fresh release per stage it writes and seq never resets. Corrected 2026-10-18: this is repeated work, not a dead end — the earlier claim that once consumed reaches the line count no later version can be released is false, because hooks/task unaided appends its own evidence line and then its own release line (hooks/task:1042-1043), so a host with a gate is never blocked by an exhausted queue. What remains true is that every version bump repeats N declarations or calls (N = stages to write); only a host without a gate actually needs real invocations
- Task: `TaskFlowDocs/achieved/2026-11-03-version-bump-bookkeeping/`
- Next action: None — completed and archived.

## The entry signal for unregistered work never fires in the state a session actual

- ID: TF-20261012-50164f
- Status: done
- Goal: The entry signal for unregistered work never fires in the state a session actually opens in: hooks/summarize-state closes three silences (no TaskFlowDocs; TaskFlowDocs with nothing recorded; a branch no task directory matches) but the second is unreachable wherever TaskFlowDocs/todo.md is tracked, and the third excludes main and master by literal name rather than resolving the base branch, so the base checkout, which is where a session most often starts, is the one state that prints neither line
- Task: `TaskFlowDocs/achieved/2026-10-17-summarize-state-entry-signal/`
- Next action: None — completed and archived.

## The pre-write capability gate is wired only on Claude Code and Trae, so on the o

- ID: TF-20261011-39bda8
- Status: done
- Goal: The pre-write capability gate is wired only on Claude Code and Trae, so on the other three supported hosts task approve can never succeed: hooks/task approve requires a taskflow/released record, capability-gate is the only writer of that file, and the Codex, CodeBuddy, and dsh hook wiring files subscribe to no tool-call event at all - only SessionStart. Measured 2026-10-11 in a fixture: with the gate wired the unaided declaration releases the stage and approve reconciles it; with the gate absent the same command reports unaided OK and exits 0 while released is never created, so approve returns 'stage [PRD] was never released by the pre-write gate' permanently, and its suggested remedy is that same unaided command, which cannot work. Approve is the only sanctioned writer of the Approval block, so in_progress, complete, and archive are all unreachable and the user is forced to hand-write the approval record. The three hosts' own deny-capable events are already recorded in the event map (Codex and CodeBuddy PermissionRequest/PreToolUse, dsh tools/pre-execute); Trae was wired by contract match without modifying either hook script. Wire the gate where the host's contract matches, and decide what an approve on a genuinely hookless host must do now that the docs say such a host needs no hooks.
- Task: `TaskFlowDocs/achieved/2026-10-11-gate-host-coverage/`
- Next action: None — completed and archived.

## Taking over work that never entered TaskFlow triggers nothing: the applicability

- ID: TF-20261010-82ec77
- Status: done
- Goal: Taking over work that never entered TaskFlow triggers nothing: the applicability gate fires on a request that asks to modify the repository, while continuing or inheriting an existing unlogged workstream reads as a continuation, and SKILL.md:75 then rules a new session or changed implementation detail is never by itself a new-task trigger, so nothing ever asks whether the work should have been registered
- Task: `TaskFlowDocs/achieved/2026-10-10-entry-point-silence/`
- Next action: None — completed and archived.

## Decouple stage capability selection from the host tool-call stream: the PreToolU

- ID: TF-20261009-8abbd6
- Status: done
- Goal: Decouple stage capability selection from the host tool-call stream: the PreToolUse gate refuses the first write of prd/spec/plan unless a Skill/Agent/MCP call already matched, so a host that has no such call, or a session driven from a different cwd than the task worktree, forces either a throwaway invocation like skill(sxng) for a PRD already researched, or the unaided declaration for a phase that really did use a capability. Give the phase a way to record its selection that is not a tool-call artifact
- Task: `TaskFlowDocs/achieved/2026-11-03-gate-stage-class/`
- Next action: None — completed and archived.

## Adapt TaskFlow to Trae IDE as a fifth host: ship hooks/hooks-trae.json and a doc

- ID: TF-20261009-369e77
- Status: done
- Goal: Adapt TaskFlow to Trae IDE as a fifth host: ship hooks/hooks-trae.json and a documented .trae/hooks.json export, with no Trae plugin mechanism to install through (Trae hooks are user-scoped .trae/hooks.json only; Trae also reads Claude Code hook configs)
- Task: `TaskFlowDocs/achieved/2026-10-09-trae-host/`
- Next action: None — completed and archived.

## Keep skills/taskflow/references/*.md and hooks/README.md in sync with the real h

- ID: TF-20261008-a4454d
- Status: done
- Goal: Keep skills/taskflow/references/*.md and hooks/README.md in sync with the real hooks directory: smoke-test pins clauses in SKILL.md and artifacts.md but never validates these two documents against the hooks that exist
- Task: `TaskFlowDocs/achieved/2026-10-24-hooks-doc-sync/`
- Next action: None — completed and archived.

## Define TaskFlow compatibility with loop and long-running tasks: repeated externa

- ID: TF-20261008-ca2fce
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: user request 2026-10-08, 8-item doc/tooling batch
- Added: 2026-10-08
- Updated: 2026-10-08
- Goal: Define TaskFlow compatibility with loop and long-running tasks: repeated external driving of one task, partial progress records, and resume boundaries when a task is entered many times
- Task: Not promoted.
- Next action: Clarify and promote when ready.

## Add a brainstorming and idea-refinement concept class to the phase-to-capability

- ID: TF-20261008-5b5635
- Status: done
- Goal: Add a brainstorming and idea-refinement concept class to the phase-to-capability table: phase 1 bundles refining a vague idea with writing the requirements document, so ideation capabilities are never considered
- Task: `TaskFlowDocs/achieved/2026-10-08-capability-concept-classes/`
- Next action: None — completed and archived.

## sessions.md needs a trigger condition, or should be demoted to a hook-only artif

- ID: TF-20261008-b1f5e0
- Status: done
- Goal: sessions.md needs a trigger condition, or should be demoted to a hook-only artifact: only the SessionStart hook ever creates it, so 2 of 88 task dirs have one and SKILL.md:289 states no condition that makes the Agent write one
- Task: `TaskFlowDocs/achieved/2026-10-08-task-open-and-continuation/`
- Next action: None — completed and archived.

## The capability-evidence hook and the capability-gate anchor on different things,

- ID: TF-20261001-efbc51
- Status: done
- Goal: The capability-evidence hook and the capability-gate anchor on different things, so a stage invocation can go unrecorded: capability-evidence locates the store and the active task from the event cwd, capability-gate locates them from the written file's path, and the two agree only when the session cwd is the task worktree - otherwise the invocation records nothing and the gate then refuses the write
- Task: `TaskFlowDocs/achieved/2026-10-11-evidence-anchor/`
- Next action: None — completed and archived.

## hooks/reopen does not rewrite the Todo Task: path back to the active root, so ta

- ID: TF-20261001-da6047
- Status: done
- Goal: hooks/reopen does not rewrite the Todo Task: path back to the active root, so task state cannot find the entry it just retrieved
- Task: `TaskFlowDocs/achieved/2026-10-01-reopen-todo-path/`
- Next action: None — completed and archived.

## Commit Todo, release, and TaskFlowDocs changes straight to main when the author

- ID: TF-20261001-331f7c
- Status: done
- Goal: Commit Todo, release, and TaskFlowDocs changes straight to main when the author can push there; open a pull request only when they cannot
- Task: `TaskFlowDocs/achieved/2026-10-01-taskflow-commit-path/`
- Next action: None — completed and archived.

## Reconcile the artifact-language rule with capability-written documents: a phase

- ID: TF-20261001-51d9c8
- Status: done
- Goal: Reconcile the artifact-language rule with capability-written documents: a phase capability emits English prose, so the rule requiring the user's working language silently stops holding
- Task: `TaskFlowDocs/achieved/2026-10-01-artifact-language/`
- Next action: None — completed and archived.

## A release skips re-running tests that CI already ran green on the same revision,

- ID: TF-20260930-c4e4c8
- Status: done
- Goal: A release skips re-running tests that CI already ran green on the same revision, and testing prefers CI over local runs
- Task: `TaskFlowDocs/achieved/2026-09-30-release-ci-test-policy/`
- Next action: None — completed and archived.

## Fix the pre-write gate's silent fail-open on Windows: Claude Code delivers tool_

- ID: TF-20260930-ba3b0c
- Status: done
- Goal: Fix the pre-write gate's silent fail-open on Windows: Claude Code delivers tool_input.file_path with backslash separators there, so the gate's directory extraction finds no separator and allows every stage write — normalize separators before any path test, and add the regression test that feeds a backslash path
- Task: `TaskFlowDocs/achieved/2026-09-27-capability-pre-write-gate/` (v2)
- Next action: None — completed and archived.

## 修复 TaskFlow hooks 的四处遗留缺陷

- ID: TF-20260929-f9b6c9
- Status: done
- Goal: 修复 TaskFlow hooks 的四处遗留缺陷
- Task: `TaskFlowDocs/achieved/2026-09-29-hook-defect-followups/`
- Next action: None — completed and archived.

## Verify the released pre-write gate end-to-end in a live session: install the rel

- ID: TF-20260929-3fc4b8
- Status: done
- Priority: normal
- Owner: Codex
- Source: direct user request
- Added: 2026-09-29
- Updated: 2026-10-10
- Goal: Verify the released pre-write gate end-to-end in a live session: install the released plugin and run the archived task Plan's 5-step recipe (deny before an invocation, allow after, deny the next stage on spent evidence, escape hatch releases) — prefer CI for anything CI can cover, hand-run only the install-and-observe steps
- Task: Not promoted.
- Next action: Narrow to one pass: re-confirm install-and-observe on the current release, then close.
- Notes: **2026-09-29 用户要求：优先采用 CI 进行测试。** 理由来自 2026-09-27-capability-pre-write-gate 的实测：本机是 Windows + MSYS，整段 `hooks/smoke-test` 跑不完（无解释器章节因软链启动的二进制找不到 DLL 而中止，用未修改的 `origin/main` 在同一处同样失败），所以本地跑既不可靠也不完整；而 CI 的 smoke 矩阵（ubuntu/macos/windows）一次就给出权威结论，其中 `macos-latest` 正是 bash 3.2 + BSD userland 的判定环境。因此凡是 CI 结构上能覆盖的（接线、门矩阵、approve 对账、无解释器下限、Windows 套件）一律不要手工跑，缺什么就往 CI 里补；人手只跑 CI 覆盖不到的——即「装上发出去的插件后，真实会话里门是否真的拦下来」。
- 2026-10-01 实测（本机 Windows，插件已升到 1.1.2 = commit `5d4fccf`）：门对宿主真实投递的路径**拦下了**。在 `TaskFlowDocs/achieved/2026-09-30-release-ci-test-policy/` 写 `prd.md` 正文被拒，消息完整且含可复制的逃生舱命令：`TaskFlow pre-write gate blocked stage [PRD]: no capability invocation is recorded for this task version. Invoke a capability first — any Skill, agent, or MCP tool — then write the document. If no capability fits this phase, declare it:  bash hooks/task unaided PRD --considered "requirements elicitation and framing"`。随后调用 `agent-skills:spec-driven-development` 记录证据，重试即放行；`plan.md` 同理需要**另一次**能力调用（逐阶段新鲜度），v2 时改用 `task unaided` 亦放行（逃生舱有效）。同日 `hooks/task approve` 成功，说明 `released` 记录确实被写下——1.1.1 上卡死的正是这一步。**判据即行为差**：同一个 `prd.md` 在 1.1.1 上静默放行、在 1.1.2 上被拒。
- 2026-10-10 收窄（用户裁定）：原配方五步里，第 1 步（发版）、第 3–5 步的门矩阵与**反斜杠路径回归**现已被 CI 结构覆盖——`hooks/smoke-test` 已断言「宿主投递的反斜杠路径与正斜杠路径必须得到同一判定」（见 smoke-test 的 `A path's spelling must not decide the verdict` 段，引用 claude-code #83877 / #64432），三 host 矩阵每次 PR 与 main 推送都跑；evals 亦入 CI。**剩下的增量只有「装上已发布插件后，真实会话里门是否真的拦下来」这一条 CI 结构上覆盖不到的观察**（2026-10-01 已在 1.1.2 上观测到：不调能力写 prd.md 被拒、消息含 stage 与可复制的 task unaided 命令、调用后放行、写 spec.md 又被拒）。故收窄为：在当前已发布版本上复核一次安装与那三类观察，完成即关；未实测的 matcher 语义（Agent / mcp__.* 是否按宿主语义命中）一并作为该次复核的观测项。

配方见归档后的 `TaskFlowDocs/achieved/2026-09-27-capability-pre-write-gate/plan.md` Verification / Review。第 1 步发版已完成（1.1.1，tag `v1.1.1` = `6df863d`，pin `bf8dc96`）；第 2 步是全局安装，属项目路径之外，需用户许可或由用户执行；第 3–5 步为观察项：不调用任何能力直接写 `prd.md` 正文应被拒（消息含 stage、概念类、可复制的 `task unaided` 命令），`task unaided PRD --considered "requirements elicitation and framing"` 后重试应放行，紧接着写 `spec.md` 应被拒（逐阶段新鲜度）。

顺带核对宿主侧尚未实测的一项：matcher 是否真按宿主语义命中 `Agent` 与 `mcp__.*`（`Skill` 已实测同时触发两个事件且携带 `tool_input.skill`）。

## Release process: make the manual three-host catalog validation conditional and a

- ID: TF-20260928-3910fb
- Status: done
- Goal: Release process: make the manual three-host catalog validation conditional and add an automated $schema assertion, since that step is never exercised by CI and its only failure mode is already covered by release-check
- Task: `TaskFlowDocs/achieved/2026-11-07-release-manual-step/`
- Next action: None — completed and archived.

## Block the first body write of prd/spec/plan until a capability-class tool was ac

- ID: TF-20260927-5814d0
- Status: done
- Goal: Block the first body write of prd/spec/plan until a capability-class tool was actually invoked: the approve-time Skills check is shape-only and fires after every document exists, so 'invoked nothing' and 'compliant' stay indistinguishable
- Task: `TaskFlowDocs/achieved/2026-09-27-capability-pre-write-gate/`
- Next action: None — completed and archived.

## Gate PRD/Spec/Plan on real capability invocation: large tasks need one real invo

- ID: TF-20260923-230f49
- Status: done
- Goal: Gate PRD/Spec/Plan on real capability invocation: large tasks need one real invoke (or qualified Unaided with considered classes); approve validates the Skills/Tools record; TaskFlow maps foreign skill outputs into prd/spec/plan; inject concept-class candidates at doc time
- Task: `TaskFlowDocs/achieved/2026-09-23-capability-invoke-gate/`
- Next action: None — completed and archived.

## Fix hooks/merge-todo so a Removed record matches its live entry by ID token

- ID: TF-20260918-985164
- Status: done
- Goal: Fix hooks/merge-todo so a ## Removed record matches its live entry by ID token and deletion wins, then clear the duplicate IDs that resurrection left in todo.md.
- Task: `TaskFlowDocs/achieved/2026-09-22-merge-todo-removed/`
- Next action: None — completed and archived.

## Windows worktree misjudgement: `hooks/task` reads a `D:/` git dir as relative.

- ID: TF-20260920-9f3c07
- Status: done
- Goal: Fix the Windows worktree misjudgement so a drive-letter git dir is not read as relative to the root.
- Task: `TaskFlowDocs/achieved/2026-09-20-windows-git-path/`
- Next action: None — completed and archived.

## State in the Skill that personal supplements are local-only

- ID: TF-20260914-03
- Status: done
- Goal: State in the Skill that personal supplements are local-only and must not be committed to Git, and align this repository with that boundary.
- Task: `TaskFlowDocs/achieved/2026-09-14-personal-docs-git-boundary/`
- Next action: None — completed and archived.

## TF-20260913-03 — Pin stable marketplace installs to released revisions

- ID: TF-20260913-03
- Status: done
- Goal: Keep the marketplace catalog on `main` while pinning stable TaskFlow plugin installs to the immutable `v1.0.4` release commit.
- Task: `TaskFlowDocs/achieved/2026-09-13-pin-marketplace-release/`
- Next action: None — completed and archived.

## TF-20260911-02 — Allow appropriate tools to contribute to task documents

- Status: done
- Goal: Allow relevant tools and capabilities to contribute to task documents without forcing a tool chain.
- Task: `TaskFlowDocs/achieved/2026-09-07-tool-participation/`
- Next action: None — completed and archived.

## TF-20260911-03 — Audit further Hook automation opportunities

- Status: done
- Goal: Audit additional Hook automation opportunities while preserving approval and mutation boundaries.
- Task: `TaskFlowDocs/achieved/2026-09-10-audit-hook-opportunities/`
- Next action: None — completed and archived.

## TF-20260911-04 — Consolidate the packaged Skill layout

- Status: done
- Goal: Consolidate the packaged Skill layout and remove stale duplicate entrypoints.
- Task: `TaskFlowDocs/achieved/2026-09-10-consolidate-skill-layout/`
- Next action: None — completed and archived.

## TF-20260911-05 — Copy-first Task versioning

- Status: done
- Goal: Preserve superseded Task documents while retaining current roots during version transitions.
- Task: `TaskFlowDocs/achieved/2026-09-10-copy-first-versioning/`
- Next action: None — completed and archived.

## TF-20260911-06 — Limit TaskFlow to development requests

- Status: done
- Goal: Restrict automatic TaskFlow intake to development requests while preserving explicit opt-in.
- Task: `TaskFlowDocs/achieved/2026-09-10-limit-taskflow-scope/`
- Next action: None — completed and archived.

## TF-20260911-07 — Unblock autonomous capability invocation

- Status: done
- Goal: Make capability selection, invocation, review, and recording explicit without forcing a provider or tool.
- Task: `TaskFlowDocs/achieved/2026-09-10-unblock-capability-invocation/`
- Next action: None — completed and archived.

## TF-20260911-08 — Update and review TaskFlow plugin

- Status: done
- Goal: Fix, publish, install, and verify the TaskFlow plugin and Windows Hook behavior.
- Task: `TaskFlowDocs/achieved/2026-09-10-update-review-plugin/`
- Next action: None — completed and archived.

## T-20260910-001 — Enforce repository-governed fork development

- ID: T-20260910-001
- Status: done
- Goal: Make the TaskFlow plugin follow fork/upstream development discipline and applicable repository, personal-supplement, code-style, contributing, and roadmap documents, creating missing governance documents with the user when needed.
- Task: `TaskFlowDocs/achieved/2026-09-10-repository-governed-development/`
- Next action: None — completed and archived.

## TF-20260910-08 — Reduce TaskFlow token use with lifecycle scripts

- ID: TF-20260910-08
- Status: done
- Goal: Replace repetitive Agent reads and Markdown rewrites with bounded lifecycle commands where automation saves tokens.
- Task: `TaskFlowDocs/achieved/2026-09-10-token-saving-lifecycle-scripts/`
- Next action: None — completed and archived.

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

- ID: T-20260908-007
- Status: done
- Goal: Allow TaskFlow to coordinate with host/harness hooks (Claude Code and Codex) via a flat `hooks/` of extensionless bash scripts + per-host JSON + `run-hook.cmd`, plus a SessionStart context summary, without automation writing core documents or skipping approval.
- Task: `TaskFlowDocs/achieved/2026-09-08-runtime-hooks/`
- Next action: None — completed and archived.

## T-20260908-006 — Reduce TaskFlow workflow token cost

- ID: T-20260908-006
- Status: done
- Goal: Reduce Agent token consumption in the TaskFlow workflow while preserving traceability and reliability.
- Task: `TaskFlowDocs/achieved/2026-09-08-token-efficiency/`
- Next action: None — completed and archived.

## T-20260908-003 — Archive completed legacy TaskFlow tasks

- ID: T-20260908-003
- Status: done
- Goal: Add Todo traceability and archive the completed standards-root and Todo-promotion tasks.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/`
- Next action: None — completed and archived.

## T-20260908-004 — Repository standards and TaskFlowDocs root

- ID: T-20260908-004
- Status: done
- Goal: Preserve the completed repository-standards and TaskFlowDocs-root design as achieved history.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-standards-and-doc-root/`
- Next action: None — completed and archived.

## T-20260908-005 — Todo intake and promotion workflow

- ID: T-20260908-005
- Status: done
- Goal: Preserve the completed Todo intake and promotion design as achieved history.
- Task: `TaskFlowDocs/achieved/2026-09-07-todo-intake-and-promotion/`
- Next action: None — completed and archived.

## T-20260908-002 — Repair TaskFlow activation and archival consistency

- ID: T-20260908-002
- Status: done
- Goal: Ensure TaskFlow applies to every repository work request and keeps task, Todo, and achieved locations consistent.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/`
- Next action: None — completed and archived.

## T-20260908-001 — Todo-first intake and achieved-task retrieval

- ID: T-20260908-001
- Status: done
- Goal: Make Todo mandatory for every direct or imported requirement and retrieve achieved tasks before material maintenance.
- Task: `TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/`
- Next action: None — completed and archived.

## Make repository-docs index the primary routing record and maintain/inject it thr

- ID: TF-20260911-01
- Status: done
- Goal: Make repository-docs index the primary routing record and maintain/inject it through SessionStart hook
- Task: `TaskFlowDocs/achieved/2026-09-11-index-hook-routing/`
- Next action: None — completed and archived.

## Identify the current TaskFlow task before phase routing

- ID: TF-20260911-02
- Status: done
- Goal: Identify the current TaskFlow task before phase routing
- Task: `TaskFlowDocs/achieved/2026-09-12-current-task-routing/`
- Next action: None — completed and archived.

## Add explicit cross-platform runtime preflight for Windows Python dependencies

- ID: TF-20260911-03
- Status: done
- Goal: Add explicit cross-platform runtime preflight for Windows Python dependencies
- Task: `TaskFlowDocs/achieved/2026-09-12-windows-runtime-preflight/`
- Next action: None — completed and archived.

## Harden the Windows hook launcher argument forwarding and failure reporting

- ID: TF-20260911-04
- Status: done
- Goal: Harden the Windows hook launcher argument forwarding and failure reporting
- Task: `TaskFlowDocs/achieved/2026-09-12-windows-launcher/`
- Next action: None — completed and archived.

## Validate repository-document index paths and protect concurrent writes

- ID: TF-20260911-05
- Status: done
- Goal: Validate repository-document index paths and protect concurrent writes
- Task: `TaskFlowDocs/achieved/2026-09-13-index-safety/`
- Next action: None — completed and archived.

## Add Linux and Windows CI coverage for TaskFlow hooks

- ID: TF-20260911-06
- Status: done
- Goal: Add Linux and Windows CI coverage for TaskFlow hooks
- Task: `TaskFlowDocs/achieved/2026-09-13-hooks-ci-matrix/`
- Next action: None — completed and archived.

## Reduce SessionStart context output to the active task by default

- ID: TF-20260911-07
- Status: done
- Goal: Reduce SessionStart context output to the active task by default
- Task: `TaskFlowDocs/achieved/2026-09-13-session-context/`
- Next action: None — completed and archived.

## Model optional repository documents and consume SessionStart event input

- ID: TF-20260911-08
- Status: done
- Goal: Model optional repository documents and consume SessionStart event input
- Task: `TaskFlowDocs/achieved/2026-09-13-event-aware-docs/`
- Next action: None — completed and archived.

## Prepare TaskFlow v1.0.4 release

- ID: TF-20260913-02
- Status: done
- Goal: Prepare TaskFlow v1.0.4 release
- Task: `TaskFlowDocs/achieved/2026-09-13-release-v1-0-4/`
- Next action: None — completed and archived.

## Revise release flow to support direct tag releases

- ID: TF-20260913-01
- Status: done
- Goal: Revise release flow to support direct tag releases
- Task: `TaskFlowDocs/achieved/2026-09-13-revise-release-flow/`
- Next action: None — completed and archived.

## Restore macOS portability for hooks and smoke tests

- ID: TF-20260914-01
- Status: done
- Goal: Make the hooks and smoke tests pass on stock macOS (bash 3.2 + BSD sed), cover macOS and the evals in CI, and align plugin license metadata with the AGPL-3.0 LICENSE.
- Task: `TaskFlowDocs/achieved/2026-09-14-macos-hook-portability/`
- Next action: None — completed and archived.

## Map TaskFlow phases to the concept class each one corresponds to in external wor

- ID: TF-20260915-01
- Status: done
- Goal: Map TaskFlow phases to the concept class each one corresponds to in external workflows, so PRD/Spec/Plan work selects the right capability instead of working unaided.
- Task: `TaskFlowDocs/achieved/2026-09-15-phase-concept-mapping/`
- Next action: None — completed and archived.

## Stop tracking TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md: the workflow draft is not

- ID: TF-20260914-05
- Status: done
- Goal: Stop tracking TaskFlowDocs/TASKFLOW_WORKFLOW_DRAFT.md: the workflow draft is not part of the TaskFlowDocs artifact system.
- Task: `TaskFlowDocs/achieved/2026-09-14-untrack-workflow-draft/`
- Next action: None — completed and archived.

## Require a short-lived branch or dedicated worktree before implementation starts,

- ID: TF-20260914-04
- Status: done
- Goal: Require a short-lived branch or dedicated worktree before implementation starts, and route contribution rules to the design phase.
- Task: `TaskFlowDocs/achieved/2026-09-14-branch-and-worktree-gate/`
- Next action: None — completed and archived.

## Run TaskFlow hooks without a Python interpreter

- ID: TF-20260915-82ec4c
- Status: done
- Goal: Run TaskFlow hooks without a Python interpreter
- Task: `TaskFlowDocs/achieved/2026-09-15-no-python-hooks/`
- Next action: None — completed and archived.

## Make concurrent Todo updates merge cleanly in parallel-task branches

- ID: TF-20260915-02
- Status: done
- Goal: Make concurrent Todo updates merge cleanly in parallel-task branches
- Task: `TaskFlowDocs/achieved/2026-09-15-todo-merge-driver/`
- Next action: None — completed and archived.

## Fix hook integrity so archived versions are never polluted, unimplemented work c

- ID: TF-20260915-0f6dda
- Status: done
- Goal: Fix hook integrity so archived versions are never polluted, unimplemented work cannot pass the approval gates, and task documents follow the user's language
- Task: `TaskFlowDocs/achieved/2026-09-15-hook-integrity/`
- Next action: None — completed and archived.

## Publish TaskFlow v1.0.5 with the no-runtime hooks, the Todo merge driver, and th

- ID: TF-20260915-a9cabf
- Status: done
- Goal: Publish TaskFlow v1.0.5 with the no-runtime hooks, the Todo merge driver, and the hook-integrity fixes
- Task: `TaskFlowDocs/achieved/2026-09-15-release-v1-0-5/`
- Next action: None — completed and archived.

## Cut the mechanical overhead out of a release: one version-consistency check, a r

- ID: TF-20260915-1f0f66
- Status: done
- Goal: Cut the mechanical overhead out of a release: one version-consistency check, a release document rule, and an archive that clears the Todo next action.
- Task: `TaskFlowDocs/achieved/2026-09-15-release-friction/`
- Next action: None — completed and archived.

## Detect a Todo entry that a merge dropped, so a silent loss cannot reach main unn

- ID: TF-20260916-2561e8
- Status: done
- Goal: Detect a Todo entry that a merge dropped, so a silent loss cannot reach main unnoticed.
- Task: `TaskFlowDocs/achieved/2026-09-16-todo-entry-loss-detection/`
- Next action: None — completed and archived.

## Hold Todo protection on the web-UI merge path

- ID: TF-20260916-2a89e2
- Status: done
- Goal: Make the Todo merge protection hold on the path where merges actually happen: a hosting web-UI pull-request merge.
- Task: `TaskFlowDocs/achieved/2026-09-16-web-ui-merge-loss-guard/`
- Next action: None — completed and archived.

## Repair the duplicate Todo ID that the old counter-derived scheme shipped: two li

- ID: TF-20260916-01bd1a
- Status: done
- Goal: Repair the duplicate Todo ID that the old counter-derived scheme shipped: two live entries both carry TF-20260915-01, so an ID lookup can resolve to the wrong task.
- Task: `TaskFlowDocs/achieved/2026-09-16-duplicate-todo-id/`
- Next action: None — completed and archived.

## Isolate a task before its documents are written, and make the choice auditable

- ID: TF-20260916-ab381b
- Status: done
- Goal: Isolate a task before its documents are written, and make the choice auditable: task documents are created in Phase 1 while the branch/worktree rule only applied from Phase 5, so documents landed in a shared checkout (usually another task's branch) and could not be checked out away; separately, the Plan's capability-selection section was marked optional, so "chose not to invoke" and "forgot the step" were indistinguishable.
- Task: `TaskFlowDocs/achieved/2026-09-16-capability-selection-enforcement/`
- Next action: None — completed and archived.

## Detect a task directory that no Todo entry references

- ID: TF-20260916-a357ee
- Status: done
- Goal: Detect a task directory that no Todo entry references, so a lost Todo record cannot leave orphaned task documents behind.
- Task: `TaskFlowDocs/achieved/2026-09-23-orphan-task-dirs/`
- Next action: None — completed and archived.

## Publish TaskFlow v1.0.6 with the CodeBuddy host, the Todo merge-drop audit, and the release version check

- ID: TF-20260917-b7bc40
- Status: done
- Goal: Publish TaskFlow v1.0.6 with the CodeBuddy host, the Todo merge-drop audit, and the release version check
- Task: `TaskFlowDocs/achieved/2026-09-17-release-v1-0-6/`
- Next action: None — completed and archived.

## Make the release atomic: push the marketplace pin and the release tag in one ato

- ID: TF-20260917-a608b7
- Status: done
- Goal: Make the release atomic: push the marketplace pin and the release tag in one atomic push so the catalog never names a tag that is missing or stale
- Task: `TaskFlowDocs/achieved/2026-09-17-atomic-release-push/`
- Next action: None — completed and archived.

## Refresh both READMEs so they document the shipped surfaces: the hooks/tools/eval

- ID: TF-20260918-13ff42
- Status: done
- Goal: Refresh both READMEs so they document the shipped surfaces: the hooks/tools/evals trees, the verification and CI checks, and the release process link
- Task: `TaskFlowDocs/achieved/2026-09-18-readme-refresh/`
- Next action: None — completed and archived.

## The plugin's hook launcher installs without the executable bit, so every Unix Se

- ID: TF-20260918-b0f73a
- Status: done
- Goal: The plugin's hook launcher installs without the executable bit, so every Unix SessionStart hook fails with Permission denied
- Task: `TaskFlowDocs/achieved/2026-09-18-hook-launcher-exec-bit/`
- Next action: None — completed and archived.

## Restore the zh-CN manifest count that a conflict resolution reverted, and rule on conflict-side review

- ID: TF-20260918-ad8348
- Status: done
- Goal: Restore the zh-CN manifest count that a conflict resolution reverted, and decide whether a resolved conflict needs a recorded side-by-side review before it is pushed.
- Task: `TaskFlowDocs/achieved/2026-09-18-conflict-side-review/`
- Next action: None — completed and archived.

## Fold the deterministic Todo bookkeeping into hooks/task instead of Agent edits:

- ID: TF-20260918-e2317d
- Status: done
- Goal: Fold the deterministic Todo bookkeeping into hooks/task instead of Agent edits: the Next action, Updated, and status fields are fixed writes with no semantic judgment, and writing them by hand spends tokens.
- Task: `TaskFlowDocs/achieved/2026-09-18-todo-field-writes/`
- Next action: None — completed and archived.

## Make the task complete transaction fail-safe: it marks both core documents compl

- ID: TF-20260918-e7c041
- Status: done
- Goal: Make the task complete transaction fail-safe: it marks both core documents completed before hooks/archive runs, so any archive failure leaves the task half-archived with no rollback.
- Task: `TaskFlowDocs/achieved/2026-09-22-archive-transaction/`
- Next action: None — completed and archived.

## Record approval in the plan from a hook instead of hand-editing four fixed-forma

- ID: TF-20260918-454ac4
- Status: done
- Goal: Record approval in the plan from a hook instead of hand-editing four fixed-format fields, and fix hooks/version writing an Approval block that disagrees with hooks/task's template.
- Task: `TaskFlowDocs/achieved/2026-09-23-task-approve/`
- Next action: None — completed and archived.

## Fix task get silently dropping indented Notes continuation lines: it prints only

- ID: TF-20260918-9acf57
- Status: done
- Goal: Fix task get silently dropping indented Notes continuation lines: it prints only lines starting with '- ', so a second Notes bullet written with the repo's two-space indent is absent from the output with no warning.
- Task: `TaskFlowDocs/achieved/2026-09-22-task-get-notes/`
- Next action: None — completed and archived.

## Make hooks/version write the same five-field Approval block hooks/task generates

- ID: TF-20260919-b7821b
- Status: done
- Goal: Make hooks/version write the same five-field Approval block hooks/task generates, so the plan gate and the version reset agree.
- Task: `TaskFlowDocs/achieved/2026-09-23-version-approval-shape/`
- Next action: None — completed and archived.

## Measure whether delegating exploration to subagents actually reduces main-thread

- ID: TF-20260919-90797c
- Status: inbox
- Priority: normal
- Owner: Codex
- Source: user request
- Added: 2026-09-19
- Updated: 2026-11-11
- Goal: Measure whether delegating exploration to subagents actually reduces main-thread context, before adopting it as guidance.
- Task: Not promoted.
- Next action: 设计少量同题对照，分别记录主线上下文、含子 Agent 的总 Token、耗时与事实质量；对搜索倾向设置独立对照。
- Notes: **2026-09-19 用户提出**：subagent 委派能不能省 token，要**实测**才知道，别先写进指引。
- **2026-10-11 用户提出**：用户观察「用了 TaskFlow 之后 Agent 似乎变得不喜欢做网络搜索」，并要求先查是不是真的。用户明确此条**不是**要强制规定调用网络搜索，只是这条倾向值得被测量。
- 2026-11-11 用户要求与整体流程 Token 优化一并调查；样本不足时不作普遍结论。

**查到的可测痕证**：72 个 achieved 任务里 63 个 `plan.md` 的 `## Reference Pointers` 非空，共 **253 条 bullet，含 URL 的 0 条**；其中 70 条是反引号包起的仓库内路径。放宽到整个任务目录，只有 17/72 出现过任何 URL，主机分布 github.com 39、docs.anthropic.com 2、developers.openai.com 2 —— 第三方外部来源合计 4 条。也就是说名为「参考指针」的槽位已经退化成「我读了哪些仓库文件」。

**指向该退化的三处机制**（推断，非因果）：(1) `SKILL.md:54` 澄清阶段唯一的动作指令 `inspect` 枚举八项全在仓库内或 Agent 自身状态里，没有任何一项指向仓库外；(2) 没有任何阶段拥有「取外部事实」这个动作——`SKILL.md:168` 的 `searching external sources` 挂在 phase 2，而 phase 2 有 `reference/` 产物要写，模型里它是**写**的阶段，不先有「我要写 reference 笔记」的决定就不会触发去外部取事实；(3) 会话开场 `summarize-state` 注入的全是内部结论，`SKILL.md:32` 又说 routing record 先读。附带：`WebSearch`/`WebFetch` 被 R12（`achieved/2026-09-27-capability-pre-write-gate/prd.md:61`）排除在能力谓词外，于是搜索在 TaskFlow 里既不拦也不奖。

**边界**：这是机制推断 + 行为统计，不是因果证明。本仓库自足，多数任务本就不需要外部来源，0/253 里有多大比例由此解释无法从数据分开——要用对照（同一任务，加/不加这套注入各跑一次）才能分开，与 [[TF-20260919-90797c]] 原有的委派测量同源。相关：TF-20261009-8abbd6（能力选择的记录位）

  **为什么值得测而不是直接采纳**：我给的论证是「读 `todo.md` 22k、整读 `SKILL.md`、反复读 `plan.md` 都在主线里做，丢给 subagent 就只回结论」。这条论证**在我这个会话里是空的**——我一次 subagent 都没用，所以那是推断不是观测。

  **反方向的可能（必须先承认）**：subagent 有 setup 成本（重建 prompt、加载工具、自己走一遍检索），一次小读取委派出去可能**比直接读更贵**；它的结论还要回主线，如果结论本身很长，省的就不多。所以「委派总是更省」很可能是错的，**该测的是阈值**：多大的读取/搜索开始值得委派。

  **测法（草案）**：同一件事（例如「找出 v1.0.6 到 main 之间哪些改动属于用户可见」）分别用「主线直接做」与「委派 subagent」各跑一次，记两边的：(a) 主线上下文增量，(b) 总 token（含 subagent 自身），(c) 结论质量是否够用。判据要**同时**看 (a) 与 (b)——只看主线增量会把成本藏进 subagent 里。

  **可用的观测手段**：`/context` 看占用；会话 jsonl 在 `~/.claude/projects/<path>/` 下可解析每轮的输入 token；`ctx stats` 若可用。选一个能复现的，别靠感觉。

  **落地条件**：只有实测显示某类探索稳定更省，才写进 `SKILL.md` 的 Phase 2/6（探索与复核）或 `CLAUDE.md` 的工作方式；否则结论就是「不采纳」，那也是有效结论。相关：本条与 `TF-20260919-76e7fb` 无关，属会话成本治理。

## Adapt TaskFlow to the DeepSeek Harness (dsh) as a fourth host: ship a dsh plugin

- ID: TF-20260919-55110d
- Status: done
- Goal: Adapt TaskFlow to the DeepSeek Harness (dsh) as a fourth host: ship a dsh plugin bundle that self-wires the existing skill and hooks with no manual config
- Task: `TaskFlowDocs/achieved/2026-09-19-dsh-host/`
- Next action: None — completed and archived.

## Take a release out of the TaskFlow task workflow: RELEASE.md runs directly on th

- ID: TF-20260919-40eca2
- Status: done
- Goal: Take a release out of the TaskFlow task workflow: RELEASE.md runs directly on the base checkout with no Todo item, task directory, branch, or PRD/Plan, and its record is the CHANGELOG section and the GitHub Release body.
- Task: `TaskFlowDocs/achieved/2026-09-19-release-flow-exception/`
- Next action: None — completed and archived.

## Map the personal rule to a single personal.md: one file, each rule in its own se

- ID: TF-20260919-495145
- Status: done
- Goal: Map the personal rule to a single personal.md: one file, each rule in its own section with its own scope etc. The repository-docs index names personal.md and explains its origin (local-only, never committed) and purpose (personal rules that cannot override repository documents).
- Task: `TaskFlowDocs/achieved/2026-09-23-single-personal-md/`
- Next action: None — completed and archived.

## Record the host SessionStart session_id in the active task's sessions.md

- ID: TF-20260914-02
- Status: done
- Goal: Record the host SessionStart session_id in the active task's sessions.md so a cross-session resume has a real, platform-specific identifier.
- Task: `TaskFlowDocs/achieved/2026-09-14-session-id-record/`
- Next action: None — completed and archived.

## Stop `TaskFlowDocs/todo.md` from growing without bound: it is at 877 lines, 45%

- ID: TF-20260919-6b4e21
- Status: done
- Goal: Stop `TaskFlowDocs/todo.md` from growing without bound: it is at 877 lines / 50 KB, of which the 47 `done` entries are 45% (22.6 KB) and the 18 live entries (`inbox` 12, `promoted` 2, `in_progress` 4) are under a third — the file is a growing archive that every task still has to read.
- Task: `TaskFlowDocs/achieved/2026-10-19-todo-done-compaction/`
- Next action: None — completed and archived.

## Cut the mechanical overhead out of a release without adding any authority to it

- ID: TF-20260919-c41f8a
- Status: done
- Goal: Cut the mechanical overhead out of a release without adding any authority to it: write the six fixed version literals from one command, move the CHANGELOG section into the tagged commit so the tag is immutable, and make a stale release record fail CI instead of passing.
- Task: `TaskFlowDocs/achieved/2026-09-21-release-overhead/`
- Next action: None — completed and archived.

## `task intake` inserts a new entry into the previous section instead of `## Items`

- ID: TF-20260921-337ab8
- Status: done
- Goal: Fix task intake inserting a new entry into the previous section instead of the Items section, and its insertion point landing inside the Removed section.
- Task: `TaskFlowDocs/achieved/2026-09-22-todo-intake-insert/`
- Next action: None — completed and archived.

## Removed

- ID: TF-20260921-4d8ae2 (removed 2026-09-22: stale: fix merged on main in PR 46 (02c1441); entry still said awaiting review)
- ID: TF-20260919-76e7fb (removed 2026-09-22: stale: delivered by release-flow-exception; merged in PR 42 (caad35b))
- ID: TF-20260919-2877ca (removed 2026-09-22: stale: delivered by release-flow-exception; merged in PR 42 (caad35b))
- ID: TF-20260918-88e04c (removed 2026-09-23: Covered by umbrella e7c041 / 2026-09-22-archive-transaction (R3 stage print + branch rule).)
- ID: TF-20260918-172455 (removed 2026-09-23: Covered by umbrella e7c041 / 2026-09-22-archive-transaction (R4 three-field rewrite lock).)
- ID: TF-20261008-ee2c27 (removed 2026-10-08: Absorbed into TaskFlowDocs/2026-10-08-task-open-and-continuation/ (R2): the same SKILL.md triage paragraph carries the overlap-report obligation, so a separate task would re-edit the same files)
- ID: TF-20261008-73facd (removed 2026-10-08: Absorbed into TaskFlowDocs/2026-10-08-task-open-and-continuation/ (R3): parent-child coordination edits the same SKILL.md section and artifacts.md Related Tasks block)
- ID: TF-20261008-6b6ecf (removed 2026-10-08: probe entry created while verifying the intake exit-code contract; not a real request)
- ID: TF-20261008-4d37b2 (removed 2026-10-10: Absorbed into TF-20261008-a4454d: both add guidance beside the same SKILL.md update points and assertions over the same document-vs-hooks reconciliation surface, so a separate task would re-edit the same files)
- ID: TF-20261008-84a0ce (removed 2026-10-10: Absorbed into TF-20261001-efbc51: same failure mode, landing somewhere other than the assumed place — the hook anchors and the missing move procedure are its two halves, and one task changes both)
- ID: TF-20261025-33b2c4 (removed 2026-10-25: Falsified by 2026-10-25-gate-desync-diagnosis A3: git applies no ignore rule to a tracked path, so a force-added copy stays visible in git status and check-ignore returns false — the concern the entry raised cannot occur)
- ID: TF-20261027-e8c6dc (removed 2026-11-01: superseded by TF-20261031-61b973, which restated and delivered it)
- ID: TF-20261102-d14d22 (removed 2026-11-02: folded into TF-20261102-7a9caa: one task covers the binding, the release format rule and the host-coverage rule)
- ID: TF-20261102-ee1698 (removed 2026-11-02: folded into TF-20261102-7a9caa: one task covers the binding, the release format rule and the host-coverage rule)

## 收窄 artifact-language 规则，使非 hook 匹配的章节标题可使用用户语言

- ID: TF-20260928-07c659
- Status: done
- Goal: 收窄 artifact-language 规则，使非 hook 匹配的章节标题可使用用户语言
- Task: `TaskFlowDocs/achieved/2026-09-15-hook-integrity/` (v2)
- Next action: None — completed and archived.

## Make the artifact-language rule actually bind: the trae-host PRD and Plan were w

- ID: TF-20261009-887511
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: user request 2026-10-09, recurrence found while writing the trae-host documents
- Added: 2026-10-09
- Updated: 2026-10-09
- Goal: Make the artifact-language rule actually bind: the trae-host PRD and Plan were written entirely in English even though the rule and its prior ruling (TF-20261001-51d9c8) are in force, because the phase capability supplied an English skeleton and nothing makes the drafter translate its own prose or flags it when it does not. Decide the mechanism and the detection
- Task: Not promoted.
- Next action: Decide the wording or mechanism that makes the drafter translate its own prose, and add a detection the next silent English run trips
- Notes: Recurrence of TF-20261001-51d9c8 with the same root cause recorded there: the phase capability brought an English skeleton and nothing carried the rule onto the prose underneath it.

## Stop hand-writing a bespoke manual install section per host in the host-facing d

- ID: TF-20261009-99045e
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: user request 2026-10-09
- Added: 2026-10-09
- Updated: 2026-10-09
- Goal: Stop hand-writing a bespoke manual install section per host in the host-facing docs: for each host state whether a real plugin or marketplace install command exists and use it where one does, and define one shared manual-install procedure (copy the skill directory plus write the host hooks file) that each host section instantiates, instead of a per-host copy/paste block with no stated reason why an install command is absent
- Task: Not promoted.
- Next action: Clarify and promote when ready.

## Make one order binding: entering work enters TaskFlow first, and capabilities ar

- ID: TF-20261009-cc463b
- Status: done
- Goal: Make one order binding: entering work enters TaskFlow first, and capabilities are selected and used inside the phase. Today the applicability gate and the phase-to-capability step are separate rules with no stated order, so a session can research before TaskFlow and then have no stage to attribute that research to, which is what forces a throwaway invocation when the document is finally written; or skip TaskFlow entirely; or never consider a phase's capability class because no available capability advertises the phase name. A phase's selection must also be able to record work already done for it, instead of requiring a fresh call the gate can find
- Task: `TaskFlowDocs/achieved/2026-10-10-taskflow-first-order/`
- Next action: None — completed and archived.

## Stop duplicating changelog/history content across prd.md, plan.md and spec.md: e

- ID: TF-20261011-e27329
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: direct user request
- Added: 2026-10-11
- Updated: 2026-11-11
- Goal: Stop duplicating changelog/history content across prd.md, plan.md and spec.md: each document repeats the same change-log or history narrative, which is pure token waste. Assign the history/changelog a single owning document and have the others reference it instead of restating it.
- Task: Not promoted.
- Next action: 抽样核实 PRD、Spec、Plan 的语义和历史重复，只修当前模板或规则中证实的重复。
- Notes: 2026-11-11 用户要求纳入整体流程 Token 优化，不改写既有归档文档。

## Agree on what a closed Step is, so `completed` stops passing one check

- ID: TF-20261027-131c2b
- Status: done
- Goal: Make `completion-gate` and `hooks/task progress` mean the same thing by a closed Step, so the word `completed` cannot be refused by one and accepted by the other.
- Task: `TaskFlowDocs/achieved/2026-10-27-close-step-status/`
- Next action: None — completed and archived.

## Stay present inside a long implementation run, not only at the prompt

- ID: TF-20261027-e4ba77
- Status: done
- Goal: Keep TaskFlow present between the steps of one implementation run, so a long turn cannot leave the approved Plan behind while nothing in the workflow speaks up again.
- Task: `TaskFlowDocs/achieved/2026-10-29-midturn-presence/`
- Next action: None — completed and archived.

## Make a task record whether its conclusion depends on a fact from outside this re

- ID: TF-20261031-61b973
- Status: done
- Goal: Make a task record whether its conclusion depends on a fact from outside this repository, and require a real search when it does — so external evidence is either gathered deliberately or explicitly ruled out, never skipped by default
- Task: `TaskFlowDocs/achieved/2026-10-31-external-facts/`
- Next action: None — completed and archived.

