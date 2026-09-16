# Plan — Isolate a task before its documents are written, and make the choice auditable
> Task version: v1
> Status: ready

No spec required — three documentation/template sentences plus one read-only report paragraph in an existing hook.

## Reference Pointers

- `skills/taskflow/SKILL.md:121-137` — 能力选择的现有规则；其中「must be a choice, not an oversight. Record it as one.」是本任务要落到模板上的那句话。
- `skills/taskflow/SKILL.md:226` — 隔离规则当前所在的**阶段 5**，本任务要把它提前到阶段 1 之前。
- `skills/taskflow/references/artifacts.md:80` 与 `hooks/task:399` — `## Skills / Tools Used (Optional)` 的两个字面量落点。
- `hooks/repository-check:57` — 既有 `Working tree: has changes` 一行；新报告接在它附近。
- `hooks/smoke-test:582` — `== repository-check is read-only and reports actionable status ==` 一节，是本任务要扩写并保住的既有断言。
- `TaskFlowDocs/achieved/2026-09-14-branch-and-worktree-gate/prd.md` — 隔离规则的来源；其 R7「No hook enforces the rule automatically」是本任务 R5 的依据。

## Related Tasks

- Depends on: None
- Related: `TaskFlowDocs/2026-09-16-duplicate-todo-id/`、`TaskFlowDocs/2026-09-16-web-ui-merge-loss-guard/`（同为本轮用户审阅发现的问题线；E 与两者均无文件重叠）
- Follows: `TaskFlowDocs/achieved/2026-09-14-branch-and-worktree-gate/`（把它的隔离规则从阶段 5 提前，并把 worktree 从「多任务时」改为「一律」）

## Skills / Tools Used

Unaided — no capability applied to this phase; considered: `superpowers:brainstorming` and `addy-agent-skills:idea-refine` / `interview-me` for requirements framing, `superpowers:writing-plans` and `addy-agent-skills:planning-and-task-breakdown` for the Plan, `skill-creator` for editing the Skill itself. All were judged unnecessary: the requirements are template/rule sentences whose evidence is already in the PRD's Background, and the user supplied the isolation decision directly.

## Preconditions

- [x] 适用仓库文档已读：`CONTRIBUTING.md`、`CODE_STYLE.md`、`.github/pull_request_template.md`。
- [x] 分支：`chore/e-task-isolation-and-capability-record`，基于 `main`。
- [x] 工作树：`.worktrees/e-task-isolation-and-capability-record`。本任务自身的隔离按本任务将写下的规则执行——先隔离，再写第一份文档。
- [x] 远程基线：`origin` 即 `hkwuks/TaskFlow`，目标 `main`；非 fork。
- [x] 本任务不新建治理文档；`SKILL.md`、`artifacts.md`、`CONTRIBUTING.md` 均已存在。

## Approval

- Status: requested
- Approved by: pending
- Approved at: pending
- Approved version: pending
- Approved scope: pending

## Steps

### Step 1 — 把隔离提前到第一份任务文档之前

- Goal: 让「文档生在别人的分支上」这件事不再可能发生——隔离先于文档，而不是先于代码。
- Dependencies: 无。
- Files: `skills/taskflow/SKILL.md`、`CONTRIBUTING.md`、`README.md`、`README.zh-CN.md`、`.gitignore`。
- Implementation checklist:
  - [ ] `SKILL.md`：在 `### Todo → PRD → Spec → Plan` 段（阶段 1 之前）写明——在创建任何 `TaskFlowDocs/<slug>/` 文档或 `todo.md` 条目**之前**，任务已在自己的分支与工作树上；给出 `git worktree add .worktrees/<slug> -b <type>/<slug> <base>`，并说明主 checkout 从此停在 base 分支且保持干净。
  - [ ] `SKILL.md:226`（阶段 5）：删掉「第一次建隔离」的语义，改为一句确认——隔离已在阶段 1 建立，此处只确认仍然成立。
  - [ ] `CONTRIBUTING.md`「Working branches」：补 worktree 命令与理由（需要隔离的包括任务文档，不只是代码）；不把 worktree 写成「多任务时才需要」。
  - [ ] `README.md:91` / `README.zh-CN.md:58`：两句各自对齐到「每任务一个工作树」，保持中英行为一致（`CODE_STYLE.md:8`）。
  - [ ] `.gitignore`：加 `.worktrees/`。
- Acceptance: 见 PRD A1–A4。
- Verification: `git worktree add` 的实际可运行性；`git status` 不再报 `.worktrees/`；`grep -c 'Skills / Tools Used (Optional)'` 与阶段编号不变；`git diff --check`。
- Rollback: 还原五处文本；无逻辑分支受影响。
- Status: pending

