# Plan — 修复 todo.md 的模板块与残留标题

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Spec Pointers

无。

## Reference Pointers

- `TaskFlowDocs/achieved/2026-09-22-todo-intake-insert/` — `intake` 插入点的既有实现与其验收条件；本次若动插入点必须与它一致。
- `TaskFlowDocs/achieved/2026-09-16-todo-entry-loss-detection/` — `todo-check` 只认 `- ID:` 行，模板里的假 ID 不在保护范围。
- `TaskFlowDocs/achieved/2026-09-22-archive-transaction/` — 曾专门修过「archive 在 `## Item template` 后多插空行」，本次动模板位置必须不破它。

## Related Tasks

- Parent: None
- Children: None
- Depends on: None
- Blocks: None
- Related: `TF-20260919-6b4e21`（todo.md 增长，本次明确不做）

## Skills / Tools Used

- [PRD] `general-purpose` — purpose: 核查 todo.md 的结构损伤面（19 个只有标题的节是否都是真条目、空壳标题的来源、截断句能否从历史还原）；outcome: `succeeded`；incorporated: 截断句确认为自文件首个版本起即存在、无法从历史还原；空壳标题定位到 `790c27a` 的 intake bug。
- [PRD] `general-purpose`（独立复核，同 worktree 只读） — purpose: 复核模板迁移与 `intake` 插入点的相互作用，以及是否有测试按字节或行数比对 todo.md；outcome: `succeeded`；incorporated: 见下，其中第 1 条是本任务最关键的一条。
- [Plan] `general-purpose` — purpose: 复核 Step 1 拆解，重点是「我漏了什么」；outcome: `succeeded`；incorporated: 见下。

### 复核结论如何改入本 Plan（用户 2026-10-18 已就「怎么修」定过的三条不受影响）

1. **模板块不是普通的文档块——它是两个 hook 的邻居，而且今天只是「碰巧」正确。**
   - **没有任何 hook 解析 markdown 围栏**（全 `hooks/` 搜 ``` 只命中文档与夹具数据）。所以围栏里的 `## T-YYYYMMDD-001 — Short title` 对每个 hook 都是一个**真的节边界**。
   - `hooks/task remove`（`:505-517`）从标题往下第一个 `^## ` 就停，于是墓碑会被写进围栏。**已实测复现**：骨架带 `- ID:` 时，`## Removed` 落在 ```markdown 与内层标题之间。
   - `hooks/summarize-state`（`:125`）只按 ID 值白名单跳过占位符；骨架带 `- ID:` 时占位条目会进每次会话的 inbox 列表。**已实测复现**（打出 `- TF-YYYYMMDD-001 | inbox | <one sentence>`）。
   - 两者今天都正确，只因**模板骨架里没有 `- ID:` 行**。所以「字段名对齐 intake」这条要求里，`- ID:` 绝不能进骨架体——它只能出现在围栏外的说明里。这是本任务的第一硬约束。
2. **`intake` 的插入点不受模板所在位置影响。** **已实测**：模板放在 `## Items` 之下时，新条目插在模板**之前**（插入点在 `hooks/task:336-343`，跳过空行与 HTML 注释即停）。所以「模板移到前言」不需要改 `intake`。但它也意味着：`## Items` 之后的第一件事最好就是真条目或非围栏块——把模板**紧贴注释**放在 `## Items` 下是最稳的位置。
3. **改模板会让与其它分支的合并变成硬冲突**（`merge-todo` 把围栏内标题当条目标题）。本任务的两个分支尚未共享，可安全落地；这一点写进 PR 正文即可，不需要额外动作。
4. **删空壳标题是本次最干净的一步**：对六个 hook 全部惰性（无 `- ID:`、无 `- Task:`、不在 `## Removed`），且它消除了 `archive`/`reopen` 的「同标题取最后一个」歧义（真条目在第 441 行，靠顺序侥幸取胜）。删除后歧义消失。
5. **新断言要读真实文件，不要加夹具目录摘要。** 仓库里没有任何断言钉过 todo 模板的字段集；而 `tools/fixture-compare` 是按目录逐文件 `cmp`（无硬编码期望，也不在 CI 里）。断言直接读真实 `TaskFlowDocs/todo.md`：围栏内字段名集合 == `hooks/task:369-381` 写出的集合，且骨架体不含 `- ID:` 行。这是仓库里第一条 fence-aware 的检查。

## Preconditions

- [x] 适用仓库文档与个人规则已检查；`TaskFlowDocs/repository-docs/index.md` 已读，`CONTRIBUTING.md`、`CODE_STYLE.md`、`.github/pull_request_template.md` 已读，无冲突。
- [x] 远端/base 已记录：`origin` = `hkwuks/TaskFlow`，base = `main`（`da2afa1`），本地分支 `fix/todo-template-repair` 从该提交切出，worktree `.worktrees/todo-template-repair`。
- [x] PR 模板路径与必填字段映射已读（`.github/pull_request_template.md`）。
- [x] 本任务不需要新建治理文档。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-18 21:47 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 修四处损伤并钉住模板与 intake 的字段一致

