# Windows smoke 套件不得因继承 stdin 而卡死
> Task version: v1
> Status: checking

## Goal

`hooks/smoke-test-windows.ps1` 在终端里手工运行时，跑到第 96 行 `Invoke-SessionStart 'pr'` 就永久停住，既不打印也不再前进。本任务让它无论 stdin 是关闭、空管道，还是打开但无数据，都能跑完；并补一条**只有在修复撤销时才会变红**的断言。

## Background / Confirmed Facts

以下均为 2026-10-28 在本机实测（Windows PowerShell 5.1，Git for Windows 位于 `D:\Git`，Windows 构建 10.0.26100）。

1. **卡死点在 96 行，不在 throw。** 用注入 `throw` 的方式逐段夹逼（88 / 95 / 97 / 110 / 121 / 142 / 160 / 197 / 208 九个位置）：
   - 注入在 96 行**之前**（88、95）→ rc=1，0–14 秒退出，错误消息正常打印；
   - 注入在 96 行**之后**（97 及其后任意一处）→ rc=124，超时。

   边界恰好是 `$first = Invoke-SessionStart 'pr'`（`hooks/smoke-test-windows.ps1:96`）。

2. **throw 本身从来不会挂。** `finally`（`:216`）只负责删夹具根目录，不吞异常；三处 throw 探针的退出码都是 1，消息完整。

3. **机制是继承 stdin，不是 PowerShell 收尾。** 对照组 `powershell.exe -NoProfile -Command 'echo hi'` 配同一条打开的 stdin → 1 秒正常退出。四个按契约读 stdin 的 hook（`session-start:29`、`capability-gate:44`、`capability-evidence:33`、`prompt-reminder:54`，都是 `event_json="$(cat)"`）在 stdin 打开且无数据时**全部**超时；`hooks/task` 不读 stdin，立刻返回。

4. **该写法换一种喂法就正常。** 同一行改成 `$output = '' | & ...` 后：打开 stdin → rc=0 / 27 秒；`/dev/null` → rc=0 / 24 秒；`mkfifo` + 两端持有但不写入 → rc=0 / 26 秒，四条 `PASSED` 横幅齐全。

5. **CI 永远看不到这个缺陷。** runner 的 stdin 是空的或 null，`cat` 立刻读到 EOF。因此 windows-latest 至今全绿，包括本仓库 2026-10-27 的 run `40521265502`（windows 51 秒 pass）。只有人在终端里手工跑才会撞上。

6. **`main` 上同样存在。** `git show main:hooks/smoke-test-windows.ps1` 逐字节相同：打开 stdin rc=124 / 59 秒，关闭 stdin rc=0 / 27 秒。不是本分支引入的。

7. **bash 套件早已修过同一个坑。** `hooks/smoke-test:564-566` 的注释写着「`< /dev/null`，不是管道……继承套件自己的 stdin 会让读操作在 stdin 保持打开时阻塞」，并真的传了 `< /dev/null`。PowerShell 套件是同一条教训的未应用版本。

## Requirements

- **R1** `hooks/smoke-test-windows.ps1` 里那一处 `session-start` 调用必须自带 stdin，不得继承运行者的。采用 `'' | & "$here\run-hook.cmd" session-start 2>&1`，与 bash 套件的 `< /dev/null` 是同一个意思。
- **R2** 套件的**其余**行为一字不改：`Invoke-TaskFlow`（`:15`）、launcher 参数检查（`:44`）、`Invoke-Hook`（`:135`，已经通过 `cmd /c ... < eventFile` 自带 stdin）都不动。`hooks/task` 不读 stdin，因此 `:15` 无需改动。
- **R3** 新增断言放在 bash 套件的 Windows 段（`hooks/smoke-test:740-744`）之后，沿用该段既有的 `powershell.exe` + `cygpath` 守卫：用一条**打开但不写入**的 stdin 再跑一遍整个 `smoke-test-windows.ps1`，要求它在限时内以 0 退出。
- **R4** 限时等待必须是**有界**的：不允许出现一个会永久等待的循环。超时即判 FAIL 并杀掉子进程，且 FAIL 消息要说明「stdin 被继承」这一原因。
- **R5** 断言必须**只有在修复撤销时才变红**。已实测：撤销 R1 后同一条命令 rc=124（>42 秒无进展），R1 在位时 rc=0 / 26 秒。
- **R6** 不引入兼容层，不新增解释器依赖，不新增文件；仍是 bash + PowerShell 5.1 原生能力。
- **R7** 文档同步：`CHANGELOG.md` 增 `### Fixed` 一条，说清「修的是继承 stdin，不是 throw」这个区别，因为 todo 条目的原始措辞是错的，后来者会照着错的找。

