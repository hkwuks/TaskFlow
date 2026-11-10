# Spec — 缺陷调查必须先被点名，才能被选择

> Task version: v1

## Objective and Success Criteria

给 TaskFlow 补上一个它作为「能力选择层」缺失的结构：**请求的种类**。现在它只知道任务大小（`small|large`），不知道任务是修错误还是做新东西，于是 `bug fix` 与 `feature` 走同一条路，而那条路的每个阶段都没有「调查」这个类别可点。

成功的判据是 PRD 的十条验收标准（A1–A10），核心是 A5/A6/A7 三条：缺陷类任务的 PRD 阶段要么点名调查类能力，要么显式记录「确认无可用调查能力」；非缺陷类不受此约束。

## Architecture Boundaries and Responsibilities

TaskFlow 的层职责在 `SKILL.md:163` 已经写明：**任务生命周期层，不是专家能力层**。这个边界决定了本次能做什么、不能做什么，并且是判断每一处改动是否落对层的依据。

| 层 | 负责 | **明确不负责** |
| --- | --- | --- |
| 能力层（`systematic-debugging`、`brainstorming` 等 Skill/MCP/Agent） | 怎么调查、怎么发散、怎么找根因；每一步的具体方法 | 何时该被调用、调用记录落在哪个任务与版本 |
| **TaskFlow 生命周期层**（`hooks/task`、`SKILL.md`、`artifacts.md`） | **这次改动的层**：请求分类、阶段→概念类别的映射、能力的点名与留痕、阶段对账 | **不实现任何调查方法**；不规定必须先重现、不要求 red-green、不写怎么找根因 |
| 仓库自身规则层（`CONTRIBUTING.md`、`CODE_STYLE.md`） | 本仓库的开发约定 | 插件行为 |

**这一列「不负责」是本次改动最容易越界的地方。** 越界的具体形状是：把 superpowers 的 `systematic-debugging` 阶段（重现、追溯数据流、单假说、red-green）写进 `SKILL.md`。那会让 TaskFlow 变成一个二流复刻，并且与 `SKILL.md:163` 的层声明直接矛盾。本 Spec 的 R1–R5 全部只涉及「点名 / 记录 / 校验」，没有一条涉及调查方法本身。

## Project Structure / Affected Files

| 文件 | 改动 |
| --- | --- |
| `hooks/task` | `intake`/`promote` 解析 `--kind`；Todo 条目写入 `- Kind:`；`promote` 的 PRD 骨架加 `## Task Kind`；`concept_class_re` 加调查类；`approve` 加缺陷类分支 |
| `skills/taskflow/SKILL.md` | Phase 1 概念类别表补调查类；Phase 1 分流说明 |
| `skills/taskflow/references/artifacts.md` | PRD 轮廓加 `## Task Kind`；说明它为什么是必填而非可选 |
| `hooks/smoke-test` | 新增断言 A1–A9；14 处既有 `promote` 调用补 `--kind` |
| `TaskFlowDocs/todo.md` | 本任务条目（`- Kind: defect`） |

## Interfaces, Data Flow, and Contracts

### 1. 命令接口

```
task intake <goal> [source] [--kind defect|capability|internal] [--root <path>]
task promote <todo-id> <task-id> <small|large> --kind defect|capability|internal [--root <path>]
```

**不对称是有意的。** `intake` 的 `--kind` 可省略（默认 `capability`）：inbox 条目的定位是「便宜地记下来」，此时还不知道要不要做，强制分类只会让人随便填一个。`promote` 的 `--kind` **必填**：这是任务真正开始的地方，也是唯一能让 A5–A7 生效的时刻，此时不给就没有第二次机会。

`--root` 仍是最后一个选项，沿用 `split_root` 的既有契约（`hooks/task:770`）。

### 2. 数据形状

Todo 条目新增一行，位置在 `- Source:` 之后、`- Added:` 之前：

```
- Kind: defect
```

`prd.md` 新增一节，位置在 `## Goal` 之后、`## Background / Confirmed Facts` 之前：

```
## Task Kind

- Kind: defect
```

**为什么两处都写。** Todo 给 triage 看（`task get` 一行可见），PRD 给审批看（`approve` 只读 PRD，不读 Todo）。两者由同一个命令在同一次 `promote` 中写入，不会分叉。

### 3. `approve` 的缺陷类分支

插在既有 stage 对账之后、`approved_version=` 之前，与 `## External Facts` 和 `## Plan Review` 的检查同层。

