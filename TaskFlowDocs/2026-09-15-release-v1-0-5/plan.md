# Plan — Publish TaskFlow v1.0.5
> Task version: v1
> Status: in_progress

No spec required — a release checklist run against a known-good base.

## Reference Pointers

- `RELEASE.md` — 本次必须逐条遵守的清单；本次走默认的直接 tag 路径。
- `TaskFlowDocs/achieved/2026-09-13-release-v1-0-4/plan.md` — 上一次发布的实际执行记录与验证写法。
- `CHANGELOG.md` — `1.0.4` 段落的格式就是 `1.0.5` 要照抄的结构。
- `.github/pull_request_template.md` — 若改为走 Release PR 路径时使用。

## Related Tasks

- Depends on: 无。`main` 上的四批改动均已合并。
- Related: `TaskFlowDocs/achieved/2026-09-15-no-python-hooks/`、`.../2026-09-15-todo-merge-driver/`、`.../2026-09-15-hook-integrity/` —— 本轮发布的主要内容来源，本轮已归档。

## Skills / Tools Used (Optional)

## Preconditions

- [x] 适用仓库文档已读：`RELEASE.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`、`ROADMAP.md`、PR 模板。
- [x] 远程 / 分支：`origin` = `hkwuks/TaskFlow`（非 fork），base = `origin/main`，发布前 `main` 与 `origin/main` 一致。
- [x] 本任务不新建治理文档；`RELEASE.md` 已存在。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-15 19:35 +0800
- Approved version: v1
- Approved scope: PRD / Plan v1 —— 发布 v1.0.5：元数据与 CHANGELOG、清单验证、注解标签与 GitHub Release、marketplace pin。推送标签前需再次确认。

## Steps

### Step 1 — 更新发布元数据与清单

- Goal: 让 `main` 上出现一个版本号自洽、CHANGELOG 完整的发布提交。
- Dependencies: 无。
- Files: `.claude-plugin/plugin.json`、`.codex-plugin/plugin.json`、`CHANGELOG.md`、`README.md`、`README.zh-CN.md`、`RELEASE.md`。
- Implementation checklist:
  - [x] 两个 manifest 更新到 `1.0.5`（Codex cachebuster 用新日期 `20260915`）。
  - [x] `CHANGELOG.md` 增加 `## [1.0.5] — 2026-09-15`，Added / Fixed / Compatibility / Verification 四节，Compatibility 写明不再需要解释器与 Todo ID 新规则。
  - [x] 两份 README 的 `claude plugin list` 示例改为 `Version: 1.0.5`。
  - [x] `RELEASE.md` 的示例 tag 改为 `v1.0.5`。
  - [x] 跑完整清单：`repository-check`、`smoke-test`、Skill 校验、`git diff --check`、两个 manifest 的版本断言。
- Acceptance: 清单每条都有记录结果；两个 manifest 与 CHANGELOG 版本一致。
- Verification: 见 `## Verification / Review`。清单全跑在同一棵树上（发布提交之前），`repository-check` 报 `Working tree: has changes` 是预期的——发布元数据尚未提交。
- Rollback: 撤回该提交的元数据改动。
- Status: done

### Step 2 — 打标签并建 Release

- Goal: 从精确的发布提交产生不可变的 `v1.0.5` 注解标签与 GitHub Release。
- Dependencies: Step 1 合入 `origin/main`。
- Files: 无仓库文件改动（Git 对象与 GitHub Release）。
- Implementation checklist:
  - [x] `git fetch` 后确认 `origin/main` 就是发布提交，工作区干净。
  - [x] 复核两个 manifest 版本与 CHANGELOG 段落。
  - [x] 创建注解标签 `v1.0.5`，推送前停下向用户确认（用户回复「推」）。
  - [x] 推送标签后，用该 tag 的提交 SHA 更新 `.claude-plugin/marketplace.json` 的 `ref`/`sha` 并再次验证。
  - [x] 从 tag 建 GitHub Release，正文用 CHANGELOG 的 `1.0.5` 段落。
  - [x] 记录 tag、Release URL、commit、marketplace pin。
- Acceptance: tag 是 `main` 的祖先、指向发布提交；Release 存在且正文一致；marketplace 的 `ref`/`sha` 与 tag 对应。
- Verification: 见 `## Verification / Review` 的发布记录。
- Rollback: 不移动/删除已推送标签；出问题走补丁版。标签推送前的失败直接不推送即可。
- Status: done

## Checkpoints

- Step 1 完成后：先确认清单全绿再动标签；标签一旦推送无法回退。
- Step 2 中"推送标签"是唯一需要再次确认的动作，其余（本地注解、Release 草稿）都可逆。

## Verification / Review

- `bash hooks/repository-check .` → `STATUS: pass`（`Working tree: has changes` 属于预期，改动在提交前）。
- `bash hooks/smoke-test` → `ALL SMOKE PASSED`。
- `python3 evals/runner.py` → `PASS (6 evals)`。
- `quick_validate.py skills/taskflow` → `Skill is valid!`。
- `git diff --check` → clean。
- 两个 manifest 版本断言：`.codex-plugin/plugin.json taskflow 1.0.5+codex.20260915`、`.claude-plugin/plugin.json taskflow 1.0.5`。
- 发布记录：注解标签 `v1.0.5` → tag 对象 `010dee28eaa01f815ae083b64533fdd8575ed00a`，指向提交 `3151d2707d7bae3602f1dfaf5d70d11370dd4f8f`（`origin/main`，`git merge-base --is-ancestor` 确认）。
- GitHub Release：`https://github.com/hkwuks/TaskFlow/releases/tag/v1.0.5`，正文即 CHANGELOG 的 `[1.0.5]` 段落。
- marketplace pin：`.claude-plugin/marketplace.json` 的 `ref` = `v1.0.5`、`sha` = `3151d2707d7bae3602f1dfaf5d70d11370dd4f8f`，与标签提交逐字符一致。
- 三个完成任务的归档在同一提交内：`TaskFlowDocs/2026-09-15-*` → `TaskFlowDocs/achieved/2026-09-15-*`，三份 `plan.md` 均为 `> Status: completed`，Todo 条目为 `- Status: done`。

## Change Log

- 2026-09-15 发布范围原为「三件事拆三个 PR、然后发布」；用户改为一次性交付，随后选定版本号 `v1.0.5`，并要求归档先行。
- 2026-09-15 用户批准 v1，并指定「推送标签前再确认一次」，因此 Step 2 的标签推送是唯一的中途停顿点。
- 2026-09-15 用户在 Step 2 前回复「推」，标签于 2026-09-15 推送；标签一经推送即不可移动，本次发布至此不可回退，只能靠后续补丁版。
- 2026-09-15 归档时发现 `hooks/archive` 只改 Todo 的 `Status` 与 `Task:` 路径，不更新 `Next action`，三条归档记录的 Next action 仍写着「Complete PRD / Spec / Plan and request approval.」；已手工改为 `None — completed and archived.`（hook-integrity 那条改为等待用户验收）。

## Follow-ups

- `2026-09-14-macos-hook-portability` 等活跃任务的 Approval 仍为 `requested`，与本次发布无关；发布不改变它们的门禁状态。

## Version History

- v1 — planning。
