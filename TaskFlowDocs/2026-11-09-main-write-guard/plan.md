# Plan — 防止开发任务修改基础工作区
> Task version: v5
> Status: in_progress

## Spec Pointers
- `spec.md`

## Reference Pointers
- `TaskFlowDocs/repository-docs/index.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`：工作树隔离、跨宿主覆盖、审批和测试规则。
- `hooks/capability-gate`、各 `hooks/hooks*.json`、`skills/taskflow/references/runtime.md`：现有事件适配与限制。
- https://learn.chatgpt.com/docs/hooks：Codex 事件覆盖、信任和限制。

## Related Tasks
- Todo: TF-20261109-e2df6d；后续关联 TF-20261109-293987（能力对齐）和 TF-20261109-3c1409（用户可见性）。
- Follows: `TaskFlowDocs/achieved/2026-09-16-capability-selection-enforcement/`（提升门禁与隔离规则）；本任务增加写入保护。

## Skills / Tools Used
- [PRD] Unaided — no capability applied to this phase; considered: requirements elicitation and framing.
- [Spec] Unaided — no capability applied to this phase; considered: architecture and design specification.
- [Plan] `agent-skills:planning-and-task-breakdown`：形成可验证步骤；任务文件按 TaskFlow 作为唯一事实源。
- [Research] `openai-docs`：核对 Codex 官方 hook 事件与限制。

## Preconditions
- worktree `.worktrees/2026-11-09-main-write-guard`，分支 `fix/2026-11-09-main-write-guard`。
- 不修改或清理基础工作区的其他 Todo 与未跟踪文件。

## Plan Review
- Verdict: 用户同意保留当前会话、写前门与非阻断变化检测；隔离仅作为可选增强。
- Coverage: 文件编辑门、跨宿主、例外和限制。
- Verifiability: 独立 Git 仓库夹具与条件允许时的真实宿主测试。
- Layer ownership: hook 拒绝可识别编辑事件；宿主权限策略负责沙箱内命令，不能由 hook 假装设置。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-10
- Approved version: v5
- Approved scope: 用户选择异步、轻量状态提示，接受事后发现并纠正；保留已批准的文件编辑门和可选隔离，不阻断命令或切换会话。

## Steps
### Step 1 — 核实事件及例外
- Goal: 对五宿主确认文件编辑事件、拒绝格式、路径与Todo 例外及发布限制，识别无法判断的场景。
- Dependencies: 无。
- Files: 各宿主接线、`runtime.md`、官方文档。
- Implementation checklist:
  - [x] 记录事件契约和证据等级，确定 Todo 例外；发布例外已延期。
- Acceptance: 每个宿主有可实现的行为或具体不支持依据。
- Verification: 官方事件契约与合成事件已核对；真实宿主尚未验证。
- Rollback: 无生产代码改动。
- Status: in_progress

### Step 2 — 写前守卫与各宿主接线
- Goal: 在支持的编辑路径拒绝写基础工作区，允许合法例外。
- Dependencies: Step 1。
- Files: `hooks/` 守卫和宿主接线；必要时 Skill 与 runtime 文档。
- Implementation checklist:
  - [x] 实现目标路径判断与可解释拒绝；写前判断所有可识别的 patch 目标。
  - [x] 对现有四宿主编辑门和 dsh 文件工具接线；记录真实宿主未验证。
- Acceptance: PRD 1、2、4。
- Verification: 基础/任务树、绝对路径、Windows、非项目及 Todo 的定向检查通过；自动 smoke 未运行。
- Rollback: 回退本步骤改动。
- Status: in_progress

### Step 3 — 验证与文档
- Goal: 验证行为、宿主覆盖和用户可见限制。
- Dependencies: Step 2。
- Files: `hooks/smoke-test`、Windows 测试、runtime 和相关 README。
- Implementation checklist:
  - [ ] 增加并运行相关自动测试；可能时运行真实 Codex 事件测试。
  - [ ] 审查 diff、更新文档，记录证据等级与不能覆盖的路径。
- Acceptance: PRD 全部验收条件；真实宿主不可测时明确标注。
- Verification: 定向测试、适用的 Windows suite、`git diff --check`、项目规定的技能校验。
- Rollback: 回退本任务变更。
- Status: pending

