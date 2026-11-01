# Plan — 外部事实：先判断，再取证
> Task version: v2
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/capability-evidence:44-52` — 谓词边界；新 hook 要复用它的定位逻辑但**不共享它的取值范围**。
- `hooks/hooks.json` — `PostToolUse` 现有两条接线，新的一条加在其后。
- `hooks/task:1396-1460` — v1 写的 `## External Facts` 校验；R3/R4 在 `yes` 分支上扩展。
- `hooks/smoke-test:1877` — approve 夹具；隔离断言 A3 加在这里。
- `skills/taskflow/SKILL.md:54`、`:204`、`:217`、`:246` — 三处停顿点的落点。
- `skills/taskflow/references/runtime.md:44-51` — 事件表，新行加在此。

## Related Tasks

- 来源：`TaskFlowDocs/todo.md` 的 `TF-20261031-61b973`（v1 `TF-20261027-e8c6dc` 重述后重定界）。
- 上游测量：`TF-20260919-90797c`（不合并，见 PRD Out of Scope）。
- 形态参照：`achieved/2026-10-29-midturn-presence/`（`PostToolUse` 能不能向模型说话，那次已测）。
- **v1 已实现的部分**（PR #108，未合并）：`## External Facts` 字段、`approve` 的四类拒绝、`promote` 骨架、9 条 smoke 断言。v2 在其上扩展，不重做。

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — purpose: 把「记录判断」重写成「矫正倾向」这个新承诺，并划清与 R12 的边界；outcome: succeeded; incorporated: 三处停顿点 + 两套存储的隔离判据（A3 的反向证明），以及「无外部证据则拦」只在 `yes` 分支触发的剩余漏洞写明而非掩盖。
- [PRD] `get-api-docs` — purpose: 查 `PostToolUse` 是否为 `WebSearch`/`WebFetch` 投递事件，这是 R2 能否成立的前提；outcome: succeeded; incorporated: 官方文档写明匹配值同 `PreToolUse` 且明确列出这两个工具，`WebSearch.tool_input` 的字段为 `query`/`allowed_domains`/`blocked_domains`（见 PRD 的 `## External Facts`）。
- [Plan] Unaided — no capability applied to this phase; considered: work breakdown and task decomposition
- [Test] `Unaided — no capability applied to this phase; considered: testing strategy` — 断言形态沿用既有夹具，未引入外部能力。

## Preconditions

- [x] 已读 `CONTRIBUTING.md`、`CODE_STYLE.md`、`artifacts.md`。
- [x] 隔离：工作树 `.worktrees/external-facts`，分支 `feat/external-facts`，v1 的提交 `96044df` 已在其中，未合并（PR #108 保持 open）。
- [x] **宿主事实已查官方文档**（2026-11-01，非记忆）：`PostToolUse` 匹配值同 `PreToolUse`，后者明确列出 `WebFetch`/`WebSearch`；`WebSearch.tool_input` 有 `query`/`allowed_domains`/`blocked_domains`。
- [x] 已确认 `hooks/summarize-state` 与 `prompt-reminder` 的现有输出形状，三处停顿点落点明确。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-01 20:09 +0800
- Approved version: v2
- Approved scope: PRD / Plan

## Steps

### Step 1 — 外部证据存储与记录器

- Goal: 让 `WebSearch`/`WebFetch` 成为可观察事件，且与能力证据**在代码上就不共用一条路径**。
- Dependencies: 无。
- Files: `hooks/external-evidence`（新建）、`hooks/hooks.json`、`hooks/README.md`（钩子清单，仓库规则要求每个 hook 在两处出现）。
- Implementation checklist:
  - [x] 新建 `hooks/external-evidence`，extensionless bash，读 `hook_event_name tool_name cwd tool_input.query tool_input.url`。
  - [x] 谓词只有 `WebSearch|WebFetch` 两个值 —— **不 import、不 fall through 到 `capability-evidence` 的任何分支**。
  - [x] 写到 `<absolute-git-dir>/taskflow/external`，行格式 `search|<query>` 或 `fetch|<url>`，字段里的 `|`/换行按 `capability-evidence:83` 同样方式清洗。
  - [x] 在 `hooks/smoke-test` 之外的位置也复述存储路径：`task approve` 读它，所以路径常量必须一致（写进注释并让 Step 2 引用）。
  - [x] `hooks.json` 加 `PostToolUse` matcher `WebSearch|WebFetch`。
  - [x] `hooks/README.md` 的清单加一行。
