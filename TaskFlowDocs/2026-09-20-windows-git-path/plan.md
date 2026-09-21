# Plan — Windows worktree misjudgement: `hooks/task` reads a `D:/` git dir as relative.

> Task version: v1
> Status: planning

No spec required — 一处 helper 的路径取值修正，加一处无消费者的索引列删除；无跨层契约、无数据迁移。

## Reference Pointers

- `hooks/task:52-62` —— `worktree_kind()`，返回值 0/1/2 的约定写在其上方注释里。
- `hooks/task:490`、`hooks/task:510` —— 两个调用点：`intake` 软警告、`promote` 硬 gate（exit 3）。
- `hooks/install-merge-driver:47` —— 仓库内既有的 drive-letter 绝对路径判定，本轮的形态参照。
- `hooks/repository-docs-context` —— 索引渲染与 carry-over 读列的权威实现。
- `hooks/smoke-test:266-330`（索引同步与路由段、拒绝不安全路径段）、`hooks/smoke-test:557-670`（隔离段）—— 改动落点。
- `hooks/smoke-test-windows.ps1` —— Windows 真机套件，本轮新增 worktree 回归。
- `skills/taskflow/SKILL.md:79`、`skills/taskflow/references/artifacts.md:11` —— 描述索引列的散文。
- `TaskFlowDocs/achieved/2026-09-18-conflict-side-review/plan.md` —— 本仓库 plan 的既有写法参照。

## Related Tasks

- Depends on: 无。
- Related: `TaskFlowDocs/achieved/2026-09-11-index-hook-routing/`（索引与 routing 的由来）、`TaskFlowDocs/achieved/2026-09-18-hook-launcher-exec-bit/`（同为 hook 层修复）。
- 无关活跃条目：`TF-20260919-c41f8a`（release 机械开销，非本任务产出，本任务不提交）。

## Skills / Tools Used

- 未调用额外 Skill。全部结论来自仓库内证据：`git rev-parse` 实测、`git worktree list`、在 Linux 上用 `D:/` 目录 + git 垫片复现 Windows 答案、逐次变异验证。
- 成因与回归都是**可重放的证据判定**（实测复现 + 变异验证），不是判断性结论，因此不依赖任何外部能力或 LLM 工具。

## Preconditions

