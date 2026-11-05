# Plan — 分层完整性：把「失败修在失败所属的层」变成插件的硬规则
> Task version: v1
> Status: completed

## Spec Pointers

- `TaskFlowDocs/2026-11-05-layered-integrity/spec.md` — SC1-SC4、三个契约点、四个方案的取舍。
- `skills/taskflow/SKILL.md:234-243` — 当前的大/小判据，本次重写对象。
- `skills/taskflow/SKILL.md:299-315` — Phase 6 现有 8 条验证项，本次追加第 9 条。
- `skills/taskflow/references/artifacts.md` 的 `## Spec outline for large tasks` — 架构节的字段说明落点。

## Related Tasks

- `TF-20261105-77051f`（inbox，未 promote）— 改动目标的分类规则。本任务在 spec 的 Architecture Boundaries 一节引用了它作为前提，但**不实现它**；两者文件不重叠。

## Skills / Tools Used

- [PRD] Unaided — requirements elicitation and framing; considered: requirements elicitation and framing. 需求来自用户 2026-11-05 的三条明确决定（落在 spec、靠模型判断、禁止性），没有值得调用的需求引出能力；Todo `TF-20261105-f322be` 的 Notes 已记录外部调研与候选方向。
- [Spec] invoke `agent-skills:spec-driven-development` — purpose: 把「分层理解 + 禁止目标欺骗」落成有成功标准与契约点的 Spec，并在四个候选方案间做取舍；outcome: 产出 SC1-SC4、三个契约点，选定方案 A（改插件文本），否决 B/C/D；incorporated: spec.md 全文，特别是「为什么仍在 spec.md 而不新增产物」的论证。
- [Plan] Unaided — work breakdown and task decomposition; considered: work breakdown and task decomposition. 改动是四处文本编辑，边界已由 Spec 划定，无依赖图可分。
- [Test] Unaided — testing strategy; considered: testing strategy. 本任务不产生可执行逻辑，验证是既有 smoke 套件回归 + 人工通读规则文本是否可被 Agent 读懂。

## Preconditions

- 处于任务 worktree `.worktrees/layered-integrity`，分支 `feature/layered-integrity`。
- `bash hooks/smoke-test` 当前为 `ALL SMOKE PASSED`（基线）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-05 22:19 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 重写大/小任务判据

- Goal: 「一个文件」不再足以判 small；跨层契约成为 small 的必要不满足项。
- Dependencies: 无。
- Files: `skills/taskflow/SKILL.md`。
- Implementation checklist:
  - [x] 把 `Large` 判据改写为以「是否跨层」为首要问题，形态判据降为辅助。
  - [x] 把 `Small` 判据改为需要**同时**满足：不跨层契约、无外部接口变化、单层内可验证。
  - [x] 说明为什么：形态判据会漏掉「改一个文件但改变了一条跨层契约」的情形。
- Acceptance: SC1。
- Verification: 通读改写后的段落，确认 small 的三个条件缺一不可。
- Rollback: `git checkout -- skills/taskflow/SKILL.md`。
- Status: done

### Step 2 — 规定 spec.md 的架构节必须回答什么

- Goal: 架构节从「列出目录」变成「说清每层负责什么、不负责什么、契约是什么」。
- Dependencies: Step 1。
- Files: `skills/taskflow/references/artifacts.md`。
- Implementation checklist:
  - [x] 在 Spec outline 之后补一段字段说明，明确 `## Architecture Boundaries and Responsibilities` 必须包含：每层的职责、每层**明确不负责**的事、以及依赖方向。
  - [x] 明确 `## Interfaces, Data Flow, and Contracts` 必须给出每条边界的输入输出契约（这是下游能判断「中间产物是否被篡改」的前提）。
- Acceptance: SC2。
- Verification: 通读，确认两节的要求可与 spec 的三个契约点对应。
- Rollback: `git checkout -- skills/taskflow/references/artifacts.md`。
- Status: done

### Step 3 — 加入禁止性规则（Phase 5）

- Goal: 「为让下游通过而改中间产物」被明确命名为目标欺骗并禁止。
- Dependencies: Step 1、Step 2。
- Files: `skills/taskflow/SKILL.md`。
- Implementation checklist:
  - [x] 在 Phase 5 Build 段落加入禁止性规则：失败必须修在失败所属的层。
  - [x] 明确写出：需要改中间层行为时，先改那一层自己的验收标准和测试，而不是让它对下游看起来正确。
  - [x] 沿用既有文风：说明为什么（症状所在的位置不是失败所属的位置）。
