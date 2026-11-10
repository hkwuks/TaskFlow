# Plan — 发布流程：手工三宿主 catalog 校验
> Task version: v1
> Status: completed

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

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- 2026-09-30 互链：`TF-20260930-c4e4c8` 提出「发布不重跑 CI 已覆盖的测试」，与本条「把手工三宿主 catalog 校验改条件式」同属一条主线——都是砍掉发布流程里 CI 覆盖不到的判断之外的重复劳动。两条宜一并 promote、一并改 `RELEASE.md`。
- 2026-10-10 前提复核（本条部分过期）：(1) 前半「三宿主手工 catalog 校验改条件式」的**前提已被 TF-20260919-40eca2 搬走**——RELEASE.md 不再有「Validate the catalog entry with Claude Code, Codex, and CodeBuddy tooling」这一段手工步骤（现 RELEASE.md 的发布检查只列 repository-check / release-check / quick_validate / diff --check 四条），所以「改条件式」已无对象。(2) 后半「自动 $schema 断言」**仍未做**：`hooks/release-check`、`hooks/smoke-test`、RELEASE.md、两份 marketplace catalog 里 `schema` 零命中，`$schema` 字段目前无任何机器校验。(3) 相邻已交付条目 TF-20260930-c4e4c8 也来自同一主线（砍掉发布流程里 CI 覆盖不到的重复劳动），其落点同样在 RELEASE.md。故本条收窄为「给两份 catalog 的 $schema 加自动断言」后再 promote。
- 2026-11-01 上述 (1) 与 (2) 都已不成立，本条只剩一半：(1) 是错的——`RELEASE.md:135-136` 那段手工步骤**从来没有被删过**，`git log -S'CodeBuddy tooling' -- RELEASE.md` 只有 `4e497c3` 一次命中，且是新增。当时把「验证清单里那四条」误读成「整份 RELEASE.md 只剩这四条」，两者不在同一节。所以「改条件式」仍有对象，前提没被搬走。(2) 的 `$schema` 断言已作为 `TF-20261029-218fdf` 交付归档，两个 404 URL 也在 2026-11-01 换成了 schemastore.org 的可用 schema。本条因此收窄为前半，Next action 已相应改写。
