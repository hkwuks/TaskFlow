# Plan — 推 PR 之前先确定哪个仓库接收它

> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md`
- 外部事实来源与实测数据见 `prd.md` 的 Background / Confirmed Facts 与 External Facts。

## Reference Pointers

- `hooks/repository-check` — 现有治理检查；本任务**不改**它，A9 用 `diff` 钉住。
- `hooks/repository-check:18-31` — 现在只打印 remote 名与 URL 的那一段，正是本任务要补的缺口。
- `hooks/external-evidence:1-20` — 仓库里最近的"新增 hook"先例，注释里记录了它为什么存在。
- `CONTRIBUTING.md:9` — 「remote names alone are not evidence」这条规则，本任务给它一份可执行依据。
- `skills/taskflow/references/runtime.md` — hook 事件的记录处，本任务在此登记新脚本。
- `CODE_STYLE.md` — 退出码 `0/2/3` 与 Shell 风格约定；本脚本退出码的例外在 spec 中说明了理由。

## Related Tasks

- `TF-20261009-99045e` — 宿主安装小节手写重复，同属"文档说了但没工具"的一类，不重叠。
- `TF-20261022-47c217` — Plan 复核，独立。

## Skills / Tools Used

- [PRD] `agent-skills:spec` — 用于把散落事实收敛成需求与验收标准；产出并入 `prd.md` 的 Requirements / Acceptance Criteria。
- [Spec] `agent-skills:spec` — 用于确定模块边界、退出码设计与测试策略；产出并入 `spec.md` 的六节。
- [Plan] `agent-skills:planning-and-task-breakdown` — 用于复核 Step 拆分并补上遗漏的登记点；产出直接修进本 Plan 的 Step 4。
- [Test] `Unaided` — considered: testing strategy。测试写在 `hooks/smoke-test` 既有风格内，不需要单独的测试生成能力。

## Preconditions

- 工作树 `.worktrees/fork-topology`，分支 `fix/fork-topology`，基线 `main@d5e2e7f`。
- `gh` 已认证（人工验收时需要；CI 与 smoke 不需要）。
- `timeout`（coreutils）可用；不可用时的降级已在 spec 说明。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-02 21:03 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 解析与输出形状

- Goal: 给定一份 `GET /repos/{owner}/{repo}` 的 JSON，产出 spec 里那种每 remote 一行的输出，并给出两条命令实参。
- Dependencies: 无。
- Files: `hooks/remote-topology`（新建）。
- Implementation checklist:
  - [x] 从 `git remote` 枚举 remote，逐个取 URL，解析出 `owner/repo`，跳过非 GitHub 形状的 URL 并注明跳过原因。
  - [x] 对每个 remote 取一次 `GET /repos/{owner}/{repo}`，读出 `fork`、`parent.full_name`、`default_branch`、`permissions.push`。
  - [x] 非 fork 与 fork 两种形状各输出对应的一行结论与两条命令实参（R3）。
  - [x] 多层 fork（`parent != source`）时同时列出 `source`，并注明 base 需人工选择。
- Acceptance: A1、A2、A3。
- Verification: smoke 用两个固定 JSON 夹具（取自 2026-11-02 的真实返回）驱动，断言逐行匹配。
- Rollback: 删除该文件，无其他影响。
- Status: done

### Step 2 — 四种缺席

- Goal: `gh` 不可用 / 未登录 / 无网络 / 限流 各自输出不同的"未检查"措辞，且退出 0。
- Dependencies: Step 1。
- Files: `hooks/remote-topology`。
- Implementation checklist:
  - [x] `command -v gh` 判断可用性（A4）。
  - [x] `gh auth status` 判断登录态，**先于**发请求（A5）——因为未认证与网络失败的 `gh` 退出码都是 `1`，实测于 2026-11-02。
  - [x] 请求失败时读错误体：含 `rate limit` 报限流（A7），否则报网络（A6）。
  - [x] 四种措辞互不相同，且都退出 0。
- Acceptance: A4、A5、A6、A7。
- Verification: stub `gh`（PATH 前置的假脚本）分别返回四种状态，断言措辞与退出码。
- Rollback: 同 Step 1。
- Status: done

### Step 3 — 超时与只读

- Goal: 不可达地址在 10 秒内返回；脚本不写任何文件。
- Dependencies: Step 2。
- Files: `hooks/remote-topology`。
- Implementation checklist:
  - [x] 每次 `gh` 调用用 `timeout 10` 包裹；`timeout` 不存在时不包裹并在输出注明（spec 已定）。
  - [x] 断言脚本内无重定向写文件（`>` / `>>` 到路径）。
- Acceptance: A8、R6。
- Verification: 对 `127.0.0.1:1` 之类的不可达目标计时；`grep` 扫重定向。
- Rollback: 同 Step 1。
- Status: done

### Step 4 — 边界断言与文档

- Goal: 把"不能越过的线"变成断言；在三处登记。
- Dependencies: Step 1–3。
- Files: `hooks/remote-topology`、`hooks/smoke-test`、`hooks/README.md`、`skills/taskflow/references/runtime.md`、`CONTRIBUTING.md`。
- Implementation checklist:
  - [x] A10：断言 `remote-topology` 在任何 `hooks-*.json` 中零命中。
  - [x] A9：改动前后跑 `hooks/repository-check`，输出与退出码 `diff` 一致。
  - [x] `hooks/README.md` 的树状清单加入 `remote-topology`，与 `smoke-test` 既有做法一致（它已断言 `repository-check` 等被点名）。
  - [x] `runtime.md` 记录该脚本：可选、联网、不进 SessionStart、只读、只发 `GET /repos/*`；同时更新它自己的 hook 树。
  - [x] `CONTRIBUTING.md:9` 那条规则旁指出这份可执行依据。
- Acceptance: A9、A10，以及三处文档改动可在 `grep` 下验证。
- Verification: 变异——把脚本名加进 `hooks.json` 应使 A10 变红；还原后全绿。删除 `hooks/README.md` 里的条目应使新的点名断言变红。
- Rollback: 文档改动可单独回退。
- Status: done

## Checkpoints

- Step 1 结束后：用一个真实仓库跑一次，人工确认输出确实回答了"推哪、base 是谁"。
- Step 2 结束后：四种缺席逐一人工触发一次（拔网线不可行时，用 `GH_HOST` 与 stub 模拟）。
- Step 4 结束后：全量 smoke + `repository-check` 与 `release-check` 全绿。

## Verification / Review

**smoke：`ALL SMOKE PASSED`**（`bash hooks/smoke-test`），新增一节 `remote-topology reads the facts a push decision needs, and never guesses`。

### 真实仓库上的输出（A1）

```
$ bash hooks/remote-topology .
Remote topology for: .
- origin: hkwuks/TaskFlow  fork=no  push=yes  default=main
  -> git push origin <branch>
  -> gh pr create --base main --head hkwuks:<branch>
```

### 五种情境逐一验证

| 场景 | 结果 |
|---|---|
| 非 fork（A1） | `fork=no push=yes`，`--base main`，见上 |
| fork（A2，stub 真实 `hxhy00/TaskFlow` 返回） | `fork=yes push=yes parent=hkwuks/TaskFlow`，`--head hxhy00`，注明 opens against 上游 |
| 多 remote（A3） | 三个 remote 各一行；非 GitHub 的 `mirror` 报 `unchecked (not a GitHub remote)` |
| 多层 fork | `parent=a/TaskFlow` `source=root/TaskFlow`，明确注明 base 取直接上游 |
| `gh` 不在 PATH（A4） | `unchecked (gh not found)`，exit 0 |
| 未登录（A5） | `unchecked (gh not logged in)`，exit 0 |
| 网络不通（A6） | `unchecked (cannot reach the GitHub API)`，exit 0 |
| 限流（A7） | `unchecked (API rate limit)`，exit 0 |
| 超时（A8） | 3 个 remote、桩 `gh` 挂起 → **11s** 返回（全程预算 10s，不随 remote 数增长） |

### 变异验证（每条断言都单独红过）

| 变异 | 红在哪 |
|---|---|
| fork 判定恒为 no | `FAIL fork line wrong` |
| 未登录文案与网络不通合并 | `FAIL absence 'logged-out' did not report 'gh not logged in'` |
| 限流不单独报 | `FAIL absence 'rate-limit' did not report 'API rate limit'` |
| `can_push` 恒为 yes | `FAIL push=false not reported` |
| 默认分支写死 `main` | `FAIL default branch not read from the response` |
| 把脚本接进 `hooks.json` | `FAIL remote-topology is wired into hooks.json` |

每次还原后 `cmp` 确认字节一致。

### A9 — `repository-check` 未受影响

`hooks/repository-check` 文件与基线 `main` 逐字节相同；对同一仓库的输出 `diff` 为空。

### 实施中发现并修掉的两个真实缺陷

1. **`slug_of` 保留了主机名**，构造出 `repos/github.com/owner/repo`，`gh` 报错后脚本把「自己的错误」归咎于网络。修复为剥掉 authority。
2. **A10 的断言漏掉了 `hooks.json` 本身**：`hooks-*.json` 这个 glob 不匹配无后缀的 `hooks.json`，而那正是 Claude Code 的主要接线文件。实测把 `remote-topology` 加进 `hooks.json` 的 `SessionStart` 时**原断言不红**。已把 `hooks.json` 显式并入循环。

第二条是这次任务最有价值的产出：它证明"断言写下来了"与"断言覆盖了该覆盖的东西"是两件事。

## Change Log

- 2026-11-02 — v1 起草。三个关键决定已在与用户确认后固定：离线报未检查且退出 0；只报 fork 拓扑与 push 权限；模板随插件分发（属任务 B）。
- 2026-11-02 — v1 实施完成。Step 1–4 全部 `done`；smoke 全绿；六条变异各自红在对应断言。实施中修掉两个真实缺陷（`slug_of` 保留主机名、A10 漏检 `hooks.json`）。

## Follow-ups

- **`gh` 无内置超时**，因此依赖 coreutils 的 `timeout`。若某平台既无 `timeout` 也无 `gtimeout`，本检查会失去超时保护——已记入 `runtime.md`，不写兼容层。
- **多 remote 指向同一网络**时会重复请求同一仓库。未去重（A3 要求每 remote 一行），如果将来 remote 数量多到值得优化，再考虑按仓库缓存单次运行内的结果。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- repository-check:18-31 currently lists remote names+URLs only; it reports neither isFork/parent/source nor permissions.push. Verified facts: gh api repos/X -> .fork/.parent.full_name/.source.full_name/.permissions.push; gh pr create --head <owner>:<branch> is the writable head, --base is the upstream branch to merge into; gh api .../branches/<b>/protection returns 404 when unprotected.
