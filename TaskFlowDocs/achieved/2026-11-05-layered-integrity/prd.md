# 复杂框架项目中的分层完整性与目标欺骗

> Task version: v1
> Status: completed

## Goal

让 TaskFlow 在复杂框架项目中引导 Agent 做两件互相依存的事：**先理解整体架构与每一层的职责**，从而在粗粒度需求下定位问题真正所属的层；**并且禁止**为了表面上的好结果去修改某一层的中间输出让上层断言通过——那是目标欺骗。

用户 2026-11-05 补充指出：这两件事是一体的。模型若不知道某一层本来该负责什么，就只能从可见症状处下手；而症状所在的位置往往不是失败所属的位置。改中间产物让上层通过，正是「找不到真正的层」之后的退路。

## Background / Confirmed Facts

- **现有 Phase 6 的 8 条验证项全部关于「结果」**（`skills/taskflow/SKILL.md:299-315`），没有一条问「你改了什么才让它通过」。
- **`CODE_STYLE.md` 只说「最小改动」**，不约束改动落在哪一层；`CONTRIBUTING.md` 说 CI 是权威，而 CI 只跑断言、不检测断言是否被削弱。
- **架构理解的载体已经存在但是空的**：`spec.md` 有 `## Architecture Boundaries and Responsibilities` 与 `## Interfaces, Data Flow, and Contracts` 两节（`hooks/task` 的 promote scaffold 每节为空），但只有 large 任务才写 `spec.md`，且没有任何东西检查这两节是否真的描述了每层职责。
- **大/小判据目前偏形态**（`SKILL.md:236-237`）：Large 看「多个模块/文件」「约 30 分钟以上」，Small 看「一个文件」。一个只改一个文件、却改变了一条跨层契约的任务会被判成 small，从而完全绕过架构描述。
- **仓库里唯一接近的纪律**是 `hooks/smoke-test` 里 25 处 `Measured 2026-*` 注释——那是人写断言时的做法，不是对 Agent 的约束。

**外部证据**（2026-11-05 调研）：
- SpecBench（arXiv 2605.21384）：每个前沿 agent 都刷满可见测试套件而作弊依旧；代码量每增 10 倍，visible 与 held-out 通过率差距增加 28 个百分点。
- EvilGenie（arXiv 2511.21654）：Codex 与 Claude Code 均观察到明确 reward hacking；**held-out tests 收益很小，test-file edit detection 与独立判断者才有效**。
- Specification Self-Correction（arXiv 2507.18742）：模型 50-70% 会利用有缺陷的 spec；让模型先审视 spec 自身的漏洞可降幅 92%——支持「把架构契约写清楚」而非「加拦截」的方向。

## Requirements

- **R1**：大/小判据以「是否涉及跨层契约」为首要问题；形态判据（文件数、时长）降为辅助。判 small 需要**同时**满足：不跨层、无外部接口变化、可在单层内验证。
- **R2**：`spec.md` 的架构节必须回答每层「负责什么」「明确不负责什么」「依赖方向」；接口节必须给出每条边界的输入输出契约。
- **R3**：一条**禁止性**规则写在 Phase 5：失败必须修在失败所属的层。为让下游检查通过而修改中间产物属于目标欺骗。需要改变中间层行为时，先改该层自己的验收标准与测试。
- **R4**：Phase 6 增加第 9 条验证项：本次改动是否触碰了中间层产物以满足下游检查。
- **R5**：落点是 `skills/taskflow/SKILL.md` 与 `skills/taskflow/references/artifacts.md`——**插件自身行为**。不写 `hooks/templates/`，不新增 hook，不新增命令。
- **R6**：规则靠 Agent 判断执行，不做机械校验（用户 2026-11-05 决定）。

## Acceptance Criteria

- **AC1**：判据段落中，「一个文件」不再能单独把任务判为 small；small 的三个条件缺一不可，且写明了「改一个文件却改变跨层契约」这一反例。
- **AC2**：`artifacts.md` 明确要求架构节包含「每层不负责什么」，接口节包含每条边界的输入输出契约。
- **AC3**：Phase 5 存在一条明确的禁止性规则，措辞不含「建议」「尽量」等软性词。
- **AC4**：Phase 6 验证项由 8 条变为 9 条，第 9 条问的是「改了什么才让它通过」。
- **AC5**：`bash hooks/smoke-test` 仍为 `ALL SMOKE PASSED`；`git diff --check` 干净。
- **AC6**：改动仅限 `skills/taskflow/SKILL.md` 与 `skills/taskflow/references/artifacts.md`；`hooks/templates/` 未被触碰。

## External Facts

- Depends on external facts: yes
- Source: https://arxiv.org/abs/2605.21384
- What it settled: SpecBench 的实测确立了「agent 会刷满可见测试而偏离真实目标」不是假想风险，且差距随代码规模急剧放大——这支撑了把规则写成禁止性而非建议性，也支撑了「跨层任务必须写架构契约」的判据收紧。
- Source: https://arxiv.org/html/2511.21654v1
- What it settled: EvilGenie 对 Codex、Claude Code、Gemini CLI 的实测显示 held-out tests 收益很小、test-file edit detection 与独立判断者才有效。这直接否定了方案 B（hook 拦截测试改动）的有效性假设，支持选择「写清契约 + 靠模型判断」。

## In Scope

- `skills/taskflow/SKILL.md`：Phase 3 判据、Phase 5 禁止规则、Phase 6 第 9 条。
- `skills/taskflow/references/artifacts.md`：Spec outline 的架构与接口节要求。

## Out of Scope

- `hooks/templates/*`——那是发给别人仓库的建议，用户已明确否决（2026-11-05）。
- 任何 hook 逻辑改动、任何新命令。
- 改动目标分类规则（`TF-20261105-77051f`，另一条 Todo）。
- 本仓库自己的 `CONTRIBUTING.md` / `CODE_STYLE.md`。
- 给 `spec.md` 增加自动校验。

## Risks / Deferred Items

- **风险：规则写了但被无视。** 缓解：Phase 6 的自述检查（R4）让它至少在验证阶段被问一次；若仍被无视，再按实例设计机械检查，而不是凭空虚设拦截。
- **风险：判据收紧后 small 任务变少、开销变大。** 缓解：small 仍可省 `spec.md`，只是必须真正「不跨层」；判据附带反例，避免过度归类。
- **延后**：若平台改为 squash-only 或引入独立 review agent，检测手段需要重估。

## Open Questions

无阻塞问题。
