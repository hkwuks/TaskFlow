# Plan — Isolate a task before its documents are written, and make the choice auditable
> Task version: v1
> Status: completed

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
- [x] 分支：`chore/e-task-isolation-and-capability-record`，基于 `main`（`985b269` 之后的 `origin/main`）。
- [x] 工作树：`.worktrees/e-task-isolation-and-capability-record`。本任务自身的隔离按本任务将写下的规则执行——先隔离，再写第一份文档。
- [x] 远程基线：`origin` 即 `hkwuks/TaskFlow`，目标 `main`；非 fork。
- [x] 本任务不新建治理文档；`SKILL.md`、`artifacts.md`、`CONTRIBUTING.md` 均已存在。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-17 23:09 +0800
- Approved version: v1
- Approved scope: PRD / Plan v1 —— 隔离提前到阶段 1（每任务一个 worktree）、`promote` 的隔离 gate、`intake` 的非阻断提示、能力留痕必填、`repository-check` 的错位报告。用户 2026-09-17 回复「批准」即批准本任务的 v1 方案。`Unaided — no capability applied to this phase; considered: <list>` 的措辞按 Open Questions 的候选定稿。

## Steps

### Step 1 — 把隔离提前到第一份任务文档之前

- Goal: 让「文档生在别人的分支上」这件事不再可能发生——隔离先于文档，而不是先于代码；并由 `promote` 的 gate 兜住，使「忘了先隔离」不能悄悄通过，同时让 `intake` 把「共享文件已写脏」当场说出来。
- Dependencies: 无。
- Files: `skills/taskflow/SKILL.md`、`CONTRIBUTING.md`、`README.md`、`README.zh-CN.md`、`.gitignore`、`hooks/task`（gate）、`hooks/smoke-test`（gate 断言）、`skills/taskflow/references/runtime.md`（`promote` 行）。
- Implementation checklist:
  - [x] `SKILL.md`：在 `### Todo → PRD → Spec → Plan` 段（阶段 1 之前）写明——在创建任何 `TaskFlowDocs/<slug>/` 文档或 `todo.md` 条目**之前**，任务已在自己的分支与工作树上；给出 `git worktree add .worktrees/<slug> -b <type>/<slug> <base>`，并说明主 checkout 从此停在 base 分支且保持干净。（`SKILL.md:110`）
  - [x] `SKILL.md:226`（阶段 5）：删掉「第一次建隔离」的语义，改为一句确认——隔离已在阶段 1 建立，此处只确认仍然成立。（现 `SKILL.md:235`）
  - [x] `CONTRIBUTING.md`「Working branches」：补 worktree 命令与理由（需要隔离的包括任务文档，不只是代码）；不把 worktree 写成「多任务时才需要」；注明 `promote` 在主工作树里会被拒。
  - [x] `README.md:91` / `README.zh-CN.md:58`：两句各自对齐到「每任务一个工作树」，保持中英行为一致（`CODE_STYLE.md:8`）。
  - [x] `.gitignore`：加 `.worktrees/`（受版本控制的那份；`.git/info/exclude` 已有同名的本地行，不动它）。验收看 `git check-ignore -v .worktrees/foo` 的来源前缀，**不看** `git status`——后者在本 clone 上已经因为 `info/exclude` 不报，断言它证明不了任何事。
  - [x] `hooks/task` 的 `promote` 加隔离 gate：先 `git -C "$root" rev-parse --show-toplevel`，失败（不是 Git 仓库）→ 放行；成功则算 `$(git -C "$root" rev-parse --git-dir)`，该目录下有 `commondir` 文件 → 放行；否则拒绝，`STATUS: blocked` + 退出 `3`。gate 必须在写任何文件**之前**。报错文案按 PRD 的 Resolved During Review：`<task-id>` 用参数真值、`<base>` 用当前分支真值，`<type>` 保持占位符并列出 `feature|fix|docs|chore`。判定收在 `worktree_kind()` 里（三态：`0` 任务工作树 / `1` 非仓库 / `2` 基础工作树）。
  - [x] `hooks/task` 的 `intake` 加同一判定的**非阻断提示**：非 linked worktree 且确在 Git 仓库里时，在 `intake OK: <id>` 之后追加一行说明 `todo.md` 现在是未提交改动、切分支前需先提交或 stash；退出码仍为 `0`，写入内容与去重逻辑不变。判定与 gate 共用一个 helper（R8），不复制粘贴两份条件。
  - [x] `hooks/smoke-test` 加断言：linked worktree 里 `promote` 放行；同一仓库主工作树里 `promote` 被拒（退出 `3`、未产生目录、`todo.md` 未变），且输出里 `<task-id>` 与 `<base>` 已替换为真值、`<type>` 仍在；非仓库目录放行；非 linked worktree 里 `intake` 成功（退出 `0`）且输出含提示行，linked worktree 与非 Git 目录里同一命令**不含**该行。逐条 mutation 验证。（新节 `== a task is isolated before its first document is written ==`，`smoke-test:557`）
  - [x] `runtime.md` 的 `promote` 行补一句前置条件与退出码；`intake` 行补一句提示行为。
