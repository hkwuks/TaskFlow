# 在一次实现运行的中途保持 TaskFlow 在场，而不只在提示词边界

> Task version: v1
> Status: in_progress

## Goal

用户报告「跑着跑着不走流程」，并明确指出**发生在 Codex 上、研究性任务、不断修改指令之后**（2026-10-29）。

排查后问题分成两件，**权重差很多**：

1. **Codex 上 TaskFlow 等于裸跑。** `hooks-codex.json` 只接了 `SessionStart` 与 `UserPromptSubmit`，没有 `PreToolUse` / `PostToolUse` —— **没有门禁，没有证据记录**。而 Codex 官方文档明确支持这些能力（见事实 10）。**这是恒定缺失，与任务长短无关，也是本任务的主要交付。**
2. **Claude Code 上存在一处绕过**：Step 闭合不走 `hooks/task progress` 而手改。但样本只有 1 个，且来自与用户报告不同的宿主，**不能用来解释 Codex 的现象**。

本任务要做的：**把 Codex 接进门禁体系**（含 `apply_patch` 的路径解析），顺带修 gate 不读 `## Approval` 的缺陷；「中途在场」的形态选择留给实证，不预设答案必须是新 hook。

## Background / Confirmed Facts

### 1. 当前每轮说什么 —— 已验证

`prompt-reminder` 在 `in_progress` / `checking` 且只有一个活动任务时，投递完整的一行：

```
- 2026-10-29-midturn-presence | v1 | in_progress — <标题> | approval: requested | next: Step 1 Implement and verify [pending]
```

实测命令（2026-10-29）：

```bash
printf '{"hook_event_name":"UserPromptSubmit","cwd":"%s"}\n' "$PWD" \
  | TASKFLOW_TASK_ID=<task> bash hooks/prompt-reminder
```

**这一行已经包含当前 Step 与它的状态。** 待确认文档（`TF-20261027-e4ba77` 首稿）里「Step 信息算了但没投递」的说法**不成立**，已实测否定。

### 2. 投递时机 —— 每回合一次

`hooks/hooks.json:21-31` 把 `prompt-reminder` 绑在 `UserPromptSubmit` 上，没有别的触发器。`runtime.md:226` 明确写着：`PostToolUse` 上只绑了 `capability-evidence`，没有任何读状态的 hook。

### 3. 每回合的工具调用数 —— 重测，旧数字偏高

用本机三份 transcript 重算：

| transcript | 回合数 | 中位数 | 均值 | 最大 |
|---|---|---|---|---|
| `7ca911df` | 11 | 5 | 21.5 | 119 |
| `dc15ffaa` | 8 | **11** | 14.0 | 34 |
| `cd141f22` | 5 | 5 | 10.8 | 28 |

**待确认文档写的是「中位数 10–15，最大 197」。** 三份里只有一份的中位数落在 10–15，最大值 119 而非 197。方向不变（确实存在 5–119 次无信号的调用），但「典型一轮 10–15 次」是**高估**。

### 4. `hooks/task progress` 是少数路径 —— **93 份归档 Plan 的格式指纹**

**A2 复验通过。方法与结论都与前一版不同。**

`hooks/task progress` 写验证记录时用固定格式（`hooks/task:465`）：

```
- <YYYY-MM-DD> Step N: <text>
```

**手改写不出这个格式**，所以它是「走过 progress」的指纹。扫描 93 份 achieved Plan（2026-10-29）：

| 时期 | 任务数 | 有 progress 指纹 | 比例 |
|---|---|---|---|
| 2026-10 之前 | 66 | 11 | **17%** |
| 2026-10 之后 | 27 | 13 | **48%** |
| **合计** | **93** | **24** | **26%** |

同时，归档 Plan 的 Step 状态分布是：

| done | pending | completed | done (v1) |
|---|---|---|---|
| 260 | 6 | 4 | 3 |

**状态几乎全部写成了 `done`（93%），但只有 26% 走了 `progress`。** 也就是说：**结果一致，路径不一致。**

复现：

```bash
grep -E '^- [0-9]{4}-[0-9]{2}-[0-9]{2} Step [0-9]+:' TaskFlowDocs/achieved/*/plan.md
```

