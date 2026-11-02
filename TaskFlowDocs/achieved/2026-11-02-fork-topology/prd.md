# 推 PR 之前先确定哪个仓库接收它

> Task version: v1
> Status: completed

## Goal

Agent 要推一个 PR 时，必须知道两件事，而这两件事都不是 `git remote -v` 能回答的：**这个分支能推到哪个仓库**，以及 **PR 的 base 应该指向谁**。在 fork 场景下二者不同——分支推到自己可写的 fork（head），PR 却要开给上游作者的仓库（base）。推错方向的结果是推送到一个没有写权限的仓库而失败，或者更糟，把 PR 开到了错误的 base 上。

本任务给 TaskFlow 增加一个可选的联网检查，把这两个问题变成**可核对的事实**，而不是从 remote 名字猜出来的结论。`CONTRIBUTING.md:9` 现在写着「remote names alone are not evidence」，但没有任何工具提供那份证据。

## Background / Confirmed Facts

以下均为 2026-11-02 在本仓库与真实 fork 上实测。

### `parent` 与 `source` 的语义（官方 OpenAPI 原文）

`GET /repos/{owner}/{repo}` 的接口描述写着：

> The `parent` and `source` objects are present **when the repository is a fork**. `parent` is the repository this repository was forked from, `source` is the ultimate source for the network.

这直接给出 R2 的依据：base 不是推断出来的，它是 `parent.full_name` 这个**直接读出的字段**；多层 fork 时 `parent` 与 `source` 不同，那是唯一需要人来决定的情形。

### `permissions` 是身份相关的，且匿名单次调用拿不到

实测同一仓库的两种身份：

| 身份 | 返回 |
|---|---|
| 已认证 `hkwuks` | `{"admin":true,"maintain":true,"pull":true,"push":true,"triage":true}` |
| 匿名 | `HTTP 403`，响应里**没有 `permissions` 字段**，也没有 `fork` 字段 |

匿名那次拿到的 403 是 **API 限流**（`API rate limit exceeded for 212.135.214.8`），不是权限错误。这一点很重要：本机在开发本任务期间真实撞上了它，说明 R4 要处理的四种缺席里，**限流不是边角情况，它就是当前的默认状态**。

两条结论：

1. `permissions.push` 回答"我这个身份能不能推"，不是仓库配置。这正是需要的事实。
2. 未认证时它根本不存在，因此**不能用一条命令的成败区分"没权限"与"没登录"**——必须按退出码和错误体分开处理（R4）。

### 现状：没有任何 hook 联网

`hooks/release-check:100` 明确写着「Deliberately no network」；`hooks/external-evidence` 只从事件 JSON 里读 URL，不发起请求；`hooks/repository-check` 是纯本地的（对它 grep `gh|curl|wget` 为 0）。

本任务将引入**第一个联网的 hook**。这个边界必须由代码与断言本身守住，而不是靠一句注释。

### remote 名不携带信息

本仓库的 remote 叫 `origin`，`CONTRIBUTING.md:9` 要求 fork 场景下核对目标仓库。但 Git 对 remote 名没有语义约束：fork 用户的 `origin` 可能是自己的 fork，也可能指向上游，还可能叫别的名字。因此**名字只能用来枚举，不能用来判断角色**。

## Requirements

- **R1 — 新增一个独立的检查，不改 `repository-check`。** 新脚本 `hooks/remote-topology`；`repository-check` 保持完全离线，输出与退出码逐字节不变。理由：`repository-check` 的判定是确定性的，把网络挂在它上面会让"网络抖动"与"仓库有问题"在输出上无法区分。

- **R2 — 只报告 fork 拓扑与 push 权限。** 每个 remote 一行：指向哪个仓库、是不是 fork、parent 是谁、当前身份能否推送。`parent`/`source` 是直接读出的字段，不是推断。不查分支保护。

- **R3 — 结论给到可执行的形状。** 输出必须让读者直接拿到两条命令的实参：`git push <remote> <branch>` 与 `gh pr create --head <owner>:<branch> --base <branch>`。只列事实不给用法，等于把判断留给下一次。

- **R4 — 四种缺席都输出"未检查"，且退出 0。** `gh` 不在 PATH、未认证、无网络、限流/API 报错——统一输出一行说明并正常退出。这个检查是帮助，不是门禁；`repository-check` 的 STATUS 不受它影响。四种要**分开说明**，因为它们对应四种不同的用户动作（装 gh / 登录 / 等网络 / 等限流恢复）。

