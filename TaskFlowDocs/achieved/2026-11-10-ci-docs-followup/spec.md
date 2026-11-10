# Spec — 避免已通过 CI 后的文档跟进重复运行重型测试
> Task version: v1

## Objective and Success Criteria
- 可证明先前通过的检查仍覆盖当前合并结果时，文档跟进免于重复重型任务；其余正常执行。

## Architecture Boundaries and Responsibilities
- GitHub 提供运行和检查结论，Git 比较基线及检查输入，工作流控制必要 job 的执行。

## Project Structure / Affected Files
- `.github/workflows/hooks.yml`、`tools/workflow-affected` 及针对性测试；具体实现以调研验证为准。

## Interfaces, Data Flow, and Contracts
- 先前成功必须对应同一 PR、相同目标基线和仍可证明等价的测试输入；结果来源、实际 check 名称和 job 结论须可核验。
- PR 工作流产生小型元数据 artifact，记录事件的仓库、PR、base 和 head；后续运行只从同一工作流的先前运行读取并与 GitHub API 元数据交叉核验。
- 仅当旧 head 是当前 head 的祖先、base 完全相同、两者差异仅为工作流分类器明确不读取的任务目录文档，且相应 job 上次确实成功时，才可复用该 job；无证据一律运行。
- `TaskFlowDocs/todo.md`、工作流/脚本、未知路径、push main 和跨仓库不在跳过范围；检查和 Todo 审计始终保留。

## Invariants and Compatibility

## Validation and Error Semantics
- API 不可用、身份不匹配、不完整或冲突的状态全部回退为完整检查。
- Artifact 和 API 数据按不可信输入验证，标识、OID 及 job 名必须精确匹配，下载时不得执行或解压任意路径；先前 skipped 不等于成功执行。
- 先前 PR 的工作流、元数据写入器或其之前执行的分类器如相对 base 有改动，不能信任所写元数据，直接回退完整检查。

## Code and Test Constraints

## Design Decisions and Alternatives
- 不通过 commit skip 或工作流路径过滤绕过整个必需工作流；对不确定情况按用户要求运行 CI。

## Open Questions
