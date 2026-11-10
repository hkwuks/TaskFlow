# Plan — README 架构图
> Task version: v1
> Status: planning

## Related Tasks
- Todo: TF-20261110-62fd8e；Token 与流程优化单独记录为 TF-20261110-84d1a9。

## Skills / Tools Used
- [PRD] Unaided — 根据用户指定的现有架构图整理范围；considered: requirements elicitation and framing。
- [Plan] Unaided — 简单双语文档修改；considered: work breakdown and task decomposition。
- [Test] Unaided — 比较两份图的关系并检查 diff；considered: testing strategy。

## Plan Review
- Verdict: needs revision
- Coverage: Step 1 覆盖两条验收标准；PR 前仍需确认图的实际渲染。
- Verifiability: 双语关系比较能验证结构一致，不能证明 GitHub 渲染结果。
- Layer ownership: 改动仅涉及 README 与任务记录，没有修改检查依据来制造通过结果。

## Approval
- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

## Steps
### Step 1 — 更新并验证架构图
- Acceptance: 中英文架构图一致，准确展示计划审核和工具引导边界。
- Verification: 比较 Mermaid 关系、检查引用路径和 `git diff --check`；CI 与 GitHub 渲染待确认。
- Status: in_progress

## Verification / Review
- 任务记录在 README 编辑后补建，未进行事前 Plan Review，也未记录虚构的计划批准；PR 保持草稿以便审阅。
- 双语图的 18 条关系一致，runtime 链接目标存在；`git diff --check` 和 TaskFlow Skill quick_validate 通过。
- PR 模板 `.github/pull_request_template.md`：Summary 写目标；TaskFlow traceability 写任务、范围和目标；Verification 写本节及 CI；Review boundaries 写边界和未验证的渲染。

## Follow-ups
- 验证 GitHub Mermaid 渲染并完成审批与 CI。