- Acceptance: 见 PRD A1–A6、A11。
- Verification: `git worktree add` 的实际可运行性；`git check-ignore -v .worktrees/foo` 的来源前缀是 `.gitignore:` 而非 `.git/info/exclude:`（新 clone 成立用临时 `git clone` 复核——**不能**用 `core.excludesFile=/dev/null` 模拟，Git 始终读 `.git/info/exclude`）；gate 三态（linked worktree / 主工作树 / 非仓库）各跑一次；`intake` 三态各跑一次并核对提示行与退出码；`bash hooks/smoke-test`；`docker run … bash:3.2 bash -n hooks/task`；`git diff --check`。
- Rollback: 还原文本；删掉 gate、提示与其断言。gate 是 `promote` 分支开头的一个 `if`，提示是 `intake` 末尾的一个 `if`，删除即回到旧行为。
- Status: done

### Step 2 — 把能力选择从可选改为必填

- Goal: 让「能力选择跑没跑」在 Plan 上留下可审计的痕迹，而不是留空。
- Dependencies: 无（与 Step 1 无文件冲突，除 `SKILL.md` 的相邻段落需按顺序编辑）。
- Files: `skills/taskflow/references/artifacts.md`、`skills/taskflow/SKILL.md`、`hooks/task`（骨架文本）、`hooks/smoke-test`。
- Implementation checklist:
  - [x] `artifacts.md:80` 的 Plan 大纲：`## Skills / Tools Used (Optional)` → `## Skills / Tools Used`，并写明两种合法填法（实际调用清单 / `Unaided — …` 一行）。（`artifacts.md:80` 去 `(Optional)`，`:82` 补 `Unaided — …` 填法行，`:113` 补必填规则段）
  - [x] `hooks/task:399` 的 `promote` 骨架同步去掉 `(Optional)`；只改这一处文本，不动其它逻辑。（现 `hooks/task:453`）
  - [x] `SKILL.md:123` / `:137` 附近补一句落点：该节必填，未调用也要写一行；与既有「must be a choice, not an oversight」措辞一致。（`SKILL.md:146` 与 `:221`）
  - [x] `hooks/smoke-test` 增加断言：`artifacts.md` 与 `hooks/task` 里都不再出现 `Skills / Tools Used (Optional)`，且 `Unaided —` 的填法与说明已写入 `artifacts.md`。（新节 `== the capability record is required, not optional ==`）
  - [x] 新增断言逐条 mutation 验证（把模板改回 `(Optional)` → 断言变红）。（M7–M12）
- Acceptance: 见 PRD A7、A9、A10。
- Verification: `bash hooks/smoke-test`；`bash hooks/task promote` 到一个临时 root 检查生成骨架；`docker run --rm -v "$PWD":/w -w /w bash:3.2 bash -n hooks/task`；`quick_validate.py skills/taskflow`；`git diff --check`。
- Rollback: 还原四处文本改动。
- Status: done

### Step 3 — 让错位的任务产物在只读检查里可见

