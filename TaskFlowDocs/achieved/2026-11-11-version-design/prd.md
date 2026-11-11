# 任务文档升版时继承并修订已有设计
> Task version: v1
> Status: completed

## Goal

修复任务升版后既有设计可能被整体重写而遗漏的问题，保留有效需求、设计和决策。

## Task Kind

- Kind: defect

## Background / Confirmed Facts

- `hooks/version` 复制选中的旧文档并保留根目录正文，只修改版本、状态和审批字段；现有 smoke 主要检查归档、版本及状态，没有完整对比三个根文档的正文。
- 现有版本参考只笼统要求编辑语义变化，未在主要升版入口明确要求逐项继承或在审核中对照。
- 已完成的 TF-20260911-05 解决历史版本留存，本任务关注新版本设计承接及后续编辑。

## Requirements

- 以当前 PRD、Spec、Plan 为基础，保留仍有效的设计、需求、约束、决策与已完成步骤；对新需求所影响的部分增补、修改或明确废止。
- 升版审核对照旧版本和新版本，确认未受影响内容保留，并说明改变或废止的依据；不增加自动阻断。
- 历史版本继续可恢复，已有版本机制和用户审批不变。

## Acceptance Criteria

- 主入口与版本参考明确继承、按需修订以及审核对照；对不同意保留的旧内容允许有明确依据的修改或废止。
- 针对三个核心文档验证升版机械转换保留正文和完成记录，同时检查历史归档及审批状态。
- 不声称机器检查可以保证模型后续语义编辑没有遗漏。

## External Facts

- Depends on external facts: no
- Why not: 依据 `hooks/version`、`hooks/smoke-test` 和用户确认的工作流决策。

## In Scope

插件自身 Skill、版本参考及现有 smoke 测试。

## Out of Scope

历史任务文档重写、模型行为强制拦截或兼容代码。

## Risks / Deferred Items

行为指导及人工审核不能保证模型总是遵循；真实宿主效果后续观察。

## Open Questions

无；用户已确认继承有效设计、非阻断对照及保留已完成步骤。