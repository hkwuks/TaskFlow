# Publish TaskFlow v1.0.5
> Task version: v1
> Status: completed

## Goal

把 `main` 上已合并的四批改动（去掉 Python 运行时依赖、Todo 合并驱动与派生 ID、hook 完整性修复、贡献/治理文档补强）作为一次稳定发布交付：更新两个 manifest、marketplace pin 与 CHANGELOG，随后从合并后的精确提交打 `v1.0.5` 注解标签、建 GitHub Release，并把 marketplace 目录指回该 tag。

## Background / Confirmed Facts

- 上一次发布是 `v1.0.4`（2026-09-13），tag 指向 `2691453a40955a6f7353c3326dd44c58638f6608`，是 `origin/main` 的祖先。
- 自那之后的用户可见变化：
  - `refactor: remove the Python runtime dependency from every hook` —— 所有 hook 不再需要解释器，`hooks/python-runtime` 与 `TASKFLOW_PYTHON` 删除。这是运行前提的变化，不只是修复。
  - `feat: merge parallel Todo updates by entry` —— Todo 合并驱动、`install-merge-driver`、以及从目标内容派生的 Todo ID（替代 `TF-<date>-<max+1>` 计数器）。
  - `fix: refuse to archive uncommitted tracked task documents` 与 `fix: require an approval before progress and completion` —— `hooks/version` 归档完整性、`task progress`/`complete` 的批准门禁。
  - macOS 可移植性（bash 3.2 + BSD userland）与 `feat: keep personal rules in repository-docs/ and out of Git`、`feat: record the host session id in the task session index`、`docs: require a working branch and isolate parallel tasks`。
- 版本号决定：用户选定 **v1.0.5**（而非语义上更"正确"的 1.1.0）。记录该决定，不重新讨论。
- `RELEASE.md` 规定：release scope 合入 base（默认 `main`）后，从**精确的合并提交**打注解标签；marketplace 目录保持 `main`，但插件 source 必须 pinned 到 release tag 与完整 commit SHA；发布前必须跑 `repository-check`、`smoke-test`、Skill 校验与 `git diff --check`，并核对两个 manifest 的版本。
- 前一个发布任务用的是一次性 PR 路径（PR #14）；本次按 `RELEASE.md` 的默认直接 tag 路径。
- 三个已完成任务（`2026-09-15-no-python-hooks`、`2026-09-15-todo-merge-driver`、`2026-09-15-hook-integrity`）已在本轮归档进 `TaskFlowDocs/achieved/`，它们承载了本次发布的主要变更；本发布任务与它们并列，不重复其内容。

## Requirements

- R1：`.claude-plugin/plugin.json` 与 `.codex-plugin/plugin.json` 都更新到 `1.0.5`；Codex 的 cachebuster 后缀按既有格式更新为新的日期。
- R2：`CHANGELOG.md` 新增 `## [1.0.5]` 段落，含 Added / Fixed / Compatibility / Verification 四节；Compatibility 必须说明"hook 不再需要 Python 解释器"这一运行前提变化，以及 Todo ID 的新派生规则。
- R3：`README.md` 与 `README.zh-CN.md` 里 `claude plugin list` 的输出示例更新为 `Version: 1.0.5`，两份行为保持一致。
- R4：`RELEASE.md` 的示例 tag 更新为当前版本号（`v1.0.5`）。
- R5：发布清单全跑：`bash hooks/repository-check .`、`bash hooks/smoke-test`、Skill 校验、`git diff --check`，以及两个 manifest 的版本断言。
- R6：在 `origin/main` 存在发布提交、两个 manifest 一致、工作区干净之后，创建并推送注解标签 `v1.0.5`，再从该 tag 建 GitHub Release，内容用 CHANGELOG 的该段落。
- R7：把 `.claude-plugin/marketplace.json` 的 `source.ref` 改为 `v1.0.5`、`sha` 改为该标签的提交 SHA，使稳定安装 pinned 到不可变的发布提交。
- R8：记录 tag、Release URL、commit、marketplace pin 与各项检查结果到本任务 Plan。

## Acceptance Criteria

- `origin/main` 上的发布提交同时含两个 manifest 的 `1.0.5` 与新的 CHANGELOG 段落。
- 注解标签 `v1.0.5` 指向该提交，`git ls-remote --tags` 可见，且 `git merge-base --is-ancestor` 确认它是 `main` 的祖先。
- GitHub Release `v1.0.5` 存在且正文与 CHANGELOG 段落一致。
- `.claude-plugin/marketplace.json` 的 `ref`/`sha` 与标签及其提交一一对应。
- 发布清单的每条命令都有记录的结果，未跑到的项明确标注为未跑而不是声称通过。

## In Scope

- 两个 manifest、`CHANGELOG.md`、`README.md`、`README.zh-CN.md`、`RELEASE.md`、`.claude-plugin/marketplace.json`。
- 注解标签与 GitHub Release 的创建。
- 本发布任务的 PRD / Plan。

## Out of Scope

- 改动 `hooks/` 或 `skills/` 的任何行为（本次发布不再夹带功能修改）。
- `0-` 类破坏性变更、签名、包registry、来源证明（`RELEASE.md` 明确未配置）。
- 移动或删除已发布的 `v1.0.4` 标签。

## Risks / Deferred Items

- 标签与 Release 是不可逆的对外动作：一旦推送，后续问题只能靠补丁版修正，`RELEASE.md` 也禁止移动共享标签。
- marketplace 的 `sha` 在标签创建**之前**无法填写，所以顺序必须是「合并 → 打标签 → 取 SHA → 更新 marketplace」，marketplace 的更新会因此成为标签之后的一次额外提交。这与 `RELEASE.md` 步骤 6 一致。
- 版本号 1.0.5 与"新增能力"的语义不完全吻合，是用户的显式选择；不在本任务里重新讨论。

## Open Questions

- 无阻塞项。

## Version History

- v1 — planning。