**这推翻了先前两版的说法**——不是「一处绕过」，也不是「Codex 特有」。**手改是多数路径，跨宿主、跨时间段都成立。**

### 5. 为什么不会走 `progress` —— **机制原因，已从代码确认**

不是「忘了」，是这条路**只有成本、没有任何可验证收益**：

**① `completion-gate` 只看结果，不看路径。**

```awk
instep && /^- Status:/ { closed = ($0 ~ /^- Status:[[:space:]]*done[[:space:]]*$/) }
```

它只问「这行是不是写着 `done`」。`progress` 写的和 `sed` 写的判定完全一样。`hooks/completion-gate` 里五处提到 `progress`，**全在注释，没有一处用它做校验**。

**② `progress` 带一条硬约束，手改没有。**

```awk
if (step_status == "done") {
  for (...) if (line[i] ~ /^[[:space:]]*- \[ \]/) die("Step N has unchecked items")
}
```

`done` 会拒绝任何未勾选的 `[ ]`；`sed` 不做检查。

| | `progress` | 手改 |
|---|---|---|
| 会不会被拒 | 会 | 不会 |
| 收尾 4 个 Step | 4 条命令 | 1 个脚本 |
| 失败时 | 中断、要处理 | 静默成功 |
| 有没有人查 | **没有** | **没有** |

**一个只增加摩擦、不产生任何可验证产出的路径，注定被绕过。这是理性选择，不是疏忽。**

**③ 所以「中途在场」原来的问题框定是错的。** 模型并不缺当前 Step 的信息——`prompt-reminder` 每轮都在投递（事实 1）。真正的结构问题是：**流程里有一条推荐路径，它既不被强制、也不被奖励、还比替代方案更难，而终点检查对两者一视同仁。**

**加提示不会改变这个激励结构。**

### 6. 用户补充的触发条件 —— **本仓库无法证实**

用户 2026-10-29 说明观察条件是「在一些非常长的任务中，不断被用户引导之后」，且**发生在 Codex 上、不是本机**。

**这组数据只能作为背景，不能作为该现象的实证：**

| 会话 | prompts | interrupted | 短「继续」 | 宿主 |
|---|---|---|---|---|
| `cd141f22` | 5 | 1 | 0 | Claude Code |
| `dc15ffaa` | 8 | 0 | 0 | Claude Code |
| `7ca911df` | 11 | 2 | 4 | Claude Code |
| 当前主会话 | **520** | 15 | 40 | Claude Code |

**当前主会话有 520 个 prompt、15 次打断，做了 29 次真实 `hooks/task progress` —— 没有走偏。** 而唯一走偏样本 `7ca911df` 是最短的之一。

所以在这批数据里，「长」和「被打断」都**不构成**走偏的充分条件。**Codex 侧的会话本机没有记录**（用户 2026-10-29：「不是本机，不用查会话了」）。

**结论：本任务不宣称「长任务 + 持续引导导致走偏」。** 能站住的只有事实 11 —— Codex 上根本没有门禁，那是恒定缺失，与任务长短无关。

范围变更的分布仍是有用的背景：

| | |
|---|---|
| 93 份 achieved 任务中，中途变过版本（有 `old/vN`） | **16** |
| 其中 Change Log 条目数 | 中位 3，最高 20 |

### 7. 把 Plan 当事后文档写 —— **单个样本，仅作线索**

`7ca911df` 的时间线（按用户 prompt 切分）：

| 回合 | Plan 文档改动 |
|---|---|
| 2–3 | 建 Plan（写模板） |
| **4** | 一次改 8 处：Step 1、Step 4、Follow-ups、Checkpoints、Change Log、Approval |
| 5–11 | **零改动** —— 包括 45 次代码编辑、2 次打断、2 次「继续」 |
| 结束 | 一个脚本批量把 4 个 Step 标 done、`> Status: completed` |

**这是一个样本，不是模式。** 它提出一个可检验的判据——「Plan 最后一次实质改动与最后一个代码提交的距离」——但**本任务没有在其余 92 个任务上验证过它**，因此不得据此下结论。A2 要求的复验正是为此。

