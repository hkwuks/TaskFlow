# 多 Todo 共同处理
> Task version: v2
> Status: completed

## Goal
用户指定一批已有 Todo 时，在同一分支和 worktree 中处理，复用一套任务文档，不新建汇总 Todo。

## Task Kind
- Kind: capability

## Background / Confirmed Facts
现有任务状态查找和归档只处理第一个关联条目；远程关联文件只能容纳一个 Issue。

## Requirements
- 共用 PRD、Spec 和 Plan，记录每个已有 Todo 的来源、关联、验收和结果。
- 其他本地 Todo 通过按 ID 指定的操作更新，远程 Issue 通过已有按 Issue 操作更新；仅已验收项目标记完成，未完成项目保留原身份和可继续处理的状态。
- 不因批量处理新建汇总 Todo；归档按各项实际结果及用户要求进行。
- 避免远程部分成功导致误报，保留恢复信息。

## Acceptance Criteria
- 选择一个现有 Todo 为主关联；其他本地 Todo 或远程 Issue 在 Plan 按身份逐项记录，不创建汇总 Todo。
- 已完成与未完成混合时，状态和归档结果准确，原始记录不丢失。
- 远程写入失败或不确定时不误报成功，保留可检查和恢复的状态。
- 单项现有流程保持正确，验证关联、状态、完成、归档及重开等受影响路径。

## External Facts
- Depends on external facts: no
- Why not: 修改本仓库任务数据和命令，依据 `hooks/task`、`hooks/archive` 和用户决定。

## In Scope
插件流程、任务关联和生命周期命令及相应测试与文档。

## Out of Scope
下载内容共享专项；已有 Todo 内容与不相关任务。

## Risks / Deferred Items
远程写入非原子；中途失败需要逐项核验。部分完成时共享任务目录的生命周期必须保留未完成项。

## Open Questions
无。