## Acceptance Criteria

- **A1** 终端里运行 `powershell.exe -NoProfile -File hooks/smoke-test-windows.ps1`（stdin 为打开的终端）→ 限时内 rc=0，四条 `PASSED` 横幅齐全。修复前同一条命令无限挂起。
- **A2** stdin 为 `/dev/null` 时 rc=0，四条横幅齐全（回归：修复不得破坏原有路径）。
- **A3** stdin 为「两端打开但不写入」的 FIFO 时 rc=0，四条横幅齐全。
- **A4** `bash hooks/smoke-test` → `ALL SMOKE PASSED`，且新增的 Windows 断言确实执行了（打印自己的 `ok`）。
- **A5** **变异验证**：把 `:31` 那一行还原成原样，`bash hooks/smoke-test` 必须在新增断言处变红并指名原因；恢复后再次 `ALL SMOKE PASSED`，且 `diff -q` 确认恢复是逐字节的。
- **A6** `git diff --check` 干净。

## In Scope

- `hooks/smoke-test-windows.ps1` 的一行（`:31`）。
- `hooks/smoke-test` 的 Windows 段末尾，新增一小节断言。
- `CHANGELOG.md` 的 `[Unreleased] / ### Fixed`。
- 本任务的 Todo 条目与 TaskFlow 文档。

## Out of Scope

- **给 `hooks/task` 加 stdin**：它不读 stdin，实测零影响。
- **改四个 hook 的 `cat`**：那是契约（宿主通过 stdin 投递事件），不是缺陷。
- **修 `hooks/smoke-test-windows.ps1` 里其他潜在的继承 stdin 问题**：`:15` 与 `:44` 的目标不读 stdin；`:135` 已经自带。
- **把新断言改成「钉住源码那一行」**：用户已选定端到端方案，见下。
- **`hooks/smoke-test` 自身的 `< /dev/null` 写法**：2026-10-25 已修，不在本任务范围。

## Risks / Deferred Items

- **CI windows job 变慢约 26 秒（51s → ~80s）。** 这是用户选定方案的自然后果：端到端复现必须真的再跑一遍套件。
- **新断言只在这台 Windows 机器与 CI 的 windows-latest 上执行**（沿用 `cygpath` 守卫）；ubuntu/macos 上跳过。这与该段既有行为一致，不额外扩大宿主差异。
- **FIFO 在 Git Bash（MSYS）下的行为未在真实 CI 上验证过。** 本机 WSL 下 `mkfifo` + 持仓 fd 复现稳定；若 CI 上 FIFO 不可用，断言必须**明确失败**而不是静默跳过——否则它就成了另一种「看起来绿」。
- **保留未修项**：`hooks/smoke-test` 里 `:743` 用 `-ExecutionPolicy Bypass` 调用子套件，属既有写法，本任务不动。

## Open Questions

无。断言形态已于 2026-10-28 由用户在两个方案（端到端 / 钉源码）之间选定**端到端**。

## 变更的影响面

只影响测试代码与一份 changelog，不触及任何 hook 的运行时行为，因此对已安装的插件零影响，无需版本兼容声明。
