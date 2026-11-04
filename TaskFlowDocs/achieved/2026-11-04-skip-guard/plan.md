# Plan — 无活动任务时，把「先记录、再动手」放到每一条提示旁边

> Task version: v1
> Status: completed

No spec required — 单个 hook 文件里加一段输出，边界由既有 `summarize-state` 输出决定。

## Reference Pointers

- `hooks/summarize-state:76-92` — 无活动任务时的两行标题，提醒的判定输入。
- `hooks/prompt-reminder:92-114` — 现有的单活动任务解析，新分支必须与它互斥。
- `TaskFlowDocs/achieved/2026-10-27-midturn-presence/plan.md` — `prompt-reminder` 的既有设计边界（fires on task state, not prompt wording）。

## Related Tasks

- 前置：TF-20261103-fa9090（本任务的来源，排查结论在 Todo Notes）。
- 无依赖、无子任务。

## Skills / Tools Used

- [PRD] Unaided — considered: requirements elicitation and framing。目标与边界由 Todo 条目已有的排查结论直接决定，用户已裁定方向。
- [Plan] Unaided — considered: work breakdown and task decomposition。单个文件一处分支。
- [Test] Unaided — considered: testing strategy。断言沿用 `hooks/smoke-test` 第 6607 节起的既有风格。

## Preconditions

- 工作在 `.worktrees/2026-11-04-skip-guard`，分支 `fix/2026-11-04-skip-guard`，基于 `eed6fdf`（v1.1.13 之后）。
- 用户已选定方向：每轮提示（不是 PreToolUse 硬拒绝）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-04 13:54 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 无活动任务时的入口提醒

- Goal: `prompt-reminder` 在 `summarize-state` 报告 `# TaskFlow (no active task)` 时输出一行入口提醒，其余状态保持静默。
- Dependencies: 无。
- Files: `hooks/prompt-reminder`、`hooks/smoke-test`
- Implementation checklist:
  - [x] 在 `hooks/prompt-reminder` 里加一个与既有单活动任务分支互斥的分支：读 `summarize-state` 输出第一行，等于 `# TaskFlow (no active task)` 时构造提醒行。
  - [x] 提醒行给出可复制命令：`bash hooks/task intake "<goal>"` 与 `git worktree add .worktrees/<slug> -b <type>/<slug> <base>`，并说明只读工作不需要。
  - [x] 现有四段式输出在此状态下是空的（无活动任务时不会有 task 行），新提醒不得依赖 `line` 变量。
  - [x] 错误路径仍全部 exit 0，且不写任何文件。
  - [x] `hooks/smoke-test` 新增断言组：入口提醒出现（AC1）、有活动任务时消失（AC2）、未使用仓库与仓库外 cwd 静默（AC3）。
  - [x] 变异检验：反转新分支条件后 AC1 变红，恢复后 `cmp` 逐字节一致。
- Acceptance: AC1–AC6 全部通过。
- Verification: `bash hooks/smoke-test`（三平台由 CI 覆盖）；本地跑 ubuntu 侧；`bash hooks/repository-check .`；`git diff --check`。
- Rollback: 单文件改动，`git checkout -- hooks/prompt-reminder hooks/smoke-test`。
- Status: done

## Checkpoints

- 断言写成两向（出现 / 消失），否则「永远输出」和「永远沉默」都能骗过一组单向断言。

## Verification / Review

- **AC1/AC2/AC3 — 通过。** 新增节 `== prompt-reminder states the entrance rule when no task is in flight ==` 在隔离运行中输出 `ok`：入口提醒含 `hooks/task intake`、`git worktree add`、`Read-only work`；`planning` 任务在场时静默；未使用 TaskFlow 的仓库静默；仓库外 cwd 静默。`hookEventName` 仍为 `UserPromptSubmit`。
- **AC4 — 通过。** 既有两节（in-flight 四段式、silence 边界）在同一隔离运行里先后输出 `ok`，逐字未变：新分支在 `line` 为空时接管，`line` 非空时行为与改动前一致。
- **变异检验 — 已做。** 把 `entrance_reminder` 的 `case` 反转（只认 `not started`）后，AC1 三条断言全红；恢复后 `cmp` 与原文件一致。第二次变异删掉 `Read-only work` 一句，对应断言独红。
- **AC5 — 部分由 CI 承担。** 本机 `bash hooks/smoke-test` 在 `== hooks run with no interpreter available ==` 节失败（`session-record failed without an interpreter`，底层是本机 Git Bash 通过 symlink 调用时丢 DLL：`error while loading shared libraries`）。该失败在改动前就存在——同一节的同一报错在本会话更早的 `main` 检出上复现过——且它会终止整个套件，因此本次用隔离运行验证新增节；三平台全量由 CI 判定。
- **AC6 — 见上。**

