# Plan — 调查 Codex 中工具引用机制的引导效果
> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`、`skills/taskflow/SKILL.md`。
- `hooks/prompt-reminder`、`hooks/session-start`、`hooks/summarize-state`、`hooks/capability-gate`、`hooks/hooks-codex.json`、`evals/README.md`。
- 原始用户案例：Codex 聊天 `Find remaining TODOs`，任务回合 01a1c328-ed5e-7133-84a8-da433fdf0b76，及随后的用户质询回合。
- https://developers.openai.com/plugins/concepts/skills ；https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra ；https://learn.chatgpt.com/docs/hooks 。

## Related Tasks

- 来源 Todo TF-20261110-a56e72；依赖已验收、已归档但尚未合并的宿主能力对齐 PR #130，基线 `76bcfea`；不修改已归档任务。
- TF-20261110-84d1a9 关注整个流程和 Token 优化；此任务只处理已观察到的能力使用引导缺口，不重复全面审计。

## Skills / Tools Used

- [PRD] Declared `agent-skills:debugging-and-error-recovery` — purpose: 从真实会话重建失败并复现提示缺口；outcome: 已读取技能和事件实现、核实合成事件；incorporated: 将事实与根因假设分开。
- [Research] `openai-docs` — purpose: 核实 Codex Skill 和事件机制；outcome: 已查阅官方技能、上下文和 hook 文档；incorporated: 按需加载、限量提示及事件时机约束。
- [Spec] Unaided — none applied; considered: architecture and design specification.
- [Plan] Unaided — none applied; considered: work breakdown and task decomposition.
- [Test] Unaided — none applied; considered: testing strategy.

## Preconditions

- 工作区：`D:/WorkSpace/Agent/TaskFlow/.worktrees/2026-11-10-codex-tool-guidance`；不更改 digdig、用户全局配置或现有文件。
- 按用户要求先调查，再一次提出三个依赖有序的问题及建议；完成 PRD / Spec / Plan 审核并获得用户批准后才实施。

## Plan Review

- Verdict: sound
- Coverage: 验收 1 由 Step 1 的会话和事件核查覆盖；验收 2 由 Step 2 的入口、规划提示和 promote 输出覆盖；验收 3 由 Step 3 的 CI、条件允许时的真实行为验证及限制报告覆盖；验收 4 由 worktree 边界与 PR #130 依赖检查覆盖。覆盖范围明确不包括绕过 promote 后的任意同轮 shell 写入。
- Verifiability: 分别测试无任务、planning、其他状态、无关仓库及非匹配事件；单次 promote 输出一次，真实调用和真实模型行为单独标记，离线 `evals` 不冒充模型测试。所有行为通过现有跨宿主输出形状及三系统 CI 检查，无法运行的真实宿主列明。
- Layer ownership: 改变现有提示和 promote 正常输出，因为它们负责相应决策时机；不写能力证据、不篡改任务产物或评估标签。更新先前要求 planning 静默的测试属于改变已批准提示契约，而非绕过检查。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-10 13:19 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 复盘案例并确定设计
- Goal: 确认现有流程、可观察事件、用户对负担及验证的边界。
- Verification: 原始会话、真实脚本的合成事件、官方契约和现有测试。
- Rollback: 只更正任务文档，不改变全局配置。
- Status: done

### Step 2 — 实施获批的轻量引导
- Goal: 按决策改造最少的提示与事件接线，保持跨宿主一致和非阻断。
- Files: `hooks/prompt-reminder`、`hooks/task`、必要的 `hooks/smoke-test` / Windows smoke 与 `skills/taskflow/references/runtime.md`。
- Acceptance: 入口、planning 和成功 promote 分别有简短按需指导；其他状态保持既有行为，无新增每次工具调用的进程或状态存储。
- Verification: 测试状态和不同事件、空/无关仓库、planning 到 in_progress 的切换、成功/失败 promotion 和单轮重复；覆盖五宿主的既有事件配置；先证实旧 planning 静默断言需要更新。
- Rollback: 回退本任务变更，不触及用户数据。
- Status: in_progress

### Step 3 — 验证、评估及交付
- Goal: 使用 CI 验证各平台；在可行范围比较真实模型行为并注明限制。
- Verification: CI、Skill 验证、差异检查、必要的受控模型测试。
- Rollback: 验证不通过则保留草稿 PR，不报告达标。
- Status: pending

## Checkpoints

## Verification / Review

- 修改层级是 `hooks/` 与 `skills/taskflow/`，影响使用该插件的各仓库；不改仓库模板或用户全局配置。
- PR 模板 `.github/pull_request_template.md`：Summary 对应 digdig 案例和提示改动；TaskFlow traceability 对应本任务、范围及 `hkwuks/TaskFlow:main`；Verification 对应 CI、diff 和 Skill 验证；Review boundaries 对应敏感信息、独立任务范围、前置 PR #130 和真实模型验证限制。先开草稿，待 CI 与文档收尾后再转待审核。

- `hooks/prompt-reminder` 对本工作树 `planning` 状态的 `UserPromptSubmit` 直接调用无输出；`hooks/summarize-state` 确实报告一项 planning 任务。该项是合成 hook 测试，不证明原始 digdig 会话收到何种系统消息。
- 原始 digdig 回合先读取规则、检索部分代码并创建 worktree，再以 Python 批量写出三个任务文档；当时 Agent 自述未调用计划审核、调试能力或 `hooks/task`，用户指出方案不足后才修正。这是已观察的流程与产物，不是模型内部原因。
- 仓库 `evals/README.md` 说明 eval 为无模型、无网络的离线规则和工件测试；即使全部通过，也不能证明真实 Codex 的能力选择发生变化。
- 2026-11-10 用户批准 v1；实施前以隔离夹具确认 planning 提示缺失，实施后验证 planning 提示和既有 in_progress 分类提示、无任务入口及只读例外、ready 静默、成功/失败 promote 输出；以上是 Windows Git Bash 的定向测试，不代表真实 Codex 采纳。
- `python evals/runner.py`：6 项通过（离线规则，不执行模型）；`quick_validate.py skills/taskflow` 通过；`git diff --check` 通过。
- 配置静态核对：Claude Code、Codex、CodeBuddy、dsh、Trae 的 `UserPromptSubmit` 均指向共享 `prompt-reminder`；Windows 专项 smoke 增加原生路径和 promote 输出检查。真实宿主和真实模型采纳仍未验证。

## Change Log

- 2026-11-10：用户验收宿主对齐范围；从其已归档分支建立独立 worktree，定位真实案例并开始调查。尚未实施本任务。
- 2026-11-10：用户确认非阻断关键时机提示、按宿主可用能力选择、CI 加条件允许的真实行为验证；形成 v1 方案并等待审批。

## Follow-ups

## Version History

- v1 — planning.
