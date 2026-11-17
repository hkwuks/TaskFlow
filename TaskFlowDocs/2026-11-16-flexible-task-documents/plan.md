# Plan — 放宽 TaskFlow 文档内容约束
> Task version: v1
> Status: checking

## Spec Pointers

- `spec.md`

## Reference Pointers

- Repository document: `CONTRIBUTING.md` — 使用独立任务分支，代码与任务文档保持一致。
- Repository document: `CODE_STYLE.md` — 任务文档和 shell 使用既有约定，不引入额外依赖。
- Repository document: `README.md` — 验证现有生命周期说明和平台测试命令。
- Repository document: `LICENSE` — 项目使用 AGPL-3.0，不改变许可。

## Related Tasks

- 关联 `TF-20261110-84d1a9`：该任务审视总体流程与 Token；本任务独立处理文档扩展与解析兼容。

## Skills / Tools Used

- [PRD] Declared `agent-skills:spec-driven-development` — 用六个规格维度拆解目标和验收，依据仓库任务文档格式归档。
- [Spec] Declared `agent-skills:spec-driven-development` — 使用边界、接口、测试与成功标准组织设计。
- [Plan] Declared `agent-skills:planning-and-task-breakdown` — 将调查、修复与验收拆成可验证步骤。
- [Test] Unaided — 初始测试策略以仓库脚本制定；considered: testing strategy
- 实际读取并使用 `agent-skills:test-driven-development`：先复现审批、归档和步骤问题，再添加回归与修复；宿主没有记录技能调用事件。

## Preconditions

- [x] 用户批准 v1 范围与实施计划。

## Plan Review

- Verdict: sound
- Coverage: 验收 1–3 由步骤 1–2 调查与修复并以生命周期测试验证；验收 4–6 由步骤 2–3 的反例、回归、文档对照和复杂度样例审查覆盖。
- Verifiability: 各步骤的检查分别验证根因、正反例及完整生命周期，不能把示例检查当作真实审批验证。
- Layer ownership: 在负责读取或写入的解析层修复误判；不通过改测试期望或伪造流程标记绕过检查。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-16 22:33 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 调查扩展内容和解析边界

- Goal: 追踪 PRD、Spec、Plan 的相关读取与写入，重现误判，并调查模板、工具输出路由和审查引导是否造成内容过度压缩。
- Dependencies: 用户批准。
- Files: `hooks/task`, `hooks/completion-gate`, `hooks/approval-check`, `hooks/version`, `hooks/archive`, 现有测试和技能说明。
- Implementation checklist:
  - [x] 列出调用者及相关解析规则，重现误判。
  - [x] 将发现和具体修复边界记录在计划中。
- Acceptance: 明确何处允许附加内容，何处存在可复现的错误及其责任层。
- Verification: 针对现有生命周期路径执行最小反例并记录输出。
- Rollback: 不修改产品行为；保留调查证据。
- Status: done

### Step 2 — 修复解析与内容保留

- Goal: 允许约定范围的工具补充内容，同时保留必需字段和真实未完成事项检查；按复杂度引导保留实施和验收所需细节。
- Dependencies: Step 1。
- Files: 由 Step 1 确定的责任 hooks、相关现有测试和 TaskFlow 技能文档。
- Implementation checklist:
  - [x] 先编写覆盖真实误判及安全反例的失败测试。
  - [x] 在责任层做最小修复，并更新说明。
- Acceptance: PRD 验收 1–4 的正反例通过，修改后内容保留。
- Verification: 针对性测试及相关平台测试；检查每项真实阻断仍生效。
- Rollback: 使用本任务版本的 Git 回退点恢复变更。
- Status: done

### Step 3 — 生命周期验证与审查

- Goal: 核对文档、实现和用户验收的一致性。
- Dependencies: Step 2。
- Files: 任务计划和验证记录；必要时补充测试。
- Implementation checklist:
  - [x] 测试真实审批、状态、版本与归档路径及补充内容保留。
  - [x] 运行适用的 smoke、Windows 测试与 diff 检查并审阅变更。
- Acceptance: 六项验收各有证据，使用简单与复杂任务样例审查内容充分性，限制与未覆盖情况明确。
- Verification: 在 Verification / Review 章节记录命令和结果。
- Rollback: 回退本版本提交，不删除用户内容。
- Status: done

## Checkpoints

- v1 基线为任务创建时的 `origin/main` 提交；代码变更在本版本完成前建立 Git 提交。

## Verification / Review

