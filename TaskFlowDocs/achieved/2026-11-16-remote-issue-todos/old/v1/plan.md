# Plan — 远程 Issues 待办
> Task version: v1
> Status: in_progress

## Reference Pointers
- `TaskFlowDocs/repository-docs/index.md`、`LICENSE`：文档路由和所有阶段规则。
- `README.md`、`README.zh-CN.md`：现有本地工作流和双语用户说明。
- `CONTRIBUTING.md`、`CODE_STYLE.md`：任务分支、批准、CI 和 shell 规范。
- `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`skills/taskflow/references/runtime.md`：插件流程、产物和宿主行为。
- `hooks/task`、`hooks/archive`、`hooks/reopen`、`hooks/summarize-state`、`hooks/todo-check`：当前本地入口与状态消费者。
- https://docs.github.com/en/rest/issues/issues — GitHub Issue 列表可能包含 PR，更新所需权限。
- https://docs.gitlab.com/api/issues/ — GitLab Issue 字段与状态事件；实施前核验实际使用的接口。

## Related Tasks
- `TaskFlowDocs/achieved/2026-09-07-todo-intake-and-promotion/`：本地 Todo 的已有设计；当时明确排除远程跟踪器，本任务有独立交付与验收。

## Skills / Tools Used
- [PRD] `agent-skills:spec-driven-development` — purpose: 梳理需求；outcome: succeeded；incorporated: 按用户选择明确验收。
- [Spec] `agent-skills:api-and-interface-design` — purpose: 界定接口；outcome: succeeded；incorporated: 平台身份与失败语义。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 拆解步骤；outcome: succeeded；incorporated: 按依赖编排验证切片。
- [Test] `agent-skills:test-driven-development` — purpose: 建立失败先行与端到端断言；outcome: succeeded；incorporated: 覆盖两平台、失败恢复、冲突和完整生命周期。
- get-api-docs 的 chub 查询仅找到 SDK 内容；以 GitHub/GitLab 官方文档为 API 来源，实施前核验选定接口。

## 前置条件和设计选择
- 改动归属插件行为：`skills/taskflow/` 与 `hooks/`，会影响使用远程模式的安装者；默认本地模式保持现有路径。
- v1 提供项目默认模式和多仓库配置，每条记录携带本地或远端归属；只在操作时访问网络，绝不增加后台轮询。
- 使用宿主已有认证能力；评估 `gh`、`glab` 的实例选择、输出和权限，不自动安装、不复制凭据。GitLab CLI 此环境当前未发现，缺失时要给出可执行提示；具体可用性须测试。
- 远端写入与本地文件不是原子操作：准备恢复意图，超时或结果不明不盲目重试，核对远端稳定标识后继续；对无法确认的情况停止并保留可恢复状态。
- GitHub 普通写请求不支持通用条件更新，用户已接受写前后核对仍有竞态；只修改指定字段并告知，不能宣称完全防止并发覆盖。GitLab 写条件支持尚未证实，同样不得假定存在。
- 每个 Task version 有代码变更时至少一个 Git 提交，合适时增加回退点；不提交其他任务文件。

## Plan Review
- Verdict: sound
- Coverage: PRD 验收 1（本地默认/配置）→ Step 2；2（汇总/分页）→ Step 2；3（创建/编辑/标签）→ Step 3；4（生命周期）→ Step 4；5（故障、恢复和已接受的竞态）→ Steps 1、3、4；6（迁移）→ Step 3；7（归属/去重）→ Steps 2–3；8（快照）→ Step 2；9（平台及回归测试）→ Steps 2–5。
- Verifiability: Step 1 比对官方文档和记录；Step 2 测试完整、部分失败与只读快照；Step 3 的服务端状态断言覆盖创建、编辑、迁移及失败；Step 4 检查远端标签和本地目录的最终状态；Step 5 逐条复核 PRD 并运行相应宿主测试。
- Layer ownership: 远端适配器负责协议和结果；本地任务层负责关联及恢复；展示层负责选择、告知及过期状态。测试断言远端实际结果和本地状态；修改已有测试仅在接口契约确有变化时记录，不以改中间值掩盖错误。

## Approval
- Status: approved
- Approved by: user
- Approved at: 2026-11-16 14:51 +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 确认平台能力和恢复契约
- Goal: 核验两平台身份、分页、写入、认证和自托管接口，确定错误与恢复协议；如文档不足则标明未验证，不虚称已测。
- Dependencies: 计划获准且官方文档可读。
- Files: `spec.md`、`plan.md`、`reference/platform-evidence.md`。
- Implementation checklist:
  - [x] 按官方文档和可控 CLI 夹具核验接口、权限及条件更新，记录不能保证的并发窗口；未运行真实 GitLab、自托管或远端写入，用户知悉限制后批准验收。
  - [x] 定义身份格式、阶段标签、明确结果不明时的恢复与重复创建防护。
- Acceptance: 已确认的官方接口约束、已知限制和恢复步骤可审核；无资料证实的行为标注未验证，接口实际行为由后续测试验证。
- Verification: 引用已核查的官方文档并逐项审阅身份、阶段标签、已知竞态和操作恢复协议；接口夹具在后续实现步骤验证实际请求。
- Rollback: 仅撤回本步骤未使用的设计记录。
- Status: done

### Step 2 — 本地模式与远端读取切片
- Goal: 配置项目默认方式与多个实例，按记录归属汇总远端及保留本地记录。
- Dependencies: Step 1。
- Files: 新增 `hooks/remote-todo`（显式远端操作）、`hooks/test-remote-todo`；按需调整 `hooks/json-field`、`hooks/smoke-test`、`skills/taskflow/SKILL.md`。
- Implementation checklist:
  - [x] 实现显式模式选择、多仓库配置及分页读取，区分身份并排除 GitHub PR。
  - [x] 实现部分失败提示和用户选择的本地只读快照，不写入凭据。
- Acceptance: 本地默认行为保持；两个平台的多仓库列表、错误和快照均可验证。
- Verification: 可控接口测试、Windows 与 Unix 入口测试。
- Rollback: 回退该切片提交，保留用户配置和已有待办。
- Status: done

### Step 3 — 创建、编辑与迁移切片
- Goal: 支持用户指定目标的创建、修改、标签操作及双向按需迁移。
- Dependencies: Steps 1–2。
- Files: `hooks/remote-todo`、`hooks/test-remote-todo`、`hooks/task`、`skills/taskflow/references/runtime.md`。
- Implementation checklist:
  - [x] 验证目标与输入，执行新建、编辑及保留无关标签的更新。
  - [x] 执行选择式迁移、关联去重及结果不明的核对恢复；保留原始记录。
- Acceptance: 同号、重复操作、部分成功、权限不足和并发更改都有明确结果，不静默删除或覆盖。
- Verification: 对两平台使用模拟服务器注入超时、丢响应、冲突和部分写入；校验服务端实际状态。
- Rollback: 回退代码提交；已创建远端 Issue 保留，由用户决定后续处理。
- Status: done

### Step 4 — 任务生命周期切片
- Goal: 把远端主记录接入提升、阶段变化、完成、取消、归档和恢复。
- Dependencies: Steps 1–3。
- Files: `hooks/task`、`hooks/archive`、`hooks/reopen`、`hooks/summarize-state`、`hooks/test-remote-todo`。
- Implementation checklist:
  - [x] 以稳定关联路由本地和远端条目，阶段标签变更保留其他标签。
  - [x] 覆盖完成、取消、重开和跨系统中断，远端失败保留本地恢复信息。
- Acceptance: 可从远端 Issue 完整走通任务生命周期；错误时不丢失任务目录或错误报告完成。
- Verification: 两平台端到端夹具及本地模式回归。
- Rollback: 回退该切片；保留任务目录、Issue 和关联记录供恢复。
- Status: done

### Step 5 — 集成与验收
- Goal: 更新全部宿主说明并验证完整功能。
- Dependencies: Steps 1–4。
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/runtime.md`、`README.md`、`README.zh-CN.md`、`.github/workflows/hooks.yml`。
- Implementation checklist:
  - [x] 更新双语文档和主机入口，说明权限、快照隐私、恢复和并发限制。
  - [ ] 覆盖 PRD 每项验收，审阅安全边界及改动，记录真实服务未验证之处。
  - [x] 运行必要的本地检查和 CI 相关测试，提交代码回退点。
