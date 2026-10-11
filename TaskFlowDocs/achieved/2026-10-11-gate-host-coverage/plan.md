# Plan — 前置能力门的宿主覆盖与 approve 的解耦

> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md` — `unaided` 的新契约、宿主接线契约、I1–I6 不变量、以及「一票否决」条件。

## Reference Pointers

- `hooks/capability-gate:119-157`（定位与放行判定）、`:190-215`（上一任务加的同级 worktree 诊断）。
- `hooks/task:976-1016`（`unaided` 现有实现与其自述的定位理由）。
- `hooks/task:1017-1100`（`approve` 的阶段对账；**本任务不改它**）。
- `TaskFlowDocs/achieved/2026-09-27-capability-pre-write-gate/prd.md:27,97,108,118` — 「v1 只接
  Claude Code」的原始决策，以及 R12（内建工具不算能力）、OQ2 的边界。
- `TaskFlowDocs/achieved/2026-09-30-release-ci-test-policy/prd.md:41` — 同一失败模式在 Windows
  上的**同族实测**（门不触发 → `released` 缺失 → approve 卡死）。本任务是它的一般化。
- `TaskFlowDocs/achieved/2026-10-09-trae-host/prd.md:52-56,117` — 「按契约匹配接线、两个脚本
  一行不改」的先例。
- `TaskFlowDocs/achieved/2026-09-19-dsh-host/prd.md:95` — dsh 那次把 `PreToolUse` 列入
  Out of Scope 的记录。
- `skills/taskflow/references/runtime.md:37,41-49,68` — 宿主表与需要改写的反向断言。
- Codex 的 payload 形状：`codex-rs/core/src/tools/handlers/apply_patch_tests.rs` 的
  `pre_tool_use_payload_uses_freeform_patch_input`（断言 `tool_input: {"command": patch}`）。

## Related Tasks

- Parent: None.
- Related: `TF-20260930-c4e4c8`（同族，Windows 上的实例，已交付）。`TF-20261009-8abbd6`
  — 本任务**不**为阶段增加非工具调用的选择通道；该条的触发面是「阶段选择与工具流解耦」，
  本任务修的是「已发布缺陷：approve 的死锁」。两者相邻但不同，且本任务完成后 `unaided` 的
  语义变化需回写进该条的 Notes。
- Relates to: `TF-20260919-40eca2`（发布流程收窄，涉及 Codex/CodeBuddy 的引用）。

## Skills / Tools Used

- [PRD] `mcp__exa__web_search_exa` — purpose: 查三个未接门宿主的工具调用契约（Codex / CodeBuddy / dsh 的 hook 事件名、matcher、deny 输出形状、以及写工具的输入字段）；outcome: 拿到 CodeBuddy 与 dsh 的官方事件与输出形状、Codex 的 `PreToolUse` 契约，以及 dsh 桥的 `preToolPayload` 源码；incorporated: PRD 的「三个宿主的契约」表与 R1/R2/R3。
- [Spec] `mcp__exa__web_search_exa` — purpose: 核实 Codex `apply_patch` 到底把什么交给 hook（「能 deny」不等于「能判定」）；outcome: 确认 `tool_input` 是 patch 文本而非路径，且第三方在 Codex 0.154.0 上实测到同一形状与同一静默失败；incorporated: Spec 的「接线契约」表与一票否决条件。
- [Plan] `mcp__exa__web_fetch_exa` — purpose: 取 Codex 官方 hooks 页全文，核对事件表、matcher 别名、插件 hook 的加载与信任流程；outcome: 得到逐条字段与「非纳管 hook 须经 `/hooks` 审查信任」的实施约束；incorporated: Plan 的 Step 3/Step 4 与 Follow-ups。

三阶段的调用均为本次会话中真实发生的 MCP 调用，由 `capability-gate` 消费 `evidence` 中对应的三条记录并写入 `released`（`v1|PRD|1`、`v1|Spec|2`、`v1|Plan|3`）。

## Preconditions

- [x] 适用的仓库文档与个人规则已检查、优先级/冲突已记录。`repository-docs/index.md` 路由
      `CONTRIBUTING.md`（design,code,commit,pr,release）与 `CODE_STYLE.md`（code,review）。
      本 clone 无个人规则。
- [x] 核心文档单一写者：Primary Agent（Claude）。分支 `fix/gate-host-coverage`，
      worktree `.worktrees/2026-10-11-gate-host-coverage`。
- [x] 既有用户裁定已记录：见 PRD 的 Open Questions。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-11 23:15 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 让 `unaided` 自己放行它声明的阶段

- Goal: R4/R5 —— `approve` 依赖的产物必须由一条在所有宿主上都能成功的命令产生。
- Dependencies: None.
- Files: `hooks/task`。
- Implementation checklist:
  - [x] 读 `plan.md` 的 `> Task version`；活任务目录缺该行 → **在任何写入之前**失败并说明。
  - [x] 幂等：`released` 已有 `<version>|<STAGE>` 行则跳过两处写入，仍报成功。
  - [x] 依次写 `evidence: unaided|<class>` 与 `released: <version>|<STAGE>|<consumed+1>|unaided|<class>`
        （`consumed` 取自 `released` 第 3 列最大值，缺失为 0）。两行成对，序号自洽。
  - [x] 保持既有失败语义与退出码不变（非法 stage / 缺 `--considered` / 概念类不合词表 → 2，零写入）。
  - [x] 不改 `approve` 的任何一行。
- Acceptance: PRD A1、A4。
- Verification: 无门夹具跑 `unaided` 两阶段 → `approve` 通过；`bash -n` 与 bash 3.2 解析。
- Rollback: revert 承载本 Step 的 commit。
- Status: completed

### Step 2 — 用无门夹具钉住它，并守住有门路径

- Goal: A1/A2/A7 —— 死锁由断言而不是靠人记着。
- Dependencies: Step 1.
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 新增独立一节：夹具仓库**不跑任何 hook**，`unaided` 两个阶段后 `approve` 必须通过；
        同时断言 `released` 的两行存在且序号自洽。
  - [x] 反面：不合格的概念类仍失败且零写入；重复 `unaided` 同阶段不产生第二条 release。
  - [x] 既有 `cg_verdict` 系列与 approve 对账节逐条不变（A2）。
  - [x] 自建夹具、末尾清理、git 操作带 `-c user.email/-c user.name`，不依赖前一节状态。
- Acceptance: PRD A1、A2、A4。
- Verification: `bash hooks/smoke-test` 全量；变异——删掉写 `released` 一行 → 本节红。
- Rollback: revert 承载本 Step 的 commit。
- Status: completed

### Step 3 — 在契约匹配的宿主上接线

- Goal: R1/R2/R3 —— 能接的接上，接不了的写明理由而不是留白。
- Dependencies: Step 1（无门宿主已可用，接线是增强而非唯一出路）。
- Files: `hooks/hooks-codebuddy.json`、`skills/taskflow/references/runtime.md`。
- Implementation checklist:
  - [x] CodeBuddy：`PreToolUse`（`Write|Edit`）+ `PostToolUse`（`Skill|Agent|Task`、`mcp__.*`）。
  - [x] dsh：**不接线**；理由（工具名小写、matcher 大小写敏感）写进 runtime.md 的 dsh 一节，
        并由断言钉住 `hooks-dsh.json` 不含 `PreToolUse`。
  - [x] Codex：**不接线**；契约不匹配的理由写进 runtime.md 的 Codex 一节，并由断言钉住
        `hooks-codex.json` 不含 `apply_patch`。
  - [x] **不得**在任何宿主上接线而门读不到目标路径，或 matcher 永不命中（Spec 的一票否决条件）。
  - [x] 每个宿主标注证据强度（packaged-CLI / measured / documented），与 Trae 先例同纪律。
- Acceptance: PRD A3、A5。
- Verification: 接线形状断言；逐宿主核对事件名与 matcher；变异——删掉 CodeBuddy 的 `PreToolUse` → 红。
- Rollback: revert 承载本 Step 的 commit。
- Status: completed

### Step 4 — 让文档与行为一致，并全量验证

- Goal: R6/R7、A6/A7/A8 —— 消除文档中的反向断言，留下可复核记录。
- Dependencies: Step 1, 2, 3.
- Files: `skills/taskflow/references/runtime.md`、`hooks/README.md`、`hooks/smoke-test`（断言）、本任务 `plan.md`。
- Implementation checklist:
  - [x] 改写 `runtime.md:68` 与 `hooks/README.md:203` 的反向断言（「没有别的东西依赖门」）。
  - [x] 事件表的门行按实际情形更新（每个宿主标出接/不接与理由）。
  - [x] 安装说明写清宿主侧的信任/复核步骤（Codex `/hooks` 审查、CodeBuddy 面板与不热加载）。
  - [x] 写明 `unaided` 的语义变化：声明即放行。
  - [x] 断言钉住文档不再含反向断言、且接线形状与文档一致。
  - [x] `bash hooks/smoke-test` 全量；`git diff --check`；`release-check`；`quick_validate`；
        `bash -n` 与 `docker run --rm -v "$PWD:/w" -w /w bash:3.2 bash -c 'bash -n …'`。
  - [x] 记录 PR 模板逐字段映射；推送后记录 CI 三 host 矩阵。
- Acceptance: PRD A6、A7、A8。
- Verification: 上述命令输出逐条记录在 `## Verification / Review`。
- Rollback: revert 承载本 Step 的 commit。
- Status: completed

