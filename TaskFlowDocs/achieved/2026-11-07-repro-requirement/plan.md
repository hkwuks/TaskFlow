# Plan — 缺陷调查必须先被点名，才能被选择

> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md`

## Reference Pointers

- `skills/taskflow/SKILL.md:163` — 层职责声明：TaskFlow 是生命周期层，不是专家能力层。本任务每一处改动都不得越过此行。
- `skills/taskflow/SKILL.md:169-177` — 七阶段 → 概念类别表，本次要在 Phase 1 一行补调查类。
- `hooks/task:767` — `concept_class_re`，八个类别，`--considered` 的唯一校验点。
- `hooks/task:850` / `hooks/task:864` — `intake` / `promote` 的参数解析位置。
- `hooks/task:525-538` — Todo 条目的字段写出位置（`- Task:` 之后是 `- Next action:`）。
- `hooks/archive:307` — 关闭条目的字段白名单，不含 `- Kind:`，故关闭后该字段消失（期望行为）。
- `hooks/completion-gate` — 三个门之一；本次不动它。

## Related Tasks

- `TF-20261024-b48e56` — 「无可用能力时回退是模型自身能力」。本任务只做到让「确认无可用」成为一条可记录的显式声明，不回退语义本身留给 b48e56。

## Skills / Tools Used

- [PRD] `agent-skills:idea-refine` — purpose: 在写 PRD 前把方向从「抄 superpowers 的方法」扭回「让 TaskFlow 点名能力」；outcome: 用户明确指出初衷不是重复实现已有工具的能力，据此把 A/B 重写为「加类别 + 加 kind 声明」；incorporated: 本任务的 R1–R5 与 Out of Scope 第一条。
- [Spec] `agent-skills:api-and-interface-design` — purpose: 定 `--kind` 的命令契约与 `approve` 缺陷类分支的判定形状；outcome: 确定 intake 可省/promote 必填的不对称、kind 缺失时不推断、以及门只查「点名了没有」的诚实边界；incorporated: spec.md 的 Interfaces 与 Design Decisions 两节。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 把改动切成可独立验证的 Step；outcome: 五个 Step，按「词汇 → 参数 → 写入 → 门 → 文档」的依赖顺序，smoke 补在每步之后；incorporated: 下方 Steps 与 Checkpoints。
- [Test] Unaided — 复用 `hooks/smoke-test` 既有的断言/变异模式，不引入测试框架；considered: testing strategy

## Preconditions

- 工作树：`.worktrees/repro-requirement`，分支 `feature/repro-requirement`，基线 `main` @ `9aaa357`。
- `TaskFlowDocs/todo.md` 的本任务条目已存在且已 promote。
- 能力证据已就位：`taskflow/released` 有 PRD 与 Spec 两行，Plan 行在首次写入本文件时释放。

## Plan Review

- Verdict: sound
- Coverage: A1/A2 → Step 2；A3 → Step 3；A4 → Step 3（`## Task Kind` 骨架写入）与 Step 5（轮廓文档）；A5/A6/A7 → Step 4；A8 → Step 1；A9 → Step 3 的一条读回断言，并进入既有 A9 的判定；A10 → 各 Step 内的 smoke 断言加上 Step 4 的收尾全量。反向：没有哪个 Step 超出 PRD 的 In Scope——Step 5 只碰 `SKILL.md` 与 `artifacts.md`，Out of Scope 明列的「不写调查方法」「不新增 stage」「不动 archive 白名单」均无对应 Step。
- Verifiability: Step 1 的 Verification 是「`task unaided PRD --considered 'root cause investigation'` 被接受，改回旧词汇被拒绝」，能证伪它的 Acceptance（正则真的加上了，而不只是改了注释）。Step 2 的「缺 `--kind` 拒绝、给了通过」同理。Step 4 最容易写成证明不了自己的验证，因此它的 Verification 同时要求 A5 拒绝、A6 通过、A7 通过三件事，缺一条都无法由「门写对了」这个结论产生。Step 5 的 Verification 是读回比对文档；它单独看是弱验证（只证明我写对了字），但 Step 5 的 Acceptance 本来就只是「文档陈述了规则」，机械正确性由 Step 1–4 的 smoke 承担，分工明确。
- Layer ownership: 逐条读改动触碰了什么。**没有哪一步的意图是改中间产物让下游变绿。** 一处必须点名的相邻情形：Step 2 与 Step 3 会让 smoke 里 14 处既有 `promote` 调用失效。处理方式是给这些调用补 `--kind capability`，不是放宽 `promote` 的门——这些夹具声称自己是「一个已 promote 的任务」，补上契约要求的新参数才是修在所属层。同样，`concept_class_re` 是追加而不是重写，避免既有归档任务的 `--considered` 记录与新正则不一致（那会是把历史记录改成迁就实现）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-07 23:01 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 概念类别词汇加入调查类

