# Plan — 修复 TaskFlow hooks 的四处遗留缺陷
> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/achieved/2026-09-15-hook-integrity/plan.md` 的 `## Follow-ups` —— 四条缺陷的原始实测记录。只读历史，本任务不修改它。
- `skills/taskflow/references/runtime.md` —— hook 的运行时底线（bash 3.2 + BSD userland，awk/sed 做文本工作，无语言运行时），第 1 处的实现必须守这条线。

## Related Tasks

- Depends on: `TaskFlowDocs/achieved/2026-09-15-hook-integrity/` —— 四条缺陷由该任务实测发现并记为 follow-up。该任务已归档，交付物是语言规则收窄，与本次不同，因此不重开、不版本化。
- Blocks: None
- Related: None

## Skills / Tools Used

- [PRD] Unaided — 需求来自已归档 Plan 记录的四条实测事实、当前 base 上的代码复读，以及用户对三处设计决定的裁定，没有需要外部能力才能确定的部分；considered: requirements elicitation and framing
- [Plan] Unaided — 工作分解由四条缺陷各自的独立修复点直接给出，不涉及需要方法学输入的设计；considered: work breakdown and task decomposition

## Preconditions

- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded. —— 读了 `CONTRIBUTING.md`、`CODE_STYLE.md`、`.github/pull_request_template.md`、`TaskFlowDocs/repository-docs/index.md`（无 personal rule）。仓库文档优先，本次无冲突。
- [x] For remote/fork/PR work: remotes, target repository, base branch, local branch/base, freshness limits, and required checks recorded. —— `origin` = `https://github.com/hkwuks/TaskFlow.git`；target = `hkwuks/TaskFlow`；base = `main` @ `f5ce0a4`；本分支 `fix/2026-09-29-hook-defect-followups` 从 `origin/main` 切出，无额外 remote。远端跟踪数据在 `git fetch origin` 时点有效。
- [x] For PR creation/update: applicable template path, every required-field mapping, and template verification recorded. —— 见下方 `## Pre-PR checks and template mapping`。
- [x] Missing governance drafts and explicit approvals recorded before they become binding. —— 本次不需要新建仓库文档。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-29 22:16 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 标题截断收在字符边界

- Goal: R1 / AC1 —— `todo.md` 的标题不再出现非法 UTF-8。
- Dependencies: None
- Files: `hooks/task`、`hooks/smoke-test`
- Implementation checklist:
  - [x] 在 `TASK_AWK` 的 `BEGIN` 里建单字节值表：`for (i = 1; i < 256; i++) ord[sprintf("%c", i)] = i`。
  - [x] 加 `cutbytes(s, max)`：从位置 1 前向扫描，按前导字节推出该字符长度（<128→1，<224→2，<240→3，否则 4），放不下就停在上一个边界，返回 `substr(s, 1, i - 1)`。
  - [x] `intake` 分支把 `title = substr(t, 1, 80)` 换成 `title = cutbytes(t, 80)`；`sub(/\.+$/, "", t)` 保持在前。
  - [x] `hooks/smoke-test` 补断言：>80 字节的中文 goal，标题行是有效 UTF-8（无孤立前导/续接字节）；同一 fixture 的 ASCII goal 标题与改动前逐字节相同。
- Acceptance: AC1 —— 中文 goal 的标题能通过 UTF-8 校验，ASCII 结果不变。
- Verification: 抽出该 smoke 段单独运行，并对照改动前的 `git stash` 输出。
- Rollback: 还原 `hooks/task` 的 `intake` 分支与 `TASK_AWK` 里新增的两个函数。
- Status: done

### Step 2 — Owner 取宿主实际 agent

- Goal: R2 / AC2 —— 新条目不再记成 Codex。
- Dependencies: None
- Files: `hooks/task`、`hooks/smoke-test`
- Implementation checklist:
  - [x] 在 `intake` 分支的 awk 调用前，镜像 `hooks/session-record:82-93` 的判定（`AI_AGENT`、`CLAUDECODE` / `CLAUDE_CODE_SESSION_ID`、`CODEX_HOME` / `CODEX_SANDBOX`），得到 `Claude` / `Codex`，都不是则 `Unknown`。注意 `set -u`，取值一律用 `:-`。
  - [x] 经环境变量传进 awk（沿用本脚本"参数走环境不走 -v"的约定），`blk[nb] = "- Owner: " owner`。
  - [x] `hooks/smoke-test` 补断言：三种环境各一例（`CLAUDE_CODE_SESSION_ID` → `Claude`，`CODEX_HOME` → `Codex`，清空全部宿主标记 → `Unknown`），每例都先 `env -u` 掉全部宿主变量再设被测的那一个，因此三个结果互不掩盖。
