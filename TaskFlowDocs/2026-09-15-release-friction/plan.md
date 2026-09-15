# Plan — Cut the mechanical overhead out of a release
> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

- `RELEASE.md` — 发布程序本身；本任务改它的 validation 段与 tag 小节。
- `CODE_STYLE.md` — 退出码约定（`0` pass / `2` needs-user-input / `3` blocked）与「检查默认只读」。
- `TaskFlowDocs/achieved/2026-09-15-release-v1-0-5/` — 上一轮发布的实际开销来源。
- `hooks/repository-check` — 输出格式与退出码的范式。`release-check` 有意照它的形状写。

## Related Tasks

- Depends on: None
- Related: `TaskFlowDocs/achieved/2026-09-15-release-v1-0-5/`（本任务的动机来源）、`TaskFlowDocs/achieved/2026-09-15-hook-integrity/`（同属「hook 行为修正」这一类）

## Skills / Tools Used (Optional)

- `docker` (`bash:3.2`) — purpose: 确认新 hook 在 macOS 出厂 bash 3.2 下可解析; outcome: succeeded; incorporated: 全部 hook 通过 `bash -n`。

## Preconditions

- [x] 适用仓库文档已读：`RELEASE.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`。
- [x] 分支：`fix/release-friction`，基于 `main`。改动先在 `main` 的工作树上完成，提交前才记录到分支上（见 Change Log 的 work revision 一条）。
- [x] 本任务不新建治理文档，`RELEASE.md` 已存在。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-15 21:15 +0800
- Approved version: v1
- Approved scope: PRD / Plan v1 —— release-check、归档 next action、发布文档规则与 RELEASE.md 收敛。回复「同意」即批准本轮方案。

## Steps

### Step 1 — 新增 release-check 并接入 CI

- Goal: 让版本字面量与 marketplace pin 的一致性由一条可运行的只读检查兜住，而不是靠发布时人工 `grep`。
- Dependencies: 无。
- Files: `hooks/release-check`（新）、`.github/workflows/hooks.yml`、`hooks/smoke-test`、`hooks/README.md`、`skills/taskflow/references/runtime.md`、`README.md`、`README.zh-CN.md`。
- Implementation checklist:
  - [x] `hooks/release-check`：按字段名 `sed` 取 manifest/CHANGELOG/README 的版本与 marketplace 的 `ref`/`sha`；版本互比，`ref` 只与 `sha` 比；退出 `0`/`2`/`3`。
  - [x] CHANGELOG 取「最新的**版本**段落」（`^## \[[0-9]`），使 `## [Unreleased]` 不被当成版本字面量。
  - [x] `.github/workflows/hooks.yml` 增加 `release` job（`fetch-depth: 0`）。
  - [x] smoke 新增一节，覆盖一致、README 漂移、CHANGELOG 漂移、cachebuster 后缀不参与比较、`sha` 不符、pin 指向上一个 release（必须通过）、tag 本地缺失、manifest 缺失（退出 `3`）。
  - [x] 两个 hook 清单（`hooks/README.md`、`references/runtime.md`）补上新脚本。
- Acceptance: smoke 全绿；`release-check` 在漂移时报 `needs-user-input` 并指名漂移处，删文件时报 `blocked`。
- Verification: 见 `## Verification / Review`。
- Rollback: 删除 `hooks/release-check` 与 CI job；版本字面量本身未改动。
- Status: done

### Step 2 — 归档时清空 Todo 的 next action

- Goal: 归档后的条目不再自相矛盾地声称还有未完成的下一步。
- Dependencies: 无。
- Files: `hooks/archive`、`hooks/smoke-test`。
- Implementation checklist:
  - [x] `hooks/archive` 的 awk 在设 `- Status: done` 的同一趟里把 `- Next action:` 写成 `None — completed and archived.`。
  - [x] 条目原本没有该字段时，在 `- Status:` 之后插入标准行而不是让归档失败。
  - [x] `hooks/archive` 自身的第 4 步校验加一条断言。
  - [x] smoke 两处：生命周期条目（有该字段）与 09-08 fixture（无该字段，断言插入）。
