# Plan — Publish TaskFlow v1.0.7

> Task version: v1
> Status: in_progress

No spec required — 一次版本字面量发布，无跨层契约。

`RELEASE.md` 是程序本身。本 Plan 按它的阶段分两步，**指章节而不抄命令**（`references/artifacts.md` 的「Release task documents」一节：抄一份会漂移的第二副本）。

## Reference Pointers

- `RELEASE.md` —— `## Before release`、`## Validation checklist`、`## Tag, catalog pin, and GitHub Release`（第 1–7 步）、`## Rollback`。
- `hooks/release-check` —— 版本字面量的判定者；它**刻意**不把 pin 与版本字面量互相比较，所以准备下一版期间 pin 仍指 `v1.0.6` 不会失败。
- `TaskFlowDocs/achieved/2026-09-17-release-v1-0-6/` —— 上一版的记录；`f8e13a0`（元数据提交）与 `42edb18`（pin 提交，只含四个字面量）是先例。
- `CHANGELOG.md` 的 `[1.0.6]` 段 —— 新版四节结构照它写。

## Related Tasks

- Related: `achieved/2026-09-17-release-v1-0-6/`（上一版）、`achieved/2026-09-15-release-friction/`（建立 `release-check` 与发布文档规则）、`achieved/2026-09-13-revise-release-flow/`（确立直接打标签为默认路径）。
- 本版内容来自 `achieved/2026-09-18-conflict-side-review/`、`achieved/2026-09-18-todo-field-writes/` 与 PR #36/#37/#38/#39。

## Skills / Tools Used

- **Unaided** —— 全程未调用外部能力。发布范围由 `git log v1.0.6..main` 与 `git show --stat` 逐提交核对；字面量一致性由仓库自带的 `hooks/release-check` 判定；CHANGELOG 结构照 `[1.0.6]` 段。无外部资料、无 LLM 判定工具。
- 版本号 `1.0.7` 不是本任务推断的：仓库无 semver 政策文档，号由用户指定。

## Preconditions

- [x] Todo 条目 `TF-20260918-985164` 已 promote 为本任务。
- [x] `bash hooks/repository-check .` → `STATUS: pass`。
- [x] `RELEASE.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`、`.github/pull_request_template.md` 已读。
- [x] 发布范围已核对：`v1.0.6` 是 `origin/main` 的祖先，`main` = `cb173cf` 且与 `origin/main` 同步。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-19 00:13 +08:00
- Approved version: v1
- Approved scope: PRD / Plan
- Note: Step 3（标签、pin、GitHub Release）另需一次明确授权——本次批准覆盖 Step 1–2 与推送前的准备，不覆盖不可逆的远端动作。

## Steps

### Step 1 — Release metadata

- Goal: 版本字面量与 CHANGELOG 就位，提交落在 `main`。
- Dependencies: 无。
- Files: 三个 `. *-plugin/plugin.json`、`CHANGELOG.md`、两份 `README.md`。
- Implementation checklist:
  - [ ] 按 `RELEASE.md` 的 `## Release scope` 移字面量；cachebuster 形状 `<release>+<host>.<yyyymmdd>` 不变。
  - [ ] `CHANGELOG.md` 写 `## [1.0.7]`，四节照 `[1.0.6]`；**Fixed 必须把执行位那条写成升级理由**（R5）。
  - [ ] README 的四处示例用字面量替换，不用正则批量改。
  - [ ] 提交直接落 `main`（不切分支），提交信息对齐 `f8e13a0`；显式按路径 add，不用 `git add -A`（drvfs 会带上 filemode）。
  - [ ] 推送 `main`。
- Acceptance: `bash hooks/release-check .` → `pass`；`origin/main` 的该提交同时含三个 `1.0.7` manifest 与新的 CHANGELOG 段。
- Verification: 见 `## Verification / Review`。
- Rollback: `git revert` 该提交（未打标签前无外部可见影响）。
- Status: pending

### Step 2 — 跑 Validation checklist

- Goal: `RELEASE.md` 的清单每条都有实际输出。
- Dependencies: Step 1。
- Files: 无。
- Implementation checklist:
  - [ ] 按 `RELEASE.md` 的 `## Validation checklist` 逐条跑，结果记入 `## Verification / Review`。
  - [ ] 记录 `git rev-parse origin/main` 作为候选标签提交。
  - [ ] 未跑到的项标注未跑，不声称通过。
