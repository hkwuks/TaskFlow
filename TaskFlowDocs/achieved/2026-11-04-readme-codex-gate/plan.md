# Plan — 文档里关于「哪些宿主接了写前门」的陈述全线对齐
> Task version: v1
> Status: completed

No spec required — 纯文档修正，改动限于四份文档的既有段落，无接口或契约变化。

## Reference Pointers

- `hooks/hooks-codex.json:27-49` — Codex 实际接线：`PreToolUse`（`apply_patch` → `capability-gate`）、`PostToolUse`（无 matcher → `external-evidence`），无 `capability-evidence`。
- `hooks/capability-gate:60-68`、`:84-128` — 补丁文本读取与四类指令提取。
- `hooks/smoke-test:6540-6552` — 钉住「Codex 不接 capability-evidence」的既有断言。
- `skills/taskflow/references/runtime.md:50-52`、`:81`、`:112-144` — 已经正确的三行与 Codex specifics，作为改写其他段落的基准措辞。
- `hooks/README.md:105-109` — 已经正确的 manifest 说明，与 `:250-255` 矛盾的那一处以其为准。

## Related Tasks

无。

## Skills / Tools Used

- [PRD] invoke `Explore`（子代理）— purpose: 独立审计全仓库「哪些宿主接了写前门」的陈述，避免只修被 Todo 点到的那两句；outcome: 找到 11 处过时/残缺陈述、12 组互相矛盾，并确认 Codex 有门但无 `capability-evidence`；incorporated: PRD 的 Background 清单、R1-R4、R8。
- [Plan] invoke `agent-skills:planning-and-task-breakdown` — purpose: 把 11 处改动拆成按文件分组的可验证 Step；outcome: 五步（runtime.md → hooks/README.md → 两份 README → smoke 注释 → 全局复核），每步带 grep 级验证；incorporated: 下方 Steps。
- [Test] Unaided — testing strategy; considered: testing strategy. 验证是 grep 断言与既有 smoke 套件，没有值得单独调用的测试设计能力。

## Preconditions

- 处于任务 worktree `.worktrees/readme-codex-gate`，分支 `docs/readme-codex-gate`。
- 以 `runtime.md:50-52` 与 `hooks/README.md:105-109` 为准绳；任何改写都先与其对齐。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-04 22:19 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — runtime.md 内部一致性

- Goal: `runtime.md` 不再自相矛盾。
- Dependencies: 无。
- Files: `skills/taskflow/references/runtime.md`。
- Implementation checklist:
  - [x] `:99` 的门宿主句补上 Codex 的 `apply_patch` 形状，并点明 Codex 不接 recorder。
  - [x] `:286` 「the Claude Code pre-write gate」改为四宿主表述。
  - [x] `:359` 目录树注释补全四个事件块。
  - [x] `:143-144` 删除「Codex's capability records come from Skill and MCP calls」的误导，改为「Codex 一条都不记」。
  - [x] `:179-180` dsh 的 `SessionStart only` 改为「无 tool-call 事件（SessionStart 与 UserPromptSubmit）」。
  - [x] `:87` 的 `PreToolUse` on `Write|Edit` 补上 `apply_patch` 形状。
- Acceptance: AC4。
- Verification: 通读改后段落，确认与 `:50`/`:81` 无冲突。
- Rollback: `git checkout -- skills/taskflow/references/runtime.md`。
- Status: done

### Step 2 — hooks/README.md 内部一致性

- Goal: 同一个文件里不再出现「Codex 接了」与「Codex 没接」并存。
- Dependencies: Step 1（措辞基准已定）。
- Files: `hooks/README.md`。
- Implementation checklist:
  - [x] `:22`、`:24` 的 `(Claude Code only)` 改为真实宿主列表。
  - [x] `:233-234` 把「gate 对」拆成「recorder 三宿主 + gate 四宿主」。
  - [x] `:250-255` 「Neither is wired」改写为「两种输入形状」框架，Codex 按第二种已接，只剩 dsh 未接。
  - [x] `:23` 的 `external-evidence` 宿主说明排除 dsh。
