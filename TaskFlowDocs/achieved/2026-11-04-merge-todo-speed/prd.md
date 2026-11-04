# Todo 合并驱动在 125 条目上耗时 180 秒，且中断后静默丢一侧

> Task version: v1
> Status: completed

## Goal

`hooks/merge-todo` 在真实的 125 条目 `todo.md` 上要跑 180 秒。它**结果是对的**，但慢到会被调用方超时打断；而一次被打断的运行会把 `%A` 留在「ours」原样，`git merge` 仍然报告成功——一侧的结果被静默丢弃。要让它在真实数据上快到一个普通合并不会碰到超时，并且当它确实没能跑完时显式失败而不是留下一个假成功。

## Background / Confirmed Facts

来源：Todo 条目 TF-20261104-b1681b（2026-11-04 实测）。

- **正确性不是问题。** 用 #117 的真实三方输入（`eed6fdf` / `35b8151` / `8953f72`）单跑，输出 `fa9090=done`、`af456a=done`，125 条目全在。
- **耗时 180 秒**（`time` 实测，Windows/Git Bash）。
- **中断的后果已取证。** #117 的首次 `git merge` 在 120 秒被杀，随后重跑落下的 merge commit `7d9d979` 里 `TaskFlowDocs/todo.md` 与 `git show 35b8151:` **逐字节相同**（`cmp` 相同），即 driver 的结果没有进入合并，而 `git merge` 退出 0。
- **代价**：main 上 `fa9090` 由 done 变回 inbox、`af456a` 的 Notes 丢失，靠手工提交 `e110454` 修正。
- **复杂度来源**：`index_side` 每侧每条目调一次 `key_of`；`match_of` / `base_of` 每次查找都起一条 `grep -nxF | head -1 | cut` 管道。125 条目 × 3 侧 → 接近一千次进程启动。同一台机器上单次子进程约 150 ms，这就是那 180 秒。
- **Git 的 driver 契约**：`%O`/`%A`/`%B` 三个路径，把结果写进 `%A`，退出 0 表示成功、非 0 表示交给 Git 报冲突。当前实现在冲突时**已经**会写冲突标记并 exit 1，所以「未完成就显式失败」缺的是「被信号杀掉时也要如此」。

## Requirements

- R1：把三方的切分、索引、匹配全部放进单个 `awk` 进程，按条目 key 建内存字典。消除「每条目一次子进程」这条路径。
- R2：真实数据的正确性不变——同一组 `%O`/`%A`/`%B` 的输出必须与当前实现**逐字节相同**，包括条目顺序、`## Removed` 的合并、冲突标记的形状。
- R3：真实数据（125 条目）的耗时降到 5 秒以内，即一个普通 `git merge` 的调用方超时不可能碰到它。
- R4：被中断时不能留下假成功。driver 在退出前先写结果、最后用一次 `mv`/`cp` 落地，任何中途退出都让 `%A` 保持 Git 给的原始内容；并明确记录「非 0 退出 = 交给 Git 内置合并报冲突」。
- R5：不改变 driver 对外契约：路径参数顺序、`%A` 承载结果、退出码语义、`git merge` 侧无需新增配置。
- R6：断言落在 `hooks/smoke-test` 的既有 `merge-todo` 节，并新增一条真实规模（构造 125 条目）的计时断言。

## Acceptance Criteria

- AC1：同一组真实三方输入（`eed6fdf` / `35b8151` / `8953f72` 的 `todo.md`）在新实现下的输出与 `git show e110454:TaskFlowDocs/todo.md` 的对应条目一致；旧实现的输出作为基线逐字节 `cmp` 相同。
- AC2：125 条目输入的运行时间 < 5 秒（在本机 Git Bash 上测）。
- AC3：既有 smoke 断言全绿：条目只在一侧、两侧相同、一侧改动、真冲突（写冲突标记 + exit 1）、`## Removed` 并集、顺序、`task remove` 墓碑不复活。
- AC4：中断语义——用 `timeout` 在 driver 中途杀掉，`%A` 仍等于原始 ours，且退出码非 0。
- AC5：`bash hooks/repository-check .`、`git diff --check` 通过；三平台 CI 通过。

## External Facts

- Depends on external facts: no
- Why not: Git 的 merge driver 契约（`%O`/`%A`/`%B`、写 `%A`、退出码语义）已在本仓库 `hooks/merge-todo` 头部注释与 `hooks/install-git-hygiene` 的配置中记录并被 smoke 断言；本次不依赖任何仓库外的规格、版本或他人行为。

## In Scope

- `hooks/merge-todo`：单进程重写三方合并逻辑。
- `hooks/smoke-test`：真实规模计时断言 + 中断语义断言。

## Out of Scope

- 改 driver 的匹配规则本身（按 ID、按 heading、`## Removed` 键为 `head:Removed`）。本次只改**怎么算**，不改**算什么**。
- `hooks/install-git-hygiene` 的安装逻辑。
- GitHub 网页端合并：那里 driver 不运行，`CONTRIBUTING.md` 已有说明，本次不改。

## Risks / Deferred Items

- **单进程重写的最大风险是语义漂移**，不是性能。缓解：R2 要求与旧实现逐字节一致，并且用真实 125 条目数据做基线——这也是 AC1 的判据。
- **`awk` 在不同平台上的行为差异**：Windows Git Bash 的 awk、macOS 的 BSD awk、Linux 的 gawk。只使用 POSIX awk 子集（`split`、`substr`、`index`、关联数组），不用 `gensub`/`asort`/`delete array` 全清这类扩展。三平台 CI 覆盖。
- **5 秒目标可能太保守也可能太松**：先测基线，再定阈值；若单进程仍超 5 秒，先查是不是又走回了子进程。
- 中断语义（AC4）只能证明「被 SIGTERM 打断时 %A 未变」，证明不了所有中断方式；以最坏情况下 `%A` 保持原样为准。

## Open Questions

无阻塞项。
