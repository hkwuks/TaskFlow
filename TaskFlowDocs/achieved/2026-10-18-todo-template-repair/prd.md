# 修复 todo.md 的模板块与残留标题

> Task version: v1
> Status: completed

## Goal

`TaskFlowDocs/todo.md` 的 `## Item template` 文档块停在条目中间、其字段名已与 `hooks/task intake` 实际写出的字段脱节、块后还留着一句被截断的半句；文件里另有一个空壳标题混在真条目之间。修掉这四处，并加一条断言让模板不再脱节。

## Background / Confirmed Facts

- **模板位置**：`## Item template` 在第 666 行，上面是 2026-09-08 的条目、下面是 2026-09-11 起的一整段条目——它不在文件前言里。
- **截断句**：第 695 行 `Every direct request or imported requireme`。**字节不可从 git 历史还原**：文件第一个版本（`660679a:152`）里它就已经是这句半句，此后未被改动，全历史检索只命中这一处。但**语意有仓库先例**：写这个模板的任务自己的 PRD 里留着完整说法——`TaskFlowDocs/achieved/2026-09-07-repository-docs-workspace/prd.md:45`：`Every direct or imported requirement is traceable to a Todo item before task handling; batch imports preserve one item per source requirement.` 所以本次是按既有先例补写，不是发明。
- **字段脱节**（模板 vs `hooks/task intake` 实际写出，见 `hooks/task:370-384`）：

  | 模板写的 | `intake` 实际写 |
  | --- | --- |
  | `## T-YYYYMMDD-001 — Short title` | `## <goal 前 80 字节>` |
  | （无 `- ID:`） | `- ID: TF-<yyyymmdd>-<checksum 前 6 位>` |
  | `- Next:` | `- Next action:` |
  | `- External:` | **不写**（全文件仅 20 处历史条目有，均为人手写） |
  | （无 `- Added:`） | `- Added: <today>` |

- **空壳标题**：第 1230 行 `## State in the Skill that personal supplements are local-only`，无正文、无 `- ID:`，夹在 `TF-20260914-02` 与 `TF-20260919-6b4e21` 之间；同名的真条目在第 441 行（`TF-20260914-03`）。它由 `790c27a` 那次「intake 写进上一个 `##` 节」的 bug 注入——正是 `TF-20260921-337ab8` 记录的那次。
- **没有任何 hook 解析 markdown 围栏**（全 `hooks/` 目录搜 ``` 只命中文档与夹具数据）。所以模板块里的 `## T-YYYYMMDD-001 — Short title` 对所有 hook 而言就是一个**真的节边界**。今天的模板没有 `- ID:` 行，两个受影响 hook 因此只是**碰巧**正确：
  - `hooks/task remove`（`:505-517`）从标题往下找第一个 `^## ` 就停——围栏内标题先被撞上，于是 `## Removed` 被写进围栏里。**实测复现**：在骨架含 `- ID:` 时墓碑落在 ```markdown 与内层标题之间。
  - `hooks/summarize-state`（`:125`）只按 ID 值白名单跳过占位符（`T-YYYYMMDD-001` / `YYYYMMDD-001`）；骨架一旦带 `- ID:`，占位条目就会出现在每次会话的 inbox 列表里。**实测复现**。
  - `hooks/task intake` 不受影响：**实测**，模板在 `## Items` 之下时新条目插在模板之前（插入点在 `:336-343`，跳过空行与 HTML 注释后即停）。
- 现状规模：`## ` 99 个、`- ID:` 84 个；差额里除三个前言节（`## Status flow`、`## Items`）与模板的两行外，其余是 **19 个只有标题、字段行在其下** 的旧式条目。**已核**：19 个全部带 `- Status: done` 与 `- Goal:`，都是真条目（早期 `## <ID> — <title>` 的写法），不含空壳。

## Requirements

