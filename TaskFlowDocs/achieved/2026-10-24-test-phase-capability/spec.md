# Spec — Test 阶段的能力选择载体

> Task version: v1
> Status: planning

## Objective and Success Criteria

给 Phase 6「写测试」一个与 PRD / Spec / Plan 同构的能力选择载体，同时不伪造一道门：测试没有单一定义文档，所以由声明命令代行门对证据队列的那次消费，`kind` 由队列状态决定而不是由声明者指定。

成功标准见 `prd.md` 的 A1–A8。本 Spec 只定义机械契约。

## Architecture Boundaries and Responsibilities

三处代码、两种记录、一条不变式。

| 位置 | 职责 | 不改的部分 |
| --- | --- | --- |
| `hooks/capability-evidence` | 记录真实调用，不知道阶段 | 完全不动 |
| `hooks/capability-gate` | 在文档首次正文写入时消费 evidence，写 `released` | 完全不动 |
| `hooks/task unaided` | 声明一个阶段的能力选择；对 `Test` 额外代行门的消费 | PRD/Spec/Plan 分支行为逐字节不变 |
| `hooks/task approve` | 对账 `[stage]` 行与 `released` | 只增加 `require_stage Test`，对账逻辑复用 |

**不变式（I1）**：`released` 的最大 `seq` 永远等于 `evidence` 的行数。门靠 `evidence > consumed` 判定有没有可消费的记录；两个文件一旦不同步，之后**所有**阶段都会被门永久拒绝。现有 `unaided` 对 PRD/Spec/Plan 同时写两个文件就是为了守这条。`Test` 的消费分支也必须守住它——它不新增 evidence 行，只是把已存在的第 `max+1` 行"标记为已消费"，所以天然满足；只有走 unaided 分支时才需要补写 evidence 行。

**I1 的入口检查（本任务新增）。** 上面说的是「怎么写才不破坏它」；还缺「进来时已经坏了怎么办」。`consumed` 只从 `released` 取，所以 `evidence` 被删或截断的 store 读起来像「已经走过队列末尾」，此后每一次声明都在把差距拉大而不是缩小。`unaided` 是唯一有机会发现它的写者，因此在写任何东西之前先比对 `consumed` 与 `total`：`consumed > total` 时拒绝并给出两个数字。丢掉的行无法重建，所以消息同时写明恢复方式——删掉 `<absolute-git-dir>/taskflow` 后逐阶段重新声明。这道检查放在 stage 分支之上，对四个阶段一视同仁。

## Project Structure / Affected Files

```text
hooks/task                       # unaided 的 stage case、消费分支、approve 的 require_stage
hooks/smoke-test                 # 新断言段 + 既有 approve 夹具补 [Test]
skills/taskflow/SKILL.md         # 阶段表、能力段落、approve 那段
skills/taskflow/references/artifacts.md   # Plan 模板的行形状、approve 说明
skills/taskflow/references/runtime.md     # store 写者数量、命令表
hooks/README.md                  # unaided 条目
CHANGELOG.md                     # Unreleased
```

SSOT 位置：**契约的权威描述只有一处是代码**——`hooks/task` 的 `unaided` 分支。四份文档是对它的描述，不是第二份契约。

## Interfaces, Data Flow, and Contracts

### 契约 1 — `task unaided <stage> --considered "<class>"`

```text
用法:  task unaided <PRD|Spec|Plan|Test> --considered "<concept class>" [--root <path>]
退出码:
  0  已记录（含幂等的"已记录过"分支）
  1  环境错误（无活动任务、找不到 git dir、读不到 Task version）
  2  参数错误（stage 不合法、缺 --considered、类不在词汇表内）
```

**输出契约（R3）。** 现有三条消息保留原文，`Test` 的 invoke 分支需要额外打印能力名，否则 Agent 无从写对 `[Test]` 行。

| 情形 | 输出 |
| --- | --- |
| PRD/Spec/Plan 首次 | `unaided OK: <stage> in <task> -> <class>` |
| 任意阶段已释放 | `unaided OK: <stage> in <task> -> <class> (already released)` |
| Test → unaided | `unaided OK: Test in <task> -> <class> (recorded as unaided)` |
| Test → invoke | `unaided OK: Test in <task> -> <class> (consumed an invocation record: <capability>)` |

`(recorded as unaided)` / `(consumed an invocation record: <cap>)` 是本 Spec 新增的**唯一**输出变化，且只出现在 `Test` 上。前两种消息在 `Test` 上复用原文时加同一后缀，保持"一句话说清记成了什么"。

**为什么用能力名作后缀而不是另起一行：** `approve` 拒绝时打印的是 `(stage [$stage] does not name a capability invoked in this Task version ($capability))`——它已经在括号里给出正确名字，声明时用同一形状，Agent 两边照着写即可，不需要第二套措辞。

### 契约 2 — `## Skills / Tools Used` 里的 `[Test]` 行文法

与既有三种阶段完全同构，不新增字段：

```text
- [Test] `<capability>` — purpose: `<why>`; outcome: `succeeded|failed|unavailable`; incorporated: `<conclusion or None>`
- [Test] Unaided — no capability applied to this phase; considered: <concept class>
```

