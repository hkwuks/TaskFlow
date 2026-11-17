# Spec — 轻量 Todo 录入
> Task version: v2

## Objective and Success Criteria
单纯记录只写入并报告结果；任务选择仍检查重叠。

## Architecture Boundaries and Responsibilities
Skill 区分只记录与开始工作；本地 intake 负责写入和身份保护；远程 Issue 继续由现有工具负责。

## Project Structure / Affected Files
skills/taskflow/SKILL.md、hooks/task、hooks/smoke-test 及必要的引用文档。

## Interfaces, Data Flow, and Contracts
成功输出仍为 intake OK 和 ID；保留近似候选提示。精确重复和 ID 冲突仍失败且不改文件。只录入不调查待办内容、不进行任务选择或规划。

## Invariants and Compatibility
保持 Todo 格式、确定性 ID、精确重复检查及既有任务历史，不增加兼容层。

## Validation and Error Semantics
保留输入、后端配置和写入错误；远程失败保留既有恢复规则。

## Code and Test Constraints
恢复近似匹配实现及其原有断言；验证中英文相似录入仍有候选，保留精确重复与 ID 回归；验证 Skill 两阶段边界。

## Design Decisions and Alternatives
不增加参数：intake 保留相似项提示；Agent 不因提示提前调查待办内容。开始工作时仍进行人工重叠判断。

## Open Questions
无。
