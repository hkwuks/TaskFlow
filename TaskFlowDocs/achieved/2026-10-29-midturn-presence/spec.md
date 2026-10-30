# Spec — Stay present inside a long implementation run, not only at the prompt
> Task version: v1

## Objective and Success Criteria

**Objective.** 关闭三个已被测量证实的缺陷，让 TaskFlow 在 Codex 上不再等于裸跑，并让 Step 的「完成」有可核验的含义：

1. **Codex 没有门禁**（PRD 事实 11）。仓库把它记成宿主限制，实际是未实现。
2. **`capability-gate` 不读 `## Approval`**（PRD 事实 9 的 ②）。
3. **Step 状态只有声明、没有证据**（PRD 事实 4、5）。`completion-gate` 无法区分「验证过」与「写了一句 `- Status: done`」。

**Success criteria** 就是 PRD 的 A9–A18；本 Spec 说明它们如何在代码里成立。**A16 已于 2026-10-30 实测否决**（见 `reject-a16.md`），本 Spec 的 D1/D2 作为该否决的证据保留，不再是实现依据。

## Architecture Boundaries and Responsibilities

三个脚本，职责不重叠：

| 组件 | 何时 | 决定什么 | 本任务的改动 |
|---|---|---|---|
| `capability-gate` | `PreToolUse`，写 `prd/spec/plan.md` 前 | **放行还是拒绝一次写入** | 读 `## Approval`；支持 `apply_patch` |
| `completion-gate` | 由 `task complete` / `archive` 调用 | **这个 Plan 算不算完成** | 每个 `done` 的 Step 必须有证据；多重 `- Status:` 报错 |
| `hooks/task` | Agent 显式调用 | 写文档 | 不改 |

`capability-gate` **不**决定 Step 是否闭合，`completion-gate` **不**拦截写入。这个分工是本任务要守住的边界：把它们合并会让「拒绝一次编辑」和「拒绝一次归档」共用一个判定，而两者的代价完全不同。

## Project Structure / Affected Files

```
hooks/approval-check      新增：Plan 审批判定的唯一实现
hooks/capability-gate     新增 $APPROVAL 段（调 approval-check）；新增 apply_patch 路径解析
hooks/completion-gate     改调 approval-check；新增 Step 证据校验；多重 Status 报错
hooks/hooks-codex.json    新增 PreToolUse 事件
hooks/smoke-test          替换「禁止给 Codex 接线」断言；新增夹具
skills/taskflow/references/runtime.md   事件表与 Codex 段落
hooks/README.md           接线说明
CONTRIBUTING.md           宿主覆盖规则（本任务已加）
CHANGELOG.md
```

## Interfaces, Data Flow, and Contracts

### C1. `capability-gate` 的输入抽象

现在它只认一个来源：`tool_input.file_path`。改动后有两个来源，**分流发生在读取 `file_path` 之前**：

```text
tool_name == "apply_patch"  →  解析 tool_input.command 得到路径列表
否则                        →  用 tool_input.file_path（单条）
→  两条路径汇合为「一组目标路径」
→  对每个路径独立走现有的 base/stage/task_dir 判定
→  任何一个被拒 → 整体 deny
```

**契约：**

- `apply_patch` 的解析取 `*** Update File:` / `*** Add File:` / `*** Delete File:` / `*** Move to:` 四种指令的目标路径，逐条处理。
- **`*** Move to:` 算两个路径**（Q6）：旧路径按删除、新路径按新增，**两个都走判定**。只算新增会留下缺口——把 `prd.md` 从任务 A 移到任务 B 时，A 那边因为「文件不见了」而不被检查，而文档确实离开了那里。
- **`tool_name` 的比较是精确的**：Codex 的 matcher 别名（`Edit`/`Write`）只影响 hook 是否触发，不影响 stdin 里的 `tool_name`——官方文档写明「hook input still reports `tool_name: apply_patch`」。所以脚本不需要认别名。
- **deny 的 payload 形状不变**（`hookSpecificOutput.permissionDecision: deny`）——Claude Code 与 Codex 两边的文档都接受同一个形状（PRD 事实 11 的表）。

### C2. `apply_patch` 解析失败的判定（PRD Q4 的可执行形态）

| 情况 | 判定 | 依据 |
|---|---|---|
| 解析出至少一个路径 | 逐条走现有判定 | — |
| `apply_patch` 的 command 为空 | `exit 0` | 没有编辑发生 |
| 非空，但没有任何 `*** … File:` 指令 | **deny**，说明是 gate 认不出该格式 | 与「读不到 `> Task version:`」同类（`capability-gate:117`），是 gate 问题不是规则问题 |
| 有路径但不在 `TaskFlowDocs/<task>/` 下 | `exit 0` | 现有的「不是本任务文档」分支（`capability-gate:95-100`） |

