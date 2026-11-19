# Spec — 多 Todo 共同处理
> Task version: v2

## Objective and Success Criteria
一个任务工作区和文档关联多个已有记录，独立验收和更新。

## Architecture Boundaries and Responsibilities
Skill 定义选择与验收；生命周期 hooks 维护关联及本地状态；远程 Todo 层负责逐 Issue 同步与失败恢复；任务文档记录逐项事实。

## Project Structure / Affected Files
`skills/taskflow/`、`hooks/task`、`hooks/archive`、`hooks/remote-todo*` 和关联测试；按调用链审查其他消费者。

## Interfaces, Data Flow, and Contracts
建立可验证的多项关联与逐项结果，保留来源身份；状态变更与归档须以明确的单项结果为依据。具体命令及持久化格式在实施前沿现有调用链选择，避免隐式批量完成。

## Invariants and Compatibility
不创建汇总 Todo；不丢失条目正文；单项路径继续正确；不为未经确认的条目标记完成。未完成条目可继续追踪，不能指向不存在的活跃目录。

## Validation and Error Semantics
先验证所有本地输入；远程逐项操作并报告已成功、失败和不确定项，禁止假称原子；重试前核实结果。

## Code and Test Constraints
覆盖本地、远程、混合、部分完成、失败、归档及重开，复用现有测试设施；不新增依赖。

## Design Decisions and Alternatives
每项状态独立，任务工作区共享。具体接口须沿现有命令与恢复机制设计，并在实施记录中说明。

## Open Questions
无。

## 调用链核查（2026-11-19）
- `hooks/task` 的 `findsec` 以任务路径只返回第一条；`state` 因而只更新首项。
- `hooks/archive` 只压缩首条匹配记录并迁移其正文；直接增加同路径条目会遗留指向已移动目录的记录。
- `hooks/reopen` 只更新首条状态，但替换所有匹配路径；会让其他已完成条目看起来重新关联活跃任务。
- `remote-issue` 是单行单 Issue；`remote-todo`、`remote-todo-local-list`、`remote-todo-promote`、`remote-todo-to-local`、`remote-todo-reattach`、`remote-todo-reattach-todo`、`remote-todo-migrate` 等均依赖这一约束及现有 detach 标记。不能只让文件支持多行：去重、迁移和重连仍会读错。
- 部分完成需要同时定义未完成项在任务目录归档后的引用、重开时是否只恢复被选中条目，以及远程成功而本地失败时逐项恢复。实现前必须在所有路径上保持身份和可恢复性。

## v2 用户选定的实现
一个现有 Todo 为唯一主关联；其他项目只在 Plan 的关联清单按 ID 或远程来源和 Issue 编号引用，不写相同 Task 路径。按 ID 更新未提升的本地条目；远程 Issue 使用现有逐项 stage。任务归档之前，主关联必须已经验收完成；其余未完成项继续留在原后端。只变更明确指定的条目，保留正文。远程结果不确定时沿用现有恢复机制。
