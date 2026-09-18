# Isolate a task before its documents are written, and make the choice auditable
> Task version: v1
> Status: completed

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
- 仓库已经在用 `.worktrees/<slug>` 这一约定（`.worktrees/hook-gates`、`.worktrees/no-python-hooks`、`.worktrees/todo-merge-driver`，本任务实施时又加了 `web-ui-merge-loss-guard`、`duplicate-todo-id`）。
- **本 PRD v1 在这里写错过一次，实施期订正**：原文写「`.gitignore` **没有**忽略 `.worktrees/`」，并据此推出 A4「`git status` 会把它报成未跟踪」。前半句字面为真（受版本控制的 `.gitignore` 从未含 `worktrees`，见 `git log -p -- .gitignore`），**后半句是错的**：这个 clone 的 `.git/info/exclude` 已经有 `.worktrees/`（第 7 行），实测 `git check-ignore -v .worktrees/foo` → `.git/info/exclude:7`，`git status --untracked-files=all -- .worktrees` 为空。所以**今天没有任何噪声**。
- 剩下的真实缺口只是**范围**：`.git/info/exclude` 是每个 clone 各自的本地文件、不进版本控制（`git ls-files --error-unmatch .git/info/exclude` 失败即为证）。**新 clone 里没有这一行**，实测（`git clone` 到临时目录后建 `.worktrees/x/f`）：`git check-ignore -v .worktrees/x/f` → 未命中；`git status --porcelain --untracked-files=all -- .worktrees` → `?? .worktrees/x/f`。即噪声真实存在，只是不在**这个** clone 里。因此把 `.worktrees/` 写进受版本控制的 `.gitignore` 的**动机是「让约定随仓库分发」，不是「修今天的噪声」**——两者强度不同，本任务的验收标准按前者写。
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
- worktree 放在 `.worktrees/<slug>`，并把 `.worktrees/` 加进受版本控制的 `.gitignore`。
- 检查落在 `hooks/repository-check`，**只读报告**。
- **2026-09-17 追加决定**：只读报告不够，(a) 升级为 (b)——`hooks/task promote` 在**非 linked worktree** 里直接拒绝。理由：报告只在有人主动跑 `repository-check` 时才可见，最自然的出错路径（在主 checkout 直接 `promote`）不会被它挡住，正是本任务要根除的形态。判定用 Git 自身的事实——`$(git rev-parse --git-dir)/commondir` 是否存在——不需要解析分支名或推断归属。

## Requirements

### 隔离提前（根因）

