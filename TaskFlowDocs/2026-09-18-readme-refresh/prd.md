# Refresh both READMEs so they document the shipped surfaces
> Task version: v1
> Status: checking

## Goal

让两份 README 覆盖当前实际交付的表面：`hooks/`、`tools/`、`evals/` 三棵树，验证与 CI 检查，以及指向 `CONTRIBUTING.md` / `RELEASE.md` 的入口；同时修正与已实现行为不符的表述，并把中文版补齐到与英文版章节对齐。

## Background / Confirmed Facts

- 两份 README 上次改动是 2026-09-17 的 v1.0.6 发布提交（`f8e13a0`）；此后只有 marketplace pin 与 `RELEASE.md` 变化。README 没有落后于功能，落后的是**覆盖面**。
- `README.md` 的 `## Project map` 只列 `skills/taskflow/` 一棵树。仓库实际还有：
  - `hooks/`（22 个文件，含 `hooks/README.md`：每个 hook 的职责、为什么是 extensionless bash、三宿主安装、scope/safety 边界）；
  - `tools/fixture-compare`（逐字节比对两次 smoke-test 产出的 fixture）；
  - `evals/`（`README.md`、`runner.py`、`cases/taskflow.json`、`fixtures/`）；
  - `.claude-plugin/`、`.codex-plugin/`、`.codebuddy-plugin/` 三个宿主清单目录。
- **四套 CI 作业没有被任何 README 提到**（`.github/workflows/hooks.yml`）：`smoke`（Ubuntu / macOS / Windows 三平台矩阵，非 Windows 跑 `bash hooks/smoke-test`，Windows 跑 `hooks/smoke-test-windows.ps1`）、`release`（`bash hooks/release-check .`）、`todo-merge-audit`（`bash hooks/todo-check . <range>`）、`evals`（`python3 evals/runner.py`）。
- `bash hooks/smoke-test` 与 `python3 evals/runner.py` 只出现在 `TaskFlowDocs/achieved/**/plan.md`；根文档里阅读者看不到「这个仓库怎么验证」。
- `RELEASE.md` 存在（`# Release process`，含 `## Validation checklist`、`## Tag, catalog pin, and GitHub Release`、`## Rollback`、`## Known limitations`），但两份 README 都没有指向它；README 只写了「catalog 跟随 main、稳定条目钉在发布 tag + SHA」这个结论。`CONTRIBUTING.md` 的 `## Checks` 列了 PR 前必须跑的命令，README 也没指向它。
- **一处与实现不符**：`README.md` 的 NOTE 说 SessionStart hook「prints a short derived state summary … it writes nothing and never approves」。实际 `hooks/session-start` 把状态摘要写到 stderr、把派生上下文注入会话（`additionalContext`），并由 `session-record` 写所选任务的 `sessions.md`、由 `repository-docs-context` 同步 index 元数据——`README.md` 自己的 `## Repository documents` 段落已经这么写了，NOTE 与之自相矛盾。
- `README.zh-CN.md` 与英文版章节不对称。英文版有而中文版没有的实质内容：`### A concrete recovery story`（具体恢复示例）、`### Choose the right layer` 表格、`## Guardrails, not bureaucracy` 表格，以及英文版 `## Repository documents` 里关于 Todo merge driver、PR 模板门禁、`repository-check` / `release-check` 的四段。中文版「无侵入 Agent」段落的 hook 描述还是旧版（只说维护 index 元数据，未提 `sessions.md`）。
- 两份 README 的 `claude plugin list` 示例版本均为 `1.0.6`，与三个 manifest 一致；`hooks/release-check` 会把这三处当作受检版本字面量，本次不得改动它们。

## Requirements

- R1：两份 README 的 project map 补全实际交付面 —— `hooks/`（以链接指向 `hooks/README.md`，不逐文件罗列）、`tools/`、`evals/`、三个宿主插件清单目录。
- R2：两份 README 新增「验证与 CI」一节：`bash hooks/smoke-test`、`python3 evals/runner.py`、`bash hooks/repository-check .`、`bash hooks/release-check .` 四条命令，`.github/workflows/hooks.yml` 的四个作业，并链接 `CONTRIBUTING.md`（PR 前检查）与 `RELEASE.md`（发布清单）。
- R3：修正两份 README 对 SessionStart hook 的描述，口径与 `hooks/README.md` 一致：注入派生状态/路由上下文；只写所选任务的 `sessions.md` 与 `repository-docs/index.md` 的路由元数据；不写核心任务文档、不批准。
- R4：中文版补齐英文版已有的实质内容（`A concrete recovery story`、`Choose the right layer`、`Guardrails, not bureaucracy`、`Repository documents` 的 merge driver / PR 模板 / release-check 段落），使两份 README 的 `##` 章节一一对应。
- R5：不改变既有章节顺序与叙事结构；除上述增补与修正外不重写既有文案。

## Acceptance Criteria

- 两份 README 都出现 `hooks/`、`tools/`、`evals/` 三类目录及其用途；`hooks/README.md`、`CONTRIBUTING.md`、`RELEASE.md` 都有可点击的相对链接。
- 两份 README 都存在一节同时列出 `smoke-test`、`evals/runner.py`、`repository-check`、`release-check` 四条命令与 CI 四个作业名。
- 两份 README 的 `##` 章节集合一一对应（`###` 允许因呈现方式不同而不同，例如英文版用表格承载的对比项）。
- 两份 README 对 SessionStart hook 的描述与 `hooks/README.md` 不再冲突：不出现「writes nothing」这类与 `sessions.md` / index 元数据写入相矛盾的表述。
- `bash hooks/release-check .` → pass（两份 README 的 `claude plugin list` 示例仍为 `1.0.6`，三个 manifest 与两个 catalog 未被触碰）。
- `git diff --check` → clean；diff 只含 `README.md`、`README.zh-CN.md`、`TaskFlowDocs/todo.md` 与本任务目录。

## In Scope

- `README.md`、`README.zh-CN.md`。
- 本任务 PRD / Plan，以及 `TaskFlowDocs/todo.md` 的状态推进。

## Out of Scope

- `hooks/`、`skills/`、`evals/`、`tools/`、三个插件清单目录、`.github/` 的任何改动 —— 本任务只改文档，不改被文档描述的东西。
- 版本号变更与发布动作。
- 新增截图 / SVG 资产；`assets/taskflow-workflow.svg` 不动。
- 叙事结构重写或新增宣传性章节。

## Risks / Deferred Items

- 补全 project map 有过度的风险；R1 以「链接到 `hooks/README.md`」把 hook 逐文件清单留在原处，project map 只保留入口。
- 中文版补段落后篇幅增加，与英文版对齐；不影响 `release-check` 的版本取样（它只读 `claude plugin list` 示例行）。
- 本机 `bash hooks/smoke-test` 与 `main` 同形态失败（无解释器的 `toolbin/bash`），按 2026-09-17 任务的记录沿用该结论；本任务不改 hook，且 CI 矩阵会覆盖该套件。

## Open Questions

- 无阻塞项。范围（补全缺失事实）、流程（分支 + Todo + Plan）、语言口径（英文为准、中文同步）已由用户在 2026-09-18 确认。

## Version History

- v1 — planning。
