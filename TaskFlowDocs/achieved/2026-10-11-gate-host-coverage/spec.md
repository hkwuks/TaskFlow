# Spec — 前置能力门的宿主覆盖与 approve 的解耦

> Task version: v1

## Objective and Success Criteria

在**不改变门自身放行语义**的前提下，让 `task approve` 在任何受支持宿主上都有可达路径：
`unaided` 成为它自己声明的那个阶段的**放行者**（写 `released`，而不只是写 `evidence`），
并在契约匹配的宿主上把门真正接起来。

成功判据：A1（无门夹具下 `unaided` 后 `approve` 通过）、A2（有门路径零回归）、
A3（接线形状被钉住）、A5（不存在「声称有门却静默放行」的宿主）。

## Architecture Boundaries and Responsibilities

- `hooks/capability-gate`：**放行判定与证据消费逻辑不变**。本 Spec 不改它的 deny/allow 决策，
  也不改它对 `evidence` 的消费方式，也不为任何宿主新增大小写分支。
- `hooks/task unaided`：**职责扩展**——从「登记声明」变为「登记声明并放行该阶段」。这是死锁
  的根修：`approve` 依赖的产物必须由一条在所有宿主上都能成功的命令产生。
- `hooks/capability-evidence`：不变（仍只写 `evidence`，仍按事件 `cwd` 定位）。
- 宿主接线文件：`hooks-codebuddy.json` 增加两个事件；`hooks-dsh.json` **不加**（见下方接线契约）。
- 文档：`runtime.md`、`hooks/README.md` 与行为对齐。

## Project Structure / Affected Files

| 文件 | 改动 |
| --- | --- |
| `hooks/task` | `unaided` 分支：补写 `released`（含幂等） |
| `hooks/hooks-codebuddy.json` | 增加 `PreToolUse`（`Write|Edit`）与 `PostToolUse`（`Skill|Agent|Task`、`mcp__.*`） |
| `hooks/hooks-dsh.json` | **不改**——工具名小写使 matcher 永不命中，接线等于静默放行 |
| `hooks/hooks-codex.json` | 保持不接，理由写进文档（工具输入不含路径） |
| `hooks/smoke-test` | 新增「无门夹具 approve 通过」一节 + 接线形状断言 + CodeBuddy 实跑节 |
| `skills/taskflow/references/runtime.md` | 事件表门行、反向断言、Codex/dsh/CodeBuddy 三节 |
| `hooks/README.md`、`README.md`、`README.zh-CN.md` | 宿主能力描述、安装信任步骤、反向断言 |

## Interfaces, Data Flow, and Contracts

### 存储行格式（不变）

```text
evidence:  <kind>|<capability>                                  kind ∈ {invoke, unaided}
released:  <version>|<stage>|<seq>|<kind>|<capability>          seq 为全局序号
```

`consumed = max(第 3 列)`；门放行条件为 `evidence 行数 > consumed`，放行时取第 `consumed+1` 行
并写 `released`，`seq = consumed+1`。

### `unaided` 的新契约

```text
task unaided <STAGE> --considered "<concept class>"：
  1. 校验 stage ∈ {PRD,Spec,Plan}、--considered 非空、概念类落在词表内   （不变）
  2. 定位唯一活跃任务目录；读该任务 plan.md 的 > Task version            （新增：读 version）
  3. git_dir = git -C <root> rev-parse --absolute-git-dir               （不变）
  4. 幂等：released 中若已有 <version>|<STAGE> 行，跳过第 5、6 步并照常报告成功
  5. 追加 evidence:  unaided|<class>                                     （不变）
  6. 追加 released:  <version>|<STAGE>|<consumed+1>|unaided|<class>      （新增）
  7. 打印 unaided OK: <STAGE> in <task> -> <class>                       （不变）
```

**为什么第 5 步必须保留**：门用 `evidence 行数 > consumed` 判定，`consumed` 取自 `released`。
若只写 `released` 不写 `evidence`，就会造出 `consumed > evidence 行数` 的状态，此后**任何**
阶段都永久 deny。两行必须成对写入，序号才自洽。

**为什么这是根修而不是绕过**：`unaided` 记录的是「本阶段有意不调用能力」这一**显式声明**，
从来不是伪装成调用（`hooks/task:996-1008` 的注释与 `runtime.md:200` 都这么定义它）。让声明
自己放行，不削弱门的边界——门仍然拒绝一切没有记录支持的写入。它消除的只是「声明的效果取决于
某个 hook 有没有被装」。

