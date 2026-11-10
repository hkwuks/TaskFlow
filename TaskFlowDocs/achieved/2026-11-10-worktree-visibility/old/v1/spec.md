# Spec — 让插件和桌面应用中的用户能够清楚获知 Agent 创建的 worktree
> Task version: v1

## Objective and Success Criteria
- 用户在关键时刻得到任务工作区的实际路径与分支或 detached 状态。

## Architecture Boundaries and Responsibilities
- TaskFlow 命令读取 Git 信息，提示 Agent 在用户可见消息中报告；宿主自身 UI 不由插件控制。

## Project Structure / Affected Files

## Interfaces, Data Flow, and Contracts
- `task promote` 成功后从目标工作树读取顶层绝对路径和当前分支；非 Git 环境不伪造值。

## Invariants and Compatibility

## Validation and Error Semantics
- 无法识别时明示未知或跳过，不阻止任务提升；兼容已存在的成功输出。

## Code and Test Constraints
- 验证路径、分支、detached、非 Git 和重复频率，不向最终用户暴露实现细节。

## Design Decisions and Alternatives

## Open Questions
