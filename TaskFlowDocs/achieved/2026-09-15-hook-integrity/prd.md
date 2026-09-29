# Hook integrity: unpolluted archives, unbypassable gates, user-language documents
> Task version: v2
> Status: completed

## Goal

修掉本轮实测发现的三个 hook 缺陷：`hooks/version` 把"被取代之后"的工作区内容当成旧版本归档；`task complete` 和 `task progress` 可以绕过批准门禁；任务文档正文使用英文，而用户惯用中文。前两个是正确性缺陷，第三个是产出可读性缺陷。

v2 修订第三个方向的规则本身：v1 把"章节标题"整体划入必须英文的一侧，而实测只有少数标题被 hook 按名字匹配。v2 把英文边界改成**显式名单**，其余章节标题归入正文散文、跟随用户语言；同时把规则在历史中的不可检索问题一并修掉。

## Background / Confirmed Facts

三个问题都在本轮排查中实测复现，不是推断：

- **归档污染。** `hooks/version` 从**工作区**复制被取代的核心文档。实测：先按 v2 修改 `prd.md`（写入 `V2 CONTENT ALREADY WRITTEN`），再跑 `version ... v2 prd.md`，归档出的 `old/v1/prd.md` 里带着这条 v2 内容；`old/v1/plan.md` 同样带着 v2 的 `- Status: done`。也就是说 `old/v1/` 记录的不是 v1 被批准时的样子，而是 v1 被替换后的残留。本仓库的 `2026-09-15-no-python-hooks/old/v1/` 就是这样产生的，后来手工从提交 `9c26465` 重建。
- **门禁可绕过。** `task state in_progress` 校验 `Approval: approved` 且 `Approved version` 等于当前版本，但 `task complete` 只校验"没有未勾选项 + 没有未完成 Step"，完全不看 Approval。实测：一个 `Approval: requested / Approved by: pending` 的全新任务，把 checklist 勾上、Step 标 done 后，`task complete --user-accepted` 返回 `complete OK` 并成功归档。实例：`TaskFlowDocs/2026-09-14-macos-hook-portability/` 的 Approval 是 `requested`，Step 是 `done`，现在跑 `complete` 就会通过。
- `task progress` 没有任何门禁。实测：在 `> Status: planning`、Step 仍为 pending 且**从未批准**的任务上，`task progress <task> 1 done` 返回 `progress OK`，把 Step 写成 done、并在 `## Verification / Review` 追加行。
- **语言。** `CODE_STYLE.md` 只要求"英文与中文 README 行为一致"，没有规定任务文档语言。本仓库全部 26 个 achieved 任务文档都是英文正文，而用户的工作语言是中文。
- 用户本轮确认的三个方向：被跟踪文件有未提交改动就拒绝归档；`complete` 与 `progress` 都补批准检查；任务文档结构行保持英文、正文用中文。
- 影响面已核对：现有活跃任务中 `session-id-record`、`untrack-workflow-draft` 的 Approval 是 `approved`，两个待归档任务（no-python-hooks、todo-merge-driver）也是 `approved`；本轮新增的批准检查不会误拦它们。仅 `macos-hook-portability` 等 `requested` 任务会被拦——那正是期望行为。

### v2 新增的确认事实（本轮复核 `origin/main` @ `65ddd0a`）

