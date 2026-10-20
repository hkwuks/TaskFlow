# Plan — 任务 ID 校验与 promote 的逆运算

> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md` — 校验器的接口契约、调用点位置、`unpromote` 的拒绝清单与成功语义。

## Reference Pointers

- `hooks/json-field` — 同构先例：一个被多个 hook 用 `bash "$HERE/<name>"` 调用的可执行文件，`hooks/README.md:23` 把它描述成共享组件。`task-id` 走同一条路。
- `hooks/task:24` — `fail()`，`exit 1` 加一行 stderr。所有校验失败都走它。
- `hooks/task:120-127` — `findsec()`，任务匹配用子串 ``` `TaskFlowDocs/<task>/` ```。这是本任务外的已知缺陷，见 Follow-ups。
- `hooks/task:273-280` — `edit` + `loadpairs`，把 Todo 条目的字段改写走已有的 `TASKFLOW_PAIRS` 通道。`unpromote` 复用它，不另写改写逻辑。
- `hooks/task:282-290` — `intake` 的重复目标检查，遍历全部条目、不看状态。决定 `unpromote` 成功输出必须提醒「同目标重 intake 会被拒」。
- `hooks/task:741-758` — 存在性检查跑在路径拼接之后，`mkdir -p "$base"`。校验必须插在这两者之前。
- `hooks/archive:12-19`, `hooks/reopen:22-29` — 两个独立 hook 的入口，同样的 `task="$1"`。
- `hooks/smoke-test:39-46` — 「every hook parses」循环，遍历 `$HERE/*` 跳过 `.md/.ps1/.json/.cmd`，新文件自动纳入。
- `hooks/smoke-test:1660-1705` — 三个 promote 夹具段落，其中任务名 `promoted-in-base` / `promoted-in-worktree` / `promoted-outside-git` 不符合新规则，必须改名。

## Related Tasks

- 前置：`TF-20261020-cd02f5`（本任务的 Todo 条目，已 promote）。
- 相关但独立：`TaskFlowDocs/achieved/2026-10-19-todo-done-compaction/` — 同一个 `hooks/task` 的最近一次改动，`archive` 的条目压缩就是它做的；`unpromote` 改写的 `Status`/`Task`/`Next action` 正是压缩保留的那五个字段中的三个。
- 相关但独立：`TaskFlowDocs/achieved/2026-09-14-branch-and-worktree-gate/` — `promote` 的 base-tree 拒绝就是它加的，`unpromote` 不动那条。

## Skills / Tools Used

- [PRD] `agent-skills:idea-refine` — purpose: 对三个开放设计问题做发散-收敛；outcome: succeeded；incorporated: 确立三条互斥的校验强度选项与两条撤销路径选项，作为向用户提问前的候选集。
- [Spec] `agent-skills:api-and-interface-design` — purpose: 定接口契约；outcome: succeeded；incorporated: 「边界校验」原则把校验器定位在唯一入口文件而不是散点；「错误语义一致」决定了统一走 `fail()`/exit 1 而非 exit 2；「偏好加法而非修改」支持新增 `unpromote` 而不放宽 `remove`。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 拆步骤与依赖；outcome: succeeded；incorporated: 校验器必须先于所有接线（纵向切片的底座），`unpromote` 依赖与 `promote` 相同的模板知识，因此排在校验接线之后；每步留一条可跑的检查。

## Preconditions

- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded — `CONTRIBUTING.md`（分支前缀、`todo.md` 合并、提交格式）、`CODE_STYLE.md`（shell：exit 0/2/3、只读除非明确状态迁移）、`RELEASE.md`（不适用：这不是 release）。`README.md` / `ROADMAP.md` 与本任务无关。个人规则文件在本 clone 不存在（session route line 报告为无）。
- [x] For remote/fork/PR work: remotes, target repository, base branch, local branch/base, freshness limits, and required checks recorded — `origin` = `hkwuks/TaskFlow`，base = `main` at `bf29cd9`，branch `fix/task-id-validation` 从 `main` 切出。远端的 PR 模板 `.github/pull_request_template.md` 在推送后映射进 PR body。
- [x] For PR creation/update: applicable template path, every required-field mapping, and template verification recorded — `.github/pull_request_template.md`；映射在 Step 5 推送后写入 `## Verification / Review`。
- [x] Missing governance drafts and explicit approvals recorded before they become binding — 无缺失。校验规则形状与 `SKILL.md` 的 `YYYY-MM-DD-short-slug` 约定一致，用户 2026-10-20 已确认严格版。

## Approval

- Status: approved
- Approved by: hkwuks
- Approved at: 2026-10-20 21:43 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 一个共享的任务名校验器

- Goal: 把「什么算合法任务名」变成一份可执行的定义，供三个 hook 共用。
- Dependencies: 无。
- Files: `hooks/task-id`（新增）、`hooks/README.md`。
- Implementation checklist:
  - [x] `hooks/task-id` 新增，`#!/usr/bin/env bash` + `set -euo pipefail`，读 `$1`。
  - [x] 合法规则 `^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9][a-z0-9-]*$`；合法 `exit 0` 静默，非法 `exit 1` 并在 stderr 一行给出非法值与期望形状；无参数 `exit 1` 给 usage。
  - [x] 用 `case` 匹配而不是 `grep -E`，与 `hooks/` 其余部分同一风格（`worktree_kind`、`state` 的参数分支都是 `case`）。
  - [x] `hooks/README.md` 的 hooks 树在 `json-field` 旁补一行。
  - [x] `bash -n` 与 `docker run --rm -i bash:3.2 bash -n` 双通过。
- Acceptance: 对 `2026-10-20-task-id-validation`、`2026-10-20-a` 退出 0；对 `--size`、`../evil`、`../../escaped`、`a/b`、`-rf`、空串、`2026-10-20-`、`2026-10-20-Ab` 退出 1。
- Verification: `for c in ...; do bash hooks/task-id "$c"; echo "$c -> $?"; done`，正反各一遍。
- Rollback: 删除该文件，`git checkout -- hooks/README.md`。
- Status: done

### Step 2 — 校验接进每一个取任务名的入口

- Goal: 让 Step 1 的规则真的生效，而不只是存在。
- Dependencies: Step 1。
- Files: `hooks/task`、`hooks/archive`、`hooks/reopen`。
- Implementation checklist:
  - [x] `hooks/task` 已有 `SCRIPT_DIR`（计划里写的 `HERE` 是记错了名字），在 `fail()` 之后新增 `need_task_id` helper 转调校验器。
  - [x] `promote`、`state`、`progress`、`approve`、`complete` 五处在 `task="${rest[…]}";` 之后、任何路径拼接之前调用校验器，失败直接经校验器自己的 stderr 走 `exit 1`。
  - [x] `hooks/archive`、`hooks/reopen` 在 `task="$1"` 之后同样调用。
  - [x] 校验在 `split_root` 之后调用，使 `--root` 仍能写在任意位置。
  - [x] 两个独立 hook 从 `$0` 推导 hooks 目录以找到校验器，不新增环境变量或配置。
- Acceptance: PRD 的六个坏输入对 `promote` 全部退出非 0、不建目录（含仓库外）、`todo.md` digest 不变；同一组输入对 `state`/`progress`/`approve`/`complete`/`archive`/`reopen` 各一条非 0 断言。
- Verification: smoke 新增段落 `== a task name is a single path component, refused before it is joined ==`，六个坏输入 × 七个入口全部断言「非 0 + 输出里有 `invalid task id`」，外加 `todo.md` digest 不变、`evil`/`a`/`escaped` 三个目录不存在，以及本仓库自己的任务名与最小合法名必须被接受。
- Rollback: 还原三个 hook 的该次改动；校验器文件保留无害。
- Status: done

### Step 3 — `task unpromote`

- Goal: 误 promote 之后有一条 CLI 退路，且它不会删掉有内容的目录。
- Dependencies: Step 2（它自己也要过校验）。
- Files: `hooks/task`。
- Implementation checklist:
  - [x] 新子命令 `unpromote`，签名 `unpromote <todo-id> <reason> [--root <path>]`，两个必填参数，reason 为空则 `fail`。
  - [x] 读条目 `Status`/`Task`；`Status` 不是 `promoted` 或 `Task` 不是 ``` `TaskFlowDocs/<slug>/` ``` 形态即 `fail`（后者顺带容纳「Task 指向别的目录」这一类）。
  - [x] 五条拒绝：`achieved/<slug>` 已存在；目录内有被 Git 跟踪的文件；Plan `## Approval` 的 `- Status:` 不是 `requested`；`prd.md`/`plan.md` 的 `> Status:` 不是 `planning`；目录不存在。每条 `fail` 都说出该走哪条路。
  - [x] 通过后把目录里的文件清单打到 stdout（让人看见删了什么），再 `rm -rf`。
  - [x] Todo 条目经 `TASKFLOW_CMD=edit` 写回 `Status: inbox`、`Task: Not promoted.`、`Next action: Clarify and promote when ready.`、`Updated: <today>`；`Notes` 追加一行 `- Unpromoted <today>: <reason>`。
  - [x] 成功输出两行：`unpromote OK: <todo-id> (<slug>)` 与一句「条目已回到 inbox；用同一个目标重跑 intake 会被 duplicate Todo goal 拒绝，改用 task next 改写下一步」。
  - [x] 不做任何 Git 状态操作（不删分支、不动索引）。
  - [x] 实现期间修正：`remove` 拒绝已 promote 条目时的提示语原本说「handle its task first」，现在指向两条真实出路（归档，或用 `unpromote` 撤销误建）。
- Acceptance: 在刚 promote 的目录上成功且四个字段正确；五条拒绝各一条断言且目录仍在。
- Verification: smoke 段落 `== unpromote undoes a promotion, and refuses the four times it must not ==`。
- Rollback: 移除子命令分支；已删目录不可恢复，这是该命令的**目的**，故其拒绝清单是唯一的保护。
- Status: done

### Step 4 — 夹具改名与文档同步

- Goal: 让仓库自己通过新规则，并让文档与命令面一致。
- Dependencies: Step 2。
- Files: `hooks/smoke-test`、`skills/taskflow/SKILL.md`、`CONTRIBUTING.md`。
- Implementation checklist:
  - [x] `promoted-in-base` / `promoted-in-worktree` / `promoted-outside-git` 改为 `2026-01-01-promoted-in-base` 等三个带日期的名字；`:1682` 那条断言打印的 `git worktree add .worktrees/<name>` 整行随之更新，仍指同一件事。
  - [x] `skills/taskflow/SKILL.md:60` 的命令列举补 `unpromote`，并加一段说明任务名形状与 `unpromote` 的拒绝条件。
  - [x] `CONTRIBUTING.md:29` 旁补一条：任务名是单个路径组件，且 `unpromote` 是误 promote 的退路。
  - [x] `hooks/README.md` 的 `task` 一行更新为含 `unpromote`。
  - [x] 实现期间发现并修：`complete rolls back doc status when archive fails` 的夹具把 `hooks/task` 单独拷进临时目录，`task` 现在经 `SCRIPT_DIR` 找校验器，那份拷贝必须同时带上 `hooks/task-id`，否则该段会以「No such file」而不是它本来的断言失败。
- Acceptance: `bash hooks/smoke-test` 全绿；`bash -n` 全部通过。
- Verification: 全量 smoke（81 段 `ok`）；`bash hooks/todo-check .`、`bash hooks/repository-check .`。
- Rollback: 还原该次改动。
- Status: done

### Step 5 — 变异验证与推送

- Goal: 证明新断言真的会红，并把工作推成可评审的 PR。
- Dependencies: Step 1–4。
- Files: `TaskFlowDocs/2026-10-20-task-id-validation/plan.md`、PR body。
- Implementation checklist:
  - [x] 逐条变异：去掉校验器的某条分支、去掉某处调用、放宽 `unpromote` 的每条拒绝、去掉 Todo 字段写回——十一个变异，每个都让一条断言变红。
  - [x] 变异在 `/tmp` 副本上做，一次一个，还原后再做下一个。
  - [x] `git diff --check`、`quick_validate.py skills/taskflow`、`docker run bash:3.2 bash -n`。
  - [x] 推送 `fix/task-id-validation`，按 `.github/pull_request_template.md` 建草稿 PR，把落地声明写进 PR body。
- Acceptance: 每个变异至少让它对应的那条断言变红；CI 六个 job 全绿。
- Verification: 映射写进 `## Verification / Review`。
- Rollback: 还原变异副本，工作树不变。
- Status: done

## Checkpoints

### Checkpoint — Step 1 之后

- [x] 校验器正反两个方向都对（17 个输入逐一验过）；此时代码里尚无任何调用点，`bash hooks/smoke-test` 保持基线绿。

### Checkpoint — Step 2 之后

- [x] 六个坏输入在七个入口上全部被拒；合规输入的既有 smoke 断言无一变红。

## Change Log

- 2026-10-20：`unpromote` 的「是不是刚 promote 出来的」判据从「与模板逐字节一致」改为四条状态判据。原因：字节判据会随模板措辞漂移，改一个标点就让所有旧 promotion 转向拒绝。四条状态判据各自对应一种「有人开始干活了」，与措辞无关。代价（改了正文但没改状态会被删）记入 PRD Risks。
- 2026-10-20：PRD 的 `unpromote` 拒绝用例从「未跟踪文件」改为「被跟踪文件 + 状态判据」。原因：未跟踪文件是**正常**的（`promote` 刚建出来的目录本身就是未跟踪的），拿它当拒绝条件会让命令永远无法成功。

## Follow-ups

- **`findsec()` 用子串匹配任务路径**（`hooks/task:120-127`）：`<task> = a/b` 与 `<task> = b` 会匹配同一个字符串。形状校验堵住了越界路径的产生，但没有修匹配逻辑本身；一旦将来允许嵌套目录名，这就是个静默串味。未在本任务范围内，因为修它需要先回答「历史目录要不要兼容」，而本仓库没有不合规目录，暂无可依据的样本。
- **`hooks/task` 的 `HERE` 是新引入的**：本任务第一次让 `hooks/task` 依赖同目录下的另一个文件。若将来有宿主把 hook 拆散布署，这里会是第一个失效点；目前所有宿主都整目录复制（`hooks.json` 的 `${CLAUDE_PLUGIN_ROOT}`）。

## Verification / Review

全部在本 worktree 的 `fix/task-id-validation` 上跑。

- [x] `bash hooks/smoke-test` — exit `0`，**81 段 `ok`**，`ALL SMOKE PASSED`。比基线多 2 段（`a task name is a single path component…`、`unpromote undoes a promotion…`），其余段落零改动通过。
- [x] CI —— run [`39440052047`](https://github.com/hkwuks/TaskFlow/actions/runs/39440052047) 在 head `ac68415` 上六项全绿：`evals`、`release`、`smoke`（ubuntu 19s / macos 1m4s / windows 35s）、`todo-merge-audit`。macOS 与 Windows 两项是这次最该看的：新校验器用 `case` glob 实现，两个平台上 bash 的类匹配行为必须一致。
- [x] `bash -n` 与 `docker run --rm -i bash:3.2 bash -n` — `hooks/task-id`、`hooks/task`、`hooks/archive`、`hooks/reopen`、`hooks/smoke-test` 五个文件全部通过。
- [x] `git diff --check` — clean。
- [x] `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow` — `Skill is valid!`
- [x] `bash hooks/todo-check .` — `STATUS: pass`
- [x] `bash hooks/release-check` — `STATUS: pass`，版本字面量未动
- [x] `bash hooks/repository-check .` — 唯一发现是本任务目录未提交（执行该检查时它确实未提交）；`Orphan task directories: none`、`Stale task worktrees: none`

### 十一个变异，十一条断言

每个变异单独打在 `/tmp` 的完整副本上，跑完即还原。两个变异先暴露的是**测试**的洞，修完测试再重跑：

| # | 变异 | 变红的断言 |
| --- | --- | --- |
| 1 | 校验器里 slug 字符类检查失效 | `FAIL task promote TF-20260101-bad 2026-01-01-a/b small accepted a bad name` |
| 2 | 日期前缀改成接受任何值 | `FAIL task promote TF-20260101-bad --size small accepted a bad name` |
| 3 | `promote` 不再调用校验器 | `FAIL task promote TF-20260101-bad --size small accepted a bad name` |
| 4 | `state` 不再调用 | `FAIL task state --size ready refused without naming the rule` |
| 5 | `archive` 不再调用 | `FAIL archive refused without naming the rule` |
| 6 | `reopen` 不再调用 | `FAIL reopen refused without naming the rule` |
| 7 | `unpromote` 去掉「目录被 Git 跟踪」拒绝 | `FAIL unpromote removed a committed task directory` |
| 8 | `unpromote` 去掉 Approval 拒绝 | `FAIL unpromote removed an approved task` |
| 9 | `unpromote` 去掉文档状态拒绝 | `FAIL unpromote removed a task whose documents moved on` |
| 10 | `unpromote` 把 `Status` 写回 `promoted` 而不是 `inbox` | `FAIL unpromote did not return the entry to inbox` |
| 11 | `unpromote` 不再打印要删的文件 | `FAIL unpromote did not name what it removed` |

**M1 第一次没有被任何断言抓住。** 六个坏输入（`--size`、`../evil`、`../../escaped`、`a/b`、`-rf`、空串）全部由**日期前缀**那一半规则拒掉，slug 字符类那半从来没有被测到——校验器只剩一半也能全绿。修法是给坏输入加上三个「日期合法、slug 非法」的样本（`2026-01-01-Ab`、`2026-01-01-a/b`、`2026-01-01-a b`），重跑后 M1 才变红。这是测试的洞，不是实现的洞。

**M10 的第一版是语法错误。** 用 `:` 顶掉那段 `printf … > "$tmp_pairs"` 时把 `}` 也吃掉了，`bash -n` 失败，整个套件在任何断言之前就死了——错误的「红」。改成一个语义变异（`Status` 写回 `promoted`）之后才是真的断言变红。

### 一处渠道错位，值得记

变异 3、4 第一次跑出来是「脚本自己坏了」而不是「断言变红」：`bash -n` 通过，但套件在别处静默死掉。原因是那台机器上同时还有别的后台 `smoke-test` 在跑，两个进程共用 `mktemp` 目录名空间之外的东西——更要紧的是，`git checkout -- .` 在第一个沙箱里跑过之后，第二个沙箱的变异被打在别的地方。教训与本次改动无关，但重跑时必须一次一个、每次独立日志文件、每次确认 `git status` 空。

### 推送与 PR

- 提交 `ac68415` 推到 `fix/task-id-validation`。
- 草稿 PR [#89](https://github.com/hkwuks/TaskFlow/pull/89)，body 按 `.github/pull_request_template.md` 五节填写；`## Verification` 里只有 CI 那一项待勾。
- 变异记录（上表）与两处测试缺陷都写进了 PR body，因为它们属于「这个断言凭什么可信」的一部分，评审时与 diff 一起读。
- PR [#89](https://github.com/hkwuks/TaskFlow/pull/89) 已标记 ready。head `fc484c6` 的 CI run [`39440465074`](https://github.com/hkwuks/TaskFlow/actions/runs/39440465074) 六项全绿。

### 落地与归档

PR [#89](https://github.com/hkwuks/TaskFlow/pull/89) 合并为 `55ed850`。归档由一个收尾 PR 完成，而不是随本任务自己的 PR —— 这是顺序失误的补救，记在下面。

**顺序错了。** `CONTRIBUTING.md:102` 要求「写验证记录 → 提交推送 → 归档 → 提交推送 → 标 ready」，我在写验证记录后就把 PR 标成了 ready，用户在归档之前合并。结果是任务文档落在了 main 上、任务目录仍活着。补救方式是唯一剩下的一条：开 `chore/archive-task-id-validation` 做归档移动 + Todo 切 `done`。`CONTRIBUTING.md:44` 明说任务文档应当随它自己的 PR 落地，所以这个 PR 形式上就是那一处禁止的拆分；它存在只是因为 #89 已经没有落点了。下次的正确顺序是标 ready 放在最后一步。
