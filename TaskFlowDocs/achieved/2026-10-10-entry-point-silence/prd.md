# 入口不静默：让「该走 TaskFlow 的工作」在会话开始时被说出来

> Task version: v1
> Status: completed

## Goal

让会话一开始就能看见「这份工作该不该进 TaskFlow」，从而修掉两个 1.1.3 上的入口缺陷：

1. **新任务发起不自动走 TaskFlow**——目标仓库从未用过 TaskFlow 时，SessionStart 完全不输出，插件在会话里等于不存在。
2. **接手一份从未进过 TaskFlow 的工作不会触发登记**——接手读起来是「延续」而非「请求」，于是没有任何东西问过「这份工作该不该登记」。

修法落在**一层**：`hooks/summarize-state`。它已经算出了这份工作有没有任务、有没有 Todo，却没有把「以上都没有」这件事说出来。

## Background / Confirmed Facts

### B1·两个缺陷都已在本仓库 1.1.3 上查证

`v1.1.3..origin/main` 共 23 个提交，无一触及这两处。记录见 `TaskFlowDocs/todo.md` 的 `TF-20261009-cc463b`（第四个失败模式）与 `TF-20261010-82ec77`（本条来源）。

### B2·静默的确切位置

```bash
docs="$repo_root/TaskFlowDocs"
[ -d "$docs" ] || exit 0          # <- 无 TaskFlowDocs 时，整条链在此处归零
```

`hooks/session-start:184` 是 `[ -z "$state_summary" ] && exit 0`，所以 `summarize-state` 空输出 = 插件在会话里零存在感。

实测（本机，临时 git 仓库，无 TaskFlowDocs）：

```
$ bash hooks/summarize-state | od -c
0000000
```

`session-start` 仍会输出一段，但内容全是 `repository-docs` 路由（`TaskFlowDocs/repository-docs/index.md` 相对该仓库而言是**不存在的路径**），没有一句说明 TaskFlow 是什么、什么时候适用。

### B3·第二个缺陷的三条规则互相咬死

- `SKILL.md:10`：适用闸门只在「请求要求**修改仓库或产出开发产物**」时生效，而「接着做 / 接手某个分支」读起来是**延续**，不构成请求。
- `SKILL.md:75`：反向明写「A new session, new Agent, or a changed implementation detail is **never by itself** a new-task trigger」——本条本意是防误建任务，但同时给「继续未登记的工作」发了许可。
- `hooks/summarize-state` 打印的只有**已存在**的 inbox 条目与活跃任务，一份从未进过 TaskFlow 的工作在其中是空的。

### B4·`UserPromptSubmit` 这条路是关闭的

`achieved/2026-09-10-audit-hook-opportunities/reference/hook-audit.md:81` 已否决：「Todo creation from every UserPromptSubmit：多数 prompt 是提问或跟进，matcher 无法可靠分类，除非再加一个模型」。`references/runtime.md:185` 亦明写写入命令永不绑 `UserPromptSubmit`/`PostToolUse`/`Stop`。

所以修复**不能**是加一个 prompt 钩子，只能是让**已经算出来的静默**变得可观测。

### B5·分支与任务目录共享一个 slug

`CONTRIBUTING.md` 的分支命名是 `<type>/<slug>`，任务目录是 `TaskFlowDocs/<date>-<slug>`。所以「这条分支属不属于某个任务」可以由此判定：取分支名的最后一段，看有没有任务目录以它结尾。这也是本轮实际形态——分支 `fix/entry-point-silence`、任务目录 `2026-10-10-entry-point-silence`。

### B6·可用的既有机制

- `hooks/repository-check` 已会报 orphan 任务目录与未提交的任务产物，但它是**opt-in、不进自动钩子**（CHANGELOG 已记）。
- `hooks/summarize-state` 已经是 SessionStart 的唯一状态产物，且会话一开始就在读 `TaskFlowDocs`。
- 无解释器不变量：`summarize-state` 只用 POSIX sh + awk，`smoke-test:52-76` 在只有 `awk`/`git` 等被 link 进 `toolbin` 的 PATH 上钉住它。

## Requirements

### R1 — 无 TaskFlowDocs 时说出义务，而不是沉默

`hooks/summarize-state` 在 `TaskFlowDocs/` 不存在时不再 `exit 0` 静默，改为输出一段入口提示：说明「修改本仓库的请求要进 TaskFlow、首条记录是 `TaskFlowDocs/todo.md`」，并说明只读类工作（解释、翻译、状态、调研、复核、诊断）不进。措辞与 `SKILL.md:10` 一致。

只此一段，且 `exit 0`——它是提示，不是建目录，更不是自动 intake。

### R2 — 分支不属任何任务时说出来

