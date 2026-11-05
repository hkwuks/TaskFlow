# Plan — 开发本仓库前先判定改动目标属于哪一类
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — 路由记录；本任务改编 `CONTRIBUTING.md`（repository-rule，phases 含 code/commit/pr）与 `hooks/smoke-test`。
- `CONTRIBUTING.md` — 本任务的落点，也是被修改的规则文档。
- `CODE_STYLE.md` — Markdown 约定（ATX 标题、一条规则一个 bullet、仓库相对路径）。
- `hooks/repo-rules` — 模板的语义来源：`show`/`create`/`check` 的分工与「只写一次」的约束。
- `hooks/smoke-test:7405` — 已有断言证明模板必须与实现细节脱钩。

## Related Tasks

- `TaskFlowDocs/achieved/2026-11-02-default-working-rules/` — 模板本身来自该任务，本任务只是给它补上归属说明。

## Skills / Tools Used

- [PRD] Unaided — 需求整理直接依据用户原话与仓库既有事实；considered: requirements elicitation
- [Plan] Unaided — 单步任务，无需拆解工具；considered: work breakdown
- [Test] Unaided — 复用仓库既有的 smoke 断言模式，不引入新测试框架；considered: testing strategy

## Preconditions

- 本 worktree 在 `docs/change-target-rule` 分支上。
- `repository-check` 在开工前为 pass。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-05 22:49 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 写入规则并 pin 住

- Goal: 在 `CONTRIBUTING.md` 增加「先判定改动目标」一节，并在 `hooks/smoke-test` 中加断言锁定它。
- Dependencies: 无
- Files:
  - `CONTRIBUTING.md`
  - `hooks/smoke-test`
- Implementation checklist:
  - [x] 在 `CONTRIBUTING.md` 的「Before you start」之后新增一节，含三落点表与判据句。
  - [x] 在 `hooks/smoke-test` 的 landing-claim 断言块之后新增一组 pin 断言。
  - [x] 跑 `bash hooks/smoke-test` 预检。
- Acceptance: PRD 的 Acceptance Criteria 全部满足。
- Verification: `bash hooks/smoke-test`；`git diff --check`；推分支后读 CI 三宿主矩阵。
- Rollback: `git checkout -- CONTRIBUTING.md hooks/smoke-test`。
- Status: done

## Checkpoints

- Step 1 完成后：本地 smoke 通过，再推分支。

## Verification / Review

**改了什么**

- `CONTRIBUTING.md`：在「Before you start」与「TaskFlow workflow」之间新增 `## Decide which rules you are changing`，含三落点表（落点 / 谁的规则 / 谁读 / 落错的代价）、判据句（「who is affected」而非「which directory」）、以及三者不可互换的双向说明，末尾要求把该行写进 TaskFlow Plan。
- `hooks/smoke-test`：新增 `== the repository is asked which of its three rule sets a change belongs to ==` 断言块，pin 标题、四条关键句、三个表格行。

**为什么放在这里而不是 `SKILL.md` 或 `hooks/templates/`**

这条规则约束的是「开发 TaskFlow 本仓库时改哪个文件」，对插件用户没有意义。写进 `skills/taskflow/SKILL.md` 会强迫每个安装者读一段与自己无关的目录布局；写进 `hooks/templates/` 等于把本仓库的私有流程当作建议发给别人。按规则自己的判据（谁受影响：只有 TaskFlow 贡献者），落点是本仓库根的 `CONTRIBUTING.md`——这条规则本身即是它主张的第一个应用。

**验证**

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| 新增断言块通过 | 抽取该块单独执行 | ok |
| 变异：删掉判据句 | 改 `Ask **who is affected**…` 为 `Ask the table.` | caught — `FAIL rule-target rule does not pin: Ask **who is affected**…` |
| 变异：删掉 plugin-behaviour 行 | 删除表格首行 | caught — `FAIL rule-target table is missing a row: \| The plugin's own behaviour \|` |
| 变异：删掉整节 | 删除 `## Decide which rules…` 到 `## TaskFlow workflow` | caught — `FAIL CONTRIBUTING does not ask which rule set a change belongs to` |
| 全量 smoke | `bash hooks/smoke-test` | `ALL SMOKE PASSED`，exit 0 |
| 空白检查 | `git diff --check` | 通过 |
| CI 三宿主矩阵 | PR #122，run [42049076206](https://github.com/hkwuks/TaskFlow/actions/runs/42049076206) | `smoke` macOS / Ubuntu / Windows、`changes`、`todo-merge-audit` 全部 pass；`release` 按预期 skipping |

本地 smoke 只是预检，CI 是判定。

**变更记录**

- 2026-11-05 — 用户指出未收到 CI 后台通知。改为直接查询 `gh pr checks 122`，确认六项全过；属工作方式修正，不改交付内容，记为 work revision。


## Change Log

- v1 — 初始计划。

## Follow-ups

- 无。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-11-05 用户原话**：「你做完这个任务，你给我的仓库增加一个规则：让后续开发的时候搞清楚是要改插件的功能，还是要改插件默认给的仓库规则模板，还是只是改我自己这个仓库的规则。」
  **为什么会有这条**：同一个仓库里存在三个**效力范围完全不同**的落点，而 Agent 容易把它们混成「都是改规则」：
  | 落点 | 生效范围 | 谁能看到 | 修改的代价 |
  | --- | --- | --- | --- |
  | `skills/taskflow/SKILL.md`、`skills/taskflow/references/`、`hooks/` | **插件自身行为**，所有安装者 | 每个用户 | 改变所有人的工作流 |
  | `hooks/templates/CONTRIBUTING.md`、`hooks/templates/CODE_STYLE.md` | **别人仓库的默认规则** | 仅当该仓库用户主动 `repo-rules create` | 建议性质，不自动生效 |
  | 本仓库的 `CONTRIBUTING.md`、`CODE_STYLE.md` | **仅 TaskFlow 开发本身** | 只影响本仓库的贡献者 | 不影响插件用户 |
  **实际教训（2026-11-05）**：Agent 在讨论「分层规则要写到哪」时，把「插件自身规则」和「发给用户的默认模板」混为一谈，向用户抛出了一个问错方向的选择题。用户纠正：*「不是应该写仓库，这跟仓库没有关系，你老是把关系搞混。我这个仓库就是开发这个插件的，这个插件要实现这个功能。」*
  **要做**：把这条判定写进插件的适用性门（`SKILL.md` 的 Applicability gate 附近）或 `CONTRIBUTING.md` 的显著位置，使每次开发本仓库时的第一个问题变成「这次改的是哪一类」。判据应当是**谁受影响**，而不是文件在哪个目录——`hooks/templates/` 容易被误读成「插件代码」，实际是「给别人仓库的建议」。
