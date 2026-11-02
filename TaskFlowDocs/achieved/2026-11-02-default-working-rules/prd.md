# 给新用户一份可用的默认仓库规则，并在规则真正被需要时提出来

> Task version: v1
> Status: completed

## Goal

用户装上 TaskFlow、开一个新仓库时，仓库里只有他自己的代码和 README。TaskFlow 的每个阶段都假设仓库有规则可依——建分支要知道 `<type>` 前缀，写 commit 要知道格式，写代码要知道风格——但新用户不可能事先写好这些。

今天的结果是 `repository-check` 一直报 `needs-user-input`：`Document CONTRIBUTING.md: missing`、`Document CODE_STYLE.md: missing`，而 `repository-docs-context` 无条件把这两份当作权威来源去路由，于是新用户一上来就被指向两个不存在的文件。

本任务给 TaskFlow 带一份**默认仓库规则**，在规则真正被用到的三个阶段提出来，征得同意后写入用户仓库。用户已有规则时，只检查它有没有与 TaskFlow 冲突的地方并给建议，**不自动改**。

## Background / Confirmed Facts

以下均为 2026-11-02 在本仓库实测。

### 新用户的仓库里什么都没有

在一个只有 `README.md` 的新仓库里跑 `hooks/repository-check`：

```
Document CONTRIBUTING.md: missing
Document CODE_STYLE.md: missing
Document ROADMAP.md: missing
Catalog: missing
STATUS: needs-user-input
```

`hooks/repository-docs-context:64-65` 却写着：

```sh
add_entry repository-rule CONTRIBUTING.md design,code,commit,pr,release -
add_entry repository-rule CODE_STYLE.md code,review -
```

即：**它把两份不存在的文件登记为路由目标**。同一个脚本会自动创建 `index.md`（实测：在空仓库里跑一次就出现），但不会创建规则文档——`index.md` 只是路由记录，缺了不影响任何人；`CONTRIBUTING.md` 会出现在用户仓库根目录，性质完全不同，不能悄悄写。

### 规则在具体位置被真正读到

| 位置 | 需要什么规则 |
|---|---|
| `SKILL.md:133`、`:283` | 建分支时的 `<type>` 前缀 |
| `SKILL.md:150` | commit 归属，原文要求「去读 CONTRIBUTING」 |
| `artifacts.md:7` | 缺文档时怎么建 |
| `CODE_STYLE.md` 的 code 阶段 | 代码风格 |

这四个是**具体时刻**，不是抽象的"入口"：用户在那个时刻才第一次真正需要规则，也才判断得了这份默认值合不合他的意。

### 已有机制可以复用

`hooks/prompt-reminder` 是一个 `UserPromptSubmit` 钩子，**每条提示都会运行**，已经在把在途任务与分类问题放进 Agent 的上下文。它明确不写任何文件、不做判断、不匹配提示词——只在任务状态上触发。本任务的提醒可以挂在同一个事件上，不需要新造一套机制。

本仓库的 `CONTRIBUTING.md` 与 `CODE_STYLE.md` 里，通用部分与 TaskFlow 特有部分是分开的：

| 节 | 性质 |
|---|---|
| `CONTRIBUTING.md` `## Branches and commits` | 通用（`feature/` `fix/` `docs/` `chore/` 前缀、`<type>: <描述>`） |
| `CONTRIBUTING.md` `## Pull requests` | 通用（草稿优先、文档随 PR、验证记录） |
| `CONTRIBUTING.md` `## Checks` | 混合——命令是本仓库的 |
| `CONTRIBUTING.md` `## Working branches` / `## TaskFlow workflow` | TaskFlow 特有（worktree、`.worktrees/`、`hooks/task promote`） |
| `CODE_STYLE.md` 的 `## Markdown` / `## Shell` / `## Simplicity and compatibility` | 通用 |
| `CODE_STYLE.md` 的 `## Task artifacts` | TaskFlow 特有 |

## Requirements

- **R1 — 默认规则随插件分发，不是写死在 Skill 里。** 模板放在 `hooks/templates/`，用户同意后复制到他的仓库根目录，成为他自己的文件。用户之后可以随意改，插件不会再去碰它。

- **R2 — 只带通用部分。** `CONTRIBUTING.md` 模板含分支命名、commit 格式、PR 流程；`CODE_STYLE.md` 模板含 Markdown 与 Shell 风格、简洁与兼容性。不含 `TaskFlowDocs/achieved/`、capability store、`hooks/task` 子命令——那些是 TaskFlow 的实现细节，与用户仓库无关。

