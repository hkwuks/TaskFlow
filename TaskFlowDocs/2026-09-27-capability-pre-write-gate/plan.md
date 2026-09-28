# Plan — Block the first body write of prd/spec/plan until a capability-class tool was ac
> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers

- 实测记录（本任务内，未落盘为独立文件）：2026-09-27 临时探针确认 `Skill` 同时触发 `PreToolUse`/`PostToolUse`、`tool_input.skill` 携带能力名、`Skill` 可作 matcher、`PreToolUse` 对 `Edit` 触发；并确认 `~/.claude/settings.json` 的 hooks 为全机全局。探针已完整还原（`settings.json` 哈希与装前一致）。

## Related Tasks

- Todo `TF-20260927-5814d0`（本任务）
- 推进的上游遗留项：`TaskFlowDocs/achieved/2026-09-23-capability-invoke-gate/` 的 Follow-ups 第一条（"hook that refuses first write to `prd.md` without a `[PRD]` line"）

## Skills / Tools Used

- [PRD] `agent-skills:idea-refine` — purpose: stress-test the requirements framing before the first body write of `prd.md`; invoked for the Define class. outcome: succeeded. incorporated: six assumptions that would otherwise have reached implementation unexamined — tool-class predicate boundary, evidence scope versus compact/resume, `plan.md` serving both as record and gated document, evidence-store placement, fail-open versus fail-closed, escape-hatch accountability.
- [Spec] `agent-skills:spec-driven-development` — purpose: produce the design contract before the first body write of `spec.md`; invoked for the Design class. outcome: succeeded. incorporated: Phase 0 scope check (one capability, not several), explicit-unknowns discipline, and its "reuse the project's own spec system instead of a duplicate SPEC.md" rule. Its `tasks/plan.md` / `SPEC-*.md` convention was deliberately not adopted — TaskFlow is this project's spec system.
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: dependency-order the steps before the first body write of this Plan; invoked for the Plan class. outcome: succeeded. incorporated: vertical-slice rule (store + capture hook before the gate that reads it), checkpoint after every 2–3 steps, and the never-overwrite-an-incomplete-plan guard. Its planning-time read-only rule is what surfaced the "evidence hook has no file path" gap, now fixed in `spec.md`.

## Preconditions

- **工作树隔离已建立**：分支 `feature/capability-pre-write-gate`，工作树 `.worktrees/2026-09-27-capability-pre-write-gate`，base = `origin/main` @ `65ddd0a`（v1.1.0）。分支**未设 upstream**（裸 `git push` 不会直推 main）。
- **适用仓库文档**（已读，据 `TaskFlowDocs/repository-docs/index.md` 路由）：`CONTRIBUTING.md`（分支前缀、提交格式、PR 模板）、`CODE_STYLE.md`（shell 约定、退出码 `0/2/3`、复用优先、双语 README 对齐）、`LICENSE`、`README.md` + `README.zh-CN.md`、`ROADMAP.md`、`.github/pull_request_template.md`、`RELEASE.md` + `CHANGELOG.md`。无个人规则（`repository-docs/personal.md` 不存在）。
- **钩子契约已实测**（见 Reference Pointers），门的两个事件面成立。
- **本任务的文档写入不会被新门拦截**：本机活动插件是 `1.1.0`，仓库里的 hooks 改动在发版重装前不生效（这是本任务最大的外部依赖，见 Verification / Review）。
- 无并发写入者：本任务 core documents 只有本会话在写。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-27 23:41 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 证据存储与捕获钩子（地基）

