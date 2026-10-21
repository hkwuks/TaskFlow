# 让 Hooks workflow 只跑改动真正能影响的 job

> Task version: v1
> Status: checking

## Goal

`Hooks` workflow 今天对每一个 pull request 跑全部六个 job，而其中多数 job 读的路径与这次改动毫无关系。给每个 job 划出**它真正读取的路径集合**，不在集合里的改动跳过它；不在任何已知集合里的路径走安全默认（跑全部）。同时加 `concurrency` 让新 push 取消被它取代的旧排队。

价值是可测的：2026-10-20 的 PR #90 只把一个任务目录移进 `achieved/` 并改了一条 Todo 条目，却排了六个 job——macOS 那项**排队 11 分钟、实际跑 42 秒**，而它前面同一分支的三次 push 每次都再排一个。

## Background / Confirmed Facts

以下全部来自本仓库当前树（`main` = `ba07c89`）的实测 grep，不是推测：

- **`hooks/release-check` 的输入是 9 个固定文件**（`hooks/release-check:20-31`）：`.claude-plugin/plugin.json`、`.codex-plugin/plugin.json`、`.codebuddy-plugin/plugin.json`、`package.json`、`.claude-plugin/marketplace.json`、`.codebuddy-plugin/marketplace.json`、`CHANGELOG.md`、`README.md`、`README.zh-CN.md`。它不调用任何 hook，也不读 `hooks/`。
- **`hooks/smoke-test` 读真实仓库树**的部分只有这些（`grep -oE '(\$repo|\$HERE/\.\.)/[^"]*'`）：`hooks/README.md`、`skills/taskflow/references/runtime.md`、`CODE_STYLE.md`、`CONTRIBUTING.md`、`RELEASE.md`、`TaskFlowDocs/todo.md`、`hooks/capability-gate`、`skills/taskflow/`。其余全部是 `mktemp` 夹具。
- **`TaskFlowDocs/todo.md` 在 smoke 的输入里**，因为 `smoke-test:1939-1961` 把它的 `## Item template` 字段集与 `hooks/task` 实际写入的字段集逐项对账。所以「改 todo.md 不用跑 smoke」是错的。
- **但 `TaskFlowDocs/<task>/` 下的文件不在任何 job 的输入里**：smoke 只读 `todo.md`，`release-check` 不读 `TaskFlowDocs`，`evals` 只读自己的 `fixtures/`。PR #90 正是这一类。
  - **这条在实现期间被推翻过一次，记录在这里因为它就是本任务的教训。** `hooks/smoke-test:1791` 原来写的是 `for d in TaskFlowDocs/*/`——遍历**真实**活动任务目录名，喂给 `task-id` 当样本。CI 的 cwd 是仓库根，所以新建或删除一个任务目录**确实**是 smoke 的输入，第 19 行原本是假话。该循环已改为字面样本（理由见 Plan 的 Change Log），第 19 行现在才成立。
  - 由此还顺带纠正第 10 行的价值陈述：PR #90 那次改动里 `TaskFlowDocs/todo.md` 也变了（归档要回写 `- Status:` / `- Task:`），而 `todo.md` 本来就是 smoke 的输入。所以**即使本次任务全部落地，PR #90 那一类仍然会跑 smoke**。真实收益是 `release` 与 `evals` 各省一个 ubuntu job、纯任务文档的 PR 连 smoke 也省掉，以及 `concurrency` 取消被取代的排队。
- **`evals/runner.py` 只读 `evals/`**：case 在 `evals/cases/taskflow.json`，artifact 期望读 `evals/fixtures/`（`runner.py:52-56`，`root = case_path.parent.parent`）。`cases/taskflow.json:45-48` 里的 `TaskFlowDocs/...` 是夹具内的相对路径，不是真实树。
- **`hooks/smoke-test-windows.ps1` 只读 `$here` 与 `CLAUDE_PLUGIN_ROOT`**（`smoke-test-windows.ps1:4`、`:30`），不读 `$repo/CONTRIBUTING.md`——它在夹具里自己写一份（`:95`）。
- **仓库没有分支保护、也没有 ruleset**（`gh api …/branches/main/protection` → `Branch not protected`；`…/rulesets` → `[]`），所以 CI 不是合并的硬门槛，跳过一个 job 不会让任何人失去合并能力；反过来也意味着**漏跑没有任何外部提示**，安全默认只能靠自己写对。
- `tools/`、`dsh/`、`assets/`、`LICENSE`、`.github/` 不在任何 job 的输入里；其中 `.github/` 决定 workflow 自己，属于必须跑的路径。

