# The entry signal for unregistered work never fires in the state a session actual

> Task version: v1
> Status: checking

## Goal

让「这类请求要先登记进 TaskFlow」这句话，在一个会话最常打开的位置——已经用过 TaskFlow 的仓库的基检出——真的被说出来。

用户价值是一句话：**一个改仓库的请求不再能在没有任何提示的情况下整条绕过 TaskFlow**。今天的代价是可复现的：本次会话（2026-10-12）就是一个「修改仓库」的请求，从第一秒起就该进 TaskFlow，结果跳过的是 Todo 记录、任务隔离和 PRD/Plan 三份文档，而整个会话期间没有任何一行输出提示过这件事。

## Background / Confirmed Facts

### B1·复现（本次实测，1.1.5，fixture 已删）

同一个仓库、同一个 commit、同一份 `todo.md`，只换分支：

```
A) 基检出（main）:
   # TaskFlow inbox (not done)
   # Active tasks
                                       ← 到此为止，一个字都没提义务

B) 同一 commit，换到 fix/something:
   # TaskFlow inbox (not done)
   # Active tasks
   # No task for branch 'fix/something'
   - Work on this branch is not registered: no TaskFlowDocs/<task>/ matches it. ...
```

A 是缺陷形态。B 反而说了话，而 B 是已经建过分支的人——他们大概率已经知道这条规则。

### B2·机制：义务句的投放条件与它的适用条件正好相反

`hooks/summarize-state` 现有四段输出，各由一个条件把守：

| 行 | 守卫 | 说什么 | 在一个**用过** TaskFlow 的仓库里 |
| --- | --- | --- | --- |
| 27 | `[ ! -d "$docs" ]` | 义务句（「Applicable work enters TaskFlow: …」） | **永不成立** |
| 54 | `[ ! -f "$todo" ]` 且目录内无其它条目 | 「TaskFlow (nothing recorded yet)」 | **永不成立** |
| 84-96 | 分支 ≠ `main`/`master` 且 slug 不匹配任何任务 | 「No task for branch …」 | 只在非基分支成立 |

第 27 行那段文字本身完全正确，但它的两个前提——「整个 `TaskFlowDocs/` 不存在」——在任何真用过的仓库里都不成立：`TaskFlowDocs/repository-docs/` 由路由钩子**自己创建**（`repository-docs-context`），`todo.md` 是**跟踪文件**。所以只要这个仓库用过 TaskFlow 一次，这段就是**死代码**。

第 54 行那段的意图正是补这个洞，但它只覆盖「目录在、条目一条都没有」这一种形态，而且它同样在 `todo.md` 存在时失效——而 `todo.md` 存在正是「用过」的定义。

### B3·既有断言锁着当前行为

| 位置 | 锁着什么 | 影响 |
| --- | --- | --- |
| `smoke-test:77` | `todo.md` 一存在，入口行就**不许**出现 | 新行为要印，此断言必改 |
| `smoke-test:123` | `branch_says master silent` | 基分支上现在要印义务句，此断言必改 |

`smoke-test:71` 断言「nothing recorded yet」这句话的字面量，`smoke-test:58` 断言「Applicable work enters TaskFlow」这句义务句。**两句话的字面量都要保留**，否则现有断言被无故打破。

### B4·改动必须落在既有的地板内

`A5`（见 Acceptance）：POSIX sh + `awk`/`sed`、bash 3.2、**不引入任何解释器**。`smoke-test` 有一节 `hooks run with no interpreter available` 在守这条线，改动后必须仍然通过。

### B5·本条在母条目里的位置

`TF-20261009-cc463b`（done）记录了五个失败模式；其第四、第五个即本条的来源，第五个明写「本条不修（需要与 `TF-20261001-efbc51` 的锚点语义一起定），在此记录」。`efbc51` 已 done（`achieved/2026-10-11-evidence-anchor/`），它解决的是「干活的落点不是以为的落点」的 hook 侧与文档侧，与本条不冲突、也不覆盖本条：**efbc51 管的是工作已经在一个错误的落点开始之后怎么搬，本条管的是工作根本不该在没有提示的情况下开始走。**

## Requirements

### R1 — 用一个判据决定要不要说义务句：有没有活跃任务

义务句由 **active 任务列表为空** 触发，不再由「目录是否存在」触发。三个形态合并到这一个判据上：

- 无 `TaskFlowDocs/`（今天的第一段）→ active 空 → 说；
- 有目录、无 `todo.md` 且无其它条目（今天的第二段）→ active 空 → 说；
- 有 `todo.md` 但**没有任何活跃任务** → active 空 → 说（**这是今天不说、也是本条要修的那一种**）。

三种形态的文案可以不同，但触发条件必须只有一个。

### R2 — 有活跃任务时一字不说

在办的会话不需要被念义务句。一个会话只要有一个活跃任务，义务句不出现。

