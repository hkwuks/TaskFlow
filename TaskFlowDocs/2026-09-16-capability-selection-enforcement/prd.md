# Isolate a task before its documents are written, and make the choice auditable
> Task version: v1
> Status: ready

## Goal

把两件在同一轮里暴露出来的事一起收口，因为它们是同一个根因：**任务没有在写第一份文档之前就被隔离，而「有没有做选择」在文档上没有强制落点。**

- 隔离：文档（`TaskFlowDocs/<slug>/` 与 `todo.md`）在阶段 1 就落盘，而隔离规则在阶段 5 才生效。于是文档生在共享 checkout、往往还是别人的分支上；未提交的改动与未跟踪目录又会随 `git checkout -b` 原样带走，checkout 回去时被自己弄脏的 `todo.md` 挡住。
- 留痕：`SKILL.md` 已经写下「未调用能力也必须是被选择的结果、并记录下来」，但 `plan.md` 模板把那一节标成 `(Optional)`，最省事的读法就是留空——本轮连续三个任务都是空节，于是「选择不调用」与「忘了这一步」不可区分。

本任务把两者都变成**阶段 1 就成立、且可审计**的状态，并让错位状态在只读检查里可见。

## Background / Confirmed Facts

**隔离（本轮实测，非推断）**

- `skills/taskflow/SKILL.md:226` 把隔离放在**阶段 5（Build）**：「Before the first edit, put the task on its own short-lived branch…」。而阶段 1（PRD）就要创建 `TaskFlowDocs/<slug>/prd.md`。所以第一份文档必然早于隔离。
- `hooks/task promote` 直接往 `$root/TaskFlowDocs/<slug>/` 写 PRD/Plan 骨架，并把条目写进共享的 `TaskFlowDocs/todo.md`。两条路径都是被跟踪的共享路径。
- 后果一：**checkout 被挡住**。当前 checkout 的工作区带着 B/C/E 三个任务的未提交产物（`todo.md` 已改 + 三个未跟踪目录）。实测 `git checkout main` → `error: Your local changes to the following files would be overwritten by checkout: TaskFlowDocs/todo.md … Aborting`。回不去 `main` 就起不了下一个任务的分支。
- 后果二：**产物本来就会跟过去**。在 scratch clone 里实测：带一个未跟踪任务目录 + 改过的 `todo.md`，`git checkout -b <new>` → 两者原样带到新分支，`git status` 里仍然是 `M TaskFlowDocs/todo.md` + `?? TaskFlowDocs/<slug>/`。所以「新任务在干净分支上开始」这个前提从未成立过。
- 本轮实证：B/C/E 三个任务的 PRD/Plan 就是这么生在了 `fix/todo-entry-loss-detection` 上——它们是 A 的分支上的未提交产物，与 A 无关。
- 后果三：**成功切走后旧任务的产物会进新任务的历史**。`hooks/task state` 只在 `complete` 时做归档事务；`todo.md` 的登账没有提交点，所以「某任务的 Todo 条目属于哪个分支」没有定义。
- `CONTRIBUTING.md:22` 已有「Never implement in the base working tree. One task, one short-lived branch, created before the first edit」，但只讲分支、不讲 worktree，且没有把时机说到「写文档之前」。`README.md:91` / `README.zh-CN.md:58` 已声明「worktree 规则写在 Skill 中」。
- 仓库已经在用 `.worktrees/<slug>` 这一约定（`.worktrees/hook-gates`、`.worktrees/no-python-hooks`、`.worktrees/todo-merge-driver`），但 `.gitignore` **没有**忽略 `.worktrees/`。
- `hooks/repository-check:57` 只有一行 `Working tree: has changes (review before rebasing or submitting)`——它知道有改动，但不知道那些改动属于哪个任务、更不知道任务目录与当前分支是否匹配。这是唯一一处已经存在、且已经打印工作树状态的只读检查。

**留痕（既有规则，执行缺失）**