- Acceptance: 文档与实现一致，两平台和本地模式回归通过，未验证内容准确披露。
- Verification: 针对性测试、`git diff --check`、skill 校验及适用的跨平台 CI。
- Rollback: 按切片提交回退代码；不自动删除用户数据或远端 Issue。
- Status: in_progress

## Checkpoints
- Steps 1–2 后检查身份、平台差异和读取端到端结果。
- Steps 3–4 后检查失败恢复、去重和完整生命周期。

## Verification / Review
- 已比较活动任务、已有 Todo 和历史成果；无覆盖本任务的活动任务。
- 仓库无 `.codegraph/`；现有本地 Todo 调用路径直接写在任务和归档脚本中。
- 工作区 `.worktrees/capability-outcomes`，分支 `feature/remote-issue-todos`，v1 基线为分支创建时 HEAD。
- 已实现配置校验、模拟远程读取、可选快照、Issue 创建及核对恢复；对应聚焦脚本红绿测试通过。真实 GitHub 公共仓库只读列表通过：1 条 Issue、141 个 Pull Request 被过滤；GitLab 和远端写入尚未真实验证。
- 已提交 `0e98b7a`、`0025359`、`f4a6189`、`e78badf`、`c854332` 作为阶段回退点；这些提交未包含另一条 Todo。
- 同仓库创建互斥与已知未决记录阻断已通过模拟并发测试；异常进程遗留互斥目录的用户恢复和真实平台行为仍未验证。
- 已实现远端标题/正文编辑、标签与阶段变更、任务提升、双向复制/显式解除关联及混合列表去重；主要写入路径仍以模拟接口验证，完整验收尚未完成。
- 远端恢复目录需要 Git 本地排除，未排除或包含已追踪文件时拒绝写入；测试覆盖固定探针绕过与强制追踪。
- GitHub 缺失阶段标签的创建、任务状态、归档/恢复、迁移与解除关联的定向夹具通过；真实 GitHub 写入、自托管实例和真实 GitLab 尚未验证。
- 2026-11-16 Windows 完整测试首次发现 `complete --root` 调用 `archive` 丢失根目录；已修复并在重跑中通过生命周期段。Windows 全量测试最终通过；Bash 全量在 Git Bash 上运行到独立复制 Bash 的原有测试时因缺少 Windows DLL 中止（该套件不在 Windows CI 运行）。Windows 运行时部分脚本使用系统临时目录，未遵守项目内临时目录边界；没有删除项目外文件，后续测试显式设置项目内临时目录。
- `quick_validate.py skills/taskflow` 使用现有 torch Python 环境通过；`git diff --check` 通过。
- 已解除关联的任务可在远端与本地阶段一致且未被其他任务占用时显式重新连接，保留历史；再次解除关联时保留旧副本并重新获取。GitHub/GitLab 夹具验证了冲突及恢复同步。未提升的远端本地副本可以明确选择远端为准并重新关联原 Issue；保留本地副本，禁止误用迁移在原仓库创建重复 Issue。用户选择稳定标记和迁移前全量检查；两平台重复标记及读取失败夹具通过。检查与创建非原子操作，同一条 Todo 不得在多台机器或 worktree 中同时迁移；用户手动移除标记也会削弱检查。
- 2026-11-16：用户同意项目级默认、条目级归属、显式迁移和可选只读快照；用户已审阅需求方向；随后明确同意实施计划。

