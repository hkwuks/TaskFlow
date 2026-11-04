# Plan — 合并后 teardown 一并删除已合并的本地分支
> Task version: v1
> Status: completed

No spec required — 改动集中在两个脚本的提示/报告节与一段文案，无跨层契约。

## Reference Pointers

- `hooks/archive:315-339` — 现有 teardown 提示与「hook 不碰 Git」的边界说明。
- `hooks/repository-check:115-192` — 现有 stale worktree 报告节，新节复用其 `--is-ancestor` 判断与「只报告、不动退出码」约束。
- `hooks/smoke-test:1000-1060` — archive teardown 断言；`hooks/smoke-test:4558-4660` — repository-check stale worktree 断言。两处都要改/加。
- `skills/taskflow/SKILL.md:337-345`、`CONTRIBUTING.md:33` — 同一句 teardown 规则的两处散文。

## Related Tasks

无。

## Skills / Tools Used

- [PRD] invoke `git-workflow` — purpose: 确认 `git branch -d` 与 `-D` 的安全语义、squash-merge 下 `--merged` 的盲区；outcome: 确认 `-d` 在未合并时拒绝删除，祖先判断对 squash 分支会漏报；incorporated: R3（只给 `-d`）、Out of Scope（不做 squash 识别）、Risks（漏报方向可接受）。
- [Plan] invoke `agent-skills:planning-and-task-breakdown` — purpose: 把 PRD 的六条需求拆成可验证、可回滚的 Step 并定依赖顺序；outcome: 四步串行（提示文案 → 报告节 → smoke 断言 → 文档对齐），每步带 verification 与 rollback；incorporated: 下方 Steps 与 Checkpoints。
- [Test] Unaided — testing strategy; considered: testing strategy. 本任务的验证全部是现有 smoke 套件的断言增改，没有值得单独调用的测试设计能力；Step 3 直接写断言、跑变异检验。

## Preconditions

- 处于任务 worktree `.worktrees/teardown-branch`，分支 `fix/teardown-branch`。
- `hooks/repository-check` 与 `hooks/archive` 当前输出作为基线（smoke 会逐字断言）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-04 22:19 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — teardown 提示：worktree 与分支一次删完

- Goal: `hooks/archive` 在 linked worktree 中归档时，teardown 提示同时给出 worktree 移除与已合并分支删除，且只出现 `-d`。
- Dependencies: 无。
- Files: `hooks/archive`。
- Implementation checklist:
  - [x] teardown 三行提示改为：条件句、`git worktree remove '<path>'`、`git branch -d '<branch>'`。
  - [x] 去掉 `(the branch survives; deleting it is a separate decision)`，改为说明 `-d` 在未合并时拒绝、因此不会误删。
  - [x] 更新段前注释，使其描述「同一步、两个动作、`-d` 是安全边界」，并保留「hook 本身不碰 Git」的边界说明。
- Acceptance: AC1。
- Verification: `bash hooks/smoke-test` 中 archive teardown 相关段；人工核对输出文本。
- Rollback: `git checkout -- hooks/archive`。
- Status: done

### Step 2 — repository-check 报告没有 worktree 的已合并分支

- Goal: worktree 移除后，已并入 base 的本地分支仍被报出。
- Dependencies: Step 1（文案已定）。
- Files: `hooks/repository-check`。
- Implementation checklist:
  - [x] 新增一节，列出「已并入 base、未被任何 worktree 检出、非 base 自身」的本地分支。
  - [x] 排除：base 分支、被 `git worktree list --porcelain` 中任一 worktree 检出的分支、detached HEAD。
  - [x] 不修改 `needs`，退出码保持现状；无 upstream 时输出 unknown。
  - [x] 报告文案明确「只报告，不删除；用 `git branch -d`」。
- Acceptance: AC2、AC3、AC4。
- Verification: `bash hooks/repository-check .`，以及 smoke 新断言。
- Rollback: `git checkout -- hooks/repository-check`。
- Status: done

### Step 3 — smoke 断言

- Goal: 两处行为都有会失败的断言。
- Dependencies: Step 1、Step 2。
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 更新 archive teardown 断言：要求出现 `git branch -d`，并断言 `branch survives` 不再出现。
  - [x] 新增 repository-check 断言：已合并无 worktree 的分支被报出；未合并、base 自身、被 worktree 检出的都不被报出；退出码不变。
  - [x] 变异检验一次一个：反转新节过滤条件，确认断言变红，然后还原。
- Acceptance: AC2、AC5、AC6。
- Verification: `bash hooks/smoke-test`；变异后单独重跑受影响段。
- Rollback: `git checkout -- hooks/smoke-test`。
- Status: done

### Step 4 — 文档对齐

