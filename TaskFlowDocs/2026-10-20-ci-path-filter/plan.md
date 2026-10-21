# Plan — 让 Hooks workflow 只跑改动能影响的 job

> Task version: v1
> Status: checking

## Spec Pointers

- `spec.md` — `tools/workflow-affected` 的输入/输出契约、退出码恒 0 的理由、三条路径集合的依据、`changes` job 的取路径方式、`concurrency` 的取消边界。

## Reference Pointers

- `.github/workflows/hooks.yml` — 现有四个 job 与它们各自的依赖，注释里已经写了每个 job 存在的理由（`release` 修的是「README 样本漂在旧版本上没人看见」，`todo-merge-audit` 修的是 2026-09-15 那次 host 端合并丢条目）。
- `hooks/release-check:20-31` — 九个固定输入文件，是 `release` 集合的唯一依据。
- `hooks/smoke-test:1939-1961` — 把 `TaskFlowDocs/todo.md` 的模板字段与 `hooks/task` 实际写的字段对账。这就是 `todo.md` 必须进 `smoke` 集合的原因。
- `hooks/smoke-test:1915-1937`、`:2019-2148`、`:4127-4149` — smoke 读真实树的其他位置（`skills/taskflow/`、`CODE_STYLE.md`、`CONTRIBUTING.md`、`RELEASE.md`、`hooks/README.md`、`hooks/capability-gate`）。
- `tools/fixture-compare` — `tools/` 的既有先例：仓库自己的开发工具，不进插件运行时，README 与 CHANGELOG 已把它与 hooks 分开描述。
- `hooks/smoke-test` 的「every hook parses」循环（`:39-46`）只遍历 `$HERE/*`，**不会**覆盖 `tools/`——所以新工具需要自己的语法断言。

## Related Tasks

- 前置：`TF-20261020-a46573`（本任务的 Todo 条目）。
- 直接相关：`TaskFlowDocs/achieved/2026-09-13-hooks-ci-matrix/` — 建立 `Hooks` workflow 的任务。本任务改的是它的调度，不是它的内容。
- 直接相关：`TaskFlowDocs/achieved/2026-09-16-web-ui-merge-loss-guard/` — `todo-merge-audit` 的来源。它必须永远跑，这是那条任务的前提。
- 相邻但独立：`TF-20260928-3910fb`（发布流程的三宿主校验）——同样在 CI 里，但动的是 release 检查的内容，不是调度。

## Skills / Tools Used

- [PRD] `agent-skills:ci-cd-and-automation` — purpose: 决定路径分诊的粒度与安全默认；outcome: succeeded；incorporated: 「只跑改动影响的」被明确列在 CI 优化的第三档，且排在缓存与并行之后——所以它值得做，但不该先于更便宜的优化；「CI failures 不得被静默」直接决定了本任务的核心约束（未知路径跑全部、分类器退出码恒 0）。
- [Spec] `agent-skills:api-and-interface-design` — purpose: 定 `tools/workflow-affected` 的契约；outcome: succeeded；incorporated: 「在边界校验、内部信任」把路径集合收进工具一处，workflow 不含 glob；「错误语义一致」决定了可疑输入走安全默认而不是非零退出；Hyrum 定律提醒三个 key 的名字与顺序是可观察行为，smoke 必须按名字取值。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 拆步骤与依赖；outcome: succeeded；incorporated: 分类器必须先于接线（它是可单测的基座），smoke 断言最后写（它要读已稳定的集合）。

## Preconditions

- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded — `CONTRIBUTING.md`（分支前缀、落地、提交格式）、`CODE_STYLE.md`（shell：exit 0/2/3、只读除非明确状态迁移）、`RELEASE.md`（不适用：不是 release）。个人规则文件在本 clone 不存在。
- [x] For remote/fork/PR work: remotes, target repository, base branch, local branch/base, freshness limits, and required checks recorded — `origin` = `hkwuks/TaskFlow`，base = `main` at `ba07c89`，branch `chore/ci-path-filter` 从 `main` 切出。**该仓库没有分支保护也没有 ruleset**，所以 required checks 为空集——这一点直接影响本任务的风险评估（漏跑没有任何外部提示）。
- [x] For PR creation/update: applicable template path, every required-field mapping, and template verification recorded — `.github/pull_request_template.md`，映射在 Step 4 推送后写入。
- [x] Missing governance drafts and explicit approvals recorded before they become binding — 无缺失。

## Approval

- Status: approved
- Approved by: hkwuks
- Approved at: 2026-10-20 23:24 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — `tools/workflow-affected`