- Goal: 一次真实能力调用在 `<absolute-git-dir>/taskflow/evidence` 追加一条记录；在非 TaskFlow 环境完全 no-op。
- Dependencies: 无（地基）
- Files: `hooks/capability-evidence`（新增）、`hooks/json-field`（新增，偏差见 Change Log）、`hooks/hooks.json`、`hooks/smoke-test`
- Implementation checklist:
  - [x] `hooks/hooks.json` 增 `PostToolUse`，matcher 覆盖 `Skill|Agent` 与 MCP 形式；保留现有 `SessionStart` 不动
  - [x] 证据钩子按事件 `cwd` 解析 `git rev-parse --absolute-git-dir`；不可解析则静默 no-op
  - [x] cwd 所属仓库无 `TaskFlowDocs/<task>/plan.md` 活动任务时 no-op（不污染非 TaskFlow 仓库）
  - [x] 能力标识映射：`Skill` → `tool_input.skill`；`Agent` → `tool_input.subagent_type`；MCP → `tool_name`；其余工具跳过
  - [x] 追加 `kind|capability`，写入前剥掉值里的 `|`、CR、LF 并截断到 200 字符
  - [x] 任何错误都退出 `0` 且不产生副作用（钩子不得让调用者失败）
  - [x] `hooks/smoke-test` 增夹具：合成任务目录 + 以 stdin 喂合成事件 JSON
- Acceptance: 合成 `Skill` 事件 → `evidence` 恰好多一行且内容正确；非 TaskFlow 路径、`achieved/` 路径、无可解析 git dir → `evidence` 零变化且退出 `0`。**已满足**。
- Verification: 定向矩阵 8 项通过（含 `args` 里的伪 `"skill"` 注入未得逞、`Bash`/非 `PostToolUse` 不记录、非 TaskFlow 与 achieved-only 仓库不建存储、坏 JSON 静默 no-op、缺 `cwd` 时回落到进程工作目录）；全套见 Verification / Review 的环境说明。
- Rollback: 移除 `hooks/capability-evidence` 与 `hooks/json-field`，还原 `hooks/hooks.json` 的 `PostToolUse` 段；`evidence` 在 `.git` 内，删除即可
- Status: done

### Step 2 — 写前门

- Goal: `prd.md`/`spec.md`/`plan.md` 的正文写入，在该 stage 尚无同版本放行记录时被拒；有证据则放行并消费。
- Dependencies: Step 1（门读的就是 Step 1 的存储）
- Files: `hooks/capability-gate`（新增）、`hooks/hooks.json`、`hooks/smoke-test`
- Implementation checklist:
  - [x] `hooks/hooks.json` 增 `PreToolUse`，matcher `Write|Edit`
  - [x] 从 `tool_input.file_path` 解析：basename 必须 ∈ {`prd.md`,`spec.md`,`plan.md`}，否则 no-op
  - [x] 文档必须**恰好**位于 `TaskFlowDocs/` 下一层（父目录名须为 `TaskFlowDocs`），且 `<task>/plan.md` 存在；否则 no-op
  - [x] 按目标文件目录解析证据存储（**不是** cwd），读该任务 `plan.md` 的 `> Task version:` 得 `V`
  - [x] 已放行 `V|stage` → 直接放行且不重复消费（幂等）
  - [x] 否则要求 `evidence` 最大行号 > *全局*已消费的最大行号，成立则追加放行记录并放行
  - [x] 拒绝时输出 `hookSpecificOutput.permissionDecision: "deny"` + `permissionDecisionReason`，内容含 stage、相位概念类、可复制的 `hooks/task unaided …` 命令
  - [x] 拒绝目标是证据存储路径的 `Write`/`Edit`（I2）
  - [x] 门自身出错（读不到版本、解析不出 git 目录）→ 明确说明"是门出错而非用户违规"并给出逃生舱
- Acceptance: PRD 的 A1–A3、A5–A7、A12 全部通过；同一版本内对同一文档的第二次编辑不再被拦。**已满足**。
- Verification: 定向矩阵 22 项通过；拒绝载荷经 JSON 解析验证（合法 JSON，含 stage/概念类/逃生舱命令，且不含需转义的裸双引号）。测试抓到两个实现缺陷并已修：achieved 豁免判错了目录层级；`consumed` 按版本统计导致版本升级后旧证据仍可放行（I4 失效）。
- Rollback: 移除 `hooks/capability-gate`，还原 `hooks/hooks.json` 的 `PreToolUse` 段
- Status: done

### Step 3 — 逃生舱

