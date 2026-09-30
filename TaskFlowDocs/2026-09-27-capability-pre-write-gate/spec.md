# Spec — Block the first body write of prd/spec/plan until a capability-class tool was ac
> Task version: v2

## Objective and Success Criteria

为 PRD/Spec/Plan 三份文档建立一道**写前门**：在 Agent 写下任一份正文之前，该 stage 必须已经有一次真实的能力类调用（或一次显式登记的 Unaided 决定）。门的判据是**真实调用流**，不是文档里的文字。

成功标准（对应 PRD 的 A1–A12）：

- 无调用而直接写正文 → 被拒，且拒绝消息自带该 stage 的概念类与逃生舱命令。
- 有一次真实 `Skill`/`Agent`/MCP 调用 → 放行；放行后该证据被消费，下一份文档需要**新的**调用。
- `task unaided <stage> --considered "<概念类>"` → 一次显式动作同时登记并放行；缺参数或概念类不合词表则失败。
- Agent 无法用 `Write`/`Edit` 写证据文件本身。
- 非活动任务目录（同机其他会话、其他仓库、`TaskFlowDocs/achieved/**`）上完全 no-op。
- `bash hooks/smoke-test` 与 `hooks/smoke-test-windows.ps1` 全绿，`tools/fixture-compare` 仍通过。

## Architecture Boundaries and Responsibilities

三层，职责不重叠：

| 组件 | 职责 | 明确不做 |
| --- | --- | --- |
| 证据钩子（`PostToolUse`，matcher 覆盖能力类工具） | 真实调用发生后追加一条证据记录。只记事实，不做判断 | 不判定 stage、不判断相关性、不写核心文档 |
| 前置门（`PreToolUse`，matcher `Write\|Edit`） | 从**目标文件路径**解析任务与 stage，判定该 stage 是否已可放行；放行时消费一条证据 | 不读文档文字作为判据、不依赖"当前任务"这类全局状态、不写核心文档、不碰 Approval |
| `hooks/task unaided` | 显式登记一次 Unaided 决定（写入同一种证据记录，`kind=unaided`），并因此放行 | 不自行判断概念类是否"合理"，只校验它在相位词表内 |
| `hooks/task approve`（改造） | 对每个必需 stage，要求 `plan.md` 的 Skills 行与一条**同版本**的放行记录对账 | 不再以文字形状为唯一判据；不引入产品白名单 |

`plan.md` 的 `## Skills / Tools Used` 由此从"写前声明"降级为**报告**：它仍存在、仍必需、仍被 approve 校验，但它的作用是陈述证据已经证明的事实，而不是替代证据。这是 OQ1(b) 的落点，也是三份文档能够统一门控的前提。

`runtime.md` 的 must/may-not 全部保持：门与证据钩子都不创建/改写核心文档、不碰 `## Approval`；`task approve` 依旧只是转录人的决定。

## Project Structure / Affected Files

```text
hooks/
├── hooks.json                 # 新增 PreToolUse(Write|Edit) 与 PostToolUse(能力类) 接线
├── capability-evidence        # 新增：PostToolUse 侧，追加一条证据
├── capability-gate            # 新增：PreToolUse 侧，判定 + 消费
├── task                       # 新增 unaided 子命令；approve 的 stage 校验改为对账
└── smoke-test                 # 新增门/逃生舱/no-op 边界/版本失效用例
skills/taskflow/
├── SKILL.md                   # 契约改写：记录的家从 plan.md 移到证据存储
└── references/
    ├── artifacts.md           # Skills 段的语义由"写前声明"改为"报告"
    └── runtime.md             # 事件映射表补 PreToolUse 一行，并记录钩子契约的实测版本
README.md / README.zh-CN.md     # 行为对齐
CHANGELOG.md, marketplace pin   # 发版才在真实会话生效
```

证据存储不在工作树内（见下），所以不产生新的受版本控制的文件。

## Interfaces, Data Flow, and Contracts

### 证据存储的位置

放**仓库的 git 目录内**，经 `git rev-parse --absolute-git-dir` 解析：

```text
<absolute-git-dir>/taskflow/evidence      # 追加型，一行一条
<absolute-git-dir>/taskflow/released      # 追加型，一行一条
```