- **规则写宽了。** v1 的 R4 把"章节标题"整体列为英文。实测 hooks 按**精确名字**匹配的章节标题只有这几个：`## Approval`（`hooks/task:508,829,907`、`hooks/version:113,141`、`hooks/summarize-state:105`）、`## Skills / Tools Used`（`hooks/task:647,837`）、`## Verification / Review`（`hooks/task:295`）、`## Change Log`（`hooks/reopen:23`）、`## Items` / `## Removed`（`hooks/task:214,222,378,394,401`、`hooks/todo-check:61`）、`## Active / Resumable` / `## Closed / Reference Only`（`hooks/session-record:269,276,282`）；另有 `### Step N — …` 与 `### SN — …`。`## ` 前缀在 `hooks/task:283`、`hooks/summarize-state:127` 只被当作**章节边界**使用，与文字无关。
- **其余大纲标题没有任何 hook 匹配。** `## Requirements`、`## Acceptance Criteria`、`## In Scope`、`## Out of Scope`、`## Risks / Deferred Items`、`## Open Questions`、`## Version History`、`## Preconditions`、`## Steps`、`## Checkpoints`、`## Follow-ups`、`## Related Tasks` 等均无人解析——它们保持英文只是规则措辞的结果。
- **`promote` 写出整个大纲。** `hooks/task:604-710` 一次性写出 PRD 10 个、Plan 15 个、Spec 9 个标题，全为英文。所以"保留英文骨架"在任何情况下都成立，**本次修订不产生可观察的行为变化**；收益是规则准确、不再把可翻译的标题误列为英文。
- **规则在历史中不可检索。** 该规则由提交 `87c30e5` 引入，其 message 为 `fix: require an approval before progress and completion`，`CHANGELOG.md` 全文无 language 相关条目，`git log -S"working language"` 只命中这一个语义错配的提交。用户因此把它记成了一次 code style 改动。

## Requirements

- R1：`hooks/version` 在归档任一核心文档前，若该文档**被 Git 跟踪且工作区或暂存区有未提交改动**，必须在任何写入之前失败并说明原因；未被跟踪的文档（file-mode，文档不进 Git）不受此限。
- R2：`task complete` 必须校验当前 Plan 的 Approval 为 `approved`、`Approved version` 等于当前 Task version、`Approved by` 不是 `pending`；不满足则在任何写入前失败。
- R3：`task progress` 使用与 `task state in_progress` 同一套批准校验，理由与拒绝文案保持一致。
- R4（v2 修订）：`SKILL.md`、`references/artifacts.md`、`CODE_STYLE.md` 记录文档语言规则，且英文边界以**显式名单**表达，而不是"章节标题"这类整体表述：名单 = 被 hook 按名字匹配的章节标题与条目标题、`## Approval` 的五个字段、Todo 字段名、`> Task version:` / `> Status:` / `> Current Task version:` 等行、`- Status:` 行、`- [ ]` / `- [x]` 标记。正文散文用用户惯用语言，**未被 hook 匹配的章节标题也归入正文**。已写好的英文文档不回改。
- R5：规则必须明说 `hooks/task promote` 写出的英文骨架标题不受语言规则影响（骨架由 hook 生成，不是 Agent 按规则写的正文），避免读者以为"标题跟随用户语言"这条规则对新建文档生效。
- R6：`bash hooks/smoke-test` 把 R4 的名单钉住，并新增一条**行为**断言：把一个未被 hook 匹配的章节标题（如 `## Checkpoints`）翻译成中文后，`hooks/task` 的解析命令仍然正常工作。
- R7：`CHANGELOG.md` 有一条可检索的记录，说明语言规则及其 v2 收窄，补上 v1 落地时缺失的变更记录。

## Acceptance Criteria

- 在一个被跟踪且有未提交改动的任务目录上跑 `hooks/version` 会失败，且未产生 `old/vN/`、未改动根文档；提交后重跑成功。
- 未被跟踪的任务目录（fixture 场景）上 `hooks/version` 仍然成功，行为不变。
- `Approval: requested` 时 `task complete --user-accepted` 失败，任务目录未被移动、Todo 未变 `done`；批准后成功。
- `Approval` 为 `approved` 但 `Approved version` 不匹配当前版本时 `complete` 与 `progress` 都失败。
- 未批准的任务上 `task progress` 失败且 Plan 未被改写。
- `SKILL.md` / `artifacts.md` / `CODE_STYLE.md` 各有一处语言规则；`bash hooks/smoke-test` 三段新断言全绿，并在 ubuntu / macos / windows 三个 runner 上通过。
- 三个新断言各自会在对应缺陷回归时失败（逐个验证，不是只看全绿）。
- v2：`artifacts.md` 的语言规则读起来是一份显式名单，不再出现"`## ` headings"这类整体表述；名单每一条都能在 hooks 里找到对应的匹配点或生成点。
- v2：把 fixture 中一个未被匹配的章节标题（`## Checkpoints`）改成中文后，`task state` / `task step` / `task progress` 仍然成功；改回英文同样成功。
- v2：`promote` 的新建文档骨架仍为英文（行为未变，回归确认）。
- v2：`CHANGELOG.md` 中能搜到该语言规则的条目。