### Step 4 — 宿主权限隔离
- Goal: 以非阻断方式检测基础工作区变化；宿主权限隔离仅作为可选增强。
- Dependencies: 宿主能力与权限模型的实测结果。
- Files: TaskFlow 宿主接入、检测逻辑、测试和运行时文档，依实测确定。
- Implementation checklist:
  - [ ] 在项目内隔离夹具验证 Codex 的有效权限，分别测试基础路径与任务路径的命令读写。
  - [ ] 核实桌面/CLI 和其他已支持宿主是否可由 TaskFlow 申请或验证隔离；无法实现时明确状态。
  - [x] 基于 Codex 和 Claude Code 的异步事件提示基础工作区现存改动，并测试已有改动、失败与不可用场景；不维护快照。其他宿主异步能力和真实宿主显示仍待核实。
  - [ ] 可选隔离只在宿主支持、用户选择并实测通过时报告，不强制停止或切换会话。
- Acceptance: 不以提示或 hook 冒充文件系统权限；真实写入验证及覆盖边界有证据。
- Verification: 在夹具中实际尝试 PowerShell/Python 和文件编辑，核查文件内容与哈希。
- Rollback: 回退本步骤变更，不改全局用户配置。
- Status: pending

## Checkpoints
- shell 前后比较存在待决的性能边界：Codex 同步 PreToolUse 会等待快照完成才启动命令；异步 PreToolUse 与命令并行，无法保证快照先于写入。PostToolUse 可异步，但不能补回缺失的可靠基线。大型仓库、已存在的未跟踪文件及并发写入还会增加扫描成本与不确定性；尚未实现该检测，不把异步竞态或已有脏状态当作可靠结果。
- 用户明确不同意因权限不满足而停止实施并要求开启新会话；不自动重启、切换聊天或修改全局配置。仅继续研究可在当前会话中使用的非破坏性方案；无法建立完整边界时如实报告。
发布例外按用户 2026-11-09 指示推迟至 TF-20261109-ccbb96；本版本不声称发布编辑不受影响。