- R1：`skills/taskflow/SKILL.md` 的隔离规则从阶段 5 提前到**阶段 1 之前**：在创建任何 `TaskFlowDocs/<slug>/` 文档或 `todo.md` 条目**之前**，任务已经拥有自己的分支与工作树。阶段 5 保留一句「确认隔离仍然成立」，不再承载「第一次建隔离」的语义。
- R2：**一律每任务一个 worktree**，不再以「同时有多个任务」为条件；`git worktree add .worktrees/<slug> -b <type>/<slug> <base>` 是给出的命令形状。主 checkout 从此停在 base 分支且保持干净。
- R3：`CONTRIBUTING.md` 的「Working branches」一节补上 worktree：分支规则不变（前缀、base、动手前先建），但明确「需要隔离的不止是代码，还包括任务文档」，并给出 worktree 命令。`README.md` / `README.zh-CN.md` 各一句保持行为对齐（`CODE_STYLE.md:8`）。
- R4：把 `.worktrees/` 写进**受版本控制的** `.gitignore`，使该约定随仓库分发而不是只存在于本 clone 的 `.git/info/exclude`；`.worktrees/<slug>` 成为记录在 `plan.md` `## Preconditions` 里的约定值（该节已有「分支」项，补「工作树」）。
- R5：`hooks/task` 的 `promote` 新增**隔离 gate**：当工作树不是 linked worktree 时拒绝并 `STATUS: blocked` 退出 `3`，提示先 `git worktree add`。判定信号是 `commondir` 文件的存在性，不是分支名。被拒时的输出给出可粘贴的命令，**填好脚本已知的部分**（`<task-id>` 取自参数、`<base>` 取自该工作树的当前分支），只把 `<type>` 留成占位符并列出合法值（`feature|fix|docs|chore`）——前缀由读输出的 Agent 或人按任务语义选，脚本不猜（理由见 Resolved During Review）。`promote` 的其它既有行为（拒绝已存在目的地、拒绝重复 promote、`small` 生成 `No spec required` 行）不变。
- R6：gate 必须**不误伤既有 fixture**：`--root <path>` 指向的目录若不是一个 Git 仓库（`git rev-parse --show-toplevel` 失败），gate 不适用、照常放行——否则 `hooks/smoke-test` 现有的两个 fixture 与用户在没有 Git 的目录里使用都会被打断。gate 只在「**确实在一个 Git 仓库里、且那个工作树不是 linked worktree**」时拒绝。
- R7：`intake` **不拒绝**，但要在同一个共享工作树上补一句反馈。理由：本任务要修的根因里，把 `git checkout main` 挡住的正是 `intake` 写脏的未提交 `todo.md`（实测报错即 `TaskFlowDocs/todo.md`），而 `promote` 只写任务目录。所以「`intake` 只动 `todo.md` 所以不必管」是错的。但纯 triage 不该被逼着先建 worktree——一个可能永远不会被计划的 inbox 条目，为它开工作树是过度。取中间：`intake` 照常写入，**在输出末尾**（`intake OK: <id>` 之后）加一行提示，说明 `todo.md` 现在是未提交改动、切分支/checkout 前需先提交或 stash，且该行只在**非 linked worktree** 里出现。该提示不改退出码（仍为 `0`）、不阻断、对 `--root` 指向非 Git 仓库时同样不适用。
- R8：gate 与提示共用同一个判定（一个 helper），避免两处逻辑漂移。

### 能力留痕必填

- R9：把 Plan 的该节从「可选」改为**必填**：`artifacts.md` 的 Plan 大纲与 `hooks/task promote` 生成的骨架都改为 `## Skills / Tools Used`（去掉 `(Optional)`），并固定两种合法填法：列出实际调用的能力及其用途/结论，或写一行 `Unaided — no capability applied to this phase; considered: <按概念类列出的候选>`（措辞见 Open Questions）。
- R10：`SKILL.md` 的相应段落与必填节对齐：明确「未调用也必须记录一行」，补上落点，不改「是否调用」的判定自由。
- R11：不改 `## Skills / Tools Used` 在既有文档里的历史内容；`TaskFlowDocs/achieved/` 只读。

### 错位仍可见（只读报告，作为 gate 的补充）

- R12：`hooks/repository-check` 增加一段**只读**报告：列出当前工作树里的任务产物中与当前分支不匹配的那些。gate 与提示只在命令跑的那一刻起作用，报告覆盖其余情形（例如产物已经写进去之后才切分支、或手工复制进来的目录）。它只报告，不阻断、不改状态、不设置 `needs`。
- R13：该报告不得把「干净状态」或「正常的单任务工作区」报成问题；`repository-check` 在干净树上的既有输出与退出码不变（`hooks/smoke-test:582` 一节必须继续通过）。
- R14：`hooks/smoke-test` 覆盖 gate、提示与报告：linked worktree 里 `promote` 放行；**同一个仓库的主工作树**里 `promote` 被拒且退出 `3`、没有产生任何文件；非仓库的临时目录里 `promote` 放行（R6）；非 linked worktree 里 `intake` 成功（退出 `0`）且输出含提示行，linked worktree 里同一命令**不含**提示行；报告的错位 fixture 打印指认行、干净 fixture 不打印。新增断言逐条 mutation 验证。

## Acceptance Criteria

