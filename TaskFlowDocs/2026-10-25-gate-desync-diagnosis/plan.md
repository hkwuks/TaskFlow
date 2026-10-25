# Plan — 让 pre-write 门在 store 失步时说出真实原因
> Task version: v2
> Status: in_progress

No spec required — small, self-contained task: one brake in one hook, its wording, and the assertions that pin all three branches.

## Reference Pointers

- `hooks/capability-gate:126-162` —— 门的放行条件与两条写 `released` 的路径；本条只动 `:222-230` 的拒绝措辞。
- `hooks/task:1136-1144` —— `unaided` 里同一不变量的检查，新措辞的两个数字与它对齐，恢复路径与它不同（它只给「删掉重来」）。
- `skills/taskflow/references/runtime.md:63-77` —— store 的两个不变量与门已有的「拒绝时说真话」先例（跨工作树点名记录去向）。
- `hooks/smoke-test:2699-2790` —— 门的既有夹具与断言风格；新断言放在这一节内。
- `TaskFlowDocs/achieved/2026-10-24-test-phase-capability/prd.md` —— 上一个改动同一批 hook 的任务，`released` 的三个写者在那里定稿。

## Related Tasks

- `TF-20261025-ef6c18`（inbox，**子任务关系，方向：本条先做**）—— 让失步的 store 真正可恢复。本条只让门把话说对，不动写入语义；那条要设计恢复路径。两者改同一个 store，但本条不改任何写者，所以不冲突。
- `TF-20261009-8abbd6`（inbox）—— 把阶段能力选择与宿主工具流解耦，会动同一个门。本条是最小改动，不预设那条的结论。

## Skills / Tools Used

- [PRD] Unaided — v2 只把 R8 与 A6 加进既有的 R1–R7 / A1–A5，没有重新推导需求; considered: requirements elicitation and framing
- [Plan] Unaided — v2 在既有四步里给 Step 2 添一条 checklist，Steps 本身未改编排; considered: work breakdown and task decomposition
- [Test] Unaided — no capability applied to this phase; considered: testing strategy

v1 的 PRD 与 Plan 由 `agent-skills:spec-driven-development` 与 `agent-skills:planning-and-task-breakdown` 产出，记录在 `old/v1/version.md`。v2 的改动是范围扩展：第一轮 CI 之后发现 Windows 没覆盖失步分支，因此补 R8 / A6。**上面三行报的是 v2 实际发生的事**，不是把 v1 的调用沿用过来——`approve` 按 Task version 对账，沿用会让记录说一件没发生的事。

## Preconditions

- 在 `fix/gate-desync-diagnosis` 工作树内（`hooks/task promote` 已强制）。
- `TF-20261025-537a8a` 已 promote，Todo 指向本目录。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-25 20:13 +0800
- Approved version: v2
- Approved scope: PRD / Plan

## Steps

### Step 1 — 门：拒绝前先判断失步

- Goal: `hooks/capability-gate` 在 `total < consumed` 时走一条自己的拒绝消息，说出两个真实数字、真实原因，以及两条恢复路径与各自代价。其余两条措辞逐字节不变。
- Dependencies: 无。
- Files: `hooks/capability-gate`
- Implementation checklist:
  - [x] 在 `:222` 处、现有 `if [ "$consumed" -gt 0 ]` 之前插入失步分支，命中即 `deny` 并结束（`deny` 自带 `exit 0`），所以下面两条分支一个字都不用改。
  - [x] 消息含：`out of step`、`released reaches seq <consumer>`、`evidence holds <total> line(s)`、缺口条数 `consumed - total`、追平需要补 `consumed - total + 1` 条记录、以及「删掉 store 重来会丢掉 released 里的记录」。
  - [x] store 路径先 `tr '\134' '/'` 再嵌进消息：这条消息会原样进 JSON，Windows 的 `--absolute-git-dir` 带反斜杠，未归一化会破坏 JSON（`stray_evidence` 早已为此归一化，理由见其注释）。
  - [x] 消息里不出现双引号与反斜杠，保持 `deny()` 的前提。
  - [x] 注释写明：为什么这三分支必须分开（失步时「已被别的文档用掉」是假话——被用掉的 seq 没有对应记录），以及追平为什么在算术上可行（`released` 完好，`approve` 只读它）。
- Acceptance: A1、A2、A3、A4。
- Verification: 临时仓库手工跑三种 store 状态。旧门必须放在 `hooks/` 里再比——`HERE` 由 `$0` 推出，放到 `/tmp` 的副本在 `json-field` 处就退出，输出为空，会让 `cmp` 误报「相同」。实测结果：队列用尽 519 字节、空账本 510 字节、store 写入守卫、放行时 0 字节，四项与 `main` 逐字节相同；失步分支给出新消息。
- Rollback: `git checkout main -- hooks/capability-gate`。
- Status: done