- **R3 — 三个触发点，每次提示都检查。** 建分支前、决定 commit 归属前、写代码前。用户选择"每次都问"，因此不做"问过一次就记住"的状态——仓库规则可能随时被创建或删除，缓存一个"已问过"标志会与仓库实际情况脱节。

- **R4 — 只在缺文件时提议，已有文件时检查冲突。** 缺失 → 问是否创建（先展示内容）。已存在 → 检查与 TaskFlow 的冲突点（例如规则要求所有改动走 PR，而 TaskFlow 的发布流程是直接 tag），**只给建议，不自动修改**。

- **R5 — 征得同意才写。** 提醒本身不改任何文件。读取、展示、等用户回答、再写——四步分开，任何一步都可以停在"不写"。

- **R6 — 冲突检查有可核对的依据。** 每条冲突建议要指向具体文件的具体行，以及它冲突的是 TaskFlow 的哪条规则。没有依据的"建议"是噪音。

## Acceptance Criteria

- **A1** 新仓库（无 `CONTRIBUTING.md`、无 `CODE_STYLE.md`）进入建分支阶段时，提醒指出缺哪份文件、并说明创建后会得到什么。

- **A2** 用户同意后，两份文件出现在仓库根目录，内容来自 `hooks/templates/`，且**不含** TaskFlow 特有内容（可 `grep` 验证：无 `TaskFlowDocs/achieved`、无 `capability`）。

- **A3** 用户不同意时不写任何文件，且下次进入同一阶段**仍会提醒**（用户选择的"每次都问"）。

- **A4** 用户仓库已有 `CONTRIBUTING.md` 时，不提议创建；若规则与 TaskFlow 冲突（如强制 PR 而发布走 tag），给出一条指向具体行的建议，且**不修改文件**。

- **A5** 提醒出现在用户选定的三个时刻：建分支前、commit 归属前、写代码前。不在这三个时刻之外触发。

- **A6** 提醒不阻塞工作流：不回答也能继续（它是一条提示，不是门禁）。

- **A7** 模板可离线使用，不依赖网络，不依赖 `gh`。

- **A8** 已有仓库（本仓库）的既有行为不受影响——提醒只在**缺文件**或**有冲突**时出现。

## External Facts

- Depends on external facts: no
- Why not: 这是纯粹的本地文件生成与文本比对，规则内容取自本仓库已有的 `CONTRIBUTING.md` 与 `CODE_STYLE.md`，不涉及任何仓库外的规范或版本化接口。钩子事件形状已在 `hooks/prompt-reminder` 的注释里记录为实测结论（2026-10-22），本任务复用同一事件，不引入新的外部契约。

## In Scope

- `hooks/templates/CONTRIBUTING.md`、`hooks/templates/CODE_STYLE.md` — 两份默认规则。
- 提醒逻辑：三个触发点，每次提示都检查缺文件/冲突。
- 冲突检查：至少覆盖"强制所有改动走 PR"这一类与 TaskFlow 发布流程相抵触的规则。
- 在 `skills/taskflow/SKILL.md` 与 `artifacts.md` 说明默认规则从哪里来、同意后才写入。
- smoke 断言覆盖 A1–A8。

## Out of Scope

- **不自动写入。** 任何未经用户同意就出现在用户仓库里的规则文件，都是本任务的失败。
- **不自动修改已有规则。** 只建议。
- **不生成 `ROADMAP.md`。** 产品方向无法从代码推断，`repository-check` 也已把它当作可选。
- **不覆盖用户已有文件。** 同名文件存在即视为用户所有。
- **不做一次性标记。** 用户明确选择每次都问。

## Risks / Deferred Items

- **"每次都问"会变成噪音。** 用户明确选择了这个代价，理由是仓库规则会变、缓存会脱节。缓解：提醒必须短，且只在三处出现；A6 保证它不阻塞。

- **模板会与本仓库的规则漂移。** 本仓库的 `CONTRIBUTING.md` 改了，`hooks/templates/` 不会自动跟随。缓解：模板只带**稳定**的通用部分（分支前缀、commit 格式），不复制会频繁变动的内容；并在模板文件头注明它源自哪一版。

- **冲突检查只能覆盖可机械判定的规则。** 例如"要求所有改动走 PR"与"发布直接 tag"这类可以判定；"分支命名是否合理"判定不了。本任务只做前者，后者留给用户。

## Open Questions

无——三个待定项已于 2026-11-02 与用户确认：从本仓库提炼通用部分；触发点为建分支前、commit 归属前、写代码前；每次都问。
