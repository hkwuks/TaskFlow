# TaskFlow 工作流草案（任务文档与版本管理）

> 状态：待修改草案
>
> 目的：建立一套独立的开发任务文档与版本管理约定，维护需求、设计、实施、验证和证据记录。本文参考公开的 Agent 工作流理念，不依赖特定 CLI、Hook、多 Agent 运行时或自动 Git 操作。
>
> 核心约定：**一个任务对应一个目录；任务材料都放在该目录内；历史版本放在该任务的 `old/`；完成任务整体移动到 `TaskFlowDocs/achieved/`。**

## 1. 核心流程

```text
创建任务
  → 检查并补齐适用的仓库规范
  → 编写 PRD（需求与验收）
  → 调研并保存 Reference（如需要的事实与证据）
  → 编写/确认 spec.md（大型任务必需，小型任务按需）
  → 编写 plan.md（步骤、进度、风险、回滚）
  → 用户批准当前规划
  → 按 Plan 实现
  → 在 Plan 中记录验证与复核
  → 沉淀长期规则
  → 归档到 TaskFlowDocs/achieved/
```

四类信息含义如下：

```text
prd.md     = 要做什么
spec.md    = 本任务采用什么设计和实现契约
plan.md    = 这次怎么做、做到哪、怎样复核
reference/ = 为什么这样做，依据是什么（可选，可容纳多种资料）
```

### 1.1 阅读层级

本文只有一个文件，但按两层阅读：

- **日常规则**：第 1、2、4 至 8、10、11 节。创建、规划、实施、验证和归档任务时按这些规则执行；
- **按需附录**：第 3 节（Task version、Git/file 历史恢复）和第 9 节（会话索引与断点恢复）。仅在升级逻辑版本、恢复历史或跨会话协作时查阅。

这样日常工作只需从当前任务目录读取 `prd.md`、`spec.md`（如有）和 `plan.md`，并按需读取 `reference/` 中的资料或其 `index.md`；不需要每次通读版本和会话细节。

### 1.2 Todo 收件箱与任务提升

`TaskFlowDocs/todo.md` 是仓库唯一且强制的需求收件箱：每个用户请求、GitHub Issue 或其他来源的导入需求，均须先创建或更新 Todo 条目，之后才能匹配任务、澄清、提升或实施。它只保存待办元数据，不保存已提升任务的需求、设计或验证事实。条目按 `inbox → clarified → promoted → in_progress → done/cancelled` 演进。

待办条目至少包含 ID、标题、状态、优先级、负责人、来源、外部编号/链接（如有）、目标、任务链接、下一步和更新时间。批量导入时，按“来源 + 外部编号”去重，但每条不同源需求都必须保留一个 Todo 条目；导入批次只是来源元数据，不能作为一个任务或需求事实源。目标、范围、验收、依赖、规模和适用规范澄清后才能进入 `clarified`；提升时创建任务目录中的 PRD、按需 Spec 和 Plan，回填任务链接，Plan 批准后才能进入 `in_progress`。任务验收通过、目录移入 `achieved/` 后标记 `done`，取消必须写明原因。不得在 Todo 中复制 PRD、Spec 或 Plan 内容。

## 2. 任务目录结构

### 2.1 进行中的任务

```text
TaskFlowDocs/
└── YYYY-MM-DD-short-slug/
    ├── prd.md                         # 必需：需求、范围、验收标准
    ├── spec.md                        # 大型任务必需；小型任务可选
    ├── plan.md                        # 必需：步骤、状态、进度、验证和复核
    ├── sessions.md                    # 推荐：Agent 会话 ID 与恢复入口
    ├── reference/                     # 可选：调研、外部证据、论文、代码勘察和实验输出
    │   ├── index.md                   # 可选：资料较多时使用的导航索引
    │   ├── papers/                    # 可选：论文、论文笔记或 DOI/链接清单
    │   ├── web/                       # 可选：网页、官方文档、竞品资料
    │   ├── codebase/                  # 可选：代码勘察、调用链和实验记录
    │   └── ...
    └── old/                           # 该任务被替代的历史版本
        └── v1/
            ├── version.md             # 必需：该历史版本的元数据和替代关系
            ├── changes/               # 可选：无法由 Git 保留时的 portable diff
            └── snapshot/              # 可选：重要里程碑的完整快照
```

### 2.2 已完成的任务

```text
TaskFlowDocs/
└── achieved/
    └── YYYY-MM-DD-short-slug/
        ├── prd.md
        ├── spec.md                         # 如为大型任务则必需；小型任务可选
        ├── plan.md
        ├── sessions.md
        ├── reference/
        └── old/
```

完成归档是整个任务目录的移动，不是只移动 `prd.md` 或删除中间材料。这样可以保留最终方案、验证证据和被淘汰的历史版本。

已完成任务的目录默认为只读历史。若新的 Todo 条目仍属于该已完成交付物，先将整个目录从 `TaskFlowDocs/achieved/<task>/` 取回到 `TaskFlowDocs/<task>/`，在 `plan.md` 记录 Todo 来源和 `reopen` 原因，归档当前版本并创建新版本，重新获得批准后才修改实现。只有具备独立可发布结果及独立验收标准，或责任边界不同的新需求，才创建关联任务。

### 2.3 目录职责

| 位置 | 回答的问题 | 主要内容 | 何时更新 |
| --- | --- | --- | --- |
| `TaskFlowDocs/<task>/prd.md` | 要做什么，什么算完成 | 目标、背景、需求、范围、验收 | 需求澄清时；重大需求变化时 |
| `TaskFlowDocs/<task>/spec.md` | 这次采用什么设计 | 架构、接口、数据流、不变量、错误契约、实现约束 | 设计确认或设计变化时 |
| `TaskFlowDocs/<task>/plan.md` | 怎么做，现在到哪 | 步骤、状态、进度、风险、回滚、验证和复核 | 每个实施步骤和验证节点 |
| `TaskFlowDocs/<task>/sessions.md` | 上一次由哪个 Agent 做到哪里 | Agent、会话 ID、工作目录、阶段、最后工作点、恢复命令 | 每次开始/结束会话或切换 Agent 时 |
| `TaskFlowDocs/<task>/reference/` | 为什么相信这个方案 | 论文、链接、原始摘录、代码勘察、实验输出 | 调研过程中；无调研可省略 |
| `TaskFlowDocs/<task>/old/vN/` | 之前的版本是什么、何时被替代、为何被替代 | 版本元数据 + Git 范围，或非 Git 模式下的快照/增量 diff | 版本里程碑或重大变更时 |
| `TaskFlowDocs/achieved/<task>/` | 已完成任务的完整记录 | 最终工件和历史版本 | 验收通过后 |

