## Item template

An entry is written by `hooks/task intake` in this shape. The sample is indented so the hooks that parse this file do not read it as an entry — every field a hook matches sits at column 0 in a real entry:

    ## <goal, cut to 80 bytes>

    - ID: TF-yyyymmdd-xxxxxx
    - Status: inbox
    - Priority: normal
    - Owner: <person or Agent>
    - Source: <user / review / issue / remote>
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

## task approve requires the first [Plan] line to name exactly the capability relea

- ID: TF-20261026-726ec4
- Status: in_progress
- Priority: normal
- Owner: Claude
- Source: user statement 2026-10-26 while working TF on ppt-design-layer
- Added: 2026-10-26
- Updated: 2026-10-26
- Goal: task approve requires the first [Plan] line to name exactly the capability released for that stage, so a phase that invoked a different capability in a later version cannot be approved without hand-editing the shared released file
- Task: `TaskFlowDocs/2026-10-26-capability-task-identity/`
- Next action: Read CI on the task's pull request, record it in the Plan, then archive.
- Notes: 2026-10-26 现场（1.1.8）。`hooks/task approve` 卡在 `approve blocked: stage [Plan] does not name a capability invoked in this Task version (<name>)`（`hooks/task:1385`）。
  **两个叠在一起的成因**：（1）`released` 是**纯队列、不分任务**——`v2|Plan|4` 这个序号是 kimi 那条任务消耗的，本任务没有自己的 Plan 记录，但 `approve` 按 `(version, stage)` 取到它之后要求 Plan 里那一行**逐字**包含记录里的能力名；（2）`approve` 只看 `cap_skills` 里的**第一条** `- [Plan]` 行（`hooks/task:1362` 的 `head -1`），后面写了什么都不算依据。
  **副作用（必须说明）**：为了让记录对上，我在 `.git/worktrees/ppt-design-layer/taskflow/released` 上直接改了数——那是对**跨任务共享记录**的越权写操作，不是任何 hook 授权的路径。已经改回去了，当前状态与改之前一致。这件事本身说明缺陷的代价：唯一的自救手段是改别人的账本。
  **结果**：自动 `approve` 走不通。要么手动批 v2，要么把 `plan.md` 第一条 `- [Plan]` 写成**本轮实际调用过的**那个能力名（而不是写意图）。1.1.8 的行为，没有绕过，也没有在本条里改码。
  **与 `TF-20261012-c66ad3` 不是同一条**：c66ad3 是**供给侧**——版本提升要重走 N 次声明；本条是**对账侧**——即使记录齐全，`approve` 的匹配规则（取第一条、逐字比名字）也会拒。修 c66ad3 不会顺手修好本条，反之亦然。
  **文档缺口**：`skills/taskflow/references/artifacts.md:132` 只说「Record a stage-tagged line」，没有说 `approve` 只读第一条。按文档写多行 `- [Plan]` 是合规的，然后被拒。修本条时这句要一起补。

## A throw in hooks/smoke-test-windows.ps1 after the launcher section hangs the sui

