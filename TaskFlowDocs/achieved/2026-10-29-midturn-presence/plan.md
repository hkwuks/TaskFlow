# Plan — Stay present inside a long implementation run, not only at the prompt
> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md` — C1/C2（`apply_patch` 解析与失败判定）、C3（审批判定抽成 `approval-check`）、D1（Step 证据形态）、D2（拒绝强制 `progress`）、D3（不另开解析脚本）

## Reference Pointers

- `[Reinforce] hooks/capability-gate` — 本任务要改它的两处（`apply_patch` 分流、审批检查），它现有的 deny 消息风格与路径归一化是本任务必须沿用的
- `[Reinforce] hooks/completion-gate` — 审批判定要从这里搬出成 `approval-check`，搬完它的行为必须逐字节不变
- `[Reinforce] CONTRIBUTING.md` — 本任务新加的宿主覆盖规则（not wired / not supported）就是本任务自己的验收标准

## Related Tasks

- `[[TF-20261027-e8c6dc]]` — 外部来源问题：若本任务最终证明「TaskFlow 该在别的地方说话」，那条可能用散文解决
- `TaskFlowDocs/achieved/2026-10-09-trae-host/` — 事实 4 的原始样本；它的 Plan 就是「4 个 Step 一次脚本翻完」的形态
- `TaskFlowDocs/achieved/2026-09-27-capability-pre-write-gate/` — `capability-gate` 的出处，本任务扩它的输入面

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — 起草 PRD v1，并据用户三次澄清重写诊断部分；incorporated: 诊断从「模型不知道 Step」改为「progress 只增摩擦、无可验证收益」
- [Spec] `mcp__exa__web_search_exa` — 查 Codex 官方 hooks 文档，确认 `PreToolUse`/`apply_patch`/`permissionDecision` 的实际形状；incorporated: 事实 11 的能力表、C1 的 `tool_name` 精确比较、C2 的失败判定表
- [Plan] `agent-skills:planning-and-task-breakdown` — 按依赖关系排定 Step 顺序与检查点；incorporated: Step 1 抽共享判定先行，其余 Step 全部依赖它
- [Test] Unaided — considered: testing strategy

## Preconditions

- [x] `TaskFlowDocs/repository-docs/index.md` 已读；`CONTRIBUTING.md`、`CODE_STYLE.md`、`LICENSE` 已作为权威来源
- [x] 远程信息已记录：`origin` → `https://github.com/hkwuks/TaskFlow.git`（`git remote get-url origin`，无 fork remote，无凭据）
- [x] 本任务的宿主覆盖规则已落在 `CONTRIBUTING.md`，并被 smoke 钉住
- [x] PR 模板字段映射在 Step 6 完成
- [x] 已知限制记录：本机没有 Codex，A12/A14 的真机验证由用户在另一台机器上执行

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-30 16:46 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 抽出 `hooks/approval-check`，两个 gate 都改调它

- Goal: 让「Plan 是否已审批」只有一处实现（Spec C3、Q7）。
- Dependencies: 无（其余 Step 都依赖它）
- Files: `hooks/approval-check`（新增）、`hooks/completion-gate`、`hooks/capability-gate`（后者仅接入，判定行为改变在 Step 2）
- Implementation checklist:
  - [x] 新建 `hooks/approval-check`，判定从 `completion-gate:86-91`、`:110-111` **原样搬出**，不改语义
  - [x] 接口：`approval-check [--stale-only] <plan.md>`，`exit 0` 通过，`exit 1` + stderr 一行
  - [x] `completion-gate` 改调它；**先跑一遍两者在全部 93 份归档 Plan 上的结论对比，必须逐份一致**
  - [x] `capability-gate` 接入调用点（不改变其判定时机）

  注：`--stale-only` 是这轮实现中补上的第二个模式。`capability-gate` 需要的不是「批没批」，而是「这份审批是否已被版本降级淘汰」——直接复用退出码会让它在 `planning` 阶段拒绝写 `prd.md`，正是 Step 2 checklist 里废弃的那个死锁。两个模式共用一个 awk、一处字段解析，结论各自成立。