- [x] 适用仓库文档已读：`README.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`、`skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`.github/workflows/hooks.yml`、`.github/pull_request_template.md`。
- [x] `git worktree add .worktrees/windows-git-path -b fix/windows-git-path main` —— 隔离先于文档，base `main` = `27987b1`。
- [x] 本任务在 `TaskFlowDocs/todo.md` 登记为 `TF-20260920-9f3c07` 并升级为任务。
- [x] 成因已在 Linux 上真实复现（`D:/` 垫片使旧实现返回 2）。
- [x] 用户已批准本 Plan（含"一并删除索引日期列"与"补 Windows 真机回归"两项范围决定）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-21 16:22 +08:00
- Approved version: v1
- Approved scope: PRD / Plan
- Note: 用户以「提交并pr」授权落地，并在同一轮的选择中明确：走完整 TaskFlow 流程、补 `hooks/smoke-test-windows.ps1` 真机回归、`todo.md` 中非本任务产出的条目不提交。

## Steps

### Step 1 — 修正 `worktree_kind` 的路径取值

- Goal: 任何平台上都能正确区分任务 worktree 与 base 工作树。
- Dependencies: 无。
- Files: `hooks/task`。
- Implementation checklist:
  - [x] `git rev-parse --git-dir` → `git rev-parse --absolute-git-dir`，删掉 `case "$git_dir" in /*) ;; *) git_dir="$root/$git_dir" ;; esac` 拼接。
  - [x] 保留返回码约定与上方注释，补一行说明 Windows drive path 为什么让旧写法失效。
  - [x] 确认 `hooks/task` 内无其他同类路径形态判断（`--show-toplevel`/`--is-inside-work-tree`/`--verify` 均为字符串比较或退出码）。
- Acceptance: `worktree_kind` 在链接 worktree 内返回 0、在 base 树返回 2、在仓库外返回 1。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout main -- hooks/task`。
- Status: done

### Step 2 — 加入 Linux 侧 Windows 形态回归测试

- Goal: 让这条只在 Windows 环境暴露的 bug 在 Linux 上可复现、可变异验证。
- Dependencies: Step 1。
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 夹具：`$iso_win/D:/repo/.git/worktrees/win/commondir`（`D:/` 在 Linux 上是普通相对目录）+ 待写 `todo.md`。
  - [x] git 垫片 `$tmp/isolation-gitbin/git`：`--absolute-git-dir` 与 `--git-dir` 都返回 `D:/repo/.git/worktrees/win`，`--show-toplevel` 返回 `D:/repo`，其余 `exec` 真 git。
  - [x] 断言：在该 root 下 `intake` 不得出现 `modified in the base working tree`。
  - [x] 垫片必须同时转发 `--git-dir` 与 `--absolute-git-dir`，否则测试绑死在实现细节上、失去变异验证能力（首轮正是这个原因导致断言在旧代码下误通过）。
- Acceptance: 旧实现下该断言失败；修复后通过。
- Verification: 见 `## Verification / Review` 的变异记录。
- Rollback: `git checkout main -- hooks/smoke-test`。
- Status: done

### Step 3 — 删除索引的 "Last checked" 列

- Goal: 去掉一个无消费者、且每个自然日把已跟踪文件弄脏一次的信号。
- Dependencies: 无（与 Step 1、2 独立）。
- Files: `hooks/repository-docs-context`、`skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`TaskFlowDocs/repository-docs/index.md`。
- Implementation checklist:
  - [x] 删 `today="$(date +%Y-%m-%d)"`、删表头 `> Last checked:` 行、删表的 "Last checked" 列（行写、表头、分隔行、渲染 awk 与 `cut` 同步改为 5 列）。
  - [x] 四个路由循环的 `read -r kind relative phases exists checked status` → 去掉 `checked`。
  - [x] carry-over 读列：`n != 8` → `n < 6 || n > 8`，取值改 `f[n - 1]`，并加末格必须匹配 `^[a-z][a-z-]*$` 的守卫（否则旧行的日期会被当成 status；也为让 `../outside.md` 负例继续报警）。
  - [x] 散文同步：`SKILL.md:79`、`artifacts.md:11` 去掉 "last-checked date"。
  - [x] 用 hook 自身重新渲染 `TaskFlowDocs/repository-docs/index.md`，使 base 树回到干净状态。
- Acceptance: 表为 5 列；旧 6 列索引行仍被读回；同一天重跑逐字节幂等；日期不参与内容。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout main -- hooks/repository-docs-context skills/taskflow/SKILL.md skills/taskflow/references/artifacts.md TaskFlowDocs/repository-docs/index.md`。
- Status: done

### Step 4 — 补 Windows 真机 worktree 回归

- Goal: 在真实 Windows 路径形态下覆盖 `return 2` 路径——Linux 垫片测试只能模拟形态，不能替代真机。
- Dependencies: Step 1。
- Files: `hooks/smoke-test-windows.ps1`。
- Implementation checklist:
  - [x] 在被测 root 里 `git init` + 一次提交，`git worktree add` 出链接树。
  - [x] 链接树内 `promote` 必须成功并写出任务目录。
  - [x] base 树内 `promote` 必须仍以 3 退出并打印拦截原因（防回归到"永远放行"）。
  - [x] `intake` 取 ID 的方式改为按 Goal 定位条目（`Get-TodoId`），删除 `- ID:` 块后再匹配，不再假设"第一条 ID 就是刚写的那条"。
  - [x] 不改动既有 launcher/lifecycle/SessionStart 段落。
- Acceptance: 该段落在 CI 的 `windows-latest` 上通过；本机（Linux）无法运行，已在 Risks 中声明。
- Verification: **由 CI 的 `windows-latest` 作业执行**。本机无 PowerShell（`command -v pwsh powershell` 均为空），连语法解析都无法在本地做——因此本轮不声称该脚本已在本地验证，只声称其逻辑与本机实测过的 `worktree_kind` 行为一致（见 `## Verification / Review` 的直连实测）。
- Rollback: `git checkout main -- hooks/smoke-test-windows.ps1`。
- Status: done

### Step 5 — 验证与范围核对

- Goal: 改动不越界，且既有检查全部未被破坏。
- Dependencies: Step 1–4。
- Files: 无（只读检查）。
- Implementation checklist:
  - [x] `bash hooks/smoke-test` → `ALL SMOKE PASSED`。
  - [x] `git diff --check` → clean。
  - [x] `python3 …/quick_validate.py skills/taskflow` → Skill is valid。
  - [x] 变异验证：一次一个，逐个记录结果。
  - [x] 范围核对：提交不含 `TaskFlowDocs/todo.md` 中 `TF-20260919-c41f8a` 那段非本任务内容。
- Acceptance: 每条的实际输出记入 `## Verification / Review`。
- Verification: 本节即为验证。
- Rollback: 不适用。
- Status: done

## Checkpoints

- Step 1 后：`grep -c "rev-parse --git-dir" hooks/task` 为 0，且 `grep -c "absolute-git-dir" hooks/task` 为 1。
- Step 3 后：`grep -c "Last checked" hooks/repository-docs-context` 为 0；`git status --short TaskFlowDocs/repository-docs/index.md` 在重新渲染后为空。
- Step 4 后：`grep -c "worktree" hooks/smoke-test-windows.ps1` 大于 0，且 launcher/lifecycle 段落行数未变。

## Verification / Review

实施于 2026-09-21，worktree `.worktrees/windows-git-path`，分支 `fix/windows-git-path`，base `main` = `27987b1`。

| 检查 | 命令 | 实际输出 |
| --- | --- | --- |
| 全套 smoke | `bash hooks/smoke-test` | `ALL SMOKE PASSED`，exit 0 |
| 空白/冲突标记 | `git diff --check` | clean |
| Skill 校验 | `python3 /home/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/taskflow` | `Skill is valid!` |
| 索引日期无关性 | `date` 垫片返回 `2099-01-01` 重跑 hook，比对摘要 | 摘要不变（断言 `FAIL index bytes depend on the current date` 未触发） |
| 索引幂等 | 连续两次渲染后比对文件摘要 | stable |
| worktree 判定（真机路径） | 在 `.worktrees/windows-git-path`（`.git` 是指针文件，`--absolute-git-dir` 指向 `.git/worktrees/…` 且其下有 `commondir`）内 `bash hooks/task promote …` | 进入任务目录写入分支，未打印 base-tree 拦截 |
| base 树仍被硬 gate | 在 base `main` 上 `bash hooks/task promote … --root "$PWD"` | `Blocked: this is the base working tree, not a task worktree.` + `STATUS: blocked`，exit 3 |
| Windows 真机套件 | `hooks/smoke-test-windows.ps1` | **未在本机执行**——主机无 PowerShell；由 CI `windows-latest` 执行，结果不在本轮本地证据内 |

变异验证（一次一个）：详见 `## Change Log` 的三条记录。

改动范围：`hooks/task`、`hooks/repository-docs-context`、`hooks/smoke-test`、`hooks/smoke-test-windows.ps1`、`skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`TaskFlowDocs/repository-docs/index.md`、本任务目录。无越界文件。

### 实施结果与 Plan 的偏差

- Step 2 首轮实现只让垫片转发 `--absolute-git-dir`，结果旧代码下断言误通过（旧代码问的是 `--git-dir`，落到真 git，失败原因与本次修复无关）。已改为两个 flag 都转发，使断言真正绑定"答案形态"而不是"某个 flag 的返回值"。
- Step 3 的旧索引兼容断言首版用了 `CONTRIBUTING.md`，但它在派生阶段会被注册表行覆盖 phases，断言永远不成立；改用非注册表路径 `docs/EXTRA_RULE.md`（phases `code,review`），使该行只能来自 carry-over。
- Step 3 的变异验证未能通过整轮 smoke 复现（见 Change Log 第 3 条），改用针对性复现证明断言有效。

## Change Log

- 2026-09-21 由 `TF-20260920-9f3c07` 提升；用户以「提交并pr」定稿范围：完整 TaskFlow 流程、补 Windows 真机回归、非本任务产出的 `todo.md` 条目不提交。
- 2026-09-21 变异验证 1（`hooks/task`）：把 `--absolute-git-dir` 还原为 `--git-dir` 并恢复 `case` 拼接 → smoke 报 `FAIL a drive-path absolute git dir was read as relative to the root`；还原修复后 `ALL SMOKE PASSED`。
- 2026-09-21 变异验证 2（索引日期）：把 `printf '> Last checked: %s\n\n' "$(date +%Y-%m-%d)"` 加回渲染块 → smoke 报 `FAIL index bytes depend on the current date`。
- 2026-09-21 变异验证 3（carry-over 容差）：把 `n < 6 || n > 8` 收紧为 `n != 6` → 直接调用 hook（7 格 fixture）报 `repository-document index contains an invalid row`。**偏差记录**：该变异下的整轮 smoke 未成功执行（本机 5 分钟墙钟限制 + 前一轮后台进程持有临时锁），因此 smoke 层的 `FAIL a pre-drop index row was not carried over` 未被观察到，原因未查明；断言本身的有效性由上述针对性复现证明。整轮 smoke 在带修复的当前代码上为 `ALL SMOKE PASSED`。

## Follow-ups

- Windows CI 目前只跑 `hooks/smoke-test-windows.ps1`，其余 hook 的路径形态无真机覆盖；若要系统性兜住这一类，方向是把 `D:/` 形态的垫片思路也搬进 PowerShell 套件或加一个 Windows 侧的 hook 矩阵。
- `TaskFlowDocs/todo.md` 的 `TF-20260919-c41f8a` 来源不明，需用户确认归属后再决定提交或丢弃。

## Version History

- v1 — planning。