- Acceptance: AC3。
- Verification: 逐行比对 `:105-109`，确认无矛盾。
- Rollback: `git checkout -- hooks/README.md`。
- Status: done

### Step 3 — 两份 README 的 Codex 段与 hook 协作段

- Goal: 读者在 Codex 安装完成后不会被误导去「先调能力再写文档」。
- Dependencies: Step 1、Step 2（措辞已定稿，避免三次返工）。
- Files: `README.md`、`README.zh-CN.md`。
- Implementation checklist:
  - [x] `README.md:229` 改为列出 Codex 四个事件，保留「documented, not yet measured」限定，并加「Codex 不记录能力调用 → 用 `unaided` 释放阶段」。
  - [x] `README.md:124`、`:126` 把门与 recorder 分开陈述，门含 Codex。
  - [x] `README.zh-CN.md:195`、`:91`、`:93` 逐段对应改写，能力名与命令保留英文。
- Acceptance: AC1、AC2、AC5。
- Verification: 中英逐段对照；`grep` 无 `SessionStart only` / `只接 SessionStart`。
- Rollback: `git checkout -- README.md README.zh-CN.md`。
- Status: done

### Step 4 — smoke 注释

- Goal: 注释不再说「两个宿主未接」。
- Dependencies: Step 2。
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] `:6414-6415` 注释改为单数（只剩 dsh）。
  - [x] 不改任何断言逻辑。
- Acceptance: AC6。
- Verification: `bash hooks/smoke-test`。
- Rollback: `git checkout -- hooks/smoke-test`。
- Status: done

### Step 5 — 全局复核

- Goal: 没有漏网的旧措辞，也没有新造的事实。
- Dependencies: Step 1-4。
- Files: 无（只读复核）。
- Implementation checklist:
  - [x] `grep -rn 'SessionStart only\|只接 SessionStart\|Claude Code only\|Neither is wired'` 在四份文档上无命中。
  - [x] 逐条把改动里新出现的宿主主张与 `hooks/hooks-*.json` 对照，确认 R8。
  - [x] 确认 `CHANGELOG.md` 未被触碰（R6）。
- Acceptance: AC5、AC7。
- Verification: `git diff --stat` 只含四份文档；`git diff --check` 干净。
- Rollback: 无需（只读）。
- Status: done

## Checkpoints

- Step 2 完成后先跑一次 `bash hooks/smoke-test`，确认没有断言依赖被改掉的措辞（`smoke-test:6414` 只 grep `Codex` 与 `lowercase`，但先跑一遍比事后 Debug 便宜）。

## Verification / Review

**逐条对照验收标准**：

- **AC1**：`README.md:229` 与 `README.zh-CN.md:195` 已改为列出 Codex 实际接的四个事件；`grep` 无 `SessionStart only` / `只接 SessionStart`。
- **AC2**：`README.md:124`/`:126` 与 `README.zh-CN.md:91`/`:93` 已含 Codex，并逐句带上「Codex 不记录能力调用 → 用 `unaided` 释放」。
- **AC3**：`hooks/README.md` 的 `(Claude Code only)` 两处、`Neither is wired`、`the pair is wired for Claude Code, CodeBuddy, and Trae` 三组已与 `:105-109` 一致。
- **AC4**：`runtime.md` 的 `:99`（现 `:99`）、`:143`、`:179`、`:286`、`:359` 五处已与 `:50`/`:81` 一致。
- **AC5**：`grep -rn 'SessionStart only\|只接 SessionStart\|Claude Code only\|Neither is wired'` 在四份文档上退出码 1（无命中）。
- **AC6**：`bash hooks/smoke-test` → `ALL SMOKE PASSED`。
- **AC7**：`git diff --check` 干净。