- Acceptance: Spec C3；搬动前后 `completion-gate` 对 93 份 Plan 的结论完全一致
- Verification: 逐份跑 `approval-check` 与旧内联逻辑，diff 结论
- Rollback: 删除新文件、还原两个 gate
- Status: done

### Step 2 — 审批保护：版本不降级（archive 侧已有，只补回归）

- Goal: 让审批在它真正该拦住的地方生效（PRD A9/A9b/A10/A10b、Spec C3）。
- Dependencies: Step 1
- Files: `hooks/capability-gate`、`hooks/smoke-test`
- Implementation checklist:
  - [x] **检查时机已修正**：`planning`/`ready` 阶段写 `prd/spec/plan.md` **不查审批**——审批是开工许可（`SKILL.md:193`），不是写文档许可。原设计「未审批不得写 prd.md」会锁死每个新任务的第一步，已废弃
  - [x] `capability-gate` 只拦一种情况：**`- Approved version:` 与 `> Task version:` 不一致时继续写那份文档**（拿旧批准写新版本）
  - [x] **不改 `hooks/archive`**——实测它已拒未审批任务（`archive:44` 调 `completion-gate`，自 `be69289`/2026-10-24 起）。本 Step 只补断言防回退
  - [x] smoke 正向：版本一致且已批准 → 放行
  - [x] smoke 反向：版本不一致 → gate 拒绝
  - [x] smoke 回归：未审批任务归档被拒（钉住既有行为，不是新功能）
  - [x] smoke 回归：93 份归档的归档路径不受影响
- Acceptance: A9、A9b、A10、A10b
- Verification: 上述用例 + 变异（去掉版本比对 → 反向用例变红）
- Rollback: 摘掉版本比对调用点
- Status: done

### Step 3 — `completion-gate`：多重 `- Status:` 报错

- Goal: 同一 Step 块两个 `- Status:` 报错，不猜（PRD A17、R12）。
- Dependencies: Step 1
- Files: `hooks/completion-gate`、`hooks/smoke-test`
- Implementation checklist:
  - [x] **A16 已否决（2026-10-30，用户裁定）**：原计划的「Step 必须有验证记录」不实现。实测证明它被一行 `ok` 满足，且会拒掉 73/93 份归档 Plan。证据与推理在 `reject-a16.md`、`evidence-a16-fake-plan.md`
  - [x] 同一 Step 块出现两个 `- Status:` 行 → 报错，不猜（现在是读最后一个）
  - [x] **A15 的夹具**：同一个 `done` 的 Step，一行由 `progress` 写、一行手写，**两者都必须通过**
  - [x] **A18 的夹具**：`achieved/` 下的 Plan 不被新规则拒绝
- Acceptance: A15、A17、A18
- Verification: 上述夹具 + 变异（让第二个 `- Status:` 静默取胜 → 报错用例必须变红）
- Rollback: 还原 `completion-gate`
- Status: done

### Step 4 — `capability-gate` 解析 `apply_patch`

- Goal: Codex 的编辑能被门禁看见（PRD A11、Spec C1/C2）。
- Dependencies: Step 1
- Files: `hooks/capability-gate`、`hooks/smoke-test`
- Implementation checklist:
  - [x] `tool_name == "apply_patch"` 时从 `tool_input.command` 解析路径
  - [x] 四种指令：`*** Update File:` / `*** Add File:` / `*** Delete File:` / `*** Move to:`
  - [x] `Move to:` 产出**两个**路径：旧路径删除、新路径新增（Q6），两个都走判定
  - [x] 一条 patch 含多个文件时逐条判定，**任何一个被拒即整体 deny**
  - [x] 解析失败（command 非空但无任何 `*** … File:` 指令）→ deny，说明是 gate 问题
  - [x] 非 `apply_patch` 路径（`file_path`）行为逐字节不变

  实测修正三处：**① substr 偏移全部算错一位**（`*** Update File: ` 是 17 字符不是 18，四个指令各差一位），错位后读到不存在的路径、门禁静默放行；**② 相对路径必须在 `judge_path` 里 join event cwd**，否则 `[ -f "$task_dir/plan.md" ]` 相对 hook 进程 cwd 判断，patch 场景永远为假；**③ 反斜杠归一化也要在函数内**，否则 Windows 路径下 `base=` 取不到。三处都是"失败即放行"的形态。