- Acceptance: 两种形态归档后 `- Next action:` 都是 `None — completed and archived.`。
- Verification: 见 `## Verification / Review`。
- Rollback: 还原 `hooks/archive` 的 awk 段。
- Status: done

### Step 3 — 发布文档规则与 RELEASE.md 收敛

- Goal: 发布任务不再重抄 `RELEASE.md`，示例 tag 不再随版本过期，两个提交的必然性有书面记录。
- Dependencies: 无。
- Files: `skills/taskflow/references/artifacts.md`、`RELEASE.md`、`hooks/smoke-test`。
- Implementation checklist:
  - [x] `artifacts.md` 增加「Release task documents」一节：PRD 记目标/版本决策/变更指针/验收，Plan 按 `RELEASE.md` 的章节分 Step 并引用而不重抄，保留 `## Approval` 与归档。
  - [x] smoke 断言该节的标题、三处关键措辞（`RELEASE.md` is the plan、不重抄清单、保留 Approval）。
  - [x] `RELEASE.md` validation 段加入 `release-check`，删掉只覆盖两个 manifest 的 `python3` 片段。
  - [x] `RELEASE.md` 示例 tag 改为 `vX.Y.Z`；tag 小节写明两个提交是构造使然，并写明 CLI 按 pinned commit 克隆、`sha` 是 tag 被移动时的兜底。
- Acceptance: 仓库内不再有随版本过期的示例 tag 字面量；发布文档规则已断言。
- Verification: 见 `## Verification / Review`。
- Rollback: 还原三处文档改动。
- Status: done

## Checkpoints

- Step 1 的 smoke 断言必须逐条 mutation 验证（把实现改坏 → 断言变红），否则新检查可能只是恒真。
- `release-check` 属于新增的可选检查，不改任何既有 hook 的行为；归档改动会改变 Todo 输出，是本轮唯一的运行时行为变化。

## Verification / Review

- 2026-09-15 Step 3: artifacts.md 新增 Release task documents 一节并断言；RELEASE.md 加入 release-check、删掉 python3 片段、示例 tag 改 vX.Y.Z、写明两个提交的构造原因

- 2026-09-15 Step 2: 归档后条目 - Next action: None — completed and archived.；缺字段条目插入标准行；两处 smoke 断言（含重复 next action 与残留旧值）

- 2026-09-15 Step 1: bash hooks/smoke-test: 新增 release-check 一节全绿；四条 mutation 逐条验证断言变红（version 比较、sha 比较、next action、发布文档规则）；docker bash:3.2 全部 hook 解析通过

- `bash hooks/smoke-test` → `ALL SMOKE PASSED`（新增 `release-check` 与发布文档两节）。
- `bash hooks/release-check .` → `STATUS: pass`，退出 `0`。
- `bash hooks/repository-check .` → `STATUS: pass`。
- `python3 evals/runner.py` → `PASS (6 evals)`。
- `quick_validate.py skills/taskflow` → `Skill is valid!`。
- 全部 hook 在 `docker run --rm -v "$PWD":/w -w /w bash:3.2` 下 `bash -n` 通过。
- `git diff --check` → 无空白错误。
- 未跑：`hooks/smoke-test-windows.ps1`（本机无 PowerShell），由推送后的 CI `smoke` job 覆盖。

## Change Log

- 2026-09-15 work revision — 初版：`release-check`、归档 next action、发布文档规则与 `RELEASE.md` 收敛，随附 smoke 断言与 CI job。
- 2026-09-15 work revision — 实现完成、验证通过后才切出 `fix/release-friction` 分支并提交；`CONTRIBUTING.md` 要求动手前建分支，本任务是在 `main` 的工作树上直接做的，属已知偏差，不改写已完成的工作。

## Follow-ups

- 本轮不改已归档条目里现存的不一致 next action（历史只读）。
- 若未来 README 不再写版本字面量，`release-check` 的 README 比对需要相应调整（见 PRD 的 Risks）。

## Version History

- v1 — planning.
