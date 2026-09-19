# Conflict side review and the zh-CN manifest count
> Task version: v1
> Status: completed

## Goal

把 `README.zh-CN.md` 第 64 行被冲突解决退回的 manifest 计数改回正确值，并给 Skill 补一条"解决冲突后要记录取舍"的规则——这一类失败没有任何自动检查能兜住。

## Background / Confirmed Facts

- **事实错误仍在 shipped 产物里**：`origin/main:README.zh-CN.md:64` 写「比对两个插件 manifest」，而 `hooks/release-check` 校验的是三个（`.claude-plugin/`、`.codex-plugin/`、`.codebuddy-plugin/`）。英文版 `README.md:97` 同一句写的是 `all three plugin manifests`，所以两份 README 目前互相矛盾。
- **成因已实测**（本任务 Todo 条目 `TF-20260918-ad8348` 的 Notes，2026-09-18 复核）：
  - `46131a1`（"Merge branch 'main' into chore/e-task-isolation-and-capability-record"）**确实带着一次真冲突**——重放三方合并（base `985b269`、ours `adfc5c1`、theirs `c083240`）得到 `git merge-file` exit 1。
  - 冲突行两侧都改过同一句：PR #37 把「两个」改成「三个」，PR #38 在同一句里加了「并列出该 checkout 里未提交的任务产物」。
  - **解决时整块取了分支侧**，于是结果里同时留下 PR #38 的新句子和 PR #37 已被覆盖的旧计数。
  - 时间窗 2 分钟：`adfc5c1` 定稿 20:08:19 → PR #37 合并 20:11:40 → `46131a1` 20:13:42。
- **为什么目视复核没抓住**：两侧都是合法中文、都在讲同一个检查，只有计数不同；只看 diff 时两个版本都读得通。
- **为什么没有自动检查能兜住**：`hooks/todo-check` 是纯 hook、无 LLM，只比较一个 merge commit 的两个 parent 与结果各自持有的 `- ID:` 集合（`sed` 提取 + `sort -u` + `comm -13`），范围仅限 `TaskFlowDocs/todo.md` 的条目级丢失，不做任何三方比较。本类失败是**解决冲突时的一次判断**，不是内容比对能判定的。它由 CI 的 `todo-merge-audit` 作业调用（非自动 hook）。
- **既有规则的空位**：`SKILL.md` 在 Phase 5 只说了「本地合并让 Todo 驱动生效；托管平台网页端合并会退化成普通冲突」，对"冲突解决后该做什么"没有要求。Phase 6 的验证清单七项里也没有冲突复核这一项。

## Requirements

- R1：`README.zh-CN.md:64` 的 manifest 计数改回「三个」，与 `README.md:97` 的 `all three plugin manifests` 和 `hooks/release-check` 的实际校验范围一致。
- R2：`skills/taskflow/SKILL.md` 增加一条规则：**任务过程中由 Agent 执行的合并发生冲突时，停下来把两侧摆给用户、由用户决定取舍**，不得自行选定一侧；用户的决定落下后记入当前任务 `plan.md` 再推送。只发生自动合并时不要求任何动作。
- R3：规则要放在能被执行的位置——与 Phase 5 已有的 merge/Todo 驱动段相邻，而不是只写在 Phase 6 的验证清单里（该清单只在任务自己的 `checking` 阶段读）。
- R4：规则要求的是**先问、再留痕**，不是禁止整块取某一侧——用户可以直接裁定「这一侧全取」，那也是一种决定，照记即可。
- R5：措辞与 `SKILL.md` 既有的同类门禁一致（`Repository document environment` 段的 "On a conflict, stop and ask the user; do not silently choose one."），复用同一套表述而不是另造一种。
- R6：不把托管平台网页端 PR 的冲突纳入本规则——那条路径上的解决动作由用户在人机界面上完成，不在 Agent 的可控范围内；本规则管的是 Agent 自己跑的 `git merge` / `git rebase`。这一点必须写明，否则读者会以为 PR 冲突也要走同一条流程。

## Acceptance Criteria

- `README.zh-CN.md:64` 与 `README.md:97` 的 manifest 计数一致，且与 `hooks/release-check` 校验的三个 manifest 相符。
- `skills/taskflow/SKILL.md` 存在一条可判定的规则：Agent 执行的合并遇到冲突时**先询问用户**再取舍，用户的决定记入任务 `plan.md`；未发生冲突时不要求动作；托管平台网页端 PR 的冲突明确不在规则范围内。
- `bash hooks/smoke-test` 在本分支通过。
- `bash hooks/release-check .` → pass（两份 README 的 `claude plugin list` 示例仍为 `1.0.6`，未被本次改动触碰）。
- 改动范围只含 `README.zh-CN.md`、`skills/taskflow/SKILL.md` 与本任务目录。

## In Scope

- `README.zh-CN.md`（一行）。
- `skills/taskflow/SKILL.md`（Phase 5 的 merge 段 + Phase 6 验证清单各一处）。
- 本任务 PRD / Plan。

## Out of Scope

- 改 `hooks/todo-check` 去检测"取错侧"——已确认它作为纯 hook 判定不了这件事（见 Confirmed Facts），本任务不改它。
- 给 CI 加通用的"已合入改动被退回"检测；那是另一个问题（需要三方比较或 LLM 判定），本任务只留规则。
- **托管平台网页端 PR 的冲突解决**——那条路径由用户在人机界面上操作，本规则不覆盖（R6）。
- `README.md` / `hooks/` / `hooks/README.md`；在 README 里同时改其他内容。
- 追溯修改历史提交 `46131a1`。

## Risks / Deferred Items

- **这条规则会在合并时把控制权交回用户，可能中断一个正在进行的任务**。这是有意的：本类失败（`46131a1`）正是"Agent 自行选定一侧、用户不知情"造成的，且没有自动检查能兜住。代价是冲突时必须等人。
- 规则是**流程性**要求，没有自动强制手段——不写进 CI 就只能靠 Agent 遵守。这是有意的：可强制的部分（条目级丢失）已由 `todo-check` 覆盖，本类不可强制。
- 如果将来要自动兜住这一类，方向是"合并后对两侧都改过的行做三方比较"，而不是继续扩 `todo-check`。
- 本机 `bash hooks/smoke-test` 曾出现与 `main` 同形态的失败记录，但 2026-09-18 复跑为 `ALL SMOKE PASSED`；本任务改 `SKILL.md` 不触及 hook，仍以实际输出为准。

## Open Questions

- 无阻塞项。用户在 2026-09-18 明确了规则强度：**发生冲突时应当询问用户**（不是仅要求记录取舍），并据此定稿 R2/R4/R6。

## Version History

- v1 — planning。
