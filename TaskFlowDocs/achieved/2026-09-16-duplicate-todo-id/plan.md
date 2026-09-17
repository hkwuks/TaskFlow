# Plan — Repair the duplicate Todo ID
> Task version: v1
> Status: completed

No spec required — one data repair in `TaskFlowDocs/todo.md`.

## Reference Pointers

- `hooks/task` 的 `intake` 分支 — ID 派生算法的唯一实现（`cksum` 摘要 6 位十六进制），本任务按同一算法重算，并**不修改**它。
- `hooks/task` 的 `findsec()` — 「按 ID 查取首个命中」的行为，是本任务的风险依据。
- `TaskFlowDocs/achieved/2026-09-15-todo-merge-driver/prd.md`（第 46 行附近）与 `plan.md` 的 Follow-ups — 撞车成因与「只对新 intake 生效、不回改历史」的既有决定。

## Related Tasks

- Depends on: None
- Related: `TaskFlowDocs/2026-09-16-todo-entry-loss-detection/`、`TaskFlowDocs/2026-09-16-web-ui-merge-loss-guard/`（同一条问题线；本任务不与其共享文件，可独立提交）

## Skills / Tools Used

Unaided — no capability applied to this phase; considered: `superpowers:writing-plans` and `addy-agent-skills:planning-and-task-breakdown` for the Plan. Both were judged unnecessary: the plan is a single data edit whose algorithm and acceptance are already fixed by the PRD's Background, and it is unchanged since this v1 was recorded.

## Preconditions

- [x] 适用仓库文档已读：`CONTRIBUTING.md`、`CODE_STYLE.md`。
- [x] 分支：`fix/duplicate-todo-id`；工作树 `.worktrees/duplicate-todo-id`；基于 `main`（`985b269`，PR #30 已合入）。
- [x] 远程基线：`origin` 即 `hkwuks/TaskFlow`，目标 `main`；非 fork。
- [x] 本任务不新建治理文档、不新增检查。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-17 21:13 +0800
- Approved version: v1
- Approved scope: PRD / Plan v1 —— 把 `no-python-hooks` 那条的 `- ID:` 改为按同一派生算法重算出的唯一值，`phase-concept-mapping` 保留原号。用户 2026-09-17 回复「先同步远端的main到本地，然后做C」即批准本任务的 v1 方案。

## Steps

### Step 1 — 重算并改写重复 ID

- Goal: 让「ID → 任务」重新是单值映射，且不触碰历史与 hook 行为。
- Dependencies: 无。
- Files: `TaskFlowDocs/todo.md`。
- Implementation checklist:
  - [x] 用 `hooks/task intake` 的同一算法（`printf '%s' "<Goal>" | cksum`，取 `%06x` 低 24 位）算出 `no-python-hooks` 条目的新 ID；先确认该值在当前 `todo.md` 中未被占用。
  - [x] 把 452 行附近那条的 `- ID:` 改为新值，`- Updated:` 改为改动日期。
  - [x] `phase-concept-mapping` 那条（413 行附近）保持 `TF-20260915-01` 与其余字段不变。
  - [x] 改完 grep 复核无重复，并逐字段 diff 确认只有两行变化。
- Acceptance: 见 PRD 的 Acceptance Criteria。
- Verification: `grep -o '^- ID: .*' TaskFlowDocs/todo.md | sort | uniq -d` 为空；`git diff -- TaskFlowDocs/todo.md` 只有预期的两行；重算脚本再跑一次得到同一 ID；`bash hooks/smoke-test` 全绿。
- Rollback: `git checkout -- TaskFlowDocs/todo.md`。
- Status: done

## Checkpoints

- 本任务不改任何可执行逻辑，因此不新增 smoke 断言；验收靠 grep 与逐行 diff。

## Verification / Review

改动：`TaskFlowDocs/todo.md` 一条 `- ID:`（`TF-20260915-01` → `TF-20260915-82ec4c`）与它自己的 `- Updated:`；`no-python-hooks` 那条的 `Task` / `Status` / `Next action` / `Priority` / `Owner` / `Source` / `Added` 七项逐字段比对**与改动前一致**（脚本逐项输出 `SAME`）。`phase-concept-mapping` 那条一行未动（`git diff` 里 `phase-concept-mapping` 出现 0 次）。没有 hook、脚本或测试被改，因此无新增断言。

**新 ID 的派生**

- 手算：`printf '%s' "Run TaskFlow hooks without a Python interpreter" | cksum | awk '{ printf "%06x", $1 % 16777216 }'` → `82ec4c`。
- 真 hook 复核（临时 root 上跑 `hooks/task intake "<同一个 Goal>"`）→ `TF-20260917-82ec4c`，**后缀一致**；日期段不同（`20260917` vs `20260915`）是刻意的：条目 ID 的日期段取自归属日，不是重算日。
- 文件内值与重算值比对 → `REPRODUCIBLE`。该值在改动前的 `todo.md` 全表 28 个 ID 中未被占用。

**ID → 任务重新是单值映射（用真 hook 的 awk 程序直接验证）**

| 查询 ID | 解析到的条目 | `Task:` |
| --- | --- | --- |
| `TF-20260915-01` | `Map TaskFlow phases to the concept class…` | `achieved/2026-09-15-phase-concept-mapping/` |
| `TF-20260915-82ec4c` | `Run TaskFlow hooks without a Python interpreter` | `achieved/2026-09-15-no-python-hooks/` |

- `grep -o '^- ID: .*' TaskFlowDocs/todo.md | sort | uniq -d` → 空。
- 修正了一条 PRD 里的错误假设：原判「`phase-concept-mapping` 先写入」结论对，但**依据的时间点是反的**——`a6d8fdd` 是 `2026-09-15 00:23:56 +0800`，`aecde45` 是 `12:44:48 +0800`，前者早 12 小时 21 分。按提交时间改正后，保留原号的仍是 `phase-concept-mapping`，R2 成立。
- 另一处实测发现：`promote` 在重复 ID 上**不可观测**——它对两条都先读到非 `Not promoted.` 的 `Task` 字段，于是都以 `Todo already promoted` 提前失败。可观测的路径是同样走 `findsec` 的 `state` / `progress`。已记入 PRD。

**其余**

- `bash hooks/smoke-test` → `ALL SMOKE PASSED`；`git diff --check` 干净；`python3 evals/runner.py` → `PASS (6 evals)`；`docker run … bash:3.2 bash -n hooks/task` 通过（无 hook 改动，作回归）。
- 未改任何可执行文件，所以 `smoke-test-windows.ps1` 无需单独跑。

## Change Log

- 2026-09-17 — Step 1 完成：`no-python-hooks` 的 ID 改为 `TF-20260915-82ec4c`，`phase-concept-mapping` 保留 `TF-20260915-01`。实施中发现并订正了 PRD Background 的两处事实（归属时间顺序的错误依据、`promote` 路径不可观测），均按 v1 的工作修订处理，未改变批准范围。

## Follow-ups

- **重复 ID 仍然无检查**：本任务只修这一处数据。要挡住下一次，需要在 `hooks/task` 的 ID 分配处断言唯一，或加一条只读检查；PRD 已把它列为 deferred，建议与 `TF-20260916-a357ee`（孤儿目录检测）一起判断落点——两者都是「Todo 表内部一致性」检查，可能该合并成一条。
- **`hooks/task` 的 `findsec` 仍是首个命中**：修完数据后不再有歧义，但若再出现同号条目会重现同一个静默错误。是否让 `findsec` 在发现多个命中时报错，属于行为变更，未在本任务内做。

## Version History

- v1 — planning.
