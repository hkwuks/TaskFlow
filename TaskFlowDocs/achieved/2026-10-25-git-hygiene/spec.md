# Spec — 本地文件由插件排除，不要求用户改 .gitignore

> Task version: v1
> Status: planning

## Objective and Success Criteria

一个 hook 把 TaskFlow 的两个 clone 本地文件写进 `.git/info/exclude`，让它们在 `git status` 里消失，且不需要用户知道 `.gitignore` 存在。成功标准见 `prd.md` 的 A1–A8；本 Spec 只定义机械契约。

## Architecture Boundaries and Responsibilities

一个 hook、三样写入、零个被跟踪的编辑。

| 位置 | 职责 | 不改的部分 |
| --- | --- | --- |
| `hooks/install-git-hygiene` | 写 per-clone Git 配置：driver、`info/attributes`、`info/exclude` | 三样都只是「缺则补」，从不删、从不改用户的行 |
| `hooks/session-start` | 每个 SessionStart 调它一次，`|| true` | 调用顺序与 best-effort 语义不变 |
| `.git/info/exclude` | Git 的 per-clone 排除表；与 `.gitignore` 取并集 | 用户自己写的行不碰 |
| `.gitignore` | 只对克隆本仓库的人生效的那一半 | 与插件规则等价，取并集，不删 |

**为什么是 `info/exclude` 而不是 `.gitignore`。** 排除的作用域必须等于「这个 clone」，因为这两个文件本身就是 clone 本地的东西。`.gitignore` 是被跟踪的共享文件：写进去等于把所有 clone 的视图改掉，包括那些确实想提交它们的仓库——那正是本任务要避免的形状。`.git/info/exclude` 是 Git 为这个用途提供的位置，且 `hooks/install-merge-driver` 已经在隔壁用 `info/attributes` 做同一件事，理由逐字相同。

**为什么规则只对未跟踪文件生效。** `info/exclude` 是忽略表，不是删除命令。被 `git add -f` 过的副本仍然参与 `git status`、仍然会被提交。这不是本实现的缺陷，是 Git 的语义；A3 把它断言下来，因为「规则把真实漂移掩盖掉」才是危险的失败——一个克隆了 8 份旧 `sessions.md` 的仓库若因此看不见对它们的改动，比看见它们更糟。真正的清理是子任务。

**为什么退化路径是「文档写一句」而不是代码兜底。** 本仓库的立场是 hooks 可选（`hooks/README.md` 的末尾段、`SKILL.md` 的无 hook 段落都这么说）。hook 不跑就没人配置，这在设计上是允许的状态，所以正确回答是「告诉用户手动跑一次」，而不是把 Git 配置写入挂到每个热路径 hook 上。后者会把一个写入放进每轮 prompt 的执行路径，而它一年只需要成功一次。

## Project Structure / Affected Files

```text
hooks/install-merge-driver -> hooks/install-git-hygiene   # 改名 + 新增 exclude 写入
hooks/session-start                    # 调用点
hooks/smoke-test                       # 既有安装段改名 + 新断言
hooks/README.md                        # 目录树 + install-* 条目 + Scope 段
skills/taskflow/references/runtime.md  # 目录树 + wiring 段
skills/taskflow/SKILL.md               # personal.md / sessions.md 的 local-only 句
skills/taskflow/references/artifacts.md # 同上
README.md, README.zh-CN.md             # 目录树
.gitignore                             # 删掉 sessions.md 那一条
CHANGELOG.md                           # Changed（改名）+ Added（自动排除）
```

SSOT：**契约的唯一实现是 `hooks/install-git-hygiene`**；五份文档是对它的描述。

## Interfaces, Data Flow, and Contracts

### 契约 1 — `hooks/install-git-hygiene [--root <path>]`

沿用既有接口，不新增参数：

```text
环境:  TASKFLOW_REPO_ROOT 可覆盖从 git 推导的根（smoke 用它）
退出码: 恒为 0
输出:   成功与跳过都静默；任何一行输出都是回归
```

三种「跳过」都是静默 exit 0，且**不产生任何写入**：无 `git`、根不是 Git 仓库、`git rev-parse --git-path` 拿不到路径。

### 契约 2 — `info/exclude` 的规则形状

追加两行，逐行精确（`grep -qxF`），不排序、不合并、不改已存在行：

```text
TaskFlowDocs/repository-docs/personal.md
TaskFlowDocs/**/sessions.md
```

| 项 | 契约 |
| --- | --- |
| 匹配方式 | 整行逐字节相等。写法不同（如 `/TaskFlowDocs/...`）视为另一条规则，再加一行 |
| 位置 | 追加到末尾。既有内容（含 Git 自带的注释与样例）整段保留 |
| 顺序 | 先 `personal.md` 后 `sessions.md`，常量字符串一次写出 |
| 文件不存在 | `mkdir -p` 后写两条 |
| 重复运行 | 两条都在时不写文件，mtime 也不变 |
| 部分存在 | 只补缺的那条，已存在的不重复 |

