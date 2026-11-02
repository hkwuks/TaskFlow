# Plan — 给新用户一份可用的默认仓库规则

> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md` — 目标、命令、目录、风格、测试策略、边界。
- `prd.md` — 需求 R1–R6 与验收 A1–A8。

## Reference Pointers

- `hooks/prompt-reminder` — 每条提示都运行的 `UserPromptSubmit` 钩子；提醒借这条事件，不新造机制。它只在 `in_progress`/`checking` 阶段输出，三个触发点都在其中。
- `hooks/prompt-reminder:140-175` — `## Reference Pointers` 的 `[Reinforce]` 解析，是"在 Plan 里声明要提醒什么"的既有先例。
- `hooks/repository-docs-context:64-65` — 无条件把 `CONTRIBUTING.md` / `CODE_STYLE.md` 登记为路由目标的两行；新用户正是被这两行指向不存在的文件。
- `hooks/repository-check:33-39` — 缺这两份文件时判 `needs-user-input`。
- `skills/taskflow/SKILL.md:95` — 已有"缺文档时帮用户创建"的规则；本任务给它一份默认内容与一个征询机制。
- `CONTRIBUTING.md` 的 `## Branches and commits`、`## Pull requests` — 模板通用内容的来源。
- `CODE_STYLE.md` 的 `## Markdown`、`## Shell`、`## Simplicity and compatibility` — 同上。
- `hooks/install-git-hygiene` — 既有的"往用户仓库写东西"先例（append-only、幂等、失败退出 0）。

## Related Tasks

- `2026-11-02-fork-topology` — 同批推进；它补 remote 拓扑，本任务补仓库规则，互不重叠。

## Skills / Tools Used

- [PRD] `agent-skills:spec` — 把散落事实收敛成需求与验收标准。
- [Spec] `agent-skills:spec-driven-development` — 确定命令形状、目录与测试策略。
- [Plan] `agent-skills:planning-and-task-breakdown` — 复核 Step 拆分，并把冲突判据收紧到可实现的精度。
- [Test] `Unaided` — considered: testing strategy。断言写在 `hooks/smoke-test` 既有风格内。

## Preconditions

- 工作树 `.worktrees/default-rules`，分支 `feat/default-working-rules`，基线 `main@d5e2e7f`。
- 本仓库没有 `TaskFlowDocs/repository-docs/personal.md`（本任务不使用个人规则通道）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-02 21:40 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — `repo-rules show` 与两份模板

- Goal: 用户不写任何文件就能看到默认规则是什么。
- Dependencies: 无。
- Files: `hooks/templates/CONTRIBUTING.md`、`hooks/templates/CODE_STYLE.md`、`hooks/repo-rules`。
- Implementation checklist:
  - [x] 从本仓库 `CONTRIBUTING.md` 的 `## Branches and commits`、`## Pull requests` 提炼通用部分；剔除 `## Working branches`、`## TaskFlow workflow`、`## Checks` 里本仓库特有的命令（R2）。
  - [x] 从 `CODE_STYLE.md` 的 `## Markdown`、`## Shell`、`## Simplicity and compatibility` 提炼；剔除 `## Task artifacts`。
  - [x] 模板头注明来源与版本（spec 的 Code style 节）。
  - [x] `repo-rules show <name>`：打印模板全文到 stdout，**不写任何文件**（A7）。
  - [x] `show` 在无网络、无 `gh` 的 PATH 下仍工作（A7）。
- Acceptance: A2（内容层面）、A7。
- Verification: smoke 断言 `show` 输出含关键字；`grep` 断言模板不含 `TaskFlowDocs/achieved`、不含 `capability`；断言 `show` 前后目标目录 `diff` 为空。
- Rollback: 删除 `hooks/templates/` 与 `hooks/repo-rules`。
- Status: done

### Step 2 — `repo-rules create`

