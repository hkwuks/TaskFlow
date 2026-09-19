# Plan — Conflict side review and the zh-CN manifest count
> Task version: v1
> Status: completed

No spec required — 一行事实修正加一条流程规则，无跨层契约。

## Reference Pointers

- `README.zh-CN.md:64` / `README.md:97` —— 同一句的中英两版，前者需与后者一致。
- `hooks/release-check` —— 校验范围的权威：`.claude-plugin/`、`.codex-plugin/`、`.codebuddy-plugin/` 三个 manifest 加 `CHANGELOG.md` 与两份 README 的 `claude plugin list` 示例行。
- `skills/taskflow/SKILL.md`（Phase 5 的 merge 段、Phase 6 的验证清单）—— R2/R3 的落点。
- `hooks/todo-check` —— 已确认覆盖不到本类失败，只读确认过其比较范围。
- `TaskFlowDocs/achieved/2026-09-17-atomic-release-push/plan.md` —— 本仓库既有的"合并后复核"讨论背景。

## Related Tasks

- Depends on: 无。
- Related: `TaskFlowDocs/achieved/2026-09-18-readme-refresh/`（引入「三个 manifest」那一版修正被退回）。
- 无关活跃任务：`TF-20260918-172455`（archive 空行）、`TF-20260918-88e04c`（归档流程开销）。

## Skills / Tools Used

- 未调用额外 Skill。成因复核用仓库内命令完成（三方合并重放、`git merge-file`、逐 rev 取文件比对），未使用外部资料或 LLM 判定工具。
- 冲突成因是**证据判定**（重放可复现），不是判断性结论，因此不依赖任何外部能力。

## Preconditions

- [x] 适用仓库文档已读：`README.md`、`README.zh-CN.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`、`skills/taskflow/SKILL.md`、`hooks/README.md`。
- [x] `git worktree add .worktrees/conflict-side-review -b fix/conflict-side-review main` —— 隔离先于文档。
- [x] 本任务在 `TaskFlowDocs/todo.md` 登记为 `TF-20260918-ad8348` 并升级为任务。
- [x] 成因已实测复现（`git merge-file` exit 1 + `46131a1` 的解决结果取分支侧）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-18 21:43 +08:00
- Approved version: v1
- Approved scope: PRD / Plan
- Note: 用户在 2026-09-18 批准 v1，含定稿后的 R2/R4/R6（冲突时先询问用户）。

## Steps

### Step 1 — 修正中文版 manifest 计数

- Goal: `README.zh-CN.md:64` 与英文版同句、与 `hooks/release-check` 的实际校验范围一致。
- Dependencies: 无。
- Files: `README.zh-CN.md`。
- Implementation checklist:
  - [x] `比对两个插件 manifest` → `比对三个插件 manifest`。
  - [x] 确认同句其余部分（`并列出该 checkout 里未提交的任务产物` 等 PR #38 引入的内容）保持不动。
  - [x] 确认两份 README 的 `claude plugin list` 示例行（`1.0.6`）逐字未动。
- Acceptance: 与 `README.md:97` 的 `all three plugin manifests` 一致；`hooks/release-check` 仍 pass。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout main -- README.zh-CN.md`。
- Status: done

### Step 2 — 给 Skill 补冲突先询问用户的规则

- Goal: Agent 执行的合并遇到冲突时停下来问用户；用户的决定记入任务 `plan.md`。规则落在 Phase 5 而非只在 Phase 6 的清单里。
- Dependencies: 无（与 Step 1 独立）。
- Files: `skills/taskflow/SKILL.md`。
- Implementation checklist:
  - [x] Phase 5 的 merge/Todo 驱动段旁边补一条：**Agent 执行的合并（`git merge` / `git rebase`）发生冲突时，停下来把两侧摆给用户、由用户决定取舍**，不得自行选定一侧；用户的决定记入当前任务 `plan.md` 后继续。只发生自动合并时不要求任何动作。
  - [x] 明确写出**托管平台网页端 PR 的冲突不在本规则范围内**（那条路径由用户在界面上解决）（R6）。
  - [x] Phase 6 的验证清单加一项：冲突已按用户裁定解决且记录在 `plan.md`。
  - [x] 措辞复用 `Repository document environment` 段已有的 "stop and ask the user; do not silently choose one" 句式（R5），不另造说法。
  - [x] 不禁止整块取某一侧——用户可以直接裁定「这一侧全取」（R4）。
  - [x] 不改 Phase 5 现有的 worktree/隔离语义，不改 Todo 驱动那句。
- Acceptance: 规则可判定（"是否发生过冲突"可观测、"已询问"与"记录在 plan.md"可检查）；未发生冲突时无额外要求；PR 冲突的例外写明。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout main -- skills/taskflow/SKILL.md`。
- Status: done

