# Plan — 避免已通过 CI 后的文档跟进重复运行重型测试
> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers
- `.github/workflows/hooks.yml`、`tools/workflow-affected`、`hooks/smoke-test`。
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs
- https://docs.github.com/en/rest/actions/workflow-runs
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows

## Related Tasks
- Todo TF-20261110-b73d49；流程 Token 优化 TF-20261110-84d1a9 记录成本但不重复实现。

## Skills / Tools Used
- [PRD] Unaided — none applied; considered: requirements elicitation and framing.
- [Spec] Unaided — none applied; considered: architecture and design specification.
- [Plan] Unaided — none applied; considered: work breakdown and task decomposition.
- [Test] Unaided — none applied; considered: testing strategy.
- [Research] `get-api-docs` — chub 本地帮助可用，但查询受网络限制未返回；改核 GitHub 官方文档和实际只读 API 输出。
- [Review] `agent-skills:code-review-and-quality` — 复核复用条件、artifact 信任边界及失败回退。

## Preconditions
- 用户同意无法可靠证明时正常运行完整 CI；主分支推送保持现有全量策略。

## Plan Review

- Verdict: sound
- Coverage: 同 PR、相同 base、旧 head 祖先、任务文档白名单、逐 job 成功及失败回退分别约束；主分支不跳过。
- Verifiability: 元数据与实际 run 和 jobs API 交叉核对；PR 默认测试合并提交，未取得证据不得复用。
- Layer ownership: Git 负责祖先和差异，GitHub 提供运行证据，仓库工作流负责执行和状态；数据视为不可信输入。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-10 17:01 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 记录并核对可复用证据

- Goal: 对同 PR、同 base 和相同测试输入记录并核验先前各 job 的成功结果。
- Dependencies: 用户批准具体方案；GitHub API 可读取相应 run 和 artifact。
- Files: `.github/workflows/hooks.yml`、最小判定工具和针对性测试。
- Implementation checklist:
  - [x] 为 PR 运行保存小型事件元数据，并在后续运行核验同 PR、相同 base、旧 head 祖先及任务文档白名单。
  - [x] 逐 job 查验先前确实成功，按 job 保守复用；身份、证据、网络、权限或数据异常全部运行完整 CI。
  - [ ] 覆盖强推、基线变化、代码和 Todo 修改、缺失或伪造元数据、先前 skipped/failed、API 失败。
- Acceptance: 符合条件的文档跟进减少重复重型 job；保留工作流与必要状态，且明确输出复用来源；不确定时完整运行。
- Verification: 官方文档、模拟 API/仓库夹具、真实 GitHub PR CI 验证及 `git diff --check`。
- Rollback: 回退工作流与判定工具；现有分类恢复。
- Status: in_progress

## Checkpoints

## Verification / Review
- 2026-11-10：当前分类读整个 PR 对比基线；`TaskFlowDocs/todo.md` 为 smoke 输入，不能直接把所有 Markdown 当作无影响。
- GitHub 文档说明跳过工作流可能令必需检查保持 Pending；工作流运行 API 支持按 head SHA 等过滤，但不能单独证明 base 与矩阵作业一致。
- 2026-11-10：只读查询先前 PR #131 的 run 42767499102；总体 success，但 release job 实际 skipped，其他矩阵通过，且运行 API 返回的 pull_requests 为空。因此不能把总体 success 当作各项实际执行，也不能仅凭该字段证明 PR 与 base；需找到可靠来源，否则完整运行。
- 该运行的 checkout 日志显示实际检出 `0132109`，合并当时的 PR head `2b64ea6` 与 base `e75fcfd`；run API 的 head SHA 只有 PR head。解析日志格式来推断基线不可靠，需明确记录并核验事件基线，不能只比 head。
- 拟采用小型 artifact 显式记录运行时事件，逐 job 通过 API 验证；这会为每次 PR 运行增加一份小型元数据，有存储和一次查询成本。老运行无 artifact 时自然回退完整 CI。
- 2026-11-10：用户批准方案；实现后 8 项 Python 单测通过，覆盖纯文档白名单、身份/base、未执行或重复 job、合法复用、强推、修改过的元数据写入路径、残缺 jobs、无效 artifact 和 API 失败回退。GitHub 托管 PR 的实际 artifact、检查状态与跨平台 CI 尚未验证。
- Windows 隔离真实 Git 历史验证：同 base、旧 head 祖先且仅追加任务文档时允许复用；将代码文件改名至任务文档目录后，`--no-renames` 同时识别原路径并拒绝复用。工作流 YAML 已由 PyYAML 解析，但此检查不能替代 GitHub 对工作流的实际验证。
- 后续加入有效 artifact 读取测试，9 项单测及 6 项 eval 通过。先前 PR 修改过工作流、元数据写入器或分类器时不复用，避免让 PR 自报可信基线。
- 复核补充：先前 job 的 head SHA 必须等于运行 head；最近一次后续运行如果全部 skipped，不应掩盖更早确实执行成功的运行。补充回归后 10 项单测通过。
- 对已合并 PR #131 的实际 GitHub 运行作只读试查，未找到满足条件的证据，三项输出均为 false；该样本的旧提交到新提交还包含 Todo 变更，因此不能仅归因于缺少 artifact。
- 首轮 CI 的 Ubuntu/macOS smoke 失败：既有断言要求三个作业的条件严格等于旧分类条件。当前已批准的复用契约确实扩展了条件，因此同步调整断言为必须同时检查分类结果和复用结果，保留 Todo 审计无条件运行，并新增复用单测 job 无条件运行的断言；并非删除该安全断言。

## Change Log
- 2026-11-10：建立 v1 调查草案；实施前需要把证据方案补齐并经过计划审核。

## Follow-ups

## Version History

- v1 — planning.
