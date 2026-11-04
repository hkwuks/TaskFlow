# 无活动任务时，把「先记录、再动手」放到每一条提示旁边

> Task version: v1
> Status: completed

## Goal

一个真实会话里，用户说出「修D1」，Agent 跳过 promote、PRD/Plan、approve、worktree，直接在 base checkout 改产品代码；全程没有任何 hook 说话。要补的是**那一刻的投递**：当仓库在用 TaskFlow、而当前工作树没有进行中的任务时，`prompt-reminder` 在用户提示旁说一行——这条提示如果是在改仓库或交开发产物，先 `intake` 再动手。

## Background / Confirmed Facts

排查结论来自 Todo 条目 TF-20261103-fa9090 的 Notes（会话 `272bb345-dcd5-4e26-8139-21b941dd3a65`，3536 行）：

- **上下文注入是发生的**，不是遗漏：SessionStart 注入两次（startup 与 compact 后）。v1.1.10 与 v1.1.12 的 `hooks/session-start`、`hooks/summarize-state` 逐字节相同。
- **违规是执行时跳过全部阶段**，不是「自作主张」——用户确实说了「修D1」。缺的是机械执行点：
  1. `hooks/capability-gate` 的谓词按 basename 只认 `prd.md`/`spec.md`/`plan.md`，产品代码不在其中，写它时没有 hook 会说话；
  2. `hooks/task promote` 只在被调用时检查工作树，没人调用就不发生检查；
  3. SessionStart 注入的是**状态**（有/无活动任务、inbox 列表），不是门；「applicable work is recorded first」在那次对话里只是一句散文；
  4. 最后拦住它的是用户本人，不是任何 hook。
- **`prompt-reminder` 是目前唯一每轮都跑的 hook**，且已经承担同类职责：有在飞任务时，它把变更分类问题放到提示旁（`hooks/prompt-reminder:265-270`）。
- **它现在在这件事上完全沉默**：`hooks/prompt-reminder:92-114` 只在「恰好一个活动任务，且状态是 in_progress/checking」时输出，其余一律静默——包括「仓库在用 TaskFlow 但没有活动任务」这个状态。
- `hooks/summarize-state` 已经把这个状态算出来了：无活动任务且仓库有使用证据时打印 `# TaskFlow (no active task)`，否则 `# TaskFlow (not started in this repository)`（`hooks/summarize-state:76-92`）。

## Requirements

- R1：当 `summarize-state` 报告 `# TaskFlow (no active task)` 时，`prompt-reminder` 输出一行入口提醒，说明：本工作树没有进行中的任务；若该提示要改本仓库或交付开发产物，先记录再动手；只读工作不需要。
- R2：判定只读 `summarize-state` 的第一行，不新增第二套状态推导（不重读 `plan.md`、不自行枚举任务目录）。
- R3：`# TaskFlow (not started in this repository)`、有活动任务（一个或多个）、仓库外 cwd、非 `UserPromptSubmit` 事件、无法解析的输入——一律保持现有静默契约。
- R4：提醒里给出的命令必须真实存在且可复制：记录用 `bash hooks/task intake "<goal>"`，隔离用 `git worktree add .worktrees/<slug> -b <type>/<slug> <base>`。
- R5：不新增 hook、不改任何宿主接线文件；改动落在 `hooks/prompt-reminder`，断言落在 `hooks/smoke-test`。

## Acceptance Criteria

- AC1：fixture 仓库含 `TaskFlowDocs/todo.md`、无活动任务 → `prompt-reminder` 输出 `hookSpecificOutput.additionalContext`，其中含 `intake` 与 `worktree add`；`hookEventName` 仍是 `UserPromptSubmit`。
- AC2：同一 fixture 加一个 `> Status: planning` 的任务目录 → 提醒消失（有活动任务，走既有静默契约）。
- AC3：`TaskFlowDocs/` 为空目录（没有 todo、没有任务）→ 静默；仓库外 cwd → 静默。
- AC4：既有断言全绿：有在飞任务时的四段式输出（含 change-event 问句与 `Searching is allowed`）逐字不变。
- AC5：`bash hooks/smoke-test` 在 ubuntu/macos/windows 三平台通过；`bash hooks/repository-check .`、`git diff --check` 无新问题。
- AC6：变异检验——把新分支的判断条件反转（改成「有活动任务时才输出」），AC1 变红且错误信息点名入口提醒缺失。

## External Facts

- Depends on external facts: no
- Why not: 判定输入是本仓库 `summarize-state` 自己的输出，宿主事件名与回包形状已在本仓库 `skills/taskflow/references/runtime.md` 的 event map 中记录（`UserPromptSubmit` → `hookSpecificOutput.additionalContext`，五宿主同形），本次不引入宿主的任何新字段。

## In Scope

- `hooks/prompt-reminder`：无活动任务状态下的入口提醒。
- `hooks/smoke-test`：新增断言组（入口提醒出现/消失/边界）与变异可红性。

## Out of Scope

- 产品代码首次写入的硬拒绝（用户 2026-11-04 选定的方向是每轮提示，不是 PreToolUse deny）。方向 (b)/(c) 中的「可检信号」与 SessionStart 措辞收窄不做。
- `hooks/task unaided` 选择「第一个活动任务」的既有缺陷（1.1.9 已记为 follow-up），本任务不修。
- `TaskFlowDocs/2026-11-03-gate-stage-class/` 未归档的事实修复（属于独立记账，单独处理）。

## Risks / Deferred Items

- **每轮提示的噪音**：规则只在「在用 TaskFlow 且本工作树无活动任务」时触发，仍会在纯问答轮次出现。缓解是把话说清（只读工作不需要），并把它放在既有输出位置的第一行之前。若实测过吵，升级路径是只在 cwd 位于 base checkout 时输出。
- **base checkout 与任务 worktree 的视角差**：任务在 `.worktrees/<slug>` 里时，base checkout 看到的是「无活动任务」，提醒会触发；措辞用「本工作树」而不是「本仓库」，两种情况都真。
- 提醒不阻止任何操作。它降低的是「完全没有信号」这个状态，不是「违反一定会被拦」——真正的拦截需要 deny 类机制，已由用户选择不做。

## Open Questions

无阻塞项。