- Goal: gate 只挡 `promote` 这一个入口；这一步覆盖其余情形——产物已经写进去之后才切分支、手工复制进来的目录——让它们看得见。
- Dependencies: 无（`hooks/repository-check` 与 Step 1/2 无文件重叠；与 Step 1 同改 `hooks/smoke-test`，按顺序编辑）。
- Files: `hooks/repository-check`、`hooks/smoke-test`、`skills/taskflow/references/runtime.md`（若清单需要同步）。
- Implementation checklist:
  - [x] `repository-check` 在 `Working tree: has changes` 附近新增一段 `Task artifacts:`：列出本 checkout 里与当前分支不匹配的任务产物；未跟踪的任务目录只按「本 checkout 的未提交产物」列出，不断言归属。（`repository-check:63-88`；判定用 `git cat-file -e HEAD:<dir>`——已在当前分支历史里的不报，未提交的按 `git ls-files --error-unmatch` 分 `untracked` / `staged, not committed` 两种）
  - [x] 干净的单任务工作区不打印该段（或打印一行 `Task artifacts: none`），既有退出码语义不变——报告不设置 `needs`。（干净时打印 `Task artifacts: none uncommitted`；M15 钉住「不设 `needs`」）
  - [x] 在输出里写明判定边界（未跟踪目录无法归属到分支），避免误读。（固定三行尾注）
  - [x] `hooks/smoke-test` 扩展 `== repository-check … ==` 一节：错位 fixture 必须打印指认行；干净 fixture 不打印；逐条 mutation 验证（去掉报告 → 断言变红）。（新节 `== repository-check names uncommitted task artifacts without changing its verdict ==`）
  - [x] 若 `runtime.md` 的 hook 清单描述了 `repository-check` 的职责，同步一句。（`runtime.md` 无 `repository-check` 行——它的清单只收录自动 hook 与 `task`/`archive`/`version`/`reopen`；改在 `README.md` 与 `README.zh-CN.md` 的那段同步，中英行为对齐）
- Acceptance: 见 PRD A7、A8、A10。
- Verification: 在一个错位工作树上跑 `bash hooks/repository-check .` 看输出；在干净 fixture 上跑；`bash hooks/smoke-test`；`bash:3.2` 容器 `bash -n`。
- Rollback: 删掉报告段与新增断言，`repository-check` 回到只打印 `Working tree` 一行。
- Status: done

## Checkpoints

- Step 1 的 gate 是**唯一一处阻断行为**，且只作用于 `promote`；`intake` 只加一行提示、退出码仍为 `0`，写入内容不变；`state` / `progress` / `complete` 与 `repository-check`（Step 3 的报告不设 `needs`）的退出码语义不变。
- gate 与提示共用同一个判定 helper，判定用 `git rev-parse` 与 `commondir` 的存在性，不解析分支名、不猜 `<type>` 前缀；非 Git 目录两者都不适用，保证既有 smoke fixture 与无 Git 环境可用。
- `smoke-test` 的既有断言（`== task lifecycle dispatcher ==`、`== repository-check is read-only … ==`、`== TaskFlow packaged Skill contract ==`）必须保持通过。
- Step 1 是本任务自身的实践：本任务的目录在 `.worktrees/e-task-isolation-and-capability-record` 里写，主 checkout 保持干净——已做到（本任务的文档原先生在主 checkout，本轮已迁入该 worktree 并把主 checkout 还原到 `origin/main`）。

## Verification / Review

- 2026-09-18 Step 3: Step 3 验证记录见 plan.md；smoke ALL SMOKE PASSED；干净/未跟踪/staged/已提交四态 + 退出码不变；bash:3.2 OK

- 2026-09-17 Step 2: Step 2 验证记录见 plan.md；smoke ALL SMOKE PASSED（连跑 3 次）；quick_validate: Skill is valid!

- 2026-09-17 Step 1: Step 1 验证记录见 plan.md 的 Verification / Review；smoke ALL SMOKE PASSED；bash:3.2 语法通过