- Goal: 让「查根因」成为一个可被 `--considered` 点名的类别，否则 R2 与 R4 无处落笔。
- Dependencies: 无。
- Files: `hooks/task`（`concept_class_re` 一处）。
- Implementation checklist:
  - [x] `concept_class_re` 末尾追加 `|root cause|defect investigation`，既有八项一字不改。
  - [x] 在正则上方补注释，说明为什么是追加而非重写。
- Acceptance: `task unaided PRD --considered 'root cause investigation'` 与 `--considered 'defect investigation'` 均被接受；`--considered 'nonsense'` 仍被拒绝。
- Verification: 在临时夹具里跑上述三条，断言前两条退出 0、第三条非 0 且信息里点名了非法值。
- Rollback: `git checkout -- hooks/task`
- Status: done

### Step 2 — intake/promote 解析并校验 --kind

- Goal: R1 的参数面。promote 必填、intake 可省，取值三选一。
- Dependencies: Step 1（词汇就位后才有意义，但参数本身不依赖它；排在这里是因为它先于写入）。
- Files: `hooks/task`（`intake` 与 `promote` 的参数解析、`split_root` 之后的校验）。
- Implementation checklist:
  - [x] `intake` 接受可选 `--kind`，默认 `capability`；非法值拒绝并点名该值。
  - [x] `promote` 要求 `--kind` 必填；缺省拒绝并给出三个取值；非法值同上。
  - [x] 两者的 `--root` 仍是最后一个选项（沿用 `split_root` 的既有契约）。
  - [x] 拒绝发生在任何写入之前。
- Acceptance: A1、A2。
- Verification: 夹具里跑 `promote` 不带 `--kind`、带 `--kind nonsense`、带 `--kind defect` 三次，断言前两次非零且信息含三个取值／点名非法值、第三次成功。
- Rollback: `git checkout -- hooks/task`
- Status: done

### Step 3 — --kind 写入 Todo 条目与 PRD 骨架

- Goal: 让声明的 kind 留下来，triage 与审批各看到一份。
- Dependencies: Step 2。
- Files: `hooks/task`（intake 的 awk 写出块、promote 的 PRD 骨架）。
- Implementation checklist:
  - [x] `intake` 在 `- Source:` 之后、`- Added:` 之前写出 `- Kind: <value>`。
  - [x] `promote` 的 PRD 骨架在 `## Goal` 之后、`## Background / Confirmed Facts` 之前写出 `## Task Kind` 与 `- Kind: <value>`。
  - [x] 没有 `- Kind:` 字段的既有条目不报错（读路径不依赖该字段）。
- Acceptance: A3、A4、A9。
- Verification: 一次 `intake --kind defect` 后读回 Todo 条目；一次 `promote --kind defect` 与一次 `--kind capability` 后各读回 `prd.md`；再用一个手写的、无 `- Kind:` 的旧条目跑 `task get`，断言输出键集合与今天一致。
- Rollback: `git checkout -- hooks/task`
- Status: done

### Step 4 — approve 的缺陷类分支

- Goal: R2 与 R4。缺陷类任务的 `[PRD]` 行必须点名调查类，或显式记录「确认无可用调查能力」。
- Dependencies: Step 1（词汇）、Step 3（`## Task Kind` 节存在才读得到 kind）。
- Files: `hooks/task`（`approve` 分支，位置在对账之后、`approved_version=` 之前）。
- Implementation checklist:
  - [x] 读 `prd.md` 的 `## Task Kind` → `- Kind:`；缺失或非 `defect` 时不施加任何约束（R5）。
  - [x] `kind=defect` 时读 `## Skills / Tools Used` 的 `[PRD]` 行。
  - [x] `Unaided` 行：`considered` 必须含调查类词根，否则拒绝并给出两条出路。
  - [x] invoke 行：能力名必须含调查类词根，否则拒绝。
  - [x] 全部拒绝在写入 Approval 之前。
