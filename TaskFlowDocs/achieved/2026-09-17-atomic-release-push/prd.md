# Atomic release push
> Task version: v1
> Status: completed

## Goal

让一次发布里「标签已存在」与「catalog 已指向该标签」在远端同时成立：pin 提交与注解标签放进同一次 `git push --atomic`，消除 v1.0.6 实际出现的那种窗口——`/plugin marketplace update taskflow` 在 pin 合入前刷新，安装评到的是旧版本 `v1.0.5`。

## Background / Confirmed Facts

- `RELEASE.md` 的 `## Tag and GitHub Release` 把发布定为两个提交（第 3–6 步，64–69 行说明理由）：标签不能在发布提交之前、`sha` 不能在标签之前。这个顺序约束是真的，不可绕开。
- **但窗口不是这个约束带来的，是「pin 走 PR」带来的。** 标签必须在 pin 可见之前存在；两者可以同一次 push 出去，只要两个 ref 都由本地控制。
- 本仓库已经实测过这个窗口：`/plugin marketplace update taskflow` → `80d35cf` → 评到 1.0.6；同一命令在 04:36 合并 pin 之前刷新则评到 v1.0.5。窗口长度 = pin 合入 `main` 所需时间（PR #34 约 5 分钟）。
- **远端支持原子推送**：`git push --atomic --dry-run origin main refs/tags/v1.0.6` → exit 0。这是本策略可行的前提，已实测而非假定。
- **本仓库三种做法都有过先例，但没有规则**：v1.0.4 的 pin 走 PR #15（`6acbde2`，双亲）；v1.0.5 的 pin 直推 `main`（`c9a91e3`，单亲）；v1.0.6 的 pin 走 PR #34（`80d35cf`）。`RELEASE.md` 第 6 步只规定*什么时候*改 catalog，没规定这 4 行*怎么合进 main*。
- **历史归档提交同样是直推 `main` 的单亲提交**（`440470b`、`4d260a7`、`17fb272`），所以「机械性改动直推 `main`」在本仓库不是新做法。
- **pin 的四行由标签机械决定**，没有可审的内容：`ref` = 标签名、`sha` = `git rev-parse <tag>^{commit}`。其正确性由 `git merge-base --is-ancestor` 与 `hooks/release-check` 强制，不依赖人工阅读。
- **官方 catalog 的证据不支持「tag 与 sha 二选一」**（本机 `~/.claude/plugins/marketplaces/claude-plugins-official/.claude-plugin/marketplace.json`，按 `source` 类型统计）：
  - `source: url`：160 个条目，**全部只有 `sha`、没有 `ref`**；
  - `source: git-subdir`：95 个条目，**同时**带 `ref` 与 `sha`；1 个只带 `sha`。
  - 即：tag 与 sha 并非互斥，官方两种写法都用于「钉住一个确定提交」。taskflow 用 `source: url` + `ref` + `sha` 属于补充写法，`hooks/release-check` 按「`ref` 解析出的提交 == `sha`」校验它。
- 本仓库的 rollout 纪律落在 `RELEASE.md` 里（「Push the tag only after explicit release-owner approval」「TaskFlow does not push tags or create GitHub Releases automatically」），`CONTRIBUTING.md` 没有涉及 release 路径。

## Requirements

- R1：`RELEASE.md` 第 6 步改为：pin 提交在本地创建后，与注解标签在**同一次** `git push --atomic origin main refs/tags/<tag>` 中推送，两端要么同时可见、要么都不可见。
- R2：`RELEASE.md` 明确这次推送同时更新一个受保护的信息（标签）与一条可回退的信息（可读的 catalog 记录），因此它一次执行、事后审阅，与本仓库对标签「事后不可回退」的既定纪律一致。
- R3：`RELEASE.md` 明确 pin 提交**不夹带其他内容**（只有 `ref`/`sha` 字面量），其正确性由 `git merge-base --is-ancestor` 与 `bash hooks/release-check .` 强制；发布元数据提交（有实质内容）仍走 Release PR 路径。
- R4：`RELEASE.md` 为「远端拒绝原子推送」留一条后路：若远端不支持 atomic，退回「先推标签、再按步骤 6 更新 catalog」的顺序，并把该次窗口记入发布任务。
- R5：`RELEASE.md` 的 `## Rollback` 与 `## Known limitations` 补齐：若标签已与 catalog 同时推送，而 catalog 记录有误，修正它意味着更新任务 `rollback` 段落同时提到的标签——修正路径是把该标签视为待重指（该文档已在 `rollback` 段落写有「删除或移动远端标签需要 owner 显式授权」）。

## Acceptance Criteria

- `RELEASE.md` 里存在一条可机械执行的推送命令：pin 提交与标签在同一次 `--atomic` push 中，且命令完整（包含 `origin main` 与 `refs/tags/<tag>`）。
- `RELEASE.md` 对「不夹带内容」「由 `release-check` 强制」「回退路径」三点各有明确表述，回归检查不再依赖读者从 64–69 行的两提交说明里推断。
- `bash hooks/release-check .`、`bash hooks/smoke-test`、`git diff --check` 在本分支上通过（或按 `RELEASE.md` 的规则记录未跑到的项）。
- 除 `RELEASE.md` 外不改任何文件；`hooks/`、`skills/`、catalog 一律不动。

## In Scope

- `RELEASE.md`：第 3–6 步、64–69 行的说明段、`## Rollback`。
- 本任务的 PRD / Plan。

## Out of Scope

- 任何代码、hook、CI、catalog 改动（`hooks/release-check` 保持现状）。
- 去掉 `sha` 的写法的讨论；官方 catalog 多用只带 `sha` 的 `source: url` 条目，本仓库保留 `ref` + `sha`，不在本任务里改。
- v1.0.6 已完成，不回改。
- 移动或删除已推送的标签。

## Risks / Deferred Items

- 文档改动不能验证「远端是否仍支持 atomic」；本任务记录的是**已实测**的当前事实（dry-run exit 0），若将来托管方关闭该能力，R4 的后路才生效。
- 直推 `main` 当前不受服务器规则集限制（PR #34 与历史 pin/归档提交都可佐证），所以 `--atomic` 推送不会因为分支保护失败；若将来加了保护规则，R4 的后路同样适用。
- 若在推送命令里误带其他文件（例如把元数据提交一起放进去），原子性会把一次「可回退的 catalog 修正」放大成一次不可回退的标签动作。R3 是为此设的边界。

## Open Questions

- 无阻塞项。用户已确认策略方向：pin 直推并绑定到 `--atomic` 推送。

## Version History

- v1 — planning。