Step 1（2026-09-17，worktree `.worktrees/e-task-isolation-and-capability-record` / 分支 `chore/e-task-isolation-and-capability-record`，基点 `origin/main` @ `985b269`）：

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| ignore 来源 | `git check-ignore -v .worktrees/probe` | `.gitignore:7:.worktrees/` —— 来源是受版本控制的那份，不是 `info/exclude` |
| 新 clone 成立 | 临时 `git clone`（无 `info/exclude` 行）+ 拷入工作区的 `.gitignore` | `.gitignore:7:.worktrees/`；该 clone 的 `info/exclude` 只有注释 —— 结论可迁移 |
| 反例（不能用什么模拟新 clone） | `git -c core.excludesFile=/dev/null check-ignore -v` | 仍解析到 `.git/info/exclude:7` —— Git 始终读该文件，故该手法**不能**证明「新 clone 也成立」，本任务因此改用临时 clone |
| gate 三态 | `hooks/task promote` 分别指向 linked worktree / 主工作树 / 非 Git 目录 | `0` / `3`（`STATUS: blocked`）/ `0` |
| gate 无副作用 | 被拒后查目录、`todo.md` 摘要、`git status --porcelain` | 三者均未变 |
| gate 输出形态 | 主工作树里的被拒输出 | `git worktree add .worktrees/<task-id> -b <type>/<task-id> <base>` 中 `<task-id>`/`<base>` 为真值、`<type>` 仍为占位符，并列出 `feature \| fix \| docs \| chore`；输出 11 行全在 stdout、stderr 为 0 字节 |
| `intake` 三态 | 分别指向主工作树 / linked worktree / 非 Git 目录 | `0` + 提示行 / `0` 无提示 / `0` 无提示 |
| 回归 | `bash hooks/smoke-test` | `ALL SMOKE PASSED`（含新节） |
| 可移植性 | `docker run --rm -v "$PWD":/w -w /w bash:3.2 bash -n hooks/task`（及 `smoke-test`） | 均 `OK` |
| 空白 | `git diff --check` | clean |

Mutation 验证（`.mutate.sh`，一次一个变异并立即还原 + `diff` 确认；该脚本已删除）。存档的还原核对始终为 `SAME`：

| # | 变异 | 结果 |
| --- | --- | --- |
| M1 | gate 永不触发 | 红 —— `FAIL promote in the base working tree exit code` |
| M2 | gate 无条件拒绝 | 红 —— suite 在 `== task lifecycle dispatcher ==` 处退出 `3`（见下） |
| M3 | 去掉「非仓库 → 放行」那行 | 绿 —— **行为等价变异**，非断言缺口（见下） |
| M4 | `intake` 提示永不触发 | 红 —— `FAIL base-tree intake did not warn that Todo is now uncommitted` |
| M5 | `intake` 提示无条件触发 | 红 —— `FAIL task worktree intake warned about the base working tree` |
| M6 | gate 自己挑一个分支前缀 | 红 —— `FAIL base-tree promote did not print a runnable command with <task-id> and <base> filled in` |

- **M2 无 `FAIL` 行的原因已查明**：该变异让 gate 无条件拒绝，于是既有节 `== task lifecycle dispatcher ==` 里那句 `promote … --root "$lifecycle"` 被拒，`promote` 退出 `3`，`set -e` 让 suite 就地中止（日志 42 行，停在标题行，`ALL SMOKE PASSED` 未出现）。退出码非 `0` 是有效的红，只是形态是「中止」而非「断言失败」——两者都是失败，记录在此以免后来者误读成「没覆盖到」。该变异的语义被 M1 与新节的断言共同钉住（base 树必拒、worktree 必放行），所以不需要为它单独加断言。
- **M3 是行为等价变异**：被删的那行是 `git -C "$root" rev-parse --show-toplevel … || return 1`，而函数中紧随其后的 `git -C "$root" rev-parse --git-dir` 在同一个非仓库目录下同样退出 `128`（两者实测均 `128`），因此 `return 1` 仍会生效，外部行为不变。要区分二者需构造「`--show-toplevel` 失败但 `--git-dir` 成功」的目录，Git 里不存在这种状态，故**该行不可被测试区分**。保留它是为了显式表达意图（三态的出口都在一处、按序短路），不是断言缺口。