- Acceptance: 每条都有输出记录。
- Verification: 本节即为验证。
- Rollback: 不适用。
- Status: pending

### Step 3 — Tag, catalog pin, Release（需授权）

- Goal: 按 `RELEASE.md` 的 `## Tag, catalog pin, and GitHub Release` 第 1–7 步完成。
- Dependencies: Step 2，**以及用户的明确授权**。
- Files: `.claude-plugin/marketplace.json`、`.codebuddy-plugin/marketplace.json`（该次提交只含四个字面量）。
- Implementation checklist:
  - [ ] 先把候选提交 SHA、pin 将改的四个字面量、以及两条不可逆命令报给用户，**停在授权前**。
  - [ ] 授权后：注解标签 → pin 提交 → `git push --atomic origin main refs/tags/v1.0.7`；被拒则按 `RELEASE.md` 的退路执行并记录窗口。
  - [ ] 推送后重跑 `bash hooks/release-check .`；建 GitHub Release，正文取自 `[1.0.7]` 段。
  - [ ] 记录标签对象 SHA、Release URL、两个 pin 到本 Plan。
- Acceptance: `git ls-remote --tags` 可见 `v1.0.7`；`release-check` pass；Release 正文与 CHANGELOG 一致。
- Verification: 见 `## Verification / Review`。
- Rollback: `RELEASE.md` 的 `## Rollback`。
- Status: pending

## Checkpoints

- Step 1 后：`bash hooks/release-check .` → `pass`。
- Step 2 后：清单每条有输出。
- Step 3 前：用户授权已记录；授权之前无任何远端标签。

## Verification / Review

（实施后填写实际命令与输出。）

## Change Log

- 2026-09-18 由 `TF-20260918-985164` 提升。
- 2026-09-18 **工作修订（文档瘦身 + 去掉自加的分支）**：初稿 Plan 把 `RELEASE.md` 的清单抄成 5 个 Step、157 行，并自加了一条 `chore/release-v1-0-7` 分支。两处都背离既有决定：
  - `skills/taskflow/references/artifacts.md:115-121`（由 `achieved/2026-09-15-release-friction/` 确立）规定发布任务**记录决策与结果、不重述程序**，Plan 应「每个 `RELEASE.md` 阶段一个 Step，指章节而非重复命令」。初稿正好是要防的第二副本，且 157 行是本仓库最重的发布 Plan（v1.0.4 77 行、v1.0.5 101 行、v1.0.6 141 行）。
  - `RELEASE.md` 与 `achieved/2026-09-13-revise-release-flow/` 已规定**直接打标签是默认路径**，Release PR 是可选路径。用户 2026-09-18 指出 `obra/superpowers`、`addyosmani/agent-skills`、`QuantumNous/new-api` 均不切分支，并否决该分支。
  - 核对后确认：**两提交是设计代价**（catalog 的 `sha` 依赖标签存在，Claude Code 逐字符校验并按 commit 克隆），而**分支是自加的**——superpowers 用 `"source": "./"` 且无 `ref`/`sha`，所以它一次提交即可发完。
  - 据此重写 PRD 与 Plan：Step 收敛为「metadata → Validation → tag/pin/Release（需授权）」三步，程序一律指 `RELEASE.md` 章节。任务本身保留——`RELEASE.md:18` 要求创建发布任务，`artifacts.md:121` 明确保留 `## Approval` 与归档。属工作修订：目标、范围、验收未变，故保持 v1。

## Follow-ups

- `.codebuddy-plugin/marketplace.json` 的 `"version": "1.0.5"` 是没人校验的滞后字面量。方向：纳入 `release-check` 并同步维护，或从 catalog 去掉——留一个没人校验的版本字段比没有更糟。
- inbox 五条（`172455`、`88e04c`、`e7c041`、`9acf57`、`454ac4`）是下一版内容；`e7c041`（`complete` 事务原子性）与 `9acf57`（`task get` 静默漏行）都在 `hooks/task`，适合一次做完。
- `hooks/README.md` 尚未提到 `task next` / `task get`。属插件内容变更，需单独任务。

## Version History

- v1 — planning；含 2026-09-18 的工作修订（见 Change Log）。
