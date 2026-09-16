# Plan — Hold Todo protection on the web-UI merge path
> Task version: v1
> Status: completed

No spec required — one range argument added to an existing read-only hook plus one CI job.

## Reference Pointers

- `TaskFlowDocs/2026-09-16-todo-entry-loss-detection/` — 本任务的前置任务，交付 `hooks/todo-check` 单提交模式。
- `.github/workflows/hooks.yml` — 既有 `smoke` / `release` / `evals` job；`release` job 的 `fetch-depth: 0` 是范围审计需要的同款 checkout。
- `skills/taskflow/references/runtime.md` 的「Only local merges」段落 — 本任务要改写的限制说明。
- `TaskFlowDocs/achieved/2026-09-15-todo-merge-driver/prd.md` — 「插件不能改托管设置」的实测依据。

## Related Tasks

- Depends on: `TaskFlowDocs/2026-09-16-todo-entry-loss-detection/`（`hooks/todo-check` 必须已合入 `main`，本任务才有文件可扩展）
- Related: `TaskFlowDocs/2026-09-16-duplicate-todo-id/`（同一条问题线的第三个任务，与本任务无文件重叠）

## Skills / Tools Used

Unaided — no capability applied to this phase; considered: `superpowers:writing-plans` and `addy-agent-skills:planning-and-task-breakdown` for the Plan, `claude-code-guide` for the GitHub Actions event fields. All were judged unnecessary: the plan was written when this v1 was first recorded and is unchanged since, and the two event fields it depends on (`github.event.before` / `github.event.after`) are stated in the PRD's Background.

## Preconditions

- [x] 适用仓库文档已读：`CONTRIBUTING.md`、`CODE_STYLE.md`、`.github/pull_request_template.md`。
- [x] 分支：`fix/web-ui-merge-loss-guard`；工作树 `.worktrees/web-ui-merge-loss-guard`；基于 `origin/main`（`3ea9ba5`，PR #28 与本任务的簿记提交均已合入）。
- [x] 远程基线：`origin` 即 `hkwuks/TaskFlow`，目标 `main`；非 fork。
- [x] 本任务不新建治理文档；CI 改动在既有 workflow 内。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-17 00:21 +0800
- Approved version: v1
- Approved scope: PRD / Plan v1 —— 给只读的 `hooks/todo-check` 加 rev 范围模式，并把 `push: main` 接进 `.github/workflows/hooks.yml`。用户 2026-09-16 回复「开始做B」即批准本任务的 v1 方案。

## Steps

### Step 1 — 范围模式与 CI 接线

- Goal: 让 `hooks/todo-check` 能审计一次推送引入的合并提交，并让 `push: main` 跑它。
- Dependencies: `TaskFlowDocs/2026-09-16-todo-entry-loss-detection/` 已合入 `main`。
- Files: `hooks/todo-check`、`.github/workflows/hooks.yml`、`hooks/smoke-test`、`hooks/README.md`、`skills/taskflow/references/runtime.md`。
- Implementation checklist:
  - [x] `hooks/todo-check` 第二参数含 `..` 时进入范围模式：`git rev-list --merges <range>` 取该范围的合并提交，逐个按单提交模式的逻辑审计，输出里带上提交哈希。
  - [x] 范围为空 → `STATUS: pass` 退出 `0`；范围不可解析 → `STATUS: blocked` 退出 `3`；任一合并丢条目 → 退出 `2`。
  - [x] 单提交模式（不含 `..`）行为与上一任务一致，回归不变。
  - [x] `.github/workflows/hooks.yml` 新 job：`fetch-depth: 0`；`push` 事件用 `github.event.before..github.event.after`，`before` 缺失或全零时退化为审计 `HEAD`；`pull_request` 事件用 `HEAD`。
  - [x] smoke 覆盖范围模式四例（含丢条目 → `2`、只有非合并提交 → `0`、坏范围 → `3`、退化路径与单提交一致）。
  - [x] `runtime.md` 的 web-UI 段落改写为「本地合并用 driver + 推送后在 CI 审计」，并给出取回丢失条目的命令；两个 hook 清单更新 `todo-check` 的范围参数说明。
- Acceptance: 见 PRD 的 Acceptance Criteria。
- Verification: `bash hooks/smoke-test`；本地对构造范围跑 `todo-check`；推送后 CI 新 job 成功；`bash:3.2` 容器 `bash -n`。
- Rollback: 还原 `hooks/todo-check` 的范围分支、删掉 CI job、还原两处文档。
- Status: done

## Checkpoints

- 新增断言逐条 mutation 验证。
- 这是本任务线里唯一改动 CI 的任务；`smoke` / `release` / `evals` 三个既有 job 的行为不得改变。

## Verification / Review

