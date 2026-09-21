# Windows worktree misjudgement: `hooks/task` reads a `D:/` git dir as relative.

> Task version: v1
> Status: completed

## Goal

TaskFlow 的 worktree 判定在 Git for Windows 上永远答错：`hooks/task` 的 `worktree_kind()` 用 `git rev-parse --git-dir` 取 git 目录，再把不以 `/` 开头的答案当成相对路径去拼 `$root/`，而 Git for Windows 返回的是 `D:/...`（在那边是绝对路径，但不带前导斜杠）。拼接结果指向一个不存在的路径，`commondir` 找不到，于是每个任务 worktree 都被判成 base tree：`promote` 直接拒跑，`intake` 发出错误的"已污染 base 工作树"警告。

同时删除 `TaskFlowDocs/repository-docs/index.md` 里没有任何消费者的 "Last checked" 列——它每次渲染都被盖上当天日期，等于每个自然日把一份已跟踪文件弄脏一次。

## Background / Confirmed Facts

- 触发环境：Windows + Git for Windows。用户在 `D:/...` 下的 worktree 里实测 `worktree_kind` 返回 2，而 `git worktree list` 同时显示该目录确实是链接 worktree。
- 根因位置：`hooks/task:52-62`（`worktree_kind`）。返回值约定：`0` = 任务 worktree，`1` = 不是仓库（允许），`2` = base 工作树。
- 两个调用点同源：`hooks/task:490`（`intake`，kind=2 时打印警告）与 `hooks/task:510`（`promote`，kind=2 时打印 "Blocked: this is the base working tree" 并以 3 退出）。改这一个 helper 即同时修复两者。
- 仓库内已有同类先例：`hooks/install-merge-driver:47` 写的是 `case "$info" in /*|[A-Za-z]:[/\\]*) ;; *) info="$root/$info" ;; esac`，说明 drive-letter 形态此前被处理过一次，只有 `hooks/task` 漏了。
- `git rev-parse --absolute-git-dir` 在 Linux/macOS 上返回 POSIX 绝对路径（本机实测 `/tmp/gt/.git/worktrees/-wt`），在 Git for Windows 上返回 `D:/...`，两者都可直接拼接使用。因此不需要手写路径形态判断。
- 测试可注入性：`D:/` 在 Linux 上是合法的普通相对路径（一个名叫 `D:` 的目录），所以 Windows 形态的答案可以在 Linux 上真实复现，不需要 Windows 机器。
- 已确认 `hooks/task` 中只有这一处路径形态判断；其余 `rev-parse` 调用（`--show-toplevel`、`--is-inside-work-tree`、`--verify`）只比较字符串或只看退出码，不受影响。
- `TaskFlowDocs/repository-docs/index.md` 的 "Last checked" 列与表头日期由 `hooks/repository-docs-context` 每次 SessionStart 重写（原 `:17` 取 `today`、`:175` 写行、`:181` 写表头）；carry-over 读旧行时明确丢弃该列（原 `:128-129` 只取 f[2]/f[3]/f[4]/f[7]），`hooks/repository-check:42` 只判断文件是否存在，smoke-test 无任何断言，`skills/taskflow/` 的散文只要求"维护/读取"。即：没有任何消费者。
- 该 hook 本有 `cmp -s` 写入守卫（原 `:201`），但 `today` 被烘进渲染内容，所以同一天重跑是无操作、跨天必写——日期恰好是守卫唯一覆盖不到的情况。
- 已核：small 任务不需要 `spec.md`（`TaskFlowDocs/achieved/2026-09-18-conflict-side-review/` 等近期任务只有 `prd.md` + `plan.md`）。

## Requirements

