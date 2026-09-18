# Publish TaskFlow v1.0.7

> Task version: v1
> Status: in_progress

## Goal

把 `v1.0.6` 之后已在 `main` 上落地的改动作为一次稳定发布交付，版本号 `1.0.7`。发布内容与理由见下；执行程序在 `RELEASE.md`，本文不重述。

## Background / Confirmed Facts

- 基线 `v1.0.6` = `ce3b03cab31c75ed467f4ccec06ea5cfc6719357`，是 `origin/main` 的祖先。当前 `main` = `cb173cf`，工作区干净。
- **版本号不是推断的**：仓库文档里没有写下来的 semver 政策，`1.0.7` 由用户在 2026-09-18 指定。先例（`v1.0.5 → v1.0.6` 加了 CodeBuddy 宿主与两个 hook，仍是 patch）与之一致，但决定权在用户。
- **发布路径是 `RELEASE.md` 的默认路径**：直接从 `main` 打标签。用户在 2026-09-18 确认，并否决了本任务初稿里那条自加的 `chore/release-v1-0-7` 分支——`RELEASE.md` 已写明 Release PR 是**可选**路径，只在发布文档需要单独审阅或需要 RC 时使用。
- **发布范围**（`git log v1.0.6..main` 逐提交核对）：
  - `196e9aa`（PR #39）——`hooks/run-hook.cmd` 在 Git 中记为可执行。**修的是 `v1.0.6` 就存在的缺陷**：`hooks.json` 以裸路径调用它，而它没有执行位，任何 Unix 安装的 SessionStart 都以 exit 126 失败。
  - `5a553f0`（PR #40）——冲突先询问用户的规则；修回 `README.zh-CN.md` 被冲突解决退回的 manifest 计数。
  - `eefd4d1` + `5a46c07`（PR #41）——`hooks/task next` 与 `hooks/task get`，以及它们在 bash 3.2 下的解析修复。
  - `adfc5c1`（PR #38）——隔离先于第一份文档；新增 `hooks/repository-check`。
  - `5a77962`（PR #37）——两份 README 补全已交付面。
  - `1ba0e1a`（PR #36）——重复 Todo ID 的派生替换。
- **不作为发布内容**：`c5a39a2`（RELEASE.md 的原子推送）、`42edb18`（v1.0.6 的 catalog pin）与全部 `chore:` 归档/登记提交——它们改的是本仓库流程与任务记录，不是插件内容。
- **两提交发布是设计结果**：catalog 的 `sha` 必须在标签存在之后才能写。Claude Code 在安装时逐字符比对 `sha`，不等即 `sha_pin_mismatch`，并按 commit 而非 tag 克隆——所以 tag 被移动时已装的版本仍锁在已审阅的提交。对照：`obra/superpowers` 的 marketplace 用 `"source": "./"`、无 `ref`/`sha`，因此它一次提交就能发完；我们的 pin 是两提交的来源。
- **`.codebuddy-plugin/marketplace.json` 有一个滞后的 `"version": "1.0.5"`**：不在 `release-check` 的比较范围内，也不影响安装（pin 决定装什么）。本次不动，见 Follow-ups。

## Requirements

- R1：三个 manifest 移到 `1.0.7`（Codex 与 CodeBuddy 的 cachebuster 后缀日期改为发布日）；`CHANGELOG.md` 新增 `## [1.0.7]` 段；两份 README 的四处 `plugin list` 示例移到 `1.0.7`。字面量必须与标签一致，由 `bash hooks/release-check .` 判定。
- R2：发布元数据提交直接落在 `main`，不切 `release/` 分支、不开 Release PR。
- R3：从该提交创建注解标签 `v1.0.7`，随后写 catalog pin，两者以一次原子推送送出（`RELEASE.md` 第 3–5 步）。
- R4：按 `RELEASE.md` 的 Validation checklist 跑并记录；未跑到的项标注未跑，不声称通过。
- R5：`CHANGELOG` 的 Fixed 一节必须把执行位那条写成升级理由——从 1.0.6 升级正是为了它。
- R6：标签推送与 GitHub Release 在用户明确授权后才执行。
- R7：记录标签、Release URL、发布提交、两个 catalog pin 与检查结果。

## Acceptance Criteria

- `origin/main` 上的发布提交同时含三个 manifest 的 `1.0.7` 与新的 CHANGELOG 段，且 `v1.0.6` 仍是其后代。
- 注解标签 `v1.0.7` 指向该提交；`git merge-base --is-ancestor v1.0.7 origin/main` 成功。
- 两个 catalog 的 `ref`/`sha` 与标签及其提交对应，`bash hooks/release-check .` 报 `STATUS: pass`。
- GitHub Release `v1.0.7` 的正文与 CHANGELOG 的 `[1.0.7]` 段一致。
- 检查结果有实际输出；推送前停下，等用户授权。

## In Scope

- 三个 manifest、`CHANGELOG.md`、两份 README 的版本字面量；两个 catalog 的 pin。
- 注解标签 `v1.0.7` 与 GitHub Release。
- 本任务 PRD / Plan 与 Todo 条目。

## Out of Scope

- **不改插件内容**：本次把关在 `main` 上的改动发出去，不顺带改 `hooks/` 或 `skills/` 的行为。
- `.codebuddy-plugin/marketplace.json` 里滞后的 `"version": "1.0.5"`。
- `RELEASE.md` 本身。
- inbox 里五条未 promote 的条目（`172455`、`88e04c`、`e7c041`、`9acf57`、`454ac4`）——下一版内容。

## Risks / Deferred Items

- **标签一旦推送即公开且难撤销**：删改远端标签需要所有者授权并记录理由。因此本任务在推送前停下。
- **原子推送是必需的**：分开推会出现「catalog 指着不存在或过期的标签」的窗口，落进去的刷新会装到上一版。若远端拒绝，按 `RELEASE.md` 的退路执行并记录该窗口。
- **本版包含一个上一版就有的缺陷修复**（启动器执行位）。CHANGELOG 若不写清楚，从 1.0.6 升级的用户不知道自己为什么该升。
- 运行时前提不变：hook 仍是 extensionless POSIX shell + awk。

## Open Questions

- 无阻塞项。路径、版本号、执行边界由用户在 2026-09-18 定稿。

## Version History

- v1 — planning。