- Goal: `hooks/task unaided <PRD|Spec|Plan> --considered "<concept class>"` 一条命令登记 Unaided 决定并因此放行。
- Dependencies: Step 1（写同一存储）、Step 2（门的放行语义）
- Files: `hooks/task`、`hooks/smoke-test`
- Implementation checklist:
  - [x] 新增 `unaided` 子命令，纳入现有 `split_root` / usage 框架
  - [x] 校验 stage 合法、`--considered` 非空、概念类命中相位词表
  - [x] 通过则追加 `unaided|<concept class>`；不通过退出 `2` 并指明原因
  - [x] 命令**不**自行判断概念类是否"合理"——只做词表校验
  - [x] 偏差：词表从 `require_stage` 的 awk 分支提升为 `hooks/task` 顶部的 shell 变量 `concept_class_re`（Step 4 要删掉 awk 里那份，提升后仍是唯一一份）
  - [x] 偏差：增加"必须存在活动任务"守卫——门是从**任务目录**的 git 目录读记录，若在 base checkout 或无任务处调用，记录会落进一个永远没人读的存储，必须当场拒绝而不是假报成功
  - [x] 参数错误用显式 `exit 2`（`CODE_STYLE.md`：需用户输入用 2），**不**用本脚本惯用的 `fail`（退 1），并在注释里写明别"统一"回去
- Acceptance: PRD 的 A4 通过；缺少 `--considered`、stage 非法、概念类不在词表 → 均退出 `2` 且存储零变化。**已满足**。
- Verification: 定向 10 项通过（4 类参数错误各退 2 且零写入、合法调用退 0、门随即放行、`released` 的 kind 记为 `unaided`、无活动任务时给出可读拒绝）。套件内的正反例已加入。
- Rollback: 移除 `unaided` 子命令分支与 `concept_class_re` 定义
- Status: done

### Step 4 — `task approve` 对账

- Goal: approve 的 stage 校验从"文字形状"升级为"与同版本放行记录对账"，并报告 invoked / unaided 计数。
- Dependencies: Step 2、Step 3
- Files: `hooks/task`、`hooks/smoke-test`
- Implementation checklist:
  - [x] 每个必需 stage 要求 `plan.md` 的 stage 行与一条同版本放行记录匹配，且 `kind` 一致（invoke 行不得由 unaided 记录背书，反之亦然）
  - [x] **删除** `require_stage` 里的大任务概念词表正则分支（`hooks/task:856-866`）——词表校验已移到 `task unaided` 这个唯一入口，在 approve 重校验一段已被存储保证的文本是纯冗余
  - [x] **删除** `invoke line is empty` 分支（`hooks/task:869-873`）——它的原意是"总得先发生一次调用"的替身，现被"行必须匹配一条 invoke 记录"完全覆盖
  - [x] 保留：`missing stage` 分支、Unaided 的 `considered:` 存在性检查、写 Approval 前的 fail-closed
  - [x] 输出 invoked / unaided 计数，使"总是 Unaided"这种模式可见
  - [x] `hooks/smoke-test:959` 那条绑实现文本的断言（`grep -q 'require_stage PRD'`）**删除**——它断言的是内部实现而非行为，重构即失效。同时删掉相邻的 `grep -q 'phase-table concept class'`：它匹配的是 `hooks/task` 里的一句注释，比绑实现更脆
  - [x] 改写 `hooks/smoke-test:884` 用例的理由：它现在**必须先有存储记录**才可能通过，注释里的 "shape only, no product allowlist" 已过期
  - [x] 复核 `b9279e6` 的 BSD-awk 换行 workaround 是否仍需要（新用例仍传多行 stage 行，预计仍需要——不预设删除）
  - [x] 现有失败行为不回退：缺 stage、Unaided 缺 `considered:` → 仍 fail closed 且不写半截 Approval
- Acceptance: PRD 的 A8、A9 通过；既有 approve 冒烟用例全绿。**已满足**。
- Verification: approve 章节重写后定向跑通（含新增 5 例：无记录被拒且消息给出逃生舱、行名与记录能力不符被拒、invoke 行压在 unaided 记录上被拒、`considered` 类与记录不符被拒、放行后计数为 `1 invoked, 1 unaided` / `0 invoked, 3 unaided`）。**夹具改为真 worktree**：放行记录存在 worktree 自己的 git 目录下，同一 worktree 里两个任务会共享同一份记录——这是生产不可能出现的碰撞（生产一任务一 worktree），所以小/大两个夹具各自成一个 `git worktree add`，顺带把"一任务一存储"这条设计钉进了测试。同段落在**改动前**的 `hooks/task`（`git archive HEAD`）上跑会红在 `FAIL approve accepted stage lines with no release record`，即新断言对旧契约有区分力。另确认套件其他段落一律用 `sed` 直接铺 Approval 字段、不调用 `task approve`，故不受本步影响。
- Rollback: 还原 `hooks/task` 的 `approve` 分支
- Status: done