Step 2（2026-09-17，同一 worktree）：

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| 骨架 | `hooks/task promote … --root <非仓库临时目录>` 后读生成的 `plan.md` | `11:## Skills / Tools Used`，无 `(Optional)` |
| 回归 | `bash hooks/smoke-test` | `ALL SMOKE PASSED`（含新节；连跑 3 次均 `0`，末节恒为 `== todo-check reports an entry a merge dropped ==`） |
| 可移植性 | `docker run … bash:3.2 bash -n hooks/task`（及 `smoke-test`） | 均 `OK` |
| Skill 契约 | `quick_validate.py skills/taskflow` | `Skill is valid!` |
| 空白 | `git diff --check` | clean |
| 措辞落点 | `grep -rn 'Skills / Tools Used (Optional)'`（排除 `.git/`） | 命中的只剩 `histories`：`smoke-test` 的断言本身、`achieved/` 只读历史、本轮另外两个任务（`-duplicate-todo-id`、`-atomic-release-push`）的 Plan、以及本任务自己 PRD/Plan 里描述该问题的引用——均属 R11 声明不改的范围 |

Mutation 验证（同 Step 1 的手法：一次一个、立即还原、`cmp` 确认 `SAME`）：

| # | 变异 | 结果 |
| --- | --- | --- |
| M7 | `artifacts.md` 标题改回 `(Optional)` | 红 —— `FAIL artifacts.md Plan outline heading is not the required one` |
| M8 | `hooks/task` 骨架改回 `(Optional)` | 红 —— `FAIL promote scaffold heading is not the required one` |
| M9 | 删掉 `Unaided — …` 填法行 | 红 —— `FAIL the unaided fill pattern is not documented` |
| M10 | 删掉「required, not optional」句 | 红 —— `FAIL artifacts.md does not state the section is required` |
| M11 | `SKILL.md` 不再提 `Unaided — …` 形状 | 红 —— `FAIL SKILL.md does not name the unaided shape` |
| M12 | `SKILL.md` 复述完整填法（破坏「一处定义、别处指路」） | 红 —— `FAIL SKILL.md duplicates the fill pattern instead of pointing at artifacts.md` |

- **措辞只写一处**：完整填法 `Unaided — no capability applied to this phase; considered: <concept classes inspected>` 只定义在 `artifacts.md`（Plan 大纲的示例行 + `:113` 的规则段），`SKILL.md` 只写 `Unaided — …` 形状并指向该节。这与本仓库既有的 release 规则同一手法（`RELEASE.md` 是 plan，别处只指路不复述）。M12 就是钉住这一点的变异。
- **M11/M12 第一次跑超时（exit 124）**：不是断言问题——两次都是 `timeout` 先到，重跑时 M11 正常返回红（`3 分钟` 内），M12 用后台跑完也是红。原因是该 suite 每次约 10 秒，但并发多次调用同一 worktree 时会互相争抢（`session-record` 那节有 `sleep 1`），我一次串了太多轮。最终确认的三次连跑都是 `exit 0`。教训写在 Follow-ups。

Step 3（2026-09-18，同一 worktree）：

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| 干净 fixture | 完整仓库（有 remote/upstream、治理文档齐全）跑 `repository-check` | `Task artifacts: none uncommitted`，`STATUS: pass`，退出 `0` |
| 错位 fixture（未跟踪） | 同上仓库里放一个只有 `prd.md` 的任务目录 | 打印 `- TaskFlowDocs/2026-09-01-misplaced/ (untracked)` + 三行判定边界；**退出码仍为 `0` / `STATUS: pass`** |
| 错位 fixture（已 staged） | `git add` 该目录 | 改报 `(staged, not committed)`；退出码不变 |
| 已提交 | `git commit` 该目录 | 回到 `Task artifacts: none uncommitted`，且输出里不再出现该目录名 |
| 本 worktree 实况 | `repository-check .` | E 的目录已在本分支 HEAD 上，故报 `none uncommitted`；`Working tree: has changes` 仍如实反映未提交的源码改动 |
| 回归 | `bash hooks/smoke-test` | `ALL SMOKE PASSED`（含新节） |
| 可移植性 | `docker run … bash:3.2 bash -n hooks/repository-check`（及 `smoke-test`、`task`） | 均 `OK` |
| 空白 | `git diff --check` | clean |

