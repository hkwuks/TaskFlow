# Spec — `released` 行的任务身份与多行阶段对账
> Task version: v1
> Status: ready

## Objective and Success Criteria

R1–R7 在 PRD 里定死。本 spec 记录选定的行格式、四个消费者各自改到的字段位、旧格式的判别规则，以及为什么不做迁移。

## Architecture Boundaries and Responsibilities

| 角色 | 读 | 写 | 本条的改动 |
| --- | --- | --- | --- |
| `capability-gate` | `evidence`、`released` | `released`（追加一行） | 写入加任务名；已释放判定改键；识别 5 字段旧行并拒绝用它放行 |
| `hooks/task unaided` | `evidence`、`released` | 两者（各追加一行） | 同上；输出带任务名 |
| `hooks/task approve` | `released`、`Plan` | `Plan` 的 Approval 块 | 对账键加任务名；接受任意一条阶段行 |
| `hooks/task recover` | `evidence`、`released` | `released`、`released.discarded` | seq 从 `$3` 变 `$4`；字段数不改写 |
| `capability-evidence` | 事件 | `evidence` | **不动**（`evidence` 行的格式不变） |

`evidence` 的格式 `kind|capability` 不变。任务身份只存在于 `released`——因为只有 `released` 需要回答「这是谁的释放」。

## Project Structure / Affected Files

```text
hooks/capability-gate   task_name 已有；写入行加它；判定键改；旧格式提示
hooks/task              unaided / approve / recover 三处 + 旧格式提示
hooks/smoke-test        新断言（跨任务、多行、旧格式、consumed 兼容）
skills/taskflow/references/artifacts.md   approve 的多行语义
skills/taskflow/references/runtime.md     released 行格式与任务身份
CHANGELOG.md            [Unreleased]
```

## Interfaces, Data Flow, and Contracts

```text
released 行（当前格式，6 字段）
  <task>|<version>|<stage>|<seq>|<kind>|<capability>
  例：2026-10-26-capability-task-identity|v1|PRD|7|invoke|agent-skills:spec-driven-development

released 行（旧格式，5 字段，只读不写，遇即报错）
  <version>|<stage>|<seq>|<kind>|<capability>
```

| 消费者 | 用它做什么 | 6 字段 | 5 字段 |
| --- | --- | --- | --- |
| 已释放判定（门 / `unaided`） | 命中则跳过 | 按 `$1,$2,$3` | **永不命中** |
| `consumed`（门 / `unaided` / `approve` / `recover`） | 取整列最大 seq | `$4` | `$3` |
| `approve` 取记录 | 取 `(task,version,stage)` 那行 | `$1,$2,$3` | **永不命中** |
| `approve` 的 `cap_pool` | 本任务本版本所有 `invoke` 行的能力名 | `$1,$2` 匹配、`$6` | **不参与** |
| `recover` | 丢 `seq > evidence 行数` | `$4` | `$3`（照读，不重排） |

**为什么 `consumed` 两种都读**：`consumed` 是「已经花掉多少条证据」，这个语义与任务无关。升级后若只读 6 字段行，旧行占用的序号就会变成「没花过」，门会把同一条证据再释放一次——把一条证据花两次，正是 1.1.0 设计这条队列时要防的。所以 `consumed` 必须保守地取两种格式的最大值。

**为什么别的判定两种都*不*读**：一条旧行说不清属于谁。让它匹配任何任务，就是本任务要修的那个 bug；让它匹配「当前任务」，就是 PRD 第 2 条实测证明过的错误推断。

## Invariants and Compatibility

**I1 — `released` 的最大 seq == `evidence` 行数。** 四个写者维持它；本任务不改这条，只改 seq 在哪个字段。

**I2 — 写侧只有一种格式。** 新的 `released` 行永远是 6 字段。R7：不做能让 5 字段继续生效的兼容层。

**I3 — 任务名来自路径，不来自文档内容。** 门用被写文档的父目录名，`unaided` 用 `TaskFlowDocs/<x>` 的 `<x>`。两者都已经被 `hooks/task-id` 的形状约束，不需要额外校验。

**I4 — 一个阶段的多个 `- [Stage]` 行是「调用过多个」，不是「有一行是错的」。** `approve` 认任意一条匹配即可（R4），因为 `artifacts.md:132` 已经允许这么写。

**兼容性（故意的破坏）**：升级后，含 5 字段行的 store 会让 `approve` 拒绝并要求清理。这不是退步——当前行为是「静默地把别的任务的释放当成本任务的」，两害相权取其明。

## Validation and Error Semantics

- 旧格式检测只看字段数：`awk -F'|' '{ print NF }'` 得到 5 或 6。其它字段数一律视为损坏，报错而不是猜。
- 门是 `PreToolUse` 钩子，**不能因为格式问题就 panic 成放行**：检测到旧行时，门的判断是「本阶段未被释放」→ 走现有的 deny 路径，只在 deny 文案里加一句旧格式说明。**不新增 fail-open 面。**
- `approve` / `unaided` 的旧格式提示走各自的 `fail`，退出非零。

## Code and Test Constraints

- 只用 POSIX `awk` / `sed`，不引入新依赖。
- 四个消费者的 seq 取法必须逐字相同（同一个 awk 形状），避免出现第五个口径——上一个任务（`2026-10-25-capability-store-recover`）已经因为「三处算法要一致」踩过一次。
- 断言用 `printf` 造 store、`--root` 指夹具；门用 JSON 事件驱动。**事件必须带 `hook_event_name`，否则门静默 exit 0**（本次实测踩到：只给 `tool_name` 的门对任何输入都放行）。

## Design Decisions and Alternatives

1. **加字段而不是换文件。** 备选「每个任务一个 `released.<task>`」被否：`consumed` 需要跨任务单调（它是证据队列的全局水位），拆文件后每次都要扫全部文件取最大值，且 `recover` 要处理 N 个文件。
2. **任务名放在第 1 字段。** 备选「追加到末尾」被否：追加在末尾会让「前缀匹配」的读法在旧行上仍然成立，等于给了旧行一条活路，与 R6 冲突。
3. **不迁移旧行。** 理由不是懒：任何自动迁移都要猜「这条行属于谁」，而 PRD 第 2 条实测已经证明那个猜法是错的。
4. **`approve` 认任意一条阶段行**，与 store 改动放在同一个任务里。备选「拆成两个任务」被否：两条缺陷的现场是同一个报错（`does not name a capability invoked`），用户看到的是一个症状，分开修会让人在两次升级之间既撞串线又撞多行。
5. **`consumed` 保守读取两种格式**，这是整个契约里唯一「读旧」的地方，而它不是兼容代码——它是把「已经花掉的量」算对。删掉它会让升级本身成为一次数据事故。

## Open Questions

无。