- Acceptance: A5、A6、A7。
- Verification: 三个夹具分别构造 A5/A6/A7 的 Plan，逐一跑 `approve` 读回；A5 必须拒绝且信息说明两条出路，A6/A7 必须通过。
- Rollback: `git checkout -- hooks/task`
- Status: done

### Step 5 — 文档：Phase 1 类别表与 PRD 轮廓

- Goal: 让模型知道有这条路可走，且知道它不越过层边界。
- Dependencies: Steps 1–4（文档描述的是已实现的行为）。
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`。
- Implementation checklist:
  - [x] `SKILL.md` 的概念类别表 Phase 1 一行补调查类，措辞指向「查清已报告错误的成因」而非「怎么查」。
  - [x] `SKILL.md` Phase 1 补分流说明：缺陷类先点名调查能力再写需求；非缺陷类不受此约束；并重申方法本身不属于 TaskFlow。
  - [x] `artifacts.md` 的 PRD 轮廓加 `## Task Kind`，并说明它为什么必填而非可选。
  - [x] `artifacts.md` 写明诚实边界：门只保证类别被点名，不保证能力合适。
- Acceptance: 两处文档陈述与 Step 1–4 的实际行为一致，无自相矛盾。
- Verification: 读回比对；`grep` 确认 `SKILL.md` 类别表与 `hooks/task:767` 的正则条目一一对应，不多不少。
- Rollback: `git checkout -- skills/taskflow/SKILL.md skills/taskflow/references/artifacts.md`
- Status: done

## Checkpoints

- Step 1 完成后单独跑一次 `unaided` 的三条用例，再进 Step 2——词汇是所有后续步骤的地基。
- Steps 2–4 完成后跑一次全量 smoke，此时 14 处既有 `promote` 调用会因为缺 `--kind` 变红；补 `--kind capability` 后再跑一次，必须全绿。
- Step 5 完成后跑最终全量 smoke 与 `git diff --check`。

## Verification / Review

**改了什么**

| 文件 | 改动 |
| --- | --- |
| `hooks/task` | `concept_class_re` 追加 `root cause`、`defect investigation`；新增 `split_kind`；`intake` 接受可选 `--kind`（默认 `capability`），`promote` 必填；Todo 条目写 `- Kind:`；PRD 骨架写 `## Task Kind`；`approve` 加缺陷类分支 |
| `hooks/capability-gate` | `stage_classes` 的 PRD 分支补两个调查类——门消息是 agent 在那一刻唯一能读到的规则，消息里没有的类别等于不存在 |
| `skills/taskflow/SKILL.md` | Phase 1 类别表补调查类；新增「请求是修已坏的东西时，先查清为什么」一段，并重申方法本身不属于 TaskFlow |
| `skills/taskflow/references/artifacts.md` | PRD 轮廓加 `## Task Kind`；补写它的来历、位置理由与诚实边界 |
| `hooks/smoke-test` | 新增整节 `== a defect task has to name what investigates the cause ==`；15 处既有 `promote` 调用补 `--kind capability` |
| `TaskFlowDocs/todo.md` | 模板样例补 `- Kind:`——模板与实际写入字段的一致性断言会抓到缺失 |

**一处实现中发现的相邻问题**

`hooks/task` 的 `intake` 与 `promote` 里，局部变量 `kind` 已经被 `worktree_kind` 的返回值占用。新增的 `--kind` 值若同名会互相覆盖，表现为「在 base 树里 promote 被拒」的假象。已把工作树判定改名为 `wt_kind`，`--kind` 的值保持 `kind`。这不是风格调整，是命名冲突导致的真实覆盖。

**验证**

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| A8 词汇 | 夹具内 `unaided PRD --considered 'root cause investigation'` / `'defect investigation'` / `'nonsense'` | 前两条接受，第三条拒绝并列出十个类别 |
| A1 promote 缺 `--kind` | 夹具 | `promote needs --kind, one of: defect capability internal...` |
| A2 非法值 | `promote ... --kind defects`、`intake ... --kind nope` | 各自点名非法值并退出 1 |
| A3 intake 默认 | `intake`（省略）、`intake --kind defect` | `- Kind: capability` / `- Kind: defect` |
| A4 骨架 | `promote --kind defect` | PRD 含 `## Task Kind` 与 `- Kind: defect`，且位于 `## Background` 之前 |
| A5 缺陷类未点名调查 | 完整 PRD + Plan | 拒绝，消息给出两条出路 |
| A6 缺陷类点名调查 | 同上，`considered: root cause investigation` | 通过，写入 `approved` |
| A7 非缺陷类 | `- Kind: capability` + `considered: requirements elicitation` | 通过 |
| A9 无 `- Kind:` 的旧条目 | 手工删除该行后 `task get` | 字段集合与改动前一致 |
| A10 全量 | `bash hooks/smoke-test` | `ALL SMOKE PASSED`（119 个 ok） |