- Goal: 用户同意后，模板落到他的仓库根目录；已存在则拒绝。
- Dependencies: Step 1。
- Files: `hooks/repo-rules`。
- Implementation checklist:
  - [x] `repo-rules create <name>`：目标文件已存在 → 拒绝，退出 2，点名该文件。
  - [x] 不存在 → 写入 `<root>/<name>`，打印写入路径。
  - [x] 只接受两个已知名字，其他名字拒绝——这个命令不是通用文件写入器。
- Acceptance: A3、R5、R2。
- Verification: 夹具仓库跑 create 后断言文件存在且内容等于模板；再跑一次断言退出 2 且文件未变（`diff`）。
- Rollback: 同 Step 1。
- Status: done

### Step 3 — `repo-rules check`：冲突判据

- Goal: 已有规则时，指出与 TaskFlow 冲突的具体行，不改文件。
- Dependencies: Step 1（同文件）。
- Files: `hooks/repo-rules`。
- Implementation checklist:
  - [x] 三条**可机械判定**的冲突，每条都说明它冲突的是 TaskFlow 的哪条规则：

    | 判据 | 冲突的 TaskFlow 规则 |
    |---|---|
    | 文档要求「所有改动走 PR」且未给发布留例外 | `RELEASE.md` 的发布是 tag + pin 直接推送，不走 PR |
    | 文档要求 commit 信息带固定前缀或模板，与 `<type>: <描述>` 冲突 | `CONTRIBUTING.md` 的 commit 约定 |
    | 文档要求直接在主分支提交 | `CONTRIBUTING.md` 的「一任务一分支一工作树」 |

  - [x] 每条判据的匹配范围写进代码注释：它们是**关键字匹配**，会漏报也会误报，因此输出措辞是"可能冲突，请确认"而不是"冲突"。
  - [x] 输出含 `文件:行号` 与命中的原文片段（R6）。
  - [x] 无冲突时输出一行 "no conflicts found"，退出 0。
  - [x] `check` 不写任何文件。
- Acceptance: A4、R6。
- Verification: 三个夹具各含一条冲突，断言各自的行号与原文被点名；再断言 `diff` 未变。**并测一个反例**：一份含 `prefix` 字样但与 commit 无关的文档，断言不误报。
- Rollback: 同 Step 1。
- Status: done

### Step 4 — 三个触发点的提醒

- Goal: 在建分支前、决定 commit 归属前、写代码前提示；其余时刻安静。
- Dependencies: Step 1–3。
- Files: `hooks/prompt-reminder`。
- Implementation checklist:
  - [x] 在既有四行输出之后追加一段，**不改那四行**（A8）。
  - [x] 判定当前 Step 的意图（建分支 / commit / 写代码），依据 Plan 的 Step 标题关键字；判定不了就不提醒——宁可漏报也不要在无关时刻打扰。
  - [x] 缺文件 → 一行，含文件名与 `repo-rules show` 用法（A1）。
  - [x] 有文件且有冲突 → 一行，含 `repo-rules check` 的结论摘要（A4）。
  - [x] 有文件且无冲突 → 零输出（A8）。
  - [x] 所有错误路径退出 0，不改变调用方的退出码（A6）。
- Acceptance: A1、A4、A5、A6、A8。
- Verification: 三种仓库状态 × 三种 Step，共九个组合，断言输出有/无；外加一个非触发阶段的 Step 断言零输出。
- Rollback: 回退 `prompt-reminder` 的这一段。
- Status: done

### Step 5 — 文档与清单同步

- Goal: 让读者知道默认规则从哪来；让仓库的清单断言继续成立。
- Dependencies: Step 1–4。
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`hooks/README.md`、`skills/taskflow/references/runtime.md`。
- Implementation checklist:
  - [x] `SKILL.md:95` 附近说明：缺 `CONTRIBUTING.md`/`CODE_STYLE.md` 时先 `show` 再征询，不自动写。
  - [x] `artifacts.md:7` 同样补充，与 SKILL.md 不矛盾。
  - [x] `hooks/README.md` 清单加 `repo-rules` 与 `templates/`。
  - [x] `runtime.md` 的 hook 树加两行。
- Acceptance: 两份清单断言仍绿（它们已要求点名每个 hook）。
- Verification: 全量 smoke。
- Rollback: 文档改动可单独回退。
- Status: done

