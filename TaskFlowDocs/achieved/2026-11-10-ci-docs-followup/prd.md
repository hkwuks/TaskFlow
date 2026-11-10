# 避免已通过 CI 后的文档跟进重复运行重型测试
> Task version: v1
> Status: completed

## Goal

让代码已通过 CI 后仅补充验证结果等任务文档的后续提交安全跳过不必要的重型测试，同时保留必要状态检查

## Task Kind

- Kind: capability

## Background / Confirmed Facts
- 现有 `changes` 使用 PR 的 base 与 head 完整差异，后续只改文档时仍包含已通过的代码改动。
- TaskFlow Todo 文件的模板是 smoke 测试输入，不能仅以扩展名判断安全；主分支 push 保持全量检查。

## Requirements
- 仅在能证明同一 PR 的先前相关代码与目标基线已通过必要检查，且后续变动不影响这些检查输入时复用结论。
- 无法证明、缺失权限、结果未完成、基线变化或检查输入变化时正常执行完整相关检查。
- 保留必需状态检查和现有 Todo 合并审计，不通过提交信息跳过整个工作流。

## Acceptance Criteria
- 覆盖通过、失败、缺失、跳过、不同 PR、基线变化、强推、混入代码和 Todo 模板变化等情况；不确定一律完整运行。
- 验证 GitHub 实际检查状态与任务 CI 对应关系，不以被跳过的检查充当已通过代码测试。

## External Facts

- Depends on external facts: yes
- Source: https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs
- What it settled: 跳过整个工作流可能令必需检查保持 Pending，不能直接依赖跳过标记。
- Source: https://docs.github.com/en/rest/actions/workflow-runs
- What it settled: 可按 head SHA、事件等查询工作流运行；仍需确认先前运行覆盖的实际基线和各必要 job。
- Source: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- What it settled: PR 工作流默认检出合并提交；可靠复用需记录该次事件的 head、base 和 PR 身份。

## In Scope
- 本仓库 GitHub Actions 工作流及可测试的判定工具。

## Out of Scope
- 改变其他仓库的 CI、跳过主分支最终检查或降低安全校验。

## Risks / Deferred Items

## Open Questions