- 2026-11-16 定向复现：围栏示例中的未勾选项曾阻止完成，示例审批曾被当作有效批准，重复审批章节曾被合并解读；修复后均按预期处理，真实未勾选项和未闭合围栏仍拒绝。
- 2026-11-16 定向复现：步骤更新、任务状态和版本转换曾改写围栏示例；步骤、状态更新和版本正例均已通过定向复测。
- 2026-11-16 定向复现：审批写入曾改写围栏中的示例审批块；修复后重放样例保留原文，真实审批仍写入。
- Git 回退点：`cc40415`、`4b1352b`、`7fdd165`、`ebe5a32`。
- 运行边界：首次完整测试因误判 Git Bash 的 `/tmp` 路径而中断，不计为通过；经 Windows 文件系统确认该目录实际映射到项目内 `reference/test-temp`。后续显式设置项目内临时目录和测试根目录。

- 规划调查：`hooks/completion-gate` 的全文件未勾选项匹配未排除围栏；`hooks/task` 按标题截取若干保留章节。后续已执行行为回归，结果见下。

- 验收 1、2：`hooks/smoke-test` 完成门及步骤/状态测试段通过；版本切换和归档定向样例确认补充章节、示例及已有 Todo Record 内容保留。
- 验收 3、4：重复审批章节、审批字段、步骤编号、计划审查；空批准人、未闭合围栏、真实未完成事项均拒绝；未闭合状态更新与未完成直接归档未改变原任务。归档正常对照通过。
- 验收 5、6：`skills/taskflow/SKILL.md` 与 `references/artifacts.md` 说明必需内容为下限、按复杂度保留细节并按可实施性审查；对照简单 README 任务和复杂远程 Issue 任务，避免以字数判断质量。`quick_validate.py skills/taskflow` 使用 torch 环境与 `PYTHONUTF8=1` 通过。
- Windows 全量 `hooks/smoke-test-windows.ps1`：隔离根 `reference/test-temp/windows-run-03`，通过含打开 stdin 的自检；该运行早于最后一轮重复字段/归档位置补充。最新代码的完成门、步骤、状态和归档 smoke 专项通过；审批专项在最终空白批准人微调前通过，最终门禁专项覆盖该微调。
- 完整 Bash smoke 在本机精简 PATH 环境中因 Git Bash 的模拟链接缺少运行库而失败；已确认本机无权限建立原生符号链接，因此该项未通过，不计为产品失败或全套通过。
- `bash -n` 检查修改过的 hooks 通过；`git diff --check` 通过。未在 Linux / macOS 实机运行；未执行真实外部工具生成文档的宿主端到端验证，工具输出能力不能由格式测试证明。
- 层归属：修改 `approval-check`、`completion-gate`、`task`、`version`、`archive` 的实际读写逻辑并新增元数据读取器；未通过篡改旧期望伪造通过。新例测试示例内容和真实未完成事项的不同结果。
- PR 模板 `.github/pull_request_template.md`：Summary 说明补充内容与解析修复；TaskFlow traceability 记录任务、范围、目标仓库及 base；Verification 记录 CI、diff 和技能校验；Review boundaries 记录范围、隐私和剩余限制。CI 尚待 PR 创建后运行。
- 2026-11-17 PR #144 首次 CI：Ubuntu 大文档门禁测试因旧夹具包含重复审批状态而失败；将非结构性尾行改为普通说明，并新增明确的 `unchecked items` 拒绝原因断言，保留原大文件与管道边界覆盖。macOS Bash 3.2 无法解析 Task AWK heredoc 中不成对的反引号，改为等价字符编码；Windows CI 通过。上述是本任务实现及测试的工作修订，不改变批准范围。
- 2026-11-17 当前工作树完成门专项（含 >64KB 未勾选反例及 50 次大批准块）通过；修改后的 macOS Bash 3.2 行为等待 CI 实证。
- 2026-11-17 CI：代码提交 `90c9fee` 的 Hooks 工作流 https://github.com/hkwuks/TaskFlow/actions/runs/43999790222 通过 Ubuntu、macOS 和 Windows smoke、evals、Todo 合并审计及 CI 复用检查；release 为按条件跳过。macOS Bash 3.2 与大文档门禁均得到 CI 复验。
## Change Log

- v1 工作修订：按已批准验收补充围栏示例和审批歧义的实际根因与回归；PR CI 暴露的本任务夹具及 Bash 3.2 问题已修复，等待复验；不改变任务范围。

- v1：建立初始规格与计划；按用户补充加入文档内容充分性与防止过度压缩的引导和验收（批准前修订）。

## Follow-ups

- 本机完整 Bash smoke 因 Git Bash 符号链接限制未通过；Linux 和 macOS 已由 CI 验证，真实宿主工具输出仍待验证。
- 本次测试自建夹具已按用户授权清理；任务文档已提交，等待验收。

- 若解析范围或安全边界需要偏离批准规格，先更新版本并重新确认。

## Version History

- v1 — planning。