选它的理由：对 `git status` 不可见；跨会话与跨 compact 存活（**不**按 session id 分片，否则一次压缩就会把合法的继续写入拦死）；linked worktree 各有自己的 git dir，于是**按任务分支天然隔离**；不会被归档进 `achieved/`，也不会被 `hooks/version` 拷进 `old/vN/`。仓库已有读绝对 git dir 的既有实现（`78390cd`），直接复用。

代价（明说）：仓库重新 clone 或 worktree 被 prune 后证据消失。这对门的用途无害——新 clone 本来就是新任务。

**存储的解析方向两处不同，这是必须写清的一点：**

- 证据钩子（`PostToolUse`）**没有文件路径可用**——`Skill` 的 `tool_input` 只有 `{skill, args}`。它按事件里的 `cwd` 解析：`git -C <cwd> rev-parse --absolute-git-dir`。若该仓库没有 `TaskFlowDocs/` 下的活动任务则 no-op，以免污染非 TaskFlow 仓库。
- 前置门（`PreToolUse`）**按目标文件的目录**解析：`git -C <dir-of-target-file> rev-parse --absolute-git-dir`。这样它读到的一定是"这份文档所在工作树"的存储，而不是 cwd 那个。

支撑两者一致的是 TaskFlow 已有的不变量：**一个任务 = 一个工作树 = 一个证据存储**，所以记录里不需要出现任务 id。副作用（已知、可接受）：若 Agent 在 base checkout 里调用能力、却把文档写进某个 linked worktree，证据会落进 base 的存储、门的判定会拒绝；拒绝消息会引导它重新调用，这正是"逐阶段新鲜度"的正常行为。

### 两条记录的格式

```text
evidence:  <line-no 隐式>  kind|capability
released:                  version|stage|line-no|kind|capability
```

- `kind` ∈ `invoke`（钩子写入）| `unaided`（`task unaided` 写入）。
- `capability` 是能力标识：`Skill` 取 `tool_input.skill`（实测形如 `agent-skills:spec-driven-development`），`Agent` 取 `tool_input.subagent_type`，MCP 取 `tool_name`。
- `stage` ∈ `PRD` | `Spec` | `Plan`。
- 字段用 `|` 分隔；写入前把值里的 `|` 与非打印字符剥掉，保证 awk 可解析。

### 关键设计：stage 在**消费时**才被赋值，不在记录时

证据钩子**不可能知道**当前在做哪个阶段，它只知道"有一次调用发生了"。stage 是门在放行某份文档时才贴上标签的。这正是这套设计不需要任何"阶段 → 工具"映射的原因，也是它比 SKILL.md 现行措辞更耐维护的地方：能力与阶段在数据流上是解耦的，门负责配对。

### 门的判定算法

触发：`PreToolUse`，`tool_name` ∈ {`Write`,`Edit`}。

