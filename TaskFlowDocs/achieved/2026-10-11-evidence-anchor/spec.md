# Spec — 证据锚点的诊断层：gate 拒绝时点名记录的真实落点

> Task version: v1

## Objective and Success Criteria

在**不改变**证据库边界（per working tree，one task one worktree）的前提下，让 `capability-gate` 的拒绝从「沉默 + 误导」变成「可诊断 + 可执行」：当本工作树的库里没有可用记录时，查明记录是否落在了**同级 worktree**，并在拒绝信息里点名该库的路径，同时给出重跑或搬移的可执行下一步。

成功判据：A1（失配被点名）、A2（同树放行不回归）、A3（去掉查找即变红）、A4（文档步骤被钉住）。

## Architecture Boundaries and Responsibilities

- `capability-evidence`：**职责不变**。仍按事件 `cwd` 定位，仍写本工作树的库。本 Spec 不改它的任何一行。
- `capability-gate`：放行逻辑不变；**新增一条只在即将 deny 时执行的诊断查找**。它读别人的库只为回答「记录落在哪」，永远不用来放行。
- `hooks/task unaided`：不变。它是把记录写进**本任务 worktree** 库的正确入口（`hooks/task:1008` 已拒绝在没有活跃任务的树里执行）。
- `SKILL.md`：负责「怎么不走到这个失配」，即搬移步骤。

## Project Structure / Affected Files

| 文件 | 改动 |
| --- | --- |
| `hooks/capability-gate` | 新增诊断函数 + 扩展末尾的 deny 文案（两处 deny：无记录、以及「已被花掉」） |
| `hooks/smoke-test` | 新增一节，夹具为主检出 + linked worktree |
| `skills/taskflow/SKILL.md` | 「Isolate before the first document」补搬移步骤；Phase 5 改指向 |
| `skills/taskflow/references/runtime.md` | four properties 增补一条；正文补一句 gate 描述 |

## Interfaces, Data Flow, and Contracts

### 诊断查找的契约

```text
capability-gate 在即将 deny 时：
  1. 取当前任务目录所属的 git common dir：git -C "$task_dir" rev-parse --git-common-dir
     （linked worktree 返回 <common>/.git，基础检出返回 `.git` → 归一为绝对路径）
  2. 枚举同级 worktree 的 git dir：
       <common>/taskflow/evidence                     ← 基础检出（若 task_dir 本就在基础检出，此即本库）
       <common>/worktrees/*/taskflow/evidence         ← 每个 linked worktree
     排除本库自身。
  3. 对每个存在的文件取行数 > 0 的第一个，记下它的 worktree 路径与行数。
  4. 把结果拼进 deny 文案；找不到则用现有文案。
```

**实现说明：common dir 从哪里来。** `spec.md` 的第一稿写的是 `git rev-parse --git-common-dir`。实测（git 2.43）它不可直接使用：在基础检出返回 `.git`，在 linked worktree 返回 `/abs/repo/.git`——**前者是相对路径，且相对于 worktree 根而不是被查询的目录**，归一化时无从判断基准。`--path-format=absolute` 能修好，但它要求 git ≥ 2.31，而这个 hook 在别人的机器上运行，抬高版本下限不是本任务该付的代价。因此改为从已经绝对化的 `--absolute-git-dir` 反推：路径含 `/worktrees/` 时取其前缀，否则它自己就是 common dir。

**为什么用 glob 而不是 `git worktree list`**：`git worktree list --porcelain` 的输出要按 `worktree <path>` 行解析，且路径可能含空格与反斜杠（Windows），在 bash 3.2 下需要额外的 while-read 与转义处理；而 `.git/worktrees/*` 与 `.git/taskflow` 这两个位置由 Git 的布局保证，用 `case` + 内建 glob 即可枚举，零解析、零外部命令。代价是：**不覆盖 `--separate-git-dir` 等非默认布局**，这类仓库静默降级到现有文案（R4 允许）。

**本库自身的排除**：`task_dir` 的 `--absolute-git-dir` 已在上方算得，与枚举结果作字符串比较即可。基础检出的任务目录不会枚举到额外的「本库」副本（`<common>/taskflow` 即其本库）。

