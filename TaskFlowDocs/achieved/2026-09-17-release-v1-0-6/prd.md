# Publish TaskFlow v1.0.6
> Task version: v1
> Status: completed

## Goal

把 `main` 上已落地的 15 个提交作为一次稳定发布交付：CodeBuddy 成为第三个宿主、Todo 合并丢条审计（`hooks/todo-check`）与发布版本一致性检查（`hooks/release-check`）进入插件、`hooks/archive` 归档时清理 `Next action`。发布同时是这三条发布期规则第一次生效的版本——它们在上一个标签 `v1.0.5` 之后才落地，所以 `v1.0.5` 不是它们的对照，本版本才是。

## Background / Confirmed Facts

- 上一次发布是 `v1.0.5`，注解标签对象 `010dee28eaa01f815ae083b64533fdd8575ed00a`，指向提交 `3151d2707d7bae3602f1dfaf5d70d11370dd4f8f`；该提交是 `origin/main` 的祖先。
- 自 `v1.0.5` 起 `main` 上新增 15 个提交（5 个合并提交 + 10 个内容提交），工作区干净，`HEAD` = `origin/main` = `4e5e8375aba3b18a865d1bcaaac804e060db8ad0`。
- 用户可见变化的来源：PR #26（`hooks/release-check`、CI `release` job）、PR #27（归档已完成任务）、PR #28（`hooks/todo-check`）、PR #29（Todo backlog）、PR #30（CI `todo-merge-audit`）、PR #31（CodeBuddy 宿主）。
- `hooks/release-check`、`hooks/todo-check` 与 `hooks/archive` 的 `Next action` 清理在 `v1.0.5` 标签树里**都不存在**（`git cat-file -e v1.0.5:hooks/release-check` 报 not in tag），因此它们各自宣告的发布规则在本版本首次适用：
  - `release-check` 要求两个 manifest、最新 CHANGELOG 段、两份 README 的 `claude plugin list` 示例四处版本字面量一致，且两个 catalog 的 `ref` 都解析到各自 `sha` 命名的提交；
  - `archive` 要求归档时把 Todo 的 `Next action` 写为 `None — completed and archived.`，否则归档自身的断言会失败。
- **两提交发布是规范而非偏差。** `RELEASE.md` 明确写着：标签不能在发布提交存在之前创建，`sha` 不能在标签存在之前写入，所以 pin 是标签之后的一次提交，「第二个提交是 pin，不是错误」。Claude Code 在安装时校验该 pin，不匹配时以 `sha_pin_mismatch` 拒绝，并按 pin 的提交而非标签克隆。
- `RELEASE.md` 里有两处等待被下次发布更新的示例值：`## Release scope` 首句仍写「for Codex and Claude Code」（未提 CodeBuddy），验证清单里仍是 `python3 /home/hk/.codex/skills/.system/...`（绝对路径，指向被移除的 Python 运行时）。两处都是纯文档、无行为影响，本次按最小步骤修正。
- 两个活跃任务（`2026-09-16-duplicate-todo-id`、`2026-09-16-capability-selection-enforcement`）的 PRD/Plan 已完成但未获批准，`main` 上没有它们的实现。它们不是本版本的发布内容。
- 本次发布走 `RELEASE.md` 的可选 Release PR 路径：发布元数据提交经 `chore/release-v1-0-6` 分支与 PR 审查后合入 `main`，再从合并提交打标签。
- 可用工具：`gh` 2.100.0 已登录 `hkwuks`（GitHub Release 创建可用）；`python3` 3.12.13 可用（`evals/runner.py` 与 Skill 校验可跑）。

## Requirements