### 8. 历史记录缺口 —— 一个已经收敛的过去

待确认文档用「59/91 份 achieved Plan 没有 stage 记录」作为「必须有人催」的依据。复测（93 份 achieved Plan）：

| 项 | 数量 |
|---|---|
| 有 `## Skills / Tools Used` 标题但**零条** stage 行 | 59 |
| 连该标题都没有 | 2 |
| 合计缺记录 | **61 / 93** |
| 缺 `## Change Log` | 8 |

按日期切开后，这个数字的含义变了：

| 时期 | 任务数 | 有 stage 行 | stage 行总数 |
|---|---|---|---|
| 2026-10 之前 | 63 | **5** | 12 |
| 2026-10 | 30 | **29** | 77 |

**缺口几乎全部落在 10 月之前。** 10 月之后 30 份里 29 份都填了。

**所以这条不能作为「现在需要新机制」的理由** —— 它描述的是一个已经收敛的过去。第 4 条提过「两者可能是同一件事的两面」，但那个推断只建立在 1 个样本上，同样不能用。**本任务只把它当背景。**

### 9. 三个「没有人会在中途检查」的开口 —— 均已实测确认

| # | 事实 | 证据 |
|---|---|---|
| ① | 某 stage 一旦释放，后续对同一文档的编辑**不再检查** | `hooks/capability-gate:133-137` 命中 `released` 记录即 `exit 0` |
| ② | 该 gate **从不读** `## Approval` | `grep -c 'Approval' hooks/capability-gate` = **0** |
| ③ | `task progress` 是 Step 状态的唯一写者，且**未绑任何 hook** | 写者：`hooks/task:1098`（`progress)` 分支）；`grep -n progress hooks/*.json` = 无 |
| ④ | 历史记录里有「Approval 填之前 Steps 1–3 已实现」 | `TaskFlowDocs/achieved/2026-10-23-archive-completion-gate/plan.md:132` |

### 10. 成本基线 —— 待确认文档未记录

```
prompt-reminder   0.27–0.30 s/次   （其中 summarize-state 0.19–0.21 s）
```

每次调用都会经 `summarize-state` 整份重读 `plan.md`。**若在 `PostToolUse` 上按同一方式每次工具调用都跑一遍，一轮 119 次调用即 ~32 秒纯开销。** 这是任何「每次工具调用都注入」方案必须先回答的约束。

### 11. 宿主能力 —— 仓库记录与官方文档不一致，**这是本任务的核心缺陷**

**本机实测：`PostToolUse` 的 `additionalContext` 在 Claude Code 上确实生效。** 2026-10-29 用两段式探针验证：hook 写日志（证明 hook 跑了）+ 模型回复 `PTU-SEEN`（证明模型读到了注入内容）。

**仓库对 Codex 的记录是错的。** `runtime.md:55` 说：

> the gate would find no path, exit 0, and allow every write… which is why **Codex is left unwired** rather than wired and hoped for.

而 Codex 官方文档（`learn.chatgpt.com/docs/hooks`，2026-10-29 读取）明确写着：

| 能力 | Codex 官方说法 |
|---|---|
| `PreToolUse` 拦截文件编辑 | 支持。`apply_patch` 可匹配，`matcher` 可用 `apply_patch` / `Edit` / `Write` 别名 |
| 拒绝写入 | 支持。`hookSpecificOutput.permissionDecision: "deny"` + `permissionDecisionReason`；另有 `{"decision":"block"}` 与 exit 2 + stderr 两条 |
| 编辑内容可见 | 支持。`tool_input.command` 携带 **patch 原文**，含 `*** Update File: <path>` / `*** Add File: <path>` |
| 注入模型可见上下文 | 支持。`PreToolUse` 与 `PostToolUse` 均可返回 `additionalContext` |
| `PostToolUse` | 支持。`apply_patch` 成功后触发 |

**所以「Codex 不支持门禁」是错的。** 真实情况是两件事被混为一谈：