### Step 2 — smoke：三个分支各一条断言

- Goal: 新增断言让三分支都被钉住，其中失步那条同时钉住「不再说假话」。
- Dependencies: Step 1。
- Files: `hooks/smoke-test`、`hooks/smoke-test-windows.ps1`
- Implementation checklist:
  - [x] 在既有 `== the pre-write gate releases a stage only against real evidence ==` 小节内、`cg_verdict` 系列之后新增一个独立 repository 夹具（既有 store 的释放计数被别的断言依赖，不能共用）。
  - [x] A1：`released` 到 seq 5 + 空 `evidence` → 消息含 `out of step`、`released reaches seq 5`、`evidence holds 0 line`，且**不含** `already spent by an earlier document`。
  - [x] A2：按消息给出的条数补 evidence 行，用循环补到门放行，断言补的行数等于消息里写的数（消息与实际不一致这条断言就会红）。
  - [x] A3/A4：同一夹具里造出 `total == consumed > 0` 与 `consumed == 0` 两种健康状态，断言消息里的 detail 原文不变。
  - [ ] **A6（CI 之后发现的缺口）：`hooks/smoke-test-windows.ps1` 也要覆盖失步分支。** 门把 `$store` 原样拼进消息，Windows 上 `--absolute-git-dir` 带反斜杠；bash 套件只跑正斜杠路径，同一份代码在那里静默正确。断言三点：消息能 `ConvertFrom-Json`、含 `out of step` 与两个数字、不再说「已被用掉」。夹具必须让 `released` 不覆盖被测阶段（用 `plan.md`）——门对被释放过的 `(version, stage)` 直接早退，失步检查根本走不到。
- Acceptance: A1–A4、A6 由断言覆盖。
- Verification: `bash hooks/smoke-test` 全绿；变异 8 项各自变红（见 `## Verification / Review`），每次用 `cp` 还原并 `cmp -s` 确认字节一致。**Windows 套件本地跑不了**（WSL 里没有 `pwsh`），只能靠 CI 的 `smoke (windows-latest)`——这一条在 Plan 里写明，不假装验证过。
- Rollback: `git checkout main -- hooks/smoke-test hooks/smoke-test-windows.ps1`。
- Status: done

### Step 3 — 文档：runtime.md 与 CHANGELOG

- Goal: 读者在 store 那一节能知道门也会这样诊断；CHANGELOG 记下修的是措辞而非语义。
- Dependencies: Step 1（措辞定稿后再写文档，避免文档描述一个中途变过的消息）。
- Files: `skills/taskflow/references/runtime.md`、`CHANGELOG.md`
- Implementation checklist:
  - [x] `runtime.md` 在 `:77` 那段「A denial says where the records went」之后追加一句：同一处拒绝也会区分失步，说出 `released` 的 seq 与 `evidence` 的行数，并给出两条恢复路径。写明这是报告，门仍然只在 `evidence > consumed` 时放行。
  - [x] `CHANGELOG.md` `[Unreleased]` → `### Fixed`：门在失步时不再把原因说成「调用已经被用掉」，并列出两个数字与两条路径；同时点名未失步的两条措辞未变。
- Acceptance: A3 文档侧——三处描述（门、`unaided`、`runtime.md`）对同一 store 状态的陈述不互相矛盾。
- Verification: 通读三处，确认「失步」「追平」「删掉重来」的说法一致；`git diff --check`。
- Rollback: `git checkout main -- skills/taskflow/references/runtime.md CHANGELOG.md`。
- Status: done

### Step 4 — 验证与落地

- Goal: A5 全绿，记录写进本 Plan，按 `CONTRIBUTING.md` 的顺序开 draft PR。
- Dependencies: Step 1–3。
- Files: 本 Plan、`TaskFlowDocs/todo.md`
- Implementation checklist:
  - [x] `bash hooks/smoke-test`、`bash hooks/release-check .`、`git diff --check`。
  - [ ] push 分支 → 读 CI → 把结果写进 `## Verification / Review` → 提交 → 归档 → 再提交 → 标记 ready。
  - [ ] `TF-20261025-537a8a` 随 `task complete` 置 done。
- Acceptance: A5。
- Verification: CI 7/7，URL 记进本 Plan。
- Rollback: 不合并即可；分支删除即回退。
- Status: in_progress

## Checkpoints

- [x] Step 1–2 之后：三分支的消息在手工夹具与 smoke 里一致。
- [x] Step 3 之后：文档与门的行为无矛盾。
- [ ] Step 4：CI 全绿后才标记 ready。

## Verification / Review

### 三分支的实际消息（临时仓库手工跑）