- R1：`.claude-plugin/plugin.json`、`.codex-plugin/plugin.json`（cachebuster 后缀用新日期）、`.codebuddy-plugin/plugin.json`（cachebuster 后缀用新日期）三个 manifest 的发布号都更新为 `1.0.6`。
- R2：`CHANGELOG.md` 新增 `## [1.0.6]` 段落，含 Added / Fixed / Compatibility / Verification 四节；Compatibility 必须写明无运行时前提变化、CodeBuddy 只在 CLI 可用、以及「发布是两个提交」。
- R3：`README.md` 与 `README.zh-CN.md` 的 `claude plugin list` 与 `codebuddy plugin list` 示例更新为 `Version: 1.0.6`。
- R4：`RELEASE.md` 的 `## Release scope` 首句补上 CodeBuddy，验证清单里的 `quick_validate.py` 改为可移植写法。
- R5：发布清单全跑并记录：`bash hooks/repository-check .`、`bash hooks/release-check .`、`bash hooks/smoke-test`、`python3 evals/runner.py`、Skill 校验、`git diff --check`。
- R6：发布元数据经 `chore/release-v1-0-6` 分支与 PR 合入 `main`；随后从该合并提交创建并推送注解标签 `v1.0.6`，再用该标签的提交建 GitHub Release，正文取自 CHANGELOG 的 `[1.0.6]` 段落。
- R7：把 `.claude-plugin/marketplace.json` 与 `.codebuddy-plugin/marketplace.json` 两个 catalog 的 `source.ref` 改为 `v1.0.6`、`sha` 改为标签提交 SHA，经第二个 PR 合入 `main`。
- R8：记录标签、Release URL、合并提交、两个 marketplace pin 与全部检查结果到本任务 Plan。
- R9：发布任务完成即归档：任务目录移入 `TaskFlowDocs/achieved/`，Todo 条目 `TF-20260917-b7bc40` 路径与状态同步。

## Acceptance Criteria

- `origin/main` 上的发布提交同时含三个 manifest 的 `1.0.6` 与新的 CHANGELOG 段落。
- 注解标签 `v1.0.6` 指向该合并提交，`git ls-remote --tags` 可见，且 `git merge-base --is-ancestor` 确认它是 `main` 的祖先。
- GitHub Release `v1.0.6` 存在且正文与 CHANGELOG 的 `[1.0.6]` 段落一致。
- 两个 marketplace catalog 的 `ref`/`sha` 与标签及其提交一一对应，`bash hooks/release-check .` 报 `STATUS: pass`。
- 发布清单每条命令都有记录的结果，未跑到的项标注为未跑，不声称通过。
- 任务归档后：活跃路径不存在、achieved 路径存在、`prd.md` 与 `plan.md` 都写 `> Status: completed`、Todo 条目的 `Next action` 为 `None — completed and archived.`。

## In Scope

- 三个 plugin manifest、`CHANGELOG.md`、两份 README、`RELEASE.md`、两个 marketplace catalog。
- `chore/release-v1-0-6` 分支、发布 PR、注解标签、GitHub Release。
- 本发布任务的 PRD / Plan 与归档。

## Out of Scope

- 改动 `hooks/`、`skills/`、`.github/workflows/` 的任何行为——本次发布不夹带功能修改。
- 两个未批准活跃任务（duplicate-todo-id、capability-selection-enforcement）的实现。
- 破坏性变更、签名、包 registry、来源证明（`RELEASE.md` 明确未配置）。
- 移动或删除已发布的 `v1.0.4`、`v1.0.5` 标签。

## Risks / Deferred Items

- 标签与 Release 是不可逆的对外动作；用户在本次一次性授权到 marketplace pin 落地为止，标签推送后的问题只能靠补丁版修正。
- `hooks/release-check` 报 `STATUS: pass` 是发布提交**之前**的预期结果（catalog 仍指向 `v1.0.5`，版本字面量仍全为 `1.0.5`）；发布提交之后它会以「CHANGELOG 说 1.0.6，manifest 说 1.0.6，catalog 仍指 v1.0.5」这一形态持续 pass——pin 与版本号是分开检查的，这正是它设计成的样子。
- 延迟项：`RELEASE.md` 的验证清单里 Skill 校验仍需要一条本地绝对路径的替代写法，本次只把不可移植的那条换成通用形式，不引入新脚本。

## Open Questions

- 无阻塞项。发布范围、落地路径、不可逆动作授权已由用户在本任务开始前确认。

## Version History

- v1 — planning：范围取 `v1.0.5..main` 的全部用户可见变化；落地路径为分支 + PR；授权一次性覆盖到 marketplace pin。