## Verification / Review
- PR #128 CI run 42741613966 的 Linux/macOS smoke 在能力门旧夹具失败：该夹具在基础工作区模拟任务写入，新增守卫按设计拒绝，导致原有证据释放断言未通过。已将该夹具改为真实 linked worktree 后重跑 CI；本次不改变守卫放行策略。
- 2026-11-10 草稿 PR 前合入最新 main：手动合并 Todo、smoke 测试和 runtime 文档冲突；逐 ID 检查两个父版本的 Todo 均保留，冲突解决后 bash 守卫和提醒定向测试、Skill quick_validate 与 diff 检查通过。完整三系统 CI 仍待远端运行。
- PR 模板映射：Summary 描述编辑守卫与异步提醒；TaskFlow traceability 指向本任务、范围、`hkwuks/TaskFlow` 和 `main`；Verification 列出定向夹具、Skill 校验与 CI 状态；Review boundaries 说明 shell、宿主和发布例外的限制。任务尚未验收，以草稿 PR 交付审查，不能提前标记完成或归档。
- 2026-11-10 提交前：`PYTHONUTF8=1` 下 bundled Python 运行 Skill quick_validate 通过，`git diff --check` 通过；默认编码首次触发 GBK 解码失败，设置 UTF-8 后通过。远端 main 已前进，需核查 PR 合并情况。
- 2026-11-10 按用户要求补充 CI：复用现有三系统 `hooks.yml` smoke job；Windows 测试增加 Codex/Claude 异步配置、两个 Claude 事件和 Windows 启动器断言，Linux/macOS 继续运行同一 bash smoke 中的基础守卫和状态提示用例。`tools/workflow-affected` 确认相关路径会触发 smoke。项目内保留夹具中执行 bash 新增测试段和 Windows 测试原文提取段均通过；完整原版测试会删除临时文件，未在本地运行；GitHub Actions 尚未运行，不能据此声称三系统远端通过，也不能代替真实宿主异步投递验证。
- 2026-11-10：项目内独立 Git 基础仓库及 linked worktree 定向测试通过：干净状态、只有 Todo 改动不提示；已有源码改动、未跟踪文件和重复检查提示，且不归因；模拟 git status 失败提示无法检查；Windows `run-hook.cmd` 启动器和 Claude `PostToolUseFailure` 合成事件输出有效 JSON。夹具 `.guard-fixtures-20261110-async/` 保留，无文件删除。Codex/Claude JSON 异步配置、bash 语法及 git diff --check 通过；未在真实 Codex 或 Claude 会话验证新异步 hook 的投递及耗时。
- Claude Code 官方文档确认 `PostToolUse` 成功、`PostToolUseFailure` 失败事件及异步 hook；异步 `systemMessage` 在后续轮次发给 Agent，不直接显示用户。https://code.claude.com/docs/en/hooks#run-hooks-in-the-background 。
- 2026-11-09 再次核对 Codex 官方 hook 文档：同步 hook 会等待完成；异步 hook 可后台执行并在安全点输出提示，但可能乱序，未完成的 hook 在会话结束时取消。官方文档未提供异步前置快照必定早于工具执行的保证：https://learn.chatgpt.com/docs/hooks 。因此不能仅靠异步前后 hook 保证获得调用前基线。
- 硬链接边界：在隔离夹具中创建从任务 worktree 指向基础文件的 NTFS 硬链接；即使使用已验证的 MXC 策略（基础目录只读、worktree 可写），通过 Python 写入 worktree 的硬链接仍成功，基础文件 SHA-256 也随之变化。首次尝试因命令行转义失败，使用独立探针文件重试后确认。不得把该策略宣称为完整隔离；仅为单机单次夹具结果。
- 当前会话默认沙箱内尝试直接嵌套启动 `codex sandbox` + MXC，返回 `native MXC is unavailable on this executor`，探针未执行；不能据此假设 hook 可以在现有会话中为 shell 加套沙箱。独立提权测试进程的 MXC 结果仍有效，但不能推广到当前嵌套执行器。
- 2026-11-09 官方资料：Codex beta 权限配置支持精确路径优先级，旧 sandbox_mode/--sandbox 可能覆盖配置；app-server 的 thread/turn 客户端可提供 sandbox policy，但当前 TaskFlow 插件 hook 的公开事件契约只提供上下文及工具判定，尚未发现插件可直接收紧正在运行的桌面会话权限的接口。依据 https://learn.chatgpt.com/docs/permissions、https://learn.chatgpt.com/docs/hooks、https://learn.chatgpt.com/docs/app-server 。
- 独立 `codex sandbox` 和真实 `codex exec` 使用单次命令行配置、MXC 和合成夹具；测试并未证明已安装 TaskFlow 插件自动选择该配置，也不覆盖 MCP、授权提权和其他宿主。两个权限探针与日志均保留在 `.guard-fixtures-20261109-2207/`。
- 2026-11-09 MXC 权限实验：同一基础仓库内的嵌套 worktree，权限配置为基础只读、worktree 可写。`codex sandbox` + Python 实际观察基础写入 PermissionError、worktree 写入成功，随后复查文件存在状态。
- 真实 Codex CLI 使用同样的 MXC 权限配置：PowerShell 同一命令分别写基础路径与 worktree 路径，前者拒绝、后者成功；apply_patch 基础路径被项目权限拒绝、worktree 成功。另一次真实会话显式接入待测 hook，基础 apply_patch 被该 hook 拒绝，worktree apply_patch 成功。测试未代表已安装插件或其他宿主。
- 默认 Windows 沙箱在嵌套执行环境分别出现 CreateRestrictedToken 87 和 helper_unknown_error；显式 `windows.sandbox=mxc` 后夹具测试成功。MXC 下直接运行 Git Bash 失败（NtCreateDirectoryObject access denied），但真实 Codex 的 hook 路径已单独证实可执行并拒绝，不能把 shell 内失败直接当作 hook 失败。
- 权限配置仅约束受沙箱管理的本地命令，MCP、已批准提权等有独立控制；官方 hook 输入只暴露 permission_mode，PermissionRequest 的 updatedPermissions 不支持，因此尚未证明插件能为当前桌面会话设置或读取完整权限策略。
- 2026-11-09 真实 Codex CLI 测试：用户授权合成夹具联网后，使用临时配置显式加载本任务 `base-write-gate`（该会话跳过 hook 信任复核；未覆盖实际已安装插件），向基础工作区的 apply_patch 被 PreToolUse 拒绝，目标文件不存在。任务 worktree apply_patch 被只读沙箱拒绝；shell 调用被独立策略拒绝，二者均不能作为 hook 放行或拦截的证据。日志保存在 `.guard-fixtures-20261109-2207/`。
- 2026-11-09 真实 Codex CLI hook 测试：在独立夹具仓库启动临时会话，但模型请求受沙箱网络限制（os error 10013），未发生文件编辑；联网重试被自动审批拒绝，原因是可能把夹具内容传给未明确授权的外部服务。测试记录保存在 `.guard-fixtures-20261109-2207/codex-edit-test.jsonl`。
- 2026-11-09 实际 shell 绕过测试：在项目内独立测试仓库的基础工作区，PowerShell 与 Python 相继修改 `source.txt`，前后 SHA-256 均变化；测试文件保留最后的 Python 内容。当前守卫不拦截 shell，因此整体防止直接修改 main 的目标未达成。
- Windows 上使用实际基础工作区与任务 worktree，合成 PreToolUse 事件通过：主目录拒绝、任务目录与 Todo 放行、跨工作树 patch 与移动拒绝、dsh 形状拒绝、MultiEdit 拒绝；非 Git 路径放行、Windows 反斜杠路径拒绝单独通过。
- `bash -n hooks/base-write-gate`、`bash -n hooks/smoke-test` 和 `git diff --check` 通过。
- 官方 quick_validate 默认 Python 缺 PyYAML；Codex bundled Python 运行通过。
- Windows 上一次守卫调用约 0.52 秒，仅单次测量，非性能基准。
- 2026-11-09 补充：使用 digdig 事故目标模拟 patch 得到拒绝；Todo 普通更新放行，删除、移动和无法解析的 patch 拒绝；上述均为合成事件，非真实宿主拦截。
- 提取并执行 `hooks/smoke-test` 的 base checkout write guard 测试段：全部通过，使用工作树内 `.guard-fixtures-20261109-2207` 夹具；首次 `.guard-fixtures-20261109-2206` 因测试启动命令转义错误失败，两套均保留。
- Windows suite 的保留夹具副本 v3 通过 ASCII、启动器参数、SessionStart、生命周期、原有能力门及新增基础工作区门（五种工具名的基础/任务工作区与 Todo）；禁用了生成事件文件的删除和开放 stdin 子测试，指定项目内 Root。首次因 Git 向上找到外部工作树导致归档失败；第二次新增测试被 PowerShell 将 Git 警告当错误而中止，调整后重跑通过。设置 GIT_CEILING_DIRECTORIES 隔离真实仓库。并未执行原版完整 Windows suite 或真实宿主 hook。
- 在测试夹具中创建 Windows 符号链接时，系统要求管理员权限，未能执行符号链接实测；未请求提权。
- 经 Windows run-hook.cmd，空格与中文路径的 20 项合成事件通过；已把其中关键基础/任务工作区和 Todo 场景加入 Windows CI 测试。
- 未运行完整 smoke：脚本创建并递归删除临时文件，与用户不删除文件及不改项目外路径的要求冲突；真实 Codex 已测试基础工作区拒绝，但任务 worktree 放行被沙箱挡住；dsh 和其他宿主未真实测试。CI 和其余真实宿主验证仍待完成。
- 限制：shell、交互输入、绕过 hook 的工具、符号链接目标以及未启用或未信任 hook 可能绕过；发布编辑可能被拒绝，另见 TF-20261109-ccbb96。

