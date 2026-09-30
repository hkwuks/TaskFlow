# Block the first body write of prd/spec/plan until a capability-class tool was ac
> Task version: v2
> Status: ready
> v2 只改一件事：门不得假设路径分隔符（R13/R14、A13/A14）。v1 的存储、谓词与逃生舱不变。

## Goal

把"写 PRD/Spec/Plan 时要调用专业能力"从一句散文规则变成可强制的前置门：门在 Agent 写这三份文档正文之前触发，校验的是**真实调用流**，而不是文档里的文字。

用户价值：现在 `task approve` 只校验 `## Skills / Tools Used` 的文字形状，且发生在三份文档全部写完之后，因此"什么都没调用"和"合规"在门禁眼里无法区分——`Unaided — …; considered: <概念词>` 与真调用等价，且可以在 approve 前事后补写。上游实测 59 个已完成 Plan 中该段为空或缺失的有 34 个。门移到写文档那一刻、证据改由 hook 记录真实调用之后，这条记录不再是 Agent 的自我声明。

## Background / Confirmed Facts

- 上游 `7eca4a8`（PR #56，v1.1.0）加入写前规则与 `task approve` 的 stage 门。其 PRD 自己把"阻止 `prd.md` 首次写入"的文件钩子列为 Out of Scope，并在 Risks 写明"时序靠 Skill 纪律 + stage 记录，不是 mtime 强制"，Follow-ups 里留了"hook that refuses first write to `prd.md` without a `[PRD]` line"。本任务就是兑现这一项。
- `hooks/task:831-879` 的 `require_stage` 只做形状校验，无产品白名单；缺失或形状不合即 fail closed，不写半截 Approval。
- 时序不可验证：检查点在 approve（三份文档都写完之后），Agent 可先无工具写完正文，再在 approve 前补三行标记。
- `hooks/hooks.json` 目前只接 `SessionStart` 一个事件。
- `references/runtime.md:88-92` 规定 hook **不得**创建/改写 `prd.md`/`spec.md`/`plan.md`、不得创建或改动 `## Approval`。本设计不触碰这两条。
- `references/runtime.md:110` 与 `hooks/README.md` 规定 hook 只能跑 bash 3.2 + BSD userland 下限的 POSIX sh，只用 `awk`/`sed`：不得出现 `declare -A`、`mapfile`、GNU-only `sed -i`。冒烟套件在"无解释器"的 PATH 下运行 hooks。
- `hooks/task promote` 已经一次性脚手架出 `prd.md`、`spec.md`（large）、`plan.md`，其中 `plan.md` 自带空的 `## Skills / Tools Used` 段，所以记录位一定存在。
- 本机已确认的能力类工具名（读本机会话 transcript 得到）：`Skill`（输入形状 `{"skill":"<plugin>:<skill>","args":"…"}`）、`Agent`、`mcp__<server>__<tool>`。
- 已确认的 Claude Code 钩子事实（子代理查官方文档所得）：`PreToolUse` 输入含 `session_id`、`transcript_path`、`cwd`、`tool_name`、`tool_input`、`tool_use_id`；当前正确的拒绝方式是 `hookSpecificOutput.permissionDecision: "deny"` 加 `permissionDecisionReason`（回喂给模型），exit 2 同样阻断；matcher 在纯字母/数字/`_`/`-`/空格/`,`/`|` 时是精确串列表，否则按无锚点正则解析，MCP 必须写 `mcp__.*`；`PostToolUse` 的 stdout **不进**模型上下文。
- **已实测（2026-09-27，临时探针）**：`Skill` **同时触发 `PreToolUse` 和 `PostToolUse`**；`tool_input.skill` 携带技能名（实测得到 `agent-skills:spec-driven-development`）；`Skill` 可作为 matcher 值；`PreToolUse` 对 `Edit` 触发。门的两个事件面都成立，证据链可以直接从钩子取能力 id，无需从文档文字推断。探针装上后立即生效，**无需重启会话**。
- **已实测：`~/.claude/settings.json` 的 hooks 是全机全局的**，对**每一个并发会话和每一个项目**都触发。探针装好后，日志里立刻出现了另一个会话在无关仓库（`D:\WorkSpace\PyCharm\QwenTuning`）编辑 plan.md 的记录。这不是本设计的假设，是实测事实，直接决定了 R8 与 A12：门必须**纯粹从文件路径**判定目标，在任何非活动 TaskFlow 任务目录上无条件 no-op，绝不能依赖"当前任务"这类全局状态。
- 仍待实测（低风险）：MCP 工具的 matcher 写法——裸 `mcp__` 是否按前缀匹配，还是必须写 `mcp__.*`。`context-mode` 用的是裸 `mcp__`，但它整体的 matcher 串全由字母/`_`/`|` 组成，按"纯字母数字串列表"解析时裸 `mcp__` 只能精确匹配名为 `mcp__` 的工具，与它的意图不符，所以两种解释都还站着。实现时用一次真实 MCP 调用定案。
- `transcript_path` 存在但是**异步落盘**（"may not include the current turn's most recent messages"），这是证据不用 transcript 的原因之一。
- 证据来源、逃生舱形态、host 覆盖范围三项已由用户于 2026-09-27 决策（分别为：hook 自写证据文件；`task unaided` 命令；v1 只接 Claude Code）。
- 本任务自身会吃自己的门：本仓库用 TaskFlow 管自己，但仓库里的 hooks 不生效于已安装插件（本机活动插件为 `1.1.0`，`~/.claude/plugins/installed_plugins.json`），所以本任务的文档写入不会被新门拦截。

