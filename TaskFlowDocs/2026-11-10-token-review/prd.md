# 审视 TaskFlow 流程中的不合理环节和 Token 开销
> Task version: v2
> Status: in_progress

## Goal

排查 TaskFlow 流程、工具引导及相关记录中不合理或浪费 Token 的环节，并在验证有效后修复或精简

## Task Kind

- Kind: capability

## Background / Confirmed Facts
- 历史会话中，同一任务的实现后归档、验证结果补充和 CI 状态复核可能产生多轮交互；工具调用次数不能直接换算成 Token，也不能仅凭次数断言步骤无用。
- 用户要求同时检查 Todo 重复合并、子 Agent 成本及文档历史重复等方向；与 TF-20260919-90797c、TF-20261011-e27329 重叠，应保留各自记录并对齐边界。

## Requirements
- 继续系统检查任务入口、规划、审核、实现、验证、归档与工具引导中的流程及上下文成本，先以事实定位再提出轻量改进。
- 与 TF-20260919-90797c 一并进行少量同题对照，分别观察主线上下文、包含子 Agent 的总 Token、耗时和结果质量；单独对照外部搜索倾向，不以小样本推断普遍规律。
- 与 TF-20261011-e27329 一并抽样核实文档历史和语义重复，只考虑修正当前模板或规则，不改写已有归档。
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
