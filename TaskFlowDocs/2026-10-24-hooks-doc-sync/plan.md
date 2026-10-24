# Plan — 让 hooks 文档与 hooks 目录保持同步

> Task version: v1
> Status: checking

No spec required — 小且自洽的任务。三个文件，没有跨层契约：改动是两处文档和两条针对已存在文件的断言。

## Reference Pointers

- `skills/taskflow/references/runtime.md`——本任务要改的表格所在；§Single-command transitions 与 §Folder layout。
- `hooks/README.md`——本任务要改的树形块所在；§Why this shape 说明这棵树是干什么的。
- `RELEASE.md`——`release-version` 与 `repository-check` 的权威描述所在。读它是为了确认 `runtime.md` 新加的行该说什么，而不是把流程抄一遍。
- `hooks/smoke-test` §`the packaged Skill ships ...`——本任务扩展的既有断言家族，包括钉条款时用的 `grep -q -F` 写法。
- `CONTRIBUTING.md`——分支前缀（`chore/`）、提交格式，以及 PR 要遵守的落地规则。

## Related Tasks

- `TaskFlowDocs/achieved/2026-10-23-archive-completion-gate/`——相邻但非依赖。那个任务修的是同一类沉默（散文里宣称的规则没有任何东西在检查）；本任务只扩展它碰过的那个断言家族。
- 吸收 `TF-20261008-4d37b2`（2026-10-10 移除），它的后半——版本跃迁断言——就是本 Plan 的 Step 2。

## Skills / Tools Used

- [PRD] Unaided — 本阶段没有调用能力；considered: documentation and decision。需求来自本仓库自己的文档和一次实测的漂移计数，不来自外部方法论。
- [Plan] Unaided — 本阶段没有调用能力；considered: work breakdown。三个文件、两条断言，再拆就是仪式。

## Preconditions

- [x] 已检查适用的仓库文档与个人规则，并记录冲突情况——读了 `CONTRIBUTING.md`、`CODE_STYLE.md`、`README.md`、`RELEASE.md`；与本改动无冲突。无个人规则适用于本任务。
- [x] 远程/fork/PR 相关：已记录 remote、目标仓库、base 分支、本地分支与 base 的关系、数据新鲜度、必需检查——只有一个 remote，`origin` = `https://github.com/hkwuks/TaskFlow.git`（可读可推）。无 fork；本仓库自己的 PR 都以 `origin` 为源和目标。目标仓库 `hkwuks/TaskFlow`，base `main`，本地分支 `chore/hooks-doc-sync` 从 `5d2ac57` 的 `main` 开出，且 `main` 是其祖先。新鲜度：远程跟踪数据读于 2026-10-24，`origin/main` = `5d2ac57`。必需检查：`Hooks` 工作流（`.github/workflows/hooks.yml`），也是仓库唯一的工作流。
- [x] PR 创建/更新相关：已记录模板路径、每个必填字段的映射、模板核对——`.github/pull_request_template.md`。映射：Summary → 改动及其目标；TaskFlow traceability → 任务路径、在范围内的文件、base `main`、目标 `hkwuks/TaskFlow`；Verification → `Hooks` 运行链接、`git diff --check`、插件/Skill 校验，以及本 Plan 记录的结果；Review boundaries → 四项都逐条核对并给出理由。模板没有标记任何字段为可选，`CONTRIBUTING` 也把未勾选框视为未完成，所以全部必填。已在开 PR 前读取该路径的模板完成核对。
- [x] 缺失的治理草稿与显式批准已在生效前记录——没有缺失项。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-24 17:51 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 先让两份文档与目录一致

- Goal: 在加任何会把它钉死的东西之前，先关掉 `hooks/README.md` 与 `runtime.md` 里实测到的漂移。
- Dependencies: 无。
- Files: `hooks/README.md`、`skills/taskflow/references/runtime.md`。
- Implementation checklist:
  - [x] 在 README 树里 `todo-check` 旁补上 `repository-check`，一行描述与相邻条目保持同样的形态。
  - [x] 在 README 里写明这棵树覆盖什么、不覆盖什么，把断言的适用范围写在读树的人会看到的地方。
  - [x] 在 `runtime.md` 里补上 `release-version` 与 `repository-check`：不作为生命周期行——它们不是生命周期命令——而是一小段点名它们并指向 `RELEASE.md`，流程的权威描述在那里。
  - [x] 保持 `runtime.md` §Folder layout 中关于 `hooks/` 的那行与树一致。
- Acceptance: `ls hooks/` 的每个文件都在 README 树里被点名，两个发布命令都在 `runtime.md` 里出现。
- Verification: `ls hooks/ | sort` 与解析出的树比对；`grep -c 'release-version\|repository-check' skills/taskflow/references/runtime.md` 非零。
- Rollback: `git checkout -- hooks/README.md skills/taskflow/references/runtime.md`。
- Status: done

### Step 2 — 把两条事实写进 smoke 套件