### 适用仓库文档（已读，据 `TaskFlowDocs/repository-docs/index.md` 路由）

- `CONTRIBUTING.md`（design,code,commit,pr,release）：工作分支前缀 `feature|fix|docs|chore`，提交格式 `<type>: <imperative description>`，PR 前读 `.github/pull_request_template.md`。
- `CODE_STYLE.md`（code,review）：shell 用 `#!/usr/bin/env bash` + `set -euo pipefail`，退出码 `0` 通过 / `2` 需用户输入 / `3` 工作流阻塞；检查保持只读，除非脚本明确实现一次具名状态转移；复用现有 hooks，不新增依赖；双语 README 行为对齐。
- `LICENSE`（all）、`README.md` / `README.zh-CN.md`（design,roadmap）、`ROADMAP.md`（design,roadmap,release）。
- `.github/pull_request_template.md`（pr）：本任务会开 PR，字段需完整映射。
- `RELEASE.md` + `CHANGELOG.md`（release）：**改插件必须发版并重装才在真实会话生效**（见 Risks）。

### v2 新增事实（2026-09-30 实测，v1 的验收在真实宿主路径形态下不成立）

- **v1 的门在 Windows 上完全不生效**，且是静默的。已发布的 1.1.1 带着这个洞。
- **更严重的是它同时把生命周期卡死在 approve（2026-09-30 实测）**：只有门会写 `released`，而 `task unaided` 只写 `evidence`；门在 Windows 上从不触发，于是没有任何 stage 能被释放。实测 v2 任务执行 `task approve` → `approve blocked: stage [PRD] was never released by the pre-write gate`，**而它给出的补救命令（`task unaided PRD …`）在这个平台上正是死路**——命令会成功登记声明，但释放 stage 的那一步永远等不到。即 Windows 上新建或修订的任务都无法通过 approve，也就无法进入 `in_progress`、无法 `complete`。这条把"门不生效"从"少了一层保护"升级为"流程不可用"。
- 实测（本机 Windows + 装机包 1.1.1）：对项目内一个真实任务文档（同级有 `plan.md`、无证据）执行 `Write` → **被放行**；直接喂装机包的门，正斜杠 `/d/WorkSpace/.../prd.md` → **deny**，反斜杠 `D:\WorkSpace\...\prd.md` → **allow（空输出）**。
- 根因：门用 `task_dir="${file_path%/*}"` 取目录，`%/*` 只认正斜杠；反斜杠路径切不出分隔符 → `task_dir == file_path` → 命中"切不出目录即视为非任务文档"的守卫 → `exit 0`。**门假设了路径分隔符，而这是它最不该假设的东西。**
- 宿主行为由上游确认，不是本仓库的臆测：claude-code issue **#83877**（Windows 上 `tool_input.file_path` 以反斜杠分隔投递，匹配路径的 hook 会静默 fail open；外面无法区分"没被拦"与"本来无物可拦"）、**#64432**（Write 工具**总是**投递带反斜杠的 `file_path`，解法即 hook 内做分隔符归一）、#40076 / #52962（WSL2 下的同类）。
- **v1 的验证为什么没抓到**：Windows 套件里的 event JSON 是测试**自己拼**的，拼的时候写的是正斜杠——测的是测试所假设的形态，而不是宿主真实投递的形态。测试与实现对同一个假设犯了同一个错，于是双双通过。这是本条最值得记住的教训，也是 R14/A14 存在的原因。
- 证据钩子不受影响：实测它拿到的 `cwd` 是 `/d/...` 形态，且它只把路径交给 `git -C`，两种分隔符都能工作。

