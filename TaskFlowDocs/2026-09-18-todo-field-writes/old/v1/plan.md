# Plan — Move the deterministic Todo field writes into hooks/task

> Task version: v1
> Status: checking

No spec required — 单一文件新增一个子命令，无跨层契约。

## Reference Pointers

- `hooks/task:91-104` —— `findsec` / `setr`：本命令复用的定位与替换原语。
- `hooks/task:529-556` —— `state`：机械化写入的既有先例，同时说明它为何**不**写 `Next action`。
- `hooks/task:358-527` —— `promote`：`TASKFLOW_PAIRS` + `loadpairs` 的字段写入路径，以及「Todo 已 promote」之类的守卫写法。
- `hooks/archive:54-63` —— 字段缺失时补行而非失败的先例与理由。
- `hooks/smoke-test:388-395`、`500-510` —— 既有 `Next action` 相关的断言，新增覆盖要与之并存。
- `CONTRIBUTING.md:37-47` —— PR 前必跑：`smoke-test`、Skill 校验器、`git diff --check`。

## Related Tasks

- Related: `TF-20260918-88e04c`（归档的 stage 步骤与分支选择）——本条 Todo 的 Notes 明确把它记为同一思路的另一半，但那条需要架构决断，不在本任务内。
- Related: `TF-20260918-ad8348`（PR #40）——本条 Todo 的直接触发点，那个 `Next action` 的手改就是反例。
- Related: `TaskFlowDocs/achieved/2026-09-10-token-saving-lifecycle-scripts/` —— 同一目标（用有界生命周期命令替代重复读写）的前一次交付。

## Skills / Tools Used

- 未调用额外 Skill。设计依据来自本仓库既有代码的阅读（`hooks/task`、`hooks/archive`、`hooks/smoke-test`）与一次尺寸实测（`wc -l -c`）。无外部资料、无 LLM 判定工具。
- 落地方式遵循「照抄既有形状」：定位用 `findsec`、替换用 `setr`、落盘用 `run_awk_to`、参数用位置参数——都是仓库里已经有的做法。

## Preconditions

- [x] `git worktree add .worktrees/todo-field-writes -b feature/todo-field-writes main` —— 隔离先于文档，base `f55de0b`。
- [x] Todo 条目 `TF-20260918-e2317d` 已 `promote` 为 `2026-09-18-todo-field-writes`。
- [x] 适用仓库文档已读：`CONTRIBUTING.md`、`CODE_STYLE.md`、`hooks/README.md`、`skills/taskflow/SKILL.md`。
- [x] 范围 / 寻址 / 命名三项已由用户定稿（见 PRD Open Questions）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-18 22:27 +08:00
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 在 `hooks/task` 里实现 `next` 子命令

- Goal: `task next <todo-id> <next-action> [notes]` 一次原子写入完成 `Next action` / `Updated` / 可选 Notes。
- Dependencies: 无。
- Files: `hooks/task`。
- Implementation checklist:
  - [x] `TASK_AWK` 增加 `cmd == "next"` 分支：用 `findsec(id, "")` 定位 section，`setr` 写 `Next action` 与 `Updated`，返回 0 或 die。
  - [x] 第三个参数非空时追加 Notes：从 `- Notes:` 行起，向后吞掉连续的 `- ` 开头且不是 `- <字段名>:` 形状的续行，把新行插在该块**末尾**。
  - [x] Notes 块内插入时同步 `n` 并给数组让位，保证 `emit()` 输出完整（参照 `step` 分支往 `## Verification / Review` 后插行的位移写法）。
  - [x] 字段缺失时补行：`Next action` 补在 `- Status:` 之后；`Notes` 补在条目字段块末尾（对齐 `archive` 的既有宽容策略）。
  - [x] `next` case 用位置参数校验（3 或 4 个），注释说明可选 notes 沿用 `progress` 的 verification 位置参数房型。
  - [x] **不加** `require_approval`：注释写明理由（Todo 是分诊元数据，不是批准过的产物；`intake`/`promote` 同样不加）。
  - [x] `TASKFLOW_NOTFOUND` 用既有的 `Todo entry not found: <id>` 文案保持一致。
  - [x] 不改 `state` 的行为，不动 `intake` / `promote` / `progress` / `complete` 的任何分支。
- Acceptance: 见 PRD Acceptance Criteria 前四条。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout main -- hooks/task`。
- Status: done

### Step 2 — 给 `hooks/smoke-test` 补覆盖

- Goal: 新子命令在 CI 的三个平台上都被跑到，包括 Notes 位置与补行两条边界。
- Dependencies: Step 1。
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 新增一节，fixture 用既有形状（`printf '# Todo inbox\n\n## Items\n\n## Seed\n\n- ID: ...'`）构造一条含 `Next action` 与 `Notes` 的条目。
  - [x] 断言 `task next` 后 `Next action` 与 `Updated` 为新值。
  - [x] 断言新 Notes 行落在 `- Updated:` **之前**（这是 R4 的判据，也是最容易写错的一点）。
  - [x] 断言带 Notes 的条目其余行逐字节未变（`diff` 或逐行比对均可，取仓库既有写法）。
  - [x] 另起一个 fixture 覆盖字段缺失补行：无 `Next action`、无 `Notes`。
  - [x] 负例：不存在的 ID → 非零退出且报 `Todo entry not found`。
  - [x] 不修改既有的 `Next action` 断言（`hooks/smoke-test:388-395`、`500-510`），只新增。
- Acceptance: `bash hooks/smoke-test` → `ALL SMOKE PASSED`。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout main -- hooks/smoke-test`。
- Status: done