- A1：`SKILL.md` 在阶段 1 之前（`### Todo → PRD → Spec → Plan` 或其紧邻处）写明隔离先于第一份任务文档，并给出 `git worktree add .worktrees/<slug> -b <type>/<slug> <base>`；阶段 5 只剩确认语义。
- A2：`CONTRIBUTING.md` 的 worktree 段落含可原样运行的命令，且不把 worktree 说成「多任务时才需要」。
- A3：`README.md` 与 `README.zh-CN.md` 的隔离句仍行为对齐（`CODE_STYLE.md:8`）。
- A4：`.gitignore` 含 `.worktrees/`，且该行**来自受版本控制的文件**——`git check-ignore -v .worktrees/foo` 的输出前缀是 `.gitignore:<行号>:` 而不是 `.git/info/exclude:<行号>:`。**不断言**「`git status` 不再报未跟踪」：本 clone 的 `info/exclude` 已经让它不报，那条断言今天就是绿的，证明不了任何事；而 `check-ignore -v` 的来源前缀正好把「哪个文件命中」摆出来，这就是要验的东西。新 clone 也成立这一条，用 `git clone` 到临时目录后重跑同一个断言来验（临时 clone 天生没有本地 `info/exclude` 那一行）。**注意**：`core.excludesFile=/dev/null` **不能**用来模拟——Git 始终读 `.git/info/exclude`，该设置只关掉全局 excludesFile，实测加不加它都仍然命中 `info/exclude`。
- A5：`hooks/task promote` 在 linked worktree 里放行、在**同一仓库的主工作树**里拒绝（`STATUS: blocked`，退出 `3`），且被拒时 `TaskFlowDocs/<slug>/` 与 `todo.md` 都未被创建/修改；在**不属任何 Git 仓库**的目录里放行（R6）。被拒的输出里 `<task-id>` 与 `<base>` 已是真值、`<type>` 仍是字面占位符，且列出四个合法前缀——即命令可直接复制粘贴，只剩前缀待选。
- A6：`hooks/task intake` 在**非 linked worktree** 里成功（退出 `0`）并在输出末尾给出 `todo.md` 已变脏的提示；在 linked worktree 里同一命令不出现该提示；在非 Git 目录里不出现该提示。
- A7：`hooks/task promote` 新建一个 small 任务后，生成的 `plan.md` 含 `## Skills / Tools Used`（无 `(Optional)`）；`artifacts.md` 同样去掉，并写明两种合法填法。
- A8：`hooks/repository-check .` 在一个错位工作树上打印指认行；在干净的单任务 fixture 上不打印，且退出码与现状一致。
- A9：`bash hooks/smoke-test` 全绿；新增断言逐条 mutation 验证变红（去掉 gate、把 gate 改成无条件拒绝、去掉 intake 提示、把提示改成无条件打印、把模板改回 `(Optional)`、去掉错位报告 → 各自变红）。
- A10：`hooks/task` 除 `promote` 的隔离 gate、`intake` 的提示行与骨架文本外不改其它逻辑——`state` / `progress` / `complete` 的既有断言（`== task lifecycle dispatcher ==`）不变。
- A11：全部 hook 在 `bash:3.2` 容器下 `bash -n` 通过；`git diff --check` 干净。

## In Scope