- Acceptance: A11、Spec C2 的四种情况表
- Verification: 夹具覆盖四种指令 + 多文件 + 解析失败；变异（只处理第一个路径 → 多文件用例必须变红）
- Rollback: 还原解析分支
- Status: done

### Step 5 — `hooks-codex.json` 接上 `PreToolUse`

- Goal: Codex 上真的有门禁（PRD A12）。
- Dependencies: Step 4
- Files: `hooks/hooks-codex.json`、`hooks/smoke-test`、`skills/taskflow/references/runtime.md`
- Implementation checklist:
  - [x] 新增 `PreToolUse`，matcher `apply_patch`，命令走 `run-hook.cmd capability-gate`，并给 `commandWindows`
  - [x] **不接** `PostToolUse`/`apply_patch`（A12b、事实 12：`apply_patch` 不是能力，接上是静默无效）
  - [x] 替换 `smoke-test:5296-5301` 那条「禁止 Codex 接线」的断言为正向断言
  - [x] `runtime.md` 的 Codex 列按新规则写：原为 **not wired**，现改为已接线（documented，待实测）
- Acceptance: A12、A12b、A13
- Verification: smoke 在夹具上跑 Codex 的接线命令，必须 deny 一个未释放的 stage 文档
- Rollback: 还原 `hooks-codex.json` 与该断言
- Status: done

### Step 6 — 文档、CHANGELOG 与 PR

- Goal: 让改动可被发现、可被追溯。
- Dependencies: Step 2–5
- Files: `CHANGELOG.md`、`hooks/README.md`、`skills/taskflow/references/runtime.md`、`TaskFlowDocs/todo.md`
- Implementation checklist:
  - [x] `CHANGELOG.md` 记录三件事：Codex 门禁、审批判定、多重 Status 报错（原「Step 证据」已否决，改为记录否决）
  - [x] `runtime.md` 事件表：Codex 的 `PreToolUse` 行；并修正 `:55` 那句把「未实现」写成「宿主限制」的话（另补 `### Codex specifics`，此前三处引用指向不存在的章节）
  - [x] `hooks/README.md` 的宿主覆盖说明
  - [x] 按 `.github/pull_request_template.md` 填 PR 正文，逐字段映射（正文见 `pr-body.md`）
  - [x] `todo.md` 条目状态
- Acceptance: 文档与实现无冲突；PR 模板每个字段都有落点
- Verification: `bash hooks/release-check .`；`git diff --check`
- Rollback: 无需
- Status: done

## Checkpoints

- Step 1 后：`approval-check` 与旧内联逻辑在 93 份归档 Plan 上结论逐份一致。
- Step 3 后：A15 的「手写 Step 必须通过」用例为绿——**这是防止强制 `progress` 的唯一闸门**。
- Step 5 后：`bash hooks/smoke-test` 全绿，且 Codex 接线断言是正向的。
- Step 6 后：CI 六 job 全绿。

## Verification / Review

