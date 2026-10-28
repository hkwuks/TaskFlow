# Plan — Windows 套件的 stdin 卡死
> Task version: v1
> Status: checking

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/smoke-test-windows.ps1:31` — 待修的那一行。
- `hooks/smoke-test-windows.ps1:96` — 卡死触发点 `$first = Invoke-SessionStart 'pr'`。
- `hooks/session-start:29` — `event_json="$(cat)"`，契约所在。
- `hooks/smoke-test:564-566` — bash 套件对同一坑的注释与 `< /dev/null` 修法。
- `hooks/smoke-test:740-744` — Windows 段，新断言的落点。
- `CONTRIBUTING.md:21-33` — worktree 与「会话开始必须先隔离」的规则。

## Related Tasks

- 无父子关系。来源记录为 `TaskFlowDocs/todo.md` 的 `TF-20261025-645ef4`。
- 与 `2026-10-25-gate-desync-diagnosis`（已归档）同源：该任务在验证时首次撞见本缺陷，但未修。

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — purpose: 把一条措辞有误的 todo 收敛成可验收的需求；outcome: succeeded; incorporated: 需求改写为 R1–R7 与 A1–A6，并把「修的是继承 stdin，不是 throw」写进 R7，因为原条目会让后来者找错对象。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 决定两处改动的先后：先修那一行，再让断言先红后绿；outcome: succeeded; incorporated: 拆成 Step 1（修 + 断言）与 Step 2（变异验证），因为断言的正确性只能由「撤销修复后它变红」来证明，二者是同一次验证的两半。
- [Test] `agent-skills:test-driven-development` — purpose: 确认这条断言在被测行为上成立（撤销修复即红）而不是只在检测自己的写法；outcome: succeeded; incorporated: 采用「Prove-It」顺序，并将 Step 2 设为前置的真实变异验证，而不是写完断言就宣布完成。


## Preconditions

- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded. — 已读 `CONTRIBUTING.md`（worktree 与分支规则）。
- [x] 隔离先于文档 — 已完成：工作树 `.worktrees/windows-smoke-stdin`，分支 `fix/windows-smoke-stdin`，基于 `main`（`b47ea3f`）。
- [x] 能力账本环境已核对 — 本会话接线的 hook 来自已安装插件 1.1.8（写五字段 `released` 行），而仓库里的 `hooks/task` 是 1.1.9（要求六字段）。两者对同一份账本的格式不相容，本任务的 `approve` 因此改用与门同版本的已安装 `hooks/task` 执行；把插件升级到 1.1.9 属项目路径之外的动作，本任务不做。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-28 22:25 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 修那一行，并补上端到端断言

- Goal: `smoke-test-windows.ps1` 在任何 stdin 形态下都能跑完；`hooks/smoke-test` 里新增一条只在修复撤销时才变红的断言。
- Dependencies: 无。
- Files: `hooks/smoke-test-windows.ps1`、`hooks/smoke-test`、`CHANGELOG.md`。
- Implementation checklist:
  - [x] `hooks/smoke-test-windows.ps1:31` 改为 `$output = '' | & "$here\run-hook.cmd" session-start 2>&1`，上方补注释说明理由（引用 `hooks/smoke-test:564-566` 的同一条理由）。
  - [x] `hooks/smoke-test` 的 Windows 段之后新增一小节：用打开的 stdin 再跑一遍子套件，有界等待，超时 FAIL 并指名原因。
  - [x] `mkfifo` 不可用时断言必须明确失败，不得静默跳过。
  - [x] `CHANGELOG.md` → `[Unreleased] / ### Fixed` 写一条，点明修的是 stdin 继承而非 throw。
- Acceptance: PRD 的 A1–A4、A6。
- Verification: `bash hooks/smoke-test` → `ALL SMOKE PASSED`；`powershell.exe -NoProfile -File hooks/smoke-test-windows.ps1` 在 stdin 打开 / `/dev/null` / FIFO 三种形态下均 rc=0。
- Rollback: `git revert` 该提交；`hooks/smoke-test-windows.ps1` 的还原是单行。
- Status: done

### Step 2 — 变异验证：撤销修复，断言必须变红

- Goal: 证明 Step 1 的断言确实在检测这件事，而不是只在检测自己。
- Dependencies: Step 1。
- Files: `hooks/smoke-test-windows.ps1`（临时还原，验证后逐字节恢复）。
- Implementation checklist:
  - [x] 把 `:31` 临时还原成 `$output = & "$here\run-hook.cmd" session-start 2>&1`。
  - [x] 运行 `bash hooks/smoke-test`，确认它在**新增断言处**变红并打印原因。
  - [x] 逐字节恢复，`diff -q` 确认一致，再跑一次 `ALL SMOKE PASSED`。
