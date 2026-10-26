# PRD — 把 8 个已被跟踪的 sessions.md 移出版本库
> Task version: v1
> Status: completed

## Goal

`TaskFlowDocs/**/sessions.md` 是每个克隆自己的续接索引，携带本机 session id、工作目录和时间戳。仓库里已有 8 个副本被 Git 跟踪，它们在别的克隆上是陈旧的、且会让 `git status` 把「别人的会话记录」当成需要提交的改动。本任务把这 8 个副本移出版本库，使「`sessions.md` 从不提交」这条规则在**存量**上也成立，而不只是对新文件成立。

## Background / Confirmed Facts

- **8 个副本全部位于 `TaskFlowDocs/achieved/`**：`2026-09-15-release-friction`、`2026-09-27-capability-pre-write-gate`、`2026-10-08-capability-concept-classes`、`2026-10-10-entry-point-silence`、`2026-10-11-evidence-anchor`、`2026-10-17-summarize-state-entry-signal`、`2026-10-22-taskflow-drift-guard`、`2026-10-24-reference-reinforce`。
- **哪一个都不是被 `git add -f` 强行加进来的。** 最早的 `4d260a7`（2026-09-16），最晚的 `1f0ad3e`（2026-10-24）；而 `.gitignore` 里的 `TaskFlowDocs/**/sessions.md` 规则是 `c630536`（2026-10-25）才加的。也就是说这 8 个是规则出现之前正常 `git add -A` 进来的，规则本身没有失效过。
- **规则现在确实是有效的。** 实测：在一个临时任务目录里同时放 `prd.md` 和一个 `sessions.md`，`git add -A -- <dir>` 只暂存 `prd.md`；`git check-ignore -v` 对已跟踪的副本加 `--no-index` 才报告命中（Git 对已跟踪路径不应用 ignore 规则，这是既定行为）。
- **`repository-check` 不在 CI 里跑，只在 `RELEASE.md:52` 与 `CONTRIBUTING.md:8/31` 手工调用。** 因此给它加一条「不应有已跟踪的 `sessions.md`」的断言，不会成为每条 PR 的回归保护——只能是发版和人工治理时的检查。这一点决定了下面 R3 的取舍。
- **`personal.md` 已经被覆盖，不需要处理。** `TaskFlowDocs/repository-docs/*` 的规则把它挡在外面，实测 `git ls-files` 里只有 `index.md`。
- **这一条不是 `TF-20261025-7c5897`（已完成）的重复。** 那一条建了 `hooks/install-git-hygiene`，解决的是**规则写在哪里**（每个克隆的 `info/exclude`）；本条解决的是**已经进入历史的存量**。CHANGELOG 1.1.8 里也把两者分开写了：「Those eight copies stay tracked until `TF-20261025-24d06c` clears them.」
- **`TF-20261025-33b2c4` 已因同一次调查被证伪并删除**（结论：git 对已跟踪路径不应用 ignore 规则，所以「force-added 的副本会被规则藏起来」这件事不可能发生）。本条不重复那个思路。

## Requirements

**R1 — 8 个副本退出索引，但留在磁盘上。** 用 `git rm --cached`，不动工作区文件。文件必须仍然可读：它们是这些任务的历史记录，删除内容不在本条范围内。

**R2 — 不重写历史。** 已经推到 `main` 的提交不改。理由：本条要修的是「当前克隆的 `git status` 噪声」和「别的克隆拿到陈旧副本」，这两件都由「从当前 tip 起不再跟踪」解决；重写历史会改写所有下游克隆的 commit id，代价与收益不成比例，且 `sessions.md` 的泄露面是本机路径与 session id，不含凭据。

**R3 — 不加自动化回归断言。** 依据是 Background 的第 4 条：`repository-check` 不进 CI，加了也不保护 PR；而要把它放进 CI 需要新增一条路径映射，为八个早已不再增长的文件付一次三平台矩阵的成本。规则的**未来**由 `.gitignore` 与 `install-git-hygiene` 承担（实测有效），存量由本条清一次。**我反对**在本条里新增检查；如果之后发现副本又出现，那是规则失效，应当先修规则而不是再加一道断言。

**R4 — 每个克隆看到的语义必须写清楚。** `git rm --cached` 之后，其他克隆 pull 时会看到 8 个文件被删除；它们磁盘上的副本变成未跟踪文件，被 ignore 规则挡住。风险在于：任何克隆里**改过**这 8 个文件的人，其改动会以「文件已删除」的形式静默丢失（未跟踪文件不进 stash、不进 merge 冲突）。这是本条唯一真实的破坏面，必须记录，且必须在 PR 描述里点名。

## Acceptance Criteria

- **A1** `git ls-files | grep 'sessions\.md'` 在合并后的 `main` 上无输出。
- **A2** 8 个文件仍在磁盘上，内容与本任务开始前逐字节相同（用 `git show main:<path>` 比对）。
- **A3** `bash hooks/smoke-test` 通过。特别地：`hooks/smoke-test:3623` 那段「已跟踪副本会保持可见」的断言必须仍然成立——它测的是 `install-git-hygiene` 的语义，不依赖本仓库里有没有真实副本。
- **A4** `git status --porcelain` 在提交后为空；不出现新的未跟踪文件。
- **A5** `CHANGELOG.md` 在 `[Unreleased]` 下记录这一条，措辞点明「这是清理存量，不是改规则」。

## In Scope

- `git rm --cached` 8 个副本。
- `.gitignore` 里那条规则的注释：现在可以补一句「存量已于 2026-10-25 清空」，因为注释里原本写着「八个副本仍被跟踪」。
- `CHANGELOG.md` 一条 `### Fixed`（或 `### Changed`——按 RELEASE.md 的分类习惯）。
- 本任务的 PRD / Plan / 归档。

## Out of Scope

- 重写历史（R2）。
- 在 `repository-check` 或 CI 里新增断言（R3）。
- 改动 `hooks/install-git-hygiene` 或它的规则形状。
- 删除磁盘上的 8 个文件。
- 改动 `sessions.md` 的生成格式或 `hooks/session-record`。

## Risks / Deferred Items

- **R4 的静默丢失面**：其他克隆里对这 8 个文件的本地修改会以「文件已删除」出现，未跟踪副本会被 ignore 规则挡住，`git status` 不会提示。缓解：PR 描述里点名这 8 个路径；本条自己的 PR 会列出清单。**这是本任务唯一的不可逆面**，但不改历史就没有更好的办法——Git 没有「只从我的索引里移除、同时告诉别人他们改过」的机制。
- **八个副本此刻是否真的一致**：`achieved/` 下的任务已归档，理论上没人再改。实测各克隆的副本与本仓库一致程度不在本条范围内，但 A2 只保证「本仓库磁盘上的内容不变」，不保证「其他克隆没改过」。这个缺口由 R4 的文字承担，不由代码承担。
- **后续**：若发现副本重新出现，先查 `install-git-hygiene` 是否在那些克隆上跑过，而不是加断言。

## Open Questions

无。R1–R4 的取舍已在上面给出理由；R3 尤其是一个**主动放弃**的决定，理由是实测得出而不是猜的。
