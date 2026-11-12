# Spec — 仓库代码版本提交与回退点
> Task version: v1

## Objective and Success Criteria

Git 任务的每个版本若修改当前任务记录以外的仓库路径，在升版或完成前必须将这些改动提交到该任务分支，形成可追溯的版本回退点。

## Architecture Boundaries and Responsibilities

`hooks/task promote` 为 v1 建立版本起点；`hooks/version` 在修改文档前检查旧版本，并为新版本建立起点；`hooks/task complete` 与可独立调用的 `hooks/archive` 在改变状态或移动文件前检查。共享检查只读取 Git 状态和版本起点，不提交、推送或清理文件。

## Project Structure / Affected Files

`hooks/task`、`hooks/version`、`hooks/archive`、共享检查脚本、现有 smoke tests、`skills/taskflow/SKILL.md` 和 `skills/taskflow/references/versioning-and-recovery.md`。

## Interfaces, Data Flow, and Contracts

- 版本起点是该 worktree 的 Git HEAD 提交，按任务 ID 与版本保存在 worktree 独立的 Git 元数据中；不得在结束时用当前 HEAD 补造起点。v1 在 promote 时建立；升版先验证旧版本，再以当前 HEAD 建立新版本起点。失败时不得留下被误认为有效的半成品或修改用户代码。
- 建立起点前，检查暂存、未暂存和未跟踪的非忽略文件；仅排除当前任务的 `TaskFlowDocs/<task-id>/` 与 `TaskFlowDocs/todo.md`。其他路径如已有未提交内容，列出并拒绝建立基线，不自动提交或删除。Git 忽略文件不纳入，须如实说明。
- 结束或升版前验证基线存在、指向有效提交且为 HEAD 的祖先；检查该 worktree 暂存、未暂存及未跟踪的非忽略文件。当前任务目录和 Todo 以外有未提交变更则拒绝；若基线后存在涉及这些路径的提交，记录可回溯的提交范围；仅有任务记录变更可通过，无需空提交。
- 必须检查整个仓库，不能按后缀判定代码。用户确认 TaskFlow 任务记录之外的 README 等设计文档也视作需要提交的改动；其他任务文件也不能作为本任务自动排除。
- 文件路径含空格、中文、换行、重命名和删除时必须正确处理；不可将其他人的未提交文件加入提交。路径归属无法由 Git 自动证明，隔离分支与清晰提示是前提；不得声称排他归属已被机器证明。
- 版本状态和文档在任一检查失败时保持原状。不存在有效基线、提交已被历史改写移除、Git 错误或存在不明未提交内容时拒绝并说明原因；不静默建立补造基线。非 Git 仓库按现行行为处理。

## Invariants and Compatibility

基线按 worktree、任务、版本隔离；检查不修改 Git 用户内容。旧活动任务或丢失本机基线的任务没有可靠起点时明确阻止，不能伪造过去版本的提交；不引入自动兼容或绕过逻辑。Git 忽略文件不受保护，本地提交也不保证后续 squash/rebase 或远端仍保留同一提交点。

## Validation and Error Semantics

以独立的真实 Git 仓库验证：仓库文件提交后通过；仅任务记录无需提交；非任务文档路径也要求提交；暂存、未暂存、未跟踪、重命名、删除、空格与中文路径正确判断；缺失基线、无祖先关系、版本切换、直接 archive 和失败不改状态；并行 worktree 互不串扰。断言 Git 内容和状态而非单纯匹配标记。

## Code and Test Constraints

沿用 shell 和项目现有 smoke 测试，无新增依赖；不写自动提交或推送代码；跨平台处理 Git 路径及错误。

## Design Decisions and Alternatives

用户选择将 TaskFlow 任务记录以外的仓库路径保守视为需要提交，避免不可靠的代码后缀推断。Git 可验证范围和内容，不能证明每个提交是否由该任务创造；不应把无关提交、忽略文件或远端留存视为已受保证。

## Open Questions

无；如果实现验证显示无法可靠记录版本起点或保持失败无副作用，停止并重新设计。
