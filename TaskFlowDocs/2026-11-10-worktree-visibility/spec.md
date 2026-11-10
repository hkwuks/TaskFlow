# Spec — 让插件和桌面应用中的用户能够清楚获知 Agent 创建的 worktree
> Task version: v2

## Objective and Success Criteria
- 用户在关键时刻得到任务工作区的实际路径与分支或 detached 状态。
- 避免归档、合并后遗漏工作区及本地分支收尾；保留任何未确认可删除的数据。

## Architecture Boundaries and Responsibilities
- TaskFlow 命令读取 Git 信息，提示 Agent 在用户可见消息中报告；宿主自身 UI 不由插件控制。
- 归档阶段不能提前删除未合并分支；合并完成后由当前 Agent 核查并在获得所需授权后清理，检测工具只报告事实。

## Project Structure / Affected Files

## Interfaces, Data Flow, and Contracts
- `task promote` 成功后从目标工作树读取顶层绝对路径和当前分支；非 Git 环境不伪造值。

## Invariants and Compatibility

## Validation and Error Semantics
- 无法识别时明示未知或跳过，不阻止任务提升；兼容已存在的成功输出。
- 合并状态、工作区完整性或用户授权不明时只报告，不强制删除；忽略文件、未跟踪文件与修改分别说明可能遗留的内容。

## Code and Test Constraints
- 验证路径、分支、detached、非 Git 和重复频率，不向最终用户暴露实现细节。

## Design Decisions and Alternatives
- 不将清理放在归档事务里，不自动强制删除脏目录；复用已有 `repository-check` 和安全的 `git branch -d`。

## Open Questions