- Goal: 把路径集合与分类规则变成一份可单独执行、可单独测试的定义。
- Dependencies: 无。
- Files: `tools/workflow-affected`（新增）。
- Implementation checklist:
  - [x] 新增可执行文件，`#!/usr/bin/env bash` + `set -euo pipefail`，参数是改动路径。
  - [x] 三条集合各写成 `case` glob，前置注释逐条给出依据（`release-check:20-31`、`smoke-test:1939-1961`、`smoke-test:3526-3650` 夹具而非真实树）。
  - [x] 输出固定三行、固定顺序：`smoke=` / `release=` / `evals=`，值只有 `true`/`false`。
  - [x] 退出码恒 `0`；空参数与未知路径都输出全 `true`，并各在 stderr 说一句。
  - [x] 无 `mapfile`、无 `declare -A`、无进程替换；`bash -n` 与 `docker run bash:3.2 bash -n` 双通过。
  - [x] 实现期间补：工具自身路径与 `.github/workflows/**` 显式进 `smoke` 集合。前者原本靠「落在 tools/ 所以算未知 → 全跑」偶然对了，答案是全跑但理由是错的；后者原本混在 smoke 的长 glob 里，挪出来与前者并列，因为两者都是「改了调度器就得跑一次」。
- Acceptance: 空参数 → 三个 `true`；`TaskFlowDocs/2026-01-01-x/plan.md` → smoke=false release=false evals=false；`TaskFlowDocs/todo.md` → smoke=true release=false evals=false；`README.md` → release=true smoke=false；`hooks/task` → smoke=true release=false；`evals/cases/x.json` → evals=true；`nonsense/path` → 三个全 `true`。每种情形退出码都是 `0`。
- Verification: 一个 `for` 循环跑上表每行并断言整行输出。
- Rollback: 删除该文件；workflow 尚未引用它，行为不变。
- Status: done

### Step 2 — workflow 接线

- Goal: 让分诊真的生效。
- Dependencies: Step 1。
- Files: `.github/workflows/hooks.yml`。
- Implementation checklist:
  - [x] 顶层加 `concurrency`：`${{ github.workflow }}-${{ github.ref }}`，`cancel-in-progress: ${{ github.event_name == 'pull_request' }}`，注释写清为什么 main 上不取消。
  - [x] 新增 `changes` job：`actions/checkout@v4` with `fetch-depth: 0`；`pull_request` 走 `git diff --name-only <base.sha> <head.sha>`，其他事件写空清单（空即「全跑」，与 spec 的契约一致）；把清单喂给 `tools/workflow-affected`，三个值写进 `$GITHUB_OUTPUT`。
  - [x] `smoke`、`release`、`evals` 各加 `needs: changes` 与 `if: needs.changes.outputs.<key> == 'true'`；**job 内容一行不改**。
  - [x] `todo-merge-audit` 不加任何条件，并补一句注释说明它为什么必须无条件。
  - [x] bash 数组用 `while IFS= read -r` 累积，不用 `mapfile`。
  - [x] 实现期间踩到并修：`done < changed` 循环体若以 `[ -n "$path" ] && paths+=(...)` 结尾，末行是空行时循环退出码为 1，`set -e` 会让这个「决定空 diff 安全」的 job 自己失败。改成 `if` 形式。
  - [x] 实现期间踩到并修：bash 3.2 下 `set -u` 里 `"${paths[@]}"` 对空数组报 `unbound variable`（实测：`bash: line 3: paths[@]: unbound variable`），改用 `${paths[@]+"${paths[@]}"}`。
- Acceptance: PRD 的 Acceptance Criteria 里那六条路径情形，在 `tools/workflow-affected` 上直接验；workflow 的结构用 `python3 -c 'yaml.safe_load(...)'` 验可解析，并断言四个 job 的 `if` 与 `needs` 字面正确。
- Verification: 读回 workflow，逐 job 断言 `needs`/`if`；本地跑分类器覆盖六种路径。
- Rollback: 还原该文件；分诊消失，行为退回「全跑」。
- Status: done

### Step 3 — smoke 里的对账与分诊断言

