# Detect a Todo entry a merge dropped
> Task version: v1
> Status: completed

## Goal

给 `TaskFlowDocs/todo.md` 加一条只读检查：一次合并的**结果**里如果少了任一父提交持有的 Todo 条目，就报出来并指名丢的是哪一条、在哪两个提交之间丢的。目标不是修好已经丢的那一次，而是让「悄悄丢一整节」在进入 `main` 时立刻可见。

## Background / Confirmed Facts

- **丢失确实发生过一次，链路完整**：`a6d8fdd`（PR #21）把 `TF-20260915-01` 写进 `todo.md`，`931c651` 仍持有；`77c25dd`（`Merge branch 'main' into chore/untrack-workflow-draft`，committer 为 `GitHub <noreply@github.com>`，2026-09-15 10:42:29）产出的 `todo.md` 与它自己的第一父提交 `8c44f1b` **逐字节相同**（blob `2e3cb1d…`），段落消失且**没有任何冲突标记**；随后 `1905984`（PR #17 的合并提交，10:45:01）取了 `77c25dd` 那一侧，`main` 就此丢了它（blob 仍是 `2e3cb1d…`）。条目后来在 PR #27 里按 `a6d8fdd` 重建。
- **不是 `merge driver` 的问题**：用当时的三个真实输入（base `3d1dcbc` / ours `8c44f1b` / theirs `931c651`）跑 `git merge-file`，git **报冲突**（退出 2，2 个冲突标记，条目仍在）；`hooks/merge-todo` 在同样输入上干净合并、条目保留。而 `77c25dd` 的输出既无标记又整段取 ours，是**托管平台侧的「Update branch」合并**的产物——它的 committer 是 GitHub，消息正是该按钮生成的那句。`hooks/merge-todo` 首次提交 `ebc62c2` 在 16:38:28，晚于 `77c25dd` 的 10:42:29，当时也不存在。
- **两边在同一锚点各追加一条，是这次冲突的成因**：base 的最后一行是 `## Restore macOS portability for hooks and smoke tests` 段；ours 在其后追加了 `TF-20260914-05`，theirs 追加了 `TF-20260915-01`。本地 `git merge` 因此冲突，平台在解这个冲突时整段保留了本分支的版本。平台内部的取舍规则无法从本仓库观察，所以本任务不去预测它，只对**结果**做校验。
- **全历史只有这一次**：扫 `git rev-list --all` 的 41 个合并提交，「结果的 ID 集合必须覆盖每个父提交的 ID 集合」这条不变量只命中 `1905984` 与 `77c25dd`（同一条 `TF-20260915-01`），此外从未触发。
- **该不变量是系统自己写下的承诺，但没有自动检查**：`hooks/merge-todo` 头部第 27-28 行断言「Todo 条目不删除、标题不改写」；`SKILL.md` 也规定条目只改状态、不做删除。目前没有任何东西在执行它。
- **两个已排除的「合并时修补」方向**（不重新提议）：`merge=union` 属性会在两条目同时插入时交错并静默丢掉共享的尾行（`2026-09-15-todo-merge-driver` 已实测），且托管平台不跑自定义 driver，服务端合并时该属性无意义；拆成一任务一文件已被用户否决。

## Requirements

- R1：新增 `hooks/todo-check [repository-root] [commit]`，只读。取 `commit`（默认 `HEAD`）的 `TaskFlowDocs/todo.md` 的 `- ID:` 集合，与**每个父提交**的同一集合比较；某 ID 在父提交里存在而在 `commit` 里缺失，即判为丢失。
- R2：`commit` 不是合并提交（无第二个父）时通过；父提交没有 `TaskFlowDocs/todo.md` 时跳过该父提交，不算丢失——这保证一个尚未引入 Todo 的仓库不被误报。
- R3：退出码遵循 `CODE_STYLE.md`：`0` 通过，`2` 发现丢失，`3` 无法判定（不在 Git 仓库内、`commit` 不可解析）。输出形状与 `hooks/repository-check`、`hooks/release-check` 一致（`Repository:`、`- ` 明细行、末行 `STATUS: pass|needs-user-input|blocked`）。
- R4：纯 bash 3.2 + POSIX 工具，不依赖任何解释器；不写任何文件，不自动恢复条目。
- R5：`hooks/smoke-test` 增加一节，用真实 Git fixture 覆盖：干净的非合并提交通过；人造的「合并丢掉父提交里的一条」退出 `2` 并指名 ID 与父提交；不可解析的 `commit` 退出 `3`；非 Git 目录退出 `3`；父提交无 `todo.md` 通过。新增断言逐条 mutation 验证（把实现改坏 → 断言变红）。
- R6：`hooks/README.md` 与 `skills/taskflow/references/runtime.md` 的 hook 清单补上 `todo-check`。

## Acceptance Criteria

- 在真实历史输入上复现：以 `931c651`（持有条目）与 `77c25dd`（丢了条目）构造的一对父子提交为 fixture 时，`bash hooks/todo-check . <子提交>` 退出 `2`，输出指名 `TF-20260915-01` 与被取的那一侧。
- `bash hooks/todo-check .` 在当前 `main` 的 `HEAD` 上退出 `0`（现状没有新增丢失；历史那两次不在默认比较范围内，见 Risks）。
- `bash hooks/smoke-test` 全绿，且新增的每条断言在对应实现被改坏后确实变红。
- 全部 hook 在 `docker run --rm -v "$PWD":/w -w /w bash:3.2 bash -n` 下解析通过。

## In Scope

- `hooks/todo-check`（新）、`hooks/smoke-test`、`hooks/README.md`、`skills/taskflow/references/runtime.md`。

## Out of Scope

- **CI 接线与托管平台合并路径的保护**：下一个任务 `TaskFlowDocs/2026-09-16-web-ui-merge-loss-guard/`。本任务只交付「能查出丢失」这条命令，不把它接进任何自动流程。
- **重复 Todo ID 的修复**：`TaskFlowDocs/2026-09-16-duplicate-todo-id/`。
- 不修正、不重写历史；不自动恢复丢失条目；不做合并时拦截。
- 不新增范围参数（如 `--since <ref>`）：见 Risks 第 1 条。

## Risks / Deferred Items

- **默认只比较 `commit` 自身**：一次推送包含多个提交、且丢失发生在中间某个合并提交上时，默认调用不会发现（推送后的 tip 两侧都已带上丢失）。需要对每个合并提交各跑一次做全历史审计，即 `for m in $(git rev-list --merges HEAD); do bash hooks/todo-check . "$m"; done`。有意不做 `--since` 之类的范围参数：CI 需要的是「本次事件引入的合并」，把范围参数化会引出「历史里那次丢失永久标红」的问题，而那属于下一个任务的 CI 设计。
- **只认 `- ID:` 行**：`## Item template` 代码块里的模板行与更早期没有 ID 字段的条目不在保护范围内。
- **只报不修**：修复仍需人从 `git show <父提交>:TaskFlowDocs/todo.md` 取回。
- 原型阶段发现的既有、与本次丢失无关的缺口：`TaskFlowDocs/achieved/2026-09-10-repository-document-placement/` 在全部历史里从未有过对应的 Todo 条目（随 `660679a feat: release TaskFlow 1.0.2` 进入仓库）。不在本任务范围。

## Open Questions

- 无。

## Version History

- v1 — approved, implemented, and verified. `hooks/todo-check` 交付后，全历史 41 个合并提交只命中这一次丢失，当前 `HEAD` 通过。