不要为了形式创建空文件：小型任务可省略 `spec.md`，`sessions.md` 和 `reference/` 也按实际需要创建；`prd.md` 和 `plan.md` 是任务的最低要求。`reference/index.md` 不是必需文件，资料较多时可选使用。复核内容直接写入 `plan.md`，不另建 `review.md`。

`reference/` 是唯一允许按资料类型扩展的目录。资料较多时可创建 `reference/index.md` 作为导航入口；没有该文件时，资料文件名和目录结构必须足以说明来源。任何新增资料都应注明文件或 URL、来源类型、关键结论及与当前 PRD/Spec/Plan 的关系。

如果存在 `reference/index.md`，其中对每条资料至少标明 `Status`（`candidate | verified | rejected | superseded | archived`）、来源、采集时间、适用结论、关联工件和 URL/DOI/文件校验信息。外部原文保持不改写；其可信度或失效状态只在索引和团队笔记中更新。Agent 可以提出状态建议；`verified`、`rejected` 或 `superseded` 等结论由 Primary Agent 或用户确认后写入。

`old/` 不是每次编辑都要复制的备份目录，也不应重复保存 Git 已经保留的内容。只有形成新的“逻辑版本”时才建立 `old/vN/`；普通修订留在当前文件，并在 `plan.md` 的变更记录中说明。版本归档有两种等价模式：文档进入 Git 时记录提交范围；文档不进入 Git 时记录基线快照和 unified diff。仅在需要可携式交付或长期冻结证据时，才额外保存 `changes/*.patch` 或 `snapshot/`。详细规则见第 3 节。非 Git 模式下，patch 只覆盖任务作者维护的 Markdown 文档；原始论文、网页快照、图片、压缩包和其他二进制资料保持原样，由资料本身的元信息、文件名或（如有）`reference/index.md` 记录来源和校验信息。

## 3. 版本管理规则

### 3.1 当前版本

`plan.md` 顶部维护当前版本和状态：

```markdown
# Plan — <任务标题>

任务：`TaskFlowDocs/2026-09-03-example/prd.md`
当前版本：v2
状态：`planning | ready | in_progress | checking | completed | blocked`
最后更新：2026-09-03
```

本流程只有一个权威的 **Task version**（例如 v1、v2、v3），由 `plan.md` 顶部维护；`prd.md` 与（如存在）`spec.md` 重复记录该版本，便于单独阅读。版本变化时，所有已存在的核心文档必须同步检查和更新；因任务简单而不存在的 `spec.md` 不参与同步。小修订不递增 Task version，只更新“最后更新时间”和变更记录。Git commit 与 file patch 保存某个 Task version 内的机械历史，不等同于 Task version。

建议当前文件都在标题后采用同一份元数据，便于未来归档时直接保留：

```markdown
> 任务：`YYYY-MM-DD-short-slug`
> 当前版本：v2
> 创建时间：2026-09-02
> 最后更新：2026-09-03
> 状态：`planning | ready | in_progress | checking | completed | blocked`
```

其中的“当前版本”都是同一个 Task version，不分别维护需求版本、设计版本和执行版本。

### 3.2 版本粒度：工作修订、逻辑版本与 Git 历史

不要把每一个改动都编号。采用三级粒度：

- **工作修订**：错别字、补链接、更新复选框、补充验证结果等不改变决策的改动。不创建 `old/` 条目，只更新当前文件的 `Last updated`，必要时在 `plan.md` 的 Change Log 追加一行。
- **逻辑版本**（例如 v1、v2）：目标、范围、验收、核心设计、契约、风险决策或实施结果发生实质变化，或者用户明确否决/批准了一套新方案。逻辑版本才进入 Version History，并需要可恢复的归档记录。
- **Git 提交**：当任务材料允许进入 Git 时，用 Git 保存每一次机械修改的完整历史和 diff；`old/` 只记录人需要理解的版本边界，而不是复制 Git 的职责。设计文档不进入 Git 时，改用文件归档模式。
- **文件归档（无 Git）**：当用户不希望提交设计文档时，第一个被替代的版本必须建立一个完整 `snapshot/` 作为基线；后续被替代版本只保存相邻版本的 patch。每累计约 5 个逻辑版本、跨越重要里程碑，或恢复成本过大时，再创建新的完整快照并从该快照重新开始。这样整个任务通常只有少量完整快照，其余版本都是增量，不需要每个版本都复制全部文档，也不会形成无限长的 patch 链。
- **可携式归档**：如果 Git 历史不会随交付物保留，或者需要对外提交独立证据包，可采用上述无 Git 模式，即使仓库本身使用 Git 也不强制把设计文档提交进去。

因此，连续几轮讨论可以一直维护 v1，不会因为每句话或每个小改动产生一个 `old/vN/`。同一 v1 内的具体修改由 Git diff 查看；v2、v3 等只表示人类决策已经跨过了一个清晰边界。

### 3.3 何时创建新逻辑版本

以下情况不能直接覆盖旧材料，而应创建新版本：

- 需求目标、范围或验收标准变化；
- 用户改变产品、兼容性或风险决策；
- 核心架构、数据流、接口契约或错误语义变化；
- 原方案被否决，换用另一种方案；
- 实施路径发生会影响结果或回滚方式的实质变化。

用户对已批准方案提出修正、否决、新增要求或实质改动时，先把该消息视为变更事件：立即停止当前阶段，判断它是普通工作修订还是上述逻辑版本变化。逻辑版本变化必须先归档当前版本，再原子更新所有已存在的 PRD、Spec、Plan，回到 `ready` 并重新取得批准；不得只改用户提到的一个文件，也不得沿用过期 Plan 继续实施。已完成任务默认只读，除非用户明确授权重开并记录原因。

`old/vN/` 的语义固定为“**如何恢复已被替代的 Task version vN**”。当前版本永远保留在任务根目录，不能同时出现在 `old/` 中。若当前 v1 被 v2 替代，则先建立 `old/v1/`，再把根目录更新为 v2；若当前 v2 被 v3 替代，则建立 `old/v2/`，再更新根目录为 v3。

版本操作顺序（根据文档是否进入 Git 选择归档模式）：

