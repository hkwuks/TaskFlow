# 文档里关于「哪些宿主接了写前门」的陈述全线对齐

> Task version: v1
> Status: completed

## Goal

`README.md` / `README.zh-CN.md` 还写着「TaskFlow 在 Codex 上只接 SessionStart，写前门接不上」，而这句话在 `af8719a`（2026-10-30，随 v1.1.10 发布）之后就不成立了。更糟的是同一个仓库里两个来源互相矛盾：`hooks/README.md:252` 与 `runtime.md:286` 说 Codex 没接，`hooks/README.md:105` 与 `runtime.md:50` 说接了。读者无法判断该信哪一句。

## Background / Confirmed Facts

**Codex 实际接线**（`hooks/hooks-codex.json`）：
- `SessionStart` → `session-start`
- `UserPromptSubmit` → `prompt-reminder`
- `PreToolUse` matcher `apply_patch` → `capability-gate`
- `PostToolUse`（无 matcher）→ **`external-evidence`**
- **没有 `capability-evidence`**。`hooks/smoke-test:6540-6552` 用断言钉住这一点（`apply_patch records nothing`）。

**写前门已经能读补丁文本**：`hooks/capability-gate:60-68` 取 `tool_input.command` 为 `patch_text`，`:84-128` 按 `tool_name = apply_patch` 提取 `*** Update File:` / `*** Add File:` / `*** Delete File:` / `*** Move to:` 四类指令，逐个判定路径。

**因此三种能力必须在文档里分开说**，混在一起就会写出假话：
| 能力 | Claude Code | Codex | CodeBuddy | Trae | dsh |
| --- | --- | --- | --- | --- | --- |
| 记录能力调用（`capability-evidence`） | 是 | **否** | 是 | 是 | 否 |
| 拒绝阶段文档首次正文写入（`capability-gate`） | 是 | **是** | 是 | 是 | 否 |
| 外部查证记录（`external-evidence`） | 是 | 是 | 是 | 是 | 否 |

**故 Codex 上的阶段只能靠 `hooks/task unaided` 释放**：store 里没有 `invoke` 记录，`approve` 的 invoke 池为空。这一点必须写进文档，否则读者会照 README 去「先调一个能力再写文档」，然后在 Codex 上永远被拒。

**现状是一组互相矛盾的陈述**（都不是崩溃，但会误导读者用 `unaided` 绕过一扇其实存在的门，从而让证据记录失真）：
- `README.md:229`、`README.zh-CN.md:195` — 「只接 SessionStart，写前门接不上」。假；连「只接 SessionStart」本身也不准确，`UserPromptSubmit` 早就接了（`CHANGELOG.md:190`）。
- `README.md:124`/`:126`、`README.zh-CN.md:91`/`:93` — 门与记录都只列 Claude Code / CodeBuddy / Trae，漏 Codex。
- `hooks/README.md:250-255` — 「Codex 有事件但没有路径……两者都没接」。与同文件 `:105-109` 直接矛盾。
- `hooks/README.md:22`/`:24` — 两个脚本都标 `(Claude Code only)`，早已过时。
- `hooks/README.md:233-234` — 「这对 gate 接了 Claude Code / CodeBuddy / Trae」，漏 Codex 的门。
- `runtime.md:99` — 门的宿主列表漏 Codex，与同文件 `:50`、`:81` 矛盾。
- `runtime.md:286` — 「the Claude Code pre-write gate」，单宿主说法。
- `runtime.md:359` — `hooks-codex.json` 注释写 `SessionStart + UserPromptSubmit`，实际四个事件块。
- `runtime.md:143-144` — 「Codex's capability records come from `Skill` and MCP calls」，读起来像 Codex 会记录；实际一条都不记。
- `runtime.md:179-180` — dsh「SessionStart only」也不准确（也接了 `UserPromptSubmit`）。
- `hooks/smoke-test:6414-6415` 注释「the two hosts that are deliberately unwired」——现在只剩 dsh。

**明确不改的**：`CHANGELOG.md` 里历史版本说 Codex 无门（1.1.6/1.1.5 等）。那些在当时是真的，改它等于伪造历史。

## Requirements