- 2026-10-30 **Review 复验（用户要求）：四个「失败即放行」的缺陷，全部实测复现后修复。** 前一轮 smoke 全绿，但绿的是我以为的路径。逐条驱动真实事件才看见它们：

  | # | 缺陷 | 触发条件 | 现象 |
  |---|---|---|---|
  | 1 | `set -- $patch_paths` 未加引号展开，按空格分词 | 路径含空格 | 一条路径裂成两条，两条各判各放行，该文档从未被检查 |
  | 2 | 提取路径未剥尾部 `\r` | **CRLF patch（Windows 常态）** | `base` 成为 `plan.md\r`，匹配不到任何 stage，`return 0` 放行 |
  | 3 | 释放与判定交错 | 多文件 patch，第二个路径被拒 | 整份被拒，但已写 `released` 行、已花证据；下次写该文档无记录也通过 |
  | 4 | `consumed` 在 `judge_path` 内每次重算 | 多文件 patch 都通过 | 两条释放行都取 seq 1 |

  第 2 条杀伤力最大：Codex 是 Windows 优先的宿主，CRLF 是默认行尾。不修则整个 Codex 门禁在真机上大概率等于没接——正是本任务要消灭的形态。

  **修法**：1、2 就地改；3、4 同一根因——判定与写入必须分离，释放行改为入队（`pending_release`），全部路径判完才落盘，`consumed` 预占序号并加 `store_loaded` 一次性守卫（否则每个路径重读文件、都看到同一最高序号）。实测确认：单路径写 1 行；双路径第二个被拒时 `released` **文件根本不创建**；双路径都通过时 seq 为 1、2。

  **变异验证**，每个都精确打红自己的断言：去掉 CR 剥离 → `FAIL a CRLF patch was allowed`；改回直接写 → `FAIL a patch whose second path had no evidence was allowed`；改回空格分词 → `FAIL a patch path containing a space was allowed`。

  **回归**：smoke `ALL SMOKE PASSED`、`release-check` `STATUS: pass`、`git diff --check` 干净、93 份归档 19 拒/74 过/0 分歧、`file_path` 六种事件形状与改动前逐字节一致。

  **过程中我自己犯的两个错**，记下来以免重犯：(a) 有一轮在 base checkout（`$PWD` 是 `/mnt/f/WorkSpace/Agent/TaskFlow`）上跑测试，把「那里根本没有我的改动」误判成「我把代码改坏了」，白查两轮——测试前应先 `pwd`。(b) `[ "$plan_only" -eq 1 ] && return 0` 在 `set -e` 下条件为假即函数退出；这个形状在 `completion-gate` 里已经踩过一次，又踩了一次，凡「测试成功才继续」一律用 `if`。

- 2026-10-30 Step 6: CHANGELOG 记 Codex 门禁/审批版本判定/多重 Status 三条（+ Compatibility 说明 5 字段 store 的一次性修复与 5 份归档不改）；runtime.md 事件表改 Codex 列、改写 gate 适用范围段、新增 ### Codex specifics（此前 Codex/dsh/CodeBuddy specifics 三处引用中 Codex 那节不存在）；hooks/README.md 补 Codex 接线说明；PR 正文按模板逐字段写入 pr-body.md。验证：smoke ALL SMOKE PASSED、release-check STATUS pass、git diff --check 干净

- 2026-10-30 Step 5: hooks-codex.json 接上 PreToolUse/apply_patch，命令走 bash "${PLUGIN_ROOT}/hooks/capability-gate" 并给 commandWindows；不接 PostToolUse（apply_patch 不是能力类，接了只 exit 0 不写记录）。smoke 把「禁止 Codex 接线」的旧断言换成执行式正向断言：从 JSON 读出命令、替换 PLUGIN_ROOT、喂真实 patch，断言 deny 未被门禁的文档且放行无关文件；并断言无 PostToolUse 段。变异：删掉 PreToolUse 段→断言报 'wires no capability-gate command'（首次尝试时 pipefail 让赋值静默退出、无消息，已加 || true 修好）。runtime.md 新增 Codex specifics 三小节并改写事件表与 gate 适用范围段。ALL SMOKE PASSED

- 2026-10-30 Step 4: capability-gate 支持 apply_patch：从 tool_input.command 解析四种指令；判定逻辑抽成 judge_path 函数供两条输入形状共用；任一路径被拒即整体 deny（deny 直接退出），全部通过才写释放行。实测修正三处失败即放行的缺陷：substr 偏移各错一位、相对路径未 join event cwd、反斜杠未归一化。file_path 形状 11 个用例与旧版逐字节一致，93 份归档零分歧。smoke 新增 8 条 patch 断言（四指令/多文件/无关/解析失败/空命令）；变异三次：只判第一个路径→multi-file 红，删除 Move to 分支→新增的 move-destination-only 红（原 move 用例靠 Update 行蒙对，已补），ALL SMOKE PASSED

