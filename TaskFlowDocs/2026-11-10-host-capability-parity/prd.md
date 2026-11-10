# 已支持宿主的 TaskFlow 能力对齐
> Task version: v1
> Status: planning

## Goal
核实并修复 TaskFlow 在已支持 Agent 宿主中的能力接线和流程差异，让真实支持的能力可用、不可观察的能力有诚实且可用的处理方式。

## Background / Confirmed Facts
- 用户实际在 Codex 中使用 Plan 能力后，审批因能力证据未释放而失败；不能将真实调用伪记为 unaided。
- 当前 Codex 的 `PostToolUse` 没有连接 `capability-evidence`；OpenAI 官方文档列出 MCP 工具的该事件，Skill 加载不应未经验证就视为可观察。
- dsh 使用小写工具名和自身事件参数；当前阶段能力门和记录器没有接入，基础工作区守卫已单独接入。
- 提醒、外部证据、基础工作区保护等能力在宿主间有已知未接线或未验证项；不能以不支持掩盖未调查。

## Requirements
- 按能力与宿主逐项核对声明、接线、实际事件、可观测性及验证等级；能通过可靠宿主接口承载的能力应对齐。
- 区分宿主直接观测的调用、不可观测但真实发生的使用和确实未使用；不得将人工声明伪装为宿主观测或将真实使用伪记为 unaided。
- 在必要时修复共享处理、宿主接线和审批对账，保留阶段身份、工作树隔离、用户审批和证据来源；不安装全局配置、不强制新会话。
- 为差异和回归增加有意义的自动测试；可行时验证真实宿主，无法验证时明确记录边界。
- Codex 工具引用引导问题 TF-20261110-a56e72 在本任务完成后单独处理，不把已确认的证据接线缺口当作该问题的已证实根因。

## Acceptance Criteria
1. 五宿主能力矩阵逐项区分已接线、未接线、不可支持与尚未验证，并给出依据。
2. 有明确事件契约的缺口得到修复，正常调用、拒绝、失败及跨工作树行为得到针对性验证。
3. Codex 中实际使用但不可自动观测的能力可被如实记录与审批，不借用伪造观测或 unaided。
4. 用户现有配置和数据不被更改，CI 覆盖相关行为，真实会话未验证项明确列明。

## External Facts
- Depends on external facts: yes
- Source: https://learn.chatgpt.com/docs/hooks
- What it settled: Codex 工具事件覆盖 MCP，提供 `tool_name` 和 `tool_input`；不同路径的观测范围须分别判断。
- Source: https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/tool-skill/README.md
- What it settled: dsh 的模型工具名为 `skill`，用户显式调用也可能直接注入内容而不经过该工具。

## Risks / Deferred Items
Codex skill 加载不一定对应独立 hook；异步提醒不是阻断权限。README 工具引用引导效果和基础守卫真实宿主验证需按相关任务跟进。