- **规则已经存在，且措辞是「必须做选择、可以不调用」**：`SKILL.md:121` 要求每个阶段做实质工作前先看当前有哪些能力；`SKILL.md:137` 明确「A phase ran unaided when its artifact exists but nothing was invoked for its concept class; that is a legitimate outcome, but it must be a choice, not an oversight. Record it as one.」；`SKILL.md:123` 要求只记录**实际被调用**的能力，并明确「Do not record discovery, selection, or an uninvoked capability as used」。
- **实际发生的是空节**：本轮三个任务（`-todo-entry-loss-detection`、`-web-ui-merge-loss-guard`、`-duplicate-todo-id`）的 Plan 里 `## Skills / Tools Used (Optional)` 下面都是空的，既没列被考虑的能力，也没写下「本阶段无适用能力」这个决定。
- **规则与自身模板冲突，是空节的结构性成因**：`artifacts.md:80` 与 `hooks/task:399` 都写 `## Skills / Tools Used (Optional)`，而 `SKILL.md:137` 说 unaided 必须是被选择的。一个「可选」的节与一个「必须记录的选择」读起来矛盾，最省事的做法就是留空。
- **`spec.md` 的省略有强制落点，能力选择没有**：本轮三个任务都判为 small，按阶段 3 可省 `spec.md`，但**必须**留 `No spec required — <brief reason>`；`hooks/task promote` 在 `small` 时已经生成这行，`hooks/smoke-test` 的 `== TaskFlow packaged Skill contract ==` 一节也断言了该措辞。两条规则的强度不一致，本任务把能力选择补齐到同一强度。
- **本轮真实的能力清单**（本机枚举，可作为「考虑过」的证据）：`superpowers:brainstorming`、`superpowers:writing-plans`、`addy-agent-skills:idea-refine` / `interview-me` / `spec-driven-development` / `planning-and-task-breakdown` / `documentation-and-adrs`、`skill-creator`、`claude-code-guide`、`codegraph` MCP、`context-mode` 技能组。

**归属决定（用户 2026-09-16 决定）**

- 新发现的隔离问题**并入本任务**，不另开一条，因为根因同一个：任务产物在隔离之前产生。
- 隔离规则**提前到阶段 1**，并**一律每任务一个 worktree**（不是只在多任务并行时）。
- worktree 放在 `.worktrees/<slug>`，并把 `.worktrees/` 加进 `.gitignore`。
- 检查落在 `hooks/repository-check`，**只读报告，不做 gate**。

## Requirements

### 隔离提前（根因）

- R1：`skills/taskflow/SKILL.md` 的隔离规则从阶段 5 提前到**阶段 1 之前**：在创建任何 `TaskFlowDocs/<slug>/` 文档或 `todo.md` 条目**之前**，任务已经拥有自己的分支与工作树。阶段 5 保留一句「确认隔离仍然成立」，不再承载「第一次建隔离」的语义。
- R2：**一律每任务一个 worktree**，不再以「同时有多个任务」为条件；`git worktree add .worktrees/<slug> -b <type>/<slug> <base>` 是给出的命令形状。主 checkout 从此停在 base 分支且保持干净。
- R3：`CONTRIBUTING.md` 的「Working branches」一节补上 worktree：分支规则不变（前缀、base、动手前先建），但明确「需要隔离的不止是代码，还包括任务文档」，并给出 worktree 命令。`README.md` / `README.zh-CN.md` 各一句保持行为对齐（`CODE_STYLE.md:8`）。
- R4：`.gitignore` 忽略 `.worktrees/`；`.worktrees/<slug>` 成为记录在 `plan.md` `## Preconditions` 里的约定值（该节已有「分支」项，补「工作树」）。
- R5：`hooks/task promote` / `state` / `complete` 的**行为不变**——不新增 branch/worktree 的自动创建，也不新增 gate。隔离是 Agent 与用户的决定，与 `2026-09-14-branch-and-worktree-gate` 的 R7 一致。

### 能力留痕必填

- R6：把 Plan 的该节从「可选」改为**必填**：`artifacts.md` 的 Plan 大纲与 `hooks/task promote` 生成的骨架都改为 `## Skills / Tools Used`（去掉 `(Optional)`），并固定两种合法填法：列出实际调用的能力及其用途/结论，或写一行 `Unaided — no capability applied to this phase; considered: <按概念类列出的候选>`（措辞见 Open Questions）。
- R7：`SKILL.md` 的相应段落与必填节对齐：明确「未调用也必须记录一行」，补上落点，不改「是否调用」的判定自由。
- R8：不改 `## Skills / Tools Used` 在既有文档里的历史内容；`TaskFlowDocs/achieved/` 只读。

### 错位可见（只读报告）

- R9：`hooks/repository-check` 增加一段**只读**报告：列出当前工作树里的任务产物，并标出与当前分支不匹配的那些——正在写的任务目录（或 `todo.md` 里 `Status` 为 `promoted` / `in_progress` 的条目）在**别的分支**上被修改时，打印一行指认。它只报告，不阻断、不改状态、不影响既有退出码语义之外的判定。
- R10：该报告不得把「干净状态」或「正常的单任务工作区」报成问题；`repository-check` 在干净树上的既有输出与退出码不变（`hooks/smoke-test:582` 一节必须继续通过）。
- R11：`hooks/smoke-test` 覆盖该报告：一个「当前分支与任务目录不匹配」的 fixture 要打印指认行；干净树不打印；新增断言逐条 mutation 验证。