- R1：所有文档把「记录能力调用」「拒绝阶段文档首次正文写入」「外部查证记录」当成三件独立的事分别陈述宿主范围，不得合并成一句。
- R2：凡是提到 Codex 有写前门的地方，同段必须说明 Codex 不记录能力调用、阶段靠 `hooks/task unaided` 释放。
- R3：`hooks/README.md` 内部自相矛盾必须消除（`:250-255` 与 `:105-109`；`:22`/`:24` 与 `:233-234`）。
- R4：`runtime.md` 内部自相矛盾必须消除（`:99`/`:286`/`:359`/`:143-144` 与 `:50`/`:81`）。
- R5：中文 README 与英文 README 逐段对应；能力名、脚本名、命令保持英文原文。
- R6：不修改 `CHANGELOG.md` 的任何历史条目。
- R7：`hooks/smoke-test:6414-6415` 的注释改为单数（只剩 dsh 未接）。
- R8：不得引入新的事实主张——每一条改动都必须能在 `hooks/hooks-*.json` 或 `hooks/capability-gate` 里核对。

## Acceptance Criteria

- AC1：`README.md:229` 与 `README.zh-CN.md:195` 不再出现 `SessionStart only` / `只接 SessionStart`，且列出 Codex 实际接的四个事件。
- AC2：`README.md:124`/`:126` 与 `README.zh-CN.md:91`/`:93` 出现 Codex，并带上「不记录能力调用 → 用 `unaided`」的限定。
- AC3：`hooks/README.md` 中 `Claude Code only`、`Neither is wired`、`the pair is wired for Claude Code, CodeBuddy, and Trae` 三处已与 `:105-109` 一致。
- AC4：`runtime.md` 中 `:99`、`:286`、`:359`、`:143-144`、`:179-180` 与 `:50`/`:81` 一致。
- AC5：`grep -rn 'SessionStart only\|只接 SessionStart\|Claude Code only\|Neither is wired'` 在 `README.md README.zh-CN.md hooks/README.md skills/taskflow/references/*.md` 上无命中（`CHANGELOG.md` 不在范围内）。
- AC6：`bash hooks/smoke-test` 全绿。
- AC7：`git diff --check` 无新问题。

## External Facts

- Depends on external facts: no
- Why not: 全部结论来自本仓库可核对的文件——接线见 `hooks/hooks-codex.json`，补丁解析见 `hooks/capability-gate:84-128`，防回归断言见 `hooks/smoke-test:6540-6552`，Codex 补丁格式的出处已由 `runtime.md:112-137` 记录。

## In Scope

- `README.md`、`README.zh-CN.md` 各自的 Codex 安装段与 hook 协作段。
- `hooks/README.md` 的文件清单、manifest 说明段、gate 需求段。
- `skills/taskflow/references/runtime.md` 的宿主表说明、gate 段落、Codex/dsh specifics、目录树注释。
- `hooks/smoke-test` 的**注释**（不改断言逻辑）。

## Out of Scope

- `CHANGELOG.md` 全部内容。
- 给 Codex 接 `capability-evidence`：那是功能变更，不是文档修正；`smoke-test:6540-6552` 目前把「不接」当契约钉着，要改需要独立任务。
- dsh 的写前门（`write`/`edit` 小写不匹配）：独立议题，本次只把「未接」的措辞改准。
- `skills/taskflow/references/artifacts.md` 的措辞：它不枚举宿主，读作通用规则成立，本次不动。
- 任何 README 的结构性重写。

## Risks / Deferred Items

- **风险：把 Codex 加进「直到该阶段确实调用过某项能力」那句话**，从而写出一个在该宿主上永远无法满足的条件。缓解：R2 要求门与记录分开陈述，AC2 逐字检查限定句在不在。
- **风险：过度修正**，例如把「documented, not yet measured」删掉。缓解：`runtime.md:50` 的 that 限定是对的，保留。
- **延后**：给 Codex 接 capability capture。若将来接上，`runtime.md:51`、`hooks/README.md` 与两份 README 需要再改一轮，届时以 `hooks-codex.json` 为准。
- **延后**：`dsh/cordis.patch.yml:3` 的「SessionStart hook」措辞（同属过时但不属本次 Codex 主线）。

## Open Questions

无阻塞问题。
