# Plan — 任务文档升版时继承并修订已有设计
> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/version`、`hooks/smoke-test`、`skills/taskflow/SKILL.md`、`skills/taskflow/references/versioning-and-recovery.md`
- `TaskFlowDocs/repository-docs/index.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`

## Related Tasks

- TF-20260911-05：已完成旧版本留存；本任务补足新版本内容继承与审核。

## Skills / Tools Used

- [PRD] Unaided — none applied; considered: requirements elicitation and framing, root cause investigation.
- [Plan] Unaided — none applied; considered: work breakdown and task decomposition.
- [Test] Unaided — none applied; considered: testing strategy.

## Preconditions

- 用户确认保留有效设计、使用非阻断审核对照及保留完成步骤。
- 变更归属：插件自身行为，修改 `skills/taskflow/` 与现有 `hooks/smoke-test`，不改宿主配置。

## Plan Review

- Verdict: sound
- Coverage: 覆盖升版后编辑与审核；现有脚本已保留正文，不添加冗余守卫。
- Verifiability: 对三个文档的不同正文和完成步骤做真实脚本前后对照，并区分行为指导与自动保证。
- Layer ownership: 语义由 Agent 判断，脚本只验证机械保留；历史存档机制维持不变。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-11 17:48 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 补强升版继承及审核

- Goal: 明确继承有效设计和完成记录，审核新旧差异。
- Dependencies: 用户确认的三个处理选择及本计划。
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/versioning-and-recovery.md`；仓库镜像如有须同步。
- Implementation checklist:
  - [x] 将继承、有限修订和审核对照加到现有升版流程。
  - [x] 检查引用及镜像一致性。
- Acceptance: 无新增阻断或兼容代码，保留用户更改设计的权利。
- Verification: 规则审核与镜像检查。
- Rollback: 回退本任务规则改动。
- Status: done

### Step 2 — 验证正文保留及回归

- Goal: 验证脚本升版保留所有核心文档正文、历史及完成记录。
- Dependencies: Step 1。
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 扩充现有升版夹具，验证 PRD、Spec、Plan 中独立正文及完成步骤。
  - [x] 执行聚焦验证和必需检查，记录未覆盖的真实模型行为。
  - [x] 三系统 CI 验证完整 smoke。
- Acceptance: 验证实际产物而非仅检查提示文案；不把机械检查等同语义保障。
- Verification: 版本 fixture、语法检查、CI。
- Rollback: 回退本任务测试修改。
- Status: done

## Checkpoints

## Verification / Review
- [PR #139 CI](https://github.com/hkwuks/TaskFlow/actions/runs/42998816536)：Ubuntu、macOS、Windows smoke、evals、CI 复用测试和 Todo 审计通过；release 按路径分类跳过。
- 本地真实 `hooks/version` 隔离夹具通过：PRD、Spec、Plan 的正文、完成步骤及三个旧版文件均保留；新版本状态与审批按现有脚本重置。
- `bash -n hooks/smoke-test`、Skill quick_validate（Python UTF-8）、`git diff --check` 通过。完整 smoke 在 Windows Git Bash 的无解释器夹具因共享库加载失败，未到达升版段；后续 CI 三系统验证通过。
- 规则和对照审核为非阻断指导，测试仅证明机械保留，不证明真实 Agent 必定遵循。

## Change Log

- 2026-11-11：调查确认升版脚本保留根正文，用户确认修复范围。

## Follow-ups

- 真实模型是否稳定执行升版审核需在实际任务中观察。

## Version History

- v1 — planning.
