# Plan — 在可用的真实宿主会话中验证 TaskFlow 能力对齐及基础工作区
> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers
- `TaskFlowDocs/repository-docs/index.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`
- `hooks/capability-gate`、`hooks/test-host-parity`、宿主 hook 配置

## Related Tasks
- TF-20261110-0c7346；承接已归档宿主能力对齐 v1 和基础工作区防护。

## Skills / Tools Used
- [PRD] Declared `agent-skills:debugging-and-error-recovery` — 调查确认遗漏的路径匹配；该技能在初步调查之后用于复核根因和回归方案，不伪称宿主自动观测。
- [Spec] Unaided — none applied; considered: architecture and design specification.
- [Plan] Unaided — none applied; considered: work breakdown and task decomposition.
- [Test] Unaided — none applied; considered: testing strategy.

## Preconditions
- 用户同意先测可运行宿主，未测项记录待验证；不修改全局宿主配置，不强制重启会话。
- 改动层：插件自身 hooks，影响安装插件的仓库。

## Plan Review

- Verdict: sound
- Coverage: 声明账本护栏、合法声明以及真实宿主事件与异步提醒分别验收。
- Verifiability: 合成事件不代表真实宿主投递或提醒可见；缺少实际证据则明确待验证。
- Layer ownership: 编辑门负责路径判定，宿主负责事件投递，任务记录证据边界。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-10 16:28 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 补齐声明账本直接编辑护栏

- Goal: 声明账本与 evidence、released 受到同等直接编辑保护，合法声明命令保持可用。
- Dependencies: 用户批准当前计划。
- Files: `hooks/capability-gate` 及相关回归测试。
- Implementation checklist:
  - [x] 覆盖声明、既有账本、正常文档和合法声明。
  - [ ] 运行必要 CI。
- Acceptance: 支持的直接编辑事件拒绝账本编辑，合法声明成功；不声称能阻止任意 shell 写入。
- Verification: 隔离夹具和 CI。
- Rollback: 回退本任务代码及测试改动。
- Status: in_progress

### Step 2 — 真实宿主验证
- Goal: 验证当前可运行宿主的事件、异步提醒及工具引导。
- Dependencies: 宿主可在不修改全局配置的条件下启动并观察。
- Files: 任务验证记录及必要隔离夹具。
- Implementation checklist:
  - [ ] 分别观察可运行宿主的事件和提醒。
  - [ ] 记录无法运行或无法观察的宿主及具体行为。
- Acceptance: 区分配置、模拟事件、真实事件、用户可见性和模型采纳。
- Verification: 最小可复现探针和实际观察记录，不改变当前会话的权限边界。
- Rollback: 停止隔离探针，不修改全局宿主配置。
- Status: pending

## Checkpoints

## Verification / Review

- 2026-11-10 Step 1: Windows parity fixture passed; real host verification and CI pending
- 2026-11-10：已有判断漏掉 declarations；原测试为模拟事件，不证明真实宿主投递。本机有 Codex CLI 0.167.0、Claude Code 2.1.311，但是否可实际验证仍待确认。
- 2026-11-10：同一合成 `apply_patch` 事件修改前对 evidence 和 released 返回 deny，对 declarations 未拒绝；补齐后 `hooks/test-host-parity` 在 Windows Git Bash 通过，涵盖三账本和嵌套路径、合法声明及原有事件测试；`git diff --check` 通过。该夹具不是宿主端到端证据。
- 2026-11-10：在当前 Codex 桌面会话调用 `mcp__codex_app__list_artifacts` 前后，基础工作区的 capability evidence 未增加对应记录。由于调用经 `functions.exec` 包装且会话根目录不同于任务 worktree，此观察不足以判断 hook 是否接线或所有 MCP 调用均未被观测；显示与异步提醒仍待验证。
- 当前会话的文件权限将仓库 `.git` 列为只读，能力账本写入可能受此影响；未提升 MCP 调用权限或改动用户宿主配置，无法仅根据未新增账本定位原因。

## Change Log
- 2026-11-10：按已有 Todo 建立 v1 计划草案。
- 2026-11-10：用户批准 v1；随后使用 debugging-and-error-recovery 复核根因。

## Follow-ups
- 未能观察的行为保留待验证，工具引导效果不以提示送达代替模型采纳。

## Version History

- v1 — planning.
