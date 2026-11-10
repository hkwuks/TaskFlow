# Spec — 在可用的真实宿主会话中验证 TaskFlow 能力对齐及基础工作区
> Task version: v1

## Objective and Success Criteria
- 补齐声明账本直接编辑保护，区分真实宿主观察与合成事件。

## Architecture Boundaries and Responsibilities
- 宿主负责事件分发；`capability-gate` 判断支持的直接编辑；`task declared` 写声明账本。

## Project Structure / Affected Files
- `hooks/capability-gate`、相关测试和任务验证记录。

## Interfaces, Data Flow, and Contracts
- declarations 采用与 evidence、released 相同的直接编辑保护；声明命令保留原语义。

## Invariants and Compatibility
- 不改变账本格式和异步提醒，不新增兼容层。

## Validation and Error Semantics
- 直接编辑被拒绝并提示正确的记录方式；正常声明不被阻止。

## Code and Test Constraints
- 测试声明和旧账本路径、无关路径及声明命令。

## Design Decisions and Alternatives
- 复用现有路径判断，不引入同步快照或全局配置更改。

## Open Questions
- 实际宿主和提示的可观察范围以探针结果为准。
