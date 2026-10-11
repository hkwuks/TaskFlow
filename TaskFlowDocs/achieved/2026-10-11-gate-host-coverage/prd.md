# 前置能力门的宿主覆盖：让未接线的宿主上的 approve 不再是死路

> Task version: v1
> Status: completed

## Goal

`hooks/task approve` 要求一条 `taskflow/released` 记录，而 `released` 的唯一写入者是
`capability-gate`（`hooks/capability-gate:155`，已穷举确认）。三个受支持宿主
（Codex CLI、CodeBuddy、dsh）的接线文件**没有任何工具调用事件**，只有 `SessionStart`，
于是门从不运行、`released` 从不产生、`approve` 永远拒绝，而它给出的补救命令
（`bash hooks/task unaided <stage> --considered '…'`）在同一平台上正是死路——该命令会打印
`unaided OK` 并退出 0，却只写 `evidence`、不写 `released`。`approve` 是 `## Approval` 块的
唯一合宪写者，因此 `in_progress`、`complete`、归档全部不可达，用户只能手写审批块
（`require_approval` 只校验文字）。

本任务做两件事，且两件都必需：(1) **在契约真的匹配的宿主上把门接上**；(2) **让
`approve` 在任何宿主上都不再依赖一个可能根本不存在的产物**。只做 (1) 会把死锁从三个宿主
缩到「任何别的宿主」；只做 (2) 会让无门宿主上每个阶段都被迫声明 `unaided`，即使真调用了
能力——那正是 `TF-20261009-8abbd6` 记的问题，等于把缺陷换了个形状。

## Background / Confirmed Facts

### 实测（2026-10-11，`/tmp` 夹具，本机）

同一夹具跑两遍，唯一差别是门跑不跑：

```text
############ 有门（Claude Code / Trae）############
$ bash hooks/task unaided PRD  --considered "requirements elicitation and framing"
unaided OK: PRD …
$ bash hooks/task unaided Plan --considered "work breakdown and task decomposition"
unaided OK: Plan …
$ <门的调用>                                   # 放行
$ cat .git/taskflow/released
v1|PRD|1|unaided|requirements elicitation and framing
$ bash hooks/task approve …
approve blocked: stage [Plan] was never released by the pre-write gate. …

############ 无门（Codex / CodeBuddy / dsh）############
$ bash hooks/task unaided PRD  --considered "…"        # 同一条命令
unaided OK: PRD …
$ bash hooks/task unaided Plan --considered "…"
unaided OK: Plan …
$ cat .git/taskflow/released
  (released does not exist)                            # ← 关键
$ bash hooks/task approve …
approve blocked: stage [PRD] was never released by the pre-write gate. …
```

同一夹具里另测：手写 `## Approval` 块后 `task state in_progress` **通过**。即这条缺陷
逼用户伪造审批记录——而那正是这套门存在的理由。

### 唯一写入者链

`released` 的写者只有 `hooks/capability-gate:155` 一处（`grep -rn released hooks/` 穷举，
`hooks/task` 只读不写，`hooks/capability-evidence` 只写 `evidence`）。`hooks/task:1052` 读它，
读不到即 `approve blocked`。

### 三个宿主的契约（本次查证）

| 宿主 | 可 deny 的事件 | deny 的输出形状 | 调用输入 | 结论 |
| --- | --- | --- | --- | --- |
| CodeBuddy | `PreToolUse`（matcher 匹配 `tool_name`，`Write`/`Edit` 是真实工具名） | `hookSpecificOutput.permissionDecision: deny` —— **与本站现在输出的逐字节相同** | SDK 文档的 `matcher: 'Write|Edit'` 样本直接读 `input.file_path` | **可原样接线** |
| dsh | `PreToolUse` → `tools/pre-execute`（桥的映射表明列，deny 生效；`allow` 不生效，本站不用） | 同上 | 桥的 `preToolPayload` 透传 `tool_input: exec.arguments` | **可接线，但 `file_path` 字段名须真机确认** |
| Codex CLI | `PreToolUse`（matcher 别名 `Edit`/`Write`） | 同上，逐字节相同 | **实测形状**：`tool_name: "apply_patch"`，`tool_input: {"command": "<patch 文本>"}`，**无 `file_path`** | **原样接线会静默失效** |

