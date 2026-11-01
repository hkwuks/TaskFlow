# Plan — 外部事实：先判断，再取证
> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/task:1383-1391` — `approve` 现有的 `Skills / Tools Used` 非空检查；新的校验插在它后面，形态照抄。
- `hooks/task:1497-1545` — `## Approval` 的写入是这段之后的第一处写；新校验必须在它之前。
- `hooks/task:813-826` — `promote` 写 PRD 骨架的 `printf` 块。
- `skills/taskflow/references/artifacts.md:25` — 「hook 按名匹配的小节」清单。
- `skills/taskflow/references/artifacts.md:54-68` — PRD outline。
- `hooks/smoke-test:1877-2070` — 既有 approve 夹具，新用例并入这里。

## Related Tasks

- 来源：`TaskFlowDocs/todo.md` 的 `TF-20261031-61b973`（由 `TF-20261027-e8c6dc` 重新界定）。
- 上游测量：`TF-20260919-90797c`（本任务不处理，见 PRD Out of Scope）。
- 形态参照：`achieved/2026-09-27-capability-pre-write-gate/`（`approve` 先校验后写入的写法）。

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — purpose: 把一条被重新界定的 todo 收敛成可验收的需求；outcome: succeeded; incorporated: 把「测量行为变化」改成「记录判断」这个可检查的形状，并把混淆写进 Background 而不是藏进 Risks。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 决定四处的先后与验证顺序；outcome: succeeded; incorporated: 先写校验再写骨架（骨架产生的字段要被校验接受），smoke 与文档放最后。
- [Test] `Unaided — no capability applied to this phase; considered: testing strategy` — 断言形态沿用 `hooks/smoke-test:1877` 既有夹具，未引入外部能力。

## Preconditions

- [x] 已读 `CONTRIBUTING.md`（分支/worktree）、`CODE_STYLE.md`（脚本风格）、`artifacts.md`（字段清单）。
- [x] 隔离：工作树 `.worktrees/external-facts`，分支 `feat/external-facts`，基线 `main` @ `b4b80a6`。
- [x] 已实测：94 个 achieved 任务的 `prd.md` 无一含 `External Facts`，字段名无冲突；`prd.md` 与 `plan.md` 成对存在（0 例外），所以不必先改 `approve` 的「prd.md 可选」行为。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-31 22:58 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — `approve` 校验 `## External Facts`

- Goal: 让 `approve` 在写 `## Approval` 之前读 `prd.md` 的 `## External Facts`，把 R2/R3 的四种坏形态各自拒绝并报出具体原因。
- Dependencies: 无。
- Files: `hooks/task`。
- Implementation checklist:
  - [x] 在 `cap_skills` 非空检查之后、`approved_version` 之前插入一段，读 `$prd`。
  - [x] 缺文件或小节缺失 → 拒绝，消息给出两种合法写法的其中一行供照抄（A5）。
  - [x] 小节存在但正文为空 → 拒绝，消息与 `Skills / Tools Used` 的「missing or empty」同形（A8）。
  - [x] `- Depends on external facts:` 既不是 `no` 也不是 `yes` → 拒绝并列出两个合法值。
  - [x] `no` 且缺 `- Why not:` → 拒绝（A1 的反面）。
  - [x] `yes` 且零条 `- Source:` → 拒绝（A2）。
  - [x] 任一 `- Source:` 的值不以 `http://` 或 `https://` 起头 → 拒绝并说出「不是绝对 http(s) URL」（A3/A4）。
  - [x] 每条 `- Source:` 之后必须有 `- What it settled:` → 缺则拒绝。
  - [x] 所有失败都发生在任何 `## Approval` 写入之前，且 `fail` 前不 `mv` 任何临时文件。
- Acceptance: PRD 的 A1–A5、A8。
- Verification: 手工构造六种坏 `prd.md` 各跑一次，确认消息与退出码；再用真实仓库的一个任务跑通一次正向。
- Rollback: 单段代码，`git revert` 即恢复。
- Status: done

### Step 2 — `promote` 的 PRD 骨架与 `artifacts.md`

- Goal: 新任务的 `prd.md` 一出生就带着这个小节，且字段名与 Step 1 的匹配逐字一致。
- Dependencies: Step 1（骨架的默认文本必须能被校验接受或至少给出可照抄的提示）。
- Files: `hooks/task`、`skills/taskflow/references/artifacts.md`。
- Implementation checklist:
  - [x] `hooks/task` 的 PRD 骨架加 `## External Facts`，正文放一行 `- Depends on external facts: ` 与 `- Why not: `（空值，等作者填）。
  - [x] 骨架的默认值必须**不能**直接通过 Step 1 的校验 —— 空值就是「没回答」，与空的 `Skills / Tools Used` 同等对待。
  - [x] `artifacts.md` 的 PRD outline 加同一小节，位置与骨架一致。
  - [x] `artifacts.md:25` 的「hook 按名匹配的小节」清单里加 `## External Facts`，并补一条说明它的两个字段名由 `approve` 逐字读。