- Goal: 模板回到前言、字段对齐真实写入、清掉截断半句与空壳标题，并用一条断言让模板字段集与 `intake` 字段集绑死。
- Dependencies: 无（但改插入逻辑前先读 `hooks/task` 的 `intake` 分支）。
- Files:
  - `TaskFlowDocs/todo.md`（前言、模板块、第 1243 行空壳标题）
  - `hooks/smoke-test`（新增断言）
  - `hooks/task`（**未改**：插入点已实测不受模板位置影响）
- Implementation checklist:
  - [x] 把模板移到前言区（`## Status flow` 之上、`# Todo inbox` 之后）。
  - [x] 模板字段列表对齐 `intake` 实际写出的集合：`ID / Status / Priority / Owner / Source / Added / Updated / Goal / Task / Next action`；不再列 `- External:`。
  - [x] **示例全行缩进 4 空格**——这一条同时取代了原计划的「不得含 `- ID:` 行」：缩进后源码里根本不出现列 0 的 `## ` 或 `- `，示例不再是任何 hook 的节边界，也不需要靠「不含 ID」来避险。`- External:` 的旁注写在缩进块**之外**。
  - [x] 模板标题行改为 `## <goal, cut to 80 bytes>`，不再出现 `T-YYYYMMDD-001` 这种形态。
  - [x] 截断半句替换为完整句，语意取自 `TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/prd.md:45` 的既有说法。
  - [x] 删除第 1243 行的空壳标题；第 454 行的 `TF-20260914-03` 未受影响。
  - [x] `hooks/smoke-test` 新增一节 `== the Todo template lists the fields intake actually writes ==`，读**真实** `TaskFlowDocs/todo.md` 与 `hooks/task` 两边的字段名集合，双向比对（缺一个点名一个、多一个点名一个），并单独断言示例区没有列 0 的字段行。
- Acceptance: 见 PRD 的 Acceptance Criteria。
- Verification: 见 `## Verification / Review`。
- Rollback: `git revert` 本任务提交；todo.md 是纯文本记录，无迁移。
- Status: done

## Checkpoints

- [x] 动 `todo.md` 之后跑 `hooks/todo-check .`，确认没有任何条目的 ID 集合变化。
- [x] 迁移后在文件副本上真跑一次 `hooks/task intake`，确认新条目落在 `## Items` 之下、模板之上。

## Verification / Review

- 2026-10-18 Step 1: smoke 73 ok / ALL SMOKE PASSED; todo-check pass; three mutations red