- R1：`worktree_kind()` 在任何平台上都能正确区分任务 worktree 与 base 工作树，不再依赖"答案是否以 `/` 开头"。
- R2：修复不得改变该函数的返回码约定（0/1/2）与两个调用点的行为差异（`promote` 硬 gate 退出码 3，`intake` 软警告）。
- R3：加入可在 Linux 上复现 Windows 形态答案的回归测试，且该测试必须能抓住旧实现（变异验证）。
- R4：`hooks/smoke-test-windows.ps1` 增加真机回归：在被测仓库里 `git worktree add` 出链接树，验证 `promote`/`intake` 在链接树内放行、在 base 树内按原语义拒绝/警告。
- R5：删除 `TaskFlowDocs/repository-docs/index.md` 的 "Last checked" 列与表头日期，表变为 `Class | Source path | Phases | Exists | Status`。
- R6：carry-over 仍能读回删除列之前写下的旧索引行（旧行多一格，最后一格仍是 status），且不会把日期误当成 status。
- R7：同步 `skills/taskflow/SKILL.md` 与 `skills/taskflow/references/artifacts.md` 中描述索引列的散文。
- R8：索引渲染结果不得依赖渲染时刻；同日重跑逐字节幂等。
- R9：本轮不引入新的 `hooks/smoke-test` 依赖，不改变 hook 的零解释器约束（POSIX awk/sed + bash 3.2）。

## Acceptance Criteria

- 旧实现下 `hooks/smoke-test` 的新增 drive-path 断言必须失败；修复后必须通过（一次一个变异，逐个记录）。
- `bash hooks/smoke-test` → `ALL SMOKE PASSED`，exit 0。
- `git diff --check` → clean；Skill 校验器通过。
- 用 `date` 垫片返回 `2099-01-01` 重跑 `hooks/repository-docs-context`，`index.md` 摘要不变。
- 旧格式（6 列含日期）索引行能被 carry-over 读回并按原 phases/status 参与路由；7 格且末格为日期的畸形行被拒绝（`contains an invalid row`）。
- `hooks/smoke-test-windows.ps1` 在链接 worktree 内 `promote` 成功，在 base 树内 `promote` 仍被拒。

## In Scope

- `hooks/task`（`worktree_kind`）。
- `hooks/repository-docs-context`（删除日期列与其渲染、放宽 carry-over 读列并加 status 形态守卫）。
- `hooks/smoke-test`（drive-path 回归、旧索引兼容、日期无关性；3 处携带日期的正则）。
- `hooks/smoke-test-windows.ps1`（真机 worktree 回归）。
- `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`（散文同步）。
- `TaskFlowDocs/repository-docs/index.md`（由 hook 重新渲染后的结果）。

## Out of Scope

- 不改 `hooks/install-merge-driver`（已具备 drive-letter 分支）。
- 不把"索引新鲜度"改成别的信号（如仅在行集变化时盖章）——该列无消费者，先删掉；需要时另开条目。
- 不处理 Windows CI 未覆盖的其他 hook 路径。

## Risks / Deferred Items

- **风险：Windows 真机回归无法在本机运行**（本机为 Linux/WSL）。R4 的 PowerShell 断言只能靠 CI 的 `windows-latest` 跑；本轮在 PR 里如实记录这一点，不声称已本地验证。
- **风险：carry-over 放宽到 `n < 6 || n > 8` 会顺带接受 5 格行**。这是有意的最小放宽：让"旧 6 列行"和"删列后的畸形行"都走同一个判定，再由末格必须是小写 status 这条守卫拦住日期。收紧成精确格数会把 `../outside.md` 那条负例，以及同一轮里被接受的其他畸形行一起打掉（已实测：收紧成 `n != 6` 会让既有负例不再报 `invalid row`）。
- **已发现、不属于本任务**：`TaskFlowDocs/todo.md` 中 `TF-20260919-c41f8a` 一条 20 行新增不是本任务产出，作者与落地路径不明；本任务不提交它，单独向用户报告。
- **已发现、不属于本任务**：本机存在 8 个 worktree，其余 7 个分支相对 `origin/main` 都是 0 commits ahead（干净）；本次 PR 不受影响。

## Open Questions

- 无。任务所需的判定（是否一并删日期列）已由用户明确指定。

## Version History

- v1 — planning。