1. **没接线** —— `hooks-codex.json` 只有 `SessionStart` 与 `UserPromptSubmit`，没有 `PreToolUse`/`PostToolUse`。
2. **没实现路径解析** —— `capability-gate` 只读 `tool_input.file_path`，而 Codex 把路径藏在 patch 原文里。`CHANGELOG.md:222` 自己写对了方向：「Codex would need the gate's path resolution changed, not just a wiring file」。

**后果：在 Codex 上跑 TaskFlow 等于裸跑** —— 没有门禁、没有证据记录，只有一句每轮提醒。用户观察到的「研究性任务不断改指令后走偏」发生在这个宿主上。

多宿主现状（修正后）：

| | Claude Code | Codex CLI | CodeBuddy | dsh | Trae |
|---|---|---|---|---|---|
| `PreToolUse` 门禁 | 已接线，measured | **官方支持，未接线** | 已接线 | 未接线 | 已接线，documented |
| 调用捕获 | 已接线 | **官方支持，未接线** | 已接线 | 未接线 | 已接线 |
| 上下文注入 | measured | **官方支持** | 未测 | 未测 | documented |

### 12. `apply_patch` 不是能力，接不上证据链 —— 实测

`capability-evidence` 的谓词是**能力类工具**（`Skill` / `Agent|Task` / `mcp__*`），不是「任何工具」。实测（2026-10-29）：

```bash
printf '{"hook_event_name":"PostToolUse","tool_name":"apply_patch","cwd":"%s","tool_input":{"command":"*** Update File: x"}}\n' "$PWD" \
  | bash hooks/capability-evidence; echo "exit=$?"     # → exit=0
```

`evidence` 文件行数**不变**。

**所以给 Codex 接 `PostToolUse`/`apply_patch` 是静默无效的接线**：hook 会跑、会 exit 0、一条记录也不写，而 `runtime.md` 会因此声称有了覆盖。这与事实 10 是同一类错误——**声称的覆盖与实际覆盖不一致**。见 R10、A12b。

Codex 上的能力证据只能来自 `Skill` 或 MCP 调用，与本次门禁改动无关。

## Requirements

- **R1 先证伪，再实现。** 诊断已由事实 4、5 确立（A2 复验通过）。**不预设答案必须是新 hook**，因为事实 5 表明问题在激励结构而非信息缺失。
- **R2 实现形态由实证决定。** 候选：(a) 不做；(b) 改 `prompt-reminder` 的投递内容；(c) `PostToolUse` 按 N 次调用注入；(d) 让 Plan 自带闭合检查清单。**事实 4 已基本排除「忘了 Plan」这一动机**，因此 (c) 只有在本任务给出「内容随状态改变」的证据时才成立。
- **R3 频率不得以线性成本换取。** 任何按工具调用触发的方案必须给出开销测算；`summarize-state` 全量重读（0.19–0.21s）不可直接放进热路径。
- **R4 逐宿主标注 standing，且不得把「未实现」写成「不支持」。** 与 `runtime.md` 现有惯例一致（measured / documented / not wired），但**「not wired」必须附带「宿主是否支持」的独立结论**，本次缺陷正是这两者被混写造成的。
- **R5 注入内容是数据，不是指令。** 若采用 `additionalContext`，注入文本不得包含可被模型当作命令执行的内容（尤其 patch 原文来自被编辑文件，属不可信输入）。
- **R6 不扩张 gate 为实现阶段的硬 gate**，但本任务**修**它的两个缺陷：无法表达「已批准版本不许被未审批内容覆盖」（见 A9/A9b）；只认 `tool_input.file_path` 因而无法服务 Codex（见 A11）。
- **R7 沉默优先。** 任何新输出都不得在「没有活动任务」「多个活动任务」「非 TaskFlow 仓库」时发声 —— 与 `prompt-reminder` 现有契约一致。
- **R8 文档同步。** `runtime.md` 的事件表与 Codex 段落、`hooks/README.md`、`CHANGELOG.md`、以及 `hooks/smoke-test:5272-5277` 那条「禁止给 Codex 接线」的断言一并更新。
- **R9 Codex 门禁必须真机验证过才能宣称可用。** 本机没有 Codex，验证由用户在另一台机器上执行；在收到验证结果之前，文档只能写 documented，不能写 measured。
- **R10 不接静默无效的线。** 每一条新接线都要能指出它**实际改变了什么**。接一个只会 `exit 0` 的 hook 不增加覆盖，却让 `runtime.md` 声称有了覆盖 —— 本任务已因此否掉 `PostToolUse`/`apply_patch`（Q5）。