### Step 5 — 契约文档

- Goal: 文档与实现一致——记录的家移出 `plan.md`，事件映射补 `PreToolUse`，双语 README 行为对齐。
- Dependencies: Step 2、Step 4（文档描述的是已实现的契约）
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`skills/taskflow/references/runtime.md`、`README.md`、`README.zh-CN.md`
- Implementation checklist:
  - [x] `SKILL.md:150`：**删除**"在写 `prd.md` 正文之前先追加 `[PRD]` 行"的整条顺序纪律——记录移出 `plan.md` 后它已无对象，时序改由门在写入那一刻机械保证。替换为一句短陈述：门会在写入前拦截，`## Skills / Tools Used` 是报告
  - [x] `SKILL.md:148`：**删除**"必须是选择而非疏忽"的说教表述——逃生舱是一条显式命令，"是选择不是疏忽"已由机制保证，不必再用文字要求；保留 unaided 的定义本身
  - [x] `references/artifacts.md:113`：**删除** `- [PRD] …` **before** `prd.md` 的 "before" 顺序要求；同步 Skills 段语义为报告
  - [x] `references/runtime.md`：事件映射表补 `PreToolUse` 一行；记录钩子契约是针对哪个 Claude Code 版本实测的（I8）；写明非 Claude Code host 无门（I6）
  - [x] **同步修 `hooks/smoke-test:1132`**：它钉着 `must be a choice, not an oversight`，正是本步要删掉的那句 `SKILL.md` 文本；不改则套件转红。改法是让断言盯住新措辞（门在写入前拦截、Skills 段是报告），而不是把这条保证删掉。
  - [x] `README.md` 与 `README.zh-CN.md` 行为对齐（`CODE_STYLE.md` 要求）
- Acceptance: PRD 的 A10、A11 通过；文档不再把 `plan.md` 描述为写前记录位。**已满足**。
- Verification: Skill 校验器通过（`quick_validate.py skills/taskflow`；本机默认 GBK 会 `UnicodeDecodeError`，需 `PYTHONUTF8=1`）。两段文档断言全绿。双语 README 逐句核对：同一行为的措辞在两份文件里对应（写前门、hook 可记录调用并拒绝首写、门只能拒绝不能批准、`task unaided` 加入命令列表）。
- 本步顺手修掉的两处**既有**文档与实现不符（不是新引入的）：`SKILL.md:56` 与两份 README 的 `task` 子命令列表都停在 `complete`，未含 `unaided`；`artifacts.md` 的 Plan 模板把 Skills 段示例写成**无 stage 标签**的 `- \`<name>\` …`，而 approve 明确要求带 `[PRD]`/`[Spec]`/`[Plan]` 标签，照着模板写必被拒——两条示例改为带标签。
- 偏差：额外改了 `hooks/README.md`（新增三个 hook 的文件清单、scope/safety 一段、lifecycle 命令）——它自称逐 hook 说明允许写什么，不改则与实现直接矛盾。
- 已知未覆盖：`reference/index.md`（Research 阶段）有意不在 v1 门范围内，`runtime.md` 不得暗示它被门覆盖。
- Rollback: 还原这 6 个文档
- Status: done

### Step 6 — 可移植性、CI 与发版面

- Goal: 新脚本守住 bash 3.2 / BSD 下限与 Windows 路径，发版面（CHANGELOG、marketplace pin）就绪。
- Dependencies: Step 1–5
- Files: `hooks/smoke-test`、`hooks/smoke-test-windows.ps1`、`tools/fixture-compare`（若需登记新脚本）、`CHANGELOG.md`、`.claude-plugin/marketplace.json`（+ 各 host catalog）
- Implementation checklist:
  - [x] Windows 套件覆盖门与逃生舱，含含空格/中文的仓库路径
  - [x] `tools/fixture-compare` 通过（无 `declare -A` / `mapfile` / GNU `sed -i`）
  - [x] 无解释器 PATH 下门与证据脚本均可运行
  - [x] `CHANGELOG.md` 新增条目；marketplace pin 与版本字面量一致（`hooks/release-check` 通过）