- `## Item template` 移到文件前言区（`## Status flow` / `## Items` 一带），不再夹在条目之间。
- **模板的骨架体不得含 `- ID:` 行。** 这是本次最硬的一条约束：一旦含 ID，`remove` 会把墓碑写进围栏、`summarize-state` 会把占位条目打进每次会话的 inbox 列表（两者均已实测复现）。对齐字段名时 `- ID:` 只能出现在围栏外的说明里，不能作为骨架行。
- 模板的字段名与顺序对齐 `hooks/task intake` 实际写出的集合：`ID / Status / Priority / Owner / Source / Added / Updated / Goal / Task / Next action`；不再列 `- External:`（或标注为「可选、非 intake 写入」）。
- 模板的标题行改为反映真实形态（heading 由 Goal 派生），不再暗示存在 `T-YYYYMMDD-001` 这种 ID 形态；**改这一行前要知道**：`merge-todo` 把围栏内标题当作条目标题，改名会让与未改分支的合并变成冲突（那些分支未共享，本次可安全落地）。
- 第 682 行的截断半句按新写的完整句或直接删除处理，不留半句。
- 删除第 1230 行的空壳标题（其同名真条目在第 441 行，信息不丢）。
- `hooks/smoke-test` 新增一条断言：**直接读真实的 `TaskFlowDocs/todo.md`**，比对模板块的字段名集合与 `hooks/task` 写入的字段名集合，并单独钉住「骨架体不含 `- ID:` 行」；失败信息要说清缺哪个字段。这条断言是仓库里第一条 fence-aware 的检查。

## Acceptance Criteria

- `todo.md` 里 `## Item template` 之前不再有任何 `- ID:` 条目。
- 模板字段集 == `intake` 写出集（由新断言钉住，且把任一字段删掉时断言变红）。
- 模板骨架体内不含 `- ID:` 行，且新断言覆盖这一点。
- 第 1230 行那个空壳标题消失，且 `TF-20260914-03`（第 441 行）仍完整。
- `bash hooks/smoke-test` 全绿；`bash hooks/todo-check .` 与 `bash hooks/repository-check .` 通过。
- `git diff --check` 干净。

## In Scope

- `TaskFlowDocs/todo.md` 的前言区、模板块、以及第 1230 行的空壳标题。
- `hooks/smoke-test`（新增断言）。
- 若模板迁移或 ID 约束需要，则同时调整 `hooks/task` 的插入/墓碑定位逻辑（使其跳过围栏）。

## Out of Scope

- **`done` 条目占 72%（82 KB / 82 条）的增长问题**——用户 2026-09-19 明确排除（「先立一个 todo，我后面研究修复」），本次不做（`TF-20260919-6b4e21`）。
- 19 个只有标题的旧式条目：除非查证发现其中有非真条目，否则只记录、不改。
- `## Removed` 节的墓碑条目。
- 任何 `TaskFlowDocs/achieved/` 下的文档。

## Risks / Deferred Items

- **风险**：把模板移入前言后，若 `intake` 的插入点是「`## Items` 之后的第一个非空行」，新条目会插到模板**之前**，于是模板又回到条目下方。缓解：已实测确认这正是会发生的行为（见 Plan 的 Skills / Tools Used 第 2 条）——所以模板**紧贴 `## Items` 注释之下**是最稳的位置，且模板会随每次新增条目被推得更靠下，这属于可接受的可读性退化（不是正确性问题）。
- **风险**：模板里的 `## T-YYYYMMDD-001` 对 hook 而言就是一个节边界（无 fence 感知）。本次改为缩进示例后，示例内不再有列 0 的 `## `，这个节边界随之消失——这是净改善。
- **`merge-todo` 的前言归属**：driver 在 `hooks/merge-todo:14` 明写「第一个 `## ` 之前的内容取我们这一侧」，**另一侧对前言的编辑会被静默丢弃**（实测：base/ours/theirs 三方各改前言 → exit 0、结果取 ours、无冲突无提示）。模板移入前言等于把更多内容放进这个「只有一侧能赢」的区域。本次不修 driver（超出范围），但记在这里。
- **`- External:` 已死，但两处规范性文字还在要求它**：`skills/taskflow/SKILL.md:58` 与 `:148` 仍写「external identifier/link when available」，而全仓库没有任何 hook 读 `External`，`intake` 也从不写它。本次只对齐模板，不顺手改这两句——留作 follow-up，避免把「模板对齐」扩大成「规则改写」。
- `TF-20260919-6b4e21`：`done` 条目占约 72%（约 82 KB / 82 条）的增长问题，用户研究后再定，本次不动。

## Open Questions

无阻塞问题。（原先挂着的「19 个只有标题的旧式条目是否都是真条目」已核完毕：全部是，且其中两条刻意用 `- Task: None — …` 记录「直接改、无任务目录」，是既有约定而非损伤。）

## Version History

- v1 — planning：修四处结构损伤 + 一条防脱节断言；增长那一半按用户既有决定排除。