## Acceptance Criteria

- A1：`SKILL.md` 在阶段 1 之前（`### Todo → PRD → Spec → Plan` 或其紧邻处）写明隔离先于第一份任务文档，并给出 `git worktree add .worktrees/<slug> -b <type>/<slug> <base>`；阶段 5 只剩确认语义。
- A2：`CONTRIBUTING.md` 的 worktree 段落含可原样运行的命令，且不把 worktree 说成「多任务时才需要」。
- A3：`README.md` 与 `README.zh-CN.md` 的隔离句仍行为对齐（`CODE_STYLE.md:8`）。
- A4：`.gitignore` 含 `.worktrees/`，且 `git status` 在存在三个 worktree 的情况下不再把 `.worktrees/` 报成未跟踪。
- A5：`hooks/task promote` 新建一个 small 任务后，生成的 `plan.md` 含 `## Skills / Tools Used`（无 `(Optional)`）；`artifacts.md` 同样去掉，并写明两种合法填法。
- A6：`hooks/repository-check .` 在当前（错位）工作树上打印指认行；在一个干净的单任务 fixture 上不打印，且退出码与现状一致。
- A7：`bash hooks/smoke-test` 全绿；新增断言逐条 mutation 验证变红（把模板改回 `(Optional)`、去掉错位报告 → 各自变红）。
- A8：`hooks/task` 只改骨架文本，不改 ID/状态/解析逻辑（`== task lifecycle dispatcher ==` 既有断言不变）。
- A9：全部 hook 在 `bash:3.2` 容器下 `bash -n` 通过；`git diff --check` 干净。

## In Scope

- `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`skills/taskflow/references/runtime.md`（若清单需要同步）
- `hooks/task`（仅 `promote` 的骨架文本）、`hooks/repository-check`、`hooks/smoke-test`
- `CONTRIBUTING.md`、`README.md`、`README.zh-CN.md`、`.gitignore`

## Out of Scope

- 不改「用哪个能力」的判断标准，不把某个能力写成必用，不引入 provider 清单。
- 不给已完成/已归档任务回填空节（历史只读）。
- 不做阶段 5/6 的强制执行（`executing-plans`、`verification-before-completion` 等）。
- 不新增自动 gate：`hooks/task` 不创建分支/worktree，`repository-check` 不阻断。
- 不自动恢复或搬运既有错位产物（本轮 B/C/E 的搬迁按簿记 PR 单独处理）。
- 不改 `hooks/merge-todo` / `install-merge-driver` / `todo-check`。

## Risks / Deferred Items

- **一律 worktree 增加每任务一步开销**：代价是每个任务多一条 `git worktree add`，换来主 checkout 永远干净。若实践中发现单任务场景过于笨重，回退点是退回「多任务时才开」——但那会重新引入共享 checkout，故保留为风险接受。
- **必填记录可能变成走过场的样板**：风险是每次都写同一行 `Unaided — …` 而不真去枚举。缓解是要求那一行必须点名按概念类考虑的候选，而不是空话；这仍是纪律问题，文档规则兜不住态度，Retained。
- **错位报告的判定边界**：`repository-check` 需要判断「任务目录属于哪个分支」，而 Todo 条目不携带分支信息。实现只能靠「该目录是否已被提交、提交在哪个分支上」来推断；未跟踪目录无法归属，这类情况按「不属于当前 checkout 的未提交产物」单独一行报出，不做更强断言。这条边界写进报告输出，避免误读。
- **与 `(Optional)` 的兼容**：历史上带 `(Optional)` 的 Plan 不会被改（只读）；新骨架不带，混合状态是本任务接受的现状。
- **`hooks/repository-check` 是本仓库自己的治理检查**，改动它会影响这一仓库的日常输出；报告措辞需要克制，避免每次都刷一屏。

## Open Questions

- 未调用时的固定措辞用哪一句？候选：`Unaided — no capability applied to this phase; considered: <list>`。若你更想用中文值或别的形状，请在批准时给出。
- `repository-check` 的指认行放在既有 `Working tree: has changes` 之后，还是新增一段 `Task artifacts:`？倾向于后者——既有行是通用状态，任务错位是另一类信息。

## Version History

- v1 — planning. 并入「隔离提前到阶段 1 + 每任务一个 worktree」与「`repository-check` 报告错位任务产物」两条线（用户 2026-09-16 决定）；原 v1 只含能力留痕。
