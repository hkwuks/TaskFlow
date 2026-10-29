# 断言插件 manifest 声明的 `$schema` 可用
> Task version: v1
> Status: in_progress

## Goal

仓库里有两个 manifest 用 `$schema` 指向一份 JSON Schema，用来让编辑器、校验器和阅读者知道这份 manifest 该按什么形状理解。这两个指针现在**都指向 404**，而仓库里没有任何检查发现这件事。本任务给 `hooks/release-check` 加一段断言，让「声明了 `$schema` 但指向不成立」和「同类 manifest 里有的声明、有的不声明」都变成一次可见的失败，而不是等到某个工具静默跳过校验才被发现。

## Background / Confirmed Facts

以下均为 2026-10-29 在本仓库实测。

### 声明现状（5 个 manifest，2 个声明）

| 文件 | `$schema` |
|---|---|
| `.claude-plugin/marketplace.json` | `https://anthropic.com/claude-code/marketplace.schema.json` |
| `.claude-plugin/plugin.json` | `https://anthropic.com/claude-code/plugin.schema.json` |
| `.codebuddy-plugin/marketplace.json` | 无 |
| `.codebuddy-plugin/plugin.json` | 无 |
| `.codex-plugin/plugin.json` | 无 |
| `package.json`（dsh） | 无 |

### 两个声明都指向 404（**这是当前正在发生的事实，不是风险**）

```
https://anthropic.com/claude-code/marketplace.schema.json
  301 -> https://www.anthropic.com/claude-code/marketplace.schema.json -> 404
https://anthropic.com/claude-code/plugin.schema.json
  301 -> https://www.anthropic.com/claude-code/plugin.schema.json -> 404
```

### 找不到能替代的正确地址

2026-10-29 逐个试探，没有一个返回真正的 JSON Schema：

| 候选 | 结果 |
|---|---|
| `json.schemastore.org/claude-code-plugin.json` | 404 |
| `code.claude.com/docs/schema/plugin.json` | 404 |
| `docs.anthropic.com/claude-code/plugin.schema.json` | 200，但内容是 **296 KB 的 HTML 错误页**，不是 schema |

因此**本任务不改 URL**：改地址只能靠猜，而猜出来的地址会让断言通过却仍然指向错误的东西 —— 那比现在更糟，因为失败的信号被伪装成了成功。

### 现有检查一个都没读过 `$schema`

`hooks/release-check`、`hooks/smoke-test`、`RELEASE.md` 三处 grep `schema` 零命中。`release-check` 已经会读这 5 个 manifest，但只读 `version` 字段。

### 仓库的检查不带网络

`hooks/release-check` 与 `hooks/repository-check` 里没有任何 `curl`/`wget`；`repository-check` 唯一出现 `http` 的地方是把 URL 里的凭据抹掉再打印。断言若联网取 schema，会把一个确定性检查变成依赖外网可用性的检查。

## Requirements

- **R1 只断言仓库内可验证的事实，不联网。** 断言不得发出任何网络请求。理由是上一条：联网会让 `release-check` 在断网、DNS 抖动或对方限流时假红，而它目前是一个完全离线的检查。
- **R2 声明了就不得为空。** `"$schema": ""`、`"$schema": null`、只有键没有值，都算失败。
- **R3 声明了就必须是绝对 HTTPS URL。** 相对路径、`http://`、以 `//` 开头的协议相对形式，都算失败。
- **R4 同一文件里只能有一个 `$schema` 键。** 重复键在 JSON 里是未定义行为，解析器取第一个还是最后一个取决于实现；这里不猜。
- **R5 五个 manifest 要么都声明、要么都不声明，或者差异被显式记录。** 现状是 2/5 声明，而这个差异没有任何地方说明它是有意的。断言必须让「有人加了第三个」和「有人删掉了一个」都留下痕迹，而不是静默通过。
- **R6 断言放进 `hooks/release-check`**，与既有的版本一致性检查并列，复用它的 `needs`/`STATUS:` 退出约定（`needs=1` → `STATUS: needs-user-input`，退出 2）。
- **R7 不修改任何 manifest。** 本任务只加检查。两个 404 作为断言第一次运行时的**已知失败**记录下来，修复留给后续任务。
- **R8 文档同步**：`CHANGELOG.md` 增一条；若 `hooks/README.md` 或 `skills/taskflow/references/runtime.md` 描述了 `release-check` 的检查范围，一并更新。
- **R9 让 CI 真的执行到这段断言。** `hooks/smoke-test` **已经**在夹具仓库上调用 `hooks/release-check`（`:4488` 起的 `== release-check catches version drift and a bad marketplace pin ==` 一节，模式是「构造合法的 → 必须 pass，再轻量破坏一个字段 → 必须点名失败」）。新的 `$schema` 用例**并入这一节**，不新建机制、不改 `tools/workflow-affected`。这同时解决两件事：`hooks/*` 属于 smoke 集合，所以改 `release-check` 时 CI 一定会执行到它；夹具仓库又使真实仓库的两个 404 不会把 smoke 拖红。

## Acceptance Criteria

