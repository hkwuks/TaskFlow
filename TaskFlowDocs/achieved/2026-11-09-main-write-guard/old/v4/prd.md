# 防止开发任务修改基础工作区
> Task version: v4
> Status: in_progress

## Goal
防止 TaskFlow 开发任务跳过独立 worktree 并直接修改基础工作区，覆盖 digdig 的实际事故。

## Background / Confirmed Facts
现有 promote 在基础工作区拒绝，但模型可以跳过 promote；每轮提示不是硬门禁。现有 capability-gate 针对阶段文档而非普通源码。Codex、Claude Code、CodeBuddy、dsh 和 Trae 的工具事件契约不同。

## Requirements
- 对支持且能识别文件目标的编辑事件，在基础工作区的源码或任务文件写入前拒绝，并指明任务 worktree 的建立方式。
- 不影响任务 worktree 内的正常写入、非 TaskFlow 仓库、只读操作与 Todo intake；例外须能被验证，不能依赖模型自报。
- 对所有声明支持的宿主核查并接入可承载能力，说明未接线、未验证和不支持的证据；不可静默降级。
- 明确 shell、交互输入、特殊工具路径与未受信 hook 无法被该门完全保护；不将命令关键词识别当作安全边界。

- 宿主权限隔离作为可选增强；不强制终止实施、切换会话或修改用户全局配置。只有宿主支持、用户选择且实测通过才报告隔离生效。
- shell 操作前后检测基础工作区变化，非阻断地提示用户核对；不得自动回滚或把并发变化归因于当前 Agent，原有工作区改动不得误称新变化。
- 验证真实宿主上 apply_patch、PowerShell 和 Python 对基础工作区拒绝、任务 worktree 放行；明确 MCP 和其他入口的独立权限边界。

## Acceptance Criteria
1. 基础工作区普通源码编辑被可支持的文件编辑 hook 拒绝；任务 worktree、非 TaskFlow 仓库以及指定例外正常工作。
2. 相对、绝对路径、跨工作树目标、多文件 patch、Windows 路径均有回归测试；拒绝发生在写入前。
3. 宿主矩阵逐项给出事件、支持依据和实际验证级别；有条件时在真实 Codex 测试通过与拒绝，失败或不可用如实报告。
4. 不丢失现有文件，不自动撤销主工作区并发改动。
5. 可选隔离仅在实际生效并验证后报告；shell 后变化提示不阻断、不覆盖或回滚，不将已有状态误称新变化。

## External Facts
- Depends on external facts: yes
- Why: 各宿主 hook 事件契约、输出及工具覆盖。
- Source: https://learn.chatgpt.com/docs/hooks
- What it settled: Codex PreToolUse 覆盖 Bash 和 apply_patch，特殊工具路径可能不经过 hook。

## In Scope
防护 hook、宿主接线、规则文档与验证。旧版能力记录的全面对齐由 TF-20261109-293987 单独处理。

## Out of Scope
解析所有 shell 命令、自动撤销修改、发布。

## Risks / Deferred Items
常规 shell 写入可由经验证的宿主权限阻止，但 Windows NTFS 硬链接在 MXC 夹具测试中仍可改变基础文件；MCP 等绕过 hook 的工具需独立验证；发布时的编辑可能被拦截；可验证的发布例外已按用户要求推迟至 TF-20261109-ccbb96。

## Open Questions
计划审批后实施；具体宿主接线必须以各自事件契约核实。