Mutation 验证（同前：一次一个、立即还原、`cmp` 确认 `SAME`）：

| # | 变异 | 结果 |
| --- | --- | --- |
| M13 | 报告永不触发（`for` 里直接 `continue`） | 红 —— `FAIL misplaced task artifact not named` |
| M14 | 去掉 `git cat-file -e HEAD:<dir>` 的跳过 | 红 —— `FAIL committed task artifact still reported` |
| M15 | 报告段里加一句 `needs=1` | 红 —— `FAIL the task-artifact report changed the exit code: 2` |

- **判定边界（写进输出、也写在这里）**：一个**已提交**的目录属于哪个分支可以从历史推断，所以「已在本分支 HEAD 上」是确定的排除条件，用它跳过；一个**未提交**的目录在原理上无法归属到任何分支——所以报告不写「这个目录走错了分支」，只写「本 checkout 里有未提交的任务产物」。这也是为什么它不改退出码：它描述状态，不判定对错。
- **报告的第一版尾注写错了，本轮实测后订正**：原尾注说未提交的任务目录「是之后 `git checkout` 拒绝跨越的那种状态」。实测（`/tmp` 下五个最小仓库）**不成立**：
  - 未跟踪的任务目录单独存在时，`git checkout <另一分支>` **成功**（rc=0）——未跟踪文件不阻塞 checkout，除非**目标分支正好跟踪同一路径**（此时 rc=1，`untracked working tree files would be overwritten`）。
  - 真正会阻塞 checkout 的是**被修改的已跟踪文件**：`TaskFlowDocs/todo.md` 本地改脏且两分支该路径不同 → rc=1 `Your local changes … would be overwritten`。这正是 `intake` 的形态，所以 `SKILL.md:117` 与 `hooks/task` 里 `intake` 的注释**仍然成立**，不需要改。
  - 未提交任务目录的真实危害是另一条：它**跟着你跨分支走**（在本分支未提交，`checkout` 到别的分支后它仍在），于是被下一个任务接手——这才是本报告要指出的形态。
  - 尾注因此改为「跟着你进入下一个 checkout 的分支 / 或在目标分支跟踪同一路径时阻塞该 checkout」，`smoke-test` 的对应断言一并改为匹配新措辞，并重跑了移除报告的变异（M13b，仍为红）。
- **M15 第一次跑出的是退化的红**：我用 `printf … ; needs=1` 的形式注入，`printf` 与 `needs=1` 之间的换行被吃掉，变异体语法错误（退出 `126`），断言是「恰好变红」而非「因为设了 `needs` 才红」。改成在 `else` 分支里单独一行 `needs=1` 重跑，才得到真正的 `exit=2`。这类退化红不算验证通过，记在此处。

## Change Log

- 2026-09-17 —— Step 1 实施完成并验证（worktree `e-task-isolation-and-capability-record`）。8 个文件落地，`smoke-test` 新节 + 6 个变异验证；表见 Verification / Review。期间订正两处本任务自己的事实：`.gitignore` 的验收改为按 `git check-ignore -v` 判定来源（`info/exclude` 已含该行的前提下 `git status` 断言证明不了任何事），以及「用 `core.excludesFile=/dev/null` 模拟新 clone」这一手法被实测证伪、改用临时 clone。

- 2026-09-17 —— Step 2 实施完成并验证（同一 worktree）。4 个文件（`artifacts.md`、`SKILL.md`、`hooks/task`、`smoke-test`）落地，新节 `== the capability record is required, not optional ==` + 6 个变异验证；表见 Verification / Review。措辞只写一处：完整填法定义在 `artifacts.md`，`SKILL.md` 只指路，M12 钉住这一点。

- 2026-09-18 —— Step 3 实施完成并验证（同一 worktree）。`hooks/repository-check` 新增只读 `Task artifacts:` 段（历史排除 + 未提交两态），`hooks/smoke-test` 新节，`README.md` / `README.zh-CN.md` 的 `repository-check` 句子中英同步。3 个变异验证；表见 Verification / Review。三个 Step 全部 `done`。

