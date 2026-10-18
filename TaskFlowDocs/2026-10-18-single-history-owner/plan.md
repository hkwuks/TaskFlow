# Plan — 让 Task 版本史只有一个归属文档

> Task version: v1
> Status: checking

No spec required — small, self-contained task.

## Spec Pointers

无。

## Reference Pointers

- `TaskFlowDocs/achieved/2026-09-23-version-approval-shape/` — `hooks/version` 与 `promote` 必须写出同一形状的 Approval 块；本次不触碰该约束。
- `TaskFlowDocs/achieved/2026-10-17-stage-capability-pairing/` — 同批「文档结构 vs 冗余」的清理，可参照其验证记录写法。

## Related Tasks

- Parent: None
- Children: None
- Depends on: None
- Blocks: None
- Related: `TaskFlowDocs/achieved/2026-10-17-stage-capability-pairing/`

## Skills / Tools Used

- [PRD] `general-purpose` — purpose: 逆向核对「谁读 `## Version History` / `## Change Log`、`> Task version:` 的读者是哪一份文档、删掉 PRD 那节会不会打红任何断言」；outcome: `succeeded`；incorporated: 已折进 PRD 的 Confirmed Facts —— 写入方四处、读取方零处；`## Change Log` 的唯一匹配点在 `hooks/reopen:137`；`> Task version:` 的读者全部指向 `plan.md`。
- [PRD] `general-purpose`（独立复核，同 worktree 只读） — purpose: 用原始命令输出复核上述三条，并专门反查 `hooks/version` 是否要求 PRD 带 `> Task version:`；outcome: `succeeded`；incorporated: 三条全部 CONFIRMED；`hooks/version:16,31-35,134-137` **确实**要求每个存在的核心文档带同一版本行——所以删的是节，`hooks/task:761` 那行版本字面量必须原样保留。
- [Plan] `general-purpose` — purpose: 复核 Step 1 拆解，重点是「我漏了什么」；outcome: `succeeded`；incorporated: 见下，五条已改入本 Plan。

### 复核结论如何改入本 Plan

- **删哪几行**：`hooks/task:778-780`（`## Version History`、空行、`- v1 — planning.`），并连 `:777` 的空行一起删，否则骨架以 `## Open Questions\n\n\n` 结尾。该块是单引号字面量，内部无 `$`/反引号/`$()`，纯删除在 bash 3.2 下解析通过（已用 `docker run bash:3.2 bash -n` 验过三种变体）。
- **断言该落哪**：不能照抄 `hooks/smoke-test:2021` 的形态——那读的是 hook 源码，看不见经 `$goal` 或运行时拼出的骨架。落在 `== task lifecycle dispatcher ==` 段（`:966`）里，复用该段已有的 `$active`（`:976`）。仓库里没有 promote 夹具助手，不要新建。
- **`SKILL.md` 改哪行**：`:208` 那一项直接**删掉**，不要改写成「current Task version」——因为 `:38` 已经是 PRD 的 artifact contract（`goal, requirements, scope, and observable acceptance criteria`），本就不含版本史。改写会造出第二份口径。
- **不要碰**：`references/versioning-and-recovery.md:11` 与 `artifacts.md:29` 都已正确（前者说的是 `> Task version:` 字段，不是历史节；后者那句在 `hooks/smoke-test:1550` 的 clause-pin 里，改它会打红）。
- **两项必须补的检查**：`CONTRIBUTING.md:78-81` 的 `quick_validate.py skills/taskflow`（本机在 `/home/hk/.claude/plugins/cache/claude-plugins-official/skill-creator/ea10b213686c/skills/skill-creator/scripts/quick_validate.py`）与 `git diff --check`；再加 PR 模板 `:16` 的「Relevant Skill/plugin validation」框。
- **本次的真实收益**（写进 Acceptance 口径）：没有任何东西在 bump 时往这节追加内容，所以**留下的那份是「结构性过期」**——v2 的 PRD 会一直写着 `- v1 — planning.`。删掉它消除的是这一整类过期，而不只是少一份重复。

## Preconditions

- [x] 适用仓库文档与个人规则已检查；`TaskFlowDocs/repository-docs/index.md` 已读，`CONTRIBUTING.md`、`CODE_STYLE.md`、`.github/pull_request_template.md` 已读，无冲突。
- [x] 远端/base 已记录：`origin` = `hkwuks/TaskFlow`，base = `main`（`da2afa1`），本地分支 `docs/single-history-owner` 从该提交切出，worktree `.worktrees/single-history-owner`。
- [x] PR 模板路径与必填字段映射已读（`.github/pull_request_template.md`）。
- [x] 本任务不需要新建治理文档。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-18 21:46 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 把归属收进 plan.md，并加一条不回归断言

- Goal: `## Version History` 只由 `plan.md` 持有：去掉 PRD 骨架里的这一节，同步 outline 与规则句，并用 smoke 把「PRD 不得再有该节」钉住。
- Dependencies: 无。
- Files:
  - `hooks/task`（`promote` 的 PRD 骨架字面量，`:777-780` 四行）
  - `hooks/smoke-test`（在 `== task lifecycle dispatcher ==` 段、`:978` 之后新增断言）
  - `skills/taskflow/SKILL.md`（`:208` 那一项，直接删除）
  - `skills/taskflow/references/artifacts.md`（`:64` PRD outline 一行）
  - `TaskFlowDocs/todo.md` 与 `TaskFlowDocs/2026-10-18-single-history-owner/`（本任务自身的记录，按 `CONTRIBUTING.md` 随任务一起进 PR）