- **R11 不强制 `progress`，改为让 `completion-gate` 做保障**（用户 2026-10-29 裁定）。事实 5 表明 `progress` 只增摩擦、不产生可验证差异；加提示不改变激励结构。因此：
  - **不**要求 Step 状态必须由 `progress` 写入，`progress` 降级为便利工具；
  - `completion-gate` 的判定**不区分**谁写了那行 `- Status: done`；
  - 保障改由 gate 自己提供：一个 `done` 的 Step 必须有**可核验的证据**，而不是一行声明。
- **R12 多重 `- Status:` 行是错误。** `completion-gate` 现有的注释（`:103-105`）写着「第二个 `- Status:` 是手改，读最后一个是人的读法」——它容忍了这种情况。R12 要求**明确报错**而不是猜，因为两个状态共存意味着文档自相矛盾。
- **R13 新规则只约束活动任务。** `achieved/` 下的 93 份归档 Plan 不改、不重验（用户 2026-10-29 裁定）。理由：它们已经发布，重写历史只会制造噪音，而补出来的证据未必真实。

## Acceptance Criteria

- **A1** PRD 与 Spec 中的每一个数字都能用仓库内的命令重算出来，且命令写在 Plan 的 `## Verification / Review` 里。
- **A2（已通过，2026-10-29）** 诊断落到机制层，且用**不依赖 transcript 抽样**的方法复验：93 份归档 Plan 的格式指纹显示只有 24 份（26%）走过 `progress`。见事实 4。
- **A3** 若诊断未能复验、或复验后判定不做，交付物是**一份带证据的否决记录**，`todo.md` 该项标 done 并在 Notes 写明理由，不得静默丢弃。
- **A4** 若决定做，方案给出：触发条件、开销测算（毫秒/次）、沉默条件、逐宿主 standing。
- **A5** 实测复现：`prompt-reminder` 已投递当前 Step —— 任何「它没投递」的说法必须先用 A1 的命令跑一遍再下结论。
- **A6** 任何新增输出在「无活动任务 / 多活动任务 / 非 TaskFlow 仓库」三种情况下**零输出**，由 smoke 断言。
- **A7** `bash hooks/smoke-test` → `ALL SMOKE PASSED`。
- **A8** `git diff --check` 干净。
- **A9** `capability-gate` **不**阻止 `planning`/`ready` 阶段写 `prd.md`/`spec.md`/`plan.md` —— 审批是**开工许可**，不是写文档许可（`SKILL.md:193`：`in_progress` 才要求批准）。它阻止的是：**当前 Task version 与 `- Approved version:` 不一致时，继续写入已批准的那份文档**。即「拿旧批准写新版本」。
- **A9b** `hooks/archive` **拒绝归档一个未审批的任务**。已实测这是真实缺口：4 份任务（`2026-09-14-branch-and-worktree-gate`、`2026-09-14-macos-hook-portability`、`2026-09-14-personal-docs-git-boundary`、`2026-09-15-phase-concept-mapping`）在 `Approved by: pending` 状态下进了 `achieved/`，现在跑 `completion-gate` 四个全部报 `current Task version is not approved`。其中 `macos-hook-portability` 的 Approval 段自己写着「No approval is claimed or implied.」——作者知道没批，仍然归档了。
- **A10** A9 由 smoke 覆盖，且**包含反向用例**：`Approved version` 与 `> Task version:` 不一致时必须拒绝；两者一致且已批准时必须放行。
- **A10b** A9b 由 smoke 覆盖：未审批任务归档被拒，已审批任务归档不受影响（现有 93 份归档的归档路径不回归）。
- **A11** `capability-gate` 能从 `apply_patch` 的 `tool_input.command` 中解析出目标文件路径，识别 `*** Update File:` / `*** Add File:` / `*** Delete File:` / `*** Move to:` 四种指令，并对**每一个**受影响的 `prd.md`/`spec.md`/`plan.md` 应用同一套判定（一个 patch 改多个文档时不得只看第一个）。
- **A12** `hooks-codex.json` 接上 `PreToolUse`（`apply_patch` → `capability-gate`），并在 `runtime.md` 标注为 **documented，待实测**。
- **A12b** **`PostToolUse` 不接 `apply_patch`。** `capability-evidence` 的判定是工具类（`Skill`/`Agent|Task`/`mcp__*`），`apply_patch` 是编辑工具**不是能力**，接上去只会每次 exit 0、一条记录也不写 —— 那正是一条静默无效的接线。Codex 上的能力证据要靠 `Skill`/MCP 调用，与本改动无关。见 Q5。
- **A13** `hooks/smoke-test:5272-5277` 那条「禁止给 Codex 接线」的断言被替换为「Codex 已接线且解析正确」的正向断言，且包含 `apply_patch` 多文件 patch 的夹具。
- **A14** 用户在一台真实 Codex 机器上验证通过后，`runtime.md` 的 Codex 列才从 documented 升为 measured；未验证前不得升。
- **A15** `completion-gate` 不区分 Step 状态由谁写入：`progress` 写的与手改写的**判定完全一致**，由同一对夹具证明（同样的 `- Status: done`，一个有 progress 指纹、一个没有，两者都必须通过）。这条是 R11 的可执行形态——**不得**让新规则偷偷变成对 `progress` 的强制。
- **A16（已否决，2026-10-30）** 「`done` 的 Step 必须带可核验证据」**不做**。实测证明 Spec D1 选定的形态被一行声明满足——一个三个 Step 什么都没做的 Plan，只在验证段写三行 `ok` 就通过；而它同时会拒掉 73/93 份归档 Plan（连走过 `progress` 的 24 份里也有 7 份），因为它量的是「验证记录有没有按 Step 编号组织」而非「有没有验证」。D1 自己的入选理由（「不能只靠再写一行声明」）因此不成立。完整实测与推理见 `reject-a16.md` 与 `evidence-a16-fake-plan.md`。**保留 A17**：多重 `- Status:` 是文档自相矛盾，判定确定，不依赖对真假的判断。
- **A17** 同一 Step 块内出现**两个** `- Status:` 行时 `completion-gate` 报错，不猜哪个为准（现状是读最后一个，见 `completion-gate:103-105`）。
- **A18** A17 只作用于活动任务；`achieved/` 下的 93 份归档 Plan 在 `archive` 时**不因 A17 被拒**（用一个含旧格式 Step 的归档夹具证明）。原 A16 已否决（2026-10-30），其归档侧要求随之取消。