- Acceptance: PRD 的 A5。
- Verification: 两次运行的输出对比写进 `## Verification / Review`。
- Rollback: 无需，验证完即恢复。
- Status: done

## Checkpoints

- Step 1 后：`bash hooks/smoke-test` → `ALL SMOKE PASSED`。
- Step 2 后：变异那次变红、恢复后变绿，两个结果都记录在案。

## Verification / Review

- 2026-10-28 Step 2: Mutation reverted the fix and the new assertion failed at its deadline

- 2026-10-28 Step 1: Bash suite passes; mutation reds at the 120s deadline; restored byte-identically

### 本机实测（2026-10-28，WSL + Windows PowerShell 5.1）

本机只能跑到 Windows 段以下的一部分：`cmd.exe` 拒绝把 WSL 的 UNC 临时目录当 cwd（`UNC 路径不受支持`），所以 `hooks/smoke-test` 里的 `== Windows launcher finds Git Bash ==` 一节的 `grep` 拿不到 JSON。**这是我进入这段代码前就有的环境限制**：用 `main` 上同一行（没有 `< /dev/null`）在本机跑，输出完全相同（只有 cmd 横幅），而加 `< /dev/null` 后 rc=0 —— 也就是说那一节在 WSL 下无论如何都过不去，与本次改动无关。因此新断言的正确性用一份等价的独立脚本（进程替换构造同样的 stdin）逐次验证，而不是靠整条 `bash hooks/smoke-test` 通过来声称。

| 检查 | 结果 |
|---|---|
| `bash -n hooks/smoke-test` | 通过 |
| 子套件，stdin `/dev/null` | rc=0，27s，四条 `PASSED` |
| 子套件，stdin 打开且不写入 | rc=0，27s，四条 `PASSED` |
| **变异**：`hooks/smoke-test-windows.ps1` 第 41 行还原为继承 stdin | **120s 期限到点被杀，新断言判红** |
| 变异后逐字节恢复 | `diff -q` 一致 |
| 恢复后再跑同一断言 | rc=0，27s |

### 变异过程中被断言自己的漏洞抓到一次

第一版新断言用 `sleep 60` 作管道写入端。撤销修复后它**通过了**（79s）—— 60 秒时写入端自己退出，卡住的 `cat` 拿到了 EOF，于是整套跑完。写入端必须活得比超时上限更久。改成 `sleep 200` 对 120s 期限后，撤销修复才稳定地在期限点被判红。这条写进断言上方的注释，因为下一个人缩短这个数字时不会有任何提示。

### CI 抓到本地验证的盲点：`'' |` 不是空 stdin（2026-10-28）

