# Plan — 批准前审查 Plan 本身
> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md` — 三层职责划分、`## Plan Review` 三行的契约、五种 `approve` 结局、四个备选方案及放弃理由。

## Reference Pointers

- `skills/taskflow/SKILL.md` Phase 4 末尾 — 审查指引的落点。
- `skills/taskflow/SKILL.md` Phase 5 — 「失败必须修在所属层」的禁止性规则，第三问直接引用它。
- `skills/taskflow/references/artifacts.md` — Plan 轮廓与说明的落点。
- `hooks/task` `approve` 分支 — 检查插入点（`## External Facts` 之后、`approved_version` 之前）。
- `hooks/completion-gate` 顶部注释 — `pipefail` 下 `printf|grep -q` 假失败的教训，节读取必须一次 `awk`。
- [Reinforce] `skills/taskflow/SKILL.md` — 本次同时改它的 Phase 4 与 `approve` 的检查，两处措辞必须指向同一组三问，跑偏了门和指令就对不上。

## Related Tasks

- `TF-20261024-b48e56`（inbox）— 无可用能力时的回退表述。本次只要求「审查发生」，不规定审查者是谁；那条 todo 落地后可以收紧 Unaided 审查行的措辞，不影响本门存在与否。
- `TF-20261009-887511`（inbox）— 「散文无检测即失效」的先例，是本次选择硬门的直接依据。

## Skills / Tools Used

- [PRD] Unaided — 需求来自用户对三个设计问题的明确选择与仓库内既有规则；considered: requirements elicitation
- [Spec] Unaided — 三层职责与契约由既有代码结构决定，无需外部设计方法；considered: architecture and design specification
- [Plan] Unaided — 四个 Step 按依赖顺序拆分；considered: work breakdown
- [Test] Unaided — 复用既有 smoke 断言模式，不引入测试框架；considered: testing strategy

## Preconditions

- [x] 本 worktree 在 `feature/plan-review` 分支上。
- [x] 适用仓库文档已读：`CONTRIBUTING.md`、`CODE_STYLE.md`、`TaskFlowDocs/repository-docs/index.md`。
- [x] 无远程/fork 相关工作，不涉及 PR 模板以外的远程事实。

## Plan Review

- Verdict: sound
- Coverage: PRD 验收标准逐条对照 —— ①轮廓含新节且位置在 `## Approval` 之前 → Step 3；②四种拒绝与一种通过 → Steps 1、4；③消息各不相同可区分 → Step 1；④已归档任务不受影响 → Step 4 的一条断言；⑤smoke 与 diff 检查通过 → Step 4。逐条皆有 Step，无遗漏。反向：无超出范围的 Step —— `PreToolUse` 门、concept class 新增、b48e56 都列在 Out of Scope 且无对应 Step。用户两次反馈后追加的两项（`Verdict` 行、有序三步流程）分别落在 Step 1 的判定检查与 Steps 2–3 的散文，Coverage 未被打破。
- Verifiability: 逐个 Step 的 Verification 对其 Acceptance —— Step 1 的 Verification 是「手工 fixture 构造五种输入逐一跑 `approve`」，能证伪其 Acceptance（「五种结局各被拒绝且消息可区分」），因为消息文本不同正是被检查的对象。Step 4 的 Verification 是「`bash hooks/smoke-test`」，同样能证伪。Step 2 的「读回比对字段名」与 Step 3 的「读回核对」单独看是弱验证——读回只能证明自己写对了，不能证明与门一致——但 Step 4 已用 grep 锁住四字段名与「needs revision 阻止批准」两处，所以这一步的 Verification 由 Step 4 接住了；若 Step 4 的断言不存在，这两步的验收确实不可验。剩余不可验项只有一项：`Verdict: sound` 是否**正确**，机器无法判定，已写入 `artifacts.md` 作为机制的诚实边界。
- Layer ownership: 逐条读改动触碰了什么 —— 没有哪一步的意图是改中间产物让下游变绿。实现中确有一处相邻情形：新门让四个既有 smoke 夹具失败。处理方式是给夹具补上 `## Plan Review` 四行，而不是放宽门或跳过断言——这些夹具声称自己是「可批准的任务」，补上契约要求的字段才是修在所属层。门的所属层是 `hooks/task`（`approve` 的拒绝路径），断言层是 `hooks/smoke-test`，两者都没有为了变绿而互相让步。改动清单里无夹具的期望值被改成迁就实现。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-07 21:52 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — `approve` 检查 `## Plan Review`

