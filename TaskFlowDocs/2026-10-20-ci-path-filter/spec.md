# Spec — job 级路径分诊

> Task version: v1

## Objective and Success Criteria

在 `Hooks` workflow 里加入一个 `changes` job，它把这次改动涉及的路径分成三组（`smoke`、`release`、`evals`），输出每个下游 job 该不该跑；下游 job 用 `needs.changes.outputs.<key> == 'true'` 决定。安全默认是：**任何不在已知集合里的路径，让全部 job 都跑**。

成功标准见 PRD 的 Acceptance Criteria。核心一条：分诊规则能被单独测，不需要 GitHub runner。

## Architecture Boundaries and Responsibilities

| 组件 | 职责 | 不做什么 |
| --- | --- | --- |
| `tools/workflow-affected` | 读改动路径清单，输出三个 key 的 `true`/`false` | 不读仓库内容（只拿到路径字符串）、不跑检查、不碰 YAML |
| `changes` job | 取 diff、调上面的工具、写 `$GITHUB_OUTPUT` | 不含任何路径规则 |
| `smoke` / `release` / `evals` | 内容一行不改，只加 `needs` + `if` | 不自己判断 |
| `todo-merge-audit` | 永远跑，不加 `if` | — |
| `hooks/smoke-test` | 新增一段：把 `tools/workflow-affected` 里的路径集合与 `release-check`/`smoke-test` 真实读取的路径对账，并断言分诊结果 | 不解析 YAML、不跑 workflow |

## Project Structure / Affected Files

```text
tools/workflow-affected       新增：分诊规则（可执行、可单测）
.github/workflows/hooks.yml   新增 changes job、concurrency、四个 if
hooks/smoke-test              新增一段：真正的输入对账 + 分诊结果断言
```

## Interfaces, Data Flow, and Contracts

### `tools/workflow-affected`

```text
usage: workflow-affected [<changed-path>...]
```

- 参数是改动路径，一次一个，从命令行读。**不读 stdin**：workflow 里 `git diff --name-only` 的输出直接进来，命令行参数让手工测试与调用点完全同形。
- stdout 固定三行，顺序固定，值只有 `true` / `false`：

```text
smoke=true
release=false
evals=true
```

- 退出码恒为 `0`。这个工具的唯一职责是分类；把「输入可疑」变成非零退出会让 workflow 的 `changes` job 失败，从而让下游全部 `skipped`——那是最坏的失败方式。可疑输入走安全默认（全部 `true`）并在 stderr 说一句。
- **零参数**：输出全部 `true`，stderr 一行 `no changed paths; running everything`。

### 为什么退出码恒为 0（这条不是懒，是契约）

`on.push` 与 `on.pull_request` 的区间计算分别有自己的失败模式，而 `changes` job 一旦失败，下游 `needs` 的 job 全部不跑且**不会显示为红色**——GitHub 里它们只是 `skipped`。也就是说一个让 `changes` 崩溃的输入会静默关闭整个 CI。所以分类器只在**内部**做安全降级，把「我不确定」翻译成「全跑」。

### 路径集合

规则写在工具里，前置注释说明每条的依据。依据已实测（PRD Background）：

```sh
smoke:   hooks/**  skills/**  TaskFlowDocs/todo.md
         CODE_STYLE.md  CONTRIBUTING.md  RELEASE.md  .github/workflows/**
release: .claude-plugin/**  .codex-plugin/**  .codebuddy-plugin/**
         package.json  CHANGELOG.md  README.md  README.zh-CN.md
evals:   evals/**  skills/**
```

三条依据值得在注释里各留一句：

- `TaskFlowDocs/todo.md` 进 `smoke`：`smoke-test:1939-1961` 把它的 `## Item template` 字段集与 `hooks/task` 实际写入的字段集对账。
- `.github/workflows/**` 进 `smoke`：改了 workflow 就必须重跑一次，否则分诊的改动本身没有验证。
- manifest 进 `release` 但**不进** `smoke`：`smoke-test` 的 release 段在夹具里自己生成 manifest（`smoke-test:3526-3650`），不读真实树的那几个文件。

**未知路径**（不匹配任何集合）→ 三个全部 `true`。实现为一个 `unknown` 标志，最后统一覆盖。

### `changes` job 的取路径

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0          # 三点比较与 HEAD~1 都需要历史
- id: diff
  run: |
    case "${{ github.event_name }}" in
      pull_request)
        git diff --name-only \
          '${{ github.event.pull_request.base.sha }}' \
          '${{ github.event.pull_request.head.sha }}'
        ;;
      *)
        git diff --name-only HEAD~1 HEAD || git ls-files
        ;;
    esac > "$RUNNER_TEMP/changed"
- run: |
    mapfile -t paths < "$RUNNER_TEMP/changed"   # ← 不用 mapfile，见下
```

**bash 3.2 没有 `mapfile`。** runner 上默认是 bash 5，但本仓库的 hook 底线是 3.2，而这个工具要能在开发者的 macOS 上跑。用 `while IFS= read -r p; do args+=("$p"); done < file` 代替；3.2 支持数组。

### `push` 事件

推送到 main 一律跑全部：main 是唯一发布源，且 `push` 的路径集合无法表达「这次合并带进了什么」。用一个显式分支，不是靠默认。

### `concurrency`

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

只在 pull_request 上取消。main 上连续两次 push 相隔很近时，取消前一次等于那个提交永远没被验过，而仓库没有 required check 兜底。

## Invariants and Compatibility

- `tools/workflow-affected` 退出码恒 `0`。
- 三个 key 的**名字与顺序**固定：`smoke`、`release`、`evals`。smoke 断言按名字取值，不按行号。
- 六个 job 的内容一行不改。
- `todo-merge-audit` 永远跑。
- 路径集合只有一份，位于 `tools/workflow-affected`。workflow 不含任何 glob。

## Validation and Error Semantics

| 情形 | stdout | stderr | 退出码 |
| --- | --- | --- | --- |
| 空参数 | 三个 `true` | `no changed paths; running everything` | 0 |
| 全部已知、有匹配 | 按集合 | — | 0 |
| 存在未知路径 | 三个 `true` | 列出那个路径 | 0 |

## Code and Test Constraints

- bash 3.2 底线：无 `mapfile`、无 `declare -A`、无进程替换。`bash -n` 与 `docker run bash:3.2 bash -n` 双通过。
- `hooks/smoke-test` 的断言只读文本（`sed`/`grep`），不引入 YAML 解析器。
- 新增断言各有一条只让它变红的变异。

## Design Decisions and Alternatives

**分诊逻辑搬出 YAML，放进 `tools/workflow-affected`。** 备选是内联在 workflow 里。否决理由：内联意味着同一套 glob 要在两处维护（workflow 一份、smoke 断言一份），而这正是本任务要消除的漂移；搬出来之后 smoke 测的就是 workflow 实际调用的那一份。

**`tools/` 而不是 `hooks/`。** `hooks/` 是随插件发布的运行时，`tools/` 是仓库自己的开发工具（先例：`tools/fixture-compare`，README 与 CHANGELOG 都已把它与 hooks 分开描述）。分诊器只在 CI 与开发机上跑，不属于插件。

**不引入 `dorny/paths-filter`。** 用户明确没选它；`fetch-depth: 0` 在这个仓库的代价是几十 MB 历史，可接受。

## Open Questions

无。
