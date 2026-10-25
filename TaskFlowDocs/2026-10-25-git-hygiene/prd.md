# 本地文件不上传，靠插件做，不靠用户改 .gitignore

> Task version: v1
> Status: in_progress

## Goal

`TaskFlowDocs/repository-docs/personal.md` 与 `sessions.md` 是 clone 本地的东西——前者是个人规则（不是团队政策），后者带会话 id、工作目录、时间戳、`Session availability: local-only`。文档三处都写着「never committed」，但**没有任何机制让它发生**：Agent 一句 `git add -A` 就把它们带进提交，而用户自己装的这一份仓库的 `.gitignore` 管不到别人的仓库。

本任务让插件在每个 clone 的 `.git/info/exclude` 里写两条规则，用户不需要知道 `.gitignore` 的存在。

## Background / Confirmed Facts

以下是 2026-10-25 在本仓库实测的：

- **`personal.md` 靠 `.gitignore` 侥幸生效，不靠机制。** `.gitignore:16-17` 的 `TaskFlowDocs/repository-docs/*` 加 `!index.md` 把它排除了——纯属那三行是为了别的目的写的（`index.md` 是仓库里的，其余是本地）。别的仓库装插件、走 `repository-docs-context` 建 `personal.md`，那就没有任何规则挡它。
- **`sessions.md` 被提交过 8 份。** `git ls-files 'TaskFlowDocs/achieved/*/sessions.md'` 有 8 条，磁盘上 8 条（`achieved/` 共 85 个任务目录）。它不是「想象的风险」，已经发生过 8 次。
- **我上一轮在 `.gitignore:12-18` 加了 `TaskFlowDocs/**/sessions.md`（commit `c630536`）。** 这条规则只对本仓库有效，而它本身是一条被跟踪的行——等于要求每个克隆这份仓库的人接受我的本地约定。这正是本任务要否掉的做法。
- **被跟踪的文件不受 ignore 影响。** 实测（本地临时仓库）：`info/exclude` 加上规则后，未跟踪的被隐藏，`git add -f` 提交过的那份仍然是 ` M `，`git check-ignore` 也报告 `not ignored`。所以规则只挡「还没被提交过的」，已经提交的要另一次决定——这是子任务 `TF-20261025-24d06c` 的事。
- **`.git/info/` 是 per-clone 的，worktree 共用。** 实测：`git -C <worktree> rev-parse --git-path info/exclude` 返回主仓库的 `.git/info/exclude`，不是 worktree 私有目录。这一点决定了规则的可见范围是「整个 clone」而非「这个 worktree」。
- **既有写者已经在用这个位置。** `hooks/install-merge-driver` 已经往 `.git/info/attributes` 写 `TaskFlowDocs/todo.md merge=taskflow-todo`，注释写明选它是「per-clone, so a repository that has not adopted the driver is unaffected by another's setup」。同一段理由原样适用于 `info/exclude`。
- **`.gitignore` 里的会话规则是我加的，不是仓库原有约定。** `git log -S'sessions.md' -- .gitignore` 只有 `c630536`。

## Requirements

- **R1 — 一个 hook 负责全部 per-clone Git 配置。** `hooks/install-merge-driver` 改名为 `hooks/install-git-hygiene`，继续写它原来那两样（driver 配置、`info/attributes`），并新增第三样（`info/exclude` 的两条规则）。`hooks/session-start` 的调用点、四份列出 `hooks/` 目录的文档同步改名。
- **R2 — 排除规则写进 `info/exclude`，不写 `.gitignore`。** 两条：`TaskFlowDocs/repository-docs/personal.md`、`TaskFlowDocs/**/sessions.md`。逐行精确匹配后追加，缺哪条补哪条，已存在的行不重复。这是 per-clone 状态，所以别人的仓库不受影响——与它已经在 `info/attributes` 做的事同理。
- **R3 — `.gitignore` 里那一条保留，但改写理由。** `c630536` 加的 `TaskFlowDocs/**/sessions.md` 留着：它管的是**克隆本仓库的人**，插件那条管的是**用户自己的项目**，两个作用域不重叠，取并集没有副作用。注释改成说明这个分工，而不是把它写成「本地文件不上传」的机制。`repository-docs/*` 那三行保留——它服务的是「`index.md` 与本地文件的分界」，不是因为 `personal.md`。
- **R4 — 文档写明它是什么，以及它什么时候不在。** `runtime.md` 的 wiring 段、`hooks/README.md` 的条目与 Scope 段、`SKILL.md` 提到 `personal.md` 是 local-only 的那两处、`artifacts.md` 的对应句，都要说清：排除由插件在每个 clone 写一次，规则只在未跟踪时生效，以及**没跑过 SessionStart 的 clone 需要手动跑一次这个 hook**（hooks 可选，本仓库同意这一点，所以不假装它一定跑过）。
- **R5 — `hooks/smoke-test` 断言它。** 覆盖：新名字存在且旧名字不存在（目录清单断言已覆盖，但要指名）、首次运行写出两条规则、二次运行不重复、`.gitattributes` 不被创建、非 Git 根静默无操作、`git check-ignore` 对两个路径生效、已跟踪的副本仍然出现在 `git status`（这一条是「规则不掩盖真实漂移」的证明）。既有那段 `install-merge-driver` 断言改写为新名字，不新增平行的一段。
- **R6 — 已提交的 8 份副本不在本任务处理。** 子任务 `TF-20261025-24d06c`。本任务交付机制；批量 `git rm --cached` 是另一个决定，影响所有 clone。