## Requirements

1. 新增一个 `changes` job，用 `git diff --name-only` 算出改动路径，按路径集合分出每个 job 该不该跑。
2. `smoke`（三平台矩阵）、`release`、`evals`、`todo-merge-audit` 各自按自己的集合判断；`todo-merge-audit` 永远跑。
3. **未知路径跑全部**：任何不在任何集合里的改动，让全部 job 都跑。这是漏了一个路径时的唯一兜底。
4. 加 `concurrency`：`${{ github.workflow }}-${{ github.ref }}` + `cancel-in-progress: true`。
5. 路径集合必须与代码的真实读取一致，且**可被检查**：加一条 smoke 断言，把集合里列的路径与 `hooks/release-check`、`hooks/smoke-test` 实际 grep 出的路径对账，防止以后单方面漂移。
6. `.github/workflows/**` 与 `.github/workflows/hooks.yml` 自身变动，以及 `push` 到 main 的事件，都走安全默认。

## Acceptance Criteria

- 在夹具仓库上用 `act` 无法验证时，用等价的方式验证分诊函数本身：给定一份路径清单，断言输出每个 job 的 `true/false`。这是本任务的**核心可测单元**，不依赖 GitHub runner。
- 一个只改 `TaskFlowDocs/2026-01-01-example/plan.md` 的改动 → `smoke`、`release`、`evals` 全 `false`，`todo-merge-audit` `true`。
- 一个只改 `TaskFlowDocs/todo.md` 的改动 → `smoke` `true`（template 对账），`release` `false`。
- 一个只改 `README.md` 的改动 → `release` `true`，`smoke` `false`。
- 一个改 `hooks/task` 的改动 → `smoke`、`release` 都 `true`（release 读 manifest，但 hooks 改动不影响它——**这一条要按实际集合判**：`hooks/task` 只让 `smoke` 为 `true`）。
- 一个改 `unknown/new-dir/x.txt` 的改动 → 全部 `true`。
- 一个 `push` 事件 → 全部 `true`（main 上的合并必须全验）。
- `bash hooks/smoke-test` 全绿；新增断言在对应变异下变红。
- `.github/workflows/hooks.yml` 通过 `actionlint`（若本机没有，至少 `python3 -c 'import yaml,sys; yaml.safe_load(open(sys.argv[1]))'`）。

## In Scope

- `.github/workflows/hooks.yml`：`changes` job、各 job 的 `needs` + `if`、`concurrency`。
- `hooks/smoke-test`：路径集合与真实读取的对账断言。

## Out of Scope

- 改任何 hook 的行为。
- 加 `dorny/paths-filter` 或任何第三方 action（用户的选项里明确没选它）。
- 分支保护 / required checks。仓库今天没有，本任务不引入。
- 减少 job 数量或并行度调整。六个 job 的总时长不是问题，排队才是。

## Risks / Deferred Items

- **漏配一个路径 = 静默不跑。** 这是本任务唯一的严重失败模式，因为仓库没有 required checks，漏跑不会有任何外部提示。三条缓解叠加：(a) 未知路径跑全部；(b) smoke 把集合与 `release-check`/`smoke-test` 的真实读取路径对账；(c) 集合写在 workflow 里、离它的使用者最近。
- **`git diff --name-only` 在 `pull_request` 上的三点比较需要显式基。** `actions/checkout@v4` 默认 shallow 且单分支，`git diff origin/main...HEAD` 会因缺历史失败。用 `fetch-depth: 0` 或显式比较 `github.event.pull_request.base.sha` 与 `head.sha`。选后者：它不要求抓全历史，且与事件语义一致。
- **`cancel-in-progress: true` 会取消 main 上的排队 run。** 如果两次 push 落在 main 上相隔很近，后一次会取消前一次的排队——前一次的提交就永远没被验过。缓解：按 `github.ref` 分组，并把 `cancel-in-progress` 限定在 `pull_request` 事件上；main 上的 push 保留完整历史。这一条是设计决定，不是实现细节。
- **`changes` job 自己也是一次 runner 占用。** ubuntu 上几秒，换来三次 macOS job 不排队，净收益为正；但它是新增的一跳延迟。若将来它变慢，正确做法是改用 `dorny/paths-filter`，本任务的集合表可以直接复用。

## Open Questions

无。三项设计选择已由用户于 2026-10-20 决定：按 job 分诊、未知路径默认跑全部、一并加 concurrency。
