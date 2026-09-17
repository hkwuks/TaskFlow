# Repair the duplicate Todo ID
> Task version: v1
> Status: completed

## Goal

`TaskFlowDocs/todo.md` 现有两条 `Status: done` 的条目共用 ID `TF-20260915-01`（`phase-concept-mapping` 与 `no-python-hooks`），而 `hooks/task` 按 ID 查找时取**首个命中**。给新条目分配唯一的 ID，并把这两条改成唯一 ID，使「ID → 任务」重新是单值映射。

## Background / Confirmed Facts

- **撞车是旧 ID 方案的产物，已被修复，但已发出的 ID 没回收**：原方案 `TF-<date>-<max+1>` 从本分支的 `todo.md` 计算，同一天同一 base 的两个分支都会分配 `TF-20260915-01`。`2026-09-15-todo-merge-driver` 已把**新** intake 改为按目标内容派生（`TF-<yyyymmdd>-<cksum 摘要>`），但当时已写在 `todo.md` 里的两条同号条目保持原样（该任务的 Follow-ups：「Todo IDs on this repository's existing entries keep their numeric suffix. The scheme is only applied to new intake; rewriting history is out of scope.」——本任务只改 Todo 里的**当前**条目，不重写历史）。
- **现状实测**：`grep -o '^- ID: .*' TaskFlowDocs/todo.md | sort | uniq -d` → 只有 `- ID: TF-20260915-01`。两条分别在 413 行（`Map TaskFlow phases to the concept class…` → `TaskFlowDocs/achieved/2026-09-15-phase-concept-mapping/`）与 452 行（`Run TaskFlow hooks without a Python interpreter` → `TaskFlowDocs/achieved/2026-09-15-no-python-hooks/`）。
- **为什么值得修**：`hooks/task` 的 `findsec()` 逐节比较 `- ID:`，**取首个命中并返回**。因此对 `TF-20260915-01` 调用 `hooks/task promote/state/progress` 会静默作用在 `phase-concept-mapping` 上，而调用者可能指的是 `no-python-hooks`。这两条目前都已 `done`，实际风险是后续任何按 ID 的引用（审计、`reopen`、再次 promote）都会解析到错误的任务。
- **引用面很小**：`TF-20260915-01` 在仓库里只出现在 `todo.md` 自身与本次三个任务的文档中。没有任何 hook、脚本、测试或治理文档**依赖**这个字面量：`hooks/smoke-test` 里有几处同名字符串，但都在 `$md` 这个一次性 fixture 仓库里（`entry 'Task ours' TF-20260915-01 …`），与真实 `todo.md` 无关；`evals/` 完全不含。`TaskFlowDocs/achieved/` 下的几处提及是历史叙述（PR #21 的引入、PR #17 的合并把哪一条带出 `main`），不是引用。
- **归属明确，且与原 PRD 的假设相反**：原判「`TF-20260915-01` 是 `phase-concept-mapping` 的条目（它先写入）」。实施时按提交时间核对，**顺序是反的**：
  - `a6d8fdd`（2026-09-15 **00:23:56 +0800**，PR #21）把 `phase-concept-mapping` 那条连同 `TF-20260915-01` 写入 `todo.md`——这是该号的**首次**出现。
  - `aecde45`（2026-09-15 **12:44:48 +0800**）把 `no-python-hooks` 那条也写成 `TF-20260915-01`——同号副本，比前者晚 12 小时 21 分。
  所以 `phase-concept-mapping` 才是先写入者，R2「先写入者保留原号」成立；被改的是 `no-python-hooks`。原 PRD 的结论恰好正确，但**依据的时间点是错的**，这里按实际提交时间改正。
- **区分两条 `findsec` 路径**：`promote` 先取 `Task` 字段，两条都是 `Not promoted.` 之外的已完成值，因此两条都会以 `Todo already promoted` 提前失败——**重复 ID 在 `promote` 上不可观测**。可观测的是同样走 `findsec` 的 `state` / `progress`：修完后按 `TF-20260915-82ec4c` 查找解析到 `no-python-hooks`，按 `TF-20260915-01` 解析到 `phase-concept-mapping`（已在真 hook 的 awk 程序上直接验证）。

## Requirements

