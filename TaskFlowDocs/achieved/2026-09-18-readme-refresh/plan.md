# Plan — Refresh both READMEs so they document the shipped surfaces
> Task version: v1
> Status: completed

No spec required — 单层文档改动，无跨文件契约（除两份 README 的章节需互相对齐）。

## Reference Pointers

- `README.md` / `README.zh-CN.md` —— 唯二被改的文件。
- `hooks/README.md` —— hook 职责与 scope/safety 边界的权威表述；R3 的中文口径与它对齐，R1 的 project map 链接指向它。
- `.github/workflows/hooks.yml` —— R2 要记录的四个 CI 作业。
- `CONTRIBUTING.md`（`## Working branches`、`## Checks`、`## Pull requests`）与 `RELEASE.md`（`## Validation checklist`）—— R2 要链接的两份文档。
- `hooks/release-check` —— 受检版本字面量清单中包含两份 README 的 `claude plugin list` 示例行；本任务不得改动这些行。
- `TaskFlowDocs/achieved/2026-09-17-atomic-release-push/plan.md` —— 本机 `bash hooks/smoke-test` 失败的既有判定记录。

## Related Tasks

- Depends on: 无。
- Related: `TaskFlowDocs/achieved/2026-09-17-release-v1-0-6/`（最后一次改 README 的发布任务）。
- 无关活跃任务：`2026-09-16-duplicate-todo-id`、`2026-09-16-capability-selection-enforcement`、`2026-09-17-atomic-release-push`（checking）。

## Skills / Tools Used (Optional)

- 未调用额外 Skill。事实核对用仓库内检索完成（两份 README 的章节/路径引用、`hooks/README.md`、`.github/workflows/hooks.yml`、`RELEASE.md`、五个插件清单与 `hooks/release-check` 的受检清单），未使用外部资料。
- 文档渲染未做浏览器验证；链接有效性以相对路径存在于仓库中为准。

## Preconditions

- [x] 适用仓库文档已读：`README.md`、`README.zh-CN.md`、`hooks/README.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`、`RELEASE.md`、`CHANGELOG.md`、`TaskFlowDocs/repository-docs/index.md`。
- [x] `git switch -c docs/readme-refresh main` —— 分支已建，未在 base 工作区实施。
- [x] 本任务在 `TaskFlowDocs/todo.md` 登记为 `TF-20260918-13ff42` 并升级为任务。
- [x] 用户在 2026-09-18 确认范围（补全缺失事实）、流程（分支 + Todo + Plan）与语言口径（英文为准、中文同步）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-18 19:57 +0800
- Approved version: v1
- Approved scope: Plan v1 全部三步——只改 `README.md` 与 `README.zh-CN.md`；不改 `hooks/`、`skills/`、`evals/`、`tools/`、三个宿主清单、`.github/`，不动 `claude plugin list` 示例的 `1.0.6` 字面量，不做发布动作。

## Steps

### Step 1 — 补全英文 README 的缺失事实并修正 hook 描述

- Goal: `README.md` 覆盖实际交付面（`hooks/`、`tools/`、`evals/`、宿主清单）、验证与 CI、以及 `CONTRIBUTING.md` / `RELEASE.md` 入口；SessionStart hook 描述与 `hooks/README.md` 一致。
- Dependencies: 无。
- Files: `README.md`。
- Implementation checklist:
  - [x] `## Project map` 扩为仓库结构：保留 `skills/taskflow/` 树，补 `hooks/`（一行 + 链接 `hooks/README.md`）、`tools/fixture-compare`、`evals/`、`.claude-plugin/` / `.codex-plugin/` / `.codebuddy-plugin/`。
  - [x] 新增 `## Verification and CI` 一节：四条本地命令（`bash hooks/smoke-test`、`python3 evals/runner.py`、`bash hooks/repository-check .`、`bash hooks/release-check .`）各一句用途，`.github/workflows/hooks.yml` 的四个作业（`smoke` 三平台矩阵 / `release` / `todo-merge-audit` / `evals`），并链接 `CONTRIBUTING.md` 与 `RELEASE.md`。
  - [x] 修正 `## Get started` 末尾的 NOTE：删除「writes nothing」，改为与 `hooks/README.md` 一致的边界表述（注入派生状态与路由上下文；只写所选任务的 `sessions.md` 与 `repository-docs/index.md` 的路由元数据；不写核心任务文档、不批准）。
  - [x] 复核 `## Repository documents` 与 `## Todo intake` 两段的既有表述无需改动（已覆盖 merge driver、PR 模板、`repository-check` / `release-check`）。
  - [x] 保持章节顺序与既有文案不变；`claude plugin list` 示例行（`1.0.6`）逐字不动。
- Acceptance: 见 PRD 的 Acceptance Criteria 第 1、2、4 条；`git diff README.md` 中不出现「writes nothing」。
- Verification: 见 `## Verification / Review`。
- Rollback: 丢弃分支，或 `git checkout main -- README.md` 单文件回退。
- Status: done