`summarize-state` 在判定「当前分支不对应任何任务目录」时输出一行报告，指出接手未登记工作这条路径。判定用 B5 的 slug 规则：分支名的最后一段若被某个任务目录名（`TaskFlowDocs/*/` 与 `TaskFlowDocs/achieved/*/`）以结尾包含，即视为已登记。

### R3 — 报告不得误报日常形态

以下形态必须保持不输出该行（否则每次会话都是噪声）：

- 工作树里正在做某个任务（分支 slug 与任务目录匹配）；
- 基分支（`main` / `master`）；
- 分离 HEAD；
- 当前目录不是一个 Git 仓库（fixture 与一次性目录）；
- 工作已经被归档（`achieved/` 下同名任务存在）。

### R4 — 仍然没有解释器依赖

新增代码只用已在内核里的 `git`、`awk`/`case` 与 POSIX sh 内建。`hooks/smoke-test` 的「no interpreter」一节继续在精简 PATH 上跑通。

### R5 — 既有断言按新行为改写，并注明是行为变更

`hooks/smoke-test:48` 的「summarize-state with no TaskFlowDocs prints nothing」钉的正是 R1 要改掉的行为，按新行为改写，并在该节注明这是一次**有意**的行为变更及理由。R2 另加正反两个方向的断言。

### R6 — 不改 SKILL.md / README 的措辞

`SKILL.md:10` 与 `README.md:103` 已经正确陈述了规则；缺的是会话开头把规则送进上下文。本轮只改 hook 与其断言，不动规则文本。

## Acceptance Criteria

- **A1**：在没有 `TaskFlowDocs/` 的 Git 仓库里跑 `hooks/summarize-state`，输出非空且含 `TaskFlowDocs/todo.md` 与「修改本仓库的请求」一层含义；退出码 0；不创建任何文件或目录。
- **A2**：在有 `TaskFlowDocs/`、当前分支不属任何任务目录的仓库里跑，输出含该分支名与「未登记」一层含义的一行。
- **A3**：R3 列的形态逐一不输出该行（含：任务工作树内、`main` 上、非 Git 目录）。
- **A4**：`bash hooks/smoke-test` 全量通过；新增/改写的断言在**变异**下确实会红（临时把 R1 改回 `exit 0` 静默 → R1 断言失败；临时去掉 slug 匹配 → A2 断言失败）。
- **A5**：`hooks/smoke-test` 的 no-interpreter 一节在新代码下仍通过。
- **A6**：`bash hooks/release-check .`、`git diff --check`、`quick_validate.py skills/taskflow` 全部通过；CI 三 host 矩阵在推送后全绿。

## In Scope

- `hooks/summarize-state`：无 docs 的入口提示（R1）、分支未登记报告（R2）。
- `hooks/smoke-test`：`:48` 断言的改写、R2 的正反断言、R4 的复用确认。
- 本任务的核心文档。

## Out of Scope

- `SKILL.md`、`README.md`、`README.zh-CN.md` 的措辞（R6；规则已正确，`SKILL.md:10` 的收窄不在本轮）。
- 任何形式的 `UserPromptSubmit`/`Stop` 钩子（B4 已否决）。
- `hooks/repository-check` 的 orphan 检测（既有机制，opt-in，不动）。
- 自动创建 `TaskFlowDocs/` 或自动 intake。
- `TF-20261009-cc463b` 的其余三个失败模式（顺序、能力归属、能力类不可见）——本任务只关闭其中「入口静默」这一半。
- 发布：本任务落地后需另起一次发布才惠及已安装用户。

## Risks / Deferred Items

- **噪声**：入口提示对「临时看一眼别人的仓库」也会出现。缓解：只有一段、只两行、只在无 `TaskFlowDocs/` 时出现；一旦仓库建了 `TaskFlowDocs/` 就永久消失。
- **基分支判定靠字面名**：只按 `main`/`master` 排除，未解析远程默认分支。默认分支叫别的名字的仓库会多一行报告。记为已知上限，见 `plan.md` 的 ponytail 注。
- **slug 匹配是启发式**：分支 `fix/foo` 与任务 `2026-01-01-foo-extra` 也会匹配（以结尾包含为准）。判据取「少报而非误报优先」，因为多报会在每个会话里变成噪声。
- **Deferred**：`SKILL.md:10` 的适用闸门是否应收窄到把「延续/接手」写进触发面——属 `TF-20261009-cc463b`，本轮不动。
- **Deferred**：`repository-docs-context` 仍会输出指向本仓库不存在的 `TaskFlowDocs/repository-docs/index.md` 的引导（B2 末段）。属另一处入口措辞，未在本轮范围。

## Open Questions

无。三个设计决定已由用户裁定：修复只落在 hook 层；「未登记工作」用 git 分支信号；`smoke-test:48` 的断言按新行为改写。

## Version History

- v1 — 规划中，等待批准。
