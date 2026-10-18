# Pair a release to the capability its phase reported, not to whatever record queue position handed it

> Task version: v1
> Status: completed

## Goal

`## Skills / Tools Used` 被文档定义为「a report of what happened」，而 approve 的校验使它必须写成**不是**实际发生的样子。本次把校验的判据从「名字等于本阶段那一条记录」改成「名字属于本版本记录过的调用」，让**如实写就过**；同时把账本「不按阶段归因」这件事写进文档，因为它是机制本身，不是缺陷。

用户价值：一次真实会话里，PRD 阶段调了两次能力、Plan 阶段调了一次，而 `plan.md` 是最后写的（常态），于是 `released` 里 PRD 那行记的是 Plan 阶段的能力。此时**如实填写的必需小节被 approve 拒绝，而把名字调成门要的顺序反而通过**——一个被文档要求「report of what happened」的必填节，只有写成与事实不符才能过。这不是理论：用户 2026-10-12 就是这样过的门，并在文件里写下了「记录按位点配对」这句本不该需要写的说明。

## Background / Confirmed Facts

### 配对的机制（读码所得，`hooks/capability-gate`）

- 门释放一个阶段时，先算 `next = max(released 第 3 字段) + 1`，再从 `evidence` 里取**第 next 行**：`awk -v n="$next" 'NR == n { print; exit }' "$evidence"`（`hooks/capability-gate:151`）。它不问这条记录属于哪个阶段。
- 写入的行是 `<version>|<stage>|<seq>|<kind>|<capability>`（`:155`），`seq` 全局单调。
- 因此**哪个阶段拿到哪条记录，取决于文档被写的先后**——即 `awk 'NR == n'` 配的是队列位点，不是阶段。
- `capability-evidence` 的注释自己承认了这一层解耦：「it does not know which phase is running, because the event does not say. The stage is attached later, when the gate releases a document and consumes a record.」**但没有任何一处文档或注释说明「stage 是按位点贴上去的」**，所以这是文档缺口叠着机制的表现面。

### 复现（本次实测，第一手，仓库 HEAD = `447eea4`）

同一 git 目录、同一版本号、同一组证据，**唯一变量是 `plan.md` 与 `prd.md` 谁先被写**。夹具里两次调用按发生顺序记入 `evidence`：`ctx_search`（PRD 阶段）、`ctx_execute`（Plan 阶段）。让 `plan.md` 先写（真实会话里的常态，因为 Plan 是正在推进的阶段）：

```
released（plan.md 先写）:
  v1|Plan|1|invoke|ctx_search      ← Plan 被记成 PRD 那次调用的能力
  v1|PRD |2|invoke|ctx_execute
```

同一份 `released`，两种写法交给 `hooks/task approve`：

| `## Skills / Tools Used` 写法 | 是否如实 | approve 结果 |
| --- | --- | --- |
| `[PRD] ctx_search` / `[Plan] ctx_execute` | 是（各阶段真用了什么） | `approve blocked: stage [PRD] does not name the recorded capability (ctx_execute)` |
| `[PRD] ctx_execute` / `[Plan] ctx_search` | 否（与事实相反） | `stages released by the gate: 2 invoked, 0 unaided` → `approve OK` |

**如实被拒、调序通过。** 复现在 `/tmp` 的副本里完成，未改动任何任务文档；`plan.md` 先行时门会先拒绝 `prd.md`，这不影响结论——`released` 的两行不受拦截影响。

### 溢出这一半（本次实测，另建探针）

一个阶段调多次时，多出的记录不会消失，而是**留在队列里给下一个阶段**。三个阶段各配一条记录的最省情况需要**三次**调用；若 PRD 阶段调了两次，第二次的那条会被 Plan 花掉。所以「一条证据只够一个阶段」是真的，但它绑的是**阶段数**，不是**阶段身份**。

### 全局单调队列不是本节要改的东西

`seq` 全局单调买的是「一条已花掉的记录不能被第二个文档再花一次」（`hooks/capability-gate:133-135` 的注释）。这一条与本次改动无关，保持不动。

### 被本次一并更正的记录

`TF-20261012-c66ad3` 的 goal 断言「once consumed reaches the line count no later version can be released without a fresh tool call in a host that has a gate」。**本次实测证伪了「版本提升是死路」这一半**：`hooks/task unaided` 在版本提升后**自己**往 `evidence` 追加一行并写 release 行（`hooks/task:1042-1043`），所以零工具调用也能释放任意多个阶段。干净探针（34 条证据全部消费，`evidence > consumed` 为假，即门自己已无法释放任何阶段）：

