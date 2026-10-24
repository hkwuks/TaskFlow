# Plan — 参考资料增强：任务执行期把部分资料带回注意力

> Task version: v1
> Status: checking

No spec required — 小且自洽的任务：一个钩子多印一行、一条断言段、三份文档说明与模板。没有跨层契约，没有数据结构变更，没有兼容性决策。

## Reference Pointers

- `skills/taskflow/references/runtime.md` — `prompt-reminder` 的输出契约写在这里，Step 1 的实现与 Step 2 的文档必须逐条对齐；改了一边没改另一边不会让任何断言变红。
- [Reinforce] `skills/taskflow/references/runtime.md` — 实现与文档必须描述同一个契约，而两者的偏离不会被任何测试抓住。
- `hooks/smoke-test` 的 `prompt-reminder` 断言段 — 新增断言沿用它的形状（`rem_silent` / `write_rem_plan` 那套）。
- `TaskFlowDocs/repository-docs/index.md` — 已确认 Phases 列不承载「任务中重读」，本任务不改它。

## Related Tasks

- `TaskFlowDocs/achieved/2026-09-08-runtime-hooks/` — `prompt-reminder` 的出处。
- `TF-20261009-887511`（inbox）— 同一类问题：规则写了但不生效。本任务不处理它，只处理「资料读了一次就再没回来」这一种。
- `TF-20261022-47c217`（inbox）— 审批前复核 Plan。本任务是它的下游：Plan 里的标记要靠那次复核才有人看。

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — purpose: 把「哪些资料值得每轮带回」从直觉变成可当场回答的判据与可测的验收条件；outcome: succeeded; incorporated: 三条判据（跨 Step / 违反时无声 / 代码无从表达）与「不做自动判定」的边界，以及 A1–A6 的可测措辞。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 把改动拆成三个各自可验证的 Step 并排出依赖；outcome: succeeded; incorporated: 三步拆分（钩子+断言 / 三份文档 / CHANGELOG 与整体验证）与两个检查点。

## Preconditions

- [x] 适用仓库文档已读：`TaskFlowDocs/repository-docs/index.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`、`skills/taskflow/references/runtime.md`、`artifacts.md`、`hooks/README.md`。无冲突，无需新建仓库文档。
- [x] 远程/PR 前置：单 remote `origin` = `hkwuks/TaskFlow`，base `main`，分支 `chore/reference-reinforce` 从 `main@165bb0e` 创建；PR 模板 `.github/pull_request_template.md` 已读，按 Summary / TaskFlow traceability / Verification / Review boundaries / Notes for review 填写。
- [x] 无 personal rule（`TaskFlowDocs/repository-docs/personal.md` 不存在）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-24 21:35 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — `prompt-reminder` 输出 Reinforce 行，并由 smoke 断言

- Goal: `hooks/prompt-reminder` 在已经输出时，多印一行 `- Reinforce while this task runs: <a>, <b>`，位置在任务行之后、分类问题之前；`hooks/smoke-test` 断言 A1–A6。
- Dependencies: 无。
- Files: `hooks/prompt-reminder`, `hooks/smoke-test`.
- Implementation checklist:
  - [x] 从 `summarize-state` 已给出的那一行里取出任务目录名，不再另做一次状态推导。
  - [x] 读 `<worktree>/TaskFlowDocs/<task>/plan.md` 的 `## Reference Pointers` 段，只在该段内取 `- [Reinforce] \`<path>\` — <reason>` 行。
  - [x] 三条同时成立才收：行首标记、理由非空、路径是仓库内相对路径；URL / `../` / 绝对路径一律跳过。
  - [x] 收下的条目再按存在性分开：存在的正常列出，不存在的带 `MISSING:` 前缀印在同一行；全部缺失时该行仍输出。
  - [x] 一条都没收下时不输出该行，现有三行逐字节不变。
  - [x] smoke 增加断言：A1 顺序与内容、A2 无理由/无标记的退化、A3 缺失标 `MISSING:`、A4 全缺失仍输出、A5 URL 与 `../` 不进任何一类、A6 静默契约不变。
  - [x] 变异验证：逐条改坏，确认每条断言真的会红。
- Acceptance: A1–A7。
- Verification: `bash hooks/smoke-test`；`bash -n hooks/prompt-reminder`。
- Rollback: `git checkout -- hooks/prompt-reminder hooks/smoke-test`。
- Status: done

### Step 2 — 把判据写进三份文档

