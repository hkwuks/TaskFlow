# Spec — hooks/remote-topology

> Task version: v1
> Status: completed

## Objective

回答一个问题：**这次推送应该推到哪个 remote，PR 的 base 应该写谁。**

`git remote -v` 只给出名字和 URL，而名字不携带语义——一个 fork 用户的 `origin` 可能是他自己的 fork，也可能指向上游。`CONTRIBUTING.md:9` 要求「remote names alone are not evidence」，但仓库里没有任何工具产出那份证据。本模块就是那份证据的生产者。

**目标用户**：在 fork 上工作、或在一个 remote 名不可信的环境里工作的 Agent。它不面向只想看看仓库状态的读者——那是 `hooks/repository-check`，保持离线不变。

**它不做判断。** 它把事实排成读者能直接使用的形状，最后两行是两条命令的实参。选哪一条仍然是人或 Agent 的决定。

## Commands

```bash
# 用法
bash hooks/remote-topology [repository-root]

# 典型输出（非 fork，已认证）
# Remote topology for: /path/to/repo
# - origin: hkwuks/TaskFlow  fork=no  push=yes  default=main
#   → git push origin <branch>
#   → gh pr create --base main --head hkwuks:<branch>
#
# 典型输出（fork，已认证）
# - origin: hxhy00/TaskFlow  fork=yes  push=yes  parent=hkwuks/TaskFlow  default=main
#   → git push origin <branch>
#   → gh pr create --base main --head hxhy00:<branch>   (opens against hkwuks/TaskFlow)
#
# 缺席（四种之一）
# - origin: unchecked (gh not found)   ← 退出 0
```

**退出码**：始终 `0`。这不是门禁，没有"失败"这个状态；四种缺席都只是"没查成"，各自说清楚原因即可。

这与 `CODE_STYLE.md` 的 `0/2/3` 约定不冲突：那个约定描述的是**有判定语义**的检查。本脚本没有判定语义，因此不占用 `2`/`3`。

## Project structure

只新增一个文件：

```text
hooks/remote-topology      # 新增，可执行
```

不新增：

- 不新增 `hooks/*-evidence` 之类的旁路存储——本脚本只读。
- 不新增宿主接线——它不出现在任何 `hooks-*.json`（A10 断言）。
- 不改 `hooks/repository-check`（A9 断言）。

## Code style

沿用 `CODE_STYLE.md` 的 Shell 节：

- `#!/usr/bin/env bash`，`set -euo pipefail`。
- 所有路径与变量展开加引号。
- **不引入解释器依赖**——这是插件的硬约束，`hooks/` 下没有任何 Python/Node 依赖，本脚本保持 `bash` + `gh` + `git`。

### 与既有 hook 不同的两点，各有理由

**1. 联网。** 仓库里目前零联网 hook（`release-check:100` 明写 offline）。本脚本是第一个。边界靠三件事守住：

- 不接任何事件（A10）；
- 只发 `GET /repos/*`（R6）；
- 不写任何文件（R6）。

**2. 始终退出 0。** 其余 hook 用 `2`/`3` 表达工作流状态。本脚本没有状态可表达——它是查询工具，不是检查器。若它退出非 0，调用方（Agent）会把它当成"仓库有问题"，而实际情况可能只是没装 `gh`。

### 四种缺席必须分开

实测（2026-11-02）：

| 情形 | `gh` 退出码 | 判据 |
|---|---|---|
| `gh` 不在 PATH | — | `command -v gh` |
| 未认证 | `1` | `gh auth status` 非 0 |
| 网络不可达 | `1` | 与上一条**退出码相同** |
| 限流 | `1` | 错误体含 `rate limit` |

**未认证与网络失败退出码相同**，所以判断顺序是：先 `auth status` 排除未认证，再发请求，请求失败时读错误体区分限流与网络。这就是 A4–A7 要四种措辞的原因——它们对应四种不同的用户动作（装 gh / 登录 / 等网络 / 等限流恢复）。

### 超时

`gh` 没有 `--timeout`。用 `timeout 10` 包裹每次调用（coreutils 的 `timeout` 在三大平台都有；macOS 通过 `gtimeout` 不保证，因此**先检测 `timeout` 是否可用，不可用则不包裹并注明**）。这比引入 `perl alarm` 之类的变通更小。

`timeout` 与 `gtimeout` 的差异记在 runtime.md，不写兼容层。

### 输出语言

沿用 artifact-language 规则：hook 匹配的字段名保持英文（`fork=`、`push=`、`parent=`），其余说明用用户工作语言。本脚本输出是给 Agent 读的**机器可辩形状**，因此整行保持英文，不翻译——与 `repository-check` 的 `STATUS: pass` 一致。

## Testing strategy

smoke 断言覆盖 A1–A10，全部**离线**：

- **夹具而非真请求。** 用固定的 JSON 字符串（真实 `gh api` 返回的拷贝）驱动解析逻辑。做法是把 `gh` 换成一个 stub：在 `PATH` 前置一个假的 `gh` 脚本，按参数返回预设 JSON 或退出码。这样四种缺席可以逐一构造，且测试不依赖网络、不消耗 API 额度、在 CI 三平台上结果一致。
- **A9 用 `diff`。** 在改动前后各跑一次 `repository-check`，比较完整输出与退出码。
- **A10 用 `grep`。** 扫 `hooks/hooks-*.json`，断言 `remote-topology` 零命中。
- **变异验证。** 每一条断言都要能被"删掉对应分支"红化，逐个做并还原（`diff -q` 确认字节一致）。

真请求只在人工验收时跑一次，结果记进 Plan 的 Verification，不进 CI。

## Boundaries

- **Always**：只读；只发 `GET /repos/*`；缺席时说明原因并退出 0；把 `push` 与 `parent` 作为**读出的字段**呈现，不推断。
- **Ask first**：把这个脚本接进任何宿主事件（`hooks-*.json`）、增加除 `GET /repos/*` 以外的请求、把它加进 `repository-check` 的 STATUS 判定。
- **Never**：写文件；改 remote；打印 token 或私有 URL；缓存结果（`permissions` 是身份相关的，跨身份复用会产生错误答案）；退出非 0 让调用方把它当成失败。
