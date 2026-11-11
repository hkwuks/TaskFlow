# Spec — 审视 TaskFlow 流程中的不合理环节和 Token 开销
> Task version: v2

## Objective and Success Criteria
- 以脱敏事实识别高成本流程，实施可证明不损害交付质量的最小改进。

## Architecture Boundaries and Responsibilities
- 会话证据提供观察；TaskFlow 规则和脚本是实际改进位置；个人数据不进入任务文档。

## Project Structure / Affected Files

## Interfaces, Data Flow, and Contracts
- 输入为 Todo 条目、现有相似项、会话与任务状态；重叠比较必须保留不同需求和用户决策。
- 针对纯中文目标，将连续常用汉字切分为相邻双字候选，与现有 ASCII token 的集合比较并保留现有最低交集、提示上限及只提示不合并的行为；不声称语义去重。

## Invariants and Compatibility

## Validation and Error Semantics
- 对照试验报告观察条件、可获得的计量数据、缺失数据和质量评价；样本不足时不宣称普遍节省或因果关系。
- 工作流优化维持验证、用户决策和信息可追溯性；候选方案须独立记录成本与收益。
- 以可比较样本验证结果；缺失数据不能变成精确节约结论；去重不静默合并不同事项。
- 覆盖中文改写、相近但不相关、英文、中英混合和重复词，确保与现有候选提示及自动化一致；稀有扩展汉字若不受支持须明示。

## Code and Test Constraints

## Design Decisions and Alternatives
- 复用现有 intake 候选提示与分类，不新建每次调用都触发的重型监控。

## Open Questions
