# Spec — 批准前审查 Plan 本身
> Task version: v1

## Objective and Success Criteria

在 `plan.md` 写完与用户批准之间，插一次对 Plan 本身的审查，并把结果写进一个 `task approve` 会检查的固定节。成功判据：四种不合格输入各被拒绝且消息互不相同；合格输入通过；已归档任务不受影响。

## Architecture Boundaries and Responsibilities

本次改动跨三层，各自职责与其**明确不负责**的部分：

**`skills/taskflow/SKILL.md`（Agent 的指令层）**
- 负责：在 Phase 4 末尾告诉 Agent「批准前要审 Plan」、审哪三问、为什么必须在这一刻。
- 不负责：判断审查是否真的做了。散文没有执行力——`TF-20261009-887511` 是同一层失效的现成证据。

**`plan.md` 的 `## Plan Review` 节（记录层）**
- 负责：承载审查结论，让用户在批准前能读到，让 `task approve` 有东西可查。
- 不负责：保证结论正确。它记录的是审查者说了什么，不是事实。

**`hooks/task approve`（执行层）**
- 负责：拒绝缺失、空白、或三问未逐条作答的节，并给出补法。
- 不负责：判断答案质量。机器读不出「覆盖是否真的完整」，只能读出「三问是否都答了」。

**依赖方向**：`SKILL.md` → 生产者写出该节 → `approve` 读它。反过来不成立：`approve` 不生成内容，不修改 Plan，不推断审查是否发生。

**明确不在本层**：`TF-20261024-b48e56`（无可用能力时用模型自身能力）解决的是「审查者是谁」的措辞；本次只要求「审查发生了」。两层可以独立变化。

## Project Structure / Affected Files

- `skills/taskflow/SKILL.md` — Phase 4 末尾（`## External Facts` 复核之后、`## Approval` 模板之前）。
- `skills/taskflow/references/artifacts.md` — Plan 轮廓加 `## Plan Review`，并在轮廓后补说明。
- `hooks/task` — `approve` 分支，在 `## External Facts` 检查之后、`approved_version` 读取之前。
- `hooks/smoke-test` — 新增一节，覆盖四种拒绝与一种通过。

## Interfaces, Data Flow, and Contracts

**生产者（Agent）保证**：`plan.md` 里有一个 `## Plan Review` 节，含三条以固定前缀开头的答案行。

**消费者（`approve`）可以假设**：只按行首前缀匹配，不去理解句子内容。

**契约三条固定行**，前缀是机器读的、其余是散文：

```
- Coverage: <每条 PRD 验收标准落到哪个 Step，或指出哪条没有>
- Verifiability: <每个 Step 的 Verification 是否真能验证其 Acceptance>
- Layer ownership: <有没有哪一步打算改中间产物/夹具/期望值让下游变绿；有则指出，没有则明说>
```

前缀选 `- Coverage:` / `- Verifiability:` / `- Layer ownership:` 的理由：
- 与 `## Approval` 的 `- Status:` 等字段同形，都是行首 `- Name: value`，`approve` 已有的解析惯例可以复用；
- 是英文，符合「hook 匹配的行用英文」这条既有规则；
- 三者互不重叠，各自对应一类真实错误。

**反向契约（消费者对生产者的义务）**：`approve` 必须能分别说出「缺哪一条」，而不是笼统报「Plan Review 不合格」。否则补齐时不知道该改什么。

**数据流**：`plan.md` 是唯一事实源。不新增存储文件，不写证据账本——这不是能力调用记录，是 Plan 的一部分。

## Invariants and Compatibility

1. **已归档任务不受影响**：`approve` 只对传入的任务目录运行，不扫描 `TaskFlowDocs/achieved/`。归档本身不重跑 `approve`。
2. **已批准任务不追溯**：检查发生在写 Approval 之前的路径上；已经 `Status: approved` 的任务不会再进这段逻辑，因为它们不再需要 `approve`。
3. **`## Plan Review` 必须排在 `## Approval` 之前**：`awk` 的节边界读取依赖这个顺序，且审查在批准前的语义也要求如此。
4. **不改变现有 stage 检查**：`[PRD]`/`[Spec]`/`[Plan]`/`[Test]` 的逻辑与顺序完全不动。

## Validation and Error Semantics

`approve` 的五种结局，消息各不相同：

| 输入 | 结局 |
| --- | --- |
| 没有 `## Plan Review` 节 | 拒绝，给出该节的完整模板 |
| 有节但空白 | 拒绝，说节存在但没写内容 |
| 缺 `- Coverage:` | 拒绝，点名这一条 |
| 缺 `- Verifiability:` | 拒绝，点名这一条 |
| 缺 `- Layer ownership:` | 拒绝，点名这一条 |
| 三条都在且非空 | 通过，继续原有流程 |

退出码沿用 `fail` 的 `1`（与 `approve` 其余拒绝一致）。

## Code and Test Constraints

- `hooks/task` 用 POSIX shell + awk，不引入解释器。
- 节读取用一次 `awk`，不用 `printf | grep -q`（`pipefail` 下大文件会假失败，`completion-gate` 顶部已记录这个坑）。
- `hooks/smoke-test` 的断言要能区分五种结局，不能只测「被拒绝了」。
- 已有 `package.json`/`RELEASE.md` 类断言不涉及本改动。

## Design Decisions and Alternatives

**为什么不用 `PreToolUse` 门。** `capability-gate` 拦的是首次正文写入。Plan 审查在 `plan.md` 写完之后才有对象，用 `PreToolUse` 拦它等于让 Plan 永远写不出来。而且 `PreToolUse` 门检查的是「有没有调用过能力」，本次要检查的是「Plan 里有没有审查结论」——两者看的对象不同。

**为什么门在 `approve` 而不是 `archive`。** `approve` 是 Approval 块的唯一写入者，`in_progress`/`complete`/`archive` 全部排在它后面。堵在这里，跳过审查就无路可走；堵在 `archive` 则要等到实现完才发现，那时改 Plan 的成本已经付过了。

**为什么记录在 `plan.md` 而不是独立文件。** `SKILL.md` 明确禁止为同一任务建第二个事实源（root `SPEC.md`、`TaskFlowDocs/plan.md`、自动 review 文件都在禁止名单里）。审查结论是 Plan 的一部分，就该在 Plan 里。

**为什么不新增 concept class。** 审查者的记录沿用现有 `[Plan]` 行形状即可。新增 `plan review` 类要同时改阶段表、`concept_class_re`、`stage_classes`，三处手抄的同步成本已经在 `hooks/smoke-test:3249` 记录过一次教训。等 b48e56 落地后若确有必要再议。

**备选方案与放弃理由。**
- *只写散文*：被 `TF-20261009-887511` 证否。
- *放在 Phase 6*：太晚，计划层面的错误在批准时已锁定。
- *用独立 review 文件*：违反单一事实源规则。
- *判断审查质量*：机器做不到，硬要做会变成关键词匹配，那正是 `repo-rules check` 已经承认只能报「possible conflict」的那类弱检查。

## Open Questions

无。