```
unaided OK: PRD in <task> -> requirements elicitation
unaided OK: Spec in <task> -> architecture and design
unaided OK: Plan in <task> -> work breakdown
stages released by the gate: 0 invoked, 3 unaided
approve OK: <task> (user, v13)
```

成立的那一半是：**每次版本提升都要重走 N 次能力声明或调用（N = 所需阶段数）**，这是重复劳动，不是死锁。该条的 goal 按此改写，Notes 记下站不住的那句；本条任务**不改它描述的机制**。

## Requirements

R1. **判据按版本，不按阶段位点。** `approve` 对 invoke 形状的 bullet，要求它**至少点名一个本任务版本内被记录为 `invoke` 的能力**；不再要求它等于该阶段自己那一条 release 行的能力名。如实填写（点的是本阶段真实用过的能力）因此能过。

R2. **不能张开成「随便写」**。以下仍须失败：(a) 点名的能力在本版本的 `released` 里**从不存在**；(b) 本版本该能力**只以 `unaided` 出现过**（即用 invoke 名义冒领一次声明）；(c) bullet 形状与本阶段记录的 `kind` 不符（invoke 行对着 `unaided` 记录，或反之——这一条原样保留）。

R3. **`Unaided` 一侧不动。** Unaided bullet 仍需带 `considered:`，且类名等于该阶段记录里的类名（`hooks/task:1104-1109` 原样）。这一侧的归因是真的——类名由 Agent 在 `unaided` 那一刻输入并被同一条命令写进记录——所以它保持逐字相等。

R4. **不改存储格式，不改消费规则。** `released` 仍是 `<version>|<stage>|<seq>|<kind>|<capability>`，仍每版本每阶段一行；`evidence` 仍是 `<kind>|<capability>`；门的 `next`/`seq` 算法与 `unaided` 的两个写入点一行不改。**溢出被接受**：一个阶段调多次时多出的记录归下一个阶段，账本不为此做补偿。

R5. **文档写明账本不按阶段归因。** 机制是「阶段数决定要几条记录，文档写作顺序决定哪条记到哪个阶段」，这一点必须**说出来**，而不是留给下一个读到驳回消息的人去反推。落点：`SKILL.md` 的 pre-write gate 段、`references/artifacts.md` 的 `## Skills / Tools Used` 与 approve 段、`hooks/README.md` 的 store 段、`hooks/capability-gate` 的队列消费注释、`hooks/task` 的 approve 注释。凡写了「name the capability that really was invoked」「one invocation is spent by one stage」的句子，改成版本域的说法。

R6. **新增断言钉住行为的两面**，且两个方向各能被咬住：一个**如实**填写的夹具必须**过**（这条在改前的实现上会红，即修复点），一个「点名本版本从未释放过的能力」的夹具必须**被拒**。R2(b) 的 `unaided` 冒领也须有断言。夹具必须把「池子只含已释放记录」这一条钉住（实测的 ①），否则该强度边界会随实现漂移而无声消失。

R7. **不改 base 检出行为、不新增依赖。** 只用既有的 POSIX 工具（`awk`/`sed`/`grep`/`tr`），不引入 bashism，不用 `awk -v` 传可能含反斜杠的值（沿用本文件既有做法：走 `ENVIRON`）。放宽后的读法必须对**尚未产生任何 release 记录**与**只有 `unaided` 记录**两种输入都安全退出（前者被更早的检查挡住，后者得空池而非报错）。

## Acceptance Criteria

A1. 同一份 `released`（Plan 先行导致错配）、同一组真实调用，**如实**填写 `[PRD] ctx_search` / `[Plan] ctx_execute` → `approve OK`。这是本任务的修复点，改前必红。

A2. 同一夹具，把 bullet 的能力名换成**本版本从未记录过**的名字 → `approve` 被拒，且消息点名该阶段。

A3. 同一夹具，把某阶段记录改为 `unaided`，而 bullet 仍以 invoke 形状写该阶段 → 被拒，消息仍是既有的 kind 不符文案。

A4. Unaided 一族的既有行为不变：缺 `considered:` 被拒；`considered:` 与记录类名不符被拒；三阶段 unaided 全通过并打印 `0 invoked, N unaided`。

A5. `bash hooks/smoke-test </dev/null` 全量通过；新增断言在**改前**的实现上必须失败（变异方向一），且把 R1 判据改回按阶段相等时也必须失败（变异方向二）。

A6. 文档如实陈述「账本按不止一个阶段数消费记录、记录不归因到阶段」，且 `smoke-test` 里凡是钉住旧措辞的断言同步更新。

A7. 无解释器不变量不破：`hooks run with no interpreter available` 一节仍通过；新代码只用 `awk`/`grep`/`tr`/`echo` 与 shell 内建。