- Acceptance: AC2 —— 宿主可识别时记真实 agent，否则记 `Unknown`，任何情况下不再写死。
- Verification: 抽出该 smoke 段单独运行。
- Rollback: 还原为字面量 `- Owner: Codex`（即回到改动前）。
- Status: done

### Step 3 — 核验行 fail closed

- Goal: R3 / AC3 —— `## Verification / Review` 找不到时不再静默丢掉核验行。
- Dependencies: None
- Files: `hooks/task`、`hooks/smoke-test`
- Implementation checklist:
  - [x] `step` 分支的插入循环加 `found` 标记；循环结束仍未命中时 `die("missing ## Verification / Review section; verification not recorded")`。
  - [x] 不改其他分支的宽容行为（`## Change Log` 等不在本次范围）。
  - [x] `hooks/smoke-test` 把现有"译名标题的核验行没有落入"那条断言，扩成三件事：命令非零退出、报错文字点出缺失的段名、`plan.md` 摘要不变。
- Acceptance: AC3 —— 非零退出且 Plan 不被修改。
- Verification: 抽出该 smoke 段单独运行；`run_awk_to` 的临时文件路径保证原子性，用 `cmp` 前后对比证明。
- Rollback: 删掉 `found` 判定与 `die` 调用。
- Status: done

### Step 4 — 路由记录不承载本地态

- Goal: R4 / R5 / AC4 —— `index.md` 只写受跟踪事实，personal 的存在性走本地通道。
- Dependencies: None
- Files: `hooks/repository-docs-context`、`hooks/smoke-test`、`skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`TaskFlowDocs/repository-docs/index.md`
- Implementation checklist:
  - [x] 去掉 `:78-81` 的 `[ -f "$docs/personal.md" ]` 包裹：`personal-rule` 行恒定加入 entries。
  - [x] 派生循环里对 `personal-rule` 特判，`Exists` 列固定写 `local`，不再读文件系统。
  - [x] `:256-260` 的 `Status: present` / `not present` 换成恒定文字：说明该行是路由位置，本 clone 是否真有 personal 规则由会话路由行报出，此文件受跟踪因而不承载它。
  - [x] 路由段（`:292-297`）只在 `$repo_root/$relative` 存在时输出 `- Local personal rules …` 行，让存在性走本地通道。
  - [x] 重新生成受跟踪的 `TaskFlowDocs/repository-docs/index.md`（正常变更：多出恒定的 personal-rule 行）。
  - [x] `hooks/smoke-test:296-339` 改写：断言新行的恒定文本；断言"有 personal.md / 删掉 personal.md"两次渲染的 `index.md` 字节相同（替换现在 `:333` 的"行消失"断言）；断言 stdout 路由行只在文件存在时出现。
  - [x] `skills/taskflow/SKILL.md:79`、`skills/taskflow/references/artifacts.md:11` 按 R4/R5 改写关于 personal-rule 存在性的措辞；连带改 `SKILL.md:106` 的"catalog picks it up"与 `:108` 的"removing the file removes it from the catalog"，两处都因同一原因变得不成立。
- Acceptance: AC4 —— 两种状态下 `index.md` 字节一致且都含该行；stdout 行随文件存在与否出现/消失。
- Verification: 抽出该 smoke 段单独运行。
- Rollback: 还原 `hooks/repository-docs-context` 的三处判定与 `index.md`。
- Status: done

## Pre-PR checks and template mapping

模板：`.github/pull_request_template.md`（`pr` 阶段路由，见 `repository-docs/index.md`）。字段映射：

| 模板字段 | 来源 |
| --- | --- |
| `## Summary` | PRD 的 Goal 与四处缺陷各自的"现状 → 修复后" |
| `## TaskFlow traceability` → Task / Scope / Base branch / Target repository | `TaskFlowDocs/2026-09-29-hook-defect-followups/`；PRD 的 In Scope；`main`；`hkwuks/TaskFlow` |
| `## Verification` 四个 checkbox | 下面的 `## Verification / Review` 逐条对应，未跑的写明原因与替代 |
| `## Review boundaries` 四项 | 无 secret；diff 只含 In Scope 列的文件；remote/base 假设已写；Known limitations 指向 PRD 的 Risks 与本 Plan 的 Follow-ups |