- Goal: R6。谁标记、怎么标记、怎么判定哪些该标记、哪些不该（不重要 / 未验证 / 错误），以及钩子不判对错的边界，都写在读者会去的地方。
- Dependencies: Step 1 定下实现，文档描述的是它。
- Files: `hooks/README.md`, `skills/taskflow/references/runtime.md`, `skills/taskflow/references/artifacts.md`.
- Implementation checklist:
  - [x] `artifacts.md` 的 Plan 模板在 `## Reference Pointers` 下给出这一行的形状与三条判据。
  - [x] `runtime.md` 在 `prompt-reminder` 的段落里补上这条输出，并说明它读的是 Plan 而不是第二次状态推导。
  - [x] `hooks/README.md` 的 `prompt-reminder` 条目补上同一句契约。
  - [x] 三处都写明：标记由写 Plan 的 Agent 打、由审批的人复核；钩子只判「是否每轮带回」，不判资料对错。
  - [x] 三处都写明判据：跨 Step 生效、违反时无声、代码里无从表达。列出一个反例（已被 smoke 强制的规则不需要标记）。
  - [x] 三处都写明资料失效的两条现成路径：文件消失会以 `MISSING:` 显示；发现内容与实现冲突时，按 User-change trigger 当作 work revision 改文档并记 Change Log 一行，若推翻已批准需求才是版本变更。
- Acceptance: R6 达成；三处措辞不互相矛盾。
- Verification: `grep -n 'Reinforce' hooks/README.md skills/taskflow/references/runtime.md skills/taskflow/references/artifacts.md` 三处命中且语义一致；`bash hooks/smoke-test`。
- Rollback: `git checkout -- hooks/README.md skills/taskflow/references/runtime.md skills/taskflow/references/artifacts.md`。
- Status: done

### Step 3 — CHANGELOG 与整体验证

- Goal: 记录变更并跑完整验证。
- Dependencies: Step 1、Step 2。
- Files: `CHANGELOG.md`, `TaskFlowDocs/todo.md`.
- Implementation checklist:
  - [x] `CHANGELOG.md` 在 `## [Unreleased]` 下加条目。
  - [x] 跑 `bash hooks/smoke-test`、`bash hooks/release-check .`、`git diff --check`。
  - [x] 结果写进 `## Verification / Review`。
- Acceptance: A7、A8。
- Verification: 三条命令全部通过。
- Rollback: `git checkout -- CHANGELOG.md`。
- Status: done

## Checkpoints

- Step 1 后：`bash hooks/smoke-test` 全绿；手工跑一次带两条标记的夹具，确认输出顺序是「任务行 → Reinforce 行 → 分类问题」。
- Step 2 后：三份文档对同一条契约的描述一致，且都带判据与反例。
- Step 3 后：`release-check` 与 `git diff --check` 干净。

## Verification / Review

本机于 2026-10-24 在 `.worktrees/reference-reinforce`（`chore/reference-reinforce`，基线 `main@165bb0e`）上跑：

| 命令 | 结果 |
| --- | --- |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED`，exit 0，约 33s |
| `bash hooks/release-check .` | `STATUS: pass` |
| `git diff --check` | 干净 |
| `bash -n hooks/prompt-reminder hooks/smoke-test` | 通过 |

CI（PR #95，`Hooks` workflow）：

| 提交 | run | 结果 |
| --- | --- | --- |
| `25ebc32` feat: bring declared reference material back on every prompt | `40101708275` | 7/7 pass（`smoke` ubuntu 23s / macos 37s / windows 38s；`release`、`evals`、`changes`、`todo-merge-audit` 全 pass） |
| `4153438` docs: state all four admission conditions in the hook header | `40101836982` | 7/7 pass（`smoke` ubuntu 19s / macos 41s / windows 32s） |

### 验收对照

| AC | 断言 | 位置 |
| --- | --- | --- |
| A1 | Reinforce 行是第 2 行、按 Plan 顺序、第 3 行仍是分类问题、第 1 行与基线一致 | `smoke-test` 的 `prompt-reminder carries the material…` 段 |
| A2 | 无理由条目不进；删掉最后一条后输出与基线逐字节相同 | 同上 |
| A3 | 缺失路径印成 `MISSING: <path>`，其余照常 | 同上 |
| A4 | 全部缺失时该行仍输出（只含 `MISSING:`） | 同上 |
| A5 | URL / `../` / 绝对路径既不列出也不标 `MISSING:` | 同上 |
| A6 | `planning`/`ready`、两个 active 任务、仓库外 cwd 静默契约不变 | 既有的 `prompt-reminder is silent…` 段，未改动且仍绿 |
| A7 | 套件通过且含上述断言 | 上表第 1 行 |
| A8 | `release-check` 通过 | 上表第 2 行 |

补充一条 AC 之外的断言：**未标记的普通 bullet 不得混入**。变异验证时发现原实现（只认 `[Reinforce]` 行首）与「任何 bullet 都收」在任何既有断言下都无法区分，`- docs/rule.md — r` 会被当成指针收进去。该断言已补进同一段。

另补两条：**缺收尾反引号**与**没有分隔符**必须丢弃。边界扫描发现修订前的解析在缺收尾反引号时会把整行当成路径、把理由当成「消失的资料」报出来 —— 一条畸形的声明被读成了一条真实的事实，比不收更糟。两条断言共用一条规则（收尾定界符靠分隔符确定，不靠猜），一次变异能同时推翻两者。

### 变异验证

逐条改坏 `hooks/prompt-reminder`、跑套件、再还原（`cp` 回原文件并由 `diff -q` 确认逐字节相同）：

| # | 故意改坏 | 结果 |
| --- | --- | --- |
| M1 | 允许无理由的条目 | `FAIL a reason-less entry was admitted` |
| M2 | 缺失条目不标 `MISSING:`（退回静默丢弃） | `FAIL a missing pointer was dropped or not marked` |
| M4 | 越过 `## Reference Pointers` 段边界继续解析 | `FAIL a marker outside Reference Pointers was admitted` |
| M5 | 不排斥 URL / 绝对路径 / `../` | `FAIL an unverifiable pointer reached the output` |
| M6 | 一条都没收下也照样输出该行 | `FAIL an undeclared Plan changed the reminder's line count` |
| M7 | 把该行移到分类问题之后 | `FAIL reinforce line is not the second line or not in Plan order` |
| M9 | 分隔符 `—` 改为可选 | `FAIL an entry with no closing backtick was parsed as a pointer` |
| M9b | 同上（保留 `—` 剥离但不定为必需） | `FAIL an entry with no closing backtick was parsed as a pointer` |