- Implementation checklist:
  - [x] 从 `hooks/task` 的 PRD 骨架删掉 `:777-780`（`## Version History`、其前后空行、`- v1 — planning.`），保留 `:761` 的 `> Task version: v1`。
  - [x] 从 `artifacts.md:64` 删掉 PRD outline 里的该行；Plan outline 不动；**未碰** `:29`。
  - [x] `SKILL.md:208` 整项删除，未回写替代句（`:38` 已是 artifact contract）。
  - [x] 在 `hooks/smoke-test` 的 `== task lifecycle dispatcher ==` 段、既有 `:978` 之后新增三条断言，读 **promote 出来的产物**（`$active`），不读 hook 源码。
  - [x] **未碰** `references/versioning-and-recovery.md`（`:11` 已正确）。
  - [x] 复核了两份 README 的「shared … version boundaries」措辞：`README.md:120` 写的是 `Project-local Markdown as task facts`，`README.zh-CN.md:31` 的对应行写的是「共享同一份任务事实和版本边界」。**判定：不动。** 它讲的是「任务事实与版本边界由仓库承载、不散落在聊天里」，与「PRD 是否自带历史节」无关；改写只会引入一处无谓的双语改动。
- Acceptance: 干净 fixture 上 `promote` 产出的 `prd.md` 无该节、`plan.md` 有；`prd.md` 仍带版本行；全仓库对 `## Version History` 的引用只剩 Plan 侧与 `skills/` 的 Plan outline。
- Verification: 见 `## Verification / Review`。
- Rollback: `git revert` 本任务提交；无数据迁移、无状态文件、无 hook 行为变更。
- Status: done

## Checkpoints

- [x] 改完 `hooks/task` 后先只跑 promote 相关那几节，再跑整套 smoke。

## Verification / Review

- 2026-10-18 Step 1: smoke 72 ok / ALL SMOKE PASSED; 3 mutations red on 3 different assertions; quick_validate OK

### 通过项

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| smoke 全套 | `bash hooks/smoke-test < /dev/null` | `ALL SMOKE PASSED`，72 个 `ok`，exit 0 |
| 空白/尾随 | `git diff --check` | clean |
| shell 解析 | `bash -n hooks/task hooks/smoke-test` | 两者 OK |
| bash 3.2 解析 | `docker run --rm -i bash:3.2 bash -n < <file>` | 两者 `3.2 OK` |
| Skill 包校验 | `python3 …/quick_validate.py skills/taskflow` | `Skill is valid!` |
| 仓库检查 | `bash hooks/repository-check .` | `Orphan task directories: none`；`needs-user-input` 仅因本任务目录未提交（预期） |

### 骨架实测

`promote` 产出的 `prd.md` 末节现在停在 `## Open Questions`，文件以 `## Open Questions\n` 结束（无多余空行）；`plan.md` 仍以 `## Version History` + `- v1 — planning.` 结尾。`> Task version: v1` 两处都在。

### 变异验证（每棵树副本，真 worktree 未被改动）

| 变异 | 变红的断言 |
| --- | --- |
| 把 PRD 的 `## Version History` 节加回骨架 | `FAIL promotion wrote a PRD Version History section` |
| 删掉 Plan 骨架里的该节 | `FAIL promotion did not write the Plan Version History section` |
| 删掉 PRD 骨架的 `> Task version: v1` 行 | `FAIL promotion dropped the PRD Task version` |

三条各红在不同的断言上，说明三个约束各自承重。

### 未执行 / 局限

- 未跑 `hooks/smoke-test-windows.ps1`（非 Windows 主机）。该套件不触及 promote 出的 PRD 形状——它只在 capability-gate 夹具里写一个极简 `prd.md`，lifecycle 段只读 `plan.md`——所以本次改动不在它的覆盖面内。
- 未跑评测套件（`evals/runner.py`）。其夹具 PRD 只有三行且不含该节，`evals/cases/taskflow.json:47` 只断言 `contains: "Task version"`。
- `old/vN/` 交互已核：`hooks/version` 只读写 `> Task version:` / `> Status:` / `## Approval`，从不解析标题集合，也不比较新旧 PRD 形状，所以下一次 bump 不会因本次改动看到任何新东西。

## Change Log

- 2026-10-18 v1 planning：立项。归档实测口径订正为 `prd` 70 / `plan` 73 / 两份都有 70（75 个目录，`old/` 已排除）。
- 2026-10-18 v1 work revision：并入两条复核结论——删 `:777-780` 四行而非三行、断言落 `lifecycle` 段且读产物不读源码、`SKILL.md:208` 整项删、不碰 `versioning-and-recovery.md`、补两项本地检查、新增「结构性过期」收益口径。

## Follow-ups

- 可选：让 `hooks/version` 在 bump 时自动往 Plan 的该节插一行（用户 2026-10-18 明确本次不做）。

## Version History

- v1 — planning：把 `## Version History` 的归属收进 `plan.md`，PRD 只留 `> Task version:`。
