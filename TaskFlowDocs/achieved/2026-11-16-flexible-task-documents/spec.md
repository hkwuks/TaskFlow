# Spec — 放宽 TaskFlow 文档内容约束
> Task version: v1

## Objective and Success Criteria

在保留 TaskFlow 必需事实及生命周期安全检查的前提下，让工具产生的有用章节、说明和示例进入现有权威文档。成功条件以 PRD 六项验收为准。

## Architecture Boundaries and Responsibilities

- `skills/taskflow/` 负责规定最低内容、可扩展内容和保留结构，不替外部技能定义完整模板。
- `hooks/task`、`hooks/completion-gate`、`hooks/approval-check`、`hooks/version`、`hooks/archive` 等各自拥有解析或修改任务文档的边界；先追踪实际调用与写入再选择共享或局部修复。
- 外部技能输出经审阅归入既有 PRD、Spec、Plan 或 reference，不形成冲突的任务事实源；保留对具体任务有用的契约、边界、示例和验证依据，不为匹配骨架而机械压缩。

## Project Structure / Affected Files

检查上述 hooks 及其调用者、`hooks/smoke-test`、Windows 启动器测试、`skills/taskflow/SKILL.md` 和 `skills/taskflow/references/artifacts.md`；根据调查确定实际改动，保持中英文说明一致。

## Interfaces, Data Flow, and Contracts

输入是含必需 TaskFlow 元数据及附加 Markdown 的任务文档。生命周期读取器仅将有效结构视为工作状态；写入器更新目标字段时保留其他内容。受支持围栏中的文本是示例，不产生字段、步骤或待办。无法判定的格式不得静默放行。

## Invariants and Compatibility

保留现有审批、版本、真实待办和步骤检查，不更改历史数据或主动转换用户内容。不引入未经授权的兼容层或依赖。

## Validation and Error Semantics

比较含与不含附加内容的等价文档；测试额外章节、围栏内伪结构、围栏外真实待办、未闭合围栏与重复保留结构，以及修改和归档后的内容完整性。明确拒绝无法安全判定的输入。用简单任务与复杂任务样例审查是否保留实施和验收所需的内容；不得用行数或标题数代替内容判断。

## Code and Test Constraints

遵循 `CODE_STYLE.md`，shell 使用仓库既有工具；先用失败测试证明具体误判，再修改责任层。运行针对性测试、适用的 Windows 测试和 `git diff --check`，必要时运行完整 smoke。

## Design Decisions and Alternatives

优先复用现有解析与测试机制；不以放松所有检查或仅新增流程标记代替功能修复。围栏语法和跨读取器共享方式以实际调用链和测试为依据，避免未核实地引入新框架。

## Open Questions

具体实现边界将在 Step 1 的代码与测试调查后收敛；若需改变上述契约则先回到用户确认。