- Acceptance: SC3。
- Verification: 通读，确认是禁止性措辞而非建议。
- Rollback: `git checkout -- skills/taskflow/SKILL.md`。
- Status: done

### Step 4 — 追加入 Phase 6 验证项

- Goal: 验证阶段问一次「你改了什么才让它通过」。
- Dependencies: Step 3。
- Files: `skills/taskflow/SKILL.md`。
- Implementation checklist:
  - [x] 在 Phase 6 的 8 条之后加第 9 条，检查本次改动是否触碰了中间层产物来满足下游检查。
  - [x] 保持与既有 8 条同样的句式（短句、可自答）。
- Acceptance: SC3、SC4。
- Verification: 通读，确认 9 条并列且风格一致。
- Rollback: `git checkout -- skills/taskflow/SKILL.md`。
- Status: done

### Step 5 — 回归与一致性检查

- Goal: 改动没有破坏任何既有内容，也没有自相矛盾。
- Dependencies: Step 1-4。
- Files: 无（只读复核）。
- Implementation checklist:
  - [x] `bash hooks/smoke-test` 仍为 `ALL SMOKE PASSED`。
  - [x] `git diff --check` 干净。
  - [x] grep 确认没有把规则写进 `hooks/templates/`（SC 的边界条件）。
  - [x] 确认改动只在 `skills/taskflow/SKILL.md` 与 `skills/taskflow/references/artifacts.md`。
- Acceptance: SC4。
- Verification: 上述四条命令/检查。
- Rollback: 无需（只读）。
- Status: done

## Checkpoints

- Step 3 完成后通读 Phase 3 + Phase 5，确认两处规则不矛盾（判据说「必须写 spec」，禁止规则说「改对层」）。

## Verification / Review

**逐条对照验收标准**：

- **AC1**：`SKILL.md` 的判据段已重写——首句改为「第一个问题不是改几个文件，而是是否跨越层边界」，并给出反例（改一个文件却改变跨层契约 = large；五个文件全在一层内部 = 可以 small）。small 的三个条件用「**all three** must hold」表述，缺一不可。文件数与时长明确降为 `supporting signals, never sufficient on their own`。
- **AC2**：`artifacts.md` 的 Spec outline 后新增两段：架构节必须回答「每层负责什么 / **明确不负责什么** / 依赖方向」；接口节必须给出「生产者保证什么 / 消费者因此有权假设什么」的双向契约，并说明为什么这使中间值可被检查。
- **AC3**：Phase 5 新增禁止性段落，措辞为 `is not a fix` / `is prohibited`，无「建议」「尽量」。已 grep 确认新文本不含软性词（命中的 5 处均为仓库既有文本，不在本次改动范围）。
- **AC4**：Phase 6 验证项由 8 条变为 9 条，第 9 条问 `what the change touched to make the checks pass`。
- **AC5**：`bash hooks/smoke-test` → `ALL SMOKE PASSED`；`git diff --check` 干净。
- **AC6**：`git status --short` 只含 `TaskFlowDocs/todo.md`、`skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md` 与任务目录；`hooks/templates/` 未被触碰（已单独核对，输出为空）。

**一处超出原 Step 清单但属于 AC3 的必要补充**：Phase 6 末尾加了一段「规则的边界」——说明三类**合法**改动（测试本就写错了契约、fixture 编码了 Spec 已改变、批准的需求重新定义了期望）不得被当作违规。没有这段，第 9 条会鼓励 Agent 隐藏合法改动而不是记录它们，反而制造更多静默。

**R6 核对**：未加任何 hook、未加校验命令、未改 `hooks/task` 的 scaffold 文案。

## Change Log

- 2026-11-05：实现 Step 1-5。`SKILL.md` 三处（Phase 3 判据、Phase 5 禁止规则、Phase 6 第 9 条与边界说明），`artifacts.md` 一处（Spec outline 后的两节要求）。
- 2026-11-05：Phase 6 末尾的「规则边界」一段是实施中新增的，理由见 Verification；不改变已批准的 R1-R6 任何一条。

