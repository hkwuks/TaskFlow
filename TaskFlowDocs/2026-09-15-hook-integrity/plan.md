# Plan — Hook integrity: unpolluted archives, unbypassable gates, user-language documents
> Task version: v1
> Status: in_progress

No spec required — three localized fixes in existing hooks plus a documentation rule.

## Reference Pointers

- `hooks/version` — 已经被取代文档的写入路径；R1 加在其归档循环之前。
- `hooks/task` — `state` 分支里已有的批准校验就是 `complete` / `progress` 要复用的那套，理由与文案需一致。
- `hooks/smoke-test` — 断言风格、`digest` 助手、fixture 目录约定。
- `TaskFlowDocs/2026-09-15-no-python-hooks/old/v1/version.md` — 上一次归档污染的实际记录，R1 就是为了不再产生它。

## Related Tasks

- `TaskFlowDocs/2026-09-15-no-python-hooks/`、`TaskFlowDocs/2026-09-15-todo-merge-driver/` — 待归档；本任务的 R2 决定它们能否通过 `complete`（两者 Approval 均为 `approved`，可通过）。
- `TaskFlowDocs/2026-09-14-macos-hook-portability/` — Approval 为 `requested` 而 Step 为 `done`；R2 落地后 `complete` 会（正确地）拦下它。

## Skills / Tools Used (Optional)

## Preconditions

- [x] 适用仓库文档与个人规则已读；无优先级冲突。
- [x] 远程 / 分支：`origin` = `hkwuks/TaskFlow`，base = `origin/main`，本地分支 `fix/hook-integrity`，独立 worktree。PR 模板为 `.github/pull_request_template.md`。
- [x] 本任务不新建治理文档。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-15 17:40 +0800
- Approved version: v1
- Approved scope: PRD / Plan v1 —— 三项修复：version 拒绝污染归档、complete/progress 批准门禁、文档语言规则。

## Steps

### Step 1 — 让 `hooks/version` 拒绝污染归档

- Goal: 归档的一定是"被取代的那一版"，而不是被 v2 编辑覆盖后的工作区副本。
- Dependencies: 无。
- Files: `hooks/version`、`hooks/smoke-test`。
- Implementation checklist:
  - [x] 归档循环开始前，对每个要归档的文档判断：被 Git 跟踪（`git ls-files --error-unmatch`）且 `git diff --quiet` / `git diff --cached --quiet` 报告有改动 → 失败退出，不写任何文件。未被跟踪的文档不检查。
  - [x] 拒绝文案指明下一步：先提交被取代的版本，归档对象就是那次提交。
  - [x] 检查在**任何写入之前**（含 `mkdir -p old/vN`）完成，失败不得留下半个归档。
  - [x] smoke：被跟踪且有未提交改动时 `version` 失败、`old/v1` 不存在、根文档字节未变；提交后重跑成功。
- Acceptance: 污染场景被拒绝且无副作用；干净场景（含未跟踪 fixture 目录）行为与今天一致。
- Verification: `hooks/smoke-test` 新增段 "version refuses to archive uncommitted tracked documents"——真实 `git init` fixture 上：脏的被跟踪文档被拒、`old/v2` 不存在、根文档字节未变；提交后归档成功且内容等于该提交；未被跟踪的文档即使脏也照常归档。手工复验：干净任务上 `version v2` 成功，追加一行未提交内容后 `version v3` 被拒并打印 `prd.md has uncommitted changes; ...`。回归验证：把该 guard 从 `hooks/version` 摘掉，smoke 立刻红在 `FAIL version archived an uncommitted tracked document`。
- Rollback: 去掉该检查，恢复原写入顺序。
- Status: done

### Step 2 — 让 `task complete` 与 `task progress` 无法绕过批准

- Goal: 未批准的任务不能被归档；未批准的任务不能被写 Step。
- Dependencies: 无（与 Step 1 独立）。
- Files: `hooks/task`、`hooks/smoke-test`。
- Implementation checklist:
  - [x] 抽出 `require_approval`（`Approval: approved`、`Approved version` = 当前 Task version、`Approved by` 非 `pending`），`complete`、`progress`、`state in_progress` 共用，理由/文案一致。
  - [x] `complete`：校验在第一个写入之前；失败时任务目录不移动、Todo 不变 `done`、PRD/Plan 不被改成 `completed`。
  - [x] `progress`：同样前置校验；失败时 Plan 字节未变。
  - [x] smoke：四段断言——`progress` 在未批准任务上被拒且 Plan 字节未变；`complete` 在未批准任务上被拒且任务未移动、状态未改；`Approved by: pending` 时两命令都被拒；版本 bump 未重新批准时两命令都被拒。
- Acceptance: 三个断言各自在缺陷回归时失败；已验证 `session-id-record`、`untrack-workflow-draft`、两个待归档任务的 Approval 仍能通过。
- Verification: `hooks/smoke-test` 新增段 "approval gates block progress and completion"。真实任务复验：`task complete 2026-09-14-macos-hook-portability --user-accepted` 现在被拒（该任务 Approval 为 `requested`，正是要拦的）；`2026-09-15-no-python-hooks`（approved v2 / version v2）与 `2026-09-15-todo-merge-driver`（approved v1 / version v1）的 Approval 仍可放行，没有误拦。回归验证：分别摘掉 `progress` 与 `complete` 的前置校验，两处断言各自变红（`progress OK` / `complete OK`）。Windows 侧同步：`smoke-test-windows.ps1` 的批准 fixture 补上 `- Approved by: user`（只翻 `Status` 与 `Approved version` 会被新门禁正确地拦下），原生跑过 `WINDOWS LIFECYCLE PASSED`。
- Rollback: 去掉前置校验调用。
- Status: done

