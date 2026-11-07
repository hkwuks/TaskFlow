# 批准前审查 Plan 本身
> Task version: v1
> Status: in_progress

## Goal

在 `plan.md` 写完、用户批准**之前**，对 Plan 本身做一次审查——不是审代码——并把审查结果写进 `plan.md` 的一个固定节；`task approve` 拒绝缺失或空白的该节。审查查三件事：PRD 验收标准的覆盖、每个 Step 的验证手段是否真能验证其验收、有没有哪一步是靠改中间产物让下游检查变绿。

## Background / Confirmed Facts

**空洞在哪**：`SKILL.md` Phase 4 结尾直接进 `## Approval` 模板，随后就是 `task approve`。中间的 `## External Facts` 复核只查「本任务的结论是否依赖仓库外的事实」，不审 Plan 的结构。Phase 6「Verify and review」审的是代码与验收，在实现**之后**。

**后果**：用户批准的那份 Plan 没有任何环节检查过。计划层面的错误——某条验收标准没有 Step 覆盖、某步的验证手段验不了它的验收、某步打算改夹具让测试变绿——在批准那一刻被锁定。之后要么改版本重走审批，要么带着缺陷实现。

**判据来自既有规则**：第三问不是新发明，它直接接 `SKILL.md` Phase 5 已有的禁止性规则——「失败必须修在失败所属的层，绝不用让生成方的输出对下游看起来正确的方式去修」。Phase 6 第 9 条要求实现后点名每个被改的中间产物；本次把同一问题提前到批准前。

**为什么用硬门而不是散文**：`TF-20261009-887511` 是现成反例——语言规则写得很清楚，但没有检测，照样失效。用户已明确要求加 hook 门。

**为什么门在 `task approve` 而不是 `PreToolUse`**：审查发生在 `plan.md` 写完之后。`PreToolUse` 门（`capability-gate`）拦的是**首次正文写入**，用它拦 Plan 审查等于让 Plan 写不出来——顺序反了。而 `task approve` 是 Approval 块的唯一写入者，且 `in_progress`、`complete`、`archive` 全都排在它后面，所以堵在这里，跳过审查就没有任何一条路能推进任务。

**「没有可调用能力时怎么办」不在这里解决**：用户指出该问题由 `TF-20261024-b48e56` 处理（无工具可引入时，回退是模型自身能力）。本节的门只要求「审查发生了」，不判断审查由什么执行；审查者写成 `- [Plan Review] <capability> — …` 或 `- [Plan Review] Unaided — …; considered: <class>` 都可以，两种形状现在都能过。b48e56 落地后可以再收紧，但那时改的是措辞而不是门的存在与否。

## Requirements

1. `plan.md` 轮廓新增 `## Plan Review` 节。
2. 该节含一个判定（`Verdict: sound | needs revision`）与三条支撑问题，答案必须逐条给出（不能只写一句「已审」）；判为 `needs revision` 时 `approve` 拒绝。
3. `task approve` 在 stage reconcile 之后、写 Approval 之前检查该节：缺失、空白、四行中任一未作答、`Verdict` 为 `needs revision` 或其词不在词表内，都拒绝并说明补法。
4. `SKILL.md` Phase 4 末尾加审查指引，说明查什么、为什么在批准前。
5. `references/artifacts.md` 的 Plan 轮廓与说明同步。
6. 现有已批准任务不追溯（避免把历史任务全变成不可推进）。

## Acceptance Criteria

- `plan.md` 轮廓含 `## Plan Review`，与 `## Approval` 相邻（在它之前）。
- `task approve` 对以下输入分别拒绝，且消息各不相同：节缺失、节空白、缺 `Verdict`、缺任一支撑问题、`Verdict: needs revision`、`Verdict` 用词不在词表内。
- 四行齐全且 `Verdict: sound` 时 `task approve` 通过。
- 已归档任务（`TaskFlowDocs/achieved/` 下）不受影响：该检查只对 `approve` 运行中的任务生效，不扫描历史。
- `bash hooks/smoke-test` 通过；`git diff --check` 通过。

## External Facts

- Depends on external facts: no
- Why not: 判据全在仓库内 —— `SKILL.md` Phase 5 的禁止性规则、Phase 6 第 9 条、`hooks/task` 的 `approve` 检查顺序、以及 `TF-20261009-887511` 这个「散文无检测即失效」的先例。

## In Scope

- `skills/taskflow/SKILL.md` — Phase 4 末尾的审查指引。
- `skills/taskflow/references/artifacts.md` — Plan 轮廓与说明。
- `hooks/task` — `approve` 的新检查。
- `hooks/smoke-test` — 覆盖四种拒绝与一种通过。

## Out of Scope

- 不在 `PreToolUse` 加门：审查在 Plan 写完之后，挡写入会颠倒顺序。
- 不判断审查质量：门只能查「三问都答了」，答得对不对是审查者的责任，机器判不了。
- 不改 concept class 词表：审查者的记录沿用现有形状，不新增阶段。
- 不追溯已批准任务：那会把历史任务变成不可推进。
- 不解决「无可用能力时的回退表述」：那是 `TF-20261024-b48e56`。

## Risks / Deferred Items

- 风险：成了「填三行字」的形式主义。缓解：三条问题的措辞直接对应三类真实错误，且第三条接的是 Phase 5 已有的禁止项；门要求逐条答案，一句「已审」会被拒。但门无法判断答案质量——这是硬门的固有限度，如实记在 Known limitations。
- 风险：让简单任务的审批变重。缓解：三问在纯文档改动上可以各写一行，成本低于一次版本重来。
- 遗留：`TF-20261024-b48e56` 落地后，可以要求 Unaided 的审查行必须说明模型用了什么能力，而不是只说「没有工具」。

## Open Questions

无。