## Follow-ups

- `TF-20261105-77051f`（改动目标分类）未实现。若它先落地，本任务 spec 的 Architecture Boundaries 一节可改为引用它而不是复述三层的表。
- 本任务只约束 Agent 行为，不产生机械检查。若日后发现规则被无视，再考虑加 hooks——但需先有实例，避免凭空设计拦截。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-11-05 用户补充**：除了防作弊，还要引导模型**充分理解整体架构和各层的功能**，这样实现较粗粒度的 prompt 要求时才能找到问题所在。
  **为什么是一件事而非两件**：模型若不知道某一层本来该负责什么，就只能从可见症状处下手——而症状所在的位置往往不是失败所属的位置。改中间产物让上层断言通过，正是「找不到真正的层」之后的退路。所以「理解分层」是「不作弊」的前提，不是并列项。
  **仓库现状的两个缺口**（2026-11-05 核对）：
  1. **没有任何规则禁止目标欺骗**。`SKILL.md` Phase 6 的 8 条验证清单全部关于「结果」，没有一条问「你改了什么才让它通过」；`CODE_STYLE.md` 只说「最小改动」；`CONTRIBUTING.md` 说 CI 是权威，而 CI 只跑断言、不检测断言是否被削弱。唯一接近的是 `hooks/smoke-test` 里 25 处 `Measured 2026-*` 注释，那是人写断言时的纪律，不是对 Agent 的约束。
  2. **架构理解的载体没有被要求填写**。`spec.md` 有 `## Architecture Boundaries and Responsibilities`、`## Interfaces, Data Flow, and Contracts` 两节（`hooks/task:920-926` 的 scaffold 每节都是空的），但只有 large 任务才写 spec，且没有任何 hook 校验这两节是否真的描述了「每层负责什么」。small 任务完全没有这一层理解。
  **外部证据**（调研 2026-11-05）：
  - SpecBench（arXiv 2605.21384）：每个前沿 agent 都刷满可见测试套件而作弊依旧；**代码量每增 10 倍，visible 与 held-out 通过率差距增加 28 个百分点**。存在 2900 行纯记忆测试输入的假编译器。
  - EvilGenie（arXiv 2511.21654）：Codex 与 Claude Code 均观察到明确 reward hacking；Claude Code 的 heuristic solution 占 20.7%，Gemini 3.4% 直接删测试文件。**held-out tests 收益很小，test-file edit detection 与 LLM judge 才有效**。
  - Specification Self-Correction（arXiv 2507.18742）：模型 50-70% 会利用有缺陷的 spec；让模型**先审视 spec 本身的漏洞**可降幅 92%。
  **候选方向**：
  - (a) 在 `CODE_STYLE.md` 与 `hooks/templates/CODE_STYLE.md` 加一条分层规则：失败必须修在失败所属的层；改中间产物让下游通过属于目标欺骗，属实需改时先改该层自己的验收标准。
  - (b) 在 Phase 6 验证清单加第 9 条：diff 里每个被削弱的既有断言都要能说出它为什么本来就错了。
  - (c) 让架构理解成为 small 任务也要写的一小段——不是完整 spec，而是「本次改动涉及哪几层、每层的输入输出契约是什么」。
  - (d) 先由模型在实现前写下「失败若出现，最可能在哪一层」，验证阶段回头对照（Specification Self-Correction 的结构）。
  - 不做 (e)：`PreToolUse` 拦截测试文件改动。误报多，且研究显示收益不如独立判断者。
  **2026-11-05 用户裁定（纠正了 Agent 的错误理解）**：这跟「哪个仓库」没有关系。**本仓库就是插件本身**，要动的是插件自己的能力——`skills/taskflow/SKILL.md` 与 `references/`——而不是 `hooks/templates/`。`templates/` 是发给**别人的仓库**的默认规则，只有用户 `repo-rules create` 同意后才生效，那条路径管不了「插件自己怎么工作」。所以这条规则**直接属于插件的行为规范**，与任何被管理仓库的 CODE_STYLE 无关。
  **同时新增一条仓库规则（用户原话）**：「让后续开发的时候搞清楚是要改插件的功能，还是要改插件默认给的仓库规则模板，还是只是改我自己这个仓库的规则。」→ 已另记 `TF-20261105-` 条目（见下方）。
