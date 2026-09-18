# Plan — Move the deterministic Todo field writes into hooks/task

> Task version: v2
> Status: checking

No spec required — 单一文件新增两个子命令，无跨层契约。

## Reference Pointers

- `hooks/task` 的 `findsec` / `setr`：本命令复用的定位与替换原语。
- `hooks/task` 的 `state`：机械化写入的既有先例，同时说明它为何**不**写 `Next action`。
- `hooks/task` 的 `promote`：`TASKFLOW_PAIRS` + `loadpairs` 的字段写入路径，以及「Todo 已 promote」之类的守卫写法。
- `hooks/archive` 的字段缺失补行而非失败的先例与理由。
- `hooks/smoke-test` 里既有的 `Next action` 断言 —— 既有 `Next action` 相关的断言，新增覆盖要与之并存。
- `CONTRIBUTING.md` 的 PR 前必跑：`smoke-test`、Skill 校验器、`git diff --check`。

## Related Tasks

- Related: `TF-20260918-88e04c`（归档的 stage 步骤与分支选择）——本条 Todo 的 Notes 明确把它记为同一思路的另一半，但那条需要架构决断，不在本任务内。
- `old/v1/` —— v1 已落地的写入侧实现与验证记录，v2 在其上继续。
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

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

## Steps

### Step 1 — 在 `hooks/task` 里实现 `next` 子命令（v1 已完成）

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

### Step 2 — 给 `hooks/smoke-test` 补 `next` 的覆盖（v1 已完成）

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
  - [x] 不修改既有的 `Next action` 断言（`hooks/smoke-test` 里既有的 `Next action` 断言），只新增。
- Acceptance: `bash hooks/smoke-test` → `ALL SMOKE PASSED`。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout main -- hooks/smoke-test`。
- Status: done

### Step 3 — 验证与范围核对（v1 已完成）

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

### Step 4 — 在 `hooks/task` 里实现 `get` 子命令

- Goal: `task get <todo-id>` 只打印该条目的字段行，让「确认条目现状」不必回读整份 `todo.md`。
- Dependencies: Step 1（复用 `TASK_AWK` 的 `findsec` / `rfield`）。
- Files: `hooks/task`。
- Implementation checklist:
  - [x] `TASK_AWK` 增加 `cmd == "entry"` 分支：`findsec(id, "")` 定位，从 `bstart` 到 `bend` **逐行原样打印**每个 `^- ` 开头的行（不重建、不改写，保住 R8 的机读形态）。
  - [x] 不打印条目标题、不打印空行、不打印隔壁条目。
  - [x] 找不到 ID 时用既有的 `TASKFLOW_NOTFOUND` 文案 `Todo entry not found: <id>` 并非零退出。
  - [x] **不叫 `get`**：`TASKFLOW_CMD=get` 已被三个内部调用点占用（`promote` 的两处与 `complete` 的一处），它们的输出契约是「标题一行 + 按 `TASKFLOW_KEYS` 选出的字段」，不能改。新增命令行用独立分支名，`hooks/task` case 里仍写作 `get`（对外名字）——两者不许混。
  - [x] case 分支校验参数个数为 1；不设批准门禁（同 `next`，理由相同）。
  - [x] **不动 `hooks/summarize-state`**：它自己内联了一份 Todo 解析（`:37-64`），每次会话都跑，本任务不改它。
- Acceptance: 见 PRD Acceptance Criteria 的 `task get` 两条与 position 解析一条。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout main -- hooks/task`。
- Status: done

### Step 5 — 给 `hooks/smoke-test` 补 `get` 的覆盖

- Goal: `task get` 的输出形状（只含目标条目、字段顺序、可 position 解析）在 CI 的三个平台上被钉住。
- Dependencies: Step 4。
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 复用 Step 2 的 fixture（已含两条条目），断言 `task get TF-20260101-aa` 的输出**只含 `aa` 的字段**：不含 `## Seed`/`## Sparse` 标题，不含 `bb` 的任何字段行。
  - [x] 断言字段顺序与 `todo.md` 中一致（`awk` 逐行比对，而非 grep 存在性）。
  - [x] 断言 position 解析可用：`task get … | awk '/^- ID:/{print $NF}'` 得到 ID 本身。
  - [x] 断言输出不含空行、不含 `## ` 开头的行。
  - [x] 负例：不存在的 ID → 非零退出且报 `Todo entry not found`。
  - [x] 断言 `get` 不改文件（`digest` 前后一致）。
  - [x] `next` 与 `get` 组合：`next` 之后 `get` 读回的值与写入一致。
- Acceptance: `bash hooks/smoke-test` → `ALL SMOKE PASSED`。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout main -- hooks/smoke-test`。
- Status: done

### Step 6 — 验证 v1+v2 合并后的整体

- Goal: v1 已跑过的检查在 v2 追加后仍成立（`hooks/task` 与 `hooks/smoke-test` 都被 v2 再次改动）。
- Dependencies: Step 4、Step 5。
- Files: 无（只读检查）。
- Implementation checklist:
  - [x] `bash hooks/smoke-test` → `ALL SMOKE PASSED`（单次运行，不串多轮）。
  - [x] `bash hooks/release-check .` → `STATUS: pass`。
  - [x] `python3 /home/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/taskflow` → `Skill is valid!`。
  - [x] 内部调用点未变：`run_task_awk … TASKFLOW_CMD=get` 三处（`promote` 的两处与 `complete` 的一处）行为不变——`promote` 与 `complete` 仍能取到 `Task:` 与 `ID` 字段。
  - [x] 变异验证（一次一个）：把 `entry` 分支改成打印整份文件，重跑 smoke 的 `get` 节，确认断言报错；还原后 `diff -q` 与备份一致。
  - [x] 手工在临时副本上跑：inbox 条目 / 已归档条目 / 不存在的 ID。
  - [x] `git diff --check` → clean。
  - [x] 范围核对：改动仅 `hooks/task`、`hooks/smoke-test`、本任务目录、`TaskFlowDocs/todo.md`。
- Acceptance: 每条的实际输出记入 `## Verification / Review`。
- Verification: 本节即为验证。
- Rollback: 不适用。
- Status: done