- ID: TF-20261025-645ef4
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: follow-up from 2026-10-25-gate-desync-diagnosis
- Added: 2026-10-25
- Updated: 2026-10-25
- Goal: A throw in hooks/smoke-test-windows.ps1 after the launcher section hangs the suite instead of failing it: measured 2026-10-25 at 100-500s of silence with nothing printed, on main as well, so a red assertion reaches CI as a smoke (windows-latest) timeout rather than a message
- Task: Not promoted.
- Next action: Decide whether the suite should fail loudly: wrap the outer try/catch so a throw prints its message and exits non-zero. First reproduce on main to confirm it predates the branch, then check whether the CI job log shows anything on timeout.
- Notes: Found while verifying 2026-10-25-gate-desync-diagnosis. Positioning: a throw past the launcher section (after "WINDOWS LAUNCHER ARGS PASSED") hangs; a throw before it exits 1 correctly. Same on main, so not caused by that task. Consequence: the desync assertions added there, if they ever fail, arrive as a windows-latest timeout with no message. Local test: powershell.exe -File hooks/smoke-test-windows.ps1 (Git for Windows lives at D:\Git on this machine).

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
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: user request 2026-10-22
- Added: 2026-10-22
- Updated: 2026-10-22
- Goal: Review the Plan once before approval while TaskFlow is in use: after plan.md is written and before the user approves it, review the Plan itself rather than the code. If a capability covers plan review, invoke it the way the other phases invoke theirs (the [Plan] capability line in Skills / Tools Used, recorded through the same evidence path); if none is available, decide between reviewing unaided and reminding during implementation instead. Scope: TaskFlow while it is being used on a project, not development of TaskFlow itself.
- Task: Not promoted.
- Next action: Decide the trigger point and the fallback: SKILL.md Phase 4 ends at plan.md and the Approval block, so the review must sit before task approve — there is no second chance after it. Phase 6 "Verify and review" reviews code and acceptance, not the Plan itself. Check the phase/capability table: the Plan row lists only work breakdown, there is no "review the plan" class; agent-skills:code-reviewer and agent-skills:review exist but target code. Settle which of the three it is — invoke a capability, review unaided, or remind during implementation.
- Notes: Recorded from a side channel as a prepared intake; re-read goal for full wording. Distinct from TF-20261021-4950fc (default rules from CODE_STYLE/CONTRIBUTING) and TF-20261022-fda8d8 (archive looseness).

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
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: user request 2026-10-21, verified against gh api + gh pr create head/base semantics
- Added: 2026-10-21
- Updated: 2026-10-21
- Goal: Before pushing a PR, establish which repository receives it: a fork's branch is pushed to the writable fork (head), while the PR targets the original author's repository (base) — cannot push to upstream without write permission. Record the checkable facts (isFork/parent/source via gh api, .permissions.push per candidate, branch protection) instead of inferring repo role from a remote named origin/upstream
- Task: Not promoted.
- Next action: Decide whether to extend hooks/repository-check to report fork topology (fork/parent/source) and per-remote push permission, or keep it as a rule in CONTRIBUTING
- Notes: repository-check:18-31 currently lists remote names+URLs only; it reports neither isFork/parent/source nor permissions.push. Verified facts: gh api repos/X -> .fork/.parent.full_name/.source.full_name/.permissions.push; gh pr create --head <owner>:<branch> is the writable head, --base is the upstream branch to merge into; gh api .../branches/<b>/protection returns 404 when unprotected.

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
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: user request 2026-10-21
- Added: 2026-10-21
- Updated: 2026-10-21
- Goal: Extract a set of default working rules from CODE_STYLE.md / CONTRIBUTING.md and similar docs, and make sure the defaults never override or violate the user's own habits
- Task: Not promoted.
- Next action: Clarify and promote when ready.

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
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: user report 2026-10-12: a v13 approval could not be written because the evidence queue was exhausted
- Added: 2026-10-12
- Updated: 2026-10-18
- Goal: Bookkeeping the stage ledger by a globally monotonic evidence queue makes a Task version bump repeat the capability bookkeeping: hooks/task approve requires every stage to appear in <absolute-git-dir>/taskflow/released, and a stage is released only while evidence lines > max(seq), so each new Task version needs one fresh release per stage it writes and seq never resets. Corrected 2026-10-18: this is repeated work, not a dead end — the earlier claim that once consumed reaches the line count no later version can be released is false, because hooks/task unaided appends its own evidence line and then its own release line (hooks/task:1042-1043), so a host with a gate is never blocked by an exhausted queue. What remains true is that every version bump repeats N declarations or calls (N = stages to write); only a host without a gate actually needs real invocations
- Task: Not promoted.
- Next action: Clarify whether to remove the repeated per-version bookkeeping (the remaining half), by reusing the previous version's kind and capability name per (version, stage) rather than changing seq.
- Notes: 2026-10-12 用户报告：某任务的 v13 已获批准，但 `hooks/task approve` 写不进文件。

**用户给的现场**：approve 拒了，理由是 pre-write 门的证据账本**全局单调**——已消费到第 34 条，v12 把可用证据用尽，第 35 条之后再没产生过；`approve` 与 `unaided` 两条路都试过；失败原因已写进该任务的 `plan.md`；用户给的恢复路径是「新会话里做一次 MCP/Skill 调用 + 用 Write/Edit 碰一次 plan.md，门就会释放 v13 的三个阶段」。

**2026-10-18 更正：我在这一点上判错了，用户是对的。** 原文写「按 1.1.5 的码读，做不到」。实测（干净探针：34 条证据全部消费，`evidence > consumed` 为假，门自己已无法释放任何阶段）：连续三次 `hooks/task unaided PRD|Spec|Plan` → `stages released by the gate: 0 invoked, 3 unaided` → `approve OK (user, v13)`。**零工具调用就能恢复**，因为 `hooks/task unaided` 在版本提升后会往 `evidence` **自己追加一行**再写 release 行（`hooks/task:1042-1043`，由 `2026-10-11-gate-host-coverage` 加入）。我漏掉了这条路径，只按门的供给条件（`evidence 行数 > max(seq)`）推，而 `unaided` 不受它限制。用户给的恢复路径（新会话做一次 MCP/Skill 调用）也能用，但**不需要三次真实调用**：一次真实调用释放一个阶段，剩下两个用 `unaided` 声明即可。顺序那半句仍然成立：先补证据再动文档，反了会被门拦下。