- 2026-09-18 —— Step 3 复核期订正报告尾注与 PRD Background 的一处措辞（均不改范围）：报告原说未提交任务目录「是 `git checkout` 拒绝跨越的状态」，实测不成立（未跟踪目录不阻塞 checkout，除非目标分支跟踪同一路径；阻塞的是被改脏的已跟踪文件）。尾注改为「跟着你进入下一个 checkout 的分支 / 或在目标分支跟踪同一路径时阻塞」，`smoke-test` 对应断言改用新措辞并重跑 M13b（仍为红），PRD 的 Background 后果一/二与 R7 按实测分成两件事，Version History 记一条。`intake` 提示与 `SKILL.md` 那句话仍然成立，未动。

## Follow-ups

- **变异测试别把多轮串在一条命令里**：本轮两次撞上 2–5 分钟的调用超时（M11/M12），原因是一次串了多轮 `bash hooks/smoke-test` 且并发跑同一个 worktree。该 suite 单次约 10 秒，串三到四轮就会贴到超时线。后续每次只跑一个变异，或把整轮放进后台。
- **`TF-20260916-a357ee`（孤儿任务目录）只被部分覆盖，不能当作已了结**：Step 3 的报告只覆盖它的一半——**未提交**的任务目录被点名。它自己的 Todo Notes 把范围写得更广：「含已提交、已归档目录」的历史审计，即「目录在、没有任何 Todo 条目指向它」。已提交目录不在本报告范围内（它们可归属分支，且历史审计要读 `achieved/`，而那是只读历史）。所以 `a357ee` 仍需独立判断：它要的「目录 → Todo」反向引用检查与本任务的「产物是否未提交」不是同一个判定。本条不代改其 Todo 记录。
- **`repository-check` 的「Branch」行在 detached HEAD 下会空着**（既有行为，非本任务引入）。Step 3 的报告不读分支名，所以未受影响；若要修，是另一个任务的事。

## Version History

- v1 — planning. 三个 Step：隔离提前（用户 2026-09-16 决定「提前到阶段 1、每任务一个 worktree、`.worktrees/<slug>` + gitignore」）、能力留痕必填、`repository-check` 错位报告。
- v1（实施前订正）——Step 1 与 Verification 中关于 `.gitignore` 的验收改为按 `git check-ignore -v` 判定来源，不再断言 `git status`：本 clone 的 `.git/info/exclude` 已含 `.worktrees/`，那条断言今天就是绿的。理由与证据见 PRD 的 Version History。
- v1（2026-09-17 追加决定）——Step 1 扩为「隔离提前 + `promote` 隔离 gate」（用户选 b，理由见 PRD Background 的追加剧）：Files 补 `hooks/task` 与 `runtime.md`，Implementation 补 gate 的三态判定与 smoke 断言，Checkpoints 从「三个 Step 都不改逻辑」改为「gate 是唯一行为变更」。Step 3 的定位相应改为 gate 的补充（覆盖 gate 挡不住的其余情形）。
- v1（迁移记录）——本任务的 PRD/Plan 最初写在主 checkout（正是本任务要修的形态），2026-09-17 迁入 `.worktrees/e-task-isolation-and-capability-record`，主 checkout 还原到 `origin/main`。
- v1（2026-09-17 补 `intake` 提示）——Step 1 的 Implementation 补 `intake` 的非阻断提示与共用 helper，smoke 断言补 `intake` 三态，`runtime.md` 同步补 `intake` 行；Checkpoints 从「gate 是唯一行为变更」改为「gate 是唯一阻断行为，`intake` 只加提示、退出码不变」。理由（`intake` 才是把 `checkout` 挡住的写入方）见 PRD 的 Version History。
- v1（2026-09-17 定 gate 文案）——报错文案的 TODO 改为按 PRD 的 Resolved During Review 执行（脚本填 `<task-id>`/`<base>`，`<type>` 留占位符并列出四个合法前缀），smoke 断言补输出形态的核对。