**R8 的机械核对**（每条新事实主张都对得上接线文件）：

```
hooks-codex.json      capability-gate=2  capability-evidence=0
hooks.json            capability-gate=1  capability-evidence=2
hooks-codebuddy.json  capability-gate=1  capability-evidence=2
hooks-trae.json       capability-gate=1  capability-evidence=2
```

Codex 的 `evidence=0` 正是「有门无记录」这条主张的来源；其余三宿主两者都有，与文档一致。

**R6 核对**：`git diff --stat` 不含 `CHANGELOG.md`。

**一处主动纠正**：改 `runtime.md` 目录树注释时先按「gate pair」写，核对 `hooks.json` 后发现 Claude Code 与 CodeBuddy 的 `PreToolUse`/`PostToolUse` 是分开的两条，不是 pair 一词能覆盖的，已按实际事件重写。

**未做**：`@codex-plugin/plugin.json`、`dsh/cordis.patch.yml:3`、`CONTRIBUTING.md:125` 的 `Claude Code only` —— 前者描述的是 Codex 自己的 manifest（正确），后两者属历史叙述或独立议题，已在 PRD 的 Out of Scope 记明。

## Change Log

- 2026-11-04：实现 Step 1-4。`runtime.md` 五处、`hooks/README.md` 三处、`README.md` 三处、`README.zh-CN.md` 三处；`hooks/smoke-test` 只改注释（`:6410` 的「two hosts」→「the host」），断言未动。
- 2026-11-04：`runtime.md` 目录树注释按接线文件实际事件重写了一次（首版沿用了「gate pair」的旧说法，与 `hooks.json` 的两条独立事件不符）。

## Follow-ups

- 若将来给 Codex 接 `capability-evidence`，本任务写的「Codex 不记录」需整体回改，并同步 `hooks/smoke-test:6540-6552` 的契约断言。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-11-04 核对结论**。用户问「D1 的门控修复 Codex 也修了吗」，答：**修了**，因为 `hooks/capability-gate` 是宿主无关的共享脚本，`stage_classes()` 的修复对所有接了它的宿主同时生效。
  **真正的问题在文档**：`README.md:229` 与 `README.zh-CN.md:196` 都还写着「Codex 只接 SessionStart，写前门要等到能解析 `apply_patch` 的补丁文本才谈得上接线」。这句话在 `af8719a feat: wire the pre-write gate on Codex and stop four silent allows`（2026-10-30，随 **v1.1.10** 发布）之后就已经不成立。
  **证据**：
  - `hooks/hooks-codex.json` 有 `PreToolUse` / `matcher: "apply_patch"` → `hooks/capability-gate`。
  - `hooks/capability-gate:84-128` 正是读 `tool_input.command` 里的 patch 文本、提取 `*** Update File:` / `*** Add File:` / `*** Delete File:` / `*** Move to:` 的那段——也就是 README 说「还做不到」的那件事。
  - `skills/taskflow/references/runtime.md:50` 的 Codex 列**已经更新**，写明 `PreToolUse`（`apply_patch`）→ deny，路径从 patch 文本读出。所以只有两份 README 落后。
  **危害属于误导而非崩溃**：读者会以为 Codex 上闸门不可用，从而用 `task unaided` 去绕过一个**其实存在**的检查。而 `task unaided` 写的是「声明该阶段无能力可用」，用它来绕开一个能用的门，会让证据记录失真。
  **要做**：两份 README 的同一段都改成「Codex 的 `PreToolUse`/`apply_patch` 已接写前门」，并保留其中仍然正确的是：「先在 `/hooks` 复核并信任，否则 enabled 但 hook 不生效」。中文那份要同步。
  **顺带核对**：同类陈述是否还有其他宿主版本（CodeBuddy 曾有过一样的过时说法，`7dcde8c` 修过一次）。修的时候应该一次性扫一遍五宿主 × 两份 README × runtime.md 是否互相一致。