## In Scope

- `hooks/version`、`hooks/task`（`complete` 与 `progress` 两个分支）、`hooks/smoke-test`。
- `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`CODE_STYLE.md` 的语言规则。
- 本任务自身的 PRD / Plan：按新规则写成中文正文，作为规则的第一个样例。
- v2：`skills/taskflow/references/artifacts.md` 的 `## Artifact language` 改写为显式名单、`skills/taskflow/SKILL.md` 的对应句子同步、`hooks/smoke-test` 的语言规则段扩为名单 + 行为断言、`CHANGELOG.md` 补条目。

## Out of Scope

- 不改 `TaskFlowDocs/achieved/` 下任何历史文档，也不回改 `2026-09-15-no-python-hooks` 与 `2026-09-15-todo-merge-driver` 的正文（用户已决定）。
- 不改 `hooks/task` 的状态机语义（不要求 `checking` 才能 complete）。
- 不引入语言探测、翻译或 i18n 机制：语言由 Skill 规则约定，不是运行时配置。
- 不改 hook 解析的结构行英文形态，因此不涉及 `merge-todo` / `archive` 的解析扩展。
- v2 不做标题本地化：`promote` 写出的骨架标题保持英文。让标题真正跟随用户语言的方案（语言声明放在 `TaskFlowDocs/repository-docs/personal.md`、由 hook 读它并写出对应语言的标题）已记录为 follow-up，不在本版范围。

## Risks / Deferred Items

- R1 的"拒绝"会让"先编辑、后升级"的现有工作方式变麻烦：必须先提交被取代的版本。这是刻意的——归档对象就应该是那次提交。file-mode（文档不进 Git）路径不受影响。
- R3 在帮助文案里承诺"任何写入之前"失败。已实测：`task state` 的拒绝发生在两处写入之前（拒绝后文件逐字节未变）。`progress` 同样只有一处写入且校验在前。
- R2 会暴露 `macos-hook-portability` 的批准缺口。那是真实缺口，不修 hook 去迁就它。
- 语言规则只覆盖文档正文。hook 生成的骨架、错误文案、章节标题保持英文，否则会与解析耦合。
- v2：本次修订**不产生可观察的行为变化**——`promote` 仍把整个大纲写成英文，用户看到的标题依然是英文。收益是规则准确且可检索；要真正让标题跟随用户语言，必须做 follow-up 里的语言探测，而那与"不引入语言探测"这条排除项直接冲突，重开时必须先改该排除项（属材料性变更）。
- v2：`CHANGELOG.md` 条目按仓库惯例是发布时由 `RELEASE.md` 写 `## [Unreleased]` 段的一部分。本版提前写入该段属于把变更记录前移；`hooks/release-check:70-73` 明确容忍 `## [Unreleased]` 作为"两次发布之间的常态"，因此不破坏发布检查。

## Open Questions

- 无阻塞项。

## Version History

- v1 — planning。
- v2 — 收窄语言规则的英文边界：由"章节标题整体英文"改为 hook 精确匹配的显式名单，非匹配标题归入正文；补 `CHANGELOG.md` 记录。取回自 `TaskFlowDocs/achieved/2026-09-15-hook-integrity/`，v1 归档于 `old/v1/`。
