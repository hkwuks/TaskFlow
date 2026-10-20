# Spec — 任务 ID 校验与 promote 的逆运算

> Task version: v1

## Objective and Success Criteria

两个交付物，一个边界、一个接口：

1. **共享任务名校验器** —— 一个文件，被三个 hook 共用，是任务名进文件系统之前的唯一一道判断。
2. **`task unpromote`** —— `promote` 的逆运算，带一份明确的拒绝清单。

成功标准是 PRD 的 Acceptance Criteria：六个坏输入不产生任何副作用；`unpromote` 在「刚 promote 出来」的目录上成功、在四类「删了会丢东西」的情况下拒绝且不删。

## Architecture Boundaries and Responsibilities

| 组件 | 职责 | 不做什么 |
| --- | --- | --- |
| `hooks/task-id` | 判断一个字符串是不是合法的任务名；把不合法的转成退出码与一段人话 | 不读文件系统、不判断该任务是否存在、不改任何东西 |
| `hooks/task` | 在所有取任务名的子命令入口调用校验器；实现 `unpromote` | 不重复实现校验规则 |
| `hooks/archive` / `hooks/reopen` | 同样在入口调用校验器 | 同上 |
| `unpromote` | 删目录、复位 Todo 条目 | 不碰 Git（分支、worktree、索引）、不删非任务文件 |

`hooks/task-id` 是**可执行文件**，与 `json-field` 同一个先例：`hooks/README.md:23` 已经把 `json-field` 描述成「shared one-level JSON reader for the two hooks above」。理由相同——`hooks/` 里没有任何文件 source 另一个文件（`grep` 全仓确认），而校验规则必须只有一份。`hooks/task` 已有 `SCRIPT_DIR`，`hooks/archive`/`hooks/reopen` 各加一个等价常量即可。

## Project Structure / Affected Files

```text
hooks/task-id       新增：校验器（可执行）
hooks/task          接入 6 处 + 新增 unpromote 子命令
hooks/archive       入口校验
hooks/reopen        入口校验
hooks/README.md     hooks 树补一行
hooks/smoke-test    新增断言；3 个夹具改名
skills/taskflow/SKILL.md   命令列举处补 unpromote 与校验约束
CONTRIBUTING.md    若提到 promote 的约束处同步（视实际内容）
```

## Interfaces, Data Flow, and Contracts

### 校验器

```text
usage: hooks/task-id <candidate>
exit 0  — 合法
exit 1  — 不合法，stderr 一行说明期望形状
```

规则：`^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9][a-z0-9-]*$`

读的是 `$1`，不读 stdin：调用点全都是位置参数，stdin 形态只会让每一处多一行管道。

**为什么是这条正则，而不是「拒空值/拒前导点/拒斜杠」：** 宽松版留下的 `2026-10-20-Typo`、`foo` 这类笔误仍能建出目录，而它们正好是 `unpromote` 需要兜底的那一类。严格版会顺带拒掉这三样，所以宽松版的唯一优势消失，代价却留着。本仓库 79 个 achieved 目录全部符合严格形态（PRD Background），所以严格版对真实任务是零影响。

### 调用点契约

每处都在**取值之后、任何拼接之前**调用：

```sh
task="${rest[1]}"
bash "$SCRIPT_DIR/task-id" "$task" || exit 1   # task; the other two use their own equivalent
```

失败时直接以校验器自己的 stderr 与退出码收场，不再包一层 `fail`：它已经说出了非法值和期望形状，包一层只会把同一句话复制成两处文案。
```

`hooks/task` 用已有的 `SCRIPT_DIR`（不是计划里一度写错的 `HERE`）；`hooks/archive`、`hooks/reopen` 各加一个 `HERE`。

失败语义统一走 `fail()`（`hooks/task:24`，`exit 1`），与现有用法参数错误一致。**不用 exit 2**：CODE_STYLE 的 exit 2 留给「需要用户输入」，而一个形状错误的参数不是需要输入，是打错了。

### `task unpromote <todo-id> <reason>`

```text
usage: task unpromote <todo-id> <reason> [--root <path>]
输出：unpromote OK: <todo-id> (<task>)  然后一句说明条目已可再次 promote
```

契约按顺序：

1. 取条目，读 `Status`、`Task`。
2. **拒绝条件（任一命中即退出非 0，不写任何东西）**：
   - `Status` 不是 `promoted` → 「只有 promoted 的条目可以撤销」
   - `Task` 不是 ``` `TaskFlowDocs/<slug>/` ``` 形态 → 「条目没有指向可撤销的目录」
   - 那个目录有 `achieved/<slug>` 同名 → 「该任务已归档，走 reopen」
   - 目录里有**被 Git 跟踪**的文件（`git ls-files` 在该目录下有输出）→ 「目录内容已提交，用 Git 回退」
   - Plan 的 `## Approval` 不是 `- Status: requested` → 「这个任务已经进入过审批，不是误建的空架子」
   - `prd.md` / `plan.md` 的 `> Status:` 不是 `planning` → 同上