- Goal: 在 `approve` 的 `## External Facts` 检查之后，新增对 `## Plan Review` 节的检查：节存在、非空、三条固定行齐全且各有内容。
- Dependencies: 无
- Files:
  - `hooks/task`
- Implementation checklist:
  - [x] 一次 `awk` 读出节体，不用 `printf | grep -q`。
  - [x] 五种拒绝消息各不相同：无节、空节、缺 Coverage、缺 Verifiability、缺 Layer ownership。
  - [x] 拒绝消息给出该节的完整模板，可直接复制。
- Acceptance: 合格输入通过，五种不合格输入各被拒绝且消息可区分。
- Verification: 手工 fixture 构造五种输入逐一跑 `approve`。
- Rollback: `git checkout -- hooks/task`
- Status: done

### Step 2 — SKILL.md Phase 4 加审查指引

- Goal: 在 Phase 4 末尾、`## Approval` 模板之前，说明批准前要审哪三问、为什么必须在这一刻。
- Dependencies: Step 1（措辞要与门检查的字段一致）
- Files:
  - `skills/taskflow/SKILL.md`
- Implementation checklist:
  - [x] 说明三问各查什么。
  - [x] 第三问显式引用 Phase 5 的禁止性规则，不另立标准。
  - [x] 说明审查者是能力还是模型自身都算，取决于宿主有什么。
- Acceptance: 指令与门检查的字段名逐字一致。
- Verification: 读回比对 `hooks/task` 里的字段名。
- Rollback: `git checkout -- skills/taskflow/SKILL.md`
- Status: done

### Step 3 — artifacts.md 的 Plan 轮廓

- Goal: 轮廓里加 `## Plan Review`（排在 `## Approval` 之前），轮廓后补说明。
- Dependencies: Step 2
- Files:
  - `skills/taskflow/references/artifacts.md`
- Implementation checklist:
  - [x] 轮廓加节，位置正确。
  - [x] 轮廓后说明三问、谁写、为什么在 Plan 里而不在独立文件。
- Acceptance: 轮廓顺序与 `approve` 的读取假设一致。
- Verification: 读回核对；`approve` 对按新轮廓写的 Plan 通过。
- Rollback: `git checkout -- skills/taskflow/references/artifacts.md`
- Status: done

### Step 4 — smoke 断言

- Goal: 覆盖五种拒绝与一种通过，并做变异验证。
- Dependencies: Steps 1–3
- Files:
  - `hooks/smoke-test`
- Implementation checklist:
  - [x] 五种拒绝各一条断言，消息互不相同。
  - [x] 合格输入通过。
  - [x] 已归档任务不受影响（`approve` 不扫描 achieved）。
  - [x] 变异：删掉任一条字段检查，对应断言变红。
- Acceptance: 五种结局都被区分。
- Verification: `bash hooks/smoke-test`。
- Rollback: `git checkout -- hooks/smoke-test`
- Status: done

## Checkpoints

- Step 1 完成后手工验证五种输入，再进 Steps 2–3 的文档。
- Steps 1–3 完成后跑一次全量 smoke，再写 Step 4 的断言。

## Verification / Review

**改了什么**

| 文件 | 改动 |
| --- | --- |
| `hooks/task` | `promote` 骨架加 `## Plan Review`（三行空字段）；`approve` 在 `## External Facts` 之后、读 `> Task version:` 之前新增该节检查 |
| `skills/taskflow/SKILL.md` | Phase 4 末尾新增审查指引：三问各查什么、为什么在批准前、谁执行 |
| `skills/taskflow/references/artifacts.md` | Plan 轮廓加节，轮廓后补两段说明 |
| `hooks/smoke-test` | 新增一整节 `== a Plan is reviewed before it is approved … ==`；四处既有夹具补上该节 |

