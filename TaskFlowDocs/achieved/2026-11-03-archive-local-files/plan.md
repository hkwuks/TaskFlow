# Plan — 归档时把任务目录里的本地专用文件带进 base 检出

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/archive:70-81` — 目录 `mv`，复制步骤要插在它之后。
- `hooks/archive:265-280` — 已经在用 `--absolute-git-dir` + `commondir` 判 worktree，base 路径从这里取。
- `hooks/install-git-hygiene:78-79` — 两条本地专用文件规则，名单的唯一来源。
- `hooks/smoke-test:900-1000` 附近 — archive 的既有夹具；新断言照此风格。
- `CONTRIBUTING.md` — worktree 移除的两个条件（已合并、树干净），是被 ignore 文件绕过的那道检查。

## Related Tasks

- `TF-20261025-24d06c` / `2026-10-25-git-hygiene`（已归档）——建立 exclude 规则的任务，本条补它的归档侧漏洞。
- `2026-10-25-untrack-sessions`（已归档）——把已跟踪的 8 份移出版本库，同样是「存量」问题。

## Skills / Tools Used

- [PRD] `agent-skills:spec` — 收敛目标与验收；产出并入 `prd.md`。
- [Spec] Unaided — considered: architecture and design specification。改法由 PRD 的 R1–R4 决定。
- [Plan] Unaided — considered: work breakdown and task decomposition。
- [Test] Unaided — considered: testing strategy。断言写进 `hooks/smoke-test`。

## Preconditions

- 在 `.worktrees/archive-local-files` 的 `fix/archive-local-files` 分支上。

## Approval

- Status: approved
- Approved by: hk
- Approved at: 2026-11-03 22:20 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — archive 把 `sessions.md` 复制到 base 检出

- Goal: `mv` 之后，若源目录有 `sessions.md`，复制到 base 检出的 `achieved/<task>/`。
- Dependencies: 无
- Files: `hooks/archive`
- Implementation checklist:
  - [x] `mv` 之前先把要搬的文件名记进变量（`mv` 之后路径就不存在了）。
  - [x] `mv` 之后解析 base 检出根：从 `--absolute-git-dir` 的 `commondir` 推出；取不到则跳过。
  - [x] 复制，`cp` 失败只打印一行、不改变退出码。
  - [x] 没有任何本地专用文件时**不打印任何东西**、也不建 base 目录（A2）。
- Acceptance: A1、A2、A3。
- Verification: smoke 新断言 + 手工在探针仓库跑一次。
- Rollback: `git checkout -- hooks/archive`
- Status: done

### Step 2 — smoke 断言

- Goal: 三个行为各有一条断言。
- Dependencies: Step 1
- Files: `hooks/smoke-test`
- Implementation checklist:
  - [x] A1：worktree 风格夹具里放 `sessions.md`，归档后 base 处存在且内容一致、且不在 `git status` 里。
  - [x] A2：无该文件时不打印、不建目录。
  - [x] A3：base 目标不可写时仍 `archive OK`，只多一行 note。
- Acceptance: `bash hooks/smoke-test` 全绿；变异（删掉复制步骤）后 A1 变红。
- Verification: 跑一次变异再还原。
- Rollback: `git checkout -- hooks/smoke-test`
- Status: done

### Step 3 — 清掉现存幽灵目录

- Goal: `TaskFlowDocs/2026-10-29-schema-check/sessions.md` 移到 `achieved/2026-10-29-schema-check/`，空目录删除。
- Dependencies: 无（可先做）
- Files: `TaskFlowDocs/2026-10-29-schema-check/`, `TaskFlowDocs/achieved/2026-10-29-schema-check/`
- Implementation checklist:
  - [x] 复制而非移动，确认一致后删源。
  - [x] 两个目录都不进版本控制。

- Acceptance: A5。
- Verification: `ls` 两处 + `git status --porcelain` 仍为空。
- Rollback: 从 `achieved/` 复制回去。
- Status: done

## Checkpoints

- Step 1 后用探针仓库手工确认一次，再写断言。

## Verification / Review

- [x] CI `Hooks` 工作流 three-host 矩阵全绿：smoke ubuntu 30s / windows 52s / macos 1m24s，changes 与 todo-merge-audit 通过（run 41663579521，PR #114）
- [x] `bash hooks/smoke-test` 本地全绿（ALL SMOKE PASSED，108 个 ok 段）
- [x] 变异验证两次：删掉 `cp` → 「archive did not carry sessions.md to the base checkout」变红；无条件建 base 目录 → 「archive created a base directory for a file that does not exist」变红
- [x] `git diff --check`
- [x] 幽灵目录已清理：`TaskFlowDocs/2026-10-29-schema-check/` 不存在，记录已到 `achieved/2026-10-29-schema-check/sessions.md`

## Change Log

- 2026-11-03 v1 — `archive` 在 `mv` 后把 `sessions.md` 复制到 base 检出（best-effort，不改变退出码）；smoke 新增三组断言；清掉现存幽灵目录。


## Follow-ups

- 「被 exclude 命中的文件」自动发现，改为显式名单之外的独立设计（PRD Deferred）。

## Version History

- v1 — planning.