- 2026-10-30 Step 3: A16 按用户裁定否决（实测：三行 ok 即通过，且拒 73/93 归档），记录在 reject-a16.md + evidence-a16-fake-plan.md；A17 实现：同一 Step 块第二个 - Status: 行报错并点名 Step 号，检查置于 unchecked/unfinished 之前；smoke 新增 7 条（多重 Status 两种顺序、跨块不算冲、指名 Step 3、progress 写与手写判定一致各一）；变异两次：去掉 dup 报错→multi-status-done-first 变红，改成必须有日期行→手写夹具变红；93 份归档零新增拒绝；ALL SMOKE PASSED

- 2026-10-30 Step 2: capability-gate 在 released 短路之前调 approval-check --stale-only，只拦「已批准版本 != 当前版本」；planning 阶段（Approved version 为 pending 或空）放行，直接验证避免死锁；smoke 新增 5 条断言（未审批放行/同版本放行/降级拒绝且点名两个要素/pending 放行/空值放行）；变异验证两次：去掉版本比对→降级用例变红，把 pending 也算版本→planning 用例变红；archive 侧 A9b 由既有 check_refusal 三元组覆盖，未改 archive

- 2026-10-30 Step 1: 取自 completion-gate:86-91/:110-111 原样搬出到 hooks/approval-check；93 份归档 Plan 上新旧结论连同 stderr 逐份一致（19 拒绝/74 通过，0 分歧）；补 --stale-only 模式供 capability-gate 用（planning 阶段放行写入，仅拦版本降级）；completion-gate 与 capability-gate 都改调它；smoke 补 rollback 夹具复制与两份 hook 清单；ALL SMOKE PASSED

## Change Log

- 2026-10-29 v1 — 初版 Plan；按用户裁定纳入 Codex 门禁（A12）、审批判定（A9）、Step 证据（A16–A18）；「中途在场加提示」被事实 4/5 降级，不再是主线

## Follow-ups

- **A14 真机验证**：用户在一台真实 Codex 机器上跑，必须覆盖 `*** Move to:`（Q6 的格式风险）
- **dsh 的门禁缺口**：按新规则记为 **not wired**，本任务不做
- **93 份归档 Plan 不重验**（R13）；若将来要回填，是独立任务

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-10-27 measured on this machine:** across the three most recent session transcripts, tool calls per user turn are median **10–15**, max **197**. `hooks/prompt-reminder` speaks once at the *start* of each turn (`hooks/hooks.json`, `UserPromptSubmit`), and nothing TaskFlow-owned fires for the remaining 10–197 calls. The user's report — "跑着跑着不走流程" — lands in that gap.
  **Four openings named at file:line** (each verified today): (1) `hooks/capability-gate:126-134` returns 0 once a stage is released for this task version, and only matches the basenames `prd.md`/`spec.md`/`plan.md` (`:96-99`), so **no edit after the first Plan write is checked at all**; (2) the gate never reads `## Approval` — recorded history has the failure happening (`achieved/2026-10-23-archive-completion-gate/plan.md:132`, "Steps 1–3 were implemented before the Approval block was filled"); (3) `hooks/task progress` is the only writer of Step status and is bound to **no hook**, so a Step's `- Status:` changes only if the Agent chooses to call it; (4) the record the gate depends on is largely absent — **59 of 91 achieved Plans have zero `## Skills / Tools Used` stage lines**, and 8 have no `## Change Log` section.
  **External evidence for the frequency lever, not for a new gate:** arXiv 2604.12147 (IBM, 21,120 SWE-agent trajectories, SWE-bench Verified + Pro) measures that re-inserting the plan **every five steps** reduces plan violations and raises success, attributing the drift to the plan losing influence as the trajectory grows. That is the same mechanism `prompt-reminder` already uses, at the wrong cadence.
  **Deliberately *not* proposed: extending the gate into the implementation phase.** It would convert a reminder problem into a new hard gate over ordinary refactoring edits, and the false-refusal cost is borne per edit. If it is ever wanted it needs its own evidence, not this item's.
  **Open question the design turns on:** whether a host's mid-turn hook can actually inject text the model reads. If none can, the lever is not a new hook at all but the Plan carrying the current Step where the turn-start reminder can restate it — a smaller change with the same effect at turn granularity only.