Codex 一行的含义：`capability-gate` **只从 `tool_input.file_path` 判定**
（`hooks/capability-gate:73-114`），接上去它会读不到字段、走 `[ -n "$file_path" ] || exit 0`
而**静默放行每一次写入**——看起来接上了、从不管，比不接更坏。这不是推测：
Codex 自己的测试 `pre_tool_use_payload_uses_freeform_patch_input`
（`codex-rs/core/src/tools/handlers/apply_patch_tests.rs`）断言的就是
`tool_input: json!({ "command": patch })`；第三方在 Codex 0.154.0 上实测到同一形状，并记录了
同一个失败模式——「hook 跑了、找不到字段、干净退出，日志里没有任何跳过痕迹」。

要接 Codex，门必须：从 patch 文本里取路径（三条指令 `*** Update File: ` / `*** Add File: ` /
`*** Delete File: `）、**循环**处理一次调用可含多个文件、并把**相对路径**（Codex 规定
「File references can only be relative, NEVER ABSOLUTE」）按事件的 `cwd` 解析。这已经是在
重写门的路径解析层，不是接线。Codex 官方文档还提示部分专用工具路径会绕过默认 hook 路径
（"Treat tool hooks as a useful guardrail, not a complete enforcement boundary"），即接上也不
构成完备边界。

### 文档现在自相矛盾

- `skills/taskflow/references/runtime.md:68`：`A host without a tool-call hook has no gate at all — and nothing else in TaskFlow depends on one.`
- `hooks/README.md:203`：同类表述。
- 两句都与 `approve` 的实际行为相反。要么改行为，要么改句子，不能都留。

### 宿主侧的信任/复核闸门

三个宿主对非纳管 hook 都有一次人工信任步骤（Codex 的 `/hooks` 审查并记录 hook 哈希、
CodeBuddy 的 `/hooks` 面板 + 设置变更不热加载）。这决定了「接上了」不等于「用户那里真的
在跑」，必须写进安装说明。

### 时间线

`hooks/task approve` 的阶段校验与门是**同一个 commit**（`d72c2b2`，2026-09-28）。该任务的
PRD 只在门与 `unaided` 上写了宿主假设（「v1 只接 Claude Code」，
`achieved/2026-09-27-capability-pre-write-gate/prd.md:27,97`），**没有把第三个继承者
`approve` 也算进去**——这是缺陷的根。自 `v1.1.1` 起每个发布版本都带着它。

## Requirements

- **R1** 在 CodeBuddy 接上 `capability-gate` 与 `capability-evidence`（`PreToolUse` 匹配
  `Write|Edit`；`PostToolUse` 匹配该宿主真实存在的能力类工具名）。
- **R2** dsh **不接线**，理由写成「契约不匹配：工具名小写，matcher 永不命中」，而不是留白。
  实测（dsh 0.2.0-rc.2，2026-10-11）：桥以 `tool_name: exec.name` 原样透传、无翻译表，
  文件工具注册为 `write`/`edit`，而 matcher 与两个钩子的 `case` 都大小写敏感。
- **R3** Codex：本任务**不改门去解析 patch**。保持不接，并在文档把理由写成
  「契约不匹配：工具输入不含路径」。
- **R4** `hooks/task unaided` 在写 `evidence` 的同时写 `released`，使它在**任何宿主、有无门**
  都真正放行该阶段。这是死锁的根修：`approve` 不再依赖一个可能永不存在的产物。
- **R5** `approve` 的失败语义与世界一致：它要求的记录必须真的可能被产生。不得存在
  「合法路径下必然失败」的状态。
- **R6** 文档与行为一致：`runtime.md:68`、`hooks/README.md:203`、事件表的门行、安装说明里的
  信任/复核步骤，全部改写为实际情形。
- **R7** 断言钉住：接线文件的形状（每个宿主文件是否含门所需事件）、`unaided` 单独即可令
  `approve` 通过（无门夹具）、以及文档不再含那句反向断言。

## Acceptance Criteria