- Acceptance: PRD 的 A1、A2。
- Verification: 喂两个真实形状的事件 JSON，检查 `external` 文件内容；喂 `Bash` 事件，确认不写。
- Rollback: 删新文件 + 去掉接线两行。
- Status: done

### Step 2 — `approve` 消费外部证据，且证明它不能顶替能力记录

- Goal: `yes` 的 `- Source:` 必须有检索记录背书；同时 A3 反向证明隔离成立。
- Dependencies: Step 1（存储与字段格式）。
- Files: `hooks/task`、`hooks/smoke-test`。
- Implementation checklist:
  - [x] 在 v1 的 `yes` 分支里，逐条 `- Source:` 去 `taskflow/external` 找匹配记录（域名包含，或 query 包含该 URL 的 host）。找到记为有据；找不到收集起来。
  - [x] 有任何一条没找到 → `fail`，消息点名是哪一条，并说明「声明依赖外部事实，但本任务版本没有任何检索记录」。
  - [x] `no` 分支：理由必须含一个仓库内可指认的东西（反引号路径，或 `path:line` 形态）——判据写死成可检查的形状，不用自然语言判断。
  - [x] **A3 的反向断言先写**：一个只有 `external` 记录、`released` 为空的夹具，`approve` 必须仍以 `stage [PRD] was never released` 拒绝。这条在 Step 1 之后就能写，先让它红着，Step 2 完成后确认它仍红（证明隔离），然后固化。
  - [x] 记录读取失败（文件不存在、行损坏）一律按「没有记录」处理并拒绝，不 fail-open。
- Acceptance: PRD 的 A3、A4、A5、A6。
- Verification: 四类夹具各跑一次；A3 在 Step 1 前后各跑一次，两次都必须拒绝且理由不同。
- Rollback: 单段代码，`git revert`。
- Status: done

### Step 3 — 三处停顿点与文档

- Goal: 让「答案在仓库外吗」这个问题在它可能被推翻的三个时刻各出现一次，并把存储写进文档。
- Dependencies: Step 1、Step 2。
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`skills/taskflow/references/runtime.md`、`CHANGELOG.md`、`hooks/smoke-test`。
- Implementation checklist:
  - [x] Phase 1 收敛段（`SKILL.md:217` 附近）加一句可执行的问句，并说明答 `yes` 时要去检索、检索会被记录。
  - [x] Phase 3 决定 Spec 之前加同一问句的复查形态（「Phase 1 答过的那次判断，在定义契约时还成立吗」）。
  - [x] Plan 定稿前加第三次复查，与 `## Approval` 相邻。
  - [x] **`SKILL.md:54` 的 `inspect` 八项不动。**
  - [x] `artifacts.md` 补 `taskflow/external` 的路径、行格式、它与 `evidence` 的区别（一句话：一个释放 stage，一个证明查过）。
  - [x] `runtime.md` 事件表加一行：`External-evidence capture (never releases a stage)`。
  - [x] `CHANGELOG.md` 在 v1 那条之外补 v2 的说明，**明确写v1 的局限**（记录判断但不改变行为）。
  - [x] smoke 断言：三处问句存在于 SKILL.md（各一条具名断言），`inspect` 八项仍完整。
- Acceptance: PRD 的 A7、A8。
- Verification: `bash hooks/smoke-test` → `ALL SMOKE PASSED`；变异破坏每一处问句与每一条 approve 分支，各自红在对应用例。
- Rollback: 文档改动 `git revert`。
- Status: done

## Checkpoints

- Step 1 后：两个真实形状的事件各写一行，`Bash` 事件不写；`external` 与 `evidence` 是两个文件。
- Step 2 后：A3 三次都拒（Step 1 前、Step 1 后、Step 2 后），A4/A6 各拒，A5 过。
- Step 3 后：`ALL SMOKE PASSED`；变异各自红在具名用例上。