1. 确认当前 PRD、Spec、Plan、Reference 的文件状态；若使用 Git，记录明确的 commit/commit range；若不使用 Git，确认最近的完整 `snapshot/` 或上一个逻辑版本目录；恢复历史版本时必须使用新的临时恢复根目录，不直接覆盖当前任务目录；
2. 在 `old/vN/` 创建 `version.md`，记录归档模式（`git` 或 `file`）、基线、涉及文件、替代原因、变更摘要和查看/恢复命令；
3. `git` 模式只记录提交范围；`file` 模式的第一个归档版本必须在 `snapshot/` 保存完整文件，后续版本在 `changes/` 保存“从上一个被归档版本到本版本”的 unified diff，遇到新的基线节点再保存一个完整 `snapshot/`。`old/vN/` 只保存“如何恢复 vN”：其中的 patch 必须命名为 `from-v<base>-to-vN.patch`，并在 `version.md` 写清输入基线、恢复根目录和恢复结果。非 Git patch 的范围固定为任务文档整体：`prd.md`、`spec.md`、`plan.md`，以及 `reference/` 中团队维护的 Markdown 笔记和索引；不修改或 patch 化下载论文、网页快照、图片、压缩包和其他二进制附件；
4. 如果保存了 `snapshot/`，其中由任务作者编写的 Markdown 必须带版本、时间、状态和替代关系；原始论文、网页快照和二进制附件不改写，来源和校验信息写入其元信息或（如存在）`reference/index.md`；
5. 在当前目录将逻辑版本递增为 `vN+1`，并更新所有已存在的核心文档及其 Version History；
6. 重新执行规划收敛和用户批准门禁。

Task version 升级必须作为一次完整操作完成：先归档旧版本，再一次性更新所有已存在的核心文档、`plan.md` 的版本和状态，最后检查版本一致后才继续实现。若中途失败，保持旧版本并将任务标记为 `blocked`，不得留下部分文档已升级的混合状态。

示例：

```text
TaskFlowDocs/2026-09-03-example/old/v1/   # 被替代的 v1 方案
├── version.md                      # v1 的语义变更、归档模式和恢复方法
└── snapshot/                       # file 模式的首个基线；后续版本改用 changes/*.patch
    ├── prd.md
    ├── spec.md
    ├── plan.md
    └── reference/

TaskFlowDocs/2026-09-03-example/old/v2/   # v2 被 v3 替代后，如何恢复 v2
├── version.md
└── changes/
    └── from-v1-to-v2.patch
TaskFlowDocs/2026-09-03-example/prd.md    # 当前 v3 需求
TaskFlowDocs/2026-09-03-example/spec.md   # 当前 v3 设计
TaskFlowDocs/2026-09-03-example/plan.md   # 当前 v3 计划和复核
```

### 3.4 历史版本包的必需元数据

每个 `old/vN/` 必须有一个 `version.md`。它不是可选说明，而是历史版本的入口文件。它必须声明 `Archive mode: git` 或 `Archive mode: file`：Git 模式提供准确的提交范围；文件模式提供基线快照、相邻 patch 顺序和校验方式。不允许出现无法解释的孤立 patch：

```markdown
# Archived Version v1 — <任务标题>

> 任务：`YYYY-MM-DD-short-slug`
> 版本：v1
> 状态：superseded
> 创建时间：2026-09-02
> 最后更新时间：2026-09-03 10:20 +08:00
> 归档时间：2026-09-03 14:35 +08:00
> 替代版本：v2（当前目录 `../../`）
> 替代原因：轮询方案无法满足延迟和成本约束，改为事件驱动方案。
> 归档模式：`git | file`
> Git 基线提交：`<v1-start-commit>`
> Git 归档提交：`<v1-final-commit>`
> 文件基线（file 模式）：`../v<base>/snapshot/`；若本版本是首个基线则为本目录 `snapshot/`
> Patch chain（file 模式）：`changes/from-v<base>-to-vN.patch`；应用后必须得到 vN
> Restore root（file 模式）：`<新的临时恢复目录>`；不得直接覆盖当前任务目录
> 查看差异：`git diff <v1-start-commit>..<v1-final-commit> -- TaskFlowDocs/YYYY-MM-DD-short-slug/`

## Change Summary
- 需求变化：...
- 设计变化：...
- 验收变化：...
- 兼容性/迁移影响：...

## Archived Materials
- Git 历史：`<v1-start-commit>..<v1-final-commit>`（git 模式必需）
- `changes/from-v<base>-to-vN.patch`：从基线恢复本目录 vN 的可携式增量（file 模式，如存在）
- `snapshot/`：完整冻结副本（file 模式的首个基线或重要里程碑，如存在）
- `reference/`：v1 方案依据（如已冻结在快照中则注明）

## Restore
1. `git` 模式：检出 `Git 归档提交`，或使用 `git diff` 查看该版本；
2. `file` 模式：在新的 `Restore root` 中读取 `File base` 指向的完整快照，按 `Patch chain` 顺序应用到目标版本；
3. 使用 `diff --exit-code` 或等价方式确认恢复结果与目标版本一致；
4. 若存在 `Checksums`，对照其验证重建结果。

## Read This Version When
- 需要理解为何放弃 v1；
- 需要回滚或比较 v1 与 v2；
- 需要复用 v1 的部分设计或证据。
```

如果使用完整快照，其中已存在的 `old/vN/snapshot/prd.md`、`old/vN/snapshot/spec.md`、`old/vN/snapshot/plan.md` 必须可独立阅读，并在标题下保留或补上；小型任务没有 `spec.md` 时不因快照而创建它：

```markdown
> 任务：`YYYY-MM-DD-short-slug`
> 文档版本：v1
> 文档状态：superseded
> 创建时间：2026-09-02
> 最后更新时间：2026-09-03 10:20 +08:00
> 归档时间：2026-09-03 14:35 +08:00
> 已被替代为：v2（见 `../../../spec.md` / `../../../plan.md`）
> 替代原因：<一句话原因>
```

这样即使有人直接打开旧快照中的 `spec.md`，不先看 `version.md`，也能立即知道它不是当前设计、何时失效、被什么替代、为何失效。若该版本仅保存 patch，则这些信息集中写在 `version.md`，并在 patch 文件头部注明版本号和基线。

如果历史快照包含 `reference/`，其历史标记写在 `old/vN/snapshot/reference/index.md`。它的顶部至少包含：

```markdown
# Reference Index — <任务标题>

> 任务：`YYYY-MM-DD-short-slug`
> 资料快照版本：v1
> 资料状态：superseded
> 最后整理：2026-09-03 10:20 +08:00
> 归档时间：2026-09-03 14:35 +08:00
> 已被替代为：v2（见 `../../../../reference/index.md`）
> 替代原因：<与 `../version.md` 一致的一句话原因>
```

