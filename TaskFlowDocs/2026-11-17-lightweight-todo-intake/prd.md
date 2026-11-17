# 简化 Todo 录入
> Task version: v1
> Status: checking

## Goal
只要求添加 Todo 时记录后结束，不做相似项或任务调查。

## Task Kind
- Kind: internal

## Background / Confirmed Facts
intake 目前扫描并提示相似目标；Skill 要求在选择任务前检查重叠。用户选择独立修复，保留 token-review 历史、精确相同目标的拒绝和确定性 ID。

## Requirements
本地和远程仅录入请求写入后结束；本地 intake 不进行近似比较；开始工作时仍检查重叠。保留精确重复、ID 冲突及写入失败保护。

## Acceptance Criteria
中英文相似目标成功录入且无相似提示；精确重复仍拒绝且文件不变；Skill 清楚区分录入和开始工作；相关回归通过。

## External Facts
- Depends on external facts: no
- Why not: 用户决策和本仓库 `hooks/task`、`skills/taskflow/SKILL.md` 与 `hooks/smoke-test` 决定行为和验证。

## In Scope
插件 Skill、intake、相关测试和文档。

## Out of Scope
Issue 计划存储、修改已有任务历史、取消精确重复保护。

## Risks / Deferred Items
录入时不再提示近似重复；开始工作时仍须判断重叠。

## Open Questions
无。