### Step 3 — 记录文档语言规则

- Goal: 之后生成的 `prd.md` / `spec.md` / `plan.md` 正文用用户惯用语言，结构行保持英文，解析不受影响。
- Dependencies: 无。
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`CODE_STYLE.md`、本任务的 `prd.md` / `plan.md`（作为首个样例）。
- Implementation checklist:
  - [x] 三处各写一条规则：结构行英文（`> Task version:`、`> Status:`、章节标题、`## Approval` 五字段、`### Step N`、Todo 字段名、`- [ ]` 标记），正文散文用用户惯用语言。
  - [x] 明确"已写好的文档不回改"，避免被理解为要求重写历史。
  - [x] `CODE_STYLE.md` 的 Markdown 小节补一条，与既有"英文中文 README 行为一致"并列不冲突。
- Acceptance: 新规则不与任何 hook 的解析前提矛盾；本任务自身文档即为样例。
- Verification: `hooks/smoke-test` 新增段 "artifact language rule is documented without contradicting the parsers"，钉住规则存在、边界措辞、不回改历史，以及四个结构记号在规则文本里被点名。读校确认三处规则互不矛盾。`python3 ~/.codex/.../quick_validate.py skills/taskflow` → `Skill is valid!`。
- Rollback: 撤回三处文档改动。
- Status: done

## Checkpoints

- Step 1 完成后：先在一个被跟踪且有未提交改动的真实任务上手工验证拒绝路径，再动 Step 2。
- Step 2 完成后：在 `macos-hook-portability` 上确认 `complete` 被拦（预期行为），不动它的文档。

## Verification / Review

- 三个缺陷各有"复现 → 修复 → 断言"的完整证据链，断言全部用真实 `git` 行为而非脚本调用模拟。
- 逐个验证每个新断言会在对应缺陷回归时失败（临时回退一行代码确认变红），避免"断言写得刚好通过"。

## Change Log

- 2026-09-15 Step 1 实现 —— `hooks/version` 增加受跟踪文档的未提交改动检查（`git ls-files --error-unmatch` + 两次 `git diff --quiet`），放在 `mkdir -p old/vN` 之前；smoke 新增真实仓库 fixture 段。
- 2026-09-15 Step 2 实现 —— `hooks/task` 抽出 `require_approval`，`progress` 与 `complete` 前置调用；`state in_progress` 的内联检查改为调用同一函数。`complete` 的既有断言仍然只覆盖"缺 `--user-accepted`"这一条，本轮补的是批准维度。
- 2026-09-15 Step 2 回归验证时误在真实任务上跑了 `version 2026-09-15-no-python-hooks v3`：该任务在本 worktree 内已被跟踪且干净，guard 正确地放行，于是产生了 `old/v2/` 并把三个文档推到 v3。已用 `git checkout` 与删除未跟踪目录完整回退，`git status` 确认无残留。教训与 R1 的设计一致：guard 只能拦住"脏工作区"，拦不住"在错误的分支/worktree 里对干净文档执行正确的命令"。
- 2026-09-15 `hooks/smoke-test-windows.ps1` 的批准 fixture 补 `- Approved by: user`；这不是测试迁就实现，而是原 fixture 只翻两个字段、恰好绕过了即将补齐的门禁。
- 2026-09-15 收尾：`require_approval` 抽出后 `state` 分支里不再使用的 `plan_text`/`version` 局部变量删除，被顺手吃掉的一个空行补回；`bash -n`、`docker bash:3.2 bash -n`、原生 `smoke-test`、`smoke-test-windows.ps1` 全部复跑通过。
- 2026-09-15 PR 拆分改为一次交付。原计划三个 PR（Step 1 / Step 2 / Step 3 各一），Step 1 已作为 PR #24 合并（`71a9b44`，含本任务目录与 Todo 条目）。拆分的代价被低估了：`hooks/smoke-test`、`plan.md` 三个 PR 都要动，成品切回三个变体要靠字符串裁剪生成，返工两轮。剩余 Step 2 + Step 3 在 `fix/hook-integrity` 上作为一次改动提交。
- 2026-09-15 语言规则落在三处：`SKILL.md`（Required artifacts 之后）、`references/artifacts.md`（新增 `## Artifact language`）、`CODE_STYLE.md`（Markdown 小节）。hook 解析的记号与取值保持英文，未做任何解析扩展。

## Follow-ups

- `2026-09-14-macos-hook-portability` 的 Approval 仍是 `requested` 而 Step 为 `done`：R2 落地后无法 `complete`，需要另行补批准或重做。
- 待归档的 no-python-hooks / todo-merge-driver 正文保持英文（用户决定），不追溯。

## Version History

- v1 — planning。
