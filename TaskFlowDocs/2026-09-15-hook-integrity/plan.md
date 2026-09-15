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

## Checkpoints

- Step 1 完成后：先在一个被跟踪且有未提交改动的真实任务上手工验证拒绝路径，再动 Step 2。
- Step 2 完成后：在 `macos-hook-portability` 上确认 `complete` 被拦（预期行为），不动它的文档。

## Verification / Review

- 三个缺陷各有"复现 → 修复 → 断言"的完整证据链，断言全部用真实 `git` 行为而非脚本调用模拟。
- 逐个验证每个新断言会在对应缺陷回归时失败（临时回退一行代码确认变红），避免"断言写得刚好通过"。

## Change Log

- 2026-09-15 Step 1 实现 —— `hooks/version` 增加受跟踪文档的未提交改动检查（`git ls-files --error-unmatch` + 两次 `git diff --quiet`），放在 `mkdir -p old/vN` 之前；smoke 新增真实仓库 fixture 段。
- 2026-09-15 Step 1 验证时误在真实任务上跑了 `version 2026-09-15-no-python-hooks v3`：该任务在本 worktree 内已被跟踪且干净，guard 正确地放行，于是产生了 `old/v2/` 并把三个文档推到 v3。已用 `git checkout` 与删除未跟踪目录完整回退，`git status` 确认无残留。教训与 R1 的设计一致：guard 只能拦住"脏工作区"，拦不住"在错误的分支/worktree 里对干净文档执行正确的命令"。

## Follow-ups

- 待归档的 no-python-hooks / todo-merge-driver 正文保持英文（用户决定），不追溯。

## Version History

- v1 — planning。
