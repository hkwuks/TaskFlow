# 证据锚点：让一次能力调用落在它真正归属的那个工作树

> Task version: v1
> Status: checking

## Goal

修掉同一失败模式的两半——**干活的落点不是以为的落点**：

1. **hook 侧**：`capability-evidence` 按事件 `cwd` 定位证据库，`capability-gate` 按目标文件路径定位。两者只在「会话 cwd 恰好就是任务 worktree」时一致；否则调用记录下来却记到了别处，gate 随后拒绝写入，且拒绝的理由**指向错误的原因**。
2. **文档侧**：`SKILL.md` 只说「move the work there」，不给可执行步骤，也不说明基础检出上的脏状态意味着什么。

修法分别落在两层，且**不合并两个证据库**：gate 在自己库里找不到时，有能力去同级 worktree 找到记录真正落在了哪里，并在拒绝信息里点名——让失配从「沉默 + 误导」变成「可诊断 + 可执行」。

## Background / Confirmed Facts

### B1·锚点确实是两个

| | 定位依据 | 代码位置 |
| --- | --- | --- |
| `capability-evidence` | 事件 `cwd` → `git -C` → `--absolute-git-dir` | `hooks/capability-evidence:60-67` |
| `capability-gate` | `tool_input.file_path` → 推任务目录 → `git -C "$task_dir"` → `--absolute-git-dir` | `hooks/capability-gate:102-124` |

`git rev-parse --absolute-git-dir` 在 linked worktree 里返回 `<common>/.git/worktrees/<name>`，在基础检出里返回 `<common>/.git`——**两者不同**。所以「事件 cwd 是基础检出、正在编辑的文件在任务 worktree」这一组合下，两个 hook 谈的不是同一个库。

### B2·已在本机复现（2026-10-11，`/tmp/anchors` 一次性夹具）

夹具形状：`repo`（基础检出）+ `wt`（linked worktree，`git worktree add ../wt -b fix/wt`）。

```
$ printf '{"hook_event_name":"PostToolUse","tool_name":"Skill","cwd":"/tmp/anchors/repo",...}' \
    | bash hooks/capability-evidence          # cwd = 基础检出
（无输出，exit 0）

$ find /tmp/anchors -path '*taskflow*' -type f
/tmp/anchors/repo/.git/taskflow/evidence       # ← 记录落在基础检出的库
/tmp/anchors/repo/.git/taskflow/evidence: invoke|probe:cap
```

同一次调用的效果对照：

```
$ ... file_path=/tmp/anchors/repo/TaskFlowDocs/2026-01-02-wt2/prd.md | bash hooks/capability-gate
（空输出 = 放行——它在基础检出的库里找到了那条记录，但那条记录属于另一个工作树）

$ ... file_path=/tmp/anchors/wt/TaskFlowDocs/2026-01-02-wt2/prd.md | bash hooks/capability-gate
{"hookSpecificOutput":{...,"permissionDecision":"deny",
 "permissionDecisionReason":"TaskFlow pre-write gate blocked stage [PRD]:
  no capability invocation is recorded for this task version. ..."}}
```

**记录确实写下了，也确实没被找到**；而且当基础检出里恰好有一个同名任务目录时，gate 会拿另一个工作树的记录放行。这是 PRD 的 In Scope 之外但必须记录的边界（见 Risks）。

### B3·本仓库的 store 现状（佐证不变量而非偶发）

`.git/taskflow/` 不存在，而 `.git/worktrees/<name>/taskflow/` 有四个——每个任务一个 `evidence` + `released`。也就是说：**至今为止的每次任务都恰好满足「cwd 就是任务 worktree」**，所以这个缺陷从未在本仓库的自我使用中显形，只在别人的用法里显形。

### B4·既有不变量（本轮不推翻）

`references/runtime.md` 的 four properties 之第一条明写：证据库在 git 目录里，**per worktree（one task, one worktree）**。`smoke-test` 有三节依赖它：每个任务夹具各建自己的 `git init` 仓库，`$cg_store` 取该夹具自己的绝对 git 目录；`approve` 从任务目录的 git dir 读回记录。

这条不变量是并行任务之间互不串账的原因。本任务**保留**它，只补「失配可诊断」。

### B5·`released` 的语义

`hooks/capability-gate:133-139` 明写消费是**全局的、不是 per task version**：`$3`（seq）取自 `evidence` 的全局行号，`consumed` 取 `released` 里 `$3` 的最大值。两条记录合并成一个队列需要重新定义排序，这是「真统一」方案的隐藏成本。

### B6·`SKILL.md` 的既有措辞

- L122-131「Isolate before the first document」：给了 `git worktree add` + `cd`，但「把工作搬过去」只在 L256（Phase 5）以一句 `then move the work there` 出现，没有步骤。
- L256 改写前是 `..., then move the work there.`。

