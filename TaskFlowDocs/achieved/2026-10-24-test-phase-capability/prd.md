# Test generation and test writing should draw in tools through the same mechanism

> Task version: v1
> Status: completed

## Goal

让 Phase 6（验证与审查）里「写测试」这一阶段的能力选择有载体：跟 PRD / Spec / Plan 一样，有东西逼它发生、有东西记录它发生过。今天它只是 `SKILL.md` 阶段表里的一行文字，没有任何机制读它。

## Background / Confirmed Facts

以下都是 2026-10-24 在本仓库实测的，不是推测：

- **阶段表有 7 行，只有 3 个阶段有载体。** `skills/taskflow/SKILL.md:171-179` 的表格给每个阶段写了「Equivalent concept class」，但 `hooks/capability-gate:96-98` 只匹配 `prd.md`/`spec.md`/`plan.md`；`hooks/task:1075` 的 `unaided` 只接受 `PRD|Spec|Plan`；`hooks/task:1254-1257` 的 `approve` 只对账这三行。Research（2）、Build（5）、Verify（6）、Complete（7）四个阶段的概念类只活在散文里。
- **测试阶段的实际使用量和记录量完全脱节。** 85 个已归档任务里，77 个的 `plan.md` 提到并跑过测试（`smoke-test` 等）；写了 `- [Test]` 或 `- [Verify]` 阶段行的：**0 个**。也就是说这一阶段的能力选择从来没有被记录过一次。
- **概念类已经合法存在，缺的只是载体。** `hooks/task:614` 的 `concept_class_re` 已含 `testing strategy`，`hooks/task:1085` 会用这个正则校验 `--considered`。所以 `task unaided Test --considered "testing strategy"` 的**词汇表校验现在就能过**，唯一挡住它的是 `case "$stage" in PRD|Spec|Plan)` 那一行。
- **门消费不了 Test。** `capability-evidence` 记录一次真实调用，`capability-gate` 在某文档**首次正文写入**时消费它并写 `released`。测试是散在多个 Step 里的一堆文件，没有那个唯一写入点——这正是本任务要绕开的地方。
- **`released` 只有两个写者**：`capability-gate:160`（门消费 evidence）与 `hooks/task:1136`（`unaided` 自写一行 evidence + 一行 release）。没有第三条路。
- **`approve` 的 invoke 分支对的是整个版本的 invoke pool**，不是该阶段自己的记录（`hooks/task:1180-1196` 的注释解释了为什么必须这么宽：store 不带阶段，阶段靠队列位置附着）。

## Requirements

- **R1 — `task unaided` 接受 `Test` 阶段。** `PRD|Spec|Plan` 扩为 `PRD|Spec|Plan|Test`，用法串与错误消息同步。词汇表校验不变。
- **R2 — 只有 `Test` 在声明时消费证据队列。** 现有 `unaided` 对 PRD/Spec/Plan 的行为是「自己写一行 evidence，再写一行 release（seq = max+1）」，**逐字节不变**。`Test` 不同：因为门永远不会为它消费，由声明代做门本来会做的事——
  - `evidence` 行数 > `released` 的最大 seq 时，取第 `max+1` 行，`kind` 与 `capability` 从该行原样取出，写 `vN|Test|seq|invoke|<capability>`；
  - 否则写 `vN|Test|seq|unaided|<considered>`，并追加对应的 evidence 行（保持两文件同步，否则后续所有阶段都会被门拒绝）。

  `kind` 由队列状态决定，不由声明者指定——声明者无法把一个没发生过的调用写成发生过。
- **R3 — 声明必须报告它记下的 kind 与能力名。** `[Test]` 行要与记录对账，所以命令输出必须让 Agent 能照着写：记成 invoke 时打印能力名，记成 unaided 时打印类名。否则 Agent 只能猜，猜错就是 `approve` 拒绝。
- **R4 — `task approve` 无条件要求 `[Test]` 行。** 与其他阶段同一套对账规则（invoke 行须点名本版本 invoke pool 里的能力；`Unaided` 行须携带记录里的类）。不设「没有测试就不要求」的判定——仓库现在没有「什么算测试文件」的约定，造一个就是第二套判断标准。
- **R5 — 四份文档同步。** `skills/taskflow/SKILL.md` 的阶段表与能力段落、`references/artifacts.md` 的 Plan 模板与 approve 说明、`references/runtime.md` 的 store 说明与命令表、`hooks/README.md` 的 `unaided` 条目，都写明 Test 是必需的第四个阶段、它的两种行形状、以及为什么它的 kind 由队列决定。
- **R6 — `hooks/smoke-test` 断言 A1–A8**（见验收条件），并覆盖 `unaided Test` 的两个分支与幂等。