- Goal: 让路径集合与真实读取的漂移变成红色。
- Dependencies: Step 1、Step 2。
- Files: `hooks/smoke-test`、`hooks/task-id` 的调用点（`hooks/smoke-test:1791` 那一段）。
- Implementation checklist:
  - [x] 新增一段：从 `hooks/release-check` 抓出它读的九个文件，逐个断言 `tools/workflow-affected` 对它们的判定包含 `release=true`。
  - [x] 从 `hooks/smoke-test` 自己抓出 `$repo/` 与 `$HERE/../` 读取路径，逐个断言 `smoke=true`。
  - [x] 断言 `tools/workflow-affected` 自身改动 → `smoke=true`（否则改了工具没有验证）。
  - [x] 断言 `.github/workflows/hooks.yml` 改动 → `smoke=true`。
  - [x] 断言未知路径 → 三个全 `true`。
  - [x] 断言 `tools/workflow-affected` 的 `bash -n` 通过（「every hook parses」循环不覆盖 `tools/`）。
  - [x] 断言 workflow 的 `todo-merge-audit` 没有 `if`。
  - [x] 实现期间发现并修：**`hooks/smoke-test:1791` 遍历真实活动任务目录名**，因为它是相对路径而不是 `$repo/` 前缀，抽取没抓到它，Step 1 的「任务目录不被任何 job 读」因此是假话。改成字面样本，并说明为什么用真实目录当样本本身是循环论证（目录存在只是因为同一条规则接受过它）。
  - [x] 实现期间发现并修：**`assert_affected` 只看值，看不见「掉进未知兜底」**。每个集合遗漏都会退化成 unknown，而 unknown 对三个 key 全答 `true`，所以删掉 `README.md` 的 release 归属后断言仍然绿（M2 实测）。新增 `assert_known`，读 stderr 判定「这个路径被归类了」。
  - [x] 实现期间发现并修：抽取出的 `SKILL.md`、`agents`、`references` 是**smoke 断言其必须不存在**的路径，不是不相关路径——它们出现即为 smoke 结果，加进 `smoke` 集合。
- Acceptance: `bash hooks/smoke-test` 全绿；每个新断言各有一条只让它变红的变异。
- Verification: 全量 smoke 82 段 `ok`，`ALL SMOKE PASSED`；变异 M1–M6 各自命中预期断言（映射见 Step 4）。
- Rollback: 还原该文件。
- Status: done

### Step 4 — 变异验证与推送

- Goal: 证明对账断言真的会红，并把工作推成可评审的 PR。
- Dependencies: Step 1–3。
- Files: `TaskFlowDocs/2026-10-20-ci-path-filter/plan.md`、PR body。
- Implementation checklist:
  - [x] 逐条变异，一次一个，在 `/tmp` 副本上：从工具里删掉 `TaskFlowDocs/todo.md` 的 smoke 匹配；删掉 `README.md` 的 release 匹配；把未知路径默认改成全 `false`；给 `todo-merge-audit` 加一个 `if`；让分类器对未知路径退出 `1`。另加两条实现期间补的：M6（删任务文档归类）、M7（把 `release` 的 `if` 指向 `smoke` 的 key）。
  - [x] `git diff --check`、`quick_validate.py skills/taskflow`、`docker run bash:3.2 bash -n`。
  - [x] 推送 `chore/ci-path-filter`，按 `.github/pull_request_template.md` 建草稿 PR（#91），把落地声明写进 PR body。
  - [x] **归档提交也要推上同一个 PR，最后才标 ready** —— 上个任务就是因为标 ready 早于归档而需要补一个 PR。
- Acceptance: 每个变异至少让它对应的那条断言变红；CI 六项全绿。
- Verification: 映射写进 `## Verification / Review`。
- Rollback: 还原变异副本。
- Status: done

## Checkpoints

### Checkpoint — Step 1 之后

- [ ] 分类器对七种路径情形的输出与 PRD 一致，且每种都退出 `0`。

### Checkpoint — Step 2 之后

- [ ] workflow 可被 YAML 解析；`todo-merge-audit` 无条件；另外三个的 `needs`/`if` 字面正确。

## Change Log

- 2026-10-20：PRD 的 Acceptance Criteria 原本要求「一个改 `hooks/task` 的改动 → `smoke`、`release` 都 `true`」，与 Background 里 `release-check` 不读 `hooks/` 的实测矛盾。改为只有 `smoke` 为 `true`，并把这条单独写成一个变异（把它改回 `release=true` 应当没有任何断言变红，因为那是过度保守而不是错误——但列出它可以让评审看到取舍）。
- 2026-10-21：**PRD 第 19 行「`TaskFlowDocs/<task>/` 不被任何 job 读」在实现期间被推翻。** `hooks/smoke-test:1791` 用相对路径 `for d in TaskFlowDocs/*/` 遍历真实活动任务目录名。这条路是在 Step 3 的抽取断言变红时发现的，不是设计时想到的。两条修正：
  1. 那一段改成五个字面样本（`2026-10-20-task-id-validation`、`2026-09-13-hooks-ci-matrix`、`2026-09-08-smoke`、`2026-01-01-a`、`2026-12-31-a1b2c3`）。用真实目录当样本本身是循环论证——目录存在只是因为同一条规则接受过它——而且让 smoke 的输入取决于当前检出哪条分支，这正是本任务要消除的那种隐性耦合。已验证：在没有活动任务目录的树里 smoke 仍然全绿；放入一个名字非法的活动目录 `2026-99-99-bogus` 也不再影响 smoke。
  2. `tools/workflow-affected` 新增 `TaskFlowDocs/*/*) matched=1`，把这条显式写出来而不是靠未知兜底——兜底会给出同样的答案，但理由与这些文件无关，而这一条恰恰是「以为没人读、其实有人读」的实证。