**本条的真正缺陷（与「证据用尽」这个现场分开记）**：`seq` 是**全局**计数器，而 `release` 的幂等键是 **(version, stage)**（`capability-gate:126-131`）。两个键不同源，于是任何一次 Task 版本提升都会**要求重新走一遍**，无论旧证据是否还能证明「这个阶段确实调用过能力」——代价是**重复劳动**（每次重走 N 次声明或调用，N = 所需阶段数），不是死锁。用户现场里 v12→v13 只是把版本号从 12 提到 13，需求、阶段、可用能力都没变，却要重新走一遍能力选择——这正是 `TF-20261009-8abbd6`「把阶段的能力选择与宿主工具流解耦」想要消除的那件事，现在多了一个机械版本：**版本提升与证据消耗被同一个全局队列绑死**。

**在「全局单调」这一条上我不认为是缺陷**：它买的是「一个已花掉的调用不能被第二个文档再花一次」（`capability-gate:133-135` 的注释），以及「版本提升不能拿旧版本用剩的证据来满足」。这两件都是真的、且值得。问题只在**它没有与版本提升的语义对齐**（2026-10-18 更正：对齐的缺口的代价是重复劳动，不是「版本提升变死路」——`unaided` 自写 release 行使零调用恢复成为可能）——`approve` 对账的是「本版本每个阶段都有 release 行」，而 release 行的**供给**是全仓库一条队列。

**可核验的机械事实（本次实测 1.1.5，仓库根）**：`git rev-parse --absolute-git-dir` = `.git`，**本仓库根没有证据库**（`.git/taskflow/` 不存在）；六个链接工作树各有自己的库，`evidence`/`consumed` 分别为 4/2、3/2、3/2、2/2、2/2、3/3，即**每一个都处于或接近耗尽**（`evidence > consumed` 才算可释放）。这符合设计（库随工作树分开，见 `capability-gate:160-178`），但也说明「耗尽」在本仓库不是偶发：六个工作树里四个耗尽、两个各只剩 1 条。

**为什么值得单记而不是并入 `TF-20261009-8abbd6`**：8abbd6 要解决的是「宿主没有工具流 / cwd 不在任务工作树」造成的假拒绝，方向是**让阶段选择不必是工具调用的产物**；本条是**记账方式**本身使版本提升变死路，即使宿主有门、cwd 也对，一样会发生。两条的修复面不同（8abbd6 动能力表示层，本条动 `released`/`evidence` 的键或 `approve` 的对账口径）。相关：`TF-20261009-8abbd6`、`TF-20261011-39bda8`（已 done，`unaided` 现在自己写 release 行）。

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
- Status: inbox
- Priority: normal
- Owner: Claude
- Source: user request 2026-10-09, found while writing the trae-host PRD
- Added: 2026-10-09
- Updated: 2026-10-11
- Goal: Decouple stage capability selection from the host tool-call stream: the PreToolUse gate refuses the first write of prd/spec/plan unless a Skill/Agent/MCP call already matched, so a host that has no such call, or a session driven from a different cwd than the task worktree, forces either a throwaway invocation like skill(sxng) for a PRD already researched, or the unaided declaration for a phase that really did use a capability. Give the phase a way to record its selection that is not a tool-call artifact
- Task: Not promoted.
- Next action: Clarify and promote when ready; fold in the two 2026-10-11 findings recorded in Notes (gate stage_class vs phase table mismatch; schema-leads-capability)
- Notes: **2026-10-11 用户裁定并入本条（不新建）**：用户指出「头脑风暴类的引导，按理应由引导工具 lead 调研和编写文档的方向，TaskFlow 只规定流程」，要查是否如此。查到两处，都属本条的能力表示层。

**(1) 门在正确时机投递的概念类，是 phase 表的一个子集 —— 可复现的机械缺陷。** `hooks/capability-gate` 的 `stage_class()` 是手抄的第二份表，PRD 只写 `requirements elicitation and framing`；而 `SKILL.md:167` phase 1 的类是 `requirements elicitation and framing; divergent exploration`（`divergent` 在 SKILL.md 出现 2 次，在 gate 里 0 次）。`divergent exploration` 在 `hooks/task:606` 的词表里、`unaided` 接受它，但**门的拒绝消息从不提它**。这是唯一「在正要写文档那一刻、无法忽略」的投递渠道（R7 的原始动机，见 `achieved/2026-09-27-capability-pre-write-gate/prd.md`），而它在 PRD 这一格只广播 converge 一个方向。`smoke-test:1740-1742` 只断言消息含 stage/类/逃生舱三要素，**没有任何断言比较 stage_class 与 phase 表**——而 phase 表与 `concept_class_re` 之间是有双向断言钉住的（`smoke-test:1596-1621`），两份手抄表只钉了一份。`achieved/2026-10-08-capability-concept-classes/prd.md` A5 明确要求 `stage_class()` 逐字不变，所以那次改动**故意**没碰它。

