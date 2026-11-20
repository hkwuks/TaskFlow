# 复用工作树时同步目录名称
> Task version: v1
> Status: completed

## Goal
复用工作树后，目录与新任务的 Todo 和分支描述一致。

## Task Kind
- Kind: capability

## Background / Confirmed Facts
仓库约定目录 `.worktrees/<slug>` 和分支 `<type>/<slug>`；现有交接保留证据并支持恢复，但不移动目录。

## Requirements
- 交接前确认空闲并完成安全检查，按目标分支的任务描述确定同级目录名。
- 目标存在时停止且不覆盖；交接中断后能定位工作树并恢复原任务。
- 开始新任务和恢复旧任务时均使用目标分支对应目录；输出最终路径。

## Acceptance Criteria
- 成功交接后目录名称与分支任务描述一致，Git 工作树登记和证据完整。
- 同名冲突不改变原工作树、分支或证据。
- 移动前后注入失败，恢复可还原原任务及路径；保留用户文件。
- 测试覆盖开始、恢复、冲突及中断，使用说明与实际一致。

## External Facts
- Depends on external facts: no
- Why not: 现有交接与验证依据为 `hooks/reuse-worktree` 和 `hooks/test-reuse-worktree`，实际 Git 行为由本地夹具验证。

## In Scope
交接脚本、对应测试和项目内 TaskFlow skill 文档。

## Out of Scope
迁移其他工作树或删除旧分支。

## Risks / Deferred Items
工作树移动可能因 Windows 文件占用失败；应停止并保留恢复信息。

## Open Questions
无。
