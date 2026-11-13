# Plan — TaskFlow 脱敏诊断日志与导出
> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md`

## Reference Pointers

- [Reinforce] `CODE_STYLE.md` — 代码风格、隐私及兼容约束。

## Related Tasks

- 关联 `TaskFlowDocs/2026-11-12-capability-outcomes/` v1：日志为后续正式安装排查提供独立交付；不宣称完成原任务的行为验收。

## Skills / Tools Used

- [PRD] Declared `agent-skills:spec-driven-development` — purpose: 形成可验收的需求和隐私边界；outcome: 区分可观测事件、未知原因和导出；incorporated: PRD 要求及验收。
- [Spec] Declared `agent-skills:spec-driven-development` — purpose: 设计事件和数据边界；outcome: 允许列表、重新校验、失败语义；incorporated: Spec。
- [Plan] Declared `agent-skills:planning-and-task-breakdown` — purpose: 设计依赖顺序及可验证步骤；outcome: 拆分事件核实、实现和独立验收；incorporated: Steps。
- [Test] Declared `agent-skills:security-and-hardening` — purpose: 考虑敏感输入和信任边界；outcome: 密钥、代码、恶意记录及失败场景；incorporated: 测试要求。
- `agent-skills:observability-and-instrumentation` — purpose: 设计可回答的问题；outcome: 事件、结果与宿主可见性分开；incorporated: Spec。

## Preconditions

- 使用项目内工作树 `D:/WorkSpace/Agent/TaskFlow/.worktrees/capability-outcomes`，分支 `fix/taskflow-capability-outcomes`。
- 已确认默认关闭、指定本地导出和允许列表；不记录用户内容，不阻塞运行。
- 项目规则 `CONTRIBUTING.md`、`CODE_STYLE.md`；任务事实以当前文档为准。

## Plan Review

- Verdict: sound — 方案覆盖已确认需求；具体宿主支持必须先验证。
- Coverage: Step 1 核实事件及隐私契约；Step 2 实现启停、异步记录与导出；Step 3 覆盖安全、非阻塞和宿主结果；Step 4 审查、提交和交付。
- Verifiability: 每项行为均由导出内容、可控阻塞测试和宿主事件检查；无法观察的原因不宣称已知。
- Layer ownership: 宿主决定可见事件，TaskFlow 负责允许列表、非阻塞采集与安全导出，用户负责正式安装后的实际场景测试。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-13 13:29 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 核实宿主事件与数据边界

- Goal: 确认可记录事件、异步机制和具体隐私边界。
- Dependencies: v1 方案获批。
- Files: 宿主 hook 配置与运行时说明。
- Implementation checklist:
  - [x] 核对宿主事件、异步语义及覆盖限制，确定固定事件与能力分类。
- Acceptance: 每个字段均有来源和允许范围，不能推断的事实明确标未知。
- Verification: 接线与受控事件对照。
- Rollback: 只更正任务记录。
- Status: done

### Step 2 — 实现诊断与导出

- Goal: 实现默认关闭、非阻塞记录和安全的本地导出。
- Dependencies: Step 1。
- Files: `hooks/`、宿主配置、TaskFlow skill、README。
- Implementation checklist:
  - [x] 实现用户启停、异步固定枚举记录和安全导出；更新用户说明。
- Acceptance: 不写用户内容；导出仅写指定新文件；不自动上传。
- Verification: 功能与格式测试。
- Rollback: 回退本步骤提交，不删除用户日志。
- Status: done

### Step 3 — 安全、非阻塞与真实宿主验证

- Goal: 验证泄露防护、日志故障和实际事件路径。
- Dependencies: Step 2。
- Files: 现有测试与项目内临时夹具。
- Implementation checklist:
  - [x] 测试敏感输入、恶意记录、默认关闭、导出失败、并发和受控阻塞。
  - [x] 运行适用 smoke、离线评估和至少一个受授权真实宿主场景，记录覆盖边界。
- Acceptance: 隐私和非阻塞测试通过，测试材料及宿主限制可审计。
- Verification: 命令、结果及脱敏证据。
- Rollback: 按授权清理本次测试夹具，保留用户数据。
- Status: done

### Step 4 — 审查与交付

- Goal: 审查差异，提交版本回退点，为用户 PR 与发布准备结果。
- Dependencies: Step 3。
- Files: 变更及任务记录。
- Implementation checklist:
  - [x] 完成审查、Git 提交、记录验证与限制。
- Acceptance: 代码、说明和测试一致；不擅自推送、合并或发布。
- Verification: `git diff --check`、Git 状态与提交检查。
- Rollback: 按提交回退。
- Status: done

## Checkpoints

## Verification / Review

- Windows 与 WSL 的 `hooks/test-diagnostic-log` 通过：默认关闭、后台入口、合成密钥和代码不落盘、恶意记录过滤、并发格式、固定技能及命令中提及的分类、禁覆盖和人为延迟的 Git/存储检查。事件记录采用异步旁路；合成阻塞测试验证入口在等待上限前返回，不证明所有文件系统和宿主都无延迟。
- 在 WSL 的 Windows 挂载目录复现并发追加丢失少量事件；保留记录格式完整，日志为尽力记录而非完整审计。达到约 1 MiB 停止追加，文档已说明。
- Windows 完整 smoke（包括最终诊断测试入口、双 shell 配置和开放 stdin）通过。`python evals/runner.py` PASS (6)；WSL Python 运行技能校验通过。Windows 默认 Python 缺 PyYAML，未安装依赖。
- 创建并临时安装本地测试插件，随后通过正式 CLI 移除插件和市场，核实缓存副本及市场均不存在，官方更新保留；第二轮真实宿主测试后再次移除插件与市场，精确删除其 11 个 hook 状态并以 TOML 结构对比确认其他配置不变。当前 computer-use 技能禁止操作 Codex CLI 和安全权限界面，无法自动信任测试 hook；用户手动信任指定诊断 hook 后，在受监控合成仓库运行 `codex exec --json --sandbox read-only`，会话和答复完成、退出 0，未观察到工具调用；项目日志出现 session 和 prompt 两条事件，用户指定本地路径的 JSONL 导出仅含五个允许字段。此次未覆盖真实宿主的工具调用事件或其他宿主，不能推断其行为。Linux 全量 smoke 的首次夹具准备因 Windows Git 工作树路径不适用于 WSL 失败；第二次复制时误排除诊断脚本而失败。修正后暴露旧的固定命令数量断言和两个脚本清单未更新；补充逐宿主逐事件接线断言及清单后，在私有 tmpfs 中重跑得到 `ALL SMOKE PASSED`。
- 自审：日志仅输出固定枚举与生成的时间，导出重新校验、通过硬链接发布而不覆盖现有目标；不支持硬链接的目标文件系统将返回失败。提及分类仅表示工具输入含固定技能名，不证明成功读取或采用；不记录原命令。

- 代码提交 `7218bfa`，检查记录提交 `67617a5`；最终验收记录将另行提交。

## Change Log

- 2026-11-13：用户确定默认关闭、本地指定路径导出、仅允许列表元数据；日志不阻塞被观察代码。
- 2026-11-13：实现固定类别的命令提及识别，只保存枚举，不保存命令；与已批准范围一致，属于工作修订。

## Follow-ups

## Version History

- v1 — planning。