1. 取 `tool_input.file_path`；**先把 `\` 归一成 `/`**，再解析为绝对路径（相对路径按事件 `cwd` 拼接）；`basename` ∈ {`prd.md`,`spec.md`,`plan.md`}，否则 **exit 0（no-op）**。

   归一必须发生在**任何**路径判断之前，理由不是整洁：宿主在 Windows 上投递的是反斜杠路径（claude-code #83877 / #64432 实测确认），而 `${file_path%/*}` 这类切分只认正斜杠——不归一就会"切不出目录 → 命中下面的 no-op 守卫 → 静默放行"。v1 正是这样在 Windows 上完全失效的，且失败是静默的。判据是"同一份文件的不同拼写得到同一判定"，见 I9。
2. 该文件的直接父目录必须是 `<root>/TaskFlowDocs/<task-id>/`，且 `task-id` ∉ {`achieved`,`repository-docs`}，且 `<task-id>/plan.md` 存在（活动任务）。否则 **no-op**。
3. `stage` = prd→`PRD`，spec→`Spec`，plan→`Plan`。
4. 读该任务 `plan.md` 的 `> Task version:` 得 `V`。
5. 若 `released` 中已有 `V|<stage>|…` → **放行**（幂等，不重复消费；同一版本内对同一文档的后续编辑不再拦）。
6. 否则取 `consumed` = `released` 中**所有版本**的 `line-no` 最大值（无则 0）——**消费是全局的，不按版本重置**：证据文件是一条时间线，某个版本已经花掉的行就是花掉了，版本升级不能拿旧证据来满足。
7. `evidence` 的总行数 > `consumed` → 取下一条（`consumed + 1`，**队列式、最旧优先**）并追加 `V|stage|consumed+1|kind|capability` 到 `released`，**放行**。取最新一行会把"先攒几次调用再动笔"这种正常节奏里攒下的调用永久作废。
8. 否则 → **拒绝**，消息含：缺失的 stage、该 stage 的相位概念类、以及可复制执行的 `hooks/task unaided <stage> --considered "…"` 命令。

第 6–7 步就是"逐阶段新鲜度"：每份文档各消费一条新证据，同一次调用不可能同时满足两个 stage。

### `task unaided` 契约

```text
hooks/task unaided <PRD|Spec|Plan> --considered "<concept class>" [--root <path>]
```

- 校验 `<stage>` 合法、`--considered` 非空、概念类命中相位词表（复用 `require_stage` 现有词表，不新造）。
- 通过则在 `evidence` 追加 `unaided|<concept class>`，随后的门按第 7 步放行。
- 不通过则退出码 `2`（需用户输入），并说明是缺参数还是概念类不合词表。

## Invariants and Compatibility

- **I1 路径唯一决定行为。** 门的行为只是目标文件路径的函数，不读任何"当前任务"状态。本机实测 `~/.claude/settings.json` 的 hooks 是全机全局、对每个并发会话与项目都触发的，所以这条是正确性条件而不是设计洁癖——邻仓一个 `prd.md` 绝不能被拦下。
- **I2 证据不可由 Agent 用 `Write`/`Edit` 写入。** 门拒绝目标是证据存储路径的 `Write`/`Edit`。**天花板声明**：Agent 仍可用 `Bash` 写它，所以这是纪律级而非密码学级的防伪；要真正堵死需要签名，v1 明确不做。
- **I3 不锁死。** 证据缺失（新 clone、换机器、非 Claude Code host）时门拒绝，但 `task unaided` 永远可用，因此用户始终有一条一命令的出路。
- **I4 版本使证据失效。** Task version 从 v1 升到 v2 时，v1 的 `released` 记录不满足 `V=v2`，三个 stage 自动重新需要调用。不需要额外清理步骤。
- **I5 门的失败安全。** 门在任何路径上都不写核心文档、不碰 Approval；最坏的副作用是少写或多写一条 `released` 记录，而它只影响门自身，不影响任务事实。
- **I6 非 Claude Code host 无门。** Codex / CodeBuddy / dsh 保持现状（仅 approve 的形状校验）。这是用户已批准的 v1 范围，必须在 `runtime.md` 写明，避免被误读为"全平台已保证"。
- **I7 兼容：** `promote` / `version` / `archive` / `reopen` 都是 Bash 调用，不经过 `Write`/`Edit`，因此不受门影响——这是 A7 的机理由。
- **I8 钩子契约对版本敏感。** 必须记录门所依赖的 `PreToolUse`/`PostToolUse` 字段与 matcher 语义是针对哪个 Claude Code 版本实测的（本任务实测于 2026-09-27）。
- **I9 路径分隔符不得被假设（v2）。** 判据是"同一份文件的不同拼写得到同一判定"：`C:\a\b\prd.md`、`C:/a/b/prd.md`、`/c/a/b/prd.md` 必须同判。实现手段是入口归一（`\`→`/`），不得依赖某一种拼写。**为什么单列一条**：v1 违反了它却不报错——不同拼写得到的是"拦"与"不拦"，而"不拦"与"本来无物可拦"在外部不可区分（宿主侧同类问题见 claude-code #83877）。任何"按路径匹配"的新 hook 都必须满足本条。

## Validation and Error Semantics

| 情形 | 行为 | 退出 |
| --- | --- | --- |
| 非活动任务目录 / 文件名不匹配 | no-op | 0 |
| stage 尚无证据 | 拒绝，消息含 stage + 概念类 + 逃生舱命令 | deny（并可 exit 2） |
| stage 已有同版本放行记录 | 放行，不重复消费 | 0 |
| 有新证据 | 放行并消费 | 0 |
| Agent 写证据文件 | 拒绝 | deny |
| `task unaided` 参数/概念类不合法 | 明确报错 | 2 |
| 门自身出错（git dir 不可解析、awk 失败等） | 按拒绝处理，并在消息中说明**是门出错而非用户违规**，同时给出 `task unaided` 出路 | deny |
| 工作流层面的硬阻塞 | 按 `CODE_STYLE.md` | 3 |

冒烟套件必须覆盖：拒绝/放行矩阵、逐阶段新鲜度（写完 `prd.md` 后直接写 `spec.md` 应被拒，中间再调用一次则放行）、`unaided` 正反例、自写证据被拒、**no-op 边界（外来仓库路径 / `achieved/` / 非任务目录）**、版本升级使证据失效、以及门出错时不产生副作用。

## Code and Test Constraints

- 只用 POSIX sh + `awk`/`sed`，bash 3.2 + BSD userland 下限：不得出现 `declare -A`、`mapfile`、GNU-only `sed -i`。`tools/fixture-compare` 是这条的守卫。
- 冒烟套件在**无解释器的 PATH** 下运行 hooks，新脚本不得引入任何语言运行时。
- 扩展名无关的 bash 脚本，放在 `hooks/` 平铺目录；Claude Code 走 `run-hook.cmd` 跨平台启动器。
- 退出码遵循 `CODE_STYLE.md`：`0` 通过 / `2` 需用户输入 / `3` 工作流阻塞。
- 复用优先：相位词表与判定逻辑取自 `require_stage`，绝对 git dir 的读法取自现有实现，`promote` 已生成的 Skills 段直接沿用。不新增依赖。
- 门的检查在被拒绝时不得产生副作用；仅在放行时追加一条记录。

## Design Decisions and Alternatives

- **证据存 `.git` 内**，而非任务目录 dotfile：后者要改 `.gitignore`，会被 `hooks/version` 拷进 `old/vN/`，还会进入归档与 `archive` 的"未提交文件"检查。`.git` 方案零受控文件改动且按 worktree 隔离。
- **stage 在消费时赋值**，而非在记录时：钩子无法知道阶段；记录时赋值就必须给工具打阶段标签，那正是要避免的映射。
- **不读会话 transcript**：实测其落盘是异步的（"may not include the current turn's most recent messages"），且是 Claude Code 私有格式，只有四 host 中的一个有。
- **不按 mtime 强制**：本机已证 `PreToolUse` 能在写入**之前**取得控制权，所以根本不需要用时间戳去事后推断时序。
- **保留 `Unaided` 出口**：相关性无法机械验证。去掉出口要么逼出假调用，要么在环境确实没有对口能力时把用户锁死。保留出口 + 显式登记，是这个约束下能拿到的最强契约。
- **`(a)` 方案被否**：不门控 `plan.md` 只把洞缩小三分之一，而 `plan.md` 恰好是用户最常抱怨的那个文档。
- **本次一并删除的东西（连同原因）**：`plan.md` 的写前言明顺序纪律（记录移出后已无对象，时序改由门机械保证）；`require_stage` 的大任务概念词表正则（词表校验移到 `task unaided` 唯一入口，在 approve 重校验一段已被存储保证的文本是冗余）；`invoke line is empty` 分支（被"行必须匹配一条 invoke 记录"完全覆盖）；`smoke-test` 里绑实现文本的断言 `grep -q 'require_stage PRD'`（断言内部实现而非行为，重构即失效）。
- **考虑后拒绝的删除：`## Skills / Tools Used` 段本身。** 存储住在 `.git` 内，重新 clone 或 worktree 被 prune 即消失；归档的任务目录才是**耐久记录**。删掉这一段，归档后就无法看出当时到底调用了什么。代价是报告可能漂移，靠 `task approve` 的对账压住——这是保留它的前提，不是可选项。

## Open Questions

无阻塞项。残余未知一项，不阻塞设计：MCP 工具的 matcher 是裸 `mcp__` 前缀匹配还是必须写 `mcp__.*`。它只影响谓词的第三条分支（`Skill` 与 `Agent` 两条主路径已实测）；实现时用一次真实 MCP 调用定案，并记入 `runtime.md`。