### R3 — 分支报告与义务句解耦

`main`/`master` 上可以印义务句，但**不印**分支报告（「No task for branch …」）。两者判据不同，不得合并。

### R4 — 基检出不因「在基分支上」而沉默

用户 2026-10-12 的裁定，也是本条的核心：**基检出恰是最需要这句义务的地方**，今天的注释把它按字面名排除，理由是「基分支上说的每句都是噪声」——这个理由对**分支报告**成立，对**义务句**不成立。

### R5 — 义务句仍是惰性的

说这句话**不得**创建任何东西：不建目录、不建 Todo、不建任务。`smoke-test:59` 已经在守「no-docs 消息不得创建 `TaskFlowDocs`」，改动后对全部形态都成立。

### R6 — 不并入 base 分支解析

用户 2026-10-12 裁定：**不做**。`main`/`master` 字面排除改成解析远程默认分支是**另一个触发面**（在默认分支不叫 `main`/`master` 的仓库里会在基检出上误报），修法要引入 `symbolic-ref` 及其无远程时的失败分支，与本条不是同一个决定。留给单独的条目。

## Acceptance Criteria

- **A1**：在一个**有活跃任务**的仓库的基检出上，义务句不出现，分支报告不出现。
- **A2**：在一个**有 `todo.md`、没有活跃任务**的仓库的基检出上，义务句出现（含 `Applicable work enters TaskFlow` 与 `TaskFlowDocs/todo.md` 两个字面量）。
- **A3**：在同一个仓库、同一个 commit 上，切到 `fix/never-registered` 后，**义务句与分支报告都在**；在 `main` 上，**只有义务句**（`No task for branch` 不出现）。
- **A4**：无 `TaskFlowDocs/` 的仓库、以及有目录但一条都没记过的仓库，输出仍含义务句与 `TaskFlowDocs/todo.md`，且**不创建任何文件**（R5）。
- **A5**：改动后 `bash hooks/smoke-test` 全量通过，含 `no interpreter available` 一节；`bash -n` 通过；`docker run bash:3.2` 解析通过。
- **A6**：状态短句不因缺少目录而谎报。有扩展任务时不得说「nothing recorded yet」；目录内无任何条目时才说。

## In Scope

- `hooks/summarize-state`——义务句的触发判据、三形态合并、与分支报告解耦。
- `hooks/smoke-test`——改两条锁旧行为的断言（`smoke-test:77`、`smoke-test:123`），新增 R1/R2/R3 的正反两向断言。
- 本任务 `TaskFlowDocs/2026-10-17-summarize-state-entry-signal/`。
- `TaskFlowDocs/todo.md`——本条的状态推进。

## Out of Scope

- **base 分支解析**（R6）。用户已裁定另记，本条不碰 `main`/`master` 的判据本身。
- **`summarize-state` 的 120 字节 goal 截断**。它在 `TaskFlowDocs/todo.md` 无界增长那一类里，是「幽灵需求」的上游；不在本条的验收面上。
- **`SKILL.md` / `README` 的措辞**。本条的产物是一行 hook 输出，不是规则文本。
- **achieved 归档任务是否算「已登记」**。本条只读活跃任务，不改变归档语义（见 D2）。

## Risks / Deferred Items

- **D1·噪声风险（真实）**：基检出现在会多出 2 行。押注是「少印 = 静默 = 更贵的失败」，与仓库自己的话一致（`capability-gate:66-68`：「A gate that silently stops gating is worse than no gate, because nothing reports that it stopped.」）。若实测被当噪声忽略，回退点是把触发条件从「无活跃任务」收紧为「无活跃任务 **且** Todo 里存在 inbox 条目」——留作 follow-up，不在本条。
- **D2·陈旧工作树的形态**：一个任务已归档、工作树还在的陈旧工作树（本仓库现存 7 个）多出**一行**义务句——其 `active` 为空，而分支 slug 仍匹配 `achieved/` 下的任务目录，所以分支报告**不**出现，只有义务句。这是**有意**的：那个工作树里确实没有任何在办任务。R3 只解耦两者，不改变分支报告的判据（`achieved/` 仍算「已登记」），所以本条比初稿预估的更安静。
- **D3·仓库根没有活跃任务的使用者**（例如只在基检出上做 release 的人）：基检出会长驻这 2 行。当前判据无法区分「正在做 release」与「正在做未登记的工作」，两者在 hook 眼里都是「基检出 + 无活跃任务」。接受，并记录。

## Open Questions

无阻塞项。用户 2026-10-12 已裁定三个决定：按 small task 走完整流程（不是直接改）、触发条件为「没有任何活跃任务时印」、base 分支解析不做并另记。

## Version History

- v1 — planning。由 `TF-20261012-50164f` promote 创建；三个设计决定由用户 2026-10-12 裁定并记入 R1/R6 与本文件。