### Step 2 — 把能力选择从可选改为必填

- Goal: 让「能力选择跑没跑」在 Plan 上留下可审计的痕迹，而不是留空。
- Dependencies: 无（与 Step 1 无文件冲突，除 `SKILL.md` 的相邻段落需按顺序编辑）。
- Files: `skills/taskflow/references/artifacts.md`、`skills/taskflow/SKILL.md`、`hooks/task`、`hooks/smoke-test`。
- Implementation checklist:
  - [ ] `artifacts.md:80` 的 Plan 大纲：`## Skills / Tools Used (Optional)` → `## Skills / Tools Used`，并写明两种合法填法（实际调用清单 / `Unaided — …` 一行）。
  - [ ] `hooks/task:399` 的 `promote` 骨架同步去掉 `(Optional)`；只改这一处文本，不动其它逻辑。
  - [ ] `SKILL.md:123` / `:137` 附近补一句落点：该节必填，未调用也要写一行；与既有「must be a choice, not an oversight」措辞一致。
  - [ ] `hooks/smoke-test` 增加断言：`artifacts.md` 与 `hooks/task` 里都不再出现 `Skills / Tools Used (Optional)`，且 `Unaided —` 的填法与说明已写入 `artifacts.md`。
  - [ ] 新增断言逐条 mutation 验证（把模板改回 `(Optional)` → 断言变红）。
- Acceptance: 见 PRD A5、A7、A8。
- Verification: `bash hooks/smoke-test`；`bash hooks/task promote` 到一个临时 root 检查生成骨架；`docker run --rm -v "$PWD":/w -w /w bash:3.2 bash -n hooks/task`；`quick_validate.py skills/taskflow`；`git diff --check`。
- Rollback: 还原四处文本改动。
- Status: pending

### Step 3 — 让错位的任务产物在只读检查里可见

- Goal: 下次再有「文档生在别的分支上」，`repository-check` 能直接说出来，而不是等人发现 checkout 被挡住。
- Dependencies: 无（`hooks/repository-check` 与 Step 1/2 无文件重叠）。
- Files: `hooks/repository-check`、`hooks/smoke-test`、`skills/taskflow/references/runtime.md`（若清单需要同步）。
- Implementation checklist:
  - [ ] `repository-check` 在 `Working tree: has changes` 附近新增一段 `Task artifacts:`：列出本 checkout 里已跟踪但**不属于当前分支**的任务产物、以及未跟踪的任务目录；对 `todo.md` 里 `Status` 为 `promoted` / `in_progress` 的条目，若其 `Task:` 指向的目录不在当前分支上，打印一行指认。
  - [ ] 干净的单任务工作区不打印该段（或打印一行 `Task artifacts: none`），既有退出码语义不变——报告不设置 `needs`。
  - [ ] 在输出里写明判定边界：未跟踪的任务目录无法归属到分支，只按「本 checkout 的未提交产物」列出，不断言归属。
  - [ ] `hooks/smoke-test` 扩展 `== repository-check … ==` 一节：错位 fixture 必须打印指认行；干净 fixture 不打印；逐条 mutation 验证（去掉报告 → 断言变红）。
  - [ ] 若 `runtime.md` 的 hook 清单描述了 `repository-check` 的职责，同步一句。
- Acceptance: 见 PRD A6、A7、A9。
- Verification: 在当前（错位）工作树上跑 `bash hooks/repository-check .` 看输出；在干净 fixture 上跑；`bash hooks/smoke-test`；`bash:3.2` 容器 `bash -n`。
- Rollback: 删掉报告段与新增断言，`repository-check` 回到只打印 `Working tree` 一行。
- Status: pending

## Checkpoints

- 三个 Step 都只改文本、模板与一个只读检查；**没有任何 hook 的判断逻辑或退出码语义被改变**。
- `smoke-test` 的既有断言（`== task lifecycle dispatcher ==`、`== repository-check is read-only … ==`、`== TaskFlow packaged Skill contract ==`）必须保持通过。
- Step 1 是本任务自身的实践：本任务的目录应当在 `.worktrees/e-task-isolation-and-capability-record` 里写成，主 checkout 保持干净。

## Verification / Review

## Change Log

## Follow-ups

## Version History

- v1 — planning. 三个 Step：隔离提前（用户 2026-09-16 决定「提前到阶段 1、每任务一个 worktree、`.worktrees/<slug>` + gitignore」）、能力留痕必填、`repository-check` 错位报告。
