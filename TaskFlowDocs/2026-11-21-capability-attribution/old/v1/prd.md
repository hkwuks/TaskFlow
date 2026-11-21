# 能力调用证据的任务和阶段归属
> Task version: v1
> Status: in_progress

## Goal

阻止其他任务或阶段的能力调用记录释放当前阶段，同时保留无合适能力时显式 unaided 的选择。

## Task Kind

- Kind: defect

## Background / Confirmed Facts

记录器把调用写成没有任务和阶段的队列行，门禁按最早未消费行放行，无法验证调用归属。用户提供的模拟显示跳过工作区交接可跨任务消费；正确交接会移走旧账本。同一任务的多次调用也可能跨阶段消费。实际 Claude 会话首次写入是否遭拦截未证实。

## Requirements

- 能力调用证据和阶段释放必须绑定同一任务、版本和阶段；歧义或缺失时不得推定归属。
- 旧账本保留，无法确认归属的旧证据不能释放新阶段；已有历史记录不得被删除或伪造。
- 保留显式 unaided、未观察到的真实调用的 declared 路径及可恢复的工作区交接。
- 适配所有已声明宿主可支持的事件路径；不能支持的明确说明及安全回退。

## Acceptance Criteria

- 跳过交接的旧任务调用、新任务不同阶段的调用均不能释放当前阶段；匹配调用可释放。
- 多次调用、不同文档顺序、版本变化和多任务歧义不能造成错误归属。
- 旧证据保留且不能被新阶段消费；合法的 unaided 和 declared 路径可用。
- 正常工作区交接、恢复、批准核对、失败和并发场景不丢失证据。
- 增加可复现的回归验证，并更新实际行为及用户操作文档。

## External Facts

- Depends on external facts: yes
- Source: https://code.claude.com/docs/en/hooks
- What it settled: Claude Code 的开始与完成事件文档包含 session_id 和 tool_use_id；真实宿主是否按此投递仍需验证。

## In Scope

插件能力记录、阶段上下文、门禁、审批、交接及其测试和文档。

## Out of Scope

强制选择具体 Skill；把 hook 变成防止任意 shell 写入的安全沙箱；推断未记录的历史调用。

## Risks / Deferred Items

宿主事件缺少阶段信息，必须通过显式阶段上下文解决；宿主真实会话需要单独验证。改变早期允许跨阶段队列的决定。

## Open Questions

无。用户确认同时修复任务和阶段、保留旧证据并保留 unaided。