**在有门宿主上的行为变化**：今天 `unaided` 后仍需门在写入时消费记录才放行；之后声明即放行。
用户可见结果相同（阶段被放行、文档可写）；差别是声明后即使不写文档也留下一条 release 记录，
这与 `approve` 需要的那条记录是同一件事，语义上更自洽。此变化必须在文档写明。

### 宿主接线契约

| 宿主 | 事件 | matcher | 判定依据 | 结论 |
| --- | --- | --- | --- | --- |
| CodeBuddy | `PreToolUse` | `Write|Edit` | `tool_input.file_path`；`PermissionUtils` 对 `Write`/`Edit` 读 `file_path` | **接线** |
| CodeBuddy | `PostToolUse` | `Skill|Agent|Task`、`mcp__.*` | `ToolNames.SKILL` 等 PascalCase 枚举 | **接线** |
| dsh | `PreToolUse` | —— | 工具名是 `write`/`edit`，matcher 大小写敏感，永不命中 | **不接线** |
| Codex | `PreToolUse` | —— | `tool_input.command` 是 patch 文本，无路径 | **不接线** |

**接线的一票否决条件**：若某宿主的工具输入不携带门能解析的目标路径，**或**其工具名不落在
两个脚本已有的 `case` 分支上，则该宿主**不得**接线。接上一个永远读不到路径、或永远不被 matcher
命中的门，都会静默放行每一次写入——比不接更坏，因为仓库与文档都会声称门在场。Codex 属于前者，
dsh 属于后者。

dsh 要接线，需要的是**给两个钩子加小写分支**（`write|edit`、`skill`），而不是改接线文件；
那是钩子语义的扩张，本任务不做。在 dsh 上放行阶段用 `hooks/task unaided`（R4）。

## Invariants and Compatibility

- **I1**　门的放行判定（`evidence 行数 > consumed`）与证据消费顺序**完全不变**。
- **I2**　`released` 行格式与 `approve` 的对账方式**完全不变**：`approve` 一行不改。
- **I3**　`released` 的写者从「只有门」变为「门与 `unaided`」，但两者写同一格式、同一序号规则。
- **I4**　`unaided` 的既有失败语义不变（非法 stage / 缺 `--considered` / 概念类不合词表 → 退出 2，
  零写入）。新增的读 version 失败必须**在第一次写之前**失败（活任务目录无 `> Task version` →
  拒绝并说明）。
- **I5**　仍只用 `git`、`awk`、`sed`、`tr`、`printf` 等既有白名单命令；不引入解释器。
- **I6**　bash 3.2 + BSD userland：不新增 `declare -A`、`mapfile`、GNU-only `sed -i`；
  `$( )` 内 heredoc 不含撇号；不用 `cmd && { …; }`。

## Validation and Error Semantics

- 无门夹具（不跑任何 hook）：`unaided PRD` + `unaided Plan` → `approve` **通过**（A1）。
- 有门夹具：既有 `cg_verdict` 系列断言逐条不变；逐阶段新鲜度不变（A2）。
- 幂等：连跑两次 `unaided PRD`，`released` 中该 `<version>|<STAGE>` 仍只有一条。
- 变异：删掉 `unaided` 写 `released` 的那一行 → A1 变红且报错信息指名该断言。

## Code and Test Constraints

- 新断言节自建夹具、末尾清理、git 操作带 `-c user.email/-c user.name`，不依赖前一节的 `$tmp`。
- 接线形状断言读各宿主 JSON 文件做 `grep -q -F`，**不做 JSON 解析**（本仓库无解释器依赖，
  且既有 Trae 断言就是这个形状）。
- `hooks/smoke-test-windows.ps1` 若含宿主接线断言，同步更新。

## Design Decisions and Alternatives

| 决定 | 选择 | 备选与否决理由 |
| --- | --- | --- |
| 死锁的修法 | `unaided` 自己放行 | 让 `approve` 在无门宿主下降级：会新增一个「宿主类型」判定，而这条状态正是缺陷源头；让门在无工具调用时也放行：等于取消门 |
| Codex | 依 OQ1 定 | 原样接线会静默放行（已实测形状），必须显式决策而非默认 |
| 无门宿主的接线 | 只接契约匹配的两个 | 三宿主文档齐备但输入形状不同；「能 deny」不等于「能判定」 |

## Open Questions

（与 PRD 的 Open Questions 同，见该节。）
