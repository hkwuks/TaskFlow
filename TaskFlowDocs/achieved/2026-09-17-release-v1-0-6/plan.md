# Plan — Publish TaskFlow v1.0.6
> Task version: v1
> Status: completed

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
  - [x] 三个 manifest 更新到 `1.0.6`；Codex 与 CodeBuddy 的 cachebuster 后缀按既有格式改为 `20260917`。
  - [x] `CHANGELOG.md` 新增 `## [1.0.6] — 2026-09-17`，Added / Fixed / Compatibility / Verification 四节；把 `[1.0.5]` 段里两条实际在标签之后才落地的条目（CodeBuddy 宿主、`release-check` 的 catalog 读取修正）移入 `[1.0.6]`。
  - [x] 两份 README 的 `claude plugin list` 与 `codebuddy plugin list` 示例改为 `Version: 1.0.6`。
  - [x] `RELEASE.md` 的 `## Release scope` 首句补上 CodeBuddy；验证清单里 Skill 校验那条由本地绝对路径改为通用形式。
  - [x] 跑完整清单并逐条记录结果（见 `## Verification / Review`）。
  - [x] 按 PR 模板开 PR，合入 `main`，删除分支：PR #33。
- Acceptance: 清单每条都有记录结果；三个 manifest 与 CHANGELOG 版本一致；`hooks/release-check .` 在发布提交后仍报 `STATUS: pass`（catalog 有意继续指向 `v1.0.5`）；发布提交在 `origin/main` 上。
- Verification: 发布提交 `f8e13a0`，合并提交 `ce3b03c`；清单逐条结果见 `## Verification / Review`。
- Rollback: 分支未合并前直接丢弃；合并后靠补丁提交修正，不改写 `main` 历史。
- Status: done

### Step 2 — 打标签、建 Release、落 marketplace pin

- Goal: 从 `main` 上的精确发布提交产生不可变的 `v1.0.6` 注解标签与 GitHub Release，并让两个 catalog 的稳定安装 pinned 到该提交。
- Dependencies: Step 1 合入 `origin/main`。
- Files: `.claude-plugin/marketplace.json`、`.codebuddy-plugin/marketplace.json`（均只改 `ref`/`sha`）。
- Implementation checklist:
  - [x] `git fetch --tags` 后确认 `origin/main` 就是发布提交（`ce3b03c`），工作区干净。
  - [x] 复核三个 manifest 版本与 CHANGELOG 段落。
  - [x] 在该提交上创建注解标签 `v1.0.6` 并推送（用户已一次性授权）。
  - [x] 用标签提交的完整 SHA 更新两个 catalog 的 `ref`/`sha`，跑 `bash hooks/release-check .` 确认两个 pin 都解析到该提交。
  - [x] 用该 tag 建 GitHub Release，正文取自 `CHANGELOG.md` 的 `[1.0.6]` 段落。
  - [x] pin 改动按 PR 模板开第二个 PR：PR #34，CI 全绿。
  - [x] PR #34 合入 `main` 后，在 `main` 上再跑一次 `bash hooks/release-check .`：合并提交 `80d35cf`，`STATUS: pass`。
  - [x] 记录 tag、tag 对象 SHA、提交 SHA、Release URL 与两个 pin 到本 Plan。
- Acceptance: 标签是 `main` 的祖先且指向发布提交；Release 存在且正文与 CHANGELOG 段落一致；两个 catalog 的 `ref`/`sha` 与标签提交逐字符一致；`release-check` 报 `STATUS: pass`。
- Verification: 见 `## Verification / Review` 的发布记录。
- Rollback: 不移动、不删除已推送标签；出问题走补丁版。标签推送前的失败直接不推送即可。
- Status: done

### Step 3 — 归档发布任务

