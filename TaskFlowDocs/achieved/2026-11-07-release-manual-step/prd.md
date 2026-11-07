# 发布流程：手工三宿主 catalog 校验
> Task version: v1
> Status: completed

## Goal

决定 `RELEASE.md` 步骤 6 里那句「Validate the catalog entry with Claude Code, Codex, and CodeBuddy tooling」的去留：它从不在 CI 里跑，唯一可离线判定的失败模式已被 `hooks/release-check` 覆盖，而它所在的位置使它无法充当门。

## Background / Confirmed Facts

**它在哪**：`RELEASE.md:151`，是步骤 6 的一部分。步骤 6 的完整内容是「在推送后的 `main` 上重跑 `release-check`、用批准的说明创建 GitHub Release、**校验 catalog 条目**」。

**它的位置决定了它不能是门**：步骤 5 已经执行 `git push --atomic origin main refs/tags/vX.Y.Z`。tag 不可变，推送已完成。此时校验失败，能做的只有回滚或补丁版本——它证明不了任何事，只是事后确认。

**它唯一的离线失败模式已被覆盖**：catalog 条目能离线判断的对错就是「`ref` 指向的 tag 是否真的解析到 `sha` 写的那个 commit」。`hooks/release-check` 已经做这件事（`git merge-base --is-ancestor` 加 `ref`/`sha` 配对校验），并且步骤 6 第一句就是重跑它。剩下的是「真实安装一次看能不能装上」，那是联网动作，CI 从未执行过。

**三宿主这个说法本身也不准**：仓库里只有两个 marketplace catalog ——`.claude-plugin/marketplace.json` 与 `.codebuddy-plugin/marketplace.json`。`.codex-plugin/` 只有 `plugin.json`，没有 catalog 文件；Codex 安装文档写的是 `codex plugin marketplace add hkwuks/TaskFlow`，用的是 Claude Code 那份 catalog。所以「three-host catalog validation」在三份 catalog 上做不到，只有两份。

**为什么它不是零成本**：它是发布清单上一条无判据的步骤。没有说通过的标准是什么、失败长什么样、记录在哪。这种步骤会被跳过，而跳过与通过无法区分——正是 `RELEASE.md` 自己在别处反对的那种东西（「Do not claim an unavailable check passed」）。

## Requirements

1. 删掉步骤 6 里的手工校验句。
2. 在同一个位置说明为什么不需要它，以及真实安装校验属于什么性质——这是本次唯一保留的信息价值。
3. 不改 `hooks/release-check`：它已经覆盖可离线判定的部分。
4. 不改步骤 6 的其余内容（重跑 `release-check`、创建 Release、标题格式）。

## Acceptance Criteria

- `RELEASE.md` 不再包含「Validate the catalog entry with Claude Code, Codex, and CodeBuddy tooling」。
- 步骤 6 说明：catalog 的机械正确性由 `release-check` 判定；端到端安装是联网的人工抽查，不是发布门，也不在清单上。
- `bash hooks/smoke-test` 通过（现有断言 pin 了 `RELEASE.md` 的其他句子，不得误伤）。
- `git diff --check` 通过。

## External Facts

- Depends on external facts: no
- Why not: 判断依据全在仓库内 —— `RELEASE.md` 的步骤顺序、`hooks/release-check` 的既有检查、`.codex-plugin/` 下没有 catalog 文件这一事实。

## In Scope

- `RELEASE.md` 步骤 6。

## Out of Scope

- 不改 `hooks/release-check`：可离线判定的部分它已经做了，重复实现是第二个漂移点。
- 不给 Codex 新建 catalog：那是另一件事（Codex 复用了 Claude Code 的 catalog 是既有安排），不在本条范围内。
- 不在发布流程里加联网校验：`RELEASE.md` 的检查全部离线且确定性，加一个 `curl` 会让发布在 DNS 抖动时变红。

## Risks / Deferred Items

- 风险：删掉后真实安装问题只能在用户那里发现。缓解：这正是当前状态——那句手工校验从未在 CI 里跑过，删掉的是一条无法证明执行过的步骤，不是一条真实存在的保护。
- 遗留：若要补端到端安装验证，它属于 CI（对已发布 tag 做一次 `plugin install`），不属于发布清单。未在本条范围内。

## Open Questions

无。