**为什么解析失败要 deny 而不是放行**：放行会让门禁在格式变化后**静默失效**，而「声称有门禁、实际没有」正是本任务要消灭的失败模式（R10）。deny 的代价是一次误拦，且消息里会说明这是 gate 的问题。

### C3. `## Approval` 判定的契约

**判定抽成 `hooks/approval-check`，`completion-gate` 与 `capability-gate` 都调它**（Q7）。同一份 Plan 的审批结论只有一处产生。

```text
usage: approval-check <plan.md>
exit 0  — 已审批，且 Approved version 等于 Plan 的 Task version
exit 1  — 未审批；stderr 一行说明哪一项不满足
```

判定的内容（从 `completion-gate:86-91`、`:110-111` 原样搬出，不改语义）：

- `- Status: approved` 只在 `## Approval` 段内匹配，写在别处不算。
- `- Approved by:` 不得是 `pending`。
- `- Approved version:` 必须等于 `> Task version:`。**只看 `Status: approved` 不够**——v2 的文档配着 v1 的批准，是两份不同的东西。
- `## Approval` 段缺失或为空 → 未审批。

**「首次正文写入」的定义**：沿用现有的 `released` 存储。一个 `(task, version, stage)` 已被释放过，后续编辑不再检查——这条现有行为**不变**。

**检查时机（2026-10-29 修正）**：审批是**开工许可**，不是写文档许可（`SKILL.md:193`：`in_progress` 才要求批准）。所以 `capability-gate` **不**阻止 `planning`/`ready` 阶段写任何文档——原设计「未审批不得写 `prd.md`」会锁死每个新任务的第一步（PRD 必须在审批前写出来）。

它只拦一种情况：**当前 `> Task version:` 与 `- Approved version:` 不一致时，继续写那份已批准的文档**。即「拿旧批准写新版本」。
判据：`Approved version` 为空或是 `pending` 时视为**尚未批准过任何版本**，此时不拦（`planning` 阶段）；一旦它填了版本号，就必须与当前版本相等。

**归档案的检查已经存在**：`hooks/archive:44` 调 `completion-gate`（自 `be69289`/2026-10-24），未审批任务会被拒。实测：`current Task version is not approved`。本任务不新增该检查，只补回归断言。

**调用方式**：`approval-check` 与其它 hook 一样是独立的可执行脚本（不 source），由两个 gate 用 `bash` 调用。这与 `capability-gate` 里 `stray_evidence` 的处境不同——那个是内部函数，而审批判定必须被两个进程共享。

## Invariants and Compatibility

- **I1** 已审批版本的 `capability-gate` 行为**逐字节不变**。A15/A18 用夹具证明。
- **I2** `completion-gate` 对 `achieved/` 下的任务不新增拒绝条件（R13/A18）。
- **I3** `progress` 的语义不变，**不新增任何强制**（R11/A15）。`progress` 写的 Step 与手写的 Step 在 `completion-gate` 眼里完全同等。
- **I4** 现有 smoke 的 100+ 节全部保持通过。
- **I5** 不引入新的运行时依赖：POSIX `awk`/`sed` + bash 3.2（`CLAUDE.md` 的既有约束）。

## Validation and Error Semantics

所有拒绝都走现有的两条通道，**不新增通道**：

| 组件 | 通道 | 退出 |
|---|---|---|
| `capability-gate` | `hookSpecificOutput.permissionDecision: deny` + 原因 | `exit 0`（由 payload 表达拒绝） |
| `completion-gate` | stderr 一行命名失败条件 | `exit 1` |

错误消息必须**可执行**：现有 gate 的惯例是给出确切的补救命令（`bash hooks/task unaided STAGE --considered '…'`、`bash hooks/task recover`）。新增的消息同样如此。

## Code and Test Constraints

- `hooks/*` 是 **smoke 集合**：改 hook 一定会跑 smoke（`tools/workflow-affected`）。新断言写进 `hooks/smoke-test`。
- **不使用 `printf … | grep -q`**：`pipefail` 下大文件会 141（`completion-gate:19-29` 记录了这次事故）。读 Plan 一律单次 `awk`。
- 每个新条件配一个**能变红**的用例，并做变异验证（破坏条件 → 命名断言变红 → 逐字节恢复）。
- `hooks/smoke-test-windows.ps1` 必须保持纯 ASCII。