- Acceptance: 两套 smoke 全绿；`bash hooks/repository-check .` 无告警；`git diff --check` 干净。**部分满足，未满足处已定性**（见下）。
- Verification:
  - **Windows 套件本机可跑，已跑通**（这是本任务此前列为"未跑"的一项）：`hooks/smoke-test-windows.ps1` 输出 `WINDOWS LAUNCHER ARGS / SESSIONSTART / LIFECYCLE / PRE-WRITE GATE PASSED`，退出 0。新增段把门与逃生舱经**真实启动器** `run-hook.cmd` 驱动，仓库路径含空格与中文。
  - **窗件的 stdin 走文件 + `cmd` 重定向，不走 PowerShell 管道**：实测 PS 5.1 把字符串管进原生命令时会写入 **UTF-8 BOM**，而 `json-field` 对 BOM 报 `exit 2`（事件被当作非法 JSON）——于是门静默 no-op，测试会"通过"却没证明任何事。改用无 BOM 文件后才有区分力。这个 BOM 是测试宿主的产物而非宿主事件：CR 尾部 `json-field` 能容忍（已实测），BOM 不能。**未修**，见 Follow-ups。
  - 无解释器段新增两项断言（证据钩子写出恰一行、门对已放行的 stage 不拒绝），本机以包装目录前置 PATH 跑通。
  - 静态可移植性：全树 `declare -A` / `mapfile` / 裸 `sed -i` **零命中**。
  - `bash hooks/release-check .` → `STATUS: pass`。
  - **更正一条计划里的错误认知**：`tools/fixture-compare` **不是**静态检查器，它是把一次运行的夹具与参考运行逐字节比对（归一化路径与时间戳）。可移植性下限实际由 smoke 的两段承担——`bash -n`（macOS 上是真 3.2 解析器）与无解释器 PATH。`references/runtime.md` 原来把这功劳记在 `fixture-compare` 上，已改正。
  - **CHANGELOG 属于本任务**（原先怀疑属发版）：查历史确认本仓库的惯例是 feature 分支加 `## [Unreleased]` 段（`83d4eb6`），发版提交只把标题改成 `[X.Y.Z] — 日期`（`620c6a7`），且 `release-check` 会跳过 `[Unreleased]`（已实测 `STATUS: pass`）。已按此写入。
  - **本机无法给出的判定**：整段 bash smoke 在 MSYS 下跑不完（既有环境问题，基线同样失败，见 Verification / Review），故"两套 smoke 全绿"只能由 CI 裁定；`bash hooks/repository-check .` 仍报 `needs-user-input`，两项都已定性为**既存**——`achieved/2026-09-10-repository-document-placement` 孤儿目录在未修改的 `main` 检出上同样报（已实测），本任务目录未提交是交付前的正常状态。
- Rollback: 还原上述文件
- Status: done

## Checkpoints

### Checkpoint A — after Steps 1–2（地基与门）

- [ ] `evidence` 与 `released` 的读写路径在合成夹具下行为正确
- [ ] no-op 边界全覆盖：外来仓库、`achieved/`、非任务目录、basename 不匹配
- [ ] 无解释器 PATH 下两个新脚本可运行

### Checkpoint B — after Steps 3–4（逃生舱与对账）

- [x] 逃生舱正反例退出码正确
- [x] approve 的既有失败用例无回退
- [x] "写完 prd 直接写 spec"被拒、中间补一次调用后放行（逐阶段新鲜度）

### Checkpoint C — after Steps 5–6（文档与发版面）

- [x] 文档不再把 `plan.md` 描述为写前记录位
- [x] 双语 README 行为一致
- [ ] 两套 smoke + fixture-compare + release-check 全绿 —— Windows 套件、release-check、静态下限本机全绿；**整段 bash smoke 只能由 CI 裁定**（MSYS 环境，基线同样失败）；`fixture-compare` 不是检查器，见 Step 6 的更正