实现改动：`hooks/todo-check`（抽出 `audit_commit`，加范围模式）、`.github/workflows/hooks.yml`（新 job `todo-merge-audit`）、`hooks/smoke-test`（6 条新断言）、`hooks/README.md` 与 `runtime.md` 的清单与说明。

**单提交模式回归（与上一任务一致，未变）**

- `bash hooks/todo-check . 1905984` → exit `2`，指名 `TF-20260915-01` 与其持有父提交 `931c651`。
- `bash hooks/todo-check .`（`HEAD` = `3ea9ba5`）→ `STATUS: pass`，exit `0`。

**范围模式（真实历史）**

- `bash hooks/todo-check . 77c25dd..1905984` → exit `2`，`Range: 77c25dd..1905984` / `- Merge commits in range: 1` / 指名 `TF-20260915-01`。
- 全历史范围（根提交 `..HEAD`，41 个合并提交）→ exit `2`，只有 `1905984` 与 `77c25dd` 两条命中，其余 39 个合并提交全部 pass——与单提交模式的命中集合完全一致，误报为零。
- `bash hooks/todo-check . HEAD..HEAD` → `Merge commits in range: 0`，exit `0`。
- `bash hooks/todo-check . f1208a4..4cff92e`（范围内全是非合并提交）→ exit `0`。
- `bash hooks/todo-check . nope..also-nope` → `Cannot resolve range`，`STATUS: blocked`，exit `3`。

**CI run block 的四种事件情形（本地按同一段 shell 复算）**

| 事件 | `BEFORE` | `AFTER` | 实际范围 | 结果 |
| --- | --- | --- | --- | --- |
| 普通 push | `f1208a4` | `4cff92e` | `f1208a4..4cff92e` | exit `0` |
| 首次 push / 强推 | 全零 | `3ea9ba5` | `3ea9ba5` | exit `0` |
| `pull_request` | 空 | 空 | `HEAD` | exit `0` |
| 承载历史丢失的那次 push | `77c25dd` | `1905984` | `77c25dd..1905984` | exit `2` |

**smoke**

- `bash hooks/smoke-test` → `ALL SMOKE PASSED`。范围用例构造在既有 fixture 里：`main` 被 `reset --hard` 到那个丢条目的合并提交（真实形态——丢失确实到了 `main`），因此 `base..HEAD` 含丢条目、`tc_merge_rev..HEAD` 不含，两个范围给出相反结论。
- 新增 6 条断言逐条 mutation 验证，每条都让 suite 变红：范围分支永不进入（M1）、坏范围退 `0`（M2）、范围里某个提交丢掉后继续静默（M3）、范围只审计 tip（M4）、单提交退化路径恒 pass（M5）、无合并的范围报 blocked（M6）。每次改完立即还原并 `diff` 确认与原件相同。

**其余**

- `python3 -c "yaml.safe_load(...)"` → `jobs: ['smoke', 'release', 'todo-merge-audit', 'evals']`，新 job 两个 step 解析正常；三个既有 job 未改。
- `python3 evals/runner.py` → `PASS (6 evals)`；`quick_validate.py skills/taskflow` → `Skill is valid!`；`bash hooks/release-check .` → `STATUS: pass`。
- `docker run --rm -v "$PWD":/w -w /w bash:3.2 bash -n` 对 `hooks/todo-check` 与 `hooks/smoke-test` 均通过；`git diff --check` 干净。
- **未在 CI 上跑过**：新 job 要等这个 PR 推上去才第一次执行。本任务被并入簿记 PR #29 之前的那次推送没有它。

## Change Log

- 2026-09-17 — Step 1 实施与验证完成。`hooks/todo-check` 的单提交逻辑抽成 `audit_commit`，范围模式复用它，因此两条路径的判定不可能漂移。smoke 的范围用例复用既有 fixture 并把 `main` 重置到那个丢条目的合并提交，没有另建仓库。

## Follow-ups

- **CI 的首次真实运行**：`todo-merge-audit` 要等本 PR 推上去才第一次跑。若它在本 PR 上失败，先看是不是 `pull_request` 事件下 `github.event.before/after` 为空导致范围退化成 `HEAD` 后再判断。
- **其他长分支仍无保护**：本 job 只监听 `push: main`。仓库目前只有 `main` 是长期分支，不扩展。
- **`review` job 的失败信息只在 CI 日志里**：GitHub 的 job 失败不会把 `todo-check` 的输出置于显眼处，恢复命令（`git show <parent>:TaskFlowDocs/todo.md`）在日志与 `runtime.md` 里。若实践中发现日志不够，再考虑 summary 输出。
- **全历史审计仍要人工**：`bash hooks/todo-check . "$(git rev-list --max-parents=0 HEAD)..HEAD"` 会命中已修复的 `1905984`/`77c25dd`，这是预期——那是审计，不是回归。

## Version History

- v1 — planning.
