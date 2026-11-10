# Plan — README 架构图
> Task version: v1
> Status: completed

## Related Tasks
- Todo: TF-20261110-62fd8e；Token 与流程优化单独记录为 TF-20261110-84d1a9。

## Skills / Tools Used
- [PRD] Unaided — 根据用户指定的现有架构图整理范围；considered: requirements elicitation and framing
- [Plan] Unaided — 简单双语文档修改；considered: work breakdown and task decomposition
- [Test] Unaided — 比较两份图的关系并检查 diff；considered: testing strategy

## Plan Review
- Verdict: sound
- Coverage: Step 1 的中英文 Mermaid 图覆盖 PRD 第 1 条；图旁说明和 runtime 链接覆盖第 2 条。
- Verifiability: 双语关系比较检查结构一致；GitHub 页面实际渲染检查补足解析与显示验证，CI 和 diff 检查覆盖仓库现有约束。
- Layer ownership: 改动仅涉及 README 与任务记录，没有修改检查依据来制造通过结果。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-10 11:06 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps
### Step 1 — 更新并验证架构图
- Acceptance: 中英文架构图一致，准确展示计划审核和工具引导边界。
- Verification: 比较 Mermaid 关系、检查引用路径和 `git diff --check`；CI 与 GitHub 渲染待确认。
- Status: done

## Verification / Review
- 任务记录在 README 编辑后补建，未进行事前 Plan Review，也未记录虚构的计划批准；PR 保持草稿以便审阅。
- 双语图的 18 条关系一致，runtime 链接目标存在；`git diff --check` 和 TaskFlow Skill quick_validate 通过。
- 2026-11-10 事后复核：GitHub 实际渲染的中英文图均展示计划审核节点；PR #129 的 CI 42745374369 三系统 smoke、release 与 Todo 审计通过。此复核不追认此前已发生的事前审核或批准。
- 2026-11-10 用户在被告知计划事后补建、归档需要事后批准及清理归档自身临时文件后，明确要求先归档已合并事项；本次批准用于事后归档，不表示实施前已有批准。
- PR 模板 `.github/pull_request_template.md`：Summary 写目标；TaskFlow traceability 写任务、范围和目标；Verification 写本节及 CI；Review boundaries 写边界和未验证的渲染。

## Follow-ups
- 无未完成的 README 交付项；流程和 Token 优化由 TF-20261110-84d1a9 继续跟踪。