### Step 3 — 验证与范围核对

- Goal: 改动不越界，且 release 一致性检查未被破坏。
- Dependencies: Step 1、Step 2。
- Files: 无（只读检查）。
- Implementation checklist:
  - [x] `bash hooks/release-check .` → `STATUS: pass`。
  - [x] `bash hooks/smoke-test` → `ALL SMOKE PASSED`。
  - [x] `git diff --check` → clean。
  - [x] 范围核对：`git status --short -- hooks README.md hooks/README.md` 为空。
  - [x] 中英一致性核对：两份 README 描述 `release-check` 的句子在"三个 manifest"上一致。
- Acceptance: 每条的实际输出记入 `## Verification / Review`。
- Verification: 本节即为验证。
- Rollback: 不适用。
- Status: done

## Checkpoints

- Step 1 后：`grep -c "三个插件 manifest" README.zh-CN.md` 为 1，且 `README.md` 未被触碰。
- Step 2 后：`skills/taskflow/SKILL.md` 的 Phase 编号与既有 Phase 5/6 标题不变；`grep -c "Skills / Tools Used (Optional)"` 为 0。

## Verification / Review

Step 1、Step 2 实施于 2026-09-18 21:43–21:50 +08:00，worktree `.worktrees/conflict-side-review`，分支 `fix/conflict-side-review`，base `main` = `7168e1b`。

| 检查 | 命令 | 实际输出 |
| --- | --- | --- |
| 中文计数 | `grep -c "三个插件 manifest" README.zh-CN.md` | `1` |
| 英文版未动 | `git diff --stat README.md` | 空 |
| Phase 编号 | `grep -n "^### [0-9]\." skills/taskflow/SKILL.md` | `1.`–`7.` 七项齐全，标题未变 |
| 无残留 Optional | `grep -c "Skills / Tools Used (Optional)" skills/taskflow/SKILL.md` | `0` |
| release 一致性 | `bash hooks/release-check .` | `STATUS: pass`（两份 README 示例均 `1.0.6`，两个 marketplace pin 均指向 `ce3b03cab31c75ed467f4ccec06ea5cfc6719357`） |
| smoke | `bash hooks/smoke-test` | `ALL SMOKE PASSED`，exit 0（单次运行，未串多轮） |
| 空白/冲突标记 | `git diff --check` | clean |
| 范围 | `git status --short -- hooks README.md hooks/README.md` | 空 |

改动范围：`README.zh-CN.md`、`skills/taskflow/SKILL.md`、本任务目录、`TaskFlowDocs/todo.md`（条目状态跟随任务推进）。无越界文件。

### 实施结果与 Plan 的偏差

- 计划里写"复用 `Repository document environment` 段的 `stop and ask the user; do not silently choose one` 句式"——实际采用了同一句式但按 Git 合并的语境重写为 `stop and put both sides in front of the user, who decides what to keep; do not silently choose one`。加 `both sides in front of the user` 是因为原文那句讲的是"两个规则冲突"，读者不会自动想到"把冲突两侧的 diff 摆出来"这个动作；只写 `stop and ask` 仍有"问一句就自己选"的余地。这是一处**措辞加强**，未改变规则强度，按工作修订记于 Change Log。
- Phase 6 清单从 7 项变 8 项，因此新增项插在第 2 位（紧跟"改动范围"），后续项序号顺延；无外部文档引用该清单的项数（已 `grep` 确认）。

## Change Log

- 2026-09-18 由 `TF-20260918-ad8348` 提升；成因复核推翻了先前「静默 auto-merge」的说法，确认为真冲突、解决时取分支侧。
- 2026-09-18 范围在任务中收窄：不再考虑泛化 `hooks/todo-check`（已确认纯 hook 判定不了"取错侧"），只留流程规则。
- 2026-09-18 用户定稿规则强度：**发生冲突时应当询问用户**，而非仅要求记录取舍。据此重写 R2（先问、再留痕）、R4（允许用户裁定整块取一侧）并新增 R6（托管平台网页端 PR 的冲突不在范围内）与对应的风险项（合并会中断等人）。
- 2026-09-18 工作修订：Step 2 落地时规则措辞加 `put both sides in front of the user`，并由此把 Phase 6 清单从 7 项扩到 8 项。措辞与清单序号属实现层，规则强度未变，保持 v1。

## Follow-ups

- 若要自动兜住这一类，方向是"合并后对两侧都改过的行做三方比较"，需单独任务。

## Version History

- v1 — planning。
