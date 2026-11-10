# 调查 Codex 中工具引用机制的引导效果
> Task version: v1
> Status: completed

## Goal

调查 digdig 新会话中工具引用机制对 Codex 的引导效果不佳的问题，并确定可验证的改进方式

## Task Kind

- Kind: defect

## Background / Confirmed Facts

- 2026-11-10 用户指出 digdig 的 Codex 会话：三个修复任务在初步检索后被批量写成简略 PRD/Spec/Plan，缺少足够调查和计划审查；用户追问后，Agent 确认没有调用适用的调试、规划能力，也没有如实记录 unaided。会话标题 `Find remaining TODOs`，问题发生在 01a1c328-ed5e-7133-8b55-3a288da0e3c8 回合；证据来自聊天记录和后续用户追问，不能推断模型内部原因。
- `hooks/prompt-reminder` 在唯一任务为 `planning` 时不输出现有 in-progress 提醒；隔离调用本任务的真实脚本和状态复现了空输出。`UserPromptSubmit` 不会在同一轮内每次命令后重新触发，所以即便为 planning 添加提示，也不能单独证明一次长回合中的能力选择被纠正。
- 宿主能力对齐 PR #130 修复能力事件接线和真实但不可观测调用的声明；它不等于模型选择了恰当能力或计划质量已合格。

## Requirements

- 在当前需要时，用轻量、不阻断的指导帮助 Agent 基于现有可用技能、工具、MCP、Agent 的描述判断适用能力；选择和实际调用按真实情况区分，不强迫每阶段调用、不虚构记录。
- 优先覆盖初始开发请求、规划及同一轮执行中的实际漏点；无需为简单任务增加固定重流程或全量工具清单。用户明确不接受阻断正常开发或为简单需求引入沉重机制。
- 对 Claude Code、Codex、CodeBuddy、dsh、Trae 按已支持事件和实际输出逐项核对；不能把未知、合成测试或不可测标作真实宿主通过。
- 区分提示已送达与 Agent 实际选择、实际调用和产物质量；客观评估改动是否带来改善，不能以字符串测试宣称行为已改善。

## Acceptance Criteria

1. 真实案例及当前各事件触发范围、跨工作树和同回合限制有可复核证据；不能把猜测写成根因。
2. 选定的轻量引导在相应宿主契约和任务状态下可靠输出；普通对话、只读工作、明确无需能力的工作不被阻断，控制每次增加的上下文和启动成本。
3. 自动测试覆盖目标状态、无关请求、事件缺失、任务切换和已支持宿主差异，纳入 CI；有条件时评估实际 Codex 行为，无法实测明确报告。
4. 不改变用户现有安装和配置，不强制开启新会话；#130 未合并前，此任务的交付需注明对已验收宿主对齐结果的依赖。

## External Facts

- Depends on external facts: yes
- Source: https://developers.openai.com/plugins/concepts/skills
- What it settled: Codex 先看到技能名称与描述，再按需求或明确调用加载全文；声明可用不等于实际调用。
- Source: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- What it settled: 技能描述过多或过长会挤占上下文，按需加载和简短的触发条件有助于控制负担。
- Source: https://learn.chatgpt.com/docs/hooks
- What it settled: `UserPromptSubmit` 与工具前后事件触发时机不同，不能将下次用户提示当作同一轮中的提醒。

## In Scope

TaskFlow 项目内流程指导、必要的事件接线和测试；用户所述 Codex 行为及已支持宿主覆盖。

## Out of Scope

强行改变全局 Codex 设置、重启用户会话、同步阻断开发、修改 digdig 或安装用户环境中的技能。

## Risks / Deferred Items

提示属于概率性引导，合成测试不证明模型会遵循；依赖 PR #130，最终 PR 基线应在其合并后重新确认。

## Open Questions

无。用户确认：关键时机非阻断提醒、从宿主当前可用能力中按需选择、CI 验证事件与边界且真实行为条件允许时再验证。
