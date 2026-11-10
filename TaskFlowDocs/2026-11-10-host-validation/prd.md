# 在可用的真实宿主会话中验证 TaskFlow 能力对齐及基础工作区
> Task version: v1
> Status: in_progress

## Goal

在可用的真实宿主会话中验证 TaskFlow 能力对齐及基础工作区异步提醒，逐项记录事件与提示是否实际到达

## Task Kind

- Kind: defect

## Background / Confirmed Facts
- `capability-gate` 保护 evidence 和 released 的直接编辑路径，但未涵盖 declarations；已有宿主测试为合成事件。

## Requirements
- 将 declarations 纳入相同直接编辑护栏；合法声明流程继续工作。
- 验证可运行宿主的实际事件、异步提醒和工具引导，区分静态接线、模拟事件、真实事件与用户可见性。

## Acceptance Criteria
- 直接编辑保护与合法声明的针对性回归通过，不宣称拦截任意 shell 写入。
- 可运行宿主按实际事件和提醒分别记录结果，其他宿主或无法观察部分标明待验证。

## External Facts

- Depends on external facts: yes
- Source: https://learn.chatgpt.com/docs/hooks
- What it settled: 先前宿主对齐使用的 Codex 事件契约；实际投递仍须真实测试。

## In Scope
- 插件 hook、相关测试与可运行宿主的非破坏性探针。

## Out of Scope
- 更改全局宿主配置、强制重启会话、阻断式快照。

## Risks / Deferred Items
- 未能观测的异步提示及宿主行为须保留待验证。

## Open Questions
- 哪些宿主可在当前环境中完整观察实际事件和提醒。
