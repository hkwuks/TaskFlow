# 审视 TaskFlow 流程中的不合理环节和 Token 开销
> Task version: v1
> Status: in_progress

## Goal

排查 TaskFlow 流程、工具引导及相关记录中不合理或浪费 Token 的环节，并在验证有效后修复或精简

## Task Kind

- Kind: capability

## Background / Confirmed Facts
- 历史会话中，同一任务的实现后归档、验证结果补充和 CI 状态复核可能产生多轮交互；工具调用次数不能直接换算成 Token，也不能仅凭次数断言步骤无用。
- 用户要求同时检查 Todo 重复合并、子 Agent 成本及文档历史重复等方向；与 TF-20260919-90797c、TF-20261011-e27329 重叠，应保留各自记录并对齐边界。

## Requirements
- 分析脱敏历史会话与当前实现，区分直接证据、假设和无法测量的 Token 成本；明确质量、审批与验证的收益和代价。
- 比较新增 Todo 与现有条目，研究避免重复流程的方法，保留不应合并的不同需求。

## Acceptance Criteria
- 可追溯样本、观察结果、可测成本与优化候选，并验证最终改动不损害质量；缺乏对照数据时不宣称量化节省。

## External Facts

- Depends on external facts: no
- Why not: 当前实现与规则位于 `skills/taskflow/SKILL.md`、`hooks/task`，会话记录由用户授权只读抽样；外部事实若影响方案须重新核对。

## In Scope
- TaskFlow 自身流程、工具引导、历史会话和 Todo 去重；保留审批及验证的真实价值。

## Out of Scope
- 使用未经对照的总 Token 数量声称节省；公开个人或项目敏感信息。

## Risks / Deferred Items

## Open Questions