- **A1** 对当前仓库运行 `bash hooks/release-check .` → 退出码 **2**，`STATUS: needs-user-input`，且输出里逐条点名两个 404 声明所在的文件与 URL。
- **A2** 把 `.claude-plugin/plugin.json` 的 `$schema` 改成 `""` → 断言报出「声明为空」，且是那条具体的失败信息，不是笼统的失败。
- **A3** 把某一处 `$schema` 改成 `http://example.com/x.json` → 断言报出「不是 HTTPS」。
- **A4** 把 `.claude-plugin/plugin.json` 的 `$schema` 整行删掉 → 断言报出「声明数量与记录的不一致」，并说明现在是几个声明、记录的是几个。
- **A5** 不联网也能得到 A1–A4 的全部结果：断网状态下跑同一条命令，结论不变。
- **A6** 断言**只在** `$schema` 相关事实变化时改变结论：把 workspace 恢复到当前 `main` 的 manifest 内容后，结论仍为 A1 描述的失败；仓库里其他任何字段变化都不影响它。
- **A7** `bash hooks/smoke-test` → `ALL SMOKE PASSED`（回归）。
- **A8** `git diff --check` 干净。
- **A9** 并进 `:4488` 那一节后，夹具里**不含**任何 `$schema` 时 `release-check` 仍 `STATUS: pass`（证明新检查不会把没有声明的仓库判红）。
- **A10** 夹具里加一个合法的 `$schema`（绝对 HTTPS URL）时仍 `STATUS: pass`；再把它改成 `""` 或 `http://…` 时退出 2 且输出点名该文件与原因。
- **A11** `hooks/smoke-test` 不读真实 manifest —— 真实仓库当前两个 404 声明不会让它变红。这一点由后果证明：把真实 manifest 原样留在仓库里跑 `bash hooks/smoke-test`，结果是 `ALL SMOKE PASSED`。

## In Scope

- `hooks/release-check` 新增一段 `$schema` 检查。
- `hooks/smoke-test` 里为该检查新增的断言（若该套件已有 `release-check` 的测试段落，则并入该段），以及一段在夹具仓库上调用 `hooks/release-check` 的回归（R9）。
- `CHANGELOG.md`。
- 本任务的 TaskFlow 文档。

## Out of Scope

- **修那两个 404 URL。** 用户已于 2026-10-29 裁定：只加断言，先不动 URL。找不到可验证的正确地址时改 URL 只能靠猜。
- **给另外三个 manifest 补 `$schema`。** 这是不是有意的差异，本任务不下结论（见 Open Questions）。
- **联网校验 schema 可达性。** 见 R1。
- **校验 manifest 内容是否符合 schema。** 断言只检查声明本身，不检查 manifest 是否符合它声明的 schema —— 那需要真的取到 schema。
- **`hooks/repository-check`。** 它是仓库结构检查，不是发布检查。
- 前半「三宿主手工 catalog 校验改条件式」：前提已被 `2026-09-19-release-flow-exception` 搬走，`RELEASE.md` 里已无该步骤，无对象可改。

## Risks / Deferred Items

- **A1 会让 `release-check` 从「通过」变成「需要用户输入」，这是有意的。** 一个当前就坏的指针应当让检查红起来。若合并后立刻阻塞了发布流程，那正是它该做的事；但要提前说明，因为它会让 main 上的 `release-check` 立刻变成非 pass。
- **A5 的断网验证**在本机可用 `unshare -n` 或临时 `HTTP_PROXY=http://127.0.0.1:1` 模拟；若宿主不支持，退化为代码审查（断言里无网络调用）+ 记录该限制。
- **R5 的「差异被显式记录」有两种实现**：断言里硬编码「允许的声明清单」，或读一个仓库内的记录文件。本任务倾向硬编码 + 注释说明理由（见 Plan），因为多一个文件就是多一个会漂移的东西。
- **两个 404 会一直红到有人决定怎么修。** 如果长期不修，检查会变成噪音，进而被忽略 —— 这是这类断言的典型死法。缓解办法是把修复 URL 作为本任务的 Follow-up 明确列出，而不是留着。

## Open Questions

- **另外三个 manifest 为什么没有 `$schema`？** `.codebuddy-plugin/*` 和 `.codex-plugin/plugin.json` 可能本来就没有公开 schema，`package.json` 是 npm 的、有自己的约定。这一点本任务不猜；如果查明是「本来就没有」，那 R5 的正确形态是「记录哪些可以有、哪些不该有」，而不是「要求五个都有」。
- **`release-check` 由谁运行、什么时候运行？—— 已查明（2026-10-29）。** CI 会跑它（`.github/workflows/hooks.yml:101-111`，`bash hooks/release-check .`），但只在 `release` 分类为真时：`.claude-plugin/*`、`.codex-plugin/*`、`.codebuddy-plugin/*`、`package.json`、`CHANGELOG.md`、`README.md`、`README.zh-CN.md` 有改动（`tools/workflow-affected` 的 `release=1` 分支）。

  **这带来一个必须解决的后果**：本任务改的是 `hooks/release-check`，而 `hooks/*` 落在 **`smoke` 集合**、不在 `release` 集合，所以这一轮 CI 会跑 smoke，**不会跑 `release-check` 自己**。断言写进去之后，CI 里没有任何一次执行会验证它。

  **用户裁定（2026-10-29）：让 `hooks/smoke-test` 直接调用 `hooks/release-check`。** 理由：`hooks/*` 属于 smoke 集合，每次改 hook 都会跑 smoke，所以改 `release-check` 时 CI 一定会执行到新断言；把 `release-check` 加进 release 触发集只在它自己被改时才生效，覆盖不到「新断言是否真的工作」。

