# Cut the mechanical overhead out of a release
> Task version: v1
> Status: in_progress

## Goal

把一次发布里纯机械、且没有任何自动检查兜住的开销砍掉：版本字面量的一致性检查、发布任务的文档规则、以及归档时清空 Todo 的 next action。

## Background / Confirmed Facts

- 上一轮发布（`TaskFlowDocs/achieved/2026-09-15-release-v1-0-5/`）的实测开销：版本号散落在 7 个位置，靠 `grep -rn '1\.0\.5'` 人工找；`RELEASE.md` 的 validation 段只用一段 `python3` 片段核对两个 manifest，CHANGELOG 段落、两份 README 示例、marketplace 的 `ref`/`sha` 配对都不在检查范围内。
- 发布任务的 Plan 把 `RELEASE.md` 的清单抄了一遍中译，两份都要维护。
- `hooks/archive` 只把 Todo 的 `- Status:` 改成 `done`，不动 `- Next action:`（`hooks/archive` 的 awk 段）。`promote` 写下的 next action 只在完成前成立，于是归档后条目变成 `Status: done` 配「Complete PRD / Spec / Plan and request approval.`。上一轮 5 个归档条目都是手工改的。
- marketplace 的 `sha` pin 是**真检查**，不是仪式：Claude Code CLI 克隆插件仓库后执行 `git rev-parse HEAD` 与 `sha` 逐字符比对，不等即抛 `SHA pin verification failed`，归类为 `sha_pin_mismatch`；且 `sha` 存在时克隆走 `--no-checkout` + `fetch --depth 1 origin <sha>`，即按 commit 取而非按 tag 取。因此「发布必然两个提交」是设计结果，不是流程失误。
- CI（`.github/workflows/hooks.yml`）目前只有 `smoke` 与 `evals` 两个 job，没有检查版本一致性。

## Requirements

- R1：新增 `hooks/release-check [repo-root]`，只读，比对 `.claude-plugin/plugin.json` 版本（`X.Y.Z`）、`.codex-plugin/plugin.json` 版本的 release 部分（剥离 `+codex.<date>` cachebuster）、`CHANGELOG.md` 最新的 `[X.Y.Z]` 段落、两份 README 的 `claude plugin list` 示例，四处必须与 `plugin.json` 一致。
- R2：同一个 hook 校验 marketplace 的 `ref` 能解析到提交、且 `sha` 等于该提交。`ref`/`sha` 与版本字面量**不做**比较——准备下一次发布时 pin 仍指向上一个 release 是正常中间态。`ref` 在本地不存在时报错并提示先 `fetch`。
- R3：退出码遵循 `CODE_STYLE.md`：一致 `0`，版本不一致 `2`，manifest 缺失 `3`。
- R4：`RELEASE.md` 的 validation 段加入 `release-check`，删掉那段只覆盖两个 manifest 的 `python3` 片段；示例 tag 改为 `vX.Y.Z`，不再随版本过期。
- R5：`RELEASE.md` 写明两个提交是构造使然（tag 依赖发布提交、`sha` 依赖 tag），并写明 CLI 按 commit 克隆、`sha` 是 tag 被移动时的兜底。
- R6：`skills/taskflow/references/artifacts.md` 增加「Release task documents」一节：发布任务记录决策与结果、不重抄 `RELEASE.md` 的程序；保留 `## Approval` 与归档。
- R7：`hooks/archive` 归档时把 Todo 的 `- Next action:` 写成 `None — completed and archived.`；条目原本没有该字段时插入标准行，而不是让归档失败。
- R8：CI 增加 `release` job 运行 `hooks/release-check .`（`fetch-depth: 0`，pin 需要 tag）。
- R9：`hooks/smoke-test` 覆盖以上全部：`release-check` 的通过/漂移/sha 不符/tag 缺失/文件缺失各一例，归档的 next action（已有字段与缺字段两种），以及发布文档规则。

## Acceptance Criteria

- `bash hooks/release-check .` 在当前树上输出 `STATUS: pass`、退出 `0`；任一版本字面量或 `sha` 被改动后退出 `2` 并指名漂移处；删掉 manifest 后退出 `3`。
- `bash hooks/smoke-test` 全绿，且新增断言在把对应实现改坏后确实变红（逐条 mutation 验证）。
- `hooks/archive` 归档后 Todo 条目的 `- Next action:` 与 `- Status: done` 自洽，包括原本没有该字段的条目。
- CI 的 `release` job 在推送后成功。
- 仓库内不再有随版本过期的示例 tag 字面量（`RELEASE.md` 用 `vX.Y.Z`）。

## In Scope

- `hooks/release-check`（新）、`hooks/archive`、`hooks/smoke-test`、`.github/workflows/hooks.yml`、`RELEASE.md`、`skills/taskflow/references/artifacts.md`、`skills/taskflow/references/runtime.md`（hook 清单）、`hooks/README.md`（hook 清单）、两份 README 的一段说明。

## Out of Scope

- 不改版本号策略，不改 marketplace 的 `sha` pin 机制。
- 不回改已归档任务文档的语言或内容。
- 不做发布自动化（打 tag、建 Release 仍由人执行）。
- Windows 侧不新增对应的 PowerShell `release-check`：`hooks/smoke-test-windows.ps1` 覆盖的是生命周期与启动器参数，版本一致性由 CI 的 `release` job 在 Linux 上覆盖。

## Risks / Deferred Items

- `release-check` 用按字段名的 `sed` 取 JSON 值而不是 JSON 解析器，是为了守住「hook 不依赖解释器」。风险是 manifest 若被重排成多行同一字段会取错；由 smoke 的 fixture 形态和 `CODE_STYLE.md` 对 manifest 形状的约束兜住。
- README 的 `Version:` 示例是可读性内容，未来若改成引用式写法（不再写字面量），`release-check` 会取不到值并报不一致；届时应改为「缺失即跳过」而不是放宽比对。

## Open Questions

- 无。

## Version History

- v1 — planning.