- Goal: 按 TaskFlow 的归档事务把本任务移入 `TaskFlowDocs/achieved/` 并同步 Todo 条目。
- Dependencies: Step 2 完成且用户在验收后确认归档。
- Files: `TaskFlowDocs/2026-09-17-release-v1-0-6/` → `TaskFlowDocs/achieved/2026-09-17-release-v1-0-6/`、`TaskFlowDocs/todo.md`。
- Implementation checklist:
  - [x] 两份核心文档状态改为 `completed`，`## Approval` 记录真实批准人与时间。
  - [x] `bash hooks/task complete 2026-09-17-release-v1-0-6 --user-accepted` 后 `bash hooks/archive 2026-09-17-release-v1-0-6`。
  - [x] 校验：活跃路径不存在、achieved 路径存在、`prd.md` 与 `plan.md` 都为 `completed`、Todo 条目 `Next action` 为 `None — completed and archived.`。
- Acceptance: 归档三项校验全部通过，Todo 条目 `TF-20260917-b7bc40` 状态 `done` 且指向 achieved 路径。
- Verification: 见 `## Verification / Review` 的归档记录。
- Rollback: 归档失败时保持 Todo 未 `done`，记录阻塞点，不声称归档完成。
- Status: done

## Checkpoints

- Step 1 完成后：清单全绿才动标签；标签一旦推送不可回退。
- Step 2 的「标签推送」是本次唯一不可逆动作，用户已一次性授权至 marketplace pin 落地；pin 的第二个 PR 合入后本次发布即结束。

## Verification / Review

- 2026-09-17 Step 2: PR #34 merged as 80d35cf (2026-09-17T04:36:21Z); release-check pass on main; both pins resolve to ce3b03ca; /plugin update confirms installed 1.0.6

本地环境：Windows 11 + Git for Windows Bash + PowerShell 5.1 + `python` 3.12.13。
逐条结果如下。

- `bash hooks/release-check .` → `STATUS: pass`（exit 0）。六个版本字面量全部 `1.0.6`：三个 manifest、CHANGELOG 首段、两份 README 的插件列表示例。
- `bash hooks/repository-check .` → 发布提交前 `needs-user-input`（`Base: ambiguous`、`Working tree: has changes`，属预期）；推送分支设上游后 `STATUS: pass`（`Base: origin/chore/release-v1-0-6`、`Working tree: clean`）。
- `bash hooks/smoke-test` → **在本机 Windows 上未通过**，停在 `hooks run with no interpreter available`：该段把宿主 Git Bash 的 `bash` 软链进 curated PATH，而该二进制仍按宿主 PATH 解析 DLL，报 `error while loading shared libraries`。**在工作区改动 stash 后于 `main` 复跑，失败形态完全相同**，因此是宿主既有限制、不是本分支引入的回归。该套件由 CI 矩阵（ubuntu / macos / windows）执行，本次两个 PR 上都为 `pass`；本机其余段与 PowerShell 套件均通过。
- `.\hooks\smoke-test-windows.ps1` → `WINDOWS LAUNCHER ARGS PASSED` / `WINDOWS SESSIONSTART PASSED` / `WINDOWS LIFECYCLE PASSED`（exit 0）。
- `python evals/runner.py` → `PASS (6 evals)`（exit 0）。注意：`python3` 在本机解析到 Microsoft Store 的别名 stub，静默 exit 49；必须用 `python`。
- Skill 校验 → `Skill is valid!`（exit 0）。需 `PYTHONUTF8=1`：脚本以默认 `gbk` 读 UTF-8 的 `SKILL.md`，否则 `UnicodeDecodeError`。脚本路径取自本机 skill-creator 安装位置。
- `git diff --check` → clean。
- CI：PR #33（发布元数据）与 PR #34（marketplace pin）的 `smoke`(ubuntu/macos/windows)、`release`、`evals`、`todo-merge-audit` 六个 job 全部 `pass`。

发布记录：