索引下逐项列出归档资料的路径或 URL、来源、采集/整理时间、适用结论和校验信息（例如 DOI、访问日期、文件哈希）。若历史版本只保存 patch，则由当前 `reference/index.md`（如存在）与 patch 一起重建索引。`reference/` 中由任务作者编写的 Markdown 笔记，可使用与 PRD/Spec/Plan 相同的归档元数据；外部原文、下载论文、网页快照和二进制附件保持原样，避免把“补版本信息”误变成篡改证据。

### 3.5 不需要新版本的修改

以下修改属于同一版本内维护：

- 修正错别字、格式或链接；
- 补充已经确定的代码路径和文件行号；
- 更新实施进度复选框；
- 记录测试命令和结果；
- 追加不改变决策的验证证据。

### 3.6 日常阅读与精确恢复

版本系统分为“日常阅读”和“历史恢复”两条路径：

- 日常阅读只打开当前任务目录的 `prd.md`、`spec.md`（如有）和 `plan.md`，需要查资料时再打开 `reference/`；若存在 `reference/index.md`，优先从该索引进入。不要求先阅读 `old/` 或逐个 patch。
- 需要审计、回滚或复用旧方案时，先读目标版本的 `old/vN/version.md`，再按其中声明的 Git 范围，或“基线 `snapshot/` + 相邻 patch”恢复。
- `changes/*.patch` 的文件范围只包括 `prd.md`、`spec.md`、`plan.md` 和 `reference/` 中团队维护的 Markdown；外部原始资料不进入 patch。
- 每个 patch 必须在文件头或 `version.md` 中写明：源版本、目标版本、基线位置、生成时间、应用目录和校验值；`old/vN/` 中的 patch 应用结果必须是 vN，而非下一个版本。
- file 模式的 patch 只能在新的临时恢复目录中应用；`version.md` 必须给出恢复根目录、应用顺序和 `diff --exit-code` 或等价的结果校验方式，禁止用历史恢复直接覆盖当前任务目录。

file 模式的推荐生命周期如下：

```text
v1 被 v2 替代：old/v1/snapshot/（v1 的完整基线）
v2 被 v3 替代：old/v2/changes/from-v1-to-v2.patch
v3 被 v4 替代：old/v3/changes/from-v2-to-v3.patch
新的基线：     old/v4/snapshot/（v4 被替代且恢复成本过大或处于重要里程碑时）
```

任务完成并移动到 `TaskFlowDocs/achieved/` 时，任务目录根部保留的当前 `prd.md`、`plan.md` 以及存在的 `spec.md`、`reference/` 就是最终版本，不再复制一套“最终快照”。`old/` 中只保留被替代版本的 `version.md`、patch 和必要的基线快照。

`TaskFlowDocs/achieved/` 中的任务默认作为只读历史。新 Todo 条目若属于其已完成交付物，必须先取回完整目录、记录来源和 `reopen` 原因、归档当前版本并重新批准；不得在 `achieved/` 原地编辑。只有新目标同时独立可发布且有独立验收标准，或责任边界不同，才创建关联任务。

### 3.7 Version History 模板

```markdown
## Version History

- v2 — 2026-09-03：改用事件驱动方案；v1 归档于 `old/v1/`，详情见 `old/v1/version.md`。
- v1 — 2026-09-02：初始规划，采用轮询方案。
```

版本记录必须说明版本号、日期、变化原因、对范围/设计/验收的影响，以及旧版本位置。

## 4. 任务生命周期

```text
planning → ready → in_progress → checking → completed
    │                         │
    └──────── blocked ◄────────┘
```

状态转换规则：

- `planning`：需求、证据或设计仍在澄清；
- `ready`：当前版本的 PRD、Spec（如需）和 Plan 已收敛，**等待用户批准**；
- `in_progress`：用户已批准当前版本，正在实现；
- `checking`：实现完成，正在按验收标准复核；验证失败时回到 `in_progress`，无法继续时转为 `blocked`；
- `completed`：任务验收通过，满足完成门禁；之后执行目录移动到 `TaskFlowDocs/achieved/`；
- `blocked`：存在明确阻塞，已记录最小复现、已尝试方案和所需输入；阻塞解除后回到被阻塞前的工作阶段。

状态写入 `plan.md`，不要只留在聊天记录中。没有 PRD 不能进入 `ready`，没有验证记录不能进入 `completed`。

`ready` 不等于已批准；没有用户批准不得进入 `in_progress`。批准记录写入 `plan.md` 的 `Approval` 区域。

## 5. 阶段一：需求澄清与 PRD

### 5.1 是否创建任务

以下情况创建 `TaskFlowDocs/<date>-<slug>/prd.md`：

- 新功能、复杂 Bug、重构或跨模块变更；
- 需要多次会话或多人协作；
- 存在多个合理方案、兼容性风险或外部依赖；
- 需要保留调研、决策和验收证据。

单文件小修可以不创建完整任务，但仍需有明确目标和最小验证。

任务规模判定：涉及多个模块或文件、架构/API/数据流/兼容性/错误语义、需要多次会话，或预计超过约 30 分钟的任务视为大型任务，必须创建 `spec.md`；单文件、边界明确且可在一次短会话内完成的小型任务可以省略 `spec.md`，但必须在 `plan.md` 写明 `No spec required` 及理由。

任务 ID 使用 `YYYY-MM-DD-short-slug`。创建后默认不可重命名；同日同 slug 冲突时追加序号或更具体的 slug。开始工作前先搜索活跃任务：推进既有交付物、计划步骤、开放问题、验证或后续事项时维护原任务；同一交付物的实质修改升级 Task version 并重新批准。只有同时具备独立验收标准和可独立发布的结果，或责任人/问责边界不同，才创建关联任务。混合请求先提出拆分并等待用户选择；新会话或新 Agent 不是新任务触发条件。

### 5.2 先查事实，再问决策

向用户提问前，先检查当前实现、调用方、测试、配置、README、既有任务、Git 状态以及工作树中的未提交改动。

将结果分成：

```text
已确认事实：代码、测试或文档可以证明
用户决策：目标、范围、体验、兼容性、风险偏好
技术未知：需要调研或实验
明确不做：本任务排除的事项
```

### 5.3 仓库文档与规则引导

仓库文档统一入口是 `TaskFlowDocs/repository-docs/index.md`，不再保留独立的 `standards/` 层。目录条目标记为 `repository-rule`、`repository-guidance` 或 `personal-supplement`，按需链接仓库已有的 README、CONTRIBUTING、代码规范、发布、路线图、PR 和 CI 文档。

