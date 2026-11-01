# Archived Version v1 — Plan — 外部事实：先判断，再取证
> Task: 2026-10-31-external-facts
> Version: v1
> Status: superseded
> Archived: 2026-11-01 20:05 +0800
> Superseded by: v2
> Archive mode: file

## Change Summary

v1 交付的是一个**可检查的字段**：`prd.md` 必须回答「本任务的结论是否依赖仓库外的事实」，`approve` 读它并拒绝四种坏形态。它在 2026-11-01 实现完毕，CI 全绿（PR #108）。

用户随后指出：**要解决的不是「没有记录」，而是「模型在当前框架下倾向于不搜索」。** 这两件事之间隔着一步 —— v1 的字段记录判断，但不改变行为；一个不搜索的模型写一句 `no` 加个像样的理由就通过了，而且看起来完全合规。v1 的 PRD 自己在 Risks 里写了这一点（「`no` 分支可能被当成橡皮图章」），但把它当成可接受的代价，而不是本任务要解决的问题。

v2 因此改变了承诺：

- **加一个真实的停顿点。** 现有框架里没有一个时刻会问「这件事的答案在仓库外吗」—— `inspect` 八项全在仓库内，`summarize-state` 注入的全是内部结论，`prompt-reminder` 每回合只说任务状态。v2 在 Phase 1、Phase 3 收敛前和 Plan 定稿前各插一个问句。
- **让检索变成可见事件。** v1 明确把 `WebSearch`/`WebFetch` 排除在 `capability-evidence` 之外（沿用 R12）。v2 把它们接进来，但**能力隔离**：检索记录与能力记录分开存放、分别消费，`TaskFlow` 的门禁仍只认 `Skill`/`Agent`/`mcp__*`。
- **无外部证据则拦。** 这是 v1 没有的强度。一个任务若声明依赖外部事实却拿不出检索记录，`approve` 拒绝。

被 v1 接受、v2 不再接受的东西：一个空口无凭的 `no`。

## Archived Materials
- prd.md
- plan.md

## Restore
Read the archived v1 core docs from a new temporary restore root. Do not overwrite the current task root.