- 注解标签 `v1.0.6` → tag 对象 `013910978391d3f7c04baaeb3cbf59c155903bff`，指向提交 `ce3b03cab31c75ed467f4ccec06ea5cfc6719357`（`git merge-base --is-ancestor v1.0.6 main` 为真；`git ls-remote --tags origin v1.0.6` 返回同一 tag 对象）。
- 发布提交 `f8e13a0`（`chore: prepare the v1.0.6 release`），合并提交 `ce3b03c`（Merge pull request #33）。
- GitHub Release：`https://github.com/hkwuks/TaskFlow/releases/tag/v1.0.6`，tag = `v1.0.6`，draft = false，prerelease = false；正文与 `CHANGELOG.md` 的 `[1.0.6]` 段落逐行一致（除行尾换行）。
- marketplace pin：`.claude-plugin/marketplace.json` 与 `.codebuddy-plugin/marketplace.json` 均为 `ref` = `v1.0.6`、`sha` = `ce3b03cab31c75ed467f4ccec06ea5cfc6719357`；提交 `42edb18`，PR #34。
- 待补：无。PR #34 已由用户合并为 `80d35cf`（2026-09-17T04:36:21Z），`main` 上 `bash hooks/release-check .` 报 `STATUS: pass`，两个 pin 均解析到 `ce3b03ca…`；`/plugin marketplace update taskflow` + `update taskflow@taskflow` 已确认安装端评到 `1.0.6`。未跑：Codex 与 CodeBuddy 端的安装验证（本机未走这两个宿主）。

归档记录：

- 用户于 2026-09-17 验收并同意归档；`bash hooks/task complete 2026-09-17-release-v1-0-6 --user-accepted` 一次通过（该命令内含 `hooks/archive`）。
- 校验：活跃路径 `TaskFlowDocs/2026-09-17-release-v1-0-6` 不存在；`TaskFlowDocs/achieved/2026-09-17-release-v1-0-6/` 下 `prd.md`、`plan.md` 齐备且都写 `> Status: completed`；Todo 条目 `TF-20260917-b7bc40` 为 `- Status: done`、`Task:` 指向 achieved 路径、`Next action: None — completed and archived.`。`Next action` 由 `hooks/archive` 本次新加的清理逻辑写入，未手工补——该逻辑的第二次实战（首次为 `hooks/smoke-test` 的 fixture）。

## Change Log

- 2026-09-17 用户确认发布范围取 `v1.0.5..main` 的全部用户可见变化，落地路径为分支 + PR，不可逆动作一次性授权到 marketplace pin 落地。
- 2026-09-17 发布路线由 `RELEASE.md` 的默认直接 tag 改为可选 Release PR 路径；`prd.md` 已记录两个潜在的不一致事实（CodeBuddy 条目当前挂在 `[1.0.5]`、`RELEASE.md` 首句未提 CodeBuddy），Step 1 按最小步骤修正。
- 2026-09-17 发现 `CHANGELOG.md` 的 `[1.0.5]` 段落列了两条在该标签之后才合入的改动（CodeBuddy 宿主 PR #31、`release-check` 的 catalog 读取修正 PR #26），它们未随任何已发布产物交付。按「改动属于实际交付它的那个版本段落」的原则移入 `[1.0.6]`；`v1.0.5` 段落其余内容不动。
- 2026-09-17 本机 `hooks/smoke-test` 在无解释器段失败，经 stash 后于 `main` 复跑确认形态一致，判定为宿主既有限制而非本分支回归；改为以 CI 矩阵结果作为该套件的依据，并在上一条记录中写明本地未通过。
- 2026-09-17 PR #33 由用户合并（本地 merge 被工具策略拒绝，用户自行完成）；PR #34 用户选择自行合并。

## Follow-ups

- `RELEASE.md` 的验证清单里 Skill 校验仍无仓库内可移植写法，本次只把不可移植的绝对路径换成通用形式，不新增脚本。

## Version History

- v1 — planning。
