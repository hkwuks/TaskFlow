# Plan — 防止开发任务修改基础工作区
> Task version: v2
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
- Verdict: 用户已同意 v2 范围；真实宿主与完整 smoke 尚待验证。
- Coverage: 文件编辑门、跨宿主、例外和限制。
- Verifiability: 独立 Git 仓库夹具与条件允许时的真实宿主测试。
- Layer ownership: hook 拒绝可识别的编辑事件；权限沙箱不由 TaskFlow hook 伪造。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-09
- Approved version: v2
- Approved scope: 用户明确指示发布例外记入 Todo、暂不处理并继续修复当前任务。

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

## Checkpoints
发布例外按用户 2026-11-09 指示推迟至 TF-20261109-ccbb96；本版本不声称发布编辑不受影响。

## Verification / Review
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
- 2026-11-09 v2：按用户明确指示将发布例外延期至 TF-20261109-ccbb96，先实现写前防护；保留发布编辑可能受阻的限制。
- 2026-11-09 用户明确同意 v1，随后明确要求手动记入；`task approve` 因 Codex 未自动记录 Plan 技能调用而拒绝，批准字段据用户指示手动记录，未伪造证据，待 TF-20261109-293987 修复该缺口。
- 2026-11-09 建立计划；源 Todo 从基础工作区复制至任务 worktree，原条目保留。

## Follow-ups
- 其他宿主能力对齐由关联 Todo 跟踪。

## Version History
- v1 — planning。
- v2 — 延期发布例外并获用户确认。