**变异验证**

| 变异 | 结果 |
| --- | --- |
| 整个缺陷检查短路为永不成立 | caught（`a defect task whose PRD phase named no investigation was approved`） |
| 接受任意类别（去掉调查类词根要求） | caught（同上） |
| `promote` 放行缺失的 `--kind` | caught（`promote accepted a promotion with no --kind`） |
| `intake` 默认值改成立 `defect` | caught（`intake did not default the kind to capability: [- Kind: defect]`） |
| 骨架去掉 `## Task Kind` | caught（`promote wrote no '## Task Kind' section`） |

**一处修正**：新断言的夹具最初把 `intake` 写在 base 树、`promote` 指向 worktree，于是 `promote` 读不到 `todo.md`。改为两者都在 worktree 内执行——`promote` 读的是它被给定的 root 下的 `todo.md`，写在别处的条目不是它要 promote 的那一条。

## Change Log

- v1 — 初始计划。用户两次纠偏后定稿：不抄 superpowers/brainstorming 的调查方法（那属于能力层，且 `SKILL.md:163` 明令 TaskFlow 不做），只补 TaskFlow 自己缺的那一环——让「调查」成为可点名、可记录、可校验的类别。原 A/B 中「必须重现」「red-green 前后一对」「撤回再验」全部删除。
- v1 — 实现完成，五个 Step 全部 done。实现中发现并修正：`kind` 变量名与 `worktree_kind` 返回值冲突；`capability-gate` 的 PRD 消息也必须补类别，否则门与类别表不一致的断言会红。

## Follow-ups

- `TF-20261024-b48e56`：本任务只让「确认无可用调查能力」成为一条显式声明，回退语义仍归它。
- 非缺陷类任务是否需要 anti-goal 字段：本次未做，观察一段时间再定。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **初查结论（2026-11-07，读了 SKILL.md / artifacts.md / hooks/task / hooks/completion-gate / 近 8 个归档任务与提交）**——不是单点，是三条同时起作用：
  **① 工作流只在「描边」上闭合，从不在「本质」上闭合。** 所有硬门读的都是文档形状，没有一处读证据内容：`approve` 读的是 `## Skills / Tools Used`、`## External Facts`、`## Plan Review` 四行的**存在与否**；`completion-gate` 读 `- Status: done` 与 `- [ ]`；`capability-gate` 只确认「这个阶段调用过某能力」。`hooks/` 里**没有任何一处**读 `git diff`，也**没有任何一处**要求「先证明缺陷存在」。`reproduc*` 在整个 SKILL.md 里只出现 1 次，而且是 `blocked` 状态的定义。所以一个任务可以在没有任何人重现过症状的情况下走完全程并归档。
  **② 验收标准本身可以被写成「周边工作」。** 190 条归档验收标准里 76 条（40%）的主语是 smoke / 断言 / README / SKILL.md 这类自身产物。这不是模型偷懒——是在照 `artifacts.md` 的 PRD 轮廓写，而那个轮廓对 `## Acceptance Criteria` 一句要求都没有（该节标题下面直接就是 `## External Facts`）。标准写歪了，之后的 Coverage 审查也只是忠实地覆盖这些歪掉的标准。
  **③ 发散探索的触发条件写反了。** SKILL.md:222 的触发条件是「当目标或路径尚未确定时」才发散。但用户这类反馈恰恰是「目标明确（有这个毛病），机制不明」——正落在触发条件的反面，于是流程直接收敛到「我来给这个状态加个标记」。由于 ① 的机制决定收敛出来的东西只要形状对就能过门，流程会稳定地奖励「改文档让门变绿」。**这是最接近你猜测的那条**：不是发散流程没看出本质，是它的触发条件恰好排除了「症状明确、根因未知」这一整类。
  方向（未定，待你选）：A 把发散触发条件从「目标是否确定」改成「机制是否已知」；B 给 PRD 加一条「缺陷必须能被重现」的必填；C 让验收标准禁止以自身产物为主语；D 都不动门，只改文档。C 和 A 会互相咬（标准写实之后覆盖审查才有意义），B 是唯一能直接堵住「没重现就归档」的。