**一个实现中发现的设计决定**

`promote` 的骨架原本没有这一节，只有 `approve` 的检查。跑 smoke 时立刻暴露后果：所有用真实 `promote` 产物的夹具都被新门拦下。这不是夹具的问题——它说明**空节检查会拒绝每一个刚 promote 的任务**，而骨架里没有那一节就等于要求作者凭空记住字段名。

所以骨架加了空节。门仍然要求填写（空字段被拒），但位置、字段名、顺序都由骨架给出。这是「空节也算缺失」这条规则能成立的前提：拒绝一个明摆着没填的空位，比拒绝一个根本不存在的节有用得多。

**验证**

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| 无节 | 手工 fixture | `has no '## Plan Review' section` |
| 空节 | 同上 | `is present but empty` |
| 缺 Verdict | 同上 | `does not answer: Verdict` |
| 缺 Coverage | 同上 | `does not answer: Coverage` |
| 缺 Layer ownership | 同上 | `does not answer: Layer ownership` |
| 缺两条 | 同上 | `does not answer: Coverage, Layer ownership` |
| 字段留空 | 同上 | `does not answer: Layer ownership` |
| `Verdict: needs revision` | 同上 | 拒绝：「says the Plan needs revision, so it is not approved」 |
| `Verdict: maybe` | 同上 | 拒绝：「must be 'sound' or 'needs revision', not 'maybe'」 |
| 四行齐全且 `sound` | 同上 | 通过，Approval 写成 `approved` |
| `bash hooks/smoke-test` | 全量 | `ALL SMOKE PASSED` |
| `git diff --check` | | 通过 |

九种拒绝各命中不同的消息，说明门能区分「缺哪一条」而不只是「不合格」。`needs revision` 这一条是关键：它让模型的判断有后果，而不是变成一个被记录下来的字段。

**变异验证**

| 变异 | 结果 |
| --- | --- |
| 跳过整个检查 | caught（`FAIL untagged should miss stage`） |
| 空字段当作已作答 | caught（非零退出） |
| 只检查 Coverage | caught（非零退出） |
| `needs revision` 也放行 | caught（非零退出） |
| 任意词当 Verdict | caught（非零退出） |
| 完全不检查 Verdict | caught（非零退出） |

**一处修正**：`promote` 骨架最初写成 Plan 轮廓的顺序，但我在 smoke 里把断言写成匹配 `- Coverage` 这个行形，而 SKILL.md 用的是 `- **Coverage** —`。断言放宽为匹配词本身——必须锁死的是字段名（`approve` 读的就是它），不是文档的排版。

## Change Log

- v1 — 初始计划；同日完成四个 Step。
- v1 — 规划细化（批准前，用户反馈）：用户指出「填了三个字段不等于审过」，新增 `- Verdict: sound | needs revision`，判为 `needs revision` 时 `approve` 拒绝。三个问题降为支撑判断的证据，判断本身成为门。
- v1 — 规划细化（批准前，用户反馈）：用户追问「模型审核的流程写进去了吗」。原稿只写了查什么与判断的后果，没写怎么得出判断。补上三步有序审查（Coverage 逐条 → Verification 对 Acceptance → 改动触碰了什么）、发现即修而非记录、修订后从头再审、`needs revision` 仅保留给审查者无权决定的情形。
- v1 — `promote` 骨架补 `## Plan Review`：实现中发现空节检查会让每个新任务在首次 approve 时失败于一个骨架没给过的字段。

## Follow-ups

- `TF-20261024-b48e56` 落地后，可要求 Unaided 的审查行说明模型动用了什么能力，而不只是「没有工具」。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- Recorded from a side channel as a prepared intake; re-read goal for full wording. Distinct from TF-20261021-4950fc (default rules from CODE_STYLE/CONTRIBUTING) and TF-20261022-fda8d8 (archive looseness).