## Acceptance Criteria

| # | 可观察条件 |
| --- | --- |
| A1 | `Skills / Tools Used` 里缺 `[Test]` 行时 `approve` 拒绝，消息点名 `[Test]` |
| A2 | 队列无未消费行时 `task unaided Test --considered "testing strategy"` 记成 `unaided`，打印类名；对应的 `[Test] Unaided …` 行通过 `approve` |
| A3 | 队列有一行 `invoke\|<cap>` 时同一命令记成 `invoke`，打印 `<cap>`；`[Test] \`<cap>\` …` 通过，而 `[Test] Unaided …` 被拒（kind 不符） |
| A4 | `--considered` 是词汇表外的类时 exit 2，且不写任何记录 |
| A5 | `task unaided Test` 对同一版本重复调用，第二次不再消费新证据行（幂等，键同为 `(version, stage)`） |
| A6 | PRD / Spec / Plan 的行为逐字节不变：既有 18 处 `approve` 断言在补上 `[Test]` 行后全部通过，且 `stages released by the gate` 的计数与改动前一致 |
| A7 | 五份文档对同一个契约的描述不互相矛盾（Test 必需、两种形状、kind 由队列定） |
| A8 | `bash hooks/smoke-test`、`bash hooks/release-check .`、`git diff --check` 全绿；CI 7/7 |

## In Scope

- `hooks/task` —— `unaided` 接受 `Test` 并实现按阶段分流的消费逻辑；`approve` 加 `require_stage Test`。用户追加要求：`unaided` 在写任何记录前先查 I1，`released` 已越过 `evidence` 行数时拒绝并给出恢复方式（原为 Follow-up，见 Change Log）。
- `hooks/smoke-test` —— A1–A6 的断言，以及把既有 approve 夹具补上 `[Test]` 行与对应 release 记录。
- `skills/taskflow/SKILL.md` —— 阶段表与能力段落。
- `skills/taskflow/references/artifacts.md` —— Plan 模板的行形状与 approve 对账说明。
- `skills/taskflow/references/runtime.md` —— store 的两个写者增加到三个的说明，命令表。
- `hooks/README.md` —— `unaided` 条目。
- `CHANGELOG.md` —— `[Unreleased]` 条目。
- `TaskFlowDocs/todo.md` —— `TF-20261024-310937` 的推进与收尾。

## Out of Scope

- **Research（2）、Build（5）、Complete（7）三个阶段的载体** —— 用户已明确本次只做测试阶段。它们各自缺的东西不一样（Research 无固定产物、Build 的产物就是改动本身、Complete 在归档之后），一起做会变成「统一重构」。
- **不新增 `PreToolUse` 门** —— 没有单一首次写入点可卡，造一个只能靠名字猜的假门。
- **不改 `Unaided` 的措辞语义** —— 「没有工具时回落到模型自身能力」这一层是 `TF-20261024-b48e56`，本任务只保证 `[Test]` 行能如实表达它。
- **不回填已归档的 85 个任务** —— `achieved/` 是只读历史，`approve` 从不在其上运行。
- **不重命名 `unaided` 命令** —— 它对 Test 可能记下 invoke，名字确实不再贴切；但这属于全仓库改名，单独立项。

## Risks / Deferred Items

- **风险：给 `Test` 一个「从队列取 kind」的例外，打破了「`unaided` 自写证据」这一条的唯一性。** 缓解：例外只对 `Test` 一个阶段生效，且写进 `runtime.md` 的 store 段落与代码注释；A6 用既有夹具把它钉住，PRD/Spec/Plan 行为变了立刻红。
- **风险：Agent 在写完 `plan.md` 之后又做了一次无关的能力调用（例如代码审查），然后 `unaided Test` 会消费那一行并记成 invoke。** 这是队列位置语义的既有性质（`capability-gate:145-149` 已记录同样的后果），不是新缺陷。缓解：R3 让命令打印它记下的名字，Agent 当场就能写对；文档写明「不要在声明 Test 前留一行不相干的能力调用」。
- **遗留：`unaided` 的名字与它可能记下 invoke 的事实不符。** 记入 Follow-ups。
- **遗留：每版本重复记账**（`TF-20261012-c66ad3`）—— 加第四个阶段会让它描述的「每版本重复 N 次」变成 N+1。本任务不改该机制。

## Open Questions

无阻塞性问题。以下两个决定已由用户在三轮问答中给定，记录在案：

1. 范围只做测试阶段。
2. 载体是 `Skills / Tools Used` 的 `[Test]` 行 + `approve` 对账，不新增门。
3. `[Test]` 行总是必需。
4. 只有 `Test` 在声明时消费证据队列。