### B7·既有断言

`smoke-test` 的 capability-gate 一节只用一个仓库夹具（`$cg_root/repo`），没有 linked worktree，所以它盖不到「两个 git 目录」这个形状——新增夹具节是必要的，不是重复。

## Requirements

- **R1**　`hooks/capability-gate` 在准备 deny 前，若本工作树的库里没有可用记录，去**同级 worktree** 查找是否存在记录了能力调用的 `taskflow/evidence`；找到时，拒绝信息必须点名该库的路径，并说明两侧分别是哪个工作树。
- **R2**　R1 的查找只用于**诊断**：它绝不能把别的 worktree 的记录当作本工作树的记录来放行。放行条件不变。
- **R3**　R1 的拒绝信息给出可执行的下一步：确认当前所在的工作树，以及把记录落在正确位置的办法（重跑一次调用，或按 `SKILL.md` 的步骤把工作搬进任务 worktree）。
- **R4**　查找必须廉价且有界：只在即将 deny 的路径上执行，不改变任何放行路径的开销；无 `git`、无同级 worktree、`git` 失败都必须静默降级到现有文案。
- **R5**　`SKILL.md` 的「Isolate before the first document」补可执行搬移步骤：`git worktree add` + 用 `git stash push -u` / `stash pop` 搬运未提交改动，并说明未修改的已跟踪文件不需要搬（它们在两个树里都在）。
- **R6**　同段说明「确认自己在哪个工作树」的可检查动作，以及基础检出的脏状态意味着什么（那是**另一个**工作树上的工作，不是本任务分支上的工作）。
- **R7**　`SKILL.md` Phase 5 的 `then move the work there` 改为指向 R5 的步骤，不再留一句无从执行的指示。
- **R8**　新增代码与断言仍落在 POSIX `awk`/`sed` + bash 3.2 地板内，不新增解释器。

## Acceptance Criteria

- **A1**　`smoke-test` 新增一节，夹具含基础检出 + 一个 linked worktree（与 B2 同形状），断言：cwd 为基础检出时写下的记录，在 gate 检查 worktree 内文件时被拒，**且拒绝信息含该记录真实所在的库路径**。
- **A2**　同一节断言：同一 worktree 内写入的记录仍正常放行（R2 不回归）。
- **A3**　变异验证：把 R1 的查找去掉，A1 变红。
- **A4**　`SKILL.md` 的两个段落被断言钉住：搬移步骤的三条命令、以及 Phase 5 指向该步骤的措辞。
- **A5**　`bash hooks/smoke-test` 全量通过；no-interpreter 一节仍通过。
- **A6**　`references/runtime.md` 的 four properties 增补一条：拒绝会点名记录的真实落点；不改变「库按工作树分离」这一条。

## In Scope

- `hooks/capability-gate`（诊断查找 + 拒绝文案）
- `hooks/smoke-test`（新增 main+worktree 夹具节）
- `skills/taskflow/SKILL.md`（搬移步骤、Phase 5 指向）
- `skills/taskflow/references/runtime.md`（properties 与 gate 描述）
- 本任务的 `prd.md` / `spec.md` / `plan.md` / Todo 条目

## Out of Scope

- **不合并两个证据库**：库仍是 per working tree，`capability-evidence` 的定位方式不变。
- **不让跨 worktree 的记录放行**：R2 明确禁止。
- `capability-evidence` 的 `active` 守卫（「任务创建前的调用不入账」）——那是 `TF-20261009-8abbd6` / `TF-20261009-cc463b` 的「已发生调研的入账」问题。(a) 方案只让失配可诊断，正是为了给那条留出干净的后续。
- Trae 宿主的接线：Trae 的 gate 走同一对脚本，本任务不新增宿主分支。

## Risks / Deferred Items

- **同名任务目录下的跨库放行仍未修。** B2 证明了它的存在：基础检出库里的一条记录能放行 worktree 里的同名任务文档。它需要「记录带工作树归属」才能修，那正是本任务排除的「真统一」。已记入 todo 的 Notes，供后续单独决策。
- **诊断查找是一层启发式。** 「同级 worktree」按 `git worktree list` 的路径集合判定；`git` 不可用、或记录落在 `.worktrees/` 之外的 worktree 都在静默降级之列（R4）。
- **搬移步骤是 prose。** `git stash push -u` 在基础检出有 staged 改动时的行为由 Git 定义，不由此处的文字定义；R5 的措辞只承诺「未修改的已跟踪文件不需要搬」这一条可核对的事实。
- **本任务落地后需一次发布才惠及已安装用户。**

## Open Questions

无。三个设计决定已由用户 2026-10-11 裁定：锚点取「保持库边界 + 失配可诊断」；搬移只补文档步骤、不加代劳命令；用新增 main+worktree 夹具节钉住。

## Version History

- v1 — planning。