在规划或实施非简单任务前，先判断适用类别：所有非简单任务检查开发流程；改代码时检查代码规范；涉及 commit、PR 或远程仓库时检查提交/PR 规范；涉及架构、UX、API 或数据契约时检查设计规范。若仓库缺失任务所需规则，暂停实施并引导用户制定范围匹配的个人补充；每轮最多问三个按依赖顺序的问题，并给出推荐答案。默认顺序是开发流程、代码、提交/PR、设计。

用户确认后，只在 `TaskFlowDocs/repository-docs/personal/` 创建确认的补充文件并从 `index.md` 链接。每个补充至少包含 `Scope`、`Repository documents checked`、`Rules`、`Verification`、`Exceptions / Change control`；提交相关补充还必须包含 `Commit format` 和 `PR checks`。补充规则只能更严格或正交，不能弱化、覆盖或冲突仓库文档；发现冲突立即暂停并询问用户。用户明确不采用某类规则时，记录豁免，不能创建空文件。

面向 PR 或远程仓库时，还应检查可访问的贡献指南、PR 模板、CODEOWNERS、分支/CI 规则和平台元数据。远程发现结果是候选信息，经审阅后再写入本地规范；不可覆盖本地规则、不可因访问失败而声称已同步、不可写入密钥或私有数据。

### 5.4 PRD 内容

`prd.md` 只描述需求，不承载完整技术设计、进度或原始调研材料：

```markdown
# <任务标题>

## Goal
要解决的问题、用户价值、完成后的可观察结果。

## Background / Confirmed Facts
已从代码、测试、配置或文档确认的事实。

## Requirements
- R1 ...

## Acceptance Criteria
- [ ] AC1：可通过命令或行为观察验证

## In Scope
- ...

## Out of Scope
- ...

## Risks / Deferred Items
- ...

## Open Questions
- 只保留会阻塞规划的用户决策

## Version History
- v1 — YYYY-MM-DD：初始版本。
```

### 5.5 规划收敛门禁

进入 `ready` 前必须满足：

- Goal 和用户价值明确；
- In Scope / Out of Scope 明确；
- Acceptance Criteria 可观察、可测试；
- 用户拥有的产品、兼容性和风险决策已解决；
- 技术未知已写入 `reference/`，或明确延期；
- 如果任务涉及架构、接口、数据流、兼容性、错误语义或跨模块约束，设计和契约已写入/确认 `spec.md`；如果不涉及这些内容，`plan.md` 明确记录 `No spec required` 及理由；
- 实施顺序、风险、回滚和验证命令已写入 `plan.md`；
- 已读取适用的仓库规范；缺失规范已由用户确认创建，或已记录明确豁免；
- PRD 已做一次收敛整理，没有重复或已解决的开放问题；
- 当前版本已经提交给用户批准；获得批准后才从 `ready` 进入 `in_progress`。

规划摘要至少包括：Goal、范围、验收标准、关键决策、风险、延期项、当前版本和工件路径。

## 6. 阶段二：Spec、Plan 与实现

### 6.0 可选工具的接入边界

本流程是任务级的**组织、持久化和治理框架**。任何 Skill、CLI、Hook 或 Agent 都可以按任务需要选用，但本文不规定它们的执行流程。框架只定义任务工件、版本、状态、批准门禁和归档；工具产生的任务结论须审阅后写入对应工件。

```text
TaskFlow：任务目录、事实源、状态、版本、会话、归档和权限边界
    └── 可选工具：按需协助调研、设计、实施、验证或审查
```

如任务使用其他工具，先确认其输入、输出和权限边界，再读取当前任务的 `prd.md`、`spec.md`（如有）和 `plan.md`。职责分工如下：

- **框架拥有**：任务 ID 与目录、PRD/Spec/Plan/Reference/Sessions/old 的位置、任务状态、用户批准门禁、Git 或 file 的版本策略、会话恢复、完成归档，以及自动化工具的写入和权限边界；任务 ID 创建后默认不可重命名，只有达到既有任务分流表定义的独立成果/责任边界才创建关联任务。
- **可选工具拥有**：其自身的执行方法、配置和生命周期；
- **任务文档拥有**：本次任务的目标、范围、决策、进度、验证结果和证据。工具不能替代 PRD、Spec 或 Plan，也不能把一次任务的临时决定直接写回通用配置；多能力任务的 Capability Map 写入 `prd.md` 的范围/概览区域或 `spec.md` 的模块边界区域，不默认拆成多个根级 Spec 文件。
- `plan.md` 可选记录使用的工具及其角色；工具更新不会自动改写历史任务；
- 任务文档仍须遵守项目安全、权限和用户明确约束；任何工具均不能自行扩大操作范围、跳过批准门禁、私自提交不允许进入 Git 的文档，或覆盖/删除任务历史；
- 通用工具参考资料与任务的 `reference/` 不混用；后者只保存本次任务的论文、网页、代码勘察和实验依据。

#### 6.0.1 任务级输出路由

外部工具的默认文件名或根级路径不构成任务事实；在本项目中，所有任务产物必须路由到当前任务目录，任务目录是唯一事实源：

| 任务产物 | 本项目输出位置 | 说明 |
| --- | --- | --- |
| PRD / requirements | `TaskFlowDocs/<task-id>/prd.md` | 需求、范围、验收和开放问题 |
| Spec / design | `TaskFlowDocs/<task-id>/spec.md` | 按本流程的 Spec 条件创建 |
| Plan、task list、checkpoint、review | `TaskFlowDocs/<task-id>/plan.md` | 同一文件分区维护；未提升的待办保留在 `TaskFlowDocs/todo.md` |
| 调研和外部证据 | `TaskFlowDocs/<task-id>/reference/` | 资料较多时可用 `reference/index.md` 导航 |
| 会话恢复信息 | `TaskFlowDocs/<task-id>/sessions.md` | 可选，不保存聊天原文 |

不得因使用工具而自动创建第二份根级 Plan、Spec 或 Review 作为并行事实源；`TaskFlowDocs/todo.md` 是唯一允许的仓库级 Todo 收件箱，但只能保存元数据和任务链接。

Hook、Slash Command、Persona 和自动化编排可以用于加速过程，但其输出和副作用同样必须遵守此路由及权限边界；它们不是任务状态和历史的独立来源。

#### 6.0.2 并发写入规则

