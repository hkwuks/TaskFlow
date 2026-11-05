# Spec — 分层完整性：把「失败修在失败所属的层」变成插件的硬规则

> Task version: v1

## Objective and Success Criteria

TaskFlow 目前能让一个任务被**记录、批准、验证、归档**，但没有任何一条规则约束**改动落在哪一层**。于是出现用户报告的两件事：

1. 模型不理解整体架构与各层职责，遇到粗粒度需求时只能从可见症状处下手；
2. 为了表面通过，去修改某一层的中间输出，让上一层的断言满足——这是目标欺骗。

本 Spec 定义修好这两件事所需的规则形状。成功标准：

- **SC1**：大/小任务的判定不再允许「一个文件」这类形态判据单独把小任务判出来；涉及跨层契约的任务必须写 `spec.md`。
- **SC2**：`spec.md` 的架构部分要求写清**每一层负责什么、不负责什么、它的输入输出契约是什么**，而不是只列出目录结构。
- **SC3**：一条**禁止性**规则明确规定：失败必须修在失败所属的层；为让下游检查通过而修改中间产物，属于目标欺骗，不是修复。
- **SC4**：上述规则能被 Phase 5/6 的现有文本引用到，不需要新 hook、新命令。

## Architecture Boundaries and Responsibilities

本仓库的三个效力层，**改动必须落在正确的那一层**（这条判定本身是另一条 Todo `TF-20261105-77051f`，此处只作为前提引用）：

| 层 | 路径 | 谁受影响 | 本次是否改 |
| --- | --- | --- | --- |
| 插件自身行为 | `skills/taskflow/SKILL.md`、`skills/taskflow/references/*.md` | 所有安装 TaskFlow 的人 | **是** |
| 发给用户仓库的默认模板 | `hooks/templates/*.md` | 仅当用户主动 `repo-rules create` | 否 |
| 本仓库自己的规则 | `CONTRIBUTING.md`、`CODE_STYLE.md` | 仅 TaskFlow 贡献者 | 否 |

**为什么是插件层**：用户 2026-11-05 明确纠正——这条规则与「哪个仓库」无关，它是插件要实现的功能。写进 `hooks/templates/` 只会在用户同意 `repo-rules create` 后才生效，管不了插件自己的工作方式。

改动涉及的两个文件，其职责也不同：

- `SKILL.md` 是**流程约束**：它是 Agent 每一步读的东西，禁止性规则必须在这里，且必须在会被读到的位置（Phase 3 分类、Phase 5 实现、Phase 6 验证）。
- `references/artifacts.md` 是**产物形状**：`spec.md` 和 `plan.md` 的模板在它里面，架构理解的具体字段属于这里。

## Project Structure / Affected Files

```text
skills/taskflow/SKILL.md
  - Phase 3「Classify the task」：重写大/小判据
  - Phase 3 末段：spec.md 内容要求，增加分层契约
  - Phase 5「Build」：新增禁止性规则
  - Phase 6「Verify and review」：新增一条验证项

skills/taskflow/references/artifacts.md
  - Spec outline：架构节的字段说明
```

**不改动**：

- `hooks/task` 的 `No spec required` scaffold 文案（它是占位符，不影响判据）
- 任何 hook 逻辑——本任务不新增校验，规则靠 Agent 读取与自述
- `hooks/templates/*`——见上

## Interfaces, Data Flow, and Contracts

本任务不引入新的接口或数据结构。它改变的是**文档中规则文本的形状**，以及 Agent 读这些文本时被要求做出的判断。

三个契约点：

1. **判据契约**：一个任务被判为 small，必须同时满足「不涉及跨层契约」——形态判据（文件数、时长）不再是充分条件。
2. **产物契约**：`spec.md` 的架构节必须能回答「这一层不负责什么」，而不只是「这一层有哪些文件」。
3. **禁止契约**：修改中间产物以使下游通过，被明确命名为目标欺骗；修复必须发生在其所属层。

## Invariants and Compatibility

- **不新增 hook**：规则靠文本与 Agent 判断执行，与此前「靠模型判定」的用户决定一致（2026-11-05）。
- **不破坏既有阶段门**：`spec.md` 仍是 large 才必需；本任务只收紧「什么算 large」。
- **既有任务不重写**：`TaskFlowDocs/achieved/` 只读。
- **中英文一致**：`SKILL.md` 是英文文档，规则文本用英文；不涉及 README 双语文档。

## Validation and Error Semantics

- 违反禁止规则时没有机械报错——它是**行为约束**，由 Phase 6 的自述检查兜底。
- 判据被误用（把跨层任务判成 small）时，后果是 `spec.md` 缺失、架构节为空；Phase 6 的验证项会发现「Plan 里没有分层说明」。
- 任何改动不得让现有 `bash hooks/smoke-test` 变红。

## Code and Test Constraints

- `SKILL.md` 与 `references/*.md` 的既有措辞风格：**陈述规则 + 说明为什么**，通常带一个实测日期或具体代价。新文本必须沿用这个风格，不能只写一句话规定。
- 不写「建议」「尽量」——用户已定为**禁止性**（2026-11-05 决定 3）。
- `hooks/smoke-test` 没有针对文档措辞的断言需要改（已核对：唯一相关的 `Codex`/`lowercase` 断言与本任务无关）。

## Design Decisions and Alternatives

| 方案 | 取舍 |
| --- | --- |
| **A（选定）**：改 `SKILL.md` + `artifacts.md` 的文本 | 零新 hook，与「靠模型判断」的决定一致；弱点是靠自觉 |
| B：加 `PreToolUse` 拦截测试文件改动 | 误报多，外部研究（EvilGenie）显示收益不如独立判断者；用户未选 |
| C：在 `hooks/task` 里校验 `spec.md` 架构节非空 | 机械但脆弱——空节可以填废话，检查不出去；且用户已决定「靠模型」 |
| D：写进 `hooks/templates/CODE_STYLE.md` | 用户已明确否决：那是发给别人仓库的建议，不是插件行为 |

**架构理解为何仍放在 `spec.md` 而不新增产物**（用户 2026-11-05 决定 1）：`spec.md` 已有 `## Architecture Boundaries and Responsibilities` 与 `## Interfaces, Data Flow, and Contracts` 两节，机制存在只是没被要求填实。新增产物会违反「不创建重复的事实来源」。真正的修法是**强化大小任务判据**，让跨层任务不会绕过 `spec.md`。

## Open Questions

无阻塞问题。