## Checkpoints

- CP1（Step 1 后）：无门夹具里 `approve` 通过；有门路径手跑不回归。
- CP2（Step 2 后）：断言在变异下变红；既有节全绿。
- CP3（Step 3 后）：接线形状被钉住；不存在「声称有门却静默放行」的宿主。
- CP4（Step 4 收尾）：全套命令通过、文档与行为一致、CI 绿。

## Verification / Review

逐条记录命令与结果。区分：**既有失败** / **新引入失败** / **环境失败**。

| 检查 | 结果 | 分类 |
| --- | --- | --- |
| **CI 三宿主矩阵**（`Hooks`，run [`38149885979`](https://github.com/hkwuks/TaskFlow/actions/runs/38149885979)） | `success`；六个 job 全绿：`smoke (ubuntu-latest)`、`smoke (macos-latest)`、`smoke (windows-latest)`、`release`、`evals`、`todo-merge-audit` | 通过（A7） |
| `bash hooks/smoke-test`（全量，本地） | exit 0，`ALL SMOKE PASSED`，72 个 `ok` 节（改动前 68） | 通过 |
| **变异验证 1**：删掉 `hooks/task:1043` 写 `released` 的那一行 | `FAIL unaided did not write the release record` | 断言有效（A1 被咬住） |
| **变异验证 2**：从 `hooks-codebuddy.json` 删掉 `PreToolUse` | `FAIL hooks/hooks-codebuddy.json is missing "PreToolUse"` | 断言有效（A3 被咬住） |
| 两处变异恢复后重跑全量 | `ALL SMOKE PASSED`，`FAIL` 计数 0 | 通过 |
| 恢复的完整性 | `diff` 两份备份 → `hooks/task` 与 `hooks-codebuddy.json` 均与变异前逐字节相同 | 通过 |
| 无门夹具（断言内，不跑任何 hook） | `unaided PRD` + `unaided Plan` → 两文件各 2 行、序号 `1`/`2` → `approve` 通过并写入 `- Status: approved` | 通过（A1、A4） |
| 声明不覆盖门的记录（断言内） | 已由门写入 `v1|PRD|1|invoke|some:cap` 后，`unaided` 不追加、`approve` 以正确理由拒绝 | 通过（I3） |
| 幂等与零写入（断言内） | 重复声明同阶段不新增行；词表外概念类与缺 `> Task version` 均在写入前失败 | 通过（I4） |
| 有门路径不回归（断言内） | 既有 `cg_verdict` 系列与 approve 对账节逐条不变 | 通过（A2） |
| CodeBuddy 接线形状与实跑（断言内） | 4 条命令、5 个模式串；`capability-gate` 输出 `permissionDecision: deny`，`capability-evidence` 记下 `invoke|codebuddy:smoke`，随后同文件放行 | 通过（A3） |
| dsh / Codex 的**不接**（断言内） | `hooks-dsh.json` 不含 `PreToolUse`；`hooks-codex.json` 不含 `apply_patch` | 通过（A5） |
| 文档反向断言（断言内） | 两份文档都不再含旧句；`capability-gate`/`capability-evidence` 仍被 `hooks/README.md` 描述 | 通过（A6） |
| `git diff --check` | 无输出 | 通过 |
| `bash hooks/release-check .` | `STATUS: pass` | 通过 |
| `quick_validate.py skills/taskflow` | `Skill is valid!` | 通过 |
| `bash -n`（hooks/task、capability-gate、capability-evidence、smoke-test、session-start） | 五个文件均无输出 | 通过 |
| `docker run --rm -v "$PWD:/w" -w /w bash:3.2 bash -c 'bash -n …'` | `bash 3.2 parse: ok` | 通过（A8） |
| 五个接线 JSON 与 `.codebuddy-plugin/plugin.json` 的 JSON 解析 | 逐个 `json.load` 通过 | 通过 |

### 实现期修正（由实测咬出）

1. **dsh 的处置从「接线」改为「不接线」。** 第一稿要往 `hooks-dsh.json` 加 `PreToolUse`
   （Spec 原 R2）。实测 dsh 0.2.0-rc.2 发现桥以 `tool_name: exec.name` 原样透传、工具名是
   `write`/`edit`，而 matcher 与两个钩子的 `case` 都大小写敏感——那个接线**必然**永不命中，
   等于静默放行。接线已回滚，`hooks-dsh.json` 保持 SessionStart-only，理由写进 runtime.md。
   该结论已回写 Spec 的接线契约与 PRD 的 R2/A3/A5。
2. **CodeBuddy 的工具名有第二套说法，按打包产物定案。** 官方两份文档面互斥：CLI 文档写
   `Write`/`Edit`，腾讯云镜像页写 `write_to_file`/`replace_in_file`。解包
   `@tencent-ai/codebuddy-code@2.137.0` 读部署代码后确认前者是事件字段、后者只是 telemetry
   别名。这条**不是**活体实测——真机会话仍未跑过，runtime.md 与 smoke 注释都据此措辞。
3. **`runtime.md` 的标题层级一度被打乱：** 改写时把 `### dsh specifics` 的正文移到了
   `### Codex specifics` 标题下，使同一文档出现两个 `### dsh specifics` 且 Codex 一节位置错乱。
   已合并回一处并复跑全量。

### PR 模板逐字段映射

`.github/pull_request_template.md` 的每个字段落点：

| 模板字段 | 落点 |
| --- | --- |
| `## Summary` | PR 正文：`approve` 只认 `released`、而 `released` 只有门一个写者 → 三个宿主永久卡死、且给出的补救命令本身不可能成功。 |
| `TaskFlow traceability` → Task | `TaskFlowDocs/2026-10-11-gate-host-coverage/` |
| `TaskFlow traceability` → Scope | 逐文件列出；`hooks-dsh.json` 与 `hooks-codex.json` 明写 **unchanged**。 |
| `TaskFlow traceability` → Base branch / Target repository | `main` / `hkwuks/TaskFlow` |
| `## Verification` 第 1 项 | 推送后取 CI run 链接回填。 |
| `## Verification` 第 2–4 项 | 本文件的 `## Verification / Review` 表逐条对应。 |
| `## Verification` 最后一项 | 本表即「recorded in the TaskFlow Plan」。 |
| `## Review boundaries` 四项 | 逐条勾选；「Remote/base assumptions」由 base branch 与 push 权限检查（unprotected + `push`）覆盖。 |
| `## Review boundaries` 末项（known limitations） | PR 正文的 Known limitations 段：CodeBuddy 无活体验证、`unaided` 在有门宿主上的语义变化、两条不接被断言钉住、既有 `repository-check` 孤儿目录。 |

## Change Log

- v1（2026-10-11）：Step 1–4 落地；`unaided` 自放行、无门夹具断言、CodeBuddy 接线、
  dsh/Codex 的两条明确不接与理由、文档反向断言清除。

- 2026-10-11 work revision — 任务由 `TF-20261011-39bda8` promote 创建；用户裁定范围
  （接线 + 兜底两件都做）、修法（`unaided` 补写 `released`）、证据门槛（文档先行 + 标注强度）；
  写入 PRD 的 Open Questions 与 `spec.md` 的 Design Decisions；affects
  `prd.md`, `spec.md`, `plan.md`, `TaskFlowDocs/todo.md`。

## Follow-ups

- Codex 不接门。要接需另起一条记录「门从 patch 取路径」的独立任务（解析三条指令、多文件、
  相对路径按 `cwd` 解析，以及 Codex 自身 guardrail 边界所限）。
- dsh 不接门的理由已实测（工具名小写 + matcher 大小写敏感）。要接需给 `capability-gate` 与
  `capability-evidence` 的 `case` 加小写分支，并在本机真机验证 deny 真的发生——这是钩子语义
  的扩张，应独立成任务。
- CodeBuddy 的接线**尚无活体会话验证**。结论来自打包 CLI 的静态阅读；用户在真机上跑一次
  CodeBuddy 会话即可确认或推翻。若 matcher 或字段名与阅读不符，请回报。
- 本任务完成后，`TF-20261009-8abbd6` 的 Notes 需补记 `unaided` 的语义变化。
- 上一任务遗留：基础检出中的同名任务目录仍会让 worktree 的文档被放行（见 `2026-10-11-evidence-anchor`）。

## Version History

- v1 — 规划中，等待用户批准。
- v1（实现完成）— Step 1–4 落地；dsh 处置由「接线」改为「不接线」（实测），CodeBuddy 接线
  依打包产物定案并待活体验证。