M3（放开标记只收普通 bullet 的一半）在修订前的代码上单独改坏会被 A1 先咬住而不是自己那条断言咬住，说明「普通 bullet 混入」这条路径当时没有独立断言 —— 已补。

### 边界输入扫描（bash 3.2 容器内）

用 `docker run --rm bash:3.2` 跑端到端，确认 3.2 + busybox awk 下行为与 Linux bash 5 一致：

| 输入 | 结果 |
| --- | --- |
| 路径含空格 | 正常列出 |
| 路径含反引号 | 丢弃（不报告） |
| 缺收尾反引号 | 丢弃（修订前误报为 `MISSING: docs/a.md — <理由>`） |
| 缺起始反引号 | 丢弃 |
| 理由含 em dash | 正常，理由按首个 `—` 之后整段取 |
| 理由只有空白 | 丢弃 |
| 完全没有分隔符 | 丢弃（修订前被收下） |
| 路径后有尾随空格 | 正常 |
| Windows 反斜杠路径 | 报 `MISSING:`（文件确实不存在），非误报 |
| CRLF 行尾 | 正常 —— 反引号紧跟 `\r` 仍被当作收尾 |

后两条不改：`cat -A` 显示 3.2 下 CRLF 行的路径没有尾随 `\r`，反引号把 `\r` 挡在外面；反斜杠路径在 Linux 上确实解析不到，报 `MISSING:` 是准确的事实陈述而不是缺陷。

### 一次自伤，已复原

清点 Step 1 的 checkbox 时误用了 `sed -n '45,54s/…/' file > tmp && cp tmp file` —— 范围打印把 Plan 截成 0 行。已按原内容重建，并由 `wc -l`（116 行 / 82 行）与全套件重跑确认无残留。同批 `sed -i` 变异没有还原成功时也由 `diff -q` 抓出并 `cp` 复原，`hooks/prompt-reminder` 现与 pristine 实现逐字节相同。记录在此，因为这类操作不该悄悄过去。

## Change Log

- 2026-10-24 v1 — 建 Plan。
- 2026-10-24 用户评审追问后修订 PRD：缺失路径改为 `MISSING:` 报告而非静默丢弃（R4、A3、A4）；影响 `prd.md`、`plan.md`。
- 2026-10-24 Step 1 完成，并补一条「未标记的普通 bullet 不得混入」的断言（变异验证发现该路径原本没有断言）；影响 `hooks/prompt-reminder`、`hooks/smoke-test`。
- 2026-10-24 一次 `sed -n '45,54s/.../' file > tmp && cp tmp file` 误把本 Plan 清空，按已写内容重建并复原；内容与清空前一致，非用户改动。影响 `plan.md`。
- 2026-10-24 边界扫描（bash 3.2 容器）发现两处解析错误并修正：缺收尾反引号被当成指针、缺分隔符被当成指针；同一根因是收尾定界符靠猜。改为要求分隔符，并补两条断言与 M9/M9b 变异。影响 `hooks/prompt-reminder`、`hooks/smoke-test`、`plan.md`。

## Follow-ups

- 外部资料（URL、其他仓库）的支持需要先有可验证的存在性来源，目前不做。
- 若单份 Plan 的 Reference Pointers 涨到数十 KB，改为只解析 `[Reinforce]` 行而非整段。
- **仓库文档本身写错**（`CONTRIBUTING.md` 之类）不在本任务范围：那是独立 deliverable，另立任务。本任务只保证「某条 Reinforce 指向的资料消失」会被看见，不检查资料内容是否正确。

## Version History

- v1 — planning.