## Verification / Review

### 实测（2026-11-01，v2）

| 检查 | 结果 |
|---|---|
| `bash hooks/smoke-test` | `ALL SMOKE PASSED`（新增 external capture、隔离、yes/no 背书、三处停顿点共约 20 条断言） |
| `bash hooks/release-check .` | `STATUS: pass` |
| `bash -n` 全部改动脚本 | 通过 |
| `git diff --check` | clean |
| `hooks/task` / `skills/taskflow/SKILL.md` 变异后恢复 | 逐字节（`diff -q`） |

### 变异验证

| 变异 | 红在哪 |
|---|---|
| `approve` 不查 `- Source:` 是否有检索记录 | `FAIL the unbacked source was not named` |
| 有未背书来源时不 fail | `FAIL the unbacked source was not named` |
| `no` 不检查理由是否指向仓库内 | `FAIL external facts message for no reason names nothing` |
| `inspect` 枚举加第 8 项（真正的第 54 行） | `FAIL the inspect enumeration changed size` |
| `inspect` 枚举加项（错改到 frontmatter 第 3 行） | 未变红 —— **变异打错位置**，断言本身是对的 |

### 实现过程中被抓到的三个缺陷

**一、`|` 会伪造字段边界。** 第一版只 `tr -d '\r\n'`，`a|b` 记成 `search|a|b` —— 一个记录里多了一个分隔符。断言比对整行而不只是行数才抓到。第二版对整个 record 跑 `tr`，把分隔符本身也换成了空格，每条记录变成 `search claude code hooks`。第三版改成只清洗分隔符之后的值。

**二、A3 夹具搞坏了共享 store。** 隔离断言第一次写在共享 store 上，而前面的用例已经把它推到 `released` 4 / `evidence` 0，`approve` 因 store 不一致拒绝 —— 理由不是我要测的那个。改用独立 worktree 后才测到真正的理由。

**三、`inspect` 断言的变异打错了位置。** `tests, configuration` 在 `SKILL.md` 出现两次（frontmatter 与第 54 行），我用字符串替换改中了前者，smoke 通过，我一度以为断言没在测东西。真正改第 54 行后它立刻变红。**教训：变异没变红时，先确认变异落到了要测的那一处。**

### 一个仍未消除的漏洞

`no` 是绕得过这一整套的：R4 的拦截只在 `yes` 分支触发。理由必须指向仓库内某处，但那只是把撒谎的成本抬高一点。要彻底堵死就得要求每个任务都产出外部证据，而那会让大多数内部任务造假。本任务选择写明它，而不是用一条让所有任务说谎的规则去堵（PRD Risks 第 1 条）。

## Change Log

- 2026-11-01 — v1 归档至 `old/v1/`。用户重述问题为「模型倾向于不搜索」，v1 的字段记录判断但不改变行为。v2 改变承诺：加三处停顿点、接 `WebSearch`/`WebFetch` 为可见事件（与能力证据隔离）、`yes` 无检索记录则拦。

## Follow-ups

- **落地后核对 `PostToolUse` 对 `WebSearch` 的真实投递形态。** 本版本依据官方文档的匹配说明，未在真实会话中观测过。第一次真实使用时看 `taskflow/external` 是否有行；没有则说明匹配值不同，需要按实际返回值修正（写进 `runtime.md` 的「documented, not yet measured」一栏）。
- **`no` 仍是可被铁了心的模型利用的漏洞。** 见 PRD Risks 第 1 条。若将来发现 `no` 占比接近 100% 且理由雷同，再考虑更强的手段。
- **外部证据存储无限增长**，同 `taskflow/evidence`，先不处理。
- **`TF-20260919-90797c` 的对照测量仍然悬空**，本任务按用户 2026-10-31 裁定不合并。

## Version History

- v1 — 交付可检查的 `## External Facts` 字段；已实现（PR #108），未合并。
- v2 — 用户 2026-11-01 重述：要解决的是倾向，不是记录。加停顿点、接检索事件、无证据则拦。