## Checkpoints

- Step 1 后：`bash hooks/task`（无参数）仍打印既有 usage；`grep -c "require_approval" hooks/task` 不变（`next` 不得引入新调用）。
- Step 2 后：`grep -c "ALL SMOKE PASSED" hooks/smoke-test` 不变（只加节，不复制结论行）。
- Step 4 后：`grep -c 'TASKFLOW_CMD=get' hooks/task` 仍为 3（内部调用点不得被新命令行改写）。
- Step 5 后：`next` 与 `get` 两节都打印 `ok`。

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

## Verification / Review — v2（Steps 4–6）

v2 实施于 2026-09-18 23:00–23:40 +08:00，同一 worktree / 分支，base 仍为 `f55de0b`。

| 检查 | 命令 | 实际输出 |
| --- | --- | --- |
| smoke（v1+v2 全量） | `bash hooks/smoke-test </dev/null` | `ALL SMOKE PASSED`，exit 0 |
| 变异验证（一次一个） | `entry` 分支改成打印整份文件 | 新节 `FAIL get printed a sibling entry` —— 断言确实在防「返回整份 todo.md」。已还原（`diff -q` 与备份 identical） |
| release 一致性 | `bash hooks/release-check .` | `STATUS: pass` |
| Skill 校验 | `quick_validate.py skills/taskflow` | `Skill is valid!` |
| 内部调用点未变 | `grep -c 'TASKFLOW_CMD=get' hooks/task` | `3`——新命令行走独立的 `entry` 分支，`promote`/`complete` 的既有输出契约未动 |
| 手工场景（临时副本） | 无 `Next action`/`Notes` 的条目、sibling 条目不串入、position 解析、不存在的 ID | 与 Acceptance 一致；`Todo entry not found: …`，exit 1 |
| 空白/冲突标记 | `git diff --check` | clean |
| 范围 | `git status --short` | 仅 `hooks/task`、`hooks/smoke-test`、本任务目录、`TaskFlowDocs/todo.md` |

### v2 实施中的实际偏差

- **smoke-test 在我的工具环境下会挂住**：`bash hooks/smoke-test` 经管道的调用会停在 `hooks/session-start` 的 `event_json="$(cat)"`（`hooks/session-start:29`）等待 stdin，进程树停在 `anon_pipe_read`。**这不是本次改动引入的**——`session-start` 读 stdin 是其既有设计（SessionStart 事件从 stdin 传入）。规避方式：给 stdin 接 `/dev/null` 并把输出重定向到文件（`bash hooks/smoke-test </dev/null > out 2>&1`），CI 不受影响。我把两条挂住的进程终止后才继续，未改动任何 hook。
- **一条断言写错、且错法本身有教育意义**：round trip 那条原先用 `awk '{print $NF}'` 取值，但值是 `round trip.`（含空格），`$NF` 只拿到最后一个词。改用 `sed -n 's/^- Next action: //p'`。position 解析的保证（R8）只对**单词值**（如 ID）成立，这一点已写进断言旁边的注释。
- **本任务自己的 v1→v2 暴露了 `hooks/version` 的一个限制**：v1 文档当时已 staged，`git diff` 是安静的，守卫没触发；但也没有提交可读，于是 `old/v1/` 落下的不是真正的 v1 文本。已在 `old/v1/version.md` 里如实标注，并记入 Follow-ups。

## Change Log

- 2026-09-18 由 `TF-20260918-e2317d` 提升；用户定稿范围（`Next action` + `Notes`）、寻址（Todo ID）与命名（`task next`）。
- 2026-09-18 v2：用户追加读侧（`task get`），并入本任务。Steps 4–6 追加；`old/v1/` 保留 v1 的写入侧实现与验证记录。
- 2026-09-18 落地时把本条 Todo 条目自己的 `Next action` 改用新命令写入（`task next TF-20260918-e2317d …`）——本条交付的第一个用例就是它自己。

## Follow-ups

- 「读」的成本已由 Step 4 的 `task get` 覆盖。
- **`hooks/version` 的 file-mode 归档对未提交文档不准确**：本任务 v1→v2 时，v1 文档已 staged，`git diff` 是安静的，守卫没触发；但也没有提交可读，于是 `old/v1/` 里落的不是真正的 v1 文本（已在 `old/v1/version.md` 如实标注）。方向：`version` 在选中文档无提交基线时应**拒绝**而非静默复制工作区，或改为从 index 取。
- `TF-20260918-88e04c` 仍在 inbox，需要架构决断（archive 的 stage 步骤 / 分支选择）。
- 同一套 Todo 字段解析现在有两份实现（`hooks/task` 的 `TASK_AWK` 与 `hooks/summarize-state` 的内联 awk）。合并它们是独立重构。

## Version History

- v1 — planning：写入侧（`task next`）。
- v2 — 用户追加「读」的一侧（`task get`），并入本任务。Steps 4–6 为 v2 追加；Steps 1–3 的 v1 工作保留（见 `old/v1/`）。
