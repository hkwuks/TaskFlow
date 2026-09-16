# Hold Todo protection on the web-UI merge path
> Task version: v1
> Status: completed

## Goal

让「合并丢掉 Todo 条目」在**实际发生合并的那条路径**上被挡住：托管平台的 web UI 合并。上一轮（`TaskFlowDocs/achieved/2026-09-15-todo-merge-driver/`）交付的 `hooks/merge-todo` 只在本地合并时生效，而 `77c25dd` 已经证明：当 PR 通过平台的「Update branch」/ web UI 合并时，整段条目可以无声消失。本任务把 `hooks/todo-check` 接进 CI 的 `push: main`，并让它在一次推送的范围里逐一审计本次引入的合并提交。

## Background / Confirmed Facts

- **web UI 路径的结构性缺口是既有的**：`skills/taskflow/references/runtime.md` 已写明「Only local merges. A hosted-platform merge runs server-side and does not run a custom driver」，`hooks/README.md` 同样记了这条限制。也就是说这条路径目前**只有文档警告，没有任何检查**。
- **实测：平台侧的取舍无法预防，只能对结果做校验**。用真实输入（base `3d1dcbc` / ours `8c44f1b` / theirs `931c651`）本地 `git merge` → 冲突；`77c25dd`（committer 为 `GitHub <noreply@github.com>`，10:42:29）的结果却与 ours 逐字节相同、无冲突标记。平台内部的冲突取舍规则无法从本仓库观察，也没有 API 或配置能让插件改变它——`2026-09-15-todo-merge-driver` 的 PRD 已确认插件不能改托管设置或 branch protection。**因此本任务不承诺预防，只承诺「落地的同一个推送窗口内被发现」。**
- **CI 已经有可用的触发点**：`.github/workflows/hooks.yml` 已同时监听 `pull_request` 与 `push: main`，并已有 `release` job 用 `fetch-depth: 0`。一个 `push: main` 的审计 job 是这条工作流的自然延伸，不需要新工作流。
- **`push` 事件自带范围**：GitHub 的 push payload 给出 `github.event.before` 与 `github.event.after`；新分支、强推或首个推送时 `before` 可能为全零 SHA，需要退化为只审计 `after`。`release` job 用的 `fetch-depth: 0` 保证两个提交都在本地。
- **范围而非全历史，是有意的**：`1905984` 与 `77c25dd` 那一次丢失已经修复（条目在 PR #27 里按 `a6d8fdd` 重建），全历史审计会让那条早已修复的旧记录让 CI 永久变红。按推送范围审计才是「本次事件」的语义。
- **丢失可被无歧义检出**：上一任务的检查（结果的 `- ID:` 集合必须覆盖每个父提交的集合）在 41 个合并提交上只命中那一次，误报为零，且已经是一条可运行的命令。
- **依赖关系**：本任务依赖 `TaskFlowDocs/2026-09-16-todo-entry-loss-detection/` 先落地——它交付 `hooks/todo-check`；本任务给它加范围模式并接线。见 Open Questions。

## Requirements

- R1：把 `hooks/todo-check` 的第二个位置参数从「一个提交」扩展为「一个 rev 或 rev 范围」。参数含 `..` 时，对该范围内**每一个合并提交**逐一审计；不含 `..` 时行为不变（只审计该提交）。范围模式仍只读。
- R2：范围里某个提交不可解析、或范围本身无法解析时 → `STATUS: blocked` 退出 `3`；范围为空（没有合并提交）→ `STATUS: pass` 退出 `0`；任一合并提交丢条目 → 列出并 `STATUS: needs-user-input` 退出 `2`。输出里必须能看出丢的是哪一条、哪一个父提交持有它、以及哪个提交丢了它。
- R3：`.github/workflows/hooks.yml` 增加 job（`push: main` 与 `pull_request` 都可触发，复用现有事件），用 `fetch-depth: 0` checkout，运行 `bash hooks/todo-check . "${{ github.event.before }}..${{ github.event.after }}"`；`before` 为全零或为空时退化为 `bash hooks/todo-check . HEAD`。job 在检测到丢失时失败（非零退出）。
- R4：CI 失败时人要知道怎么修：`skills/taskflow/references/runtime.md` 记录本条路径的保护现在是「本地合并用 driver + 推送后在 CI 审计」，并给出取回丢失条目的命令（`git show <持有它的父提交>:TaskFlowDocs/todo.md`）。
- R5：`hooks/smoke-test` 覆盖范围模式：范围内含一个丢条目的合并 → `2`；范围里只有非合并提交 → `0`；空范围 / 坏范围 → `3`；全零 `before` 的退化路径（以 `HEAD` 调用）→ 与单提交模式一致。新增断言逐条 mutation 验证。
- R6：`hooks/README.md` 与 `skills/taskflow/references/runtime.md` 更新 `todo-check` 的说明（范围参数、CI 接线、仍然做不到的事）。

## Acceptance Criteria

- 在真实 Git fixture 上：`bash hooks/todo-check . <before>..<after>` 在范围内含一个丢条目的合并提交时退出 `2` 并指名该 ID 与其父提交；范围内全是干净提交时退出 `0`。
- `bash hooks/todo-check .` 在当前 `HEAD` 上仍退出 `0`（与上一任务一致，回归不变）。
- 推送后 `.github/workflows/hooks.yml` 的新 job 在 `main` 上成功；把范围指向构造出的问题提交时本地同一命令退出 `2`。
- `bash hooks/smoke-test` 全绿，新增断言逐条 mutation 验证变红。
- 全部 hook 在 `bash:3.2` 容器下 `bash -n` 通过。

## In Scope

- `hooks/todo-check`（扩展范围模式）、`.github/workflows/hooks.yml`、`hooks/smoke-test`、`hooks/README.md`、`skills/taskflow/references/runtime.md`。

## Out of Scope

- **预防平台侧的取舍**：不可达，本任务只做落地后的快速检出（见 Background 的实测结论）。
- 不改 `hooks/merge-todo`、不改 `hooks/install-merge-driver`、不改托管平台的 repository/branch protection 设置。
- 不自动恢复丢失条目：CI 报告 + 文档命令，恢复仍由人执行（改动 `todo.md` 是受审的动作）。
- 重复 Todo ID 的修复：`TaskFlowDocs/2026-09-16-duplicate-todo-id/`。
- 不审计全历史（见 Background）。

## Risks / Deferred Items

- **检出发生在合并之后**：CI 变红时条目已经不在 `main` 上，恢复到修复提交之间的窗口里别的工作可能基于缺条目的树。缓解：本任务把窗口压到一次推送；真正的预防不在本任务可达范围。
- **只在 `push: main` 兜住 `main`**：其他长分支之间的平台合并仍无保护。本仓库目前只有 `main` 是长期分支，暂不扩展。
- **`pull_request` 事件下 `github.event.before/after` 不存在**：workflow 需要按事件类型分支，避免在 PR 上取到空值。实现里显式处理，并由 CI 自身的运行结果验证（smoke 无法覆盖 YAML）。
- **范围模式的依赖顺序**：本任务修改 `hooks/todo-check`，必须等上一任务的 PR 合入后再开分支（见 Open Questions）。

## Open Questions

- 是否接受本任务排在 `2026-09-16-todo-entry-loss-detection` **之后**串行执行？它修改同一个文件（`hooks/todo-check`），并行会让两个 PR 冲突。当前按串行排序。
- 是否需要给范围模式加一个 `--all-merges`（或类似）以支持人工全历史审计？当前不做，理由见 Background 最后一条；人工需要时用 `git rev-list --merges` 自己循环。

## Version History

- v1 — planning.