判别规则（复用 `approve` 现有分支，不新增代码路径）：
- 行里出现 `Unaided` → 必须对上 `kind=unaided` 的记录，且 `considered:` 后的文本必须**逐字**包含记录里的类名。
- 否则 → 必须对上 `kind=invoke` 的记录，且行里必须出现本版本 invoke pool 中的某个能力名（**子串匹配**，与另外三个阶段一致）。

### 契约 3 — `released` 的第五字段

现有格式 `vN|Stage|seq|kind|capability` 不变。`Test` 的 `kind` 只有两种取值：

| `kind` | `capability` 字段放什么 | 谁决定的 |
| --- | --- | --- |
| `invoke` | 从 evidence 第 `max+1` 行原样取出的能力名 | 队列状态 |
| `unaided` | `--considered` 的值 | 声明者 |

**这是本任务唯一的新语义：** `kind` 不是声明参数，是队列的可观察结果。声明者只能决定"哪个概念类"，不能决定"这算不算一次调用"。

## Invariants and Compatibility

- **I1**（上文）`released` 最大 seq == `evidence` 行数。
- **I2** 幂等键仍是 `(version, stage)`，与门一致。对 `Test` 重复声明不消费新证据行。
- **I3** PRD/Spec/Plan 的代码路径不变：`case "$stage" in PRD|Spec|Plan)` 内的逻辑原样保留，`Test` 走独立分支。用既有 18 处 `approve` 断言守住。
- **兼容性代价（必须承认）**：`approve` 无条件要求 `[Test]`，所以**所有在途任务**（本仓库当前 0 个 active，但被 `version` 提升的老任务、以及用户自己的项目）下一次 `approve` 会失败。缓解措施是失败消息必须给出补救命令——与既有 `was never released by the pre-write gate` 那条同构：`bash hooks/task unaided Test --considered 'testing strategy'`。

  这是有意的破坏性变更，不是兼容问题：不要求它，就又是「自觉性」。CHANGELOG 归入 `Changed` 而不是 `Added`。

- **不写兼容代码**：不加 `--allow-no-test` 之类的开关（用户明确反对写兼容代码）。

## Validation and Error Semantics

校验位置与现有 `unaided` 一致，不做第二次：

| 校验 | 位置 | 退出码 |
| --- | --- | --- |
| stage 属于 `PRD|Spec|Plan|Test` | `case` | 2 |
| `--considered` 非空 | 显式检查 | 2 |
| 类在 `concept_class_re` 内 | 现有正则 | 2 |
| 有活动任务 | 现有循环 | 1 |
| 能读 Task version | 现有 sed | 1 |
| store 已在入站前失同步（`consumed > total`） | I1 入口检查 | 1 |

最后一行归 1 而不是 2：它不是「参数没用对，改一下重来」，而是「环境里有一份说不清的记录」——与「找不到 git dir」「读不到 Task version」同族，走同一个 `fail`。消息给出两个数字与恢复方式，因为调用者无法自己推断丢了几行。

`approve` 侧不重复校验词汇表（现有注释已说明理由：`unaided` 是唯一边界）。

## Code and Test Constraints

- **bash 3.2 + busybox awk + POSIX sed**，无 Python、无 `declare -A`、无 `mapfile`、无 GNU-only `sed -i`。这是仓库的硬约束（`CODE_STYLE.md:12-18`）。
- **不用管道喂大文本给 `grep -q`**：`set -o pipefail` 下 `printf | grep -q` 会因 SIGPIPE 假失败（`hooks/completion-gate` 的头注释记录了这次实测）。读 `released` 一律 `awk` 读文件。
- **断言风格**：沿用 `hooks/smoke-test` 现有的 `grep -q 'FAIL …' || { echo; exit 1; }` 形状，不引入测试框架。
- **变异验证**：每条新断言都要有一次"故意改坏 → 套件变红 → `cp` 还原 → `diff -q` 确认"。

## Design Decisions and Alternatives

| # | 决定 | 备选与拒绝理由 |
| --- | --- | --- |
| D1 | `Test` 由 `unaided` 代行队列消费 | 备选：新增 `task declare Test`。命令名更干净，但要多一条命令 + 一套文档 + 一次全仓库改名；用户选了前者。 |
| D2 | 只有 `Test` 消费队列 | 备选：四个阶段统一。会让 `unaided PRD` 在有未消费行时被记成 invoke，而 PRD 的行随即又被门消费一次，破坏 I1 与 18 处既有断言。 |
| D3 | `[Test]` 行总是必需 | 备选：仅当 Plan 有测试 Step 时。仓库没有"什么是测试文件"的约定，判定要么靠名字猜（假门）要么造正面清单（脆）。零判定的一行更诚实。 |
| D4 | 不新增 PreToolUse 门 | 测试散在多个 Step，无唯一首次写入点；卡住第一个测试文件需要先定义什么是测试文件——把 D3 拒绝的东西转移到门里。 |
| D5 | 输出后缀携带 `kind` 与能力名 | 备选：静默成功。那样 Agent 必须去读 `<absolute-git-dir>/taskflow/released`（一个故意不让人依赖的内部存储）才能写对行。 |

## Open Questions

无。四个决定已由用户给定，见 `prd.md` 的 Open Questions。