- `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`skills/taskflow/references/runtime.md`（gate 与清单同步）
- `hooks/task`（`promote` 的隔离 gate + 骨架文本）、`hooks/repository-check`、`hooks/smoke-test`
- `CONTRIBUTING.md`、`README.md`、`README.zh-CN.md`、`.gitignore`

## Out of Scope

- 不改「用哪个能力」的判断标准，不把某个能力写成必用，不引入 provider 清单。
- 不给已完成/已归档任务回填空节（历史只读）。
- 不做阶段 5/6 的强制执行（`executing-plans`、`verification-before-completion` 等）。
- **`promote` 硬 gate + `intake` 提示**，两者都不扩散到 `state` / `progress` / `complete`：这三个操作的对象已经存在于某个工作树里，按工作树拒绝会打断正常的收尾流程。`intake` 只提示不拒绝（理由见 R7）。这是有意的覆盖面取舍，不是遗漏。
- 不自动创建分支或 worktree：gate 只拒绝并给出命令，不代跑 `git worktree add`。
- 不改 `intake` 的退出码、写入内容与去重逻辑——提示行只加在输出末尾。
- 不自动恢复或搬运既有错位产物（本轮 B/C/E 的搬迁按簿记 PR #29 处理，已合入）。
- 不改 `hooks/merge-todo` / `install-merge-driver` / `todo-check`。
- **不动 `.git/info/exclude`**：它是这个 clone 的本地文件，本任务只往受版本控制的 `.gitignore` 加一行，让新 clone 也成立；已存在的本地行保留（重复的忽略规则无害）。

## Risks / Deferred Items

- **一律 worktree 增加每任务一步开销**：代价是每个任务多一条 `git worktree add`，换来主 checkout 永远干净。若实践中发现单任务场景过于笨重，回退点是退回「多任务时才开」——但那会重新引入共享 checkout，故保留为风险接受。
- **gate 改变了一个既有命令的可用性**：`hooks/task promote` 过去在主 checkout 里能用，现在会被拒。这是本任务的目的，但属于破坏性变更，需要在 `runtime.md` 的 `promote` 行与 `CONTRIBUTING.md` 里写明，否则使用者会以为命令坏了。已在 R1/R3 的文档改动里覆盖。
- **`intake` 的提示是软的**：它只说，不拦。真实路径是：有人看完提示还是接着 `git checkout main` → 被 `todo.md` 挡住 → 自己去 stash。提示把信息提前给出，但不消除这一步。这是 R7 选择「不拒绝 triage」的代价，接受。
- **gate 的报错会随仓库的分支前缀约定而过时**：文案里列的 `feature|fix|docs|chore` 抄自本仓库 `CONTRIBUTING.md`。换一个用别的约定（例如 `feat/`）的仓库，那句提示就与它自己的规则不符。这是文档化的取舍——hook 不读 `CONTRIBUTING.md` 来提取约定（那需要解析自然语言），选择给出本仓库的合法值并接受它在别处可能需要手改。若哪天要通用，做法是从仓库文档读前缀而不是硬编码。
- **triage 与计划的边界靠人判**：`intake` 不拒、`promote` 拒，意味着「先 intake 一批 idea、之后再逐个 promote」这种用法要求每次 promote 前都在 worktree 里。若实践中发现 intake 也常在主 checkout 里被当成半成品用（即 intake 完立刻 promote），说明两者该一起 gate——那时再改。
- **gate 的判定是「工作树形态」而非「这是哪个任务」**：它在 `.worktrees/anything` 里都放行，不检查该 worktree 是不是为这个 `<task-id>` 建的。更严的判定需要 Todo 携带分支信息，不在本任务内。这是有意的边界：拦的是「在共享树里写文档」，不是「在错的 worktree 里写」。
- **不做 linked worktree 时的 `--root` 语义**：gate 用 `git -C "$root" rev-parse` 判定，因此判定的是 `$root` 那个仓库的形态，而不是进程的 CWD。若某天需要「CWD 与 `--root` 不一致也拒绝」，是另一个任务。
- **必填记录可能变成走过场的样板**：风险是每次都写同一行 `Unaided — …` 而不真去枚举。缓解是要求那一行必须点名按概念类考虑的候选，而不是空话；这仍是纪律问题，文档规则兜不住态度，Retained。
- **错位报告的判定边界**：`repository-check` 需要判断「任务目录属于哪个分支」，而 Todo 条目不携带分支信息。实现只能靠「该目录是否已被提交、提交在哪个分支上」来推断；未跟踪目录无法归属，这类情况按「不属于当前 checkout 的未提交产物」单独一行报出，不做更强断言。这条边界写进报告输出，避免误读。
- **与 `(Optional)` 的兼容**：历史上带 `(Optional)` 的 Plan 不会被改（只读）；新骨架不带，混合状态是本任务接受的现状。
- **`hooks/repository-check` 是本仓库自己的治理检查**，改动它会影响这一仓库的日常输出；报告措辞需要克制，避免每次都刷一屏。

## Open Questions

- 未调用时的固定措辞用哪一句？候选：`Unaided — no capability applied to this phase; considered: <list>`。若你更想用中文值或别的形状，请在批准时给出。
- `repository-check` 的指认行放在既有 `Working tree: has changes` 之后，还是新增一段 `Task artifacts:`？倾向于后者——既有行是通用状态，任务错位是另一类信息。

## Resolved During Review

- **gate 报错文案（2026-09-17 定）**：`<type>` 是 `CONTRIBUTING.md` 自己的分支前缀词汇（`feature`/`fix`/`docs`/`chore`），脚本推不出来也不该去猜——按目标文本猜前缀是启发式，与插件「不做猜测」的一贯做法冲突。但**不需要**脚本猜：读这段输出的是 Agent（或人），语义判断本来就在它那一侧。所以脚本给出**填好能填的部分**、把唯一不可推断的那一段留成占位符并列出合法值即可：
  ```
  Blocked: this is the base working tree, not a task worktree.
  Create one and rerun promote from inside it:
    git worktree add .worktrees/<task-id> -b <type>/<task-id> <base>
  <base> is the current branch here (filled in below); <type> is one of
  feature | fix | docs | chore, chosen from what the task changes.
  ```
  其中 `<task-id>` 取自 `promote` 的第二个参数，`<base>` 取自 gate 触发时该工作树的当前分支——这两项脚本都知道，实际打印时替换为真值，只有 `<type>` 保持字面占位符。这样报错既不含猜测，也不需要读它的人自己拼命令。

## Version History

- v1 — planning. 并入「隔离提前到阶段 1 + 每任务一个 worktree」与「`repository-check` 报告错位任务产物」两条线（用户 2026-09-16 决定）；原 v1 只含能力留痕。
- v1（实施前订正，仍为 v1）——修正 Background 的一处事实错误：原文称 `.gitignore` 没忽略 `.worktrees/`「所以 `git status` 会报未跟踪」，实测本 clone 的 `.git/info/exclude` 已含该行、无任何噪声。A4 据此改写：不断言一条今天就已经绿的 `git status`，改为断言该规则来自受版本控制的文件（`git check-ignore -v` 指回 `.gitignore`），R4 补上「随仓库分发」的动机，并把「不动 `.git/info/exclude`」写进 Out of Scope。范围与结论不变，只是依据从「修噪声」改成「让约定分发」。发现于 2026-09-17 任务 B 建 worktree 时。
- v1（2026-09-17 追加决定，仍为 v1）——检查从「只读报告」升级为「报告 + `promote` 隔离 gate」（用户选 b）：新增 R5（gate）、R6（不误伤非仓库 root）、R14（smoke 覆盖 gate 与报告），原 R6–R11 顺延，A5–A10 重编号并补 gate 的验收，Out of Scope 补「gate 只装在 `promote` 上」与「不自动建 worktree」，Risks 补 gate 的破坏性与判定边界。
- v1（2026-09-17 补 `intake` 提示，仍为 v1）——原 Out of Scope 的理由「`intake` 只动 `todo.md`，所以不必管」是**错的**：把 `git checkout main` 挡住的正是 `intake` 写脏的未提交 `todo.md`，而 `promote` 只写任务目录。改为 `promote` 硬 gate + `intake` 非阻断提示（用户选 c）：新增 R7（提示）、R8（共用判定 helper），R9–R14 顺延（原 R7–R12），A6 拆出 `intake` 提示的验收（A5–A11），Risks 补「提示是软的」与「triage/计划边界靠人判」，Out of Scope 的该条改写并补「不改 intake 的退出码与写入内容」。
- v1（2026-09-17 定 gate 文案，仍为 v1）——`<type>` 前缀的处置定案（用户指出语义判断在 LLM 侧）：脚本填好 `<task-id>` 与 `<base>`、只把 `<type>` 留成占位符并列出 `feature|fix|docs|chore`，不猜前缀。R5 与 A5 补上输出形态的验收，Open Questions 该条移入 Resolved During Review，Risks 补「前缀列表会随仓库约定过时」。
- v1（2026-09-18 实施期订正 Background 措辞，仍为 v1）——Background 后果一/后果二与 R7 把两种未提交产物混为一句「checkout 被挡住」。实测（`/tmp` 下五个最小仓库）分开成两件事：**被修改的已跟踪文件**（`todo.md`，即 `intake` 的形态）确实让 `git checkout` 失败（`would be overwritten by checkout`）；**未跟踪的任务目录**不阻塞 checkout，除非目标分支正好跟踪同一路径，它的真实危害是**跟着你跨分支走**。结论与范围不变（`intake` 提示、`promote` gate、`repository-check` 报告都不动），只是 R12 那条报告的输出措辞与对应断言按实测改写。发现于 Step 3 写报告尾注时。
