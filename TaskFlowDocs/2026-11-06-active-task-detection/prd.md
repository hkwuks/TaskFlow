# 修复活跃任务识别：按证据而非目录顺序
> Task version: v1
> Status: in_progress

## Goal

让 `hooks/task unaided` 与 `hooks/task external` 不再按目录字母序猜测「当前是哪个任务」，改为按证据解析：显式 `TASKFLOW_TASK_ID` → 调用者所在的任务目录 → 唯一的活跃任务；三者都得不出答案时拒绝并列出候选，而不是静默选一个。

## Background / Confirmed Facts

**缺陷（已读代码确认，修复前）**：`hooks/task` 的 `unaided`（原 1166–1174 行）与 `external`（原 1293–1301 行）各自复制了一段相同的循环：

```sh
active=""
for dir in "$root/TaskFlowDocs"/*/; do
  [ -d "$dir" ] || continue
  name="${dir%/}"; name="${name##*/}"
  case "$name" in achieved|repository-docs) continue ;; esac
  if [ -f "$dir/plan.md" ]; then active="$name"; break; fi
done
```

它取的是 glob 展开后**字母序第一个**含 `plan.md` 的目录，与调用者的 cwd、分支、意图都无关。

**危害**：`unaided` 把这个名字写进 `released` 行并决定 `dir` 路径。名字错了，就等于把甲任务的阶段证据记在乙任务名下，而 `approve` 正是拿 `released` 对账——它会让乙任务的审批凭一条本不属于它的记录通过。

**为什么长期不可见**：隔离规则要求一任务一 worktree，正常情况下每个树只有一个任务目录，缺陷与正确行为无法区分。它在两种情形下现形：父任务与子任务同处一棵树，或从别的分支取任务文档进来。

**顺带发现**：`external` 分支解析出 `$active` 后**从未使用**它——`external` 的存储只按 git dir 键，不需要任务名。所以那段循环在 `external` 处既是错的、又是多余的：它对一个自己不关心的问题做了猜测。

**既有约定**：`TASKFLOW_TASK_ID` 已是 `hooks/summarize-state` 与 `hooks/session-record` 的显式选择变量（`runtime.md:270,273`）。本修复沿用同名同义，不引入新变量。

**退出码约定**：`CODE_STYLE.md:16` —— `0` pass、`2` needs-user-input、`3` blocked。「无法判定是哪个任务」属于 needs-user-input，所以是 `2`；`fail()` 是 `1`，不能直接复用。

## Requirements

1. 抽出单一 resolver，消除两处重复。
2. 解析优先级：`TASKFLOW_TASK_ID` → cwd 所在任务目录（含其子目录）→ 唯一个活跃任务。
3. 多个活跃任务且前两者都不成立时，**拒绝**，退出码 `2`，列出全部候选，并给出两条可执行的补救命令。
4. `TASKFLOW_TASK_ID` 指向非活跃任务时，同样拒绝并列候选。
5. `external` 不再解析任务名——它只需要「存在活跃任务」，多个任务不得使其拒绝。
6. 拒绝时一个字节都不写。

## Acceptance Criteria

- 存在两个活跃任务、cwd 在仓库根时，`unaided` 退出 2、列出两个名字、不产生 `released` 文件。
- cwd 位于其中某个任务目录（或它的子目录）时，记录写到该任务，且该任务在字母序上**不是**第一个。
- `TASKFLOW_TASK_ID` 覆盖 cwd 推断。
- 只有一个活跃任务时，从仓库根直接可用，无需任何证据。
- `external` 在多任务树下正常工作。
- `bash hooks/smoke-test` 全绿；三个变异（退回目录序、拒绝码改 1、忽略 `TASKFLOW_TASK_ID`）各自触发不同的断言失败。
- `git diff --check` 通过。

## External Facts

- Depends on external facts: no
- Why not: 缺陷、约定与修复面都在本仓库内 —— `hooks/task`、`CODE_STYLE.md:16` 的退出码约定、`skills/taskflow/references/runtime.md:270,273` 的 `TASKFLOW_TASK_ID` 既有语义。

## In Scope

- `hooks/task`：新增 `active_task_names` 与 `resolve_active_task`，替换两处重复循环。
- `hooks/smoke-test`：新增一组断言覆盖三种解析来源与两种拒绝。
- `skills/taskflow/references/runtime.md`：说明解析顺序与 `TASKFLOW_TASK_ID` 在 `task` 命令上的含义。

## Out of Scope

- 不改 `hooks/summarize-state`、`hooks/session-record` 的选择逻辑：它们已正确（显式优先、多个则不写），且不写证据记录，误判不会污染账本。
- 不改 `hooks/archive`、`hooks/approve` 等按显式 task-id 参数工作的命令：它们从来不需要「猜」。
- 不引入 `--task` 命令行参数：`TASKFLOW_TASK_ID` 已有先例且不必改 `split_root` 的参数契约。若后续发现别扭，再加 `--task` 作为同义写法。

## Risks / Deferred Items

- 风险：cwd 推断依赖 `pwd -P`，若调用方通过软链接进入任务目录，解析后路径可能不匹配。缓解：取物理路径正是为了与 `--root` 的规范化方式一致（`split_root` 同样用 `cd … && pwd -P`）。
- 风险：`TASKFLOW_TASK_ID` 在宿主 hook 环境里可能被意外继承。缓解：它是显式的调用方输入，误设会立刻以「not an active task here」暴露，而不是静默生效。
- 遗留：`prompt-reminder` 等 hook 仍走自己的状态推导，不走本 resolver；它们的输出是提示而非证据，风险面不同。

## Open Questions

无。