## Design Decisions and Alternatives

### D1. 为什么「Step 必须有证据」不可行 —— 设计后实测，已否决

> **2026-10-30 结果：本节的方案被实测否决，A16 撤销。** 下文保留作为否决的证据链。结论写在 `reject-a16.md`，两处关键实测：
>
> 1. **它被一行声明满足。** 一个三个 Step 什么都没做的 Plan，只在验证段写三行 `ok`，按下面的形态判定为通过。本节自己的入选标准（「不能只靠再写一行声明」）因此不成立。
> 2. **它拒掉的 73/93 份归档里，包含 7 份真正走过 `progress` 的。** 因为它量的是「验证记录有没有按 Step 编号组织」，不是「有没有验证」——而只有部分 Step 走 `progress` 是常态（`2026-10-27-close-step-status`：Step 2 有指纹，Step 1/3/4 手写）。
>
> 根本原因：`hooks/task progress` 写的 `- <date> Step <N>: <text>` 与手写的同一行在文件里逐字节相同，**任何只读 Plan 的检查都无法区分二者**。本节下表把「要求在 `## Verification / Review` 里出现指认该 Step 的行」标为 ✓，那个 ✓ 是错的。

A16 要求 `done` 的 Step 带可核验证据。**设计前先量了现状：93 份归档 Plan 里只有 5 份的 `## Verification / Review` 是空的（88 份有内容）。**

这个数字决定了提案的形态：**要求不是新的，证据也不是新的 —— 缺的只是「把两者关联起来」。**

| 方案 | 判定 |
|---|---|
| 要求 Step 里出现某段固定文字 | ✗ 又一条形式主义：查不出「验证过」与「写了句话」的区别 |
| 要求 `## Verification / Review` 非空 | ✗ 88/93 已经满足，等于不约束 |
| **要求在 `## Verification / Review` 里出现指认该 Step 的行** | ✓ 手写能写、`progress` 已经这样写、且**指认关系**是可核验的 |

**选定形态：**

```text
## Verification / Review 段内存在一行，包含 `Step <N>` 且 N 是该 Step 的编号
```

这同时覆盖两条路径：

- `hooks/task progress <task> <N> done "<text>"` **已经**写 `- <date> Step <N>: <text>`（`hooks/task:465`），因此走 `progress` 零改动即满足。
- 手写时补一行同样形状的文字即可。

**这条检查能查出什么、查不出什么，必须写明：**

| 能查出 | 查不出 |
|---|---|
| Step 声称完成，但 `## Verification / Review` 里没有任何指向它的一行 | 那一行是真是假 |
| 一个 Plan 里 4 个 Step 只有 2 个有记录 | 记录是否对应真正的验证 |

**它抓的是一个真实的失败模式**：Step 被标 `done`，而整个 Plan 的验证段从未提到它 —— 这正是手改收尾时的典型形态（PRD 事实 4 的样本：4 个 Step 一次脚本翻完，验证记录另写）。

### D2. 为什么拒绝 `progress` 强制（重申 R11 的可执行含义）

D1 的形态**刻意让两条路径都能满足**。若把条件写成「必须有 `progress` 的日期行」，那就变成了对 `progress` 的强制，违反 R11/A15。**这是本 Spec 最容易走错的一处**，因此 A15 用一对夹具把它钉住：同样一个 `done` 的 Step，一行由 `progress` 写、一行手写，两者都必须通过。

### D3. `apply_patch` 解析放在 `capability-gate` 里，不另开脚本

一个 hook 脚本的输入解析多一个分支，比对两个脚本保持同步便宜。且 `capability-gate` 的判定逻辑（base/stage/task_dir）完全复用，不需要重复。

## Open Questions

- **Q6 已决（2026-10-29，用户裁定）** `*** Move to:` 按**旧路径删除 + 新路径新增**处理，两个路径都走门禁。理由：只算新增的话，把 `prd.md` 从任务 A 移到任务 B 时，A 那边因为「文件不见了」而不被检查——而文档确实离开了那里。
  **格式风险仍在**：本机没有 Codex，`*** Move to:` 后面的路径写法按官方文档实现，A14 的真机验证必须包含一个 Move 用例。
- **Q7 已决（2026-10-29，用户裁定）** 抽成 `hooks/approval-check`，`completion-gate` 与 `capability-gate` 都调它。理由：这个仓库已经出现过同类分歧——`completion-gate` 的注释里就记着两个读同一份文件的实现漂移过。判定只有一处，就不会有第二次。