### Step 2 — 中文版补齐到与英文版章节对齐

- Goal: `README.zh-CN.md` 与英文版 `##` 章节一一对应，顺序一致，实质内容不缺失。
- Dependencies: Step 1（章节与措辞以英文版为准）。
- Files: `README.zh-CN.md`。
- Implementation checklist:
  - [x] 在 `## 防止设计丢失的一条规则` 下补「具体恢复示例」（英文版 `### A concrete recovery story` 的 diff 块与说明）。
  - [x] 补 `## 设计原则` 之外的 `## 护栏，而非官僚流程`（英文版 `## Guardrails, not bureaucracy` 的表格）——或与既有 `## 设计原则` 合并为一个章节，两者内容不重复。
  - [x] 在 `## 与相邻工具的比较` 下补 `### 如何选择` 的英文版呈现方式（表格 `Choose the right layer`），保留中文版现有的列表式表述之内容，二者不并存重复。
  - [x] 补 `## 仓库文档` 缺失的四段：Todo merge driver 与 web-UI 限制、PR 模板门禁、`repository-check`、`release-check`。
  - [x] 修正「无侵入 Agent」段的 hook 描述：与 Step 1 的新口径一致（补 `sessions.md` 与 index 元数据写入、不写核心文档、不批准）。
  - [x] 补 `## 验证与 CI` 一节，与英文版逐条对应。
  - [x] 补 `## 仓库结构` 的 `hooks/`、`tools/`、`evals/`、宿主清单入口。
  - [x] `claude plugin list` 示例行与 `codebuddy plugin list` 的 `Version: 1.0.6` 逐字不动。
- Acceptance: 两份 README 的 `##` 章节集合一一对应；PRD 的 Acceptance Criteria 第 3、4 条成立。
- Verification: 见 `## Verification / Review`。
- Rollback: 同 Step 1。
- Status: done

### Step 3 — 验证并核对改动范围

- Goal: 证明文档改动没有破坏发布一致性检查，也没有越出范围。
- Dependencies: Step 1、Step 2。
- Files: 无（只读检查）。
- Implementation checklist:
  - [x] `bash hooks/release-check .` → `STATUS: pass`。
  - [x] `git diff --check` → clean。
  - [x] 相对链接核对：两份 README 中出现的仓库相对路径（`hooks/README.md`、`CONTRIBUTING.md`、`RELEASE.md`、`skills/taskflow/SKILL.md`、`LICENSE` 等）均存在。
  - [x] 范围核对：`git status --short -- hooks skills evals tools .claude-plugin .codex-plugin .codebuddy-plugin .github CHANGELOG.md` 为空。
  - [x] 章节对齐核对：两份 README 的 `## ` 标题列表逐项对应。
- Acceptance: 每条检查的实际输出记录进 `## Verification / Review`；未跑的项（如本机 `smoke-test`）按既有判定记录并说明理由。
- Verification: 本节即为验证。
- Rollback: 不适用。
- Status: done

## Checkpoints

- Step 1 完成后：`README.md` 只新增 `## Verification and CI` 一个章节标题，`claude plugin list` 示例行未变 —— 已确认（`git diff README.md | grep 1.0.6` 无输出）。
- Step 2 完成后：中文版未出现英文版没有的承诺性表述；合并 `## 设计原则` 与 `## 护栏` 时以英文版的表格为准 —— 已确认。
- 提交前：`git diff --stat` 只含两份 README、`TaskFlowDocs/todo.md` 与本任务目录 —— 已确认。

## Verification / Review

- 2026-09-18 Step 3: release-check pass; links resolve; scope empty; evals PASS (6)

- 2026-09-18 Step 2: 13 ## headings each side, item-by-item aligned; zh added 4 missing sections

- 2026-09-18 Step 1: release-check pass; diff --check clean; scope confined to two READMEs

- 2026-09-18 Step 1-3：两份 README 补全 `hooks/`/`tools/`/`evals/`/宿主清单入口、新增 `## Verification and CI`（英文）/`## 验证与 CI`（中文）、修正 SessionStart NOTE 的「writes nothing」、中文补齐 4 处缺失内容并合并重复章节。

`bash hooks/release-check .` → `STATUS: pass`；七个版本字面量仍为 `1.0.6`（三份 README/manifest 行未动），两个 pin 仍解析到 `ce3b03ca…`。

```text
- .claude-plugin/plugin.json: 1.0.6
- .codex-plugin/plugin.json: 1.0.6+codex.20260917
- .codebuddy-plugin/plugin.json: 1.0.6+codebuddy.20260917
- CHANGELOG.md (first section): 1.0.6
- README.md (plugin list sample): 1.0.6
- README.zh-CN.md (plugin list sample): 1.0.6
Marketplace pin (.claude-plugin/marketplace.json): v1.0.6 -> ce3b03cab31c75ed467f4ccec06ea5cfc6719357
Marketplace pin (.codebuddy-plugin/marketplace.json): v1.0.6 -> ce3b03cab31c75ed467f4ccec06ea5cfc6719357
```

