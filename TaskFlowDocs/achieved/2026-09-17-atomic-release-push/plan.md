# Plan — Atomic release push
> Task version: v1
> Status: completed

No spec required — 单文件文档改动，无跨层契约。

## Reference Pointers

- `RELEASE.md` —— 唯一被改的文件；本任务改的是它的 `## Tag and GitHub Release` 第 3–6 步、64–69 行的说明段与 `## Rollback`。
- `TaskFlowDocs/achieved/2026-09-17-release-v1-0-6/plan.md` —— 本任务要消除的窗口的实测记录（`/plugin marketplace update` 在 pin 合入前评到 v1.0.5）。
- `hooks/release-check` —— pin 的强制检查，读它确认策略改动后校验路径不变。
- `CONTRIBUTING.md` 的 `## Working branches` —— 本任务用 `docs/` 前缀的分支。
- `.github/pull_request_template.md` —— 本任务走普通 PR 路径。

## Related Tasks

- Depends on: 无。
- Related: `TaskFlowDocs/achieved/2026-09-17-release-v1-0-6/`（暴露窗口的那次发布）、`TaskFlowDocs/achieved/2026-09-13-pin-marketplace-release/`（`sha` pin 的来源任务）。
- 无关活跃任务：`2026-09-16-duplicate-todo-id`、`2026-09-16-capability-selection-enforcement`。

## Skills / Tools Used (Optional)

- 未调用额外 Skill。官方 catalog 的 `ref`/`sha` 分布用本机 `python` 直接统计 JSON 得出（见 PRD 的 Confirmed Facts），这是一次性核算，不是可复用工具。

## Preconditions

- [x] 适用仓库文档已读：`RELEASE.md`、`CONTRIBUTING.md`、`TaskFlowDocs/repository-docs/index.md`、PR 模板。
- [x] `git push --atomic --dry-run origin main refs/tags/v1.0.6` → exit 0，远端支持原子推送（已实测）。
- [x] 本任务在 `TaskFlowDocs/todo.md` 登记为 `TF-20260917-a608b7` 并升级为任务。
- [x] 用户已确认策略方向。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-17 13:05 +0800
- Approved version: v1
- Approved scope: Plan v1，范围收窄为只改 `RELEASE.md`（第 3–6 步、两提交说明段、`## Rollback`）；不改 `CONTRIBUTING.md`、不改 `hooks/`、`skills/`、catalog。

## Steps

### Step 1 — 改写 RELEASE.md 的推送步骤并验证

- Goal: 让 `RELEASE.md` 只规定一条可执行的发布路径——pin 提交与标签同一次 `--atomic` 推送，一步执行、事后审阅。
- Dependencies: 无。
- Files: `RELEASE.md`。
- Implementation checklist:
  - [x] 第 6 步改写：pin 提交本地创建（只含 `ref`/`sha` 四行）→ 与标签一次 `git push --atomic origin main refs/tags/<tag>` 推送 → 推送后在本地与 `main` 上跑 `bash hooks/release-check .`。
  - [x] 新增一小节说明为什么一次执行而不是走 PR：这次推送同时移动一个受保护的信息（标签）与一条可回退的记录（catalog），内容由标签机械决定、无待审内容；正确性由 `git merge-base --is-ancestor` 与 `release-check` 强制。发布元数据提交（有实质内容）仍走 Release PR。
  - [x] 在 64–69 行的两提交说明之后补一句次序关系：两个提交是必需的，两次 push 不是。
  - [x] 加回退路径：远端不支持 atomic 时，退回「先推标签、再更新 catalog」，并把窗口记入发布任务；推送命令不得夹带其他文件。
  - [x] `## Rollback` 补一句：catalog 记录有误时的修正路径，引用既有的「移动远端标签需 owner 显式授权」。
- Acceptance: 清单每条都落在 `RELEASE.md` 里；文档里能读到唯一一条推送命令，且包含 `--atomic origin main refs/tags/<tag>`。
- Verification: 见 `## Verification / Review`。
- Rollback: 丢弃分支即可，`RELEASE.md` 不在任何发布产物里。
- Status: done

## Checkpoints

- Step 1 完成后：确认 `hooks/`、`skills/`、两个 catalog 均未出现在 diff 里（本任务只改文档）。

## Verification / Review

- 2026-09-17 Step 1: RELEASE.md rewritten: step 5 atomic push of pin+tag, rationale subsection, fallback path, Rollback clarified; diff --check clean; release-check pass; scope confined to RELEASE.md

改动范围核对：`git status --short` 只有 `RELEASE.md`、`TaskFlowDocs/todo.md`、新任务目录；`git status --short -- hooks skills .claude-plugin .codebuddy-plugin .codex-plugin .github` 为空，验收标准里「除 `RELEASE.md` 外不改任何文件」成立。

- `git diff --check` → clean（exit 0）。
- `bash hooks/release-check .` → `STATUS: pass`；两个 pin 仍解析到 `ce3b03ca…`（未被本次改动影响，符合预期）。
- `bash hooks/repository-check .` → `needs-user-input`，原因是 `Working tree: has changes`（本任务尚未提交，属预期）。
- `bash hooks/smoke-test` → 与 `main` 同形态：停在无解释器的 `toolbin/bash: error while loading shared libraries`。本任务未触及 hook，且该失败在本机 `main` 上同样复现，判定为宿主既有限制；该套件由 CI 矩阵覆盖，本任务的 PR 上会再跑一次。
- 文档自洽性：`grep -n "atomic" RELEASE.md` 命中 8 处，覆盖第 5 步的推送命令、64–69 行说明之后的新增段、以及远端拒绝时的回退路径；`grep -i "publishing the catalog change" RELEASE.md` 为 0 命中——旧第 6 步那句「validate … _before publishing the catalog change_」已随改写消失，不再与「一次推送」矛盾。
- 拼写：`catalogue` → `catalog` 全文归正（6 处），与本文件原有的 8 处 `catalog` 及 `CHANGELOG.md`/`README.md`/`hooks/README.md` 的用法一致。
- 未跑：Codex / CodeBuddy 端对「catalog 记录」的安装验证——本任务只改文档，不改 catalog，该项由下一次发布按 `RELEASE.md` 第 6 步执行。

## Change Log

- 2026-09-17 任务由 v1.0.6 发布后的策略讨论产生；用户确认「pin 直推 + 绑定到原子推送」为方向。
- 2026-09-17 核算官方 catalog：`source: url` 条目 160 个全部只带 `sha`；`git-subdir` 95 个同时带 `ref` 与 `sha`。结论是「tag 与 sha 并非二选一」，本仓库的 `ref` + `sha` 写法保留，去掉 `sha` 的选项不再是待议项，已移出 In Scope。

## Follow-ups

- 无。`RELEASE.md` 里 Skill 校验仍用通用 `<skill-creator>` 占位符（由 v1.0.6 发布任务记录），本任务不改。

## Version History

- v1 — planning。
