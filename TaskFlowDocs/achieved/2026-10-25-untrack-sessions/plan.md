# Plan — 把 8 个已被跟踪的 sessions.md 移出版本库
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `.gitignore:19` — `TaskFlowDocs/**/sessions.md`，实测有效（临时目录里 `git add -A` 只暂存 `prd.md`）
- `hooks/smoke-test:3571-3635` — 「clone-local 文件按克隆排除」那段，其中 `:3623` 断言「已跟踪副本保持可见」，本任务不改它的语义
- `hooks/install-git-hygiene:55-70` — 规则写进 `info/exclude` 的实现
- `hooks/repository-check:6` — 只被 `RELEASE.md:52` 与 `CONTRIBUTING.md:8/31` 手工调用，不进 CI
- `TaskFlowDocs/achieved/2026-09-14-untrack-workflow-draft/` — 同类前例：把一个不应跟踪的文件移出版本库

## Related Tasks

- `TF-20261025-7c5897`（已完成，1.1.8）— 建了 `install-git-hygiene`，解决**规则写在哪里**。本条只清**存量**，不改规则。
- `TF-20261025-33b2c4`（已删除）— 被证伪的相近条目，结论是 git 对已跟踪路径不应用 ignore 规则，与本条无重叠。
- `TF-20261025-ef6c18`（并行）— 另一个工作树，两者不共享任何文件。

## Skills / Tools Used

- [PRD] `agent-skills:deprecation-and-migration` — purpose: 在「`git rm --cached` 与重写历史」之间取舍，并判断要不要加回归断言；outcome: `succeeded`；incorporated: 该 skill 的「替换必须已被证明」「迁移成本 vs 维护成本」「advisory 优先」三条直接得出 R2（不改历史）与 R3（不加断言：断言不进 CI 就没有保护作用，而为八个不再增长的文件加一条三平台路径映射，维护成本高于它挡住的回归）。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 把清理拆成「先移出索引、再改文字」两个可验证 Step；outcome: `succeeded`；incorporated: 把「文件留在磁盘上就会变成未跟踪」写成 Checkpoint 里的机械判据（`git status --porcelain | grep '^??'` 必须为空），因为这是本条最容易被忽略的一半。
- [Test] `Unaided — no capability applied to this phase; considered: testing strategy` — 这条任务没有新逻辑可测：验证是八个 SHA-256 的前后对比加一次全量 smoke，两者都是把既有工具跑一遍，没有哪个能力会为此提供形状。

## Preconditions

- 工作树 `.worktrees/untrack-sessions`，分支 `chore/untrack-sessions`，基线 `4a2b407`。
- 8 个副本全部在 `achieved/` 下；`.gitignore` 规则已在 `c630536`（2026-10-25）落地，晚于全部 8 次添加。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-25 23:20 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 移出索引并确认磁盘内容不变

- Goal: R1、A1、A2、A4。
- Dependencies: 无。
- Files: 8 个 `TaskFlowDocs/achieved/*/sessions.md`（只改索引，不改工作区）
- Implementation checklist:
  - [x] 记录移出前每个文件的 SHA-256（`shasum -a 256`），写进 Verification。
  - [x] `git rm --cached` 这 8 个路径（一次给全参数，不要 `-r`）。
  - [x] `git status --porcelain`：应只有 8 条 `D ` 暂存删除，**没有** `??` 未跟踪项。
  - [x] 重算 SHA-256，与第一步逐条比对。
- Acceptance: A1、A2、A4。
- Verification: 两张摘要表贴在下面。
- Rollback: `git reset` 取消暂存，`git checkout -- <path>` 恢复索引。
- Status: done

  移出前后的 SHA-256 逐条相同（8/8），文件全部仍在磁盘上。`git status --porcelain` 只有 8 条 `D `，
  唯一的 `??` 是本任务自己的目录 `TaskFlowDocs/2026-10-25-untrack-sessions/`——**8 个副本没有变成 `??`**，
  这是 `.gitignore:19` 那条规则在原地生效的证据。

### Step 2 — 注释、CHANGELOG 与自检