## Requirements

R1. **前置门**：在 Claude Code 上，Agent 对活动 TaskFlow 任务目录内 `prd.md`、`spec.md`、`plan.md` 的**正文写入**，在该 stage 尚无证据时被拒绝。
R2. **证据由 hook 产生，不由 Agent 声明**：能力类工具被真实调用后，由 `PostToolUse` 侧写一条证据记录。Agent 手写的文字不构成证据。
R3. **谓词是工具类别，不是产品清单**：不得引入"某阶段该用哪个工具"的映射，也不得做产品白名单。类别取 host 自己的工具分类（`Skill` / `Agent` / `mcp__*`）。
R4. **逐阶段新鲜度**：stage 证据在放行后被消费；下一个文档需要一次新的调用。同一次调用不得同时满足两个 stage。
R5. **逃生舱**：`hooks/task unaided <stage> --considered "<concept class>"` 一条命令登记该 stage 的 Unaided 决定并放行；缺 `--considered` 或概念类不命中相位词表则失败。**相位词表校验的唯一入口就是这里**——`task approve` 不再重复校验（见 R11 与 A9）。
R6. **证据不可由 Agent 写入**：门同时拒绝 Agent 对证据文件的 `Write`/`Edit`。
R7. **拒绝消息自解释**：必须给出缺失的 stage、该 stage 的概念类提示、以及可复制执行的逃生舱命令。这是规则送达的时机从 SKILL.md 中段移到"正要写文档"那一刻的手段。
R8. **生效边界**：仅活动任务目录；`TaskFlowDocs/achieved/**`、非 TaskFlow 目录、以及 TaskFlow 自身 transition 命令（Bash 调用）写核心文档均不受影响。
R9. **失败语义**：任何情况下不得把用户锁死——`task unaided` 永远可用；门自身出错时按拒绝处理，并在消息里说明是门出错而非用户违规。
R10. **复用既有件**：`require_stage` 的相位词表与判定逻辑、`promote` 已生成的 `## Skills / Tools Used` 段，以及 `CODE_STYLE.md` 的退出码约定。
R11. **记录的家从 `plan.md` 移到证据存储**（用户 2026-09-27 决定，解 OQ1）：`plan.md` 的 `## Skills / Tools Used` 从"写前声明"改为"由证据生成、被 `task approve` 对账的报告"。这是让三份文档能够**统一门控**的前提——只要 `plan.md` 还兼任写前记录位，它就无法在自己的 stage 上被门控。
R12. **谓词边界**（用户 2026-09-27 决定，解 OQ2）：能力类 = `Skill`、`Agent`（`Task`）、MCP 工具；**不含** `WebSearch`、`WebFetch`、`Read`、`Bash`、`Write` 等内建工具。若把内建搜索算作能力，门随手可满足，等于失效。
R13. **路径分隔符不得被假设**（v2，2026-09-30）：门在任何路径判断之前先把 `\` 归一成 `/`，此后所有切分、比较、`git -C`、`[ -f ]` 都在同一形态上进行。判据是"同一份文件的不同路径拼写必须得到同一判定"，而不是"某一种拼写能用"。
R14. **回归测试必须喂宿主真实投递的形态**（v2，2026-09-30）：测试不得自己构造一个"我认为宿主会投递的"路径形态。Windows 侧的用例必须喂**反斜杠**路径（宿主在 Windows 上的实际形态），bash 侧至少各喂正反斜杠一次；且该用例在"门不做归一"的实现上必须**失败**——否则它证明不了任何东西。

## Acceptance Criteria

A1. 新任务，本会话无任何能力类调用而直接写 `prd.md` 正文 → 写入被拒；消息同时含 stage 名、概念类、逃生舱命令。
A2. 先真实调用任一 `Skill`/`Agent`/MCP 工具，再写 `prd.md` → 放行。
A3. 写完 `prd.md` 后中间无新调用而直接写 `spec.md` → 被拒；中间再真实调用一次 → 放行（验证 R4 新鲜度）。
A4. 执行 `task unaided PRD --considered "requirements elicitation and framing"` 后写 `prd.md` → 放行；缺 `--considered` 或概念类不在词表内 → 失败且消息指明原因。
A5. Agent 用 `Write`/`Edit` 直接写证据文件 → 被拒（验证 R6）。
A6. `TaskFlowDocs/achieved/**` 下对同名文档的写入不被门拦截。
A7. 非活动任务目录，以及 `task promote` / `hooks/version` / `hooks/archive` 等 Bash 命令写核心文档 → 完全不受影响。
A8. `bash hooks/smoke-test` 与 `hooks/smoke-test-windows.ps1` 全绿，新增用例覆盖门与逃生舱；`tools/fixture-compare` 仍通过（无解释器 PATH、bash 3.2/BSD 下限）。
A9. 失败面不回退，但**校验位置**有一处迁移，必须写清：缺 `[PRD]`/`[Spec]`/`[Plan]`、Unaided 缺 `considered:` 仍在 approve 失败；而"概念类不合词表"改在 `task unaided` 入口失败（唯一入口），approve 不再重复校验——那段文本已由存储保证。验收方式相应改为：`task unaided` 传不合词表的概念类必须失败，且此刻存储零变化。
A10. `skills/taskflow/SKILL.md`、`references/artifacts.md`、`references/runtime.md` 记录新门的契约与事件映射（含"Claude Code 的守卫事件用 `PreToolUse`"这一偏离现有事件映射表的说明）；`README.md` 与 `README.zh-CN.md` 行为对齐。
A11. 记录门所依赖的钩子契约是针对哪个 Claude Code 版本实测的（`runtime.md` 要求：host 事件名与输出字段对版本敏感）。
A12. 门与证据钩子在**非活动 TaskFlow 任务目录**上完全 no-op：覆盖同机并发会话、无关仓库、`TaskFlowDocs/achieved/**`。本机实测 hooks 是全机全局的，所以这条不是理论边界而是正确性条件，必须有对应用例。
A13. （v2）**同一份文件的不同路径拼写得到同一判定**：在 Windows 上，反斜杠路径与正斜杠路径在无证据时同样被拒、有证据时同样放行；反斜杠形态的非任务目录与 `TaskFlowDocs/achieved/**` 仍 no-op。本机实测（正斜杠 deny / 反斜杠 allow）即 v1 在此条上的失败证据。
A14. （v2）反斜杠用例在**不做归一**的实现上会红：这条断言必须能区分"门真的在把守"与"门静默放行"，否则重犯 v1 那个"测试与实现共享同一个错误假设"的错。
A15. （v2）**逃生舱在自己的平台语义下闭环，approve 因此可用**：在 Windows（反斜杠路径）上，`task unaided <stage> --considered "<class>"` 之后写该 stage 文档，门必须放行**并写出 `released` 记录**，随后 `task approve` 通过。判据是"这条命令真的把人从锁死里救出来"，而不是"它自己退出 0"——v1 恰恰是后者成立、前者为空。

## In Scope

- `hooks/hooks.json`：新增 `PreToolUse`（门）与 `PostToolUse`（证据）接线。
- 新增证据写入脚本与前置门脚本（扩展名无关的 POSIX sh）。
- `hooks/task`：新增 `unaided` 子命令。
- `hooks/smoke-test`：门与逃生舱的用例。
- `skills/taskflow/SKILL.md`、`references/artifacts.md`、`references/runtime.md`：契约与事件映射。
- `README.md`、`README.zh-CN.md`：行为对齐。
- `CHANGELOG.md` 与 marketplace pin（发版才生效，见 Risks）。

## Out of Scope

- **不保证相关性。** 门只能保证"类别上有工具被调用过、且发生在写文档之前"，不能保证调用的是*对的*能力。要保证相关就必须引入阶段→工具的映射（用户明确不要）或模型评审（非确定性、且会让门变成可争议的）。这是本设计的天花板，不是遗漏。
- `reference/index.md` 与 Research 阶段的前置门（相位表里有这一阶段，但用户诉求集中在 PRD/Spec/Plan）。
- Codex / CodeBuddy / dsh 三个 host 的接线（用户决策：v1 只接 Claude Code）。非 Claude Code host 上保持现状，即仅 approve 时的形状校验。
- 不引入文件监听 / mtime 强制；不做证据的密码学防伪（见 Risks 的天花板声明）。

## Risks / Deferred Items

- **改仓库不生效。** v1 写作时本机活动插件是 `1.1.0`，仓库改动要发版重装才进真实会话；**v2 起这条已实测成立**：1.1.1 已发布并安装在本机，门确实在会话里触发了（证据钩子写入了真实记录）——也正因为装上了，才在真实路径形态下暴露出反斜杠 fail-open。修好之后同样需要再发一版才惠及用户。
- **（v2）路径形态是枚举不完的。** R13 只归一分隔符，不能证明覆盖了 Windows 的全部形态：UNC（`\\server\share\...`）、扩展长度前缀（`\\?\C:\...`）、以及宿主未来可能改成 `/c/...` 或 `C:/...`。归一是必要条件而非充分条件。缓解：判据写成"同一份文件的不同拼写必须同判"（A13），并在用例里至少覆盖反斜杠这一种**已实测的真实形态**；其余形态作为已知未覆盖项写进 Plan，不假装已证。
- ~~两条未实测的钩子事实落在关键路径上~~ — 已于 2026-09-27 实测解除，证据链成立（见 Background）。残余未知只剩 MCP matcher 的写法，且它不影响 Skill/Agent 两条主路径。真正的残余风险换成了另一条：**门是全机全局的**，所以"no-op 边界"从设计细节升为必须被 smoke 覆盖的正确性条件（A12）。
- **`plan.md` 的双重身份**是本次审查发现的最尖锐问题：`plan.md` 既是 stage 记录的家（SKILL.md 要求写 `prd.md` 之前先往它里面追加 `[PRD]` 行），又是被门控的文档。因此它无法在"首次写入"上被门控——加 `[PRD]` 行本身就是对 `plan.md` 的首次写入。**用户已于 2026-09-27 决定取 OQ1(b)**：把 stage 记录的家移出 `plan.md`，见 In Scope 与 Requirements R11。
- **证据文件的可信度是纪律级，不是密码学级。** 门可以拒绝 Agent 用 `Write`/`Edit` 写证据文件（R6），但 Agent 仍可用 `Bash` 写。要真正堵死需要签名或放进门禁不覆盖的位置；v1 接受这一残余风险并明确声明。
- **compact / resume 会换 session id**，所以证据不能按会话存，否则一次压缩就会把合法的继续写入拦死。证据的范围划分见 spec 的设计决策。
- **谓词边界决定门的强度。** 若把 `WebSearch`/`WebFetch` 之类内建工具也算作能力，门几乎随手可满足，也就失去意义。默认取 `Skill`/`Agent`/`mcp__*`，见 Open Questions OQ2。
- **子代理写入**：子代理的 `PreToolUse` 输入带 `agent_id`/`agent_type`。核心文档同时只允许一个具名 owner 写入，但门对子代理写入的行为需要一条明确判定。
- **宿主裁剪**：`runtime.md` 的"Must / may-not"要求 hook 失败时 fail safe、不留半截核心写入。门只做允许/拒绝，不写核心文档，天然满足；但需要在 smoke 里验证门出错时不产生副作用。
- 留作 follow-up：Research 阶段门控；Codex/dsh/CodeBuddy 接线；把 approve 的形状校验升级为"记录 vs 证据"对账。

## Open Questions

无阻塞项。三项在 2026-09-27 全部定案：

- **OQ1 → (b)**：stage 记录的家从 `plan.md` 移到证据存储，`plan.md` 的 Skills 段改为对账报告。理由：只要 `plan.md` 兼任写前记录位，它就无法在自己的 stage 上被门控，(a) 只是把洞缩小而不是补上。代价是 `SKILL.md` 与 `artifacts.md` 措辞要改。见 R11。
- **OQ2 → 只算 `Skill`/`Agent`/MCP**：不含内建搜索与读写工具。见 R12。
- **钩子未知项 → 已实测**：`Skill` 同时触发 PreToolUse/PostToolUse，`tool_input.skill` 带能力名，`Skill` 可作 matcher，PreToolUse 对 `Edit` 触发。见 Background。

唯一的残余未知（MCP matcher 写法）不阻塞设计：它只影响第三条谓词分支，且实现时用一次真实 MCP 调用即可定案。

## Version History

- v1 — 前置门 + hook 证据存储 + `task unaided` 逃生舱；v1 只接 Claude Code；stage 记录移出 `plan.md`（OQ1(b)）；谓词限定 `Skill`/`Agent`/MCP（OQ2）；门依赖的钩子事实已于 2026-09-27 实测。
- v2 — 修正 v1 在 Windows 上的静默 fail-open：门按 `file_path` 的路径形态取目录，而宿主在 Windows 上投递**反斜杠**路径，切不出分隔符即静默放行。新增 R13（分隔符不得被假设）、R14（回归测试必须喂宿主真实形态）、A13/A14。范围只有"归一 + 回归测试 + 文档"，不改谓词、不改存储、不改逃生舱。