- Windows 完整回归 `windows-full-05` 通过，包括开放标准输入测试；之后对只读关联记录语义、孤立记录、跨仓库迁移与历史去重的调整分别运行 Windows 启动器定向测试通过，未重跑整个套件。
- Linux/macOS 完整回归未在本机运行：Git Bash 执行 Bash 全量测试时，仓库原有的隔离 Bash 夹具缺少 Windows DLL 而中止；不可把它当作 Linux/macOS 通过。真实 GitHub 写入、自托管服务和真实 GitLab 仍未验证。
- 用户在知悉真实 GitLab、自托管和远端写入未实测的情况下批准本次验收；这些真实平台验证保留为后续工作。测试夹具留在任务参考目录，另一条独立 Todo 保留在未提交工作区。

- PR #143 的首轮 Hooks CI：Ubuntu 在 hooks 清单检查失败，原因是两份清单遗漏新增脚本；已在 `hooks/README.md` 和 `runtime.md` 列出实际脚本，并修正网络命令说明。与 CI 相同的清单检查和 `git diff --check` 在项目内通过；修复后的完整 CI 待重跑。

- PR #143 第二轮 macOS 回归在中文标签 URL 编码失败；怀疑 Bash 3.2 的字节符号扩展。编码时显式限制为无符号 8 位，Windows Git Bash 的中文标签回归通过；macOS 结果以重跑 CI 为准。