## In Scope

- **`capability-gate` 支持 `apply_patch`**：从 `tool_input.command` 的 patch 原文解析目标路径（A11）。
- **`hooks-codex.json` 接线**：`PreToolUse`（门禁）与 `PostToolUse`（证据捕获）（A12）。
- **`capability-gate` 读 `## Approval`**（A9/A10）。
- `hooks/smoke-test`：替换禁止 Codex 接线的断言，新增 patch 解析夹具（A13）。
- `CONTRIBUTING.md` 的宿主覆盖规则（已在本任务中加入，附 smoke 钉）。
- `runtime.md` 的 Codex 列与「not wired / not supported」措辞修正、`hooks/README.md`、`CHANGELOG.md`。
- 本任务的 TaskFlow 文档与 `TaskFlowDocs/todo.md` 条目状态。
- **`completion-gate` 的多重 `- Status:` 报错**（R12、A17）。**Step 证据校验不做**——2026-10-30 实测否决，见 A16 与 `reject-a16.md`。原先「中途在场加提示」的思路也已由事实 4/5 降级。

## Out of Scope

- **把 `capability-gate` 扩展成实现阶段的硬 gate。** `TF-20261027-e4ba77` 已明确否决，理由成立：那会把「提醒问题」变成对普通重构编辑的新硬 gate，代价按每次编辑计。本任务不翻案。
- **要求每次实现都必须有 stage 记录。** 事实 8 显示缺口在收敛，强推会变成噪音。
- **外部搜索相关（[[TF-20261027-e8c6dc]]）。** 只在「若本任务落地则该问题可能用散文解决」这一点上相关，不在范围内。
- **dsh 的门禁缺口。** 同样未接线，但用户未提出，且本任务已经很大。按新规则记为 **not wired**，留待后续。