- **A1** 无门夹具：只跑 `task unaided <stage>`，随后 `task approve` **通过**（当前失败）。
- **A2** 有门夹具不回归：同树放行、逐阶段新鲜度、既有 approve 对账全部不变。
- **A3** CodeBuddy 的接线文件含门所需事件，且由断言钉住形状；dsh 与 Codex 的**不接**同样被断言钉住
  （接回去即变红）。
- **A4** `unaided` 写入的 `released` 行能被 `approve` 正确对账（kind/capability 与
  `## Skills / Tools Used` 的 `Unaided — …; considered:` 一致），且其序号不破坏
  「一次调用一个阶段」的既有语义。
- **A5** Codex 与 dsh 的去向在文档中有明确表述（各自的契约不匹配理由），
  且**不存在**「接线文件声称有门、门却静默放行」的状态。
- **A6** 文档中不再出现「没有别的东西依赖门」一类表述；宿主事件表与安装说明与行为一致。
- **A7** `bash hooks/smoke-test` 全量通过；新增断言在变异下变红（删掉 `unaided` 写 `released`
  一行 → A1 红）。
- **A8** bash 3.2 + BSD userland 下限、无解释器 PATH 一节不回归。

## In Scope

`hooks/hooks-codebuddy.json`、`hooks/hooks-dsh.json`、`hooks/task`（`unaided`）、
`hooks/capability-gate` 与 `hooks/capability-evidence`（仅在真需要时）、`hooks/smoke-test`、
`skills/taskflow/references/runtime.md`、`skills/taskflow/SKILL.md`（若措辞需同步）、
`hooks/README.md`、以及本任务文档。

## Out of Scope

- 把内建工具（Read/Grep/WebSearch/WebFetch）算作能力——`2026-09-27` 已否决（R12：门会随手可满足）。
- 按 `TF-20261009-8abbd6` 为阶段增加「非工具调用的选择记录」通道。
- 在真实 Codex/CodeBuddy/dsh 宿主上跑一次活体会话（见 Risks）。
- 发布本身。

## Risks / Deferred Items

- **契约证据的强度不一，一律标注。** CodeBuddy 的结论来自**打包后的 CLI 本体**
  （解包 `@tencent-ai/codebuddy-code@2.137.0` 读部署产物），不是活体会话；dsh 的两条
  （工具名小写、matcher 大小写敏感）是**真机实测**；Codex 的形状来自其自身测试与第三方实测。
  本任务照 Trae 的先例标注强度，不把文档、也不把静态阅读当活体实测。
- **信任步骤可能让门形同未装。** 宿主跳过来审查的 hook 时是静默的；文档必须写清这一步骤，
  否则「接上了」只是仓库里的事实。
- **`unaided` 写 `released` 会改变它在有门宿主上的语义**：今天它只登记声明、放行仍靠门；
  之后它自己放行。须确认这不削弱「门只认可真实调用」的边界——`unaided` 本来就是显式声明
  而非伪装调用，故不破坏该边界，但要在 Spec 里把序号与对账语义写死。
- **回滚点**：每个 Step 独立成 commit，可单独 revert。

## Open Questions

1. **Codex 是否纳入本任务？** 选项：(a) 纳入，门增加「从 patch 取目标路径」的分支（多文件、
   相对路径解析、且仍受 Codex 自身 guardrail 边界所限）；(b) 不纳入，接线文件保持不接并在
   文档写明契约不匹配的理由（**推荐 (b)**：这是重写门的路径解析层，属独立风险面，且不接
   Codex 也能靠 R4 让该宿主完全可用；也为 (a) 单独留出干净的后续）。
2. **`approve` 在完全没有门、也没有 `unaided` 记录时该怎样？** 选项：(a) R4 足够，保持
   `approve` 不变，失败信息改为指向 `unaided`（推荐）；(b) 增加「该宿主无门」的显式降级。
3. **dsh 怎么办？** 实测已给出答案，此问已收敛：dsh 的工具名是 `write`/`edit`、matcher 大小写
   敏感，**接线文件改不动这件事**——要接就得给两个钩子加小写分支，那是钩子语义的扩张。选项：
   (a) 本任务不接，保持 `SessionStart`-only，并在文档写明（**已采用**）；(b) 本任务内给两个钩子
   加小写形态并在本机真机验证 deny 生效；(c) 另开任务做 (b)。

## Version History

- v1 — 规划中，等待用户批准。