- `git diff --check` → clean（exit 0）。
- 相对链接核对：两份 README 的相对链接各 6 个（`LICENSE`、`README.md`、`README.zh-CN.md`、`hooks/README.md`、`skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`），逐个 `-e` 判定全部存在；`CONTRIBUTING.md` / `RELEASE.md` 以行内代码路径而非链接出现，同样存在于仓库根。页内锚点 5 个（`#get-started`、`#the-problem`、`#where-taskflow-fits`、`#verification-and-ci`、`#验证与-ci`）逐个对应到同名标题。
- 范围核对：`git status --short` 只有 `README.md`、`README.zh-CN.md`、`TaskFlowDocs/todo.md`（任务状态）与未跟踪的任务目录；`git status --short -- hooks skills evals tools .claude-plugin .codex-plugin .codebuddy-plugin .github CHANGELOG.md RELEASE.md CONTRIBUTING.md` 为空。
- 章节对齐：两份 README 均为 13 个 `##` 标题，逐项对应（`The problem`↔`它解决什么问题` … `License`↔`许可证`），顺序一致；`## Verification and CI` ↔ `## 验证与 CI` 位置相同（`Get started` 之后、工具比较之前）。
- `python3 evals/runner.py` → `PASS (6 evals)`（本任务未触及 evals，作为环境可用性佐证）。
- 提交前重跑（此前预判的 `smoke-test` 失败未复现，按实际输出修正结论）：
  - `bash hooks/smoke-test` → `ALL SMOKE PASSED`（exit 0）。2026-09-17 记录的 `toolbin/bash: error while loading shared libraries` 本次未出现，说明那是当时宿主/PATH 的瞬时状态而非稳定限制；本任务从未改 hook，两次结论对本任务的范围判定无影响。按「变异验证一次一个」的纪律只跑了一遍，未串多轮。
  - `python3 /home/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/taskflow` → `Skill is valid!`（exit 0）。
  - `bash hooks/repository-check .` → `STATUS: needs-user-input`：`Base: ambiguous (no upstream tracking branch)`（本地分支尚未 `-u`）与 `Working tree: has changes`（尚未提交），两项都是提交/推送前修改 PR 的预期中间态，不是缺失的基础治理文档。
  - 运行后 `git status --short` 未变化 —— 冒烟套件在临时目录工作，未污染工作区。

## Change Log

- 2026-09-18 任务由用户「帮我更新一下 Readme」触发；三方确认后按仓库流程建分支、登记 Todo、升级任务。
- 2026-09-18 事实核对发现 README 的 SessionStart NOTE 与 `hooks/README.md` 及 README 自身 `## Repository documents` 段矛盾（「writes nothing」），已纳入范围（R3）。
- 2026-09-18 实施中发现中文版 `## 设计原则`（列表）与英文版 `## Guardrails, not bureaucracy`（表格）是同一内容的两种表述，按 Plan Step 2 的允许项合并为一个章节，保留英文版表格；中文版因此不出现英文版没有的章节。
- 2026-09-18 顺带修正中文版 `## 仓库文档` 里的 manifest 计数：写的是「两个插件 manifest」，实际 `hooks/release-check` 校验三个（含 CodeBuddy），英文版同段未提数量。
- 2026-09-18 用户授权提交并开 PR；按 `.github/pull_request_template.md` 逐项填写，字段映射记录在本 Plan 的 `## Verification / Review`。

## Pull request field mapping

按 `.github/pull_request_template.md` 的必填项：

- **Summary** — 两份 README 覆盖实际交付面（`hooks/`、`tools/`、`evals/`、宿主清单）、新增验证与 CI 一节、修正与 `hooks/README.md` 矛盾的 hook 描述，并把中文版补齐到与英文版章节对齐。
- **TaskFlow traceability** — Task: `TaskFlowDocs/2026-09-18-readme-refresh/`；Scope: 仅 `README.md`、`README.zh-CN.md`、`TaskFlowDocs/todo.md` 与本任务目录；Base branch: `main`；Target repository: `hkwuks/TaskFlow`（`origin`，凭证不落盘）。
- **Verification** — 四项全部勾选，命令与结果见上（`smoke`、`diff --check`、Skill 校验器、`Plan` 记录）。
- **Review boundaries** — 无密钥或不可读远端载荷；无无关任务或用户文件改动（范围核对为空）；remote/base 假设已写明（`origin` 是 `hkwuks/TaskFlow`，remote 名不构成角色证明，本任务只读 `origin` 未做任何 fetch/rebase/push）；已知限制：本机未验证文档在 GitHub 上的渲染，页内锚点仅按标题同名判定。

## Follow-ups

- 无。`assets/taskflow-workflow.svg` 未更新；若后续要重绘流程图，另开任务。

## Version History

- v1 — planning。