- Goal: 让漂移失败，双向都失败，再加上本条目吸收的版本跃迁缺口。
- Dependencies: Step 1——断言是针对已经正确的文档写的，所以它从 `ok` 起步，而不是从一个白名单起步。
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 增加 `== the two documents that inventory hooks/ name every file in it ==`：解析 ` ```text ` 树形块，剥掉框线前缀，与 `ls hooks/` 双向比对。两条文档合并进同一节、同一个 `doc_tree` 辅助函数——README 的树是整份文件，`runtime.md` 的树要按 `hooks/` 子树解析（`doc_tree <file> hooks` 以目录行开、以下一个同级目录行止）。
  - [x] **偏离**：原计划是「每个真实 hook 必须在 `runtime.md` 里出现；`runtime.md` 里每个 `hooks/<名字>` 必须对应真实文件」。改成直接比对 `runtime.md` §Folder layout 的 `hooks/` 子树与 `ls hooks/`——效果更强（同一份清单双向），且 `hooks/README.md` 也不必进 `runtime.md`。理由记在这里，因为这是对已批准 checklist 的措辞改动而非契约改动。
  - [x] 增加 `== an achieved Task version has its old/ directory for every version below it ==`：对每个 achieved 任务，读根 `plan.md` 的 `> Task version: vN`（兼容旧的 `- Task version: vN`），要求 `1..N-1` 每一版都有 `old/vM`；失败时点名任务和缺失目录。
  - [x] 断言针对的是形状时用夹具，而不是真实仓库——版本缺口这一条需要一个真有缺口的任务，而现存树里没有。夹具三个任务：有缺口（v3 只有 old/v1）、健全（v3 有 v1+v2）、旧形态（`- Task version: v2` 有 v1）。夹具自检断言「只应有 2026-01-01-gap old/v2」，多一个少一个都红。
  - [x] 失败消息必须点名文档或任务，让失败无需手工复跑就能定位。
- Acceptance: 三个小节在真实仓库上打印 `ok`；各自的事实被破坏时失败（一次一个做变异验证）。
- Verification: `bash hooks/smoke-test`；然后三次变异——删掉树里一行、新增一个 `hooks/` 文件、从夹具里移除一个 `old/vN`——每次都要产生点名缺失物的失败，每次在下一个之前还原。
- Rollback: `git checkout -- hooks/smoke-test`。
- Status: done

### Step 3 — Changelog、全量验证、PR 记录

- Goal: 把改动记到发布要读的地方，跑全量验证，并把任务推进到 `checking`。
- Dependencies: Steps 1–2。
- Files: `CHANGELOG.md`、`TaskFlowDocs/2026-10-24-hooks-doc-sync/plan.md`。
- Implementation checklist:
  - [x] 在 `Unreleased` 下加记录：两条 `Added`（文档核对断言、版本缺口断言）+ 一条 `Fixed`（两份文档补上两个发布命令）。
  - [x] 跑 `bash hooks/smoke-test`、`bash hooks/release-check .`、`bash hooks/repository-check .`，结果记在 `## Verification / Review`。
  - [x] 把文档与目录的核对写成 `## Verification / Review` 里的一条可执行命令，而不是一句断言。
  - [x] 按 `CODE_STYLE.md` 复查新增的 shell（`set -euo pipefail` 由整份脚本持有、变量全部加引号、只读、不打印凭据）。
- Acceptance: 三条命令全部通过；changelog 点名了改动；Plan 的验证小节带有每条命令与其结果。
- Verification: 上面三条命令。
- Rollback: 还原 changelog 那一条；断言本身独立成立。
- Status: done

## Checkpoints

- Step 1 之后：文档先变正确，再让东西去断言它正确。反过来会把今天的漂移钉死。
- Step 2 之后：每条新断言做一次变异测试，之间还原。从没见它失败过的断言，不能算知道它在跑。

## Verification / Review

- 2026-10-24 Step 3: bash hooks/smoke-test -> ALL SMOKE PASSED; release-check -> STATUS: pass; repository-check -> needs-user-input（未提交的任务目录，提交后消失）; git diff --check -> 0

- 2026-10-24 Step 2: bash hooks/smoke-test -> ALL SMOKE PASSED；6 次变异逐个还原验证，每次失败都点名缺失物（见下表）

- 2026-10-24 Step 1: ls hooks/ (29) vs README tree (29) 与 runtime.md hooks 子树 (29)：双向 diff 为空；文档提到的每个 hooks/<名字> 都落地，没有文件未被提及

全部于 2026-10-24 在本 worktree（`.worktrees/hooks-doc-sync`，分支 `chore/hooks-doc-sync`）执行。

### 命令与结果