| store 状态 | 消息 | 与 `main` 比对 |
| --- | --- | --- |
| `released` seq 5 / `evidence` 0 行 | 新：`out of step` + 两个数字 + 缺口 5 + 追平需 6 条 + 删 store 丢记录 | 新分支，仅此处不同 |
| `released` seq 1 / `evidence` 1 行（队列用尽） | `the most recent invocation was already spent by an earlier document` | 519 字节，`cmp` 相同 |
| 空 store | `no capability invocation is recorded for this task version` | 510 字节，`cmp` 相同 |
| store 写入守卫 | `the capability store is not writable…` | `cmp` 相同 |
| 放行 | 无输出 | 0 字节，`cmp` 相同 |

**比对方法上的一个坑（已记在这里，避免下次重犯）**：旧门必须复制进 `hooks/` 再比。`HERE` 由 `$0` 推出，放在 `/tmp` 的副本找不到 `json-field`，在解析事件处就退出、输出为空——`cmp` 会把它报成「与新版相同」，看起来像通过。第一次比对就是这么错的。

### 变异（每一项都变红，还原后 `cmp -s` 字节一致）

| # | 改坏的地方 | 变红的断言 |
| --- | --- | --- |
| M1 | 用 `main` 的旧门 | `did not name an out-of-step store as such` |
| M2 | 追平条数写成缺口 `gap` 而不是 `gap + 1` | `kept denying after the 5 records it asked for` |
| M3 | 追平条数写成 `gap + 2` | `allowed after 6 of the 7 records it asked for` |
| M4 | 消息里塞回 `already spent by an earlier document` | `still reported as a spent invocation` |
| M5 | 去掉 `out of step` 字样 | `did not name an out-of-step store as such` |
| M6 | `-lt` 改成 `-le` | `a spent queue no longer says so` |
| M7 | 改「队列用尽」那句措辞 | `a spent queue no longer says so` |
| M8 | 改「空账本」那句措辞 | `an empty store no longer says so` |

**设计上的一处修正**：初版断言把追平条数写死成 `produce 6 more`，于是 M2/M3 先被形状断言拦住——它能过一条「形状对、数字错」的消息，也就没在测真正的东西。改成从消息里读出数字、再按该数字实际补记录并检查门是否恰好放行之后，M2 与 M3 分别落到「少补一条仍拒绝」「补够即放行」两条断言上，数字错了必然红。

### 本地

- `bash hooks/smoke-test` — `ALL SMOKE PASSED`，耗时约 6 分钟（含新增小节）。
- `bash hooks/release-check .` — `STATUS: pass`，版本 1.1.7 一致。
- `git diff --check` — 干净。
- `python3 -I <skill-creator>/scripts/quick_validate.py skills/taskflow` — `Skill is valid!`

### CI

[run 40191640310](https://github.com/hkwuks/TaskFlow/actions/runs/40191640310) @ `327bdfd` — **7/7 pass**：`changes` 6s、`evals` 7s、`release` 6s、`todo-merge-audit` 4s、`smoke (ubuntu-latest)` 21s、`smoke (macos-latest)` 43s、`smoke (windows-latest)` 39s。

**这一轮绿不能证明归一化生效，我一开始写错了。** Windows 那条 job 跑的是 `hooks/smoke-test-windows.ps1`，而它只断言门会 deny、消息里有逃生命令——没有一条碰过失步分支，也就从没读过新消息。真正会暴露反斜杠问题的是「把 `$store` 原样拼进 JSON」这条路径，而它只在 `total < consumed` 时走到。

补法（Step 2 追加）：在 Windows 套件里造一个失步 store，断言消息 parse 得开、含 `out of step`、含两个数字、且不再说「已被用掉」。这条只在 Windows 上有意义——bash 套件跑在正斜杠路径上，同一份代码在那里**静默正确**，测不出来。

## Change Log

- v1 — 任务建立，PRD 与 Plan 同批写完。
- v1 — Step 1–3 完成：门的三分支、8 项变异、`runtime.md` 与 `CHANGELOG` 同步。新增一处 Plan 内的设计修正（断言不该写死条数）。
- v2 — **Task-version 提升**，原因：v1 的验收条件没有覆盖 Windows。第一轮 CI 7/7 之后发现 `smoke (windows-latest)` 跑的是 `hooks/smoke-test-windows.ps1`，其中没有任何断言进入失步分支——于是「反斜杠会破坏 JSON」这个本任务最需要 Windows 证实的点，恰好没被验证。v1 的 R1–R7 / A1–A5 一字未改，新增 R8 / A6 与 `hooks/smoke-test-windows.ps1` 的范围。

## Follow-ups

- 门的 class 表 `stage_class()` 是 `SKILL.md` 阶段表的手抄子集（PRD 格少 `divergent exploration`），`smoke-test` 没有比较这两份表。属 `TF-20261009-8abbd6`，本任务不碰。

## Version History

- v1 — planning，Approval 由用户 2026-10-25 给出。
- v2 — 提升以纳入 Windows 覆盖（R8 / A6）；其余需求与验收条件不变。