### 通过项

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| **CI（权威）** | `Hooks` workflow，run [39136903763](https://github.com/hkwuks/TaskFlow/actions/runs/39136903763) @ `1ead9f4` | `success`，六个作业全绿（`evals`、`release`、`smoke` × ubuntu/macos/windows、`todo-merge-audit`） |
| smoke 全套（本地） | `bash hooks/smoke-test < /dev/null` | `ALL SMOKE PASSED`，73 个 `ok`（基线 72 + 新增 1 节），exit 0 |
| 条目丢失审计 | `bash hooks/todo-check .` | `STATUS: pass` |
| 仓库检查 | `bash hooks/repository-check .` | `Orphan task directories: none` |
| 空白/尾随 | `git diff --check` | clean |
| shell 解析 | `bash -n hooks/smoke-test` | OK |
| bash 3.2 解析 | `docker run --rm -i bash:3.2 bash -n < hooks/smoke-test` | `3.2 OK` |

本地跑 smoke 的用途按 `CONTRIBUTING.md` 的 Checks 一节核对过：本次改动落在 CI 覆盖的面上，所以 CI 是权威判据；本地那一轮是为了在推送前拿到变异验证的红/绿，不是替代 CI。

### 四条损伤的处置

| 损伤 | 处置 | 证据 |
| --- | --- | --- |
| 模板夹在条目中间 | 移到 `# Todo inbox` 之后的顶部 | `grep -n '^## '` 首项现为 `## Item template`（第 7 行），其下紧接 `## Status flow`、`## Items` |
| 第 695 行截断半句 | 换成完整句（有仓库先例） | 全文件已无 `Every direct request or imported requireme` 半句 |
| 模板字段与 `intake` 脱节 | 字段表按 `hooks/task:372-381` 重写，并加断言绑死 | 新增断言双向比对通过 |
| 第 1243 行空壳标题 | 删除 | `grep -c '^## State in the Skill that personal supplements are local-only$'` 现为 1（只剩第 454 行的真条目） |

### 方案调整（为什么从「围栏代码块」改成「缩进示例」）

原计划把示例留在 ```markdown 围栏里，只靠「骨架体不含 `- ID:` 行」避险。实测否掉了这个方案：**没有任何 hook 解析 markdown 围栏**，所以围栏内的 `## T-YYYYMMDD-001 — Short title` 对每个 hook 都是一个**真的节边界**。三条后果都在**真实修复后的文件**上复现过：

| 场景 | 实测结果 |
| --- | --- |
| 围栏版 + 示例含 `- ID:` → `hooks/task remove` | 墓碑 `## Removed` 被写进围栏里（落在 ```markdown 与内层标题之间），并把示例体劈成两半 |
| 围栏版 + 示例含 `- ID:` → `hooks/summarize-state` | 占位条目进 SessionStart 的 inbox 列表：`- TF-YYYYMMDD-001 \| inbox \| <one sentence>` |
| 围栏版 → `hooks/merge-todo` | 示例内标题被当作条目标题参与合并，改它会让与其它分支的合并变成硬冲突 |

改成**缩进示例**后，源码里不再出现列 0 的 `## ` 或 `- `，示例退出所有 hook 的视野，三条风险一次消失。已在真实修复后的文件上逐一复验：

- `hooks/task remove`（走**插入** `## Removed` 的路径）→ 墓碑落在第一个真条目之上（第 35 行），未触及模板；
- `hooks/summarize-state` → inbox 列表不含任何占位条目；
- `hooks/task intake`（在副本上真跑）→ 新条目插在 `## Items` 之下、模板之上；
- `hooks/todo-check .` → pass。

### 变异验证（树副本，真 worktree 未被改动）

| 变异 | 变红的断言 |
| --- | --- |
| 从示例里删掉 `- Priority:` | `FAIL the Todo template is out of step with intake:` / `template lacks: Priority` |
| 往示例里加一行 `- External:` | `FAIL the Todo template lists fields intake does not write:` / `template invents: External` |
| 把示例里的 `- ID:` 行退回列 0 | 字段集断言先红（缩进守卫在无 `- ` 前缀可匹配时同样失效） |

第一条守卫（缩进检查）单独做过单元验证：往一份带列 0 字段的样本上跑，它正确地报出；在真实文件上通过。（初版守卫写成 `exit 1` 在规则里、`END{exit 0}` 在外，会被 `END` 覆盖——已改成把状态存进标志位再由 `END` 退出。）

### 未执行 / 局限

- 未跑 `hooks/smoke-test-windows.ps1`（非 Windows 主机）。该套件对模板没有任何断言。
- 未跑评测套件（`evals/runner.py`）。它用的是自己的 8 行夹具，`evals/cases/taskflow.json:45` 只要求真实文件里存在 `Status flow` 字符串——该字符串保留在前言中。
- **`hooks/merge-todo` 的前言归属未改**：driver 取「我们这一侧」的前言，另一侧的前言编辑静默丢弃。模板移入前言后受影响面积变大。这是既有行为，列入 Follow-ups，本次不动。

## Change Log

- 2026-10-18 v1 planning：立项。范围按用户 2026-10-18 的三选一取「修损坏 + 防脱节断言」，增长那一半仍按 2026-09-19 的既有决定排除。
- 2026-10-18 v1 work revision：并入复核结论——**第一硬约束：骨架体不得含 `- ID:` 行**（否则 `remove` 把墓碑写进围栏、`summarize-state` 把占位条目打进 inbox 列表，两者均已实测复现）；`intake` 插入点经实测不受模板位置影响；断言改读真实 `todo.md`；19 个标题式条目已核为真条目。
- 2026-10-18 v1 work revision：按复核把方案从「围栏代码块」改为**缩进示例**——源码里不出现列 0 的 `## `，示例因此不再是任何 hook 的节边界，`remove`/`summarize-state`/`merge-todo` 三条风险一次性消失（每条都在真实修复后的文件上实测过）。同时补进：截断句在 `2026-09-07-repository-docs-workspace/prd.md:45` 有仓库先例、`merge-todo` 前言归属的静默丢弃、`SKILL.md:58/:148` 的 `External` 陈词。

## Follow-ups

- `TF-20260919-6b4e21`：`done` 条目占约 72%（约 82 KB / 82 条）的增长问题，用户研究后再定，本次不动。
- `skills/taskflow/SKILL.md:58` 与 `:148` 仍把 `external identifier/link` 列为 Todo 字段，而没有任何 hook 读 `External`、`intake` 也不写它。本次只对齐模板，这两句的改写留作后续（否则会把「模板对齐」扩成「规则改写」）。
- `hooks/merge-todo:14` 的「前言取我们这一侧」使另一侧的前言编辑被静默丢弃；模板移入前言后受影响面积变大。driver 的修法未定，本次不动。

## Version History

- v1 — planning：修四处结构损伤 + 一条防脱节断言；增长那一半按既有决定排除。