| 命令 | 结果 |
| --- | --- |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED`，exit `0`；新增两节均打印 `ok` |
| `bash hooks/release-check .` | `STATUS: pass`（v1.1.7 字面量与 marketplace pin 一致） |
| `bash hooks/repository-check .` | `STATUS: needs-user-input` — 报告的是本任务目录尚未提交、以及分支没有 upstream。这两条在提交并推送后自然消失，不是本改动的缺陷；`Orphan task directories: none`、`Stale task worktrees: none` |
| `bash -n hooks/smoke-test` | 解析通过 |
| `git diff --check` | 无输出，exit `0` |

### CI（推送后）

`Hooks` 工作流，run [`40095811263`](https://github.com/hkwuks/TaskFlow/actions/runs/40095811263)，提交 `51702d8`，八个检查全部 pass：

| 检查 | 结果 | 用时 |
| --- | --- | --- |
| `changes` | pass | 4s |
| `evals` | pass | 7s |
| `release` | pass | 6s |
| `smoke (macos-latest)` | pass | 46s |
| `smoke (ubuntu-latest)` | pass | 18s |
| `smoke (windows-latest)` | pass | 35s |
| `todo-merge-audit` | pass | 3s |

三个平台都跑了完整的 smoke 套件，包括本次新增的两节；macOS 与 Windows 各自 46s/35s，说明新断言在其中也真的执行了，而不只是在 ubuntu 上通过。`repository-check` 在上一张表里报的 `needs-user-input` 在推送后按预期消失——CI 是在一个干净的检出上评分的。

### 文档与目录核对（可执行，替代一句「已同步」）

```bash
awk '/^```text/{f=1;next} /^```$/{f=0} f' hooks/README.md | sed -n 's/^[│├└─ ]*[├└]── \([^ ]*\).*/\1/p' | sort -u > /tmp/doc.txt
awk '/^```text/{f=1;next} /^```$/{f=0} f && /hooks\/$/{h=1;next} h' skills/taskflow/references/runtime.md \
  | sed -n 's/^[│├└─ ]*[├└]── \([^ ]*\).*/\1/p' | sort -u > /tmp/doc2.txt
ls -1 hooks/ | sort -u > /tmp/real.txt
comm -3 /tmp/doc.txt /tmp/real.txt; comm -3 /tmp/doc2.txt /tmp/real.txt
```

两条 `comm -3` 都无输出即一致；实测 `doc=29 real=29 doc2=29`。

### 变异验证（一次一个，每次还原后才做下一个）

| # | 改坏什么 | 断言给出的失败 |
| --- | --- | --- |
| M1 | 从 README 树删掉 `repository-check` 行 | `FAIL hooks/README.md does not name: repository-check` |
| M2 | 把树里 `repository-check` 改名成 `repository-checker` | `FAIL hooks/README.md does not name: repository-check` |
| M3 | 复制一个 `hooks/nonesuch-hook` 文件，不写进文档 | `FAIL hooks/README.md does not name: nonesuch-hook` |
| M4 | 从 `runtime.md` 树删掉 `release-version` 行 | `FAIL skills/taskflow/references/runtime.md does not name: release-version` |
| M5 | 把真实任务 `2026-09-08-runtime-hooks` 的 `old/v1` 移走 | `FAIL achieved task versions have gaps: 2026-09-08-runtime-hooks old/v1` |
| M6 | 篡改夹具自检的期望值 | `FAIL version-gap fixture: expected only 2026-01-01-gap old/v2, got [...]` |

M6 的意义：证明夹具本身带缺口，所以 M5 那条不是对空集合做检查。

### 过程中发现并修掉的两个问题

1. **新断言把 CI 分类器断言弄红了。** `hooks/smoke-test` 会把自身源码里出现的 `$repo/...` 路径抽出来，逐个断言 `tools/workflow-affected` 认得；我最初写的是 `hooks_dir="$repo/hooks"`，于是裸的 `hooks` 作为一条「路径」进入比对，而它对不上任何真实文件，分类器报 unknown。改用 `$HERE`（同一目录），并在注释里写明原因——否则下一个写这段的人会再犯一次。
2. **`doc_tree` 的子树模式一开始把 `runtime.md` 整个仓库布局都算进去了。** 需要的是 `hooks/` 之后、下一个同级目录之前的那一段；已改为该范围，解析数为 29，与 `ls hooks/` 相等。

## Change Log

- 2026-10-24 — 写下 Plan。记录了实测到的漂移（README 树缺 `repository-check`；`runtime.md` 两个发布命令都没提），好让 Step 1 有一个可关闭的「之前」状态；并把断言范围收在名字上，不含散文。
- 2026-10-24 — 用户批准后按主要语言中文改写 PRD 与 Plan 的散文；`approve` 首次被拒，原因是 Stage 行写的是 `document/deployment decision` 而记录里是 `documentation and decision`，已改回记录值。
- 2026-10-24 — Step 2 实施时把两个断言节合并为「两份文档 + 一个 `doc_tree` 辅助函数」，并把 `runtime.md` 那半从「按名字扫全文」改成「按子树双向比对」。这是对已批准 checklist 的措辞偏离，不是契约偏离：PRD 的 Requirements 2、4 与对应的 Acceptance 仍然逐条满足，且效果更强。
- 2026-10-24 — 修掉新断言与 CI 分类器断言的两处冲突（裸 `hooks` 路径、子树解析范围），见上节。

## Follow-ups

- `TF-20261008-a4454d` 就是本任务，归档时关闭。
- 两份文档的散文级检查没有做；若名字对而描述漂了，那仍然是评审问题。

## Version History

- v1 — planning。