- Goal: 不再有地方说「分支必然留下」。
- Dependencies: Step 1（最终文案）。
- Files: `skills/taskflow/SKILL.md`、`CONTRIBUTING.md`。
- Implementation checklist:
  - [x] `SKILL.md` teardown 段：命令块加 `git branch -d <branch>`，散文改为「两个动作、同一时刻、`-d` 拒绝未合并」。
  - [x] `CONTRIBUTING.md:33` 同步。
  - [x] 全文 grep 确认无残留 `branch survives` / `separate decision`。
- Acceptance: AC1 的文档侧、R5。
- Verification: `grep -rn 'branch survives' --include='*.md' .` 为空。
- Rollback: `git checkout -- skills/taskflow/SKILL.md CONTRIBUTING.md`。
- Status: done

## Checkpoints

- Step 1+2 完成 → 在 fixture 上手动跑一次 `archive` 与 `repository-check`，确认文本形状再写断言（避免断言反复改）。

## Verification / Review

**逐条对照验收标准**：

- **AC1**（teardown 输出含 `git worktree remove` 与 `git branch -d`，且不再有 `branch survives`）：smoke 的 archive teardown 段断言三者全部通过；`grep -qi 'branch survives'` 断言已从「必须有」反转为「必须没有」。
- **AC2**（已合并无 worktree 的分支被报出；未合并、base 自身、被 worktree 检出的不被报出）：新增四条 smoke 断言全部通过。fixture 首轮暴露了一个真实缺陷——`git branch chore/loose-unmerged` 从已合并的 HEAD 建出来，本身就是已合并的，断言因此报红；改为「在临时 worktree 里加一个提交再移除」，让该分支真正领先 base。
- **AC3**（报告出现时退出码仍为 0）：`[ "$rc" -eq 0 ]` 断言通过；`needs` 未在新节中被赋值。
- **AC4**（无 upstream 输出 unknown）：新节沿用 `[ -n "$base_ref" ]` 外层判断，与 stale worktree 一节同一个分支，输出 `unknown (no upstream base to compare against)`。
- **AC5**：`bash hooks/smoke-test` → `ALL SMOKE PASSED`；`git diff --check` 干净。
- **AC6**（变异检验）：两次，一次一个。
  - `git merge-base --is-ancestor … || continue` 反转为 `&& continue` → `FAIL a merged branch with no worktree was not reported`，已还原。
  - `git branch -d` 改为 `git branch -D` → `FAIL teardown did not delete the merged branch in the same step`，已还原。

**排除项核对**：base 分支由「主 worktree 检出」和显式的 `[ "$candidate" != "$base_ref" ]` 双重排除；detached HEAD 的 worktree 不在 `refs/heads` 里，`for-each-ref refs/heads` 天然不受影响。

**未做**：未删除仓库里现存的任何分支或 worktree——本任务只改行为与报告，实际清理是执行者的动作。

## Change Log

- 2026-11-04：实现 Step 1-4。`hooks/archive` 的 teardown 提示改为「移除 worktree + `git branch -d`，顺序有意义」；`hooks/repository-check` 的 stale worktree 提示同步改为两步；新增 `Merged branches without a worktree` 报告节；`hooks/smoke-test` 反转一条断言、新增六条断言；`SKILL.md` 与 `CONTRIBUTING.md` 的 teardown 段同步。
- 2026-11-04：fixture 缺陷修正（未合并分支必须真正领先 base），属于验证方法修正，不影响已批准的需求。

## Follow-ups

- squash/rebase 合并的残留分支不在报告范围：若平台改为 squash-only，另起任务按 patch-id 处理。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-11-04 用户的疑问**：合并完发现本地还留着 `fix/2026-11-04-skip-guard`、`-ci-skip-archive`、`-merge-todo-speed` 三条分支。它们**不是** worktree 的产物——`git worktree add -b` 创建的是仓库级 ref，worktree 只是它的检出目录，`git worktree remove` 从不删分支。所以拆掉 worktree 之后分支就留在那里了。
  **现状为什么没人清**：`hooks/archive` 在 teardown 提示里明说 `(the branch survives; deleting it is a separate decision)`，这是刻意的——分支可能还持有唯一一份提交，`-d` 恰好也会拒绝未合并的。但「刻意」和「没人做」之间的差额就是这三条分支。
  **要定的判据**：只有**已合并进 base** 的分支才可以删，而且删除只能发生在合并之后——`archive` 本身跑在 push 之前（`CONTRIBUTING.md` 的次序是 `task complete` → commit → push → PR → merge），那一刻分支必然还没合并。所以删除不能放进 `archive` 的归档事务里，只能出现在**合并之后的 teardown 步骤**。
  **候选**：(a) 在 `archive` 的 teardown 提示里加一行 `git branch -d <branch>`，与 `git worktree remove` 并列，让读者一次做完两件事；(b) 加一个独立小命令，枚举所有已合并的本地分支并逐个 `git branch -d`，由 teardown 提示指向它；(c) `repository-check` 报告已合并的残留分支（只是报告，不改状态）。
  注意 `-d` 与 `-D` 的区别是这道题的安全边界：`-d` 在未合并时拒绝，正是想要的。