## Verification / Review

仓库内可完成的验证（Step 1–6 各自列出的命令）与 PRD A1–A12 的对应关系：

| PRD 验收 | 覆盖方式 |
| --- | --- |
| A1–A5 | Step 2 / 3 的 smoke 矩阵（合成事件 JSON + 合成任务目录） |
| A6、A12 | Step 2 的 no-op 边界用例 |
| A7 | 断言 `promote`/`version`/`archive` 路径不经 `Write`/`Edit`，且不受门影响 |
| A8 | Step 1 / 2 / 6 的 smoke + 无解释器 PATH + Windows 套件 |
| A9 | Step 4 保留既有 approve 失败用例 |
| A10、A11 | Step 5 的文档与 skill 校验 |

**接线本身也已验证（不是只验证钩子脚本）**：从 `hooks/hooks.json` 里取出 `PreToolUse` / `PostToolUse` 各条目的 `command` 原串，按宿主的方式替换 `${CLAUDE_PLUGIN_ROOT}` 后交给 shell 执行——`PreToolUse` 条目对未放行的 stage 返回 `deny`、有证据后放行；`PostToolUse` 的 `Skill|Agent|Task` 条目写出 `invoke|wired:cap`；`mcp__.*` 条目可执行且以 `tool_name`（`mcp__x__y`）入账；`released` 落成 `v1|PRD|1|invoke|wired:cap`。**未覆盖**：matcher 是否真的按宿主语义命中 `Agent`/`mcp__.*`（宿主侧行为，需真实会话）。

**A8 的判定环境受限（实测，必须明说）**：本机是 Windows + MSYS/Git-Bash。套件那个"无解释器"章节会把白名单工具**软链**进一个临时 PATH，而 MSYS 下经软链启动的二进制找不到自己的 DLL（`error while loading shared libraries: ?`），整套在那一章即中止，随后章节一律跑不到。用**未修改的 `origin/main`** 复现，**同一位置同样失败** —— 因此这不是本任务引入的。为拿到真实结论，本地以一个按绝对路径 exec 真二进制的包装目录前置 PATH 跑通了整套；即便如此仍有一个既有章节失败（`a drive-path absolute git dir was read as relative to the root`），基线在同样包装下同样失败，属包装/环境所致而非代码回归。**结论：本机不能给出 A8 的权威判定**，需由 CI（`.github/workflows/hooks.yml`，Linux/macOS）裁定；本机结果只作为"新章节通过、未引入新失败"的证据。

**仓库内无法完成的验证（必须明说）**：A1–A5 描述的是**真实会话**里的行为，而插件改动只有发版并重装后才进入真实会话。因此本任务交付时，门只能在合成夹具下被证明，端到端行为待发版后按下述配方验证：

```text
1. 走 RELEASE.md 发版（用户操作；release 不经 TaskFlow，不在本任务范围内）
2. 重装插件：claude plugin marketplace add hkwuks/TaskFlow && claude plugin install taskflow@taskflow
3. 新会话：promote 一个新任务，不调用任何能力，直接写 prd.md 正文
   期望：写入被拒，消息含 [PRD]、概念类、以及可复制的 task unaided 命令
4. 执行 hooks/task unaided PRD --considered "requirements elicitation and framing"，重试写入
   期望：放行
5. 紧接着写 spec.md 正文（中间不调用）
   期望：被拒（逐阶段新鲜度）
```

未通过上述 1–5 之前，不得宣称"门已保证生效"——只能宣称"已实现且夹具通过"。

## PR

- 模板：`.github/pull_request_template.md`（已读；没有任何字段标为可选，按必填处理）
- 目标仓库：`https://github.com/hkwuks/TaskFlow`（`origin`，https，已抹去凭据）；base 分支 `main`
- head：`feature/capability-pre-write-gate`；base commit `origin/main` @ `65ddd0a`
- 新鲜度：开 PR 前执行 `git fetch origin main`，本地 `origin/main` 仍为 `65ddd0a`，本分支领先 1、落后 0——创建时的结论只在这个时点成立
- 字段映射：

