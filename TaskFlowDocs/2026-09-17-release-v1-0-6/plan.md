# Plan — Publish TaskFlow v1.0.6
> Task version: v1
> Status: in_progress

No spec required — 对已知良好基线执行一次发布清单，不新增设计。

## Reference Pointers

- `RELEASE.md` —— 本次必须逐条遵守的清单。本次走 `### Optional Release PR path`，Step 1–2 的内容就是它的 `## Release scope` 与 `## Validation checklist`。
- `TaskFlowDocs/achieved/2026-09-15-release-v1-0-5/plan.md` —— 上一次发布的实际执行记录与验证写法。
- `TaskFlowDocs/achieved/2026-09-15-release-friction/prd.md` —— `release-check` 与「release 任务文档不重述流程」规则的来源。
- `skills/taskflow/references/artifacts.md` 的 `## Release task documents` —— release 任务的 `prd.md` / `plan.md` 应当只记决策与结果，不复制 `RELEASE.md` 的清单。
- `.github/pull_request_template.md` —— 两个 PR 的必填字段与本次映射。

## Related Tasks

- Depends on: 无。`4e497c3`（PR #31）已合入 `main`。
- Related: `TaskFlowDocs/achieved/2026-09-15-release-friction/`（`release-check` 的来源）、`TaskFlowDocs/achieved/2026-09-16-todo-entry-loss-detection/`（`todo-check` 的来源）、`TaskFlowDocs/achieved/2026-09-16-web-ui-merge-loss-guard/`（CI `todo-merge-audit` 的来源）—— 本次发布的主要内容来源。
- 不相关的活跃任务：`TaskFlowDocs/2026-09-16-duplicate-todo-id/`、`TaskFlowDocs/2026-09-16-capability-selection-enforcement/`（均未批准、未实现，不进入发布范围）。

## Skills / Tools Used (Optional)

- 未调用额外 Skill 或工具。发布是一次既存流程的执行，`gh` CLI 用于 GitHub Release，`git` 用于标签；两者的实际调用记录在 Step 2 的验证结果里。

## Preconditions

- [x] 适用仓库文档已读：`RELEASE.md`、`CONTRIBUTING.md`、`ROADMAP.md`、`.github/pull_request_template.md`、`TaskFlowDocs/repository-docs/index.md`。
- [x] 远程 / 分支：`origin` = `hkwuks/TaskFlow`（非 fork），base = `origin/main`，本地 `main` 与 `origin/main` 一致（均为 `4e5e8375aba3b18a865d1bcaaac804e060db8ad0`）。
- [x] 工作区干净；发布范围（`v1.0.5..main` 的全部用户可见变化）已与用户确认。
- [x] 本任务已在 `TaskFlowDocs/todo.md` 登记（`TF-20260917-b7bc40`）并升级为任务。
- [x] 本任务不新建治理文档；`RELEASE.md` 已存在。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-17 11:41 +0800
- Approved version: v1
- Approved scope: PRD / Plan v1 —— 发布 v1.0.6：范围取 `v1.0.5..main` 的全部用户可见变化，经 `chore/release-v1-0-6` 分支与 PR 落地，授权一次性覆盖注解标签推送、GitHub Release 与两个 marketplace pin 的落地。

## Steps

### Step 1 — 发布元数据提交与清单验证

- Goal: 在 `chore/release-v1-0-6` 分支上产生一个版本号自洽的发布提交，并让发布清单全绿后经 PR 合入 `main`。
- Dependencies: 无。
- Files: `.claude-plugin/plugin.json`、`.codex-plugin/plugin.json`、`.codebuddy-plugin/plugin.json`、`CHANGELOG.md`、`README.md`、`README.zh-CN.md`、`RELEASE.md`。
- Implementation checklist:
  - [ ] 三个 manifest 更新到 `1.0.6`；Codex 与 CodeBuddy 的 cachebuster 后缀按既有格式改为 `20260917`。
  - [ ] `CHANGELOG.md` 新增 `## [1.0.6] — 2026-09-17`，Added / Fixed / Compatibility / Verification 四节；把 `[1.0.5]` 段里两条实际在标签之后才落地的条目（CodeBuddy 宿主、`release-check` 的 catalog 读取修正）移入 `[1.0.6]`。
  - [ ] 两份 README 的 `claude plugin list` 与 `codebuddy plugin list` 示例改为 `Version: 1.0.6`。
  - [ ] `RELEASE.md` 的 `## Release scope` 首句补上 CodeBuddy；验证清单里 Skill 校验那条由本地绝对路径改为通用形式。
  - [ ] 跑完整清单并逐条记录结果（见 `## Verification / Review`）。
  - [ ] 按 PR 模板开 PR，合入 `main`，删除分支。