3. 通过后：`rm -rf` 那个目录；把 Todo 条目写回 `Status: inbox`、`Task: Not promoted.`、`Next action: Clarify and promote when ready.`、`Updated: <today>`；`Notes` 追加一行 `- Unpromoted <today>: <reason>`。
4. 复用现有的 `TASKFLOW_CMD=edit` 通道（`hooks/task:273-280` + `loadpairs`），不新写一套 Todo 改写。

**为什么 `Status` 回到 `inbox` 而不是 `clarified`：** 两者都保留原来的 `Goal`，所以**都不解决**重复目标问题——`intake` 的重复目标检查（`hooks/task:282-290`）看的是 Goal 字节，与状态无关。选 `inbox` 是因为它如实描述处境：条目被退回，还没重新澄清过。真正的后果是：`unpromote` 之后想用同一个目标语句重新 intake 会被 `duplicate Todo goal` 拒绝，正确做法是改这条条目的下一步动作（`task next`），或者说明为什么目标要换。这句话必须写进 `unpromote` 的成功输出，一句话，免得下一个 Agent 撞上。

这一点写进 `unpromote` 的成功输出里，一句话，免得下一个 Agent 撞上。

**为什么「刚 promote 出来」的判据用状态而不是字节比对：** `promote` 的模板是确定性的（PRD Background），本可以用 `cmp` 逐字节比。但那会让规则随模板文本漂移：模板改一个标点，所有旧 promotion 就转向拒绝。改判「没人动过它」——条目仍 `promoted`、目录未被 Git 跟踪、文档仍是 `> Status: planning`、`## Approval` 仍是 `requested`——四个条件都与模板措辞无关，且分别对应一种「有人开始干活了」。代价是：有人改了正文但没动状态时，`unpromote` 仍会删掉那份正文；所以成功输出里点明它删了什么，并且删之前把目录内容列给调用者。这一点记在 PRD Risks。

## Invariants and Compatibility

- **合法任务名集合只增不减地覆盖现存目录**：79/79 achieved 目录 + 全部 `- Task:` 路径通过校验（PRD Background 已普查）。实施后跑一次全量断言。
- **`promote` 的成功路径字节级不变**：合规名字下，生成的 prd/plan 与今天完全一致。smoke 的现有 promote 断言必须原样通过。
- **`task remove` 对已 promote 条目的拒绝不变**：`unpromote` 是并列动作，不是替代。
- **不引入兼容代码**：不为旧的宽松输入留旁路（`CLAUDE.md` 明确禁止未授权的兼容代码）。

## Validation and Error Semantics

| 触发 | 退出码 | 输出位置 |
| --- | --- | --- |
| 任务名形状非法 | 1（`fail`） | stderr，一行，含非法值与期望形状 |
| `unpromote` 拒绝 | 1（`fail`） | stderr，一行，含该走哪条路代替 |
| `unpromote` 成功 | 0 | stdout `unpromote OK: …` + 一句注意事项 |
| 校验器自身被误用（无参数） | 1 | stderr `usage: task-id <candidate>` |

## Code and Test Constraints

- POSIX `awk`/`sed` + bash 3.2，无 Python、无 `declare -A`、无 `mapfile`、无进程替换。与 `hooks/` 其余部分同一底线。
- 校验器必须能在 `bash -n` 与 `docker run bash:3.2 bash -n` 下通过。
- `hooks/smoke-test` 的「every hook parses」循环会自动覆盖新文件（它遍历 `$HERE/*` 跳过 `.md/.ps1/.json/.cmd`）——所以 `hooks/task-id` 会被自动检查语法，无需额外接入。
- 新增断言必须各有**一条只让它变红**的变异，沿用本仓库既有做法。

## Design Decisions and Alternatives

**选 `hooks/task-id` 可执行文件，而不是 source 一个 `.sh`。** 备选是给三个 hook 各自加一个 `HERE` 再 `. "$HERE/task-id.sh"`。否决理由：`hooks/` 里没有任何文件互相 source，全仓 grep 无匹配；引入第一个 source 关系会改变这一层的加载模型，且 `.sh` 后缀会触发 Claude Code Windows 的自动加 `bash` 行为（`hooks/README.md` 的「Why this shape」第一条）。可执行文件与 `json-field` 完全同构。

**选 `unpromote` 而不是放宽 `remove`。** 用户 2026-10-20 决定。`remove` 的拒绝理由（删条目会 orphan 任务目录）依然成立；把「删目录 + 复位条目」塞进同一个入口会让那个拒绝条件变成两个入口的布尔判断，而不只是一句话。

**校验覆盖全部读写入口，不只 `promote`。** 用户 2026-10-20 决定。只拦创建点的话，`state`/`archive` 仍能用 `../` 穿过 `TaskFlowDocs` 去操作仓库外的目录（实测 `task state ../evil in_progress` 已能走到审批检查）。三处各三行，成本低于漏一处。

## Open Questions

无。三项设计选择已由用户决定，已记入 PRD 的 Open Questions。
