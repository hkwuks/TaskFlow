# 任务 ID 没有校验，误建的任务也没有退路

> Task version: v1
> Status: checking

## Goal

给 `hooks/task` 和两个独立 hook 里所有接受「任务名」的入口加一条统一的形状校验，并补一个真正能撤销误得 promotion 的命令。

今天这些入口把用户给的字符串直接拼进文件系统路径，拼完再判存在性。所以 `--size` 会变成目录名，`../evil` 会在 `TaskFlowDocs/` 之外建出一个**完整可用**的任务目录，`../../escaped` 能建到仓库外。更糟的是 `promote` 往往**成功**：候选条目变成 `promoted`，而 `task remove` 明确拒绝撤销已 promote 的条目，于是 CLI 没有任何回头路，只能手改 `todo.md`。

## Background / Confirmed Facts

以下均在隔离的 `/tmp` 仓库里实测（2026-10-20，基线 `bf29cd9`），不污染本仓库：

- `hooks/task:710` 取 `task="${rest[1]}"`，`:742` 拼 `base="$docs/$task"`，`:758` 直接 `mkdir -p "$base"`。中间没有任何字符集或形态判断。
- `:741` 的存在性检查 `[ -e "$root/TaskFlowDocs/$task" ]` 跑在拼接**之后**，所以它顺带承担了校验的角色：`..` 因为指向已存在的 `TaskFlowDocs/` 被侥幸拦住，`../evil` 因为不存在而放行。
- 实测 `promote … ../evil small` → `mkdir` 建出仓库根下的 `evil/`，内含 `prd.md` + `plan.md`；`task state ../evil in_progress` 能走到「current Task version is not approved」这一步。也就是说仓库外那个目录是一个**功能完整**的任务。
- 实测 `promote … ../../escaped small` → `/tmp/escaped/` 被创建。
- 实测 `promote … --size small` → `promote OK: TF-… -> --size (small)`，退出码 0。`--size` 落到第三个位置成了 size，`small` 落到第二个位置成了 task-id 的一半——标志位错位并不会必然报错。
- `hooks/archive:12` 和 `hooks/reopen:22` 同样是 `task="$1"` 直接拼路径。`hooks/archive` 以 `mv` 收尾（`:52`），能把仓库外的目录搬进 `achieved/`。实测 `bash hooks/archive ""` 输出 `achieved/ already exists` 并以 0 退出——空任务名的失败信息读起来像成功。
- `findsec()`（`hooks/task:120-127`）的任务匹配用的是子串 ``` `TaskFlowDocs/<task>/` ```。v1 认为这是**真漏洞**：`<task> = a/b` 会匹配到 `TaskFlowDocs/a/b/`，但 `<task> = b` 也会匹配到同一个字符串。不过这个缺陷只在越界路径已经存在之后才有意义，形状校验先行堵住，因此列为 Follow-up 而不是本任务范围。
- 现状普查：`TaskFlowDocs/achieved/` 下 79 个目录，**全部**符合 `^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$`；`todo.md` 里全部 `- Task:` 路径也都是合规 slug。所以严格校验对本仓库现存的真实任务是零影响的。
- `hooks/task:282-290` 的重复目标检查遍历 `hc`（全部条目），**不区分状态**。所以把误 promote 的条目状态改回 `clarified` 而不清空 `Goal`，会让目标语句永远无法再次 intake。这是 `unpromote` 必须恢复 `Status: inbox` 的理由。
- `todo-check` 在 merge 上能抓到丢条目（实测 `TF-1 present in <parent> but missing from <head>`，`STATUS: needs-user-input`），**但在非 merge 提交上什么也不比**（实测输出 `1 parent(s): not a merge commit; nothing to compare.`）。所以手工 `git checkout` 或手删条目的那条「退路」没有任何检查兜底——这正是它不该被当作退路的实证。
- 证据库（`<absolute-git-dir>/taskflow/`）是每 worktree 一份，`promote` 的 templates 是**确定性**的（`hooks/task:758-837` 只有 `# $title`、`## Goal` 的值和 size 分支会变）。因此「这个目录是 promote 造的」可以被逐字节判定，而不用猜。

## Requirements

1. 新增一个共享的校验器，同时供 `hooks/task`、`hooks/archive`、`hooks/reopen` 使用。规则：任务名必须匹配 `^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9][a-z0-9-]*$`。
2. 校验覆盖**所有**读写入口，不只是会建目录的那一个：`hooks/task` 的 `promote`、`state`、`progress`、`approve`、`complete`、`unpromote`，以及 `hooks/archive`、`hooks/reopen`。
3. 拒绝时给出可执行的下一步，而不是只说「非法」：说明期望形状，并在可行的命令里补 `<YYYY-MM-DD>-<slug>` 形态的示例。
4. 新增 `task unpromote <todo-id> <reason>`，作为 `promote` 的逆运算：删除该次 promotion 建出的目录，把 Todo 条目恢复成可再次 promote 的状态。
5. `unpromote` 必须拒绝那些「删掉目录会丢东西」的情况，并说明该走哪条路代替：目录里有未被跟踪的文件、目录内容与 promote 模板不逐字节一致、Plan 已被批准过、Todo 的 `- Task:` 指向的不是这个 id。
6. `promote` 的输出与 `unpromote` 的输出都在最后一行给出 `promote OK:` / `unpromote OK:` 形式，`unpromote` 附带一句「Todo 条目已可再次 promote」。
7. 文档同步：`hooks/README.md` 的 hooks 树、`skills/taskflow/SKILL.md` 里列举这些命令的位置，以及 `CONTRIBUTING.md` 若已提到 `promote` 的约束处。