并行 Agent 可以读取同一任务、维护各自的 `sessions.md` 条目，或产出独立的临时调研/审查材料；但同一时刻，`prd.md`、`spec.md`、`plan.md` 和 `reference/index.md` 只能由一个明确的写入负责人修改。涉及这些核心文档的合并、Task version 升级、任务阶段变更和批准记录，由 `Primary` Agent 或用户统一完成。并行产出的结论必须先由负责人审阅后再写入核心文档。

写入负责人交接时，当前负责人先更新自己的 `sessions.md` 条目，并在 `plan.md` 记录最后完成步骤、下一步和未提交变更；新负责人确认已读取当前 PRD、Spec（如有）、Plan 与 Reference（如有）后，由 Primary Agent 或用户明确接手。交接完成后，旧负责人不得继续修改核心文档。

### 6.1 Spec 的边界

任务 `spec.md` 保存本任务采用的设计和实现约束：

- 架构边界和模块职责；
- 数据流、接口、事件或数据库契约；
- 不变量、兼容要求和错误语义；
- 关键设计取舍及其原因；
- 需要遵守的代码模式和测试要求。

如果某条规则经过多个任务验证，确实有跨任务价值，再另行提炼到项目公共规范位置；不要把未经验证的临时想法写成全局规则。公共规范的实质变更与任务目标、范围、契约或风险变更一样：先归档当前 `old/vN/`，再原子更新核心文档、回到 `ready` 并重新获得批准；不得直接扩展已完成任务。

### 6.2 Plan 的边界

`plan.md` 保存本次任务的执行记录，不重复抄写完整 Spec：

```markdown
# Plan — <任务标题>

任务：`TaskFlowDocs/<date>-<slug>/prd.md`
当前版本：v1
状态：planning
最后更新：YYYY-MM-DD

## Spec Pointers
- `spec.md`
<!-- 若不需要 Spec：写 No spec required，并说明理由 -->

## Reference Pointers
- `reference/`（如存在；`reference/index.md` 仅在资料较多时使用）

## Related Tasks
- Depends on: `<task path or None>`
- Blocks: `<task path or None>`
- Related: `<task path or None>`

## Skills Used (Optional)
| Skill | Revision / source | Why used |
| --- | --- | --- |
| `...` | `...` | `...` |

## Preconditions
- 必须读取的规范
- 分支/工作树要求

## Approval
- Approved by: <user / role>
- Approved at: YYYY-MM-DD HH:mm +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan
- Notes: ...

## Steps
### Step 0 — 事实确认
- 目标：确认需求、现状和实施前提，消除会影响方案的未知。
- 依赖：无。
- 文件范围：预计读取或修改的路径。
- 实施项：
  - [ ] ...
- 验收：事实、假设和待确认项已记录，且没有未暴露的关键歧义。
- 验证：`<command>` / 代码勘察 / 用户确认。
- 回滚点：不修改代码；撤销本步骤新增的勘察记录即可。
- 状态：`pending | in_progress | done | blocked`

每个 Step 的 `实施项` 是必须逐项勾选的 checklist。所有必选项未完成，或聚焦验证未通过时，Step 不得标记为 `done`。

### Step 1 — <最小变更>
- 目标：本步骤完成后用户或系统获得的能力。
- 依赖：Step 0 / 无。
- 文件范围：预计涉及的代码、配置、测试或文档路径（尽量不超过 5 个文件）。
- 实施项：
  - [ ] ...
- 验收：本步骤必须成立的可观察条件。
- 验证：`<focused test command>` / 手工验证步骤。
- 回滚点：失败时回退到的提交、文件状态或数据状态。
- 状态：`pending | in_progress | done | blocked`

## Checkpoints

### Checkpoint 1 — <阶段名称>
- [ ] 前置步骤完成且工作树处于可验证状态。
- [ ] 相关测试、构建或手工场景通过。
- [ ] 如存在 `spec.md`，与 PRD 验收标准和 Spec 契约的偏差已记录；不存在时已确认 `No spec required` 仍成立。
- [ ] 用户批准继续下一阶段（如该阶段要求批准）。

## Verification / Review
<!-- 记录命令、结果、基线失败、新增失败和未覆盖项 -->

## Follow-ups
- ...

## Version History
- v1 — YYYY-MM-DD：初始计划。
```

### 6.3 实现前检查

1. 阅读当前任务的 `prd.md`；
2. 如果存在 `spec.md`，阅读任务 `spec.md`；如果 Plan 标记 `No spec required`，确认其理由；
3. 如果存在 `reference/`，按需阅读其中资料；如果存在 `reference/index.md`，先阅读该索引；
4. 阅读 `plan.md`，确认当前状态和下一步；
5. 阅读 `TaskFlowDocs/repository-docs/index.md` 及本次任务适用的仓库文档/个人补充；若任务所需规则缺失、不完整且未明确豁免，回到规则引导；
6. 如果代码或任务材料进入 Git，查看 Git 状态，避免覆盖其他改动；如果设计文档采用 file 模式，检查基线、patch 与当前文档的对应关系；
7. 若目标、范围、契约、风险或适用规范的实质内容发生变化，停止实现，创建新版本并回到规划门禁；不得直接扩展已完成任务。

### 6.4 实现边界

- 只修改 PRD 范围内的代码和文档；
- 不顺手重构无关代码；
- 不擅自改变公共 API、事件顺序、数据格式或错误语义；
- 新增命令、配置、事件字段或跨层契约时，大型任务先在 `spec.md` 写清输入、输出、校验和失败行为；小型任务若仍无需 Spec，则在 `plan.md` 中记录这些约束及 `No spec required` 理由；
- 每个逻辑步骤完成后运行最小相关检查，并把结果写入 `plan.md`；
- 不以“测试通过”替代需求验收；
- 默认不自动 commit、push、删除或覆盖用户文件。

## 7. 阶段三：验证与复核

### 7.1 验证顺序

1. 如果代码或任务材料进入 Git，运行 `git diff --name-only` / `git status` 确认改动范围；如果设计文档采用 file 模式，检查基线快照、patch、校验值和恢复结果；代码与文档使用不同存储时分别验证两套范围；
2. 对照 `prd.md`：逐条检查需求和验收标准；
3. 如果存在 `spec.md`，对照它检查设计、契约、错误和兼容约束；没有 `spec.md` 时，确认 Plan 中 `No spec required` 的理由仍然成立；
4. 对照 `plan.md`：检查步骤、进度、偏离说明和回滚点；
5. 如果存在 `reference/`，按需核对其中的关键证据；存在 `reference/index.md` 时同时核对其索引记录；
6. 运行项目规定的 lint、类型检查、单元测试、集成测试和端到端场景；
7. 检查调试代码、临时绕过、未覆盖分支和无关改动。