| 模板字段 | 落点 |
| --- | --- |
| Summary | PR 体首段：approve 期的"形状"校验换成写前门 + 钩子证据 + 对账 |
| TaskFlow traceability → Task | `TaskFlowDocs/2026-09-27-capability-pre-write-gate/` |
| TaskFlow traceability → Scope | `hooks/{capability-evidence,capability-gate,json-field,hooks.json,task,smoke-test,smoke-test-windows.ps1,README.md}`、`skills/taskflow/{SKILL.md,references/artifacts.md,references/runtime.md}`、`README.md` + `README.zh-CN.md`、`CHANGELOG.md` |
| TaskFlow traceability → Base branch | `main` |
| TaskFlow traceability → Target repository | `https://github.com/hkwuks/TaskFlow`（origin；无凭据） |
| Verification 四行 | `git diff --check`、skill 校验、Plan 记录三项已实际执行并勾选；`bash hooks/smoke-test` **不勾**，理由见下 |
| Review boundaries 四行 | 四条均成立，理由写在 Known limitations |

- 勾选口径：`bash hooks/smoke-test` 本机跑不完（MSYS 既有问题，未修改的 `origin/main` 在同一段失败），因此**不勾**该行并在 PR 体里写明由 CI 矩阵裁定——`CONTRIBUTING.md` 要求不得声称未发生的检查。已实际执行的是可提取章节、Windows 套件、`hooks.json` 接线、无解释器段、静态下限、`release-check`、skill 校验器。
- 用户决定：推送与开 PR 由用户明确要求。

## Change Log

- 2026-09-27 — Plan 初稿：6 个 Step + 3 个 Checkpoint。按 `planning-and-task-breakdown` 的垂直切片规则把"存储 + 捕获钩子"排在门之前。
- 2026-09-27 — `spec.md` 修正（措辞/方法澄清，非 Task-version 变更）：证据钩子按事件 `cwd` 解析存储，而非按文件路径——`Skill` 的 `tool_input` 里没有路径。该缺口是 Step 5 的 read-only 规划规则逼出来的。
- 2026-09-27 — 记录实测：`Skill` 同时触发 `PreToolUse`/`PostToolUse`，`tool_input.skill` 带能力名，`Skill` 可作 matcher，`PreToolUse` 对 `Edit` 触发；`~/.claude/settings.json` 的 hooks 为全机全局（探针日志曾捕获到另一个并发会话在无关仓库的写入，已改为最小足迹并完整还原配置）。
- 2026-09-27 — 删除清单折入（用户提问"有什么之前无效的设计可以去掉"）。Step 4 增 3 条显式删除项与 1 条待复核项，Step 5 增 3 条文档删除项（含行号锚点），`spec.md` 的设计决策段记录删除原因与**被拒绝的那一处删除**。PRD 的 R5 与 A9 相应改写：概念词表校验的唯一入口变成 `task unaided`，approve 不再重复校验——A9 的失败面因此"位置迁移但不缩小"，验收方式跟着改。
- 2026-09-28 — Step 1–2 实现完成。两处偏差：新增共享文件 `hooks/json-field`（把 `session-start` 那份手写 JSON 解析器加一层嵌套取值——两个新钩子都要从 `tool_input.*` 取字段，复制一份已验证的解析器比再写一个更安全）；MCP matcher 用 `mcp__.*` 而非裸 `mcp__`，强制按正则解析，避开 matcher 精确串/正则语义的未知。定向测试抓到两个实现缺陷并已修：achieved 豁免按目录名判层级，会把 `TaskFlowDocs/achieved/<task>/` 当活动任务；`consumed` 按版本统计，使版本升级后旧证据仍可放行（I4 失效），改为全局消费。
- 2026-09-28 — 主动删掉一行自己刚写的代码：证据钩子里原本有一句把反斜杠 cwd 归一化成正斜杠。试写它的测试时测得 MSYS 自己就会转换反斜杠，且该变量在钩子里的唯一消费者是 `git -C`（不再用于 `[ -d ]`），这行既保护不了什么也无法在任何平台上被测试鉴别。删掉并在原位留了一句说明。
- 2026-09-28 — 发现 Step 5 会连带打破既有断言：`hooks/smoke-test:1132` 钉着 `must be a choice, not an oversight`，正是 Step 5 计划删掉的那句 `SKILL.md` 文本。Step 5 必须同步改这条断言，否则套件转红。
- 2026-09-28 — 验证环境受限，已定性（见 Verification / Review）：本机 MSYS 下整套 smoke 无法原样跑通，用未修改的 `origin/main` 做基线复核后确认同一失败点，与本次改动无关。
- 2026-09-28 — Step 3–4 实现完成。approve 的 stage 校验改为与同版本放行记录对账，并删掉两处冗余分支与两处绑实现文本的断言（其中 `phase-table concept class` 匹配的是一句注释）。改写既有 approve 章节时发现夹具不成立：放行记录按 worktree 的 git 目录存放，而原夹具把两个任务放在同一个非 Git 目录里，于是小/大两个夹具改成同一仓库的两个 `git worktree add`——这既修好了夹具，也把"一任务一 worktree 一存储"钉成了测试。新增 5 例（无记录、能力名不符、kind 不符、`considered` 类不符、计数），并用改动前的 `hooks/task` 复跑同一段确认新断言会红。
- 2026-09-28 — Step 5 完成。契约文档改为"门在写入时拦、Skills 段是报告"：删掉 `prd.md` 前先写 `[PRD]` 的顺序纪律与"必须是选择而非疏忽"的说教，`artifacts.md` 的 before 要求同步删除，`runtime.md` 补 `PreToolUse` 行、门的独立小节、实测版本（Claude Code 2.1.282）与非 Claude Code host 无门，双语 README 对应改写。顺带修掉两处既有文档/实现矛盾：`task` 子命令列表缺 `unaided`；Plan 模板的 Skills 示例无 stage 标签，照抄必被 approve 拒。
- 2026-09-28 — Step 6 完成。**Windows 套件本机跑通**（此前一直列为未跑），并新增"门 + 逃生舱"段，经真实启动器在一个含空格与中文的仓库路径上驱动；为此实测出一个测试宿主的坑：PS 5.1 管道会写入 UTF-8 BOM，而解析器视 BOM 为非法 JSON，于是门静默 no-op、测试会假装通过——改成无 BOM 文件 + `cmd` 重定向后才有区分力，并把 BOM 记为 fail-open 的独立遗留项。无解释器段补上两个新钩子。静态下限零命中。CHANGELOG 加 `[Unreleased]` 段（查历史确认这是本仓库 feature 分支的惯例，且 `release-check` 会跳过它）。更正计划里的一条错误认知：`tools/fixture-compare` 是夹具比对器而非静态检查器，`runtime.md` 里那句错误归因一并改正。