- 2026-10-21：**PRD 第 10 行的价值陈述也偏了。** PR #90 的 `todo.md` 改动（归档回写 `- Status:` / `- Task:`）落在 smoke 的输入集合里，所以那一类改动**即使本任务全部落地也仍然跑 smoke**。现在的收益是：`release`、`evals` 各省一个 ubuntu job（纯文档 PR 合计约 1 分钟），纯任务文档（不动 `todo.md`）的 PR 连 smoke 也省掉，以及 `concurrency` 取消被取代的排队。

## Verification / Review

**CI（权威）**：run `39615724218`，`gh pr view` 可见。`changes: success`、`smoke (ubuntu|macos|windows): success`、`todo-merge-audit: success`、`release: skipped`、`evals: skipped`。skipped 两项不是漏跑——这次改动只碰 `hooks/smoke-test`，它们本来就不读这个路径，正是本任务要的结果。

**第一次 CI 是红的，原因值得记**：run `39614963300`，`smoke (macos-latest)` 报 `ModuleNotFoundError: No module named 'yaml'`。`todo-merge-audit` 的结构断言用了 `python3 + yaml.safe_load`，ubuntu 镜像带 PyYAML、macOS 不带，所以这条断言在两个宿主上通过、在第三个上根本没执行。改为 `awk` 读两空格 job 名与四空格键，形状不合即红。这也踩在本仓库自己的硬规矩上——hooks 不依赖任何语言运行时，`smoke-test:174` 专门用一条精简 PATH 测它。

**全量 smoke**：`bash hooks/smoke-test` → `ALL SMOKE PASSED`，82 段 `ok`（实现前 81）。

**语法底线**：`bash -n` 与 `docker run --rm -i bash:3.2 bash -n` 双通过（`tools/workflow-affected`）。

**本地检查**：`git diff --check` 通过；`quick_validate.py skills/taskflow` → `Skill is valid!`。

**变异验证**：一次一个，各自在 `/tmp` 副本与独立日志里跑全量 smoke。

| 变异 | 改了什么 | 命中 |
| --- | --- | --- |
| M1 | 从 `smoke` 集合删掉 `TaskFlowDocs/todo.md` | `FAIL TaskFlowDocs/todo.md is in no set (classified as unknown)` |
| M2 | 从 `release` 集合删掉 `README.md` | `FAIL README.md is in no set (classified as unknown)` |
| M3 | 未知路径默认改成全 `false` | `FAIL an unknown path did not run smoke` |
| M4 | 给 `todo-merge-audit` 加 `if: always()` | `FAIL todo-merge-audit gained or lost a condition` |
| M5 | 分类器对未知路径 `exit 1` | `FAIL workflow-affected exited 1 for [no-such-directory/x]` |
| M6 | 删掉 `TaskFlowDocs/*/*` 的显式归类 | `FAIL smoke for TaskFlowDocs/2026-01-01-example/plan.md: expected false, got 'true'` |
| M7 | 把 `release` 的 `if` 改成读 `smoke` 的 key | `release has the wrong condition: [needs.changes.outputs.smoke == 'true']` |

M1、M2 第一版**没有变红**，是这次实现里最值得记下的一件事：`assert_affected` 只比较值，而集合遗漏会退化成 unknown，unknown 对三个 key 全答 `true`——只删掉 `README.md` 的 release 归属，`assert_affected release true README.md` 仍然绿。补了 `assert_known`（读 stderr）之后才真正被抓住。断言写在「值」上而不写在「它被归类了没有」上，等于给兜底逻辑让路。

**未覆盖**：`hooks/task-id` 接受/拒绝的断言本身没有独立变异——改动 `task-id` 会让 smoke 在 `archive happy path`（`:679`）就先红，早于 `:1794` 那段，所以测不到。用真实目录当样本的旧写法**不是**靠这条断言守住的（顺序上永远走不到），这也印证了它本来就抓不到东西：在 `/tmp/proof` 里放一个 `TaskFlowDocs/Bogus/`，旧循环报 `FAIL the rule rejects this repository's own active task: Bogus`，新循环正常通过。

## Follow-ups

- **`changes` job 自身占一次 runner。** ubuntu 上几秒，换三次 macOS 不排队。若将来它变慢，正确做法是换 `dorny/paths-filter`，路径集合表可以直接搬过去。
- **跳过的 job 在 Checks 里显示 `skipped`，不是绿色。** 仓库没有 required checks，所以这不阻塞；若将来启用分支保护，需要把 `skipped` 当作通过处理，否则每个纯文档 PR 都会卡住。这一条不写进 workflow，因为它取决于将来是否启用分支保护。
