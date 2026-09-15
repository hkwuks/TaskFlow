# Hook integrity: unpolluted archives, unbypassable gates, user-language documents
> Task version: v1
> Status: in_progress

## Goal

修掉本轮实测发现的三个 hook 缺陷：`hooks/version` 把"被取代之后"的工作区内容当成旧版本归档；`task complete` 和 `task progress` 可以绕过批准门禁；任务文档正文使用英文，而用户惯用中文。前两个是正确性缺陷，第三个是产出可读性缺陷。

## Background / Confirmed Facts

三个问题都在本轮排查中实测复现，不是推断：

- **归档污染。** `hooks/version` 从**工作区**复制被取代的核心文档。实测：先按 v2 修改 `prd.md`（写入 `V2 CONTENT ALREADY WRITTEN`），再跑 `version ... v2 prd.md`，归档出的 `old/v1/prd.md` 里带着这条 v2 内容；`old/v1/plan.md` 同样带着 v2 的 `- Status: done`。也就是说 `old/v1/` 记录的不是 v1 被批准时的样子，而是 v1 被替换后的残留。本仓库的 `2026-09-15-no-python-hooks/old/v1/` 就是这样产生的，后来手工从提交 `9c26465` 重建。
- **门禁可绕过。** `task state in_progress` 校验 `Approval: approved` 且 `Approved version` 等于当前版本，但 `task complete` 只校验"没有未勾选项 + 没有未完成 Step"，完全不看 Approval。实测：一个 `Approval: requested / Approved by: pending` 的全新任务，把 checklist 勾上、Step 标 done 后，`task complete --user-accepted` 返回 `complete OK` 并成功归档。实例：`TaskFlowDocs/2026-09-14-macos-hook-portability/` 的 Approval 是 `requested`，Step 是 `done`，现在跑 `complete` 就会通过。
- `task progress` 没有任何门禁。实测：在 `> Status: planning`、Step 仍为 pending 且**从未批准**的任务上，`task progress <task> 1 done` 返回 `progress OK`，把 Step 写成 done、并在 `## Verification / Review` 追加行。
- **语言。** `CODE_STYLE.md` 只要求"英文与中文 README 行为一致"，没有规定任务文档语言。本仓库全部 26 个 achieved 任务文档都是英文正文，而用户的工作语言是中文。
- 用户本轮确认的三个方向：被跟踪文件有未提交改动就拒绝归档；`complete` 与 `progress` 都补批准检查；任务文档结构行保持英文、正文用中文。
- 影响面已核对：现有活跃任务中 `session-id-record`、`untrack-workflow-draft` 的 Approval 是 `approved`，两个待归档任务（no-python-hooks、todo-merge-driver）也是 `approved`；本轮新增的批准检查不会误拦它们。仅 `macos-hook-portability` 等 `requested` 任务会被拦——那正是期望行为。

## Requirements

- R1：`hooks/version` 在归档任一核心文档前，若该文档**被 Git 跟踪且工作区或暂存区有未提交改动**，必须在任何写入之前失败并说明原因；未被跟踪的文档（file-mode，文档不进 Git）不受此限。
- R2：`task complete` 必须校验当前 Plan 的 Approval 为 `approved`、`Approved version` 等于当前 Task version、`Approved by` 不是 `pending`；不满足则在任何写入前失败。
- R3：`task progress` 使用与 `task state in_progress` 同一套批准校验，理由与拒绝文案保持一致。
- R4：`SKILL.md`、`references/artifacts.md`、`CODE_STYLE.md` 记录文档语言规则：hook 解析的结构行（`> Task version:`、`> Status:`、章节标题、`## Approval` 的五个字段、`- ID:` 等）保持英文；正文散文用用户惯用语言。已写好的英文文档不回改。

## Acceptance Criteria

- 在一个被跟踪且有未提交改动的任务目录上跑 `hooks/version` 会失败，且未产生 `old/vN/`、未改动根文档；提交后重跑成功。
- 未被跟踪的任务目录（fixture 场景）上 `hooks/version` 仍然成功，行为不变。
- `Approval: requested` 时 `task complete --user-accepted` 失败，任务目录未被移动、Todo 未变 `done`；批准后成功。
- `Approval` 为 `approved` 但 `Approved version` 不匹配当前版本时 `complete` 与 `progress` 都失败。
- 未批准的任务上 `task progress` 失败且 Plan 未被改写。
- `SKILL.md` / `artifacts.md` / `CODE_STYLE.md` 各有一处语言规则；`bash hooks/smoke-test` 三段新断言全绿，并在 ubuntu / macos / windows 三个 runner 上通过。
- 三个新断言各自会在对应缺陷回归时失败（逐个验证，不是只看全绿）。

## In Scope

- `hooks/version`、`hooks/task`（`complete` 与 `progress` 两个分支）、`hooks/smoke-test`。
- `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`CODE_STYLE.md` 的语言规则。
- 本任务自身的 PRD / Plan：按新规则写成中文正文，作为规则的第一个样例。

## Out of Scope

- 不改 `TaskFlowDocs/achieved/` 下任何历史文档，也不回改 `2026-09-15-no-python-hooks` 与 `2026-09-15-todo-merge-driver` 的正文（用户已决定）。
- 不改 `hooks/task` 的状态机语义（不要求 `checking` 才能 complete）。
- 不引入语言探测、翻译或 i18n 机制：语言由 Skill 规则约定，不是运行时配置。
- 不改 hook 解析的结构行英文形态，因此不涉及 `merge-todo` / `archive` 的解析扩展。

## Risks / Deferred Items

- R1 的"拒绝"会让"先编辑、后升级"的现有工作方式变麻烦：必须先提交被取代的版本。这是刻意的——归档对象就应该是那次提交。file-mode（文档不进 Git）路径不受影响。
- R3 在帮助文案里承诺"任何写入之前"失败。已实测：`task state` 的拒绝发生在两处写入之前（拒绝后文件逐字节未变）。`progress` 同样只有一处写入且校验在前。
- R2 会暴露 `macos-hook-portability` 的批准缺口。那是真实缺口，不修 hook 去迁就它。
- 语言规则只覆盖文档正文。hook 生成的骨架、错误文案、章节标题保持英文，否则会与解析耦合。

## Open Questions

- 无阻塞项。

## Version History

- v1 — planning。