## Follow-ups

- 发版后执行 Verification / Review 里的 1–5 配方，把真实会话结果回填本 Plan；未验证前不得宣称端到端保证。
- 定案 MCP matcher 写法（裸 `mcp__` 前缀匹配 vs `mcp__.*`），记入 `references/runtime.md`。
- Research 阶段（`reference/index.md`）是否也需要写前门——本任务有意未覆盖。
- Codex / CodeBuddy / dsh 三 host 的等价接线；接线前需先摸清各 host 是否有 tool-call 级钩子。
- 证据防伪的下一层：`Bash` 仍可绕过 I2。若有需要，考虑签名或把存储移出 Agent 可达路径。
- **BOM 会让两个新钩子静默 no-op**（fail-open）：`json-field` 对开头带 UTF-8 BOM 的事件报 `exit 2`，钩子随即 `exit 0` 什么都不做。实测 BOM 来自 PowerShell 把字符串管进原生命令，宿主事件里没有；`session-start` 共享同一套解析器，因此这是仓库级决定而非本任务能顺手改的一行。若判定值得，应在解析器入口统一剥离 BOM 并同时覆盖三个钩子。
- `hooks/task:251` 把 `Owner: Codex` 写死（intake 在任何 host 都填 Codex）；本任务未处理，应作为独立条目。

## Version History

- v1 — 前置门 + 证据存储 + `task unaided` 逃生舱 + approve 对账；v1 只接 Claude Code；stage 记录移出 `plan.md`；谓词限定 `Skill`/`Agent`/MCP。