## In Scope

- `hooks/task` — `approve` 的 `require_stage` 里 invoke 分支的判据（一处判据 + 注释）。
- `hooks/smoke-test` — 该节改写 1 条既有断言的期望文案，新增 3 条夹具：如实错配必须通过（修复点）、只在 `evidence` 里未释放的名字不得背书、本版本从未记录的名字仍须被拒。
- `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`hooks/README.md`、`hooks/capability-gate`、`hooks/task` — 陈述层（R5）。
- `TaskFlowDocs/todo.md` — `TF-20261012-c66ad3` 的 goal/Notes 更正；本条目状态推进。

## Out of Scope

- **改记账格式**（记录阶段窗口、一条 release 记多条能力、给 `released` 加字段）。用户 2026-10-12 决定取「不改存储格式」的那条路；改格式需要另定旧文件怎么办。
- **改消费规则**（一个阶段一次花完窗口内的记录、或把多出的记录标为已花）。溢出被接受。
- **`TF-20261012-c66ad3` 描述的机制**。本次只更正它的 goal 与 Notes，不动 `seq` 与版本提升的关系。
- **`TF-20261009-8abbd6` 的能力表示层**（让阶段选择不必是工具调用的产物）。相邻但不同面。
- 发版。改动落在 `hooks/task` 与三份文档上，用户可见面是 approve 的通过条件；是否需要一次发布以惠及已安装用户，留待完成时由用户裁定。

## Risks / Deferred Items

**先说两条实测出来的强度边界**（两者都由 Step 3 的对抗性检查指出、由本人在放宽后的副本上**独立复现**；探针在 `/tmp/tf-relax-probe`，未改动任务文档）：

- **① 池子只含「已被某次释放花掉」的记录，不含仍在队列里未释放的。** 放宽后 `[PRD]` 点名的名字必须在 `released` 里以 `invoke` 出现过。实测：`late-skill` 在 `prd.md` 释放之后才调用、仍留在队列里未被任何阶段释放时，`[PRD] late-skill` **仍被拒**；等 `spec.md` 把那条花掉之后，同一行**通过**。这是 `cap_released`（release 记录）与 `cap_pool` 同源带来的**意外收益**：声明侧的自放行会先写 `released` 再写 `evidence`，所以自报的名字必在池中；而真调用的名字在它的阶段释放前不在池中。副作用是同一条 bullet 的判定会随另一个阶段是否先被写入而变——不理想，但方向是**更严**，且 `Unaided` 一族的判定本来就是逐字相等，不受影响。
- **② 池子不判「调用发生在文档写入之前」，但受 ① 限制，可达性比读起来窄。** 「事后调用再回来补 PRD 的 bullet」这条路径本次**未能复现**：那样调用留下的记录仍在队列里未被释放，命中 ① 的拒绝。要让它真能通过，必须先有第二个阶段把那条记录花掉，于是该名字同时出现在那个阶段的记录里——这恰好就是本条缺陷本身（错配），不是新增口子。

**已知的、有意接受的弱化：**

- **判的是「本版本被调用过」，不是「在这个阶段被调用过」。** 一个把 A 阶段调用的名字写到 B 阶段的 bullet 仍然通过（如实的 `[PRD] prd-skill` 与错配的 `[PRD] plan-skill` 都能过）。这是**有意**的代价——「哪个阶段调了哪个能力」在账本层面**不可知**（`capability-evidence` 不知道阶段，门按队列位点贴阶段），强行逐字校验必然要求文档写成与事实不符的样子，那正是本条要消除的病。
- **散文提到也算命中**：判据是「bullet 里出现该名字」，所以 `- [PRD] I reused \`plan-skill\` from the Plan phase` 会通过。既有实现（`grep -qF`）已经是这个强度，本条不新增也不收紧。
- **`stages released by the gate: N invoked` 不再意味着 N 个不同能力**：同一条被花掉的记录可以给多个阶段的 bullet 当背书，计数行照旧打印。这行从未声称过「不同」，但放宽后更容易被误读，故写明。
- **溢出会持续存在**：单阶段多次调用时，多出的记录归下一个阶段。文档写明后，读者按「本版本被调用过」读它即可。
- **`v1` 不是任务身份**：store 只按 git 目录分，同工作树内两个任务目录会共用队列（本次同工作树内实测确认）。生产形态是「一任务一工作树」，且该守卫只在 `promote`（`hooks/task:719-739`），`approve` 侧没有任务↔记录的绑定。不作为本次范围。
- 若日后要让归因成为真的，只能让门或证据钩子知道阶段（例如按「自上次释放以来的记录」成组释放），那是另一条触发面，需另立条目。
