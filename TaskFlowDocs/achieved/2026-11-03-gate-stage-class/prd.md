# 门拒绝提示只广播了阶段的一半概念类

> Task version: v1
> Status: completed

## Goal

让 `hooks/capability-gate` 的拒绝提示说出该阶段的**全部**概念类，和 `SKILL.md` phase 表保持一致；并使这两份手抄表之间的差异由断言捕获，而不是靠人记住。

## Background / Confirmed Facts

同一份概念类名单在本仓库有三份手抄副本，其中两份被双向对账钉住，第三份没有：

| 位置 | 作用 | 是否被断言钉住 |
| --- | --- | --- |
| `skills/taskflow/SKILL.md:171` phase 表 | 人读的文档副本 | ✅ `hooks/smoke-test:2993` 与 `concept_class_re` 双向对账 |
| `hooks/task:660` `concept_class_re` | `unaided --considered` 的校验词表 | ✅ 同上 |
| `hooks/capability-gate:29-35` `stage_class()` | 门的拒绝提示写哪个类 | ❌ **零断言**（`stage_class` 在 smoke-test 中 0 次命中） |

实测差异（2026-11-03 读本仓库）：phase 表 phase 1 行写的是

```
requirements elicitation and framing; divergent exploration
```

而 `stage_class PRD` 只返回 `requirements elicitation and framing`。`divergent exploration` 在 `hooks/task:660` 的词表里，`hooks/task unaided PRD --considered 'divergent exploration'` 完全合法（`hooks/smoke-test:3445` 专门断言它必须被接受），但门的拒绝提示从不提它。

**本会话的现场证据。** 写本 PRD 时被门拦下，提示原文是：

```
TaskFlow pre-write gate blocked stage [PRD]: no capability invocation is recorded for this task version. ... If no capability fits this phase, declare it:  bash hooks/task unaided PRD --considered 'requirements elicitation and framing'.
```

本次这个阶段真正适用的正是它没提到的那个类。

这条不对称不是疏忽，是上一轮任务的显式决定：`TaskFlowDocs/achieved/2026-10-08-capability-concept-classes/prd.md:79` 的验收标准 **A5** 要求 `stage_class()` 文本「不变」，并写明「拒绝提示因此不含 `divergent exploration`，该选择在 Spec 判定中记录」。本次是补它的空，不是推翻那个决定——当时的取舍是「不动门的文本」，代价正是本条。

**为什么值得修**：门是唯一「在正要写文档那一刻、无法忽略」的投递渠道。被拦下的模型看到什么，几乎决定它下一步做什么。若它本想发散探索，提示只给出收敛那个类，它要么去调一个不合适的能力，要么用错误的类申报 unaided——而正确答案一直存在，只是在需要它的那一刻没被说出口。

## Requirements

### R1 — 门的提示列出阶段的全部概念类

`stage_class()` 对每个受门控的阶段（PRD / Spec / Plan）返回 phase 表该阶段概念类列的**原文**，以 `; ` 分隔。

### R2 — 逃生命令仍然可复制粘贴

拒绝提示里的 `bash hooks/task unaided <stage> --considered '<class>'` 仍给出**一个**类（列表中的第一个），因为 `--considered` 记录的是「实际适用的是哪一个」。多类时提示另起一句列出全部候选，让读者按实际情形改写。

### R3 — 断言钉住两份手抄表

`hooks/smoke-test` 新增断言：对 PRD / Spec / Plan 三个受门控阶段，从 `SKILL.md` phase 表中按产物名（`` `prd.md` `` / `` `spec.md` `` / `` `plan.md` ``）定位该阶段行，取概念类列；`stage_class` 的输出与该列在**双向**上一致，允许 `concept_class_re` 已有的「类名词根 + 可选后缀」变体约定。

## Acceptance Criteria

- **A1**：`bash hooks/capability-gate` 对 `prd.md` 的拒绝提示同时含 `requirements elicitation and framing` 与 `divergent exploration`。
- **A2**：该提示里的 `task unaided PRD --considered '<...>'` 命令可原样执行并成功（退出 0）。
- **A3**：`stage_class Spec` / `stage_class Plan` 的返回值与 phase 表对应行一致（当前已一致，断言防回归）。
- **A4**：新增断言在把 `divergent exploration` 从 `stage_class PRD` 里删掉时**变红**（变异验证）。
- **A5**：`bash hooks/smoke-test` 全绿。

## External Facts

- Depends on external facts: no
- Why not: 三份表的对齐关系是本仓库内部的机械事实，证据是 `skills/taskflow/SKILL.md`、`hooks/task`、`hooks/capability-gate`、`hooks/smoke-test` 四个文件本身。

## In Scope

- `hooks/capability-gate`：`stage_class()` 的返回值与拒绝提示措辞。
- `hooks/smoke-test`：新增对账断言 + 变异验证。
- 本任务的两份核心文档。

## Out of Scope

- 重构三份表为单一来源（`2026-10-08-capability-concept-classes` 的 Deferred 已记，属独立的较大改动）。
- `hooks/task:660` `concept_class_re` 的子串宽松校验（同 PRD 的 B5）。
- `TF-20261009-8abbd6` 主体：把阶段能力选择与宿主工具调用流解耦。

## Risks / Deferred Items

- **R1 风险**：从 markdown 表格按产物名取行，依赖表头与行格式。缓解：按 `` `<artifact>` `` 单元格定位，不按行号，且断言失败信息打印找到的行。
- **Deferred**：三份表合并为单一来源，另立任务。
