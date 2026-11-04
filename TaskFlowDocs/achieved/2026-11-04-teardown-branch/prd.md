# 合并后 teardown 一并删除已合并的本地分支

> Task version: v1
> Status: completed

## Goal

合并完 PR、拆掉 worktree 之后，任务分支仍然留在本地且没有任何东西报告它，于是 `fix/2026-11-04-skip-guard` 这类分支不断堆积。用户在 teardown 那一步只看到三条命令：`task complete` 提示的 worktree 移除、以及一句「分支会留着，删它是另一个决定」。本次要让「拆 worktree」与「删已合并分支」在同一个 teardown 步骤里一次做完，并让 `repository-check` 在只剩分支时也能报出来。

## Background / Confirmed Facts

- **分支不是 worktree 的产物**：`git worktree add -b` 建的是仓库级 ref，worktree 只是它的检出目录；`git worktree remove` 只删目录，从不删分支。
- **现状刻意留了分支**：`hooks/archive:329-338` 的 teardown 提示明写 `(the branch survives; deleting it is a separate decision)`；同样的句子在 `skills/taskflow/SKILL.md:339` 与 `CONTRIBUTING.md:33`。理由是分支可能还持有唯一一份提交，所以不能自动删。
- **但「刻意」和「没人做」之间有差额**：`hooks/repository-check` 只报告「分支已并入 base 且工作树干净」的 *worktree*（`hooks/repository-check:122-192`）。worktree 一旦按提示移除，分支就从所有报告里消失，从此没有任何东西再提到它。
- **删除时机不能放进 `archive`**：`archive` 在 push 与 merge 之前运行（`CONTRIBUTING.md` 的次序是 `task complete` → commit → push → PR → merge），那一刻分支必然还没并入 base，任何删除都会失败或误删。删除只能发生在合并之后的 teardown 步骤，由执行者按条件手动运行。
- **`git branch -d` 本身就是安全边界**：未合并时它拒绝删除并报 `not fully merged`；`-D` 才是强制。所以 teardown 里给出的命令应当且只能是 `-d`。
- **用户已确认要这条**：Todo `TF-20261104-d535ae` 记录了三条真实残留分支与其成因，用户 2026-11-04 要求处理。
- 本仓库的合并方式有 merge commit（`aaaf4cb Merge pull request #118 …`），因此祖先判断 `--is-ancestor` 对已合并分支成立；squash/rebase 合并的分支则不会被认作已合并，这与 `repository-check` 现有的「宁可少报」取向一致。

## Requirements

- R1：`hooks/archive` 的 teardown 提示在 `git worktree remove` 之后增加一条 `git branch -d <branch>`，并把它写成与移除同一时刻、同一条件下的动作；仍须保留「未合并则拒绝」这一安全说明。
- R2：`hooks/repository-check` 增加一节「已并入 base 但仍在本地、且没有被任何 worktree 检出的分支」，只报告不删除，且不改变退出码（与现有 stale worktree 一节同一条约束：`needs` 不变）。
- R3：报告与提示都不得输出 `git branch -D`，也不得自动执行任何删除；删除始终是执行者的一步。
- R4：`repository-check` 必须排除 base 分支自身、被任何现存 worktree 检出的分支、以及 detached HEAD 情形；无 upstream 时与现有分支一样输出 unknown 而不是猜。
- R5：所有仍写着「分支会留着，删它是单独决定」的文档与新行为对齐：`hooks/archive` 的注释与提示、`skills/taskflow/SKILL.md` 的 teardown 段、`CONTRIBUTING.md` 的 teardown 条。
- R6：`hooks/smoke-test` 的既有断言随文案更新，并为新报告节补断言；不新增 hook、不改宿主接线。

## Acceptance Criteria

- AC1：在 linked worktree 中归档，teardown 输出同时含 `git worktree remove '<path>'` 与 `git branch -d <branch>`，且不再出现 `branch survives`。
- AC2：fixture 中一个已并入 base 且无 worktree 检出的分支被 `repository-check` 报出；一个未合并的分支不被报出；base 分支自身不被报出；被 worktree 检出的分支不被报出。
- AC3：上述报告出现时 `repository-check` 退出码保持 0（`STATUS: pass`），与 stale worktree 一节一致。
- AC4：无 upstream 的仓库输出仍是 `unknown (no upstream base to compare against)`，退出码不受影响。
- AC5：`bash hooks/smoke-test` 全绿；`git diff --check` 无新问题。
- AC6：变异检验——把新增报告节的过滤条件反转（改成报告未合并分支），AC2 变红并点名哪个断言失败。

## External Facts

- Depends on external facts: no
- Why not: 结论全部由本仓库可核对的既有实现与文档决定——删除安全边界是 `git branch -d` 的既有语义，报告机制复用 `hooks/repository-check:122-192` 的 `--is-ancestor` 判断，teardown 文案在 `hooks/archive:329-338` 与 `skills/taskflow/SKILL.md:339`。

## In Scope

- `hooks/archive` teardown 提示文案与相应注释。
- `hooks/repository-check` 新增报告节。
- `hooks/smoke-test` 的断言增改（archive teardown、repository-check 新节）。
- `skills/taskflow/SKILL.md`、`CONTRIBUTING.md` 中同一句 teardown 规则的措辞对齐。

## Out of Scope

- 任何自动删除行为：`archive`、`task complete`、`repository-check` 都不删分支。
- 远端分支删除（`git push origin --delete`）与 `git fetch -p`：合并后远端分支的清理由托管平台的「delete branch」承担，不在本仓库流程内。
- squash/rebase 合并的分支识别：需要比较 patch-id 或平台 API，收益不足以覆盖误判风险。
- 把 teardown 做成新命令（Todo 中的候选 b），以及让 `repository-check` 直接删除（候选 c 的加强版）。
- 清理当前机器上已存在的其他残留 worktree 与分支。

## Risks / Deferred Items

- **风险：读者误用 `-D`**。缓解：提示与文档只出现 `-d`，并在同一句说明它在未合并时会拒绝。
- **风险：`repository-check` 报告误报被当作删除许可**。缓解：报告只列已并入 base 的分支，且明确写「只报告，不删除」；删除仍需 `-d` 二次校验。
- **延后**：squash/rebase 合并识别；若将来托管平台改成 squash-only，本节会整体漏报，届时再按 patch-id 处理。

## Open Questions

无阻塞问题。