### 7.2 验证矩阵

所有验证与复核直接写入 `plan.md`，不另建 `review.md`：

| 检查项 | 命令/证据 | 结果 | 备注 |
| --- | --- | --- | --- |
| 需求 AC1 | `...` | PASS/FAIL | ... |
| Spec 契约 | `...` | PASS/FAIL | ... |
| 静态检查 | `...` | PASS/FAIL | ... |
| 类型检查 | `...` | PASS/FAIL | ... |
| 单元测试 | `...` | PASS/FAIL | 基线失败/新增失败 |
| 集成测试 | `...` | PASS/FAIL | ... |
| 回归路径 | 场景名或手工步骤 | PASS/FAIL | ... |

明确区分：

```text
既有失败：变更前已有，并有基线证据
新增失败：由本次变更引入，必须修复或重新评估
环境失败：依赖、网络、服务或权限导致，记录重现条件
```

### 7.3 失败处理

- 可以在当前范围内修复：修复并重新验证；
- 暴露需求或设计缺口：更新 PRD/Spec，必要时创建新版本并重新获得批准；
- 同一问题反复失败：记录最小复现、已尝试方案和阻塞输入，停止盲目试错；
- 无法验证：不得宣称完成，保持 `checking` 或标记 `blocked`。

## 8. 阶段四：沉淀与 Achieved 归档

### 8.1 是否沉淀到长期规范

只把跨任务仍然有效、且已经验证过的内容提炼到项目公共规范位置：稳定接口、数据和错误契约；反复适用的架构边界或目录规则；有证据的工程约定；以及经过验证的设计决策。

一次性上下文、个人偏好、未验证猜测和任务临时 workaround 留在当前任务的 `spec.md`、`plan.md` 或 `reference/`，不要污染公共规范。

### 8.2 完成门禁

移动到 `TaskFlowDocs/achieved/` 前必须满足：

- [ ] PRD 的每个验收标准已逐条验证；
- [ ] `plan.md` 记录了命令、结果、基线失败、新增失败和未覆盖项；
- [ ] 如存在 `spec.md`，实现与当前 Spec 一致，偏离处已说明；
- [ ] 未解决事项已转为明确 Follow-up 或阻塞说明；
- [ ] 可复用经验已提炼，临时信息未写入公共规范；
- [ ] 当前任务版本和 Version History 完整；
- [ ] 所有已存在的核心文档使用同一个 Task version；小型任务没有 `spec.md` 时不为同步而创建；
- [ ] Git 改动范围已经人工确认；
- [ ] 若任务文档未进入 Git，已确认最近基线、相邻 patch 和当前文件可恢复；
- [ ] 若任务目录将被移动，已更新已知的跨任务引用；`sessions.md` 中的工作目录和恢复命令仍然可解释；
- [ ] 归档前确认没有其他 Agent 正在写入核心文档，且目录移动已获授权；
- [ ] 已完成任务的当前根目录保留最终文档，且不删除 `old/` 中的历史版本；
- [ ] 若保留 `sessions.md`，已将失效会话标为 `closed` / `unavailable`，并保留仍有审计价值的恢复入口；
- [ ] 任务状态改为 `completed`；
- [ ] 整个任务目录移动到 `TaskFlowDocs/achieved/<task>/`。

归档后不要删除 `old/`。已完成任务是可检索的工程记录，不是临时缓存。

## 9. Agent 会话记录与断点恢复

### 9.1 会话记录边界

需要跨会话继续、切换 Claude/Codex 等 Agent，或需要保留可复查的 Agent 工作上下文时，在任务根目录创建 `sessions.md`。它是**会话索引**，不是聊天日志、提示词转储或第二份 Plan：

- 记录能够恢复会话所需的最小信息：平台、会话 ID、启动时间、最后活动时间、工作目录、任务版本、阶段、最后工作点、下一步和恢复命令；
- 不复制用户对话、模型思考过程、密钥、终端完整输出或外部服务令牌；这些内容仍由各平台自己的会话存储负责；
- 任何 PRD、Spec、Plan、Reference、Sessions、snapshot 或 patch 都不得包含密钥、令牌、个人隐私、客户数据或未经授权的敏感信息；需要保留时使用脱敏占位符，并记录受限原始资料的位置。
- 会话记录不替代 `prd.md`、`spec.md`、`plan.md`。任何已确认的需求、设计、进度或验证结论仍要落在对应任务文档中；
- `sessions.md` 只保留当前任务可恢复或具有审计价值的会话。过期、不可恢复且没有独特证据的会话可从索引移除，并在 `plan.md` 简述其结论；
- 会话 ID 不属于设计版本本体，不随每次 `old/vN/` 复制；如果某个历史版本只能通过特定会话理解，在对应 `old/vN/version.md` 中链接该会话记录即可。
- 会话 ID 通常受平台、账号、机器和本地会话存储限制；迁移到另一台机器或另一种 Agent 前，必须确认该平台仍能访问该会话。不能把 Codex ID 当作 Claude ID，也不能假设不同平台之间可以直接 resume。
- `sessions.md` 分开记录 `Code working directory`（代码仓库路径）和 `Task artifact directory`（当前任务文档路径）；任务归档移动后前者通常不变，后者应更新为 `TaskFlowDocs/achieved/<task>/`。

### 9.2 `sessions.md` 模板

```markdown
# Sessions — <任务标题>

> 任务：`YYYY-MM-DD-short-slug`
> 当前任务版本：v2
> 最后更新：2026-09-04 10:20 +08:00

## Active / Resumable

### S1 — Codex

- Status: resumable
- Primary: yes | no
- Session availability: `local-only | account-scoped | shared | expired`
- Session ID: `019...-...`
- Started: 2026-09-04 09:00 +08:00
- Last active: 2026-09-04 10:20 +08:00
- Code working directory: `/absolute/path/to/project`
- Task artifact directory: `TaskFlowDocs/YYYY-MM-DD-short-slug/`
- Task version / phase: v2 / `in_progress`
- Last completed: 已完成 Step 2，验证结果写入 `plan.md`
- Next step: 执行 Step 3
- Resume: `codex resume 019...-... -C /absolute/path/to/project`
- Notes: 先读取 `prd.md`、`spec.md`、`plan.md`；工作树有未提交改动。

### S2 — Claude

- Status: resumable | closed | unavailable
- Primary: yes | no
- Session availability: `local-only | account-scoped | shared | expired`
- Session ID: `<Claude session identifier>`
- Started / Last active: ...
- Code working directory: ...
- Task artifact directory: ...
- Task version / phase: v2 / `checking`
- Last completed / Next step: ...
- Resume: `<根据该 Claude 客户端当前文档填写的恢复命令>`
- Notes: ...

## Closed / Reference Only

| ID | Agent | Closed at | Useful conclusion | Related task version |
| --- | --- | --- | --- | --- |
| S0 | Codex | 2026-09-03 18:00 +08:00 | 完成 v1 方案比较，结论已写入 `spec.md` | v1 |
```