第一次推送后 [run 40712165629](https://github.com/hkwuks/TaskFlow/actions/runs/40712165629) 的 `smoke (windows-latest)` **失败**，其余六个 job 通过：

```
run-hook.cmd : TaskFlow SessionStart error: invalid event JSON: expected a JSON object
At D:\a\TaskFlow\TaskFlow\hooks\smoke-test-windows.ps1:41 char:24
+         $output = '' | & "$here\run-hook.cmd" session-start 2>&1
```

**原因**：PowerShell 把空字符串送进管道时不是「零字节」，而是按 `$OutputEncoding` 编码后写一行。实测本机是 `hex=0d 0a`（两个字节），CI runner 上多一个 BOM；`session-start` 把 BOM 当非法 JSON，非零退出，套件 `throw`。

**我本地的漏洞**：我只验证了「加了 `'' |` 后不再卡住」，没有验证「它送进去的是什么字节」。卡死消失这一点是真的，但代价是一个依赖环境编码的输入 —— 这种修复本身就是缺陷。

**改法**：`& cmd /c "`"$here\run-hook.cmd`" session-start < nul" 2>&1`。重定向在任何宿主上都是确定的零字节；本文件 `Invoke-Hook`（`:135`）已经是这个形状。

| 改后验证 | 结果 |
|---|---|
| 子套件，stdin `/dev/null` | rc=0，24s，四条 `PASSED` |
| 子套件，stdin 打开且不写入 | rc=0，25s，四条 `PASSED` |
| **变异**：还原为继承 stdin | **120s 期限到点被杀，断言判红** |
| 变异后逐字节恢复 | `diff -q` 一致 |

## Change Log

### CI 结果（最终）

[run 40718420289](https://github.com/hkwuks/TaskFlow/actions/runs/40718420289) @ `9ec581d` — **7/7 pass**：`changes` 5s、`release` 6s、`todo-merge-audit` 6s、`smoke (ubuntu-latest)` 25s、`smoke (macos-latest)` 1m3s、`smoke (windows-latest)` **1m0s**，`evals` skipped（路径过滤，符合预期）。

windows job 日志确认两条新断言**确实被执行**，而不是被跳过：

```
15:41:21  WINDOWS SCRIPT IS ASCII
15:41:46  WINDOWS PRE-WRITE GATE PASSED
15:42:07  WINDOWS OPEN STDIN PASSED in 21s
```

PR [#103](https://github.com/hkwuks/TaskFlow/pull/103) 已由用户合并为 `125f052`。

### CI 抓到第二个问题：新断言在任何 CI 上都不会执行（2026-10-28）

[run 40713839917](https://github.com/hkwuks/TaskFlow/actions/runs/40713839917) 7/7 全绿，但那个绿是假的。查 job 步骤：

```
Run bash smoke tests   -> skipped     (.github/workflows/hooks.yml:91, runner.os != 'Windows')
Run Windows smoke tests -> success
```

Windows runner 根本不跑 `bash hooks/smoke-test`；ubuntu/macos 上又没有 `powershell.exe`/`cygpath`，被守卫跳过。**我把断言放在 `hooks/smoke-test` 里，等于放在任何 CI 都不会执行的位置** —— 而它要复现的现象只在 Windows 上存在。上一轮我在 PR 里声称「撤销修复即判红」，那不假，但判红发生在本机，不在 CI。

**改法**：断言搬进 `hooks/smoke-test-windows.ps1` 自己 —— 那是 windows runner 上唯一执行的 TaskFlow 检查。用 `ProcessStartInfo` + `RedirectStandardInput` 自 spawn 一次，stdin 是一条从不写入也不关闭的管道；`TASKFLOW_STDIN_SELFCHECK` 防递归。`hooks/smoke-test` 那边只留 `< /dev/null` 的一行修复。

| 验证 | 结果 |
|---|---|
| 正常跑（含自检） | rc=0，51s，5 条 PASSED（含 `WINDOWS OPEN STDIN PASSED in 25s`） |
| **变异**：还原为继承 stdin | **rc=1，117s，`blocked for 90s`** |
| 恢复 | `diff -q` 逐字节一致 |

期限从 180s 缩到 90s：变异那一轮 208s 太长，CI 上一次失败要等三分半才看到原因。

- 2026-10-28 — Step 1 完成：`hooks/smoke-test-windows.ps1:41` 给出空 stdin（附理由注释）；`hooks/smoke-test` 的 Windows 段新增端到端断言；`CHANGELOG.md` 记两条。`hooks/smoke-test:735` 是同一缺陷的第二个实例（`cmd.exe //d //c ... session-start` 也继承 stdin），实测本机 rc=124、加 `< /dev/null` 后 rc=0，一并修了 —— 它原本不在 PRD 的 In Scope 里，但在同一个 shard、同一个原因，单独留着就是把已知缺陷留在原地。
- 2026-10-28 — CI 反馈修正（work revision）：第 41 行的 `'' |` 改为 `cmd /c "... < nul"`。前者在 PowerShell 里按 `$OutputEncoding` 编码后写一行（本机 `0d 0a`，CI 上带 BOM），CI 因此报 `invalid event JSON` 并失败；后者是确定的零字节。同一次修正也补上了我本地验证的盲点记录。
- 2026-10-28 — CI 反馈修正二（work revision）：端到端断言从 `hooks/smoke-test` 搬进 `hooks/smoke-test-windows.ps1`。前者在 windows runner 上被 `runner.os != 'Windows'` 跳过、在 ubuntu/macos 上被 `command -v` 守卫跳过，等于任何 CI 都不执行。期限 180s → 90s。
- 2026-10-28 — CI 反馈修正三（work revision）：`hooks/smoke-test-windows.ps1` 恢复纯 ASCII，并新增 `WINDOWS SCRIPT IS ASCII` 自检。PS 5.1 按 ANSI 码页读无 BOM 的 .ps1，我在 throw 消息里写的 em dash 导致整个文件解析失败。同轮把 Populate 了最终 CI 结果。
- 2026-10-28 — 能力账本环境：本会话接线的 pre-write 门来自已安装插件 1.1.8（写五字段 `released` 行），仓库里的 `hooks/task` 是 1.1.9（读六字段）。为不复用一套不相容的账本，首次释放后用仓库版重放同一批阶段。把插件升级到 1.1.9 属项目路径之外的动作，未做。


## Follow-ups

- `hooks/smoke-test:743` 用 `-ExecutionPolicy Bypass` 调用子套件，属既有写法；本任务不评估它是否必要。

## Version History

- v1 — planning.