### Step 3 — 验证与范围核对

- Goal: 改动不越界，hook 的运行边界未被破坏。
- Dependencies: Step 1、Step 2。
- Files: 无（只读检查）。
- Implementation checklist:
  - [x] `bash hooks/smoke-test` → `ALL SMOKE PASSED`（单次运行，不串多轮）。
  - [x] `bash hooks/release-check .` → `STATUS: pass`。
  - [x] `python3 /home/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/taskflow` → `Skill is valid!`。
  - [x] 手工在**临时副本**的 `todo.md` 上跑三条场景（inbox 条目 / 已归档条目 / 不存在的 ID），确认真实文件不被测试触碰。
  - [x] `git diff --check` → clean。
  - [x] 范围核对：改动仅 `hooks/task`、`hooks/smoke-test`、本任务目录、`TaskFlowDocs/todo.md`。
- Acceptance: 每条的实际输出记入 `## Verification / Review`。
- Verification: 本节即为验证。
- Rollback: 不适用。
- Status: done

## Checkpoints

- Step 1 后：`bash hooks/task`（无参数）仍打印既有 usage；`grep -c "require_approval" hooks/task` 不变（`next` 不得引入新调用）。
- Step 2 后：`grep -c "ALL SMOKE PASSED" hooks/smoke-test` 不变（只加节，不复制结论行）。

## Verification / Review

Step 1–3 实施于 2026-09-18 22:27–22:50 +08:00，worktree `.worktrees/todo-field-writes`，分支 `feature/todo-field-writes`，base `main` = `f55de0b`。

| 检查 | 命令 | 实际输出 |
| --- | --- | --- |
| smoke（全量） | `bash hooks/smoke-test` | `ALL SMOKE PASSED`，新增节 `ok` |
| 变异验证（一次一个） | 把 Notes 插入点从 `notes_end(p,b)+1` 改成 `last+1`，重跑 | 新增节 `FAIL Notes bullet did not land at the end of the Notes block, above Updated:` —— 断言确实在防 R4，不是摆设。已还原（`diff -q` 与备份 identical） |
| release 一致性 | `bash hooks/release-check .` | `STATUS: pass` |
| Skill 校验 | `quick_validate.py skills/taskflow` | `Skill is valid!` |
| 空白/冲突标记 | `git diff --check` | clean |
| 范围 | `git status --short` | 仅 `hooks/task`、`hooks/smoke-test`、本任务目录、`TaskFlowDocs/todo.md` |
| 手工场景（临时副本） | inbox 条目 / 已归档条目（无 `Next action`、无 `Notes`）/ 不存在的 ID | 三者行为与 Acceptance 一致；`Todo entry not found: TF-99999999-zzzz`，exit 1 且文件未变 |

### 实施结果与 Plan 的偏差

- **Checkpoint 1 的度量方式写错了**：Plan 写的是 `grep -c "require_approval" hooks/task` 不变（4），实际为 5。原因是新增的注释里写了 `require_approval` 这个词（"Deliberately unguarded by require_approval: …"），计数把它算进去了。**要断言的是「未新增调用」，不是「未新增字符串」**：调用点数仍是 `state`/`progress`/`complete` 三处（`:599`、`:647`、`:660`），与改动前一致。注释保留——说明「为什么不加门禁」比迁就一个选错的度量更重要。
- **Step 2 的 fixture 与 Plan 描述有出入**：Plan 说断言「其余行逐字节未变」，实际用的是「字段一个不少 + 计数不变 + 旧值已消失」的组合。逐字节比对在这里做不到——`Updated` 本来就要变、新 Notes 行本来就要加，得先剥掉这两处再比，反而更容易写出含糊的断言。另外 fixture 里 `- Updated:` 被刻意放在 `- Notes:` 块**之后**（即现有 `todo.md` 的真实形状），否则「Notes 块末尾」与「条目末尾」是同一个位置，这条断言就测不出东西。
- **测试脚本自身的 bug**：首版断言里把整文件的 `- Next action:` / `- Updated:` 计数写成 2，但 fixture 的第二条条目没有这两个字段，正确值是 1。失败是断言写错而非实现写错，已修正。

## Change Log

- 2026-09-18 由 `TF-20260918-e2317d` 提升；用户定稿范围（`Next action` + `Notes`）、寻址（Todo ID）与命名（`task next`）。
- 2026-09-18 落地时把本条 Todo 条目自己的 `Next action` 改用新命令写入（`task next TF-20260918-e2317d …`）——本条交付的第一个用例就是它自己。

## Follow-ups

- 「读」的成本未解决：Agent 为确认条目现状仍可能读整个 `todo.md`。若之后要做，方向是让 `task next` 顺带回显更新后的条目，或给 `task get` 加一个只打印单条的命令行入口。
- `TF-20260918-88e04c` 仍在 inbox，需要架构决断（archive 的 stage 步骤 / 分支选择）。

## Version History

- v1 — planning。