```
kind = prd 中 ## Task Kind 的 - Kind: 值
若 kind == defect:
    取 ## Skills / Tools Used 中 [PRD] 开头的行
    若该行以 Unaided 开头:
        considered 必须含调查类词根（root cause|defect investigation）
        否则拒绝，信息说明缺陷类任务必须点名调查类能力，或声明 "root cause investigation"
    否则（invoke 行）:
        能力名必须含调查类词根，否则拒绝
若 kind 缺失或非 defect: 不施加任何额外约束
```

**`kind` 缺失时不推断、不拒绝。** R5 要求既有任务继续工作；一个没有 `## Task Kind` 节的 PRD 说明它是本次改动之前创建的，此时拒绝等于改坏历史。

### 4. 词汇

`hooks/task:767` 的正则末尾追加两项：

```
|root cause|defect investigation
```

追加而非重写：既有八个类别一个字都不动，避免让已归档任务的 `--considered` 记录与新正则不一致。

## Invariants and Compatibility

**不变式 1 — 阶段集合不变。** 仍是 `{PRD, Spec, Plan, Test}`。调查折进 PRD（用户已定），因此 `capability-gate`、`approve` 的 `rel_max_seq` 对账、`hooks/task recover` 全部不动。

**不变式 2 — 不新增存储。** 复用 `taskflow/evidence` 与 `taskflow/released`。本次不写新的 store 键，也不改 release 行的六字段形状。

**不变式 3 — 既有 Todo 条目字段集合不变。** `- Kind:` 是新增字段；`hooks/task get` 对没有该字段的条目返回的键集合与今天一致（A9）。`hooks/archive` 的关闭白名单（`hooks/archive:307`）不含 `- Kind:`，所以已关闭条目会失去该字段——这是期望行为，closure 之后 triage 不再需要它。

**不变式 4 — 既有 14 处 smoke `promote` 调用。** 全部需要补 `--kind`，否则冒烟立即变红。补 `capability` 而非 `defect`：这些夹具都是新增能力，且改成产物之外的取值会掩盖 A1 的缺省拒绝。

## Validation and Error Semantics

沿用 `hooks/task` 既有两种退出语义，不新增第三种：

| 情形 | 退出 | 信息 |
| --- | --- | --- |
| `promote` 缺 `--kind` | 1（`fail`） | 点名 `defect\|capability\|internal` 三个取值，并给出 `usage:` 行 |
| `--kind` 非法值 | 1（`fail`） | 点名该非法值 |
| `intake` `--kind` 非法值 | 1（`fail`） | 同上 |
| 缺陷类 PRD 未点名调查类 | 1（`fail`） | 说明两条出路：点名调查类能力，或 `unaided --considered 'root cause investigation'` |
| 合理 | 0 | 既有输出不变 |

全部拒绝发生在写入之前，与 `approve` 既有行为一致（`fail` 在 `approved_version=` 之前）。

## Code and Test Constraints

- **POSIX awk/sed + bash 3.2**，不引入 Python；BSD 上无 `\+`，正则一律用 `-E` 或 awk。
- 读文档一次一个 `awk`，不用管道（`pipefail` 下 `printf | grep -q` 会因 SIGPIPE 误判）。
- 新增 smoke 断言必须可被变异打红；每条变异单独验证后立即还原。
- 不新增脚手架字段却不加断言——`## Task Kind` 既进骨架就必须有 A4 覆盖。

## Design Decisions and Alternatives

**决定 1：`kind` 是命令参数，不是从散文推断。** 备选是让 `approve` 按 `## Background` 里是否提到「缺陷」来推断。否决理由：散文推断会误判，而且判错时无人可追责；显式参数至少把决定记在一个确定的位置上。

**决定 2：调查折进 PRD，不新增 stage。** 备选是新增 `Diagnose` 阶段。否决理由：阶段集合被 `capability-gate`、`approve` 对账、`recover`、smoke 四处消费，新增一个阶段的成本远高于它带来的区分度；而用户已明确选择折进 PRD。

**决定 3：门只查「点名了没有」，不查「查得对不对」。** 这是本次改动最大的诚实边界，必须写进 `artifacts.md`。一个含 `investigat` 但实际无关的能力名能过门。接受它，因为替代方案是把方法写进 TaskFlow——那正是本 Spec 明确不做的事。

**决定 4：`intake` 默认 `capability`，`promote` 必填。** 默认值只出现在还不需要精确的时刻。

## Open Questions

无阻塞项。R4 与 `TF-20261024-b48e56` 的关系已声明：本次只做最小接线，不实现 b48e56 的回退语义。
