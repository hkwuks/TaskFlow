# Spec — 能力调用证据归属
> Task version: v2

## Objective and Success Criteria

用可验证的任务、版本、阶段身份绑定新调用；不从队列位置推断身份。

## Architecture Boundaries and Responsibilities

任务工作流在阶段开始时显式设置活动上下文；记录器从工作区及该上下文获取任务、版本和阶段，并在无法唯一确认时不写可用于释放的证据。门禁和审批只消费并核对身份匹配的记录。交接负责隔离、保存和恢复上下文和账本；`repository-check` 只识别并报告明确的 WSL Git 与 Windows worktree 元数据路径错配，不断言进程或会话空闲；工作流文档说明切换及宿主限制。

## Project Structure / Affected Files

`hooks/repository-check`、`hooks/test-worktree-candidates`、`hooks/capability-evidence`、`hooks/capability-gate`、`hooks/task`、`hooks/reuse-worktree`、锁及相关宿主接线（如需）、`hooks/smoke-test` 与交接测试；`skills/taskflow/`、运行时参考及中英文 README 中受影响的说明。

## Interfaces, Data Flow, and Contracts

引入显式阶段上下文命令，写入工作区私有账本，包含任务 ID、版本和阶段；后续调用携带同一身份。阶段切换和新建任务须校验身份及任务状态。仅当运行环境为 WSL 且 Git 候选路径呈现已观察到的 `.git/worktrees/<id>/D:/...` 错配形态时，检查器输出原因和使用 Git for Windows 的 Bash 重试的建议；其他不可访问原因保持未知。写入文档只可消耗与当前任务版本阶段完全匹配且未消费的调用记录；审批逐阶段对账，不再用整版本调用池。Test 的无文档路径执行同样的匹配。具体命令及格式在实施前通过现有调用者、恢复和并发分析确定，不依赖宿主猜测阶段。

## Invariants and Compatibility

历史账本原样保留且不能作为新调用证据；不伪造旧记录的归属。已有审阅历史保留；不要求读取旧数据时创建兼容转换代码。任务与版本切换、恢复和复用不得遗留可使其他任务获释的上下文。显式 unaided 继续独立释放指定阶段；declared 只用于真实但不可观察的调用。

## Validation and Error Semantics

上下文缺失、歧义、过期或损坏时明确提示并拒绝归属或释放；锁保护切换与写入，保留失败现场，不能静默丢弃已有账本。不得将暂未消费的其他阶段证据改写为当前阶段。

## Code and Test Constraints

保持现有 Bash 可移植性、输入校验及失败保护，不新增依赖。先构造失败回归再修复；覆盖旧工作区跳过交接、正确交接、跨阶段溢出、精确匹配、版本、旧记录、unaided、declared、Test、恢复及并发。

## Design Decisions and Alternatives

宿主事件本身不提供阶段身份，不能仅调整 FIFO、依赖调用名称或文档措辞；采用显式上下文及身份核对。取代 `2026-10-17-stage-capability-pairing` 中接受跨阶段消费、按整版本调用池对账的决定。

## Open Questions

无。工作区诊断按用户确认使用明确提示，不添加自动路径转换或兼容逻辑。