## Change Log
- 2026-11-10：用户要求补充 CI，扩展既有 Windows smoke 覆盖宿主异步接线和失败事件，不新增 CI job。
- 2026-11-10 v5：用户选择异步并要求轻量；用事后 Git 状态提醒替代前后快照比较，不归因，已存在改动可重复触发。
- 2026-11-09 v4：用户同意保持当前会话、文件编辑保护、shell 变化的非阻断提示以及可选权限隔离。
- 2026-11-09 用户否决“停止实施并要求新会话”的提议；该提议尚未纳入 v3 已批准方案，本次仅记录约束并继续当前会话调查。
- 2026-11-09 v3：用户同意增加宿主权限隔离与 hook 两层方案；先验证权限能力及 TaskFlow 可接入方式，未授权修改全局配置。
- 2026-11-09 v2：按用户明确指示将发布例外延期至 TF-20261109-ccbb96，先实现写前防护；保留发布编辑可能受阻的限制。
- 2026-11-09 用户明确同意 v1，随后明确要求手动记入；`task approve` 因 Codex 未自动记录 Plan 技能调用而拒绝，批准字段据用户指示手动记录，未伪造证据，待 TF-20261109-293987 修复该缺口。
- 2026-11-09 建立计划；源 Todo 从基础工作区复制至任务 worktree，原条目保留。

## Follow-ups
- 其他宿主能力对齐由关联 Todo 跟踪。

## Version History
- v1 — planning。
- v2 — 延期发布例外并获用户确认。
- v3 — 加入宿主权限隔离与实际写入验证，用户同意。
- v4 — 隔离为可选，增加非阻断变化检测，用户同意。
- v5 — 用户选择异步、轻量的事后状态提示。