**为什么用 `TaskFlowDocs/**/sessions.md` 而不是枚举位置。** `sessions.md` 出现在两个位置：active 任务目录与 `achieved/<task>/`。Git 的 `**` 在 `info/exclude` 里与 `.gitignore` 同义（两者共用同一套 pathexpr），所以一条覆盖两处；枚举会漏掉第三个将来出现的位置。

**为什么 `.gitignore` 那一条留着，而不是删掉。** 两条规则的作用域不同：`.gitignore` 跟着仓库走，管的是「克隆了本仓库、但还没跑过 hook 的人」；`info/exclude` 跟着 clone 走，管的是「在别人的项目里用这个插件」。取并集没有副作用（同一条路径两种等价写法），而删掉前者会让一个刚克隆、还没跑 SessionStart 的树把 `sessions.md` 带进 `git add -A`。真要避免的是「两处出处描述不同的东西」——所以注释里写清分工，而不是让 `.gitignore` 假装自己是机制。

### 契约 3 — 与 `info/attributes` 的共存

同一个 hook 顺序写两个文件，互不知情：

1. `merge.taskflow-todo.driver`（`--local` config）
2. `TaskFlowDocs/todo.md merge=taskflow-todo`（`info/attributes`）
3. 两条 ignore 规则（`info/exclude`）

任何一步失败都 `exit 0`，**后面的步骤不再执行**——与既有实现一致（每步 `|| exit 0`）。这不是「尽量多写一点」，而是「配置到一半的仓库要停下」：半套配置比没有配置更难诊断，而 SessionStart 下次还会再来。

## Invariants and Compatibility

- **I1** 该 hook 只追加，从不修改或删除任何已存在的行——无论 `info/attributes`、`info/exclude` 还是 `--local` config。
- **I2** 输出恒为空，退出码恒为 0。
- **I3** 不写仓库树内的任何文件；被跟踪的 `.gitignore` / `.gitattributes` 不创建、不修改。
- **兼容性代价（必须承认）**：hook 改名。任何文档或脚本照抄 `hooks/install-merge-driver` 会失败。CHANGELOG 归入 `Changed` 并给出新名字；仓库内不再出现旧字符串（A5）。这是有意的重命名，不是兼容问题——留一个别名脚本就是让两个名字永远同时存在。

## Validation and Error Semantics

| 情形 | 行为 | 退出码 |
| --- | --- | --- |
| 无 `git` | 静默返回 | 0 |
| `TASKFLOW_REPO_ROOT` 不是 Git 仓库 | 静默返回，不写任何文件 | 0 |
| `git rev-parse --git-path` 失败 | 该步骤静默返回 | 0 |
| `info/` 不可写 | 静默返回 | 0 |
| 参数错误 | 无参数接口，无从传错 | — |

没有一条路径返回非零。这是既有的契约，本任务不改：这个 hook 从 SessionStart 被调用，一个失败的 Git 配置不该让会话失败。

## Code and Test Constraints

- **bash 3.2 + busybox awk + POSIX sed**，无 Python、无 `declare -A`、无 `mapfile`、无 GNU-only `sed -i`（`CODE_STYLE.md:12-18`）。
- **不用管道喂大文本给 `grep -q`**：`set -o pipefail` 下会因 SIGPIPE 假失败。`info/exclude` 很小，但仍沿用 `grep -qxF -- "$pattern" "$file"` 读文件的形式。
- **断言风格**：沿用 `hooks/smoke-test` 的 `... || { echo "FAIL …"; exit 1; }`，不引入框架。
- **变异验证**：每条新断言都要一次「故意改坏 → 套件红 → `cp` 还原 → `diff -q` 确认逐字节相同」。

## Design Decisions and Alternatives

| # | 决定 | 备选与拒绝理由 |
| --- | --- | --- |
| D1 | 扩展并改名号为 `install-git-hygiene` | 备选：新开第二个 hook。两个 hook 写同一个 `info/` 目录，将来改 exclude 得先找对是哪个；备选：塞进旧名字，名字名不副实。 |
| D2 | 写 `info/exclude` | 备选：写被跟踪的 `.gitignore`。改的是所有人的视图，包括想提交这些文件的仓库。 |
| D3 | 逐行精确匹配 | 备选：按前缀或正则去重。等价写法被判重就会漏，漏的方向是「文件又被提交」。 |
| D4 | 已跟踪的 8 份留给子任务 | 备选：本任务一并 `git rm --cached`。机制与批量删除是两种风险，混在一个 PR 里 review 判不准。 |
| D5 | 无 hook 时文档写一句 | 备选：热路径 hook 也调一次。把一个一年只需成功一次的 Git 写入放进每轮 prompt 的路径。 |
| D6 | 失败即停，不继续后续步骤 | 备选：每步独立 try。半套配置比没有配置更难诊断，而下次 SessionStart 会重来。 |

## Open Questions

无。三个决定由用户给定，见 `prd.md` 的 Open Questions。
