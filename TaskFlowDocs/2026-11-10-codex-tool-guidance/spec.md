# Spec — 调查 Codex 中工具引用机制的引导效果
> Task version: v1

## Confirmed boundary

现有规划阶段 `UserPromptSubmit` 无能力提示；该事件只发生在用户提交时，不能代替同一轮中工具事件。前次 digdig 实例确有遗漏，但现存聊天记录不证明哪一条系统消息被模型注意或忽略。

## Design

复用两个现有触点，不增加后台观察器、定时器或每次工具调用的 hook：

1. `hooks/prompt-reminder` 的现有无活跃任务入口提示追加一条简短指导，明确仅适用于进入开发流程的请求；已有的只读例外不变。唯一活动任务处于 `planning` 时，随 `UserPromptSubmit` 输出任务摘要和同一条简短指导；`ready`、多活动任务、非 TaskFlow 仓库与不适用事件保持原有行为。
2. `hooks/task promote` 成功后紧接成功消息输出一条简短指导，提醒在编写 PRD/Spec/Plan 前根据当前宿主实际可用能力、任务复杂度和阶段选择可用的 Skill、工具、MCP 或 Agent；真正不适用时可 unaided。这个现有命令输出可在用户消息之后、同一轮规划开始时送达，没调用 promote 时不声称产生了提醒。

两处均不硬编码第三方名称，不要求全量枚举或强迫调用，不新增同步前置拦截。指令只建议选择，不记录一次调用、不绕过计划审核；现有能力观测和声明仍各自负责真实来源。提示是否被模型采纳是待验证的行为，不是 hook 的保证。SessionStart / UserPromptSubmit、`task promote` 的现有五宿主接入仍由各宿主运行方式决定，不安装全局配置或重启会话。

声明是当事 Agent 对确实使用能力的记录，自动事件是宿主观测；候选清单、自动事件和计划质量为不同事实。实证应对提示文本、状态与宿主契约使用自动测试，实际模型行为另用受控对照评估；缺少真实模型测试时不得声称采纳率提升。

当前约束：单次长回合内如果 Agent 绕过 `task promote`、忽略最初的提示或宿主没有执行 hook，TaskFlow 不保证能在任意 shell 或 Python 写入前纠正；这里不对 shell 命令做关键词归因，也不以阻断开发换取更强控制。

## Objective and Success Criteria

## Architecture Boundaries and Responsibilities

## Project Structure / Affected Files

## Interfaces, Data Flow, and Contracts

## Invariants and Compatibility

## Validation and Error Semantics

## Code and Test Constraints

## Design Decisions and Alternatives

## Open Questions