## Acceptance Criteria

| # | 可观察条件 |
| --- | --- |
| A1 | 在一个没有 `.gitignore` 的临时仓库里跑一次 `install-git-hygiene`，`personal.md` 与任意 `TaskFlowDocs/<task>/sessions.md` 都不出现在 `git status --porcelain`（`git check-ignore -q` 两者均命中） |
| A2 | 二次运行，`info/exclude` 逐字节不变（不重复、不重排、不动用户自己写的行） |
| A3 | 已跟踪的 `sessions.md` 仍出现在 `git status`（规则不掩盖真实漂移），`git check-ignore` 对它返回未忽略 |
| A4 | 该 hook 在非 Git 目录、只读 `.git`、无 `git` 命令三种情形下 exit 0 且不打印任何东西 |
| A5 | `hooks/session-start` 调的是新名字；仓库里不再出现 `install-merge-driver` 这个文件名（含四份文档树与调用点） |
| A6 | `.gitignore` 的 `sessions.md` 规则保留但注释说明分工；`personal.md` 的排除只由插件提供（`.gitignore` 没有针对它的规则，命中它的是 `repository-docs/*`） |
| A7 | 五份文档对同一机制描述一致：per-clone、只在未跟踪时生效、没跑过 hook 的 clone 要手动跑一次 |
| A8 | `bash hooks/smoke-test`、`bash hooks/release-check .`、`git diff --check` 全绿；CI 7/7 |

## In Scope

- `hooks/install-merge-driver` → `hooks/install-git-hygiene`（改名 + 新增 exclude 写入）。
- `hooks/session-start` 的调用点与它的注释。
- `hooks/smoke-test`：既有安装段落改名并补断言。
- `hooks/README.md`：目录树、`install-*` 条目、Scope 段的说明。
- `skills/taskflow/references/runtime.md`：目录树、wiring 段。
- `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`：local-only 那几句补上「由插件排除」与手动兜底。
- `README.md`、`README.zh-CN.md`：目录树。
- `.gitignore`：删掉 `sessions.md` 那一条。
- `CHANGELOG.md`：`Changed`（hook 改名，破坏性：文档里照抄旧名字会失败）+ `Added`（本地文件被自动排除）。
- `TaskFlowDocs/todo.md`：`TF-20261025-7c5897` 的推进与收尾，`TF-20261025-33b2c4` 的结论并入本任务的 spec。

## Out of Scope

- **已跟踪的 8 份 `sessions.md`** —— 子任务 `TF-20261025-24d06c`。
- **改 `hooks/capability-evidence` / `capability-gate` 的 store 位置** —— 它们已经在 `<absolute-git-dir>` 里，本来就不在仓库树内，不需要排除。
- **给 `todo.md` 之类加任何新排除** —— 只两条，理由各自写清。
- **`info/exclude` 的逆向操作（卸载）** —— 本任务不提供卸载命令；删掉那两行就是了。
- **把规则写进 `.git/info/attributes`** —— `attributes` 不是排除机制，混用会让 `git check-attr` 的语义变味。

## Risks / Deferred Items

- **风险：改名是破坏性的。** 任何照抄 `hooks/install-merge-driver` 的外部脚本或文档会失败。缓解：CHANGELOG 归入 `Changed` 并写明新名字；仓库内不再有这个字符串（A5 钉住）。
- **风险：用户可能在 `info/exclude` 里写过同一条规则，只是写法不同**（例如带前导 `/`）。缓解：逐行精确匹配，写法不同就再加一行——那是两条等价规则，Git 取并集，无害；注释里写明不退化成模糊匹配。
- **风险：把「不该上传」当成「上传了也没事」。** 已跟踪的 8 份仍然在仓库里，本任务后它们继续可见（A3 就是钉这个）。真正的清理是子任务，别在本任务结束后以为已经干净了。
- **遗留：插件管不到「已经 `git add -f` 过的副本」。** 这是 Git 的语义，不是可以绕的东西；文档写明「规则只挡未跟踪的」。
- **遗留：没有 hook 的宿主（Codex / dsh 等）不跑 SessionStart 的这个调用。** 它们需要手动跑一次，或者用户自己写 `.gitignore`。这是既有 hook 可选性的直接后果，不做兜底代码。

## Open Questions

无。三个决定已由用户给定，记录在案：

1. 载体：扩展并改名 `install-merge-driver` → `install-git-hygiene`，不新开第二个 hook。
2. 已跟踪的 8 份副本：留给子任务 `TF-20261025-24d06c`。
3. 没跑过 hook 的 clone：文档里写一句，不另造兜底代码。
