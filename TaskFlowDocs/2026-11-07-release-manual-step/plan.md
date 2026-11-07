# Plan — 发布流程：手工三宿主 catalog 校验
> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

- `RELEASE.md:145-152` — 步骤 6 的完整上下文。
- `hooks/release-check` — 已覆盖的可离线判定部分（`ref`/`sha` 配对与祖先关系）。
- `.claude-plugin/marketplace.json`、`.codebuddy-plugin/marketplace.json` — 仅有的两份 catalog。
- `hooks/smoke-test:6268-6282` — pin 住 `RELEASE.md` 若干句式的断言，改动不得误伤。

## Related Tasks

- `TaskFlowDocs/achieved/` 下无相关任务；`TF-20261029-218fdf`（`$schema` 断言）已交付，本条不重叠。

## Skills / Tools Used

- [PRD] Unaided — 判断依据来自仓库内既有检查与步骤顺序；considered: requirements elicitation
- [Plan] Unaided — 单步文档修改；considered: work breakdown
- [Test] Unaided — 复用既有 smoke 断言，不新增测试机制；considered: testing strategy

## Preconditions

- 本 worktree 在 `chore/release-manual-step` 分支上。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-07 20:09 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 删掉无判据的手工校验，并说明为什么

- Goal: 从 `RELEASE.md` 步骤 6 移除手工三宿主 catalog 校验，改为说明可离线判定部分由 `release-check` 负责、端到端安装是联网抽查而非发布门。
- Dependencies: 无
- Files:
  - `RELEASE.md`
- Implementation checklist:
  - [x] 删除 `RELEASE.md:151` 那句。
  - [x] 在同一段补上替代说明。
- Acceptance: PRD 的全部验收标准。
- Verification: `bash hooks/smoke-test`；`git diff --check`；读回核对步骤 6 语义完整。
- Rollback: `git checkout -- RELEASE.md`
- Status: done

## Checkpoints

- Step 1 后跑本地 smoke 再提交。

## Verification / Review

**改了什么**

`RELEASE.md` 步骤 6 删掉「Validate the catalog entry with Claude Code, Codex, and CodeBuddy tooling」，并在步骤列表之后补两段说明：catalog 的机械正确性由 `release-check` 判定；端到端安装是联网动作、发生在不可逆推送之后，因此不能作为门，若要做应放进 CI。

**为什么删而不是改条件式**

原 Todo 的表述是「make the manual step conditional」。读完上下文后判断：它**没有任何条件可以让它变成有效的门**。步骤 5 已经原子推送了 tag，步骤 6 才开始校验——此时 tag 不可变。失败时能做的只有回滚或发补丁版，而 `RELEASE.md` 的 Rollback 一节明确说移动 tag 需要 owner 授权。一条只能事后告警、失败后无既定响应的步骤，条件化与否都不改变它的性质。

**顺带纠正的事实**

「three-host catalog」不成立：仓库只有两份 catalog（`.claude-plugin/`、`.codebuddy-plugin/`），`.codex-plugin/` 只有 `plugin.json`，Codex 装的是 Claude Code 那份。原句让读者以为存在第三份需要单独校验的东西。

**验证**

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| 目标句已消失 | `grep -c 'Validate the catalog entry' RELEASE.md` | `0` |
| 步骤 6 其余内容完好 | 读回 146–152 行 | 重跑 `release-check`、Release 标题与首行格式、步骤 7 均在 |
| 全量 smoke | `bash hooks/smoke-test` | `ALL SMOKE PASSED`，exit 0 |
| 空白检查 | `git diff --check` | 通过 |

smoke 里 pin 住 `RELEASE.md` 的五条句式断言（`hooks/smoke-test:6273-6281`）未受影响——本次改动不触及它们。

CI 三宿主矩阵在推送后读取。

## Change Log

- v1 — 初始计划；同日完成 Step 1。

## Follow-ups

- 端到端安装验证若要落地，属于 CI 对**已发布 tag** 的动作（`claude plugin install` 等），不是发布清单步骤。未做。

## Version History

- v1 — planning.
