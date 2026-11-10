# 让插件和桌面应用中的用户能够清楚获知 Agent 创建的 worktree
> Task version: v1
> Status: planning

## Goal

让插件和桌面应用中的用户能够清楚获知 Agent 创建的 worktree 所在路径及对应分支，并研究宿主可见性与展示方式

## Task Kind

- Kind: capability

## Background / Confirmed Facts
- 当前 skill 要求 Agent 使用 `pwd` 和分支命令确认隔离；这不保证用户在插件或桌面会话中看到路径。

## Requirements
- 创建或进入任务 worktree 后，向用户清楚展示实际绝对路径和对应分支；只在关键时机展示一次，避免重复提示。
- 普通分支、detached HEAD、非 Git 目录须如实显示，不编造分支。

## Acceptance Criteria
- 用户可通过宿主可见消息获得实际路径和分支；自动化分别覆盖 worktree、普通仓库、detached 和非 Git 情况。
- 不因提示阻断开发或引入强制重启；无法验证的宿主显示边界如实记录。

## External Facts

- Depends on external facts: no
- Why not: `hooks/task` 和 `skills/taskflow/SKILL.md` 定义当前入口及工作区流程；宿主展示效果另列实际验证而不作跨宿主保证。

## In Scope
- TaskFlow 插件的任务入口提示、用户可见沟通指导及必要测试。

## Out of Scope
- 修改宿主桌面 UI、用户全局配置或改变 worktree 位置。

## Risks / Deferred Items

## Open Questions
