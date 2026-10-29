# Plan — 断言 manifest 的 `$schema` 声明
> Task version: v2
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/release-check:20-31` — 它读的九个文件清单；新检查的判断范围。
- `hooks/release-check:221-226` — `needs=1` → `STATUS: needs-user-input` → 退出 2 的既有约定。
- `hooks/smoke-test:4488` — `== release-check catches version drift and a bad marketplace pin ==`，新用例并入这里。
- `tools/workflow-affected:87-89` — `release=1` 的路径集合；`hooks/*` 不在其中，这就是 R9 的由来。
- `.claude-plugin/marketplace.json:2`、`.claude-plugin/plugin.json:2` — 当前两个声明。

## Related Tasks

- 来源：`TaskFlowDocs/todo.md` 的 `TF-20260928-3910fb`（re-scoped 为 `TF-20261029-218fdf`）。
- 前置已交付：`achieved/2026-09-19-release-flow-exception`（把本条目前半的「三宿主手工校验」前提搬走）。

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — purpose: 把一条前提已过期的 todo 收敛成可验收的需求；outcome: succeeded; incorporated: 去掉已无对象的前半，只做 `$schema` 断言；v2 又删掉了与 R1 互斥的「点名 404」验收项，并把「断言必须能被 CI 执行」写进 R9。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 决定两处改动的先后与验证顺序；outcome: succeeded; incorporated: 先写检查再写用例（用例的期望消息以检查实际打印的为准），变异验证放在最后。
- [Test] `Unaided — no capability applied to this phase; considered: testing strategy` — 断言形态沿用 `hooks/smoke-test:4488` 既有夹具模式，没有引入外部能力；三次变异验证由本任务手工执行。

## Preconditions

- [x] 已读 `CONTRIBUTING.md`（分支/worktree 规则）、`CODE_STYLE.md`（脚本风格）。
- [x] 隔离：工作树 `.worktrees/schema-check`，分支 `chore/schema-check`，基线 `main` @ `ba3d9e7`。
- [x] 已实测：两个声明都 404；6 个候选地址无一可用；现有检查零处读 `schema`；CI 的 `release` job 只在 manifest/CHANGELOG/README 变化时运行。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-29 20:50 +0800
- Approved version: v2
- Approved scope: PRD / Plan

## Steps

### Step 1 — 在 `release-check` 里加 `$schema` 断言

- Goal: 让「声明了但为空 / 不是绝对 HTTPS / 同一文件重复声明 / 声明集合与 pin 不符」四种情况各自报出具体原因。**不检测 URL 是否可达**（R1 不联网，v2 起 A1 也不再要求）。
- Dependencies: 无。
- Files: `hooks/release-check`。
- Implementation checklist:
  - [x] 新增一段，遍历五个 manifest，逐条实现 R2–R5。
  - [x] 每种失败打印自己的消息并置 `needs=1`。
  - [x] 「数量与记录不符」用脚本内硬编码的清单（两个文件 + 各自 URL）+ 注释说明为什么不读外部文件。
  - [x] 不引入任何网络调用。
- Acceptance: PRD v2 的 A1–A6。A1 期望 `STATUS: pass` 退出 0 —— 当前两个声明按本任务的规则是合法的。
- Verification: 手工构造四种坏法各跑一次，确认消息与退出码。
- Rollback: 单段代码，`git revert` 即恢复。
- Status: done

### Step 2 — 把用例并进 `smoke-test:4488` 那一节

- Goal: 让新断言在 CI 里真的被执行，且不被真实仓库的两个 404 拖红。
- Dependencies: Step 1。
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 在既有 `rel` 夹具上加三个 case：无声明 → pass；合法声明 → pass；空值/非 HTTPS → 退出 2 且点名。
  - [x] 复用该节已有写法（`bash "$HERE/release-check" "$rel"` + `grep -q` 消息片段）。
  - [x] 不在真实仓库上调用 `release-check`。
- Acceptance: PRD 的 A9–A11。
- Verification: `bash hooks/smoke-test` → `ALL SMOKE PASSED`。
- Rollback: 删除新增 case。
- Status: done

### Step 3 — 变异验证与文档

- Goal: 证明 Step 2 的用例真的在检测 Step 1 的检查；补 `CHANGELOG.md`。
- Dependencies: Step 1、Step 2。
- Files: `hooks/release-check`（临时破坏，验证后逐字节恢复）、`CHANGELOG.md`。
- Implementation checklist:
  - [x] 依次破坏 R2 空值、R3 非 HTTPS、R4 重复键、R5 数量，每次确认对应用例变红并指名。
  - [x] 每次逐字节恢复，`diff -q` 确认。
  - [x] `CHANGELOG.md` 增一条，说明这是「发现既有问题」而非「预防未来问题」：两个声明今天就 404。
- Acceptance: 四次变异各自红在**对应**的用例上。
- Verification: 四次结果写进 `## Verification / Review`。
- Rollback: 无需。
- Status: done

## Checkpoints

- Step 1 后：`bash hooks/release-check .` 在当前仓库返回退出 2 并点名两个 404 声明。
- Step 2 后：`bash hooks/smoke-test` → `ALL SMOKE PASSED`。
- Step 3 后：四次变异各自红在对应用例，恢复后再次全绿。

## Verification / Review

- 2026-10-29 Step 3: Four mutations each reddened its own case; restored byte-identically

- 2026-10-29 Step 2: Six schema cases added to the existing release-check fixture section

- 2026-10-29 Step 1: release-check reports pass on the real repo; four format rules implemented

### 实测（2026-10-29）

| 检查 | 结果 |
|---|---|
| `bash hooks/release-check .`（真实仓库） | `STATUS: pass`，退出 0。符合 PRD v2 的 A1：两个声明都非空、都是绝对 HTTPS、无重复键、都在 pin 清单里。 |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` |
| `git diff --check` | 干净（见收尾） |

### 变异验证（四次，各自红在对应用例）

| 变异 | smoke 输出 |
|---|---|
| 删掉空值分支 | `FAIL empty $schema accepted` |
| 去掉 https 判定 | `FAIL non-https $schema accepted: http://example.invalid/x.schema.json` |
| 不数重复键 | `FAIL duplicate $schema accepted` |
| 不执行 pin | `FAIL a pinned declaration was dropped silently` |
| 逐字节恢复后 | `ALL SMOKE PASSED`，`diff -q` 一致 |

### 实现过程中被自己抓到的一个缺陷

第一版用提取出的值判断「有没有声明」（`[ "$count" -eq 0 ] && continue`），于是 `"$schema": ""` 在空值检查之前就被当成「没有声明」跳过了——**空值这个用例本身永远不会红**。改成先 `grep -q` 键是否存在、再分别报「空字符串」与「非字符串值」（`null`、数字），两次消息不同，因为它们是两个不同的错误。

### 与 v1 的差别

v1 的 A1 要求点名两个 404，与 R1（不联网）互斥，实测时表现为 `release-check` 退出 0 而 A1 要求 2。v2 已改（见 `old/v1/version.md`）。**后果**：本任务合并后两个 404 依然不会被任何自动化发现，只记在 Follow-ups 里。

## Change Log

- 2026-10-29 — Step 1–3 完成：`hooks/release-check` 新增 `$schema` 段（值/pin/重复/协议四项），`hooks/smoke-test` 在既有 release-check 夹具段新增一整节六个用例，`CHANGELOG.md` 记两条。四次变异各自红在对应断言。
- 2026-10-29 — v1 → v2：R1（不联网）与 A1（点名两个 404）矛盾，离线断言无法判定可达性。A1 改为只断言声明合法性，期望 `pass`；404 移入 Follow-ups。原因记录在 `old/v1/version.md`。

## Follow-ups

- **修那两个 404 URL。** 本任务只加断言不改 URL（用户 2026-10-29 裁定）。
- **另外三个 manifest 是否需要 `$schema`。** `.codebuddy-plugin/*`、`.codex-plugin/plugin.json`、`package.json` 都不声明；查明是「本来就没有」还是「漏了」后再定 R5 的正确形态。
- **`release-check` 在 CI 里只在 manifest 变化时运行。** 本任务通过 smoke 让它每次改 hook 都跑；若将来两者解耦，这条路会断，届时要回到 `tools/workflow-affected`。

## Version History

- v1 — planning.