## Checkpoints

- Step 1–3 后：在一个空夹具仓库里手工跑 `show` → `create` → `check`，确认输出对用户有意义。
- Step 4 后：三个触发点各手工验一次，确认提醒出现且不阻塞。
- Step 5 后：全量 smoke + `repository-check` + `release-check` 全绿。

## Verification / Review

**smoke：`ALL SMOKE PASSED`**，新增两节：
`repo-rules offers a default rule set, and only writes when asked`
`the default-rules reminder fires where a rule is needed and nowhere else`

### 真实输出

```
$ bash hooks/repo-rules check --root <含冲突的仓库>
CONTRIBUTING.md:3: possible conflict — requires a pull request for every change,
  but RELEASE.md tags the base commit and pushes the pin directly
  All changes must go through a pull request.
CONTRIBUTING.md:5: possible conflict — states a commit prefix;
  TaskFlow writes <type>: <imperative description>
  Use prefix `[FEAT]` for commits.
CONTRIBUTING.md:7: possible conflict — commits directly to the main branch;
  TaskFlow works one task per branch in its own worktree
  Commit directly to main when convenient.
```

```
$ bash hooks/repo-rules create CONTRIBUTING --root <空仓库>
repo-rules: wrote <repo>/CONTRIBUTING.md
$ bash hooks/repo-rules create CONTRIBUTING --root <同一仓库>
repo-rules: CONTRIBUTING.md already exists at <repo>/CONTRIBUTING.md; leaving it alone
exit=2
```

### 变异验证

| 变异 | 红在哪 |
|---|---|
| `create` 不再拒绝已存在文件 | `FAIL repo-rules create did not refuse an existing file (exit 0)` |
| 模板泄漏 `TaskFlowDocs/achieved/` | `FAIL CONTRIBUTING template names achieved/` |
| 提醒不看 Step 标题，永远触发 | `FAIL an undeclared Plan changed the reminder's line count` |
| 提醒不再点名缺失的文件 | `FAIL 'branch' did not offer the default rules` |

每次还原后 `cmp` 确认字节一致。

### 实施中修掉的四个真实缺陷

1. **`check` 的三条判据全部漏报**：`$(grep ...)` 在 `set -e` 下，grep 找不到时退出非 0，把整个函数带走。改用进程替换 + `|| true`。
2. **commit prefix 判据的方向反了**：只匹配 `commit.*prefix`，而 “Use prefix X for commits” 是 prefix 在前。
3. **`dr_case` 留下多个任务目录**：`summarize-state` 因此报 “Multiple active tasks” 并静默，只有字母序最后一个用例可能通过。
4. **`&&` 作函数最后一条语句**：absence 正确地让 grep 返回 1，`set -e` 于是无消息地结束整个 suite。同一形态在另一处也存在，一并改成 `if`。

第 3 与第 4 条属于同一类：**一个断言静默不执行，看起来和"没有失败"一样**。这正是本仓库 smoke 反复要防的东西。

## Change Log

- 2026-11-02 — v1 起草。用户已确定：模板从本仓库提炼通用部分、放 `hooks/templates/`、同意后才复制；触发点为建分支前／commit 归属前／写代码前；每次都问，不做一次性标记。
- 2026-11-02 — 应用户要求用 `planning-and-task-breakdown` 复核，拆出五步（原为三步），其中把 `repo-rules` 拆成 show / create / check 三个可独立验收的 Step，并把冲突判据从一句描述收紧成三条具体规则 + 一个反例测试。

## Follow-ups

- **三条冲突判据是关键字匹配，会漏报也会误报。** 输出因此写成"可能冲突，请确认"。若要更准，需要真正的 Markdown 语义解析，本任务不做。
- **"每次都问"在没有规则文件的仓库里会持续出现。** 用户明确选择的代价。若要改，正确做法是让提醒变短而非加缓存。
- **模板与本仓库规则会漂移。** 模板头注明来源版本；本仓库规则大幅变动时应重新提炼。

## Version History

- v1 — planning.