- Acceptance: 清单每条都有记录结果；三个 manifest 与 CHANGELOG 版本一致；`hooks/release-check .` 在发布提交后仍报 `STATUS: pass`（catalog 有意继续指向 `v1.0.5`）；发布提交在 `origin/main` 上。
- Verification: `bash hooks/release-check .` 输出六个 `1.0.6` 字面量与两个 `v1.0.5 -> 3151d27…` pin，`STATUS: pass`；`bash hooks/smoke-test` 报 `ALL SMOKE PASSED`。
- Rollback: 分支未合并前直接丢弃；合并后靠补丁提交修正，不改写 `main` 历史。
- Status: in_progress

### Step 2 — 打标签、建 Release、落 marketplace pin

- Goal: 从 `main` 上的精确发布提交产生不可变的 `v1.0.6` 注解标签与 GitHub Release，并让两个 catalog 的稳定安装 pinned 到该提交。
- Dependencies: Step 1 合入 `origin/main`。
- Files: `.claude-plugin/marketplace.json`、`.codebuddy-plugin/marketplace.json`（均只改 `ref`/`sha`）。
- Implementation checklist:
  - [ ] `git fetch --tags` 后确认 `origin/main` 就是发布提交，工作区干净。
  - [ ] 复核三个 manifest 版本与 CHANGELOG 段落。
  - [ ] 在该提交上创建注解标签 `v1.0.6` 并推送（用户已一次性授权）。
  - [ ] 用标签提交的完整 SHA 更新两个 catalog 的 `ref`/`sha`，跑 `bash hooks/release-check .` 确认两个 pin 都解析到该提交。
  - [ ] 用该 tag 建 GitHub Release，正文取自 `CHANGELOG.md` 的 `[1.0.6]` 段落。
  - [ ] pin 改动按 PR 模板开第二个 PR 合入 `main`，再跑一次 `bash hooks/release-check .`。
  - [ ] 记录 tag、tag 对象 SHA、提交 SHA、Release URL 与两个 pin 到本 Plan。
- Acceptance: 标签是 `main` 的祖先且指向发布提交；Release 存在且正文与 CHANGELOG 段落一致；两个 catalog 的 `ref`/`sha` 与标签提交逐字符一致；`release-check` 报 `STATUS: pass`。
- Verification: 见 `## Verification / Review` 的发布记录。
- Rollback: 不移动、不删除已推送标签；出问题走补丁版。标签推送前的失败直接不推送即可。
- Status: pending

### Step 3 — 归档发布任务

- Goal: 按 TaskFlow 的归档事务把本任务移入 `TaskFlowDocs/achieved/` 并同步 Todo 条目。
- Dependencies: Step 2 完成且用户在验收后确认归档。
- Files: `TaskFlowDocs/2026-09-17-release-v1-0-6/` → `TaskFlowDocs/achieved/2026-09-17-release-v1-0-6/`、`TaskFlowDocs/todo.md`。
- Implementation checklist:
  - [ ] 两份核心文档状态改为 `completed`，`## Approval` 记录真实批准人与时间。
  - [ ] `bash hooks/task complete 2026-09-17-release-v1-0-6 --user-accepted` 后 `bash hooks/archive 2026-09-17-release-v1-0-6`。
  - [ ] 校验：活跃路径不存在、achieved 路径存在、`prd.md` 与 `plan.md` 都为 `completed`、Todo 条目 `Next action` 为 `None — completed and archived.`。
- Acceptance: 归档三项校验全部通过，Todo 条目 `TF-20260917-b7bc40` 状态 `done` 且指向 achieved 路径。
- Verification: `ls TaskFlowDocs/2026-09-17-release-v1-0-6` 报不存在；`grep -n "TF-20260917-b7bc40" -A 8 TaskFlowDocs/todo.md` 显示 achieved 路径与已清空的 `Next action`。
- Rollback: 归档失败时保持 Todo 未 `done`，记录阻塞点，不声称归档完成。
- Status: pending

## Checkpoints

- Step 1 完成后：清单全绿才动标签；标签一旦推送不可回退。
- Step 2 的「标签推送」是本次唯一不可逆动作，用户已一次性授权至 marketplace pin 落地；pin 的第二个 PR 合入后本次发布即结束。

## Verification / Review

待执行后填写。

## Change Log

- 2026-09-17 用户确认发布范围取 `v1.0.5..main` 的全部用户可见变化，落地路径为分支 + PR，不可逆动作一次性授权到 marketplace pin 落地。
- 2026-09-17 发布路线由 `RELEASE.md` 的默认直接 tag 改为可选 Release PR 路径；`prd.md` 已记录两个潜在的不一致事实（CodeBuddy 条目当前挂在 `[1.0.5]`、`RELEASE.md` 首句未提 CodeBuddy），Step 1 按最小步骤修正。

## Follow-ups

- `RELEASE.md` 的验证清单里 Skill 校验仍无仓库内可移植写法，本次只把不可移植的绝对路径换成通用形式，不新增脚本。

## Version History

- v1 — planning。