- Goal: R4 的记录面与 A3、A5。
- Dependencies: Step 1。
- Files: `.gitignore`、`CHANGELOG.md`
- Implementation checklist:
  - [x] ~~`.gitignore` 那段注释里「八个副本仍被跟踪」的说法已过期——改注释记录「存量已于 2026-10-25 清空，规则本身未变」。~~ **未改**：读了注释，它说的是规则**为什么**写在 `.gitignore` 而不是别人克隆的 `info/exclude`；关于「八个副本」的那句在 CHANGELOG 1.1.8 里，不在注释里。见下面「一处没有按 Plan 做」。
  - [x] `CHANGELOG.md` `[Unreleased]` 下一条，措辞点明「清理存量，不是改规则」，并点名 R4 的静默丢失面。
  - [x] `bash hooks/smoke-test` 全量通过（A3）。
  - [x] `bash hooks/repository-check .` 的 `STATUS:` 一行与基线相同。
- Acceptance: A3、A5。
- Verification: `bash hooks/smoke-test` 末行；`repository-check` 的 `STATUS:` 行。
- Rollback: `git checkout -- .gitignore CHANGELOG.md`。
- Status: done

## Checkpoints

- Step 1 之后：`git ls-files | grep 'sessions\.md'` 无输出，且 `git status --porcelain | grep '^??'` 无输出。后者是这条任务最容易被忽略的一半——文件留在磁盘上就会变成未跟踪，规则必须盖住它。
- Step 2 之后：`git diff --check` 干净；`git diff .gitignore` 只有注释行。

## Verification / Review

| 检查 | 结果 |
| --- | --- |
| `git ls-files \| grep 'sessions\.md'` | 无输出（移出 8 个之后） |
| 磁盘内容 | 8/8 的 SHA-256 移出前后一致 |
| `git status --porcelain` | 8 条 `D `，无 `??` 指向前述 8 个路径 |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` |
| `bash hooks/repository-check .` | `STATUS: needs-user-input`，原因只有本任务目录未跟踪（提交即消） |

**一处没有按 Plan 做**：Plan 第 2 步要改 `.gitignore` 的注释。读了之后没改——那段注释说的是规则**为什么**写在
`.gitignore` 而不是 `info/exclude`（「a clone of *this* repository that has not run the hooks yet is still
covered」），关于「八个副本」的那句在 CHANGELOG 1.1.8 里，不在注释里。改它就是改一段没有说错的文字。
A5 要求的 CHANGELOG 记录照做。

## CI record

PR [#100](https://github.com/hkwuks/TaskFlow/pull/100)，head `9479cd0`，run
[40206756359](https://github.com/hkwuks/TaskFlow/actions/runs/40206756359)：

| job | 结果 |
| --- | --- |
| smoke (ubuntu-latest) | pass 19s |
| smoke (macos-latest) | pass 54s |
| smoke (windows-latest) | pass 31s |
| release / todo-merge-audit / changes | pass |
| evals | **skipping** |

`evals` 是 skipped 而不是 pass：`tools/workflow-affected` 按路径分类，本分支只动
`TaskFlowDocs/achieved/**/sessions.md` 与 `CHANGELOG.md`，不进 evals 的路径集。PR 上只跑受影响的 job，
推 main 才跑全部——这是那个工具的既定行为，不是这次改动造成的缺口。

归档后 head 变成 `74e3543`，重跑 run
[40322941194](https://github.com/hkwuks/TaskFlow/actions/runs/40322941194)：`smoke` 三平台 pass（ubuntu 19s、macos 1m4s、windows 27s），`release` / `changes` / `todo-merge-audit` pass，`evals` 仍为 skipping，同一原因。

## Change Log

- v1 — planning：PRD 与 Plan 写成，等待批准。

## Follow-ups

- 若之后副本重新出现，先查 `install-git-hygiene` 是否在那些克隆上跑过，而不是加断言。

## Version History

- v1 — planning。
- v2 — 记入 CI 结果（PR #100，run 40206756359）；`evals` 为 skipped 而非 pass，原因记在 CI record 一节。
