# 开发本仓库前先判定改动目标属于哪一类
> Task version: v1
> Status: in_progress

## Goal

在本仓库开工前，先判定这次改动落在三个**效力范围完全不同**的哪一处，并据此选对文件；把这条判定写成一条仓库规则，使后续开发不会再把「插件自身能力」「插件发给用户仓库的默认规则模板」「本仓库自己的规则」混为一谈。

## Background / Confirmed Facts

本仓库同时是插件本体和它自己的开发仓库，因此同一个「改规则」的动作有三个落点：

| 落点 | 生效范围 | 谁能看到 | 改错的代价 |
| --- | --- | --- | --- |
| `skills/taskflow/`、`hooks/`（`hooks/templates/` 除外） | 插件自身行为 | 每一个安装者 | 静默改变所有人的工作流 |
| `hooks/templates/CONTRIBUTING.md`、`hooks/templates/CODE_STYLE.md` | 插件发给用户仓库的默认规则 | 仅当该仓库主动 `hooks/repo-rules create` | 只是建议性质，装不装由用户决定 |
| 本仓库根的 `CONTRIBUTING.md`、`CODE_STYLE.md` | 仅本仓库的开发约定 | 只影响 TaskFlow 自己的贡献者 | 不影响任何插件用户 |

已确认的事实：

- `hooks/repo-rules` 的注释（第 8–27 行）写明 `show`/`create`/`check` 三者的分工，`create` 只在文件不存在时写入。模板是「别人仓库的文件」，不是插件代码。
- `hooks/smoke-test:7405-7414` 断言模板里**不得**出现 `TaskFlowDocs/achieved` 和「capability」，即模板必须与实现细节脱钩。这从机制上证明模板不是插件行为的一部分。
- 本仓库 `CONTRIBUTING.md` 已经承载了落地规则，`hooks/smoke-test:3043-3086` 逐条 pin 住其中若干固定句式，说明这是仓库规则的既有维护方式。
- `#121` 之前的实际教训：讨论「分层规则写到哪」时，把「插件自身规则」和「发给用户的默认模板」当成了一回事，向用户提出了方向错误的选择题。用户纠正原话：「不是应该写仓库，这跟仓库没有关系，你老是把关系搞混。我这个仓库就是开发这个插件的，这个插件要实现这个功能。」

## Requirements

1. 在 `CONTRIBUTING.md` 中新增一节，把「先判定改动目标」作为开工的第一个问题，并给出三个落点的表。
2. 判据必须是**谁受影响**，而不是文件在哪个目录——`hooks/templates/` 与 `hooks/` 同属一个父目录，靠目录判断会出错。
3. 明确 `hooks/templates/` 的特殊性：它是发给别人仓库的建议，改动它等于改「插件给用户的默认值」，不是改插件行为，也不是改本仓库规则。
4. 该节必须能独立回答「这条规则改动本身落在哪」这一类问题，避免规则自身成为反例。
5. 在 `hooks/smoke-test` 中加断言，把该节的存在与关键判据 pin 住，防止后续改写时静默丢失。

## Acceptance Criteria

- `CONTRIBUTING.md` 含一个新节，标题与位置能让人在「Before you start」附近读到它。
- 该节含三行落点表，三行都与上表语义一致。
- 该节明确写出：判据是「谁受到影响」，不是「文件在哪个目录」。
- `hooks/smoke-test` 新增断言在该节被删除或关键句被改写时失败。
- `bash hooks/smoke-test` 通过（CI 三宿主矩阵为准，本地仅作预检）。
- `git diff --check` 通过。

## External Facts

- Depends on external facts: no
- Why not: 三者的效力范围由本仓库自身的实现与文档决定，`hooks/repo-rules`、`hooks/smoke-test`、`CONTRIBUTING.md` 都是仓库内事实，无需外部来源。

## In Scope

- `CONTRIBUTING.md` 新增一节。
- `hooks/smoke-test` 新增对应断言。
- `TaskFlowDocs/todo.md` 该条目的状态流转。

## Out of Scope

- 不修改 `skills/taskflow/SKILL.md`：那条规则对插件用户没有意义，写进去等于强迫所有人学 TaskFlow 的开发布局。
- 不修改 `hooks/templates/` 下任何文件。
- 不改 `CODE_STYLE.md`：本次要约束的是「改哪个文件」的判定，不是代码风格。
- 不重构 `hooks/repo-rules`。

## Risks / Deferred Items

- 风险：新增一节若写得太抽象，仍会被跳过。缓解：判据落成一句可直接自问的话，并配具体例子（`hooks/templates/` 那个反直觉例子）。
- 遗留：未给 `SKILL.md` 增加任何交叉引用，因此插件用户在别的仓库里不会看到这条规则——这是刻意的，见 Out of Scope。

## Open Questions

无。