> `capability-gate` 不读 `## Approval`（事实 9 的 ②）**已由用户 2026-10-29 裁定纳入范围**，从 Out of Scope 移出，见 R6。

## Risks / Deferred Items

- **Codex 无法在本机验证（最大风险）。** 本机没有 Codex，A12 的接线只能靠文档 + 夹具验证；真机行为由用户确认（R9/A14）。**在用户确认前，`runtime.md` 只能写 documented。**
- **patch 解析是新解析面。** `apply_patch` 的原文格式由 Codex 定义，可能与文档不一致。A11 必须容忍解析失败的**安全默认**——解析不出来时是拒绝还是放行，须在 Spec 里明确决定，不能由实现顺手决定。
- **一次 patch 改多个文件。** 只看第一个匹配会漏掉后面的 `prd.md`，A11 要求逐个处理。
- **「做了但没用」的风险仍在。** 一个每 N 次调用重复恒定语的行，第 20 次之后同样是背景噪声。若不能说明**注入内容会随状态改变**，加频率只是把噪声变密。
- **成本风险（事实 10）。** 朴素实现会让每轮多花数十秒。
- **A16 的「证据形态」是最难的一处 —— 2026-10-30 实测后已否决。** 当时的判据：若 Spec 给不出一个真能区分「验证过」与「写了句话」的形态，正确做法是缩小承诺并在 PRD 里改 A16，而不是实现一个查不出东西的检查。实测正是这个结果：D1 的形态被一行 `ok` 满足，且会拒掉 73/93 份归档。按判据执行，A16 撤销，见 `reject-a16.md`。

## Open Questions

- **Q1 已结（2026-10-29）。** 「走偏」的可判定定义：**Step 闭合绕过 `hooks/task progress`，改用手改**。可从 transcript 数出来（`progress` 调用数 vs 代码编辑数）。
- **Q2 已结（2026-10-29，用户澄清）。** 用户说明观察条件是「非常长的任务 + 不断被引导」，**发生在 Codex 上**。本机没有 Codex 会话记录，且 Claude Code 侧的对照（520 prompt、15 次打断、29 次 progress、未走偏）说明「长 + 被打断」不是充分条件。**结论：不再追这条因果，改判为「Codex 缺门禁」这一机制事实**（事实 10）。
- **Q3 已结。** Codex 官方支持 `PreToolUse`/`PostToolUse` 与 `additionalContext`，因此不再需要「为未测能力做设计」的顾虑——按 A12 直接接线、按 A14 待真机确认。
- **Q4 已决（2026-10-29，依据仓库既有先例）。** `apply_patch` 解析不出任何目标路径时，gate **不拒绝**——因为现有 gate 对「不是本任务文档」的路径一律 `exit 0`（`capability-gate:95-100`），一个不含 `TaskFlowDocs/**/{prd,spec,plan}.md` 的 patch 本来就不该被管。
  但**解析失败**与**确实无关**必须分开：前者（`apply_patch` 有内容、但没有一条 `*** … File:` 指令）属于**这个 gate 认不出该宿主**，与「读不到 `> Task version:`」同类，现有先例是 **deny**（`capability-gate:117`）。所以：**解析不出路径但 patch 非空 → deny，并说明是 gate 问题、给出补救命令**；解析出路径 → 逐条判定。
- **Q5 已决（2026-10-29，实测）。** 不接 `PostToolUse`/`apply_patch`。`capability-evidence` 的谓词是**能力类工具**（`Skill`/`Agent|Task`/`mcp__*`），`apply_patch` 是编辑工具。实测：`tool_name=apply_patch` 喂给它 → `exit=0`，evidence 文件行数不变。接上去是静默无效的接线。见 A12b 与事实 11。
