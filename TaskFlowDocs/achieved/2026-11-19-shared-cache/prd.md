# 测试、编译等下载的非仓库内容不在各 worktree 重复创建，优
> Task version: v1
> Status: completed

## Goal

测试、编译等下载的非仓库内容不在各 worktree 重复创建，优先共用 main 工作区已有内容，以减少重复写入和硬盘磨损。

## Task Kind

- Kind: capability

## Background / Confirmed Facts
- 现有 Todo：TF-20261119-bf0c36；其主工作区原记录未改动，本任务 worktree 中已提升。
- 本仓库 572 个受跟踪文件当前逻辑大小约 4.69 MiB；并非物理写入测量。
- 现有一个 worktree 含未提交修改，另一个含被忽略的会话记录；不能仅凭干净的 Git 状态判定可重用。
- Git worktree 共享仓库元数据，但独立检出工作文件；包管理器通常已有下载缓存，环境及构建产物的共享安全性需分别判断。

## Requirements
- 作为 TaskFlow 通用规则，优先复用工具支持的下载缓存及已存在的资源，避免每个 worktree 重复下载；仅在授权范围内读取或写入，不更改用户全局配置。
- 严格区分不可变下载缓存与可能因路径、版本、构建参数或并发而失效的虚拟环境、node_modules 与构建输出；不无条件共享后者。
- 只有原任务已完成并归档、归档记录和所有修改均已提交且无人使用时，才可复用既有 worktree；先切到已核实的 main 提交，再从该提交创建新分支，不自动追踪旧分支；未合并时保留原分支。
- 保护跟踪、未跟踪、被忽略文件、子模块及 TaskFlow 的 Git 元数据；跨任务证据不得沿用，旧任务的证据与 Git 基线可恢复。
- 条件不满足或状态不确定时拒绝切换且保留可恢复信息，回退到独立 worktree；不因任务归档自动删除可复用工作树或缓存。
- 将工作树去留与本地分支清理分开：原任务归档、分支合并并确认允许删除后，从该分支安全切出，再按现有安全条件用 `git branch -d` 清理；删除被拒绝时保留并报告。

## Acceptance Criteria
- 面向各仓库的流程清楚说明：优先已有工具缓存，访问/写入权限和位置可验证，不假定安装产物可共享；不要求修改全局配置。
- 原任务已完成归档且归档记录已提交时，空闲、安全的 worktree 先切到已核实 main 提交，再从该提交创建不自动追踪旧分支的新分支；未合并旧分支与提交仍可找回；未归档任务一律拒绝切换。
- 已有用户授权且确认原分支合并后，本地分支可按安全条件清理，同时工作树保留可复用；若 Git 拒绝 `-d`（包括某些 squash/rebase 合并），保留分支并报告。
- 未提交或未跟踪变化、被忽略文件冲突、活跃占用、损坏元数据及切换中断时不得覆盖用户数据或误报成功；保留明确恢复方式。
- 前一任务未消费的能力证据和外部 URL 不得证明新任务的执行；返回旧任务时其证据和版本基线仍可核验。
- 指引、生命周期提示和测试一致；覆盖共享缓存边界、旧分支保留、拒绝条件、不同任务证据隔离、失败恢复和既有单任务流程。

## External Facts
- Depends on external facts: yes
- Source: https://git-scm.com/docs/git-worktree
- What it settled: worktree 有独立工作文件和元数据，同仓库共享引用，不等于共享所有工作文件。
- Source: https://docs.npmjs.com/cli/commands/npm-ci/
- What it settled: npm ci 开始安装前移除已有 node_modules，不能将其无条件作为并发共享目录。
- Source: https://pip.pypa.io/en/stable/topics/caching/
- What it settled: pip 默认缓存下载及构建的 wheel；缓存不保证完全离线，不能等同可移植虚拟环境。
- Source: https://git-scm.com/docs/git-sparse-checkout
- What it settled: 稀疏检出仅在工作树填充跟踪文件的一部分，且涉及 worktree 专用配置；不能默认忽略构建所需文件。
- Source: https://git-scm.com/docs/git-checkout
- What it settled: 切换分支默认可能覆盖被忽略文件；`--no-overwrite-ignore` 在目标有冲突时中止。
- Source: https://git-scm.com/docs/git-switch
- What it settled: 可从指定起点创建新分支，原分支不需要先合并。

## In Scope
- 所有 TaskFlow 用户的缓存及复用指引、必要的安全复用流程、工作树/本地分支分离清理和相应 hook 提示、测试。
- 本仓库 `CONTRIBUTING.md` 与相关约定中与复用直接冲突的规定。

## Out of Scope
- 实测 SSD 写入量或承诺延长寿命；默认稀疏检出；未经授权的自动删除或强制覆盖；修改用户主目录、全局配置或安装依赖。
- 将虚拟环境、node_modules、构建输出默认共用；自动断定未合并分支可删除。

## Risks / Deferred Items
- 当前证据和外部 URL 在每个 worktree Git 元数据下共用；复用时必须隔离，且中断后不能悄悄遗漏或错认。
- Git 状态默认不显示忽略文件；使用防覆盖参数仍不表示旧缓存适合新任务。
- 同路径跨进程同时使用无法仅靠 Git 状态证明不存在；调用方负责确认空闲，复用操作需互斥并失败关闭。

## Open Questions
- 无。用户确认通用规则与安全缓存边界，并要求原任务先归档、复用工作树不影响本地分支按安全条件清理。