### 拒绝文案的形状

```text
TaskFlow pre-write gate blocked stage [PRD]: <原有原因>. <诊断句，仅当找到时>.
TaskFlow is entered before the work and a capability is chosen inside the phase, so
invoke one first — any Skill, agent, or MCP tool — then write the document.
If no capability fits this phase, declare it:  bash hooks/task unaided PRD --considered '<class>'
```

诊断句（找到时）形如：

```text
Capability records exist for this repository but in a different working tree:
<path>/.git/worktrees/<name> (N records). This session is writing evidence where its
cwd points, and editing a document in <task_dir>, so the two disagree. Confirm with
`git branch --show-current` and `pwd`, then either re-run the invocation from this working
tree or move the work here — see SKILL.md, Isolate before the first document.
```

文案约束（与既有断言共存的硬要求）：**不含双引号、不含反斜杠**——它要被塞进 JSON 而不做转义。因此路径里的反斜杠必须先归一为 `/`（沿用上方既有的 `tr '\134' '/'`），且文案里不得出现 `"`。既有断言要求保留 `[<STAGE>]`、概念类别名、`task unaided <STAGE> --considered`。

## Invariants and Compatibility

- **I1**　放行判定与 evidence/released 的读写语义**完全不变**。诊断只在 `deny` 之前发生，且只读。
- **I2**　库仍是 per working tree。`capability-evidence` 一行不改。
- **I3**　无 `git`、无 common dir、无同级 worktree、glob 无匹配：全部静默降级到现有文案，退出码与输出形状不变。
- **I4**　文案保持 JSON 安全（无双引号、无反斜杠），这是既有 `deny()` 的契约。
- **I5**　新增命令仍落在 on-PATH 白名单内（`smoke-test` 的 no-interpreter 一节只 link 了 `awk sed grep cut tr od printf mktemp dirname basename cat date mv rm mkdir find head tail sort wc chmod cmp diff env ls pwd bash sh ln touch git`）。诊断只用 `git`、内建 glob、`case`、`printf`。
- **I6**　诊断查找**只在 deny 路径上**执行：gate 自身的耗时不希望被每一次写入拖长。

## Validation and Error Semantics

- 每一次 `git` 调用都带 `2>/dev/null` 并接受失败；失败即视为「找不到」，不改变 deny 原因。
- 诊断结果为「未找到」时，文案与当前**逐字一致**——既有断言（`cg_verdict` 系列）不会因此改动。
- 记录条数为 0 的文件视为不存在（与 gate 自身的 `total > consumed` 语义一致）。

## Code and Test Constraints

- bash 3.2 + BSD userland 下限；`$( )` 内的 heredoc 不得含撇号（Task A 的 macOS CI 失败根因）；`cmd && { ...; }` 是 bash 3.2 解析陷阱，用 `if ... then ... fi`。
- 新断言节必须自建夹具，不依赖前一节的 `$tmp` 状态；夹具用 `mktemp -d` 并在末尾清理。
- 夹具的 git 操作必须带 `-c user.email=... -c user.name=...`，与既有节一致。

## Design Decisions and Alternatives

| 决定 | 选择 | 备选与否决理由 |
| --- | --- | --- |
| 锚点 | 保持库边界，失配改为可诊断 | 「真统一」要把库移进 common dir、给记录加任务归属、并重定义 `released` 的全局 seq 排序（B5）；它会让并行任务共用一个队列，削弱隔离 |
| 搬移 | 只补文档步骤 | 代劳命令要处理 staged/unstaged/分支分叉，做错时比不做更危险；本仓库既有风格是拒绝 + 交出命令（`promote` 已是这个形状） |
| 钉住方式 | 新增 main+worktree 夹具节 | 现有 gate 节只有单仓库夹具，盖不到「两个 git 目录」这个形状 |
| 枚举方式 | glob `.git/worktrees/*` | `git worktree list` 要解析含空格/反斜杠的路径，bash 3.2 下成本高于收益；非默认布局静默降级 |

## Open Questions

无。