- PR #143 的 Hooks CI 在代码提交 `4e1b09fb59b95e984b116552e7ad9e507db308a9` 全部通过，包括 Ubuntu、macOS、Windows、评估、发布和 Todo 合并检查：[CI run 43848406813](https://github.com/hkwuks/TaskFlow/actions/runs/43848406813)。此前两次失败的清单及 macOS 中文标签问题均已修复。真实 GitLab、自托管及远端写入仍未实测。

- 用户于 2026-11-16 批准本任务验收；此批准不表示已运行真实 GitLab、自托管或远端写入测试。PRD 逐项审阅：配置/本地默认对应配置与 intake 夹具；多源分页和 PR 过滤对应列表夹具及 GitHub 只读验证；创建、编辑、标签、阶段和恢复对应两平台 CLI 夹具；迁移、去重、快照和任务生命周期对应各自回归及三平台 Hooks CI。真实平台验证边界列为后续工作，不伪称通过。

- 归档前复核发现 `snapshot` 原样写入远端 Issue 内容，若内容含凭据则违反 PRD 的快照凭据要求。先撤回未提交的归档；用户批准验收基于此前披露的限制，不应误认为已接受该新发现。需确定快照隐私方案并修复后再完成验收。

## PR Template Mapping
- Summary：GitHub / GitLab Issues 作为可选 Todo 主记录，覆盖多仓库、状态标签、迁移和恢复。
- TaskFlow traceability：本任务 `TaskFlowDocs/2026-11-16-remote-issue-todos/`；范围为远端适配器、任务生命周期、双语文档及回归测试；目标 `hkwuks/TaskFlow:main`。
- Verification：`git diff --check origin/main...HEAD` 和 skill 校验通过；Windows 完整测试通过后有额外代码提交；PR Hooks CI 已在代码提交 `4e1b09f` 通过 Ubuntu、macOS、Windows。Git Bash 本机测试不单独构成 Linux/macOS 验收。
- Review boundaries：不提交恢复数据、测试夹具或其他 Todo；不含凭据；真实 GitLab、自托管与远程写入未验证，远程创建及并发编辑存在已披露竞态。
- PR 状态：用户已在知悉真实服务测试限制后批准验收；归档前新发现快照凭据风险，修复前保持草稿。

## Change Log
- 2026-11-16：记录用户决定、起草规格，并基于任务拆解技能编写计划。
- 2026-11-16：核验官方接口，发现 GitHub 常规写请求不能依赖通用条件更新；用户接受仅更新指定字段、写前后核对并提示剩余竞态。
- 2026-11-16：用户明确同意实施计划；手工记录批准，因为 `hooks/task` 每次运行会删除其临时目录，而当前用户规则禁止未经许可删除文件。
- 2026-11-16：实现并提交配置、模拟读取、快照、创建恢复、编辑、标签、阶段同步和 Git 私有记录保护；全部是阶段成果，不代表完整功能已完成。

## Follow-ups
- 实际服务测试资源尚未确定；继续验证真实 GitLab、自托管及远端写入，不把模拟结果说成真实宿主验证。
- 2026-11-16：用户选择跨工作区稳定标记与迁移前核对，明确不得并发迁移同一条；GitHub/GitLab 重复标记、读取失败、正文编辑保留标记及 Windows 启动器定向测试通过。