- **R5 — 网络调用必须有超时，且不得阻塞会话。** 本检查**不进 `SessionStart`**，只在读者显式调用时运行。一次调用至多 N 次请求（N = remote 数），不重试。

- **R6 — 只读。** 不写任何文件，不改 remote，只发 `GET /repos/*`。

## Acceptance Criteria

- **A1** 非 fork 仓库上运行，输出 `origin: hkwuks/TaskFlow  fork=no  push=yes`，并给出 `--base main`。

- **A2** fork 夹具上运行（用真实的 `hxhy00/TaskFlow` 返回构造），能区分可推的 fork 与不可推的上游，并给出 `--head <fork-owner>:<branch> --base <parent>`。

- **A3** 多个 remote 指向同一仓库网络时，每个 remote 各占一行，不合并、不去重。

- **A4** `gh` 不在 PATH：输出「未检查：gh 不可用」，退出 0，**不输出任何看似结论的文字**。

- **A5** `gh` 未认证：输出「未检查：gh 未登录」，与 A4 措辞不同。

- **A6** 无网络 / 连不上：输出「未检查：无法访问 GitHub API」，在一次调用内失败，不重试。

- **A7** 限流（HTTP 403 且 `message` 含 rate limit）：输出「未检查：API 限流」，与 A4/A5/A6 措辞不同。

- **A8** 超时：对不可达地址，命令在 10 秒内返回。

- **A9** `repository-check` 的输出与退出码，在本任务前后逐字节相同（`diff` 对比）。

- **A10** 该脚本不出现在任何 `hooks-*.json` 的事件接线里（`grep` 可验证）。

## External Facts

- Depends on external facts: yes
- Source: https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json
- What it settled: `parent` 与 `source` 只在 fork 上出现，`parent` 是直接上游、`source` 是网络根；`permissions` 含 `admin`/`maintain`/`push`/`triage`/`pull` 五个布尔。这决定了 R2 只读一次调用即可给出 base，不必再查协作者或组织成员。
- Source: https://api.github.com/repos/hkwuks/TaskFlow
- What it settled: 匿名请求返回 `403 API rate limit exceeded`，响应体里既无 `permissions` 也无 `fork`；同一仓库用已认证的 `gh` 请求则返回完整字段且 `push:true`。这证明 `permissions` 是身份相关的、匿名不可得，从而决定了 R4 必须按退出码与错误体把"未登录"、"无限流"、"限流"三种情况分开，而不能统一报"没权限"。

## In Scope

- 新增 `hooks/remote-topology`。
- 在 `skills/taskflow/references/runtime.md` 记录这个检查：可选的、联网的、不进 SessionStart。
- 在 `CONTRIBUTING.md:9` 那条规则旁指出这份可执行依据。
- smoke 断言覆盖 A1–A10，联网部分用固定 JSON 夹具，不真的发请求。

## Out of Scope

- **不改 `repository-check`。** 它的离线性是设计决定，不是疏漏；A9 钉住它。
- **不查分支保护。** 另一次调用、另一类问题，且多数用户仓库未保护（404），信息价值低。
- **不在 SessionStart 里运行。** 见 R5。
- **不实现推送或建 PR。** 只回答"该往哪推"，不代劳。
- **不为其他宿主适配。** `gh` 是本地 CLI，与宿主无关；该脚本不被任何 `hooks-*.json` 接线（A10）。

## Risks / Deferred Items

- **引入第一个联网 hook，是一条会长期存在的边界变化。** 缓解：它不接任何事件，只能被显式调用；`repository-check` 被 A9 钉住；A10 断言它不在任何事件接线里。真正的风险不是它联网，而是**将来有人把它接进 SessionStart**——A10 存在的目的就是让这种改动必须显式发生。

- **`permissions.push` 依赖身份，因此不能跨身份缓存。** 本任务不缓存。

- **多层 fork 时 `parent` 与 `source` 不同。** 本任务报告两者，但不为这种情况给出 base 建议——"提给直接上游还是网络根"是人的决定，已在输出中注明。

- **限流。** 认证 5000 次/小时，本检查每次至多 N 次调用。不重试，限流时按 R4 报"未检查"。开发期间已真实撞上一次匿名限流，这验证了 R4 不是假想场景。

## Open Questions

无——三个待定项已于 2026-11-02 与用户确认：离线即报未检查且退出 0；只报 fork 拓扑与 push 权限；模板随插件分发（后者属任务 B）。