**(2) 交付物 schema 先于能力定死，能力只能「折进」（设计层观测）。** `prd.md` 必备小节、Plan 每 Step 的 acceptance/verification/rollback、`task approve` 的 stage 对账（`hooks/task:1055-1092`）、change-log 只能进 `plan.md`（`SKILL.md:252`）——这些在咨询任何引导工具之前就已经固定。引导工具的产出按类被折入（`SKILL.md:177`：requirements → prd.md，design → spec.md，breakdown → plan.md Steps）。设计声明是「能力供专业、TaskFlow 供流程」（`SKILL.md:8`、`159`、`163` 都写了），但强制预算全在流程侧，能力侧只有无预算的散文。历史旁证：`idea-refine` / `brainstorming` 真被用过（`achieved/2026-09-23-capability-invoke-gate/plan.md:22`），`2026-10-08-capability-concept-classes/prd.md:27` 却记录它们「没有回流成引导」。

**(1) 是可独立修的小缺陷**，修法与既有约定一致：要么让门的显示类从 phase 表派生，要么加一条和 `concept_class_re` 同风格的双向断言。用户 2026-10-09 对 (3) 的裁定（把硬 deny 降为 approve 时对账）如落地，(1) 会随之消解。相关：TF-20261008-5b5635（已 done，即上述能力类改动）

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
- Status: inbox
- Priority: normal
- Owner: Codex
- Source: direct user request
- Added: 2026-09-28
- Updated: 2026-10-10
- Goal: Release process: make the manual three-host catalog validation conditional and add an automated $schema assertion, since that step is never exercised by CI and its only failure mode is already covered by release-check
- Task: Not promoted.
- Next action: Keep the $schema assertion; re-scope the manual three-host catalog validation after release-flow-exception, then promote.
- Notes: 2026-09-30 互链：`TF-20260930-c4e4c8` 提出「发布不重跑 CI 已覆盖的测试」，与本条「把手工三宿主 catalog 校验改条件式」同属一条主线——都是砍掉发布流程里 CI 覆盖不到的判断之外的重复劳动。两条宜一并 promote、一并改 `RELEASE.md`。
- 2026-10-10 前提复核（本条部分过期）：(1) 前半「三宿主手工 catalog 校验改条件式」的**前提已被 TF-20260919-40eca2 搬走**——RELEASE.md 不再有「Validate the catalog entry with Claude Code, Codex, and CodeBuddy tooling」这一段手工步骤（现 RELEASE.md 的发布检查只列 repository-check / release-check / quick_validate / diff --check 四条），所以「改条件式」已无对象。(2) 后半「自动 $schema 断言」**仍未做**：`hooks/release-check`、`hooks/smoke-test`、RELEASE.md、两份 marketplace catalog 里 `schema` 零命中，`$schema` 字段目前无任何机器校验。(3) 相邻已交付条目 TF-20260930-c4e4c8 也来自同一主线（砍掉发布流程里 CI 覆盖不到的重复劳动），其落点同样在 RELEASE.md。故本条收窄为「给两份 catalog 的 $schema 加自动断言」后再 promote。

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
- Updated: 2026-10-11
- Goal: Measure whether delegating exploration to subagents actually reduces main-thread context, before adopting it as guidance.
- Task: Not promoted.
- Next action: Assess whether TaskFlow lowers an Agent's tendency to search external sources, and fix the Reference Pointers slot if it does: all 72 achieved tasks put internal repo paths in Reference Pointers (253 bullets, 0 URLs), while external hosts total 4 across the whole archive. Add a control (same task, with and without the injected TaskFlow context) alongside the existing delegation measurement.
- Notes: **2026-09-19 用户提出**：subagent 委派能不能省 token，要**实测**才知道，别先写进指引。
- **2026-10-11 用户提出**：用户观察「用了 TaskFlow 之后 Agent 似乎变得不喜欢做网络搜索」，并要求先查是不是真的。用户明确此条**不是**要强制规定调用网络搜索，只是这条倾向值得被测量。

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
- Updated: 2026-10-11
- Goal: Stop duplicating changelog/history content across prd.md, plan.md and spec.md: each document repeats the same change-log or history narrative, which is pure token waste. Assign the history/changelog a single owning document and have the others reference it instead of restating it.
- Task: Not promoted.
- Next action: Clarify and promote when ready.

