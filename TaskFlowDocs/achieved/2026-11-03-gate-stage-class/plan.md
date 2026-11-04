# Plan — 门拒绝提示只广播了阶段的一半概念类

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/capability-gate:26-35` — `stage_class()`，本次要改的函数。
- `hooks/capability-gate:390` — `class="$(stage_class "$stage")"`，唯一的调用点。
- `hooks/capability-gate:414`, `:442` — 三处拒绝提示里 `'$class'` 的插入位置。
- `hooks/task:660` — `concept_class_re`，词表本身；本次不动。
- `skills/taskflow/SKILL.md:167-178` — phase 表，唯一的权威列表。
- `hooks/smoke-test:2993-3025` — 既有的 phase 表 ↔ `concept_class_re` 双向对账，新断言照此风格。
- `hooks/smoke-test:3229-3232` — 既有断言：门提示必须含概念类。新断言叠加在它旁边。

## Related Tasks

- `TF-20261009-8abbd6`（inbox，本条是其子缺陷 1）：主体是把阶段能力选择与宿主工具调用流解耦，本次只修提示广播不全。
- `2026-10-08-capability-concept-classes`（已归档）：新增了 `divergent exploration`，其 A5 明示 `stage_class()` 不变，本条是那次取舍的已知代价。

## Skills / Tools Used

- [PRD] `agent-skills:spec` — 把缺陷收敛成可验收需求；产出并入 `prd.md` 的 Requirements / Acceptance Criteria。
- [Spec] Unaided — considered: architecture and design specification。改法由 PRD 的 R1–R3 直接决定，无跨层契约。
- [Plan] Unaided — considered: work breakdown and task decomposition。
- [Test] Unaided — considered: testing strategy。断言写在 `hooks/smoke-test` 既有风格内。

## Preconditions

- 在 `.worktrees/gate-stage-class` 的 `fix/gate-stage-class` 分支上。

## Approval

- Status: approved
- Approved by: hk
- Approved at: 2026-11-03 22:12 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 让 `stage_class` 说出该阶段的全部概念类

- Goal: `stage_class PRD` 返回 `requirements elicitation and framing; divergent exploration`；Spec 与 Plan 保持与 phase 表一致。
- Dependencies: 无
- Files: `hooks/capability-gate`
- Implementation checklist:
  - [x] `stage_classes()` 返回 phase 表原文（`; ` 分隔），`stage_class()` 取其第一项。
  - [x] 更新函数上方注释，说明它必须与 phase 表一致，且差异由 smoke 断言捕获。
- Acceptance: `bash -c 'source 提取 stage_class; stage_class PRD'` 含两个类。
- Verification: 直接调用函数断言返回值。
- Rollback: `git checkout -- hooks/capability-gate`
- Status: done

### Step 2 — 拒绝提示：一个可执行类 + 全部候选

- Goal: 逃生命令仍给一个类且原样可执行；提示另起一句列出全部候选。
- Dependencies: Step 1
- Files: `hooks/capability-gate`
- Implementation checklist:
  - [x] `class` 变量取列表第一项，供 `--considered` 使用。
  - [x] 新增 `classes_note`，在两处拒绝提示里追加全部候选。
  - [x] 只有列表多于一项时才追加那句，单类阶段不产生多余措辞。
- Acceptance: 对 `prd.md` 的拒绝提示含两个类名，且其中的 `unaided` 命令执行退出 0。
- Verification: `hooks/smoke-test` 的新断言 + 手工跑一次提示里的命令。
- Rollback: `git checkout -- hooks/capability-gate`
- Status: done

### Step 3 — 断言钉住门 ↔ phase 表

- Goal: `stage_class` 与 phase 表任一方向不一致时 smoke 变红。
- Dependencies: Step 1, Step 2
- Files: `hooks/smoke-test`
- Implementation checklist:
  - [x] 在 `:3025` 那段对账之后新增：按产物名定位 phase 表行，取概念类列。
  - [x] 对 PRD / Spec / Plan 三个阶段双向比对，允许词根 + 后缀变体。
  - [x] 断言失败时打印具体缺哪一个类、哪个方向。
- Acceptance: 变异（从 `stage_class PRD` 删掉 `divergent exploration`）后 smoke 变红。
- Verification: 跑一次变异，再还原跑一次全绿。
- Rollback: `git checkout -- hooks/smoke-test`
- Status: done

## Checkpoints

- Step 2 完成后手工确认提示可读、命令可执行；再进入 Step 3。

## Verification / Review

- 2026-11-03 Step 3: 见 ## Verification / Review

- 2026-11-03 Step 2: 见 ## Verification / Review

- 2026-11-03 Step 1: 见 ## Verification / Review

- [x] `bash hooks/smoke-test` 全绿（ALL SMOKE PASSED）
- [x] 变异验证两次（A4）：删掉 `divergent exploration` → 红，报 "phase table offers a class the gate message omits for PRD"；给 Plan 凭空加类 → 红，报 "the gate message names a class the phase table does not offer for Plan"
- [x] `git diff --check`
- [x] 手工确认：真实拒绝提示现在同时列出两个类，且提示里的 `unaided` 命令原样执行退出 0

## Change Log

- 2026-11-03 v1 — 拆出 `stage_classes()`（全量）与 `stage_class()`（首项），提示追加全量列表；smoke 新增门 ↔ phase 表双向对账。


## Follow-ups

- 三份概念类表合并为单一来源（PRD 已记为 Deferred）。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-10-11 用户裁定并入本条（不新建）**：用户指出「头脑风暴类的引导，按理应由引导工具 lead 调研和编写文档的方向，TaskFlow 只规定流程」，要查是否如此。查到两处，都属本条的能力表示层。
**(1) 门在正确时机投递的概念类，是 phase 表的一个子集 —— 可复现的机械缺陷。** `hooks/capability-gate` 的 `stage_class()` 是手抄的第二份表，PRD 只写 `requirements elicitation and framing`；而 `SKILL.md:167` phase 1 的类是 `requirements elicitation and framing; divergent exploration`（`divergent` 在 SKILL.md 出现 2 次，在 gate 里 0 次）。`divergent exploration` 在 `hooks/task:606` 的词表里、`unaided` 接受它，但**门的拒绝消息从不提它**。这是唯一「在正要写文档那一刻、无法忽略」的投递渠道（R7 的原始动机，见 `achieved/2026-09-27-capability-pre-write-gate/prd.md`），而它在 PRD 这一格只广播 converge 一个方向。`smoke-test:1740-1742` 只断言消息含 stage/类/逃生舱三要素，**没有任何断言比较 stage_class 与 phase 表**——而 phase 表与 `concept_class_re` 之间是有双向断言钉住的（`smoke-test:1596-1621`），两份手抄表只钉了一份。`achieved/2026-10-08-capability-concept-classes/prd.md` A5 明确要求 `stage_class()` 逐字不变，所以那次改动**故意**没碰它。
**(2) 交付物 schema 先于能力定死，能力只能「折进」（设计层观测）。** `prd.md` 必备小节、Plan 每 Step 的 acceptance/verification/rollback、`task approve` 的 stage 对账（`hooks/task:1055-1092`）、change-log 只能进 `plan.md`（`SKILL.md:252`）——这些在咨询任何引导工具之前就已经固定。引导工具的产出按类被折入（`SKILL.md:177`：requirements → prd.md，design → spec.md，breakdown → plan.md Steps）。设计声明是「能力供专业、TaskFlow 供流程」（`SKILL.md:8`、`159`、`163` 都写了），但强制预算全在流程侧，能力侧只有无预算的散文。历史旁证：`idea-refine` / `brainstorming` 真被用过（`achieved/2026-09-23-capability-invoke-gate/plan.md:22`），`2026-10-08-capability-concept-classes/prd.md:27` 却记录它们「没有回流成引导」。
**(1) 是可独立修的小缺陷**，修法与既有约定一致：要么让门的显示类从 phase 表派生，要么加一条和 `concept_class_re` 同风格的双向断言。用户 2026-10-09 对 (3) 的裁定（把硬 deny 降为 approve 时对账）如落地，(1) 会随之消解。相关：TF-20261008-5b5635（已 done，即上述能力类改动）