## Acceptance Criteria

- 对 `--size`、`../evil`、`../../escaped`、`a/b`、`-rf`、空串这六个输入，`task promote` 一律退出非 0、不创建任何目录（含仓库外）、不改 `todo.md`。断言用「执行前后 `todo.md` 的 digest 相同且目标路径不存在」来表达。
- 同一个校验对 `task state`、`task progress`、`task approve`、`task complete`、`hooks/archive`、`hooks/reopen` 同样生效：每个都给出一条非 0 退出的断言。
- 一个合规但形如 `2026-10-20-` 的尾巴（缺 slug）被拒；`2026-10-20-a` 被接受。这是校验器的正反两个方向。
- `task unpromote` 在「刚 promote 出来的目录」上成功：目录消失，Todo 条目的 `Status` 回到 `inbox`、`Task` 回到 `Not promoted.`、`Next action` 回到 `Clarify and promote when ready.`，且条目里出现一行说明这次撤销的记录。
- `task unpromote` 拒绝时说明该走哪条路，并**不删任何东西**：目录里有被 Git 跟踪的文件、Plan 的 `## Approval` 不是 `requested`、`prd.md`/`plan.md` 的 `> Status:` 不是 `planning`、Todo 的 `- Task:` 指向的不是这个 id、条目不是 `promoted` 状态。每一种各一条断言。
- `bash hooks/smoke-test` 通过；每个新增断言都有一条只由它变红的变异。
- `bash hooks/todo-check .`、`bash hooks/repository-check .` 在本仓库为 `pass`。

## In Scope

- `hooks/task`：共享校验器、`promote`/`state`/`progress`/`approve`/`complete` 接入、新增 `unpromote` 子命令。
- `hooks/archive`、`hooks/reopen`：入口校验。
- `hooks/smoke-test`：上述两个方向的断言，以及把 3 个不合规的夹具任务名改成带日期的形态。
- `hooks/README.md`、`skills/taskflow/SKILL.md`、`CONTRIBUTING.md`（若相关）。

## Out of Scope

- **修 `findsec` 的子串匹配。** 它是真缺陷，但形状校验通过之后 `a/b` 已经进不来，剩下的暴露面需要单独的判断（严格 slug 之外要不要保留对历史目录的兼容）。记录为 Follow-up。
- **自动删除分支、worktree 或任何 Git 状态。** `unpromote` 只动 `TaskFlowDocs/` 与 `todo.md`，与现有 hook 的边界一致。
- **自动修已经误建的任务（如果用户现场存在）。** 本仓库普查结果是没有，所以不需要迁移脚本。
- **放宽 `task remove` 对已 promote 条目的拒绝。** 那条拒绝是对的：直接删条目会让任务目录变成 orphan。`unpromote` 是另一个动作。

## Risks / Deferred Items

- **严格形状会拒掉未来的合法 ID 变体。** 本仓库约定是 `YYYY-MM-DD-short-slug`（`SKILL.md` 的 Safety 段）。如果将来出现带大写或下划线的合法任务，这条校验会误拦。缓解：拒绝信息里明确写出期望形状，改规则时只改一处。
- **smoke 夹具改名会削弱一个已有断言。** `promoted-in-base` / `promoted-in-worktree` 这类名字本身在断言「promote 在 base 树被拦、在 worktree 通过」，改名不影响被断言的行为，但 diff 会碰 3 个既有夹具；每处都要确认断言仍然指向同一件事。
- **`unpromote` 会删掉「改了正文但没改状态」的目录。** 判据是四条状态（条目仍 `promoted`、目录未被 Git 跟踪、文档仍 `> Status: planning`、`## Approval` 仍 `requested`），它们都与模板措辞无关——这是刻意选的，否则改一个标点就会让所有旧 promotion 转向拒绝。代价是一个刚写了正文、还没动状态的任务目录会被判成「空架子」。缓解：删除前把目录里的文件清单打给调用者，成功输出点明删了什么；这是**可见**的删除，不是静默的。
- **`unpromote` 不检查分支/worktree。** 如果任务已经在自己的分支上提交过，删目录是一次 Git 改动，应由人决定。因此判据是「目录内所有文件都未跟踪」——已提交过的目录自然会被拒。

## Open Questions

无阻塞项。三项设计选择已由用户于 2026-10-20 决定：严格形状校验、新增 `unpromote` 子命令（而非放宽 `remove`）、校验覆盖全部读写入口。