`bash hooks/repository-check .` — STATUS: pass（在本 worktree 跑）。
`git diff --check` — clean。

## Change Log

- v1 — 初始计划。
- v1 实现 — `hooks/prompt-reminder` 增加 `entrance_reminder()` 与一次互斥调用；`escape_for_json` 上提到函数定义之前，供两处共用；`hooks/smoke-test` 新增一节断言。

## Follow-ups

- 若入口提醒在纯问答会话里过吵，升级为只在 cwd 是 base checkout 时输出（PRD Risks 已记）。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-11-03 排查结论（会话 `272bb345-dcd5-4e26-8139-21b941dd3a65`，3536 行，digdig）**。
  **先更正一条我起初写错的判断**：我先前说「该会话全程没有注入 TaskFlow 的 SessionStart 上下文」，**这是错的**。逐条读 `attachment.hookName` 可见注入发生了两次：line 4（startup，`# Active tasks - 2026-11-02-release-tag-fix`）与 line 2341（compact 之后，5161 字符，含 `# TaskFlow (no active task)` 与全部 inbox 条目）。版本也无关——`v1.1.10` 与 `v1.1.12` 的 `hooks/session-start` 与 `hooks/summarize-state` 逐字节相同，`diff` 为空。
  **真实时序**（用户消息全程只有三句）：
  - 2347「第一个问题是什么问题」→ Agent 逐条讲解 P1…D1；
  - 2449「我说的是D1」；
  - **2688「修D1」**——明确指令。
  - Agent 在 **2746** 改 `cli/src/deep/session.ts`，2766/2774 改测试，2846 报告「D1 修好了」。
  - **2867 用户发现**：「你说得对，两个问题都在：没进 TaskFlow，直接在 main 工作区改」。
  - 2879 Agent 承认违规；2914 移到 worktree；2975+ 才 `promote` 建任务。
  **所以违规不是「自作主张改代码」**——用户确实说了「修D1」。违规是**执行时跳过了全部阶段**：没有 promote、没有 PRD/Plan、没有 approve、没有 worktree，直接在 base checkout 改产品代码。
  **为什么没有一道门拦住**（这是本条真正要修的）：
  1. `hooks/capability-gate` 的 `judge_path` 按 basename 只认 `prd.md`/`spec.md`/`plan.md`。**产品代码（`cli/src/deep/session.ts`）不在谓词里**，改它时没有任何 hook 会说话。
  2. `hooks/task promote` 只在被调用时才检查 worktree；**没有人调用它就不发生检查**。
  3. SessionStart 注入的是**状态**（有/无活动任务、inbox 列表），不是**门**。它说了「applicable work is recorded first」，但这话在 2688 那一刻没有可执行的强制力——它是一条散文，而对话里紧接着就是一句「修D1」。
  4. 真正起作用的拦截来自用户本人（2867），不是任何 hook。
  **与既有条目的关系**：`2026-10-10-taskflow-first-order`（已 done）确立的是「进入工作先进 TaskFlow」的次序；本条是**那个次序在真实会话里没有任何机械执行点**。`TF-20261027-e4ba77`（已 done，midturn-presence）解决的是「长实现过程里 TaskFlow 不再发声」，本条的入口更早——**第一行产品代码写入**。不是 `TF-20261009-8abbd6`（阶段选择与工具流解耦）。
  **待定的修法方向**（三者不互斥）：
  (a) 给产品代码的首次写入加一道提示，与 `capability-gate` 同构，但**不能拒绝**（会毁掉所有非 TaskFlow 场景），只能提示并指向 `task promote`；
  (b) 让 `promote`/`state` 之外多一个可检的「本仓库有未 promote 的活跃工作」信号；
  (c) 收窄 SessionStart 的措辞，让「进入工作先进 TaskFlow」带上一个可执行动作而不是一句陈述。
  需要先定方向再 promote。