- R1：`TaskFlowDocs/todo.md` 中 `no-python-hooks` 那条（452 行附近的 `## Run TaskFlow hooks without a Python interpreter`）的 `- ID:` 改为一个唯一值，形如 `TF-20260915-<6 位十六进制>`（沿用现有 `hooks/task` 的派生形状），由该条目的 `- Goal:` 用同一算法（`cksum` 摘要）算出，使 ID 可复现。
- R2：`phase-concept-mapping` 那条保留 `TF-20260915-01` 不变（先写入者保留原号，避免动它的历史引用）。
- R3：改完后 `grep -o '^- ID: .*' TaskFlowDocs/todo.md | sort | uniq -d` 必须为空。
- R4：**不改 `hooks/task` 的 ID 分配算法**（撞车已由目标派生方案解决）。不在本任务内给 `findsec` 加重复 ID 检测——那是行为变更，另立任务时再评估。
- R5：只改 ID 字段与受影响条目的 `- Updated:`；条目其余字段、顺序、`Status`、`Task` 链接不动。

## Acceptance Criteria

- `grep -o '^- ID: .*' TaskFlowDocs/todo.md | sort | uniq -d` 输出为空。
- `no-python-hooks` 条目的新 ID 由其 `- Goal:` 重算得到同一值（可复现，不是手编的字面量）。实际值 `TF-20260915-82ec4c`（`cksum` 摘要低 24 位）。
- `no-python-hooks` 与 `phase-concept-mapping` 两条的 `- Task:`、`- Status:`、`- Next action:`、`- Priority:`、`- Owner:`、`- Source:`、`- Added:` 与改动前一致；仅 `- ID:` 与 `- Updated:` 变化。
- 按 ID 查找重新是单值映射：`TF-20260915-82ec4c` → `no-python-hooks`，`TF-20260915-01` → `phase-concept-mapping`。
- `bash hooks/smoke-test` 全绿（既有断言不依赖这两个 ID；已确认无引用）。
- `git diff -- TaskFlowDocs/todo.md` 对真实条目的改动只有那两行（其余 hunk 是本任务自己的 `Status`/`Updated` 生命周期更新）。

## In Scope

- `TaskFlowDocs/todo.md`（一条 `- ID:` 字段；该条与本任务自身条目的 `- Updated:`）。

## Out of Scope

- 不改 `hooks/task` 的 ID 分配或查找逻辑（R4）。
- 不重写历史里的 Todo 条目；`TaskFlowDocs/achieved/` 只读不动（其中 `2026-09-15-todo-merge-driver/plan.md` 记录旧方案的 Follow-up 保留原文；`2026-09-15-phase-concept-mapping/` 等文档里的历史叙述保留）。
- 不新增检查/CI：本任务是一次数据修复，验收靠上一条 grep 即可，不为一次性修复造工具。
- 本任务**不需要** `hooks/smoke-test` 的新断言（没有新增可执行逻辑）。

## Risks / Deferred Items

- 新 ID 用 `cksum` 摘要重算，与 `hooks/task intake` 当时的算法一致。已用真 hook 在临时 root 上跑 `task intake` 得到同一后缀 `82ec4c`，因此同一算法可复现；但 ID 里的日期段是 `20260915`（条目原本的 `Added`），而今天的 `intake` 会给出 `20260917`——日期段取自条目归属日，不是重算日，这是有意的（改日期段会让 ID 与 `Added` 字段不一致）。
- 若未来再次出现重复 ID（例如有人手工复制条目），目前没有任何检查会喊。是否加一条只读检查并入 `hooks/smoke-test` 或 CI，建议留到本任务线收尾时统一判断；本任务不夹带。
- 派生 ID 的摘要被截到 24 位（`%06x`）。按当前条目量（28 条）碰撞概率可忽略，且碰撞后果只是一次重复 ID 而非丢数据；这是有意的取舍，不在本任务内改算法。实测该值在当前 `todo.md` 中未被占用。

## Open Questions

- 无（若倾向另一种 ID 形态，例如复用 `TF-20260915-01` 之外的顺序号，请在批准时指出）。

## Version History

- v1 — planning.
- v1（实施期订正，仍为 v1）——Background 的「归属明确」按实际提交时间改正：`a6d8fdd`（00:23:56）早于 `aecde45`（12:44:48），结论（`phase-concept-mapping` 先写入、保留原号）不变但依据的时间点原先是错的；补记 `promote` 因 `Task` 字段保护而**不可观测**重复 ID，可观测的是同样走 `findsec` 的 `state` / `progress`；Acceptance Criteria 补齐所验字段与新 ID 实际值。均属措辞与证据修订，不改变已批准的范围。