## Checkpoints

## Verification / Review

- 2026-09-29 Step 4: smoke section 'repository document index sync and phase routing' green new, red on HEAD; tracked index.md digest identical with and without personal.md

- 2026-09-29 Step 3: smoke section 'a heading the language rule leaves as prose is free to be translated' now asserts nonzero exit + unchanged Plan; green new, red on HEAD (which exited 0)

- 2026-09-29 Step 2: smoke section 'a Todo entry names the host that created it as its owner' green new, red on HEAD (Owner: Codex literal)

- 2026-09-29 Step 1: smoke section 'a Todo title is cut on a character boundary' green on the new hook, red on HEAD's (the goal's 80th byte is mid-character)

- 本地能跑的 smoke 段落全部通过：`hooks/smoke-test` 的解析段、`summarize-state` 段，以及第 146 行起到文件结尾的全部段落（逐字抽出成独立脚本运行，末行 `ALL SMOKE PASSED`，含 todo ID 确定性、intake 插入位置、`task next`/`get`/`remove`、capability gate、release-check）。三处新断言都做了正反两跑：新 hook 绿、`HEAD` 的 hook 红。
- 本机两处失败与本次改动无关，且基线同样失败：`hooks run with no interpreter available` 段在 MSYS 上以 `error while loading shared libraries` 中止；隔离段的 `a drive-path absolute git dir was read as relative to the root` 断言在 `HEAD` 的 `task` 上同样失败（已实测对照）。整卷以 CI 为准。
- `git diff --check` 干净。
- `PYTHONUTF8=1 python3.12 /c/Users/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/taskflow` → `Skill is valid!`。
- AC4 除 smoke 断言外另做手工对照：同一仓库在有 `personal.md`、无 `personal.md` 两种状态下渲染，`index.md` 摘要均为 `dcc6968…`，且 `- Local personal rules …` 只在文件存在时出现。
- 环境限制：本会话加载的插件是 1.1.0，1.1.1 的 `PreToolUse` gate 未触发，因此 `v1|PRD|1|unaided|…` 与 `v1|Plan|2|unaided|…` 两条 release 记录由仓库自己的 `hooks/capability-gate` 配一条真实形状的 `PreToolUse` 事件产生，而不是宿主自动写入。两条 `unaided` 声明本身是真实的，`hooks/task unaided` 也确实写了证据行。

## Change Log

- 2026-09-29 v1 — 四处修复实现完毕，PRD 的 R1–R8 全部落地，未越出 In Scope。`hooks/smoke-test` 新增三段断言（标题字符边界、Owner 宿主判定、路由记录本地态），并把"译名标题的核验行没有落入"那条扩成"非零退出 + Plan 摘要不变"。`CHANGELOG.md` 记入 `## [Unreleased]` 的 Changed 与 Fixed。
- 2026-09-29 v1 — 手工把本任务自己的 Todo 条目的 `- Owner:` 从 `Codex` 改为 `Claude`：该条目是今天由修复前的 hook 建立的，不属于 Out of Scope 所指的历史条目；把已知为假的值留在修复它的那个 diff 里自相矛盾。同时把已过期的 Next action 更新为下一步。

## Follow-ups

- `hooks/task` 的宿主判定与 `hooks/session-record:82-93` 重复（D4 的代价）。抽 `hooks/agent-id` 会让本次改动扩散到一个当前正常的 hook，故未做；新增宿主时需要改两处。
- `CHANGELOG.md` 的 `## [1.1.0]` 条目仍写着 index 会 "marks the file present or not present"。已发布段落的正文不追溯改写，本次变化记在 `## [Unreleased]`。
- 归档 Plan 记录的"标题本地化"（语言声明放 `personal.md`、由 hook 执行）仍未做：需要先修订 v1 批准的"不引入语言探测/i18n"排除项，是独立的实质性变更。
- `hooks/task stop` 之外的静默路径未审：本次只让核验行 fail closed，其它段若被改名行为不变。

## Version History

- v1 — planning.