并发规则：每个 Agent 只更新自己的会话条目；不得覆盖其他 Agent 的最后工作点或下一步。`Primary`、任务阶段和冲突处理由主 Agent 或用户维护；会话结束时集中更新一次即可，不要求每条消息都写文件。需要并行协作时最多指定一个 `Primary: yes` 会话；如果出现多个候选，先人工选择再继续。

Codex 当前 CLI 支持按 ID 恢复：

```bash
codex resume <SESSION_ID> -C <working-directory>
```

也支持 `codex resume --last`，但它依赖本机最近会话顺序，不适合写入任务文档作为确定性恢复入口。其他 Agent 只记录其当前客户端实际支持的会话 ID 和恢复命令；不要假设 Claude、Codex 或未来工具共享同一种 ID 或命令格式。

### 9.3 断点恢复

新会话、上下文压缩或中断后，按以下顺序恢复：

1. 定位 `TaskFlowDocs/<task>/` 或 `TaskFlowDocs/achieved/<task>/`；
2. 如存在 `sessions.md`，先读取最近的 `resumable` 会话，确认 Agent、会话 ID、工作目录、当前阶段和恢复命令；
3. 先决定是否恢复该会话；即使恢复成功，也必须继续读取任务文档，不能只依赖聊天上下文；
4. 读取 `plan.md` 顶部的当前版本和状态；
5. 读取当前版本的 `prd.md`；
6. 如果存在 `spec.md`，读取 `spec.md`；如果 Plan 标记 `No spec required`，确认该理由仍然成立；
7. 如果存在 `reference/`，按需读取其中资料；存在 `reference/index.md` 时先读取该索引；
8. 查看 Plan 中最后一个已完成步骤、下一步和未解决项；
9. 如果代码或任务材料进入 Git，检查 Git 状态；如果设计文档采用 file 模式，检查基线、patch 和恢复条件；
10. 若文档状态与代码证据不一致，先修正文档或回到规划阶段，不直接继续改代码。

恢复摘要：

```text
任务：...
当前版本：...
当前阶段：...
已完成：...
下一步：...
阻塞：...
工作树风险：...
可恢复会话：...
```

## 10. 默认不纳入的自动化能力

本流程默认不纳入特定产品的 CLI、自动状态机、Hook、自动上下文注入、专用子 Agent、多 Agent channel、跨会话原始日志索引、多平台模板同步、自动 Git commit/push/归档或远程任务同步。其他工具如被采用，只需遵守本文任务工件、权限和事实源规则。

未来如需增加其中任何一项，先定义权限边界、失败回滚、并发写入规则、数据流向和验收标准。其他工具的专属配置、命令和生命周期不由本文代为管理。

## 11. 一页版执行清单

### 创建任务

- [ ] 先在 `TaskFlowDocs/todo.md` 创建或更新本次请求的 Todo 条目；批量导入时每条源需求各有一条记录
- [ ] 建立 `TaskFlowDocs/<date>-<slug>/prd.md`
- [ ] 如需跨会话或跨 Agent 协作，建立 `sessions.md` 并记录当前会话 ID 与恢复入口
- [ ] 勘察代码、测试、配置、文档和 Git 状态
- [ ] 搜索活跃与 achieved 任务并判断维护、取回版本化或提出拆分；检查 `TaskFlowDocs/repository-docs/index.md`；缺失适用规则时先引导用户制定个人补充或记录豁免
- [ ] 区分确认事实、用户决策、技术未知和明确不做
- [ ] 编写目标、范围和可观察验收标准

### 规划

- [ ] 如需调研，证据放入 `reference/`；资料较多时建立或更新 `reference/index.md`
- [ ] 大型任务将设计、架构和契约放入 `spec.md`；小型任务在 `plan.md` 写明 `No spec required` 及理由
- [ ] 步骤、进度、风险、回滚和命令写入 `plan.md`
- [ ] 如使用其他 Skill 或工具，确认其产物已路由到当前任务目录
- [ ] 当前版本通过规划收敛门禁
- [ ] 用户批准当前版本规划

### 实现

- [ ] 读取当前 `prd.md`、`spec.md`（如有）、`reference/`（如有；存在 `index.md` 时先读索引）和 `plan.md`
- [ ] 按需读取本次使用工具的必要资料；不把任务临时决定写回通用配置
- [ ] 只修改任务范围内内容
- [ ] 每个逻辑步骤更新 Plan 并运行最小检查
- [ ] 每次会话结束或切换 Agent 时，更新 `sessions.md` 的最后工作点、下一步和恢复状态
- [ ] 需求或设计实质变化时，创建 `old/vN/version.md`；Git 模式记录提交范围，file 模式记录基线与相邻 patch；只有需要可携式归档时才附加 patch 或快照
- [ ] 适用规范的实质变化同样先归档 Task version、更新核心文档并重新获得批准；不直接扩展 `completed` 任务
- [ ] 与其他 Agent 交接时，先由当前负责人更新 `sessions.md` 和 `plan.md`，再由 Primary Agent 或用户确认新的核心文档写入负责人

### 验证与完成

- [ ] 逐条对照 PRD 验收标准，并在存在 Spec 时对照其契约
- [ ] 运行适用的静态检查、类型检查、测试和回归场景
- [ ] 区分既有失败、新增失败和环境失败
- [ ] 记录验证证据和未覆盖项
- [ ] 状态改为 `completed`，整体移动到 `TaskFlowDocs/achieved/`，同步 Todo 的 `Task:` achieved 路径和 `done` 状态，并核对活动路径不存在、归档路径存在且根 PRD/Plan 状态一致
- [ ] 保留 `old/` 历史版本和 Follow-up

## 12. 设计来源与独立性声明

本文参考公开的 Agent 工作流理念，形成自己的任务文档与版本管理模型：

```text
定义 → 规划 → 实施 → 验证 → 归档
```