- Acceptance: PRD 的 A7；`promote` 生成的新 `prd.md` 在不填该小节时 `approve` 拒绝。
- Verification: 在夹具里 `promote` 一个新任务，读回 `prd.md` 确认小节存在；直接 `approve` 确认被拒且消息指向该小节。
- Rollback: 两处 `printf` 与一行清单，`git revert`。
- Status: done

### Step 3 — smoke 断言与 SKILL.md

- Goal: 让 Step 1 的每条拒绝在 CI 里被执行，且每条都有一个能被变异打红的具名断言；SKILL.md 说明这个字段是什么。
- Dependencies: Step 1、Step 2。
- Files: `hooks/smoke-test`、`skills/taskflow/SKILL.md`。
- Implementation checklist:
  - [x] 在既有 approve 夹具（`hooks/smoke-test:1877`）上，给 `ap_task/prd.md` 写入合法的 `## External Facts`，让原有正向用例继续通过。
  - [x] 新增 case：小节缺失 / 正文为空 / 值非 no|yes / `no` 缺 `Why not` / `yes` 缺 `Source` / `Source` 非 URL / 缺 `What it settled`，各一条具名断言。
  - [x] 每条断言都检查**消息片段**，不只检查退出码 —— 否则八条拒绝退化成一条。
  - [x] 变异验证：逐条破坏 Step 1 的分支，确认**对应**的断言变红，然后逐字节恢复（`diff -q`）。
  - [x] `SKILL.md:204` 的「`prd.md` must state」列表加一条；`SKILL.md:54` 的 `inspect` 八项**不动**（PRD Out of Scope）。
- Acceptance: PRD 的 A6；变异 7 次各自红在对应用例，恢复后 `ALL SMOKE PASSED`。
- Verification: `bash hooks/smoke-test`；七次变异的结果写进 `## Verification / Review`。
- Rollback: 删除新增 case 与那一行 SKILL.md。
- Status: done

## Checkpoints

- Step 1 后：`bash -n hooks/task` 通过；真实任务的 `prd.md` 填好两种形态各一次都能 `approve`。
- Step 2 后：夹具里 `promote` 出的新任务，不填该小节时 `approve` 被拒。
- Step 3 后：`bash hooks/smoke-test` → `ALL SMOKE PASSED`；七次变异各自红在对应用例。

## Verification / Review

### 实测（2026-11-01）

| 检查 | 结果 |
|---|---|
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` |
| `bash -n hooks/task hooks/smoke-test` | 通过 |
| `hooks/task` 变异后恢复 | 六次变异后逐字节回到 pristine（`diff -q`） |

### 六次变异（每次红在自己的具名断言上）

| 变异 | smoke 输出 |
|---|---|
| `no` 不检查 `- Why not:` | `FAIL external facts message for no without a reason` |
| `yes` 允许零条 `- Source:` | `FAIL external facts message for yes without a source` |
| `- Source:` 不校验是否为绝对 http(s) URL | `FAIL external facts message for source is not a URL` |
| 不要求每条 `Source` 配 `- What it settled:` | `FAIL external facts message for source settled nothing` |
| 接受 `no` / `yes` 之外的值 | `FAIL external facts message for not no-or-yes` |
| 空答案（小节缺失或空）直接放行 | `FAIL external facts message for missing section` |

### 实现过程中被自己抓到的两个缺陷

**一、一行死代码。** 第一版在 `## External Facts` 正文为空时先 `fail`，再进入 `case`。但空正文意味着 `ext_answer` 也是空，`case` 的 `""` 分支会打出**同一条消息** —— 那行 `fail` 永远不会是唯一的拒绝原因，删掉它不影响任何断言。删掉后 Step 3 的「missing section」与「empty section」两条用例仍然各自通过，证明它们走的是同一个 `""` 分支。

这是变异验证的价值所在：那行看起来像「更早、更明确地拒绝」，实际上是一条 `grep -v` 就能删掉、而测试不会有任何反应的代码。

**二、`prd.md` 自己成了新规则的第一个用户。** 本任务的 PRD 在 `approve` 之后才补上 `## External Facts`，因为批准时规则还不存在。补的时候必须真的回答，而不是写一句占位 —— 答案 `no` 的理由是「本任务的每条验收标准都由仓库内既有实现判定，无一处依赖外部规范」。

## Change Log

- 2026-11-01 — Step 3 完成：smoke 新增 9 条 `## External Facts` 断言；SKILL.md 与 artifacts.md 同步；本任务 PRD 补上该小节。

## Follow-ups

- **`no` 分支的比例与理由雷同度值得回看。** 落地一段时间后统计 `Depends on external facts: no` 在 `achieved/` 里的占比，若接近 100% 且 `Why not` 措辞雷同，说明字段退化成了橡皮图章（PRD Risks 第 1 条）。
- **`TF-20260919-90797c` 的对照测量仍然悬空**，本任务按用户 2026-10-31 裁定不合并。

## Version History

- v1 — planning.
