# Plan — Test 阶段的能力选择载体

> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers

- `hooks/task` 的 `unaided` 分支 —— 契约的权威实现；PRD/Spec/Plan 的路径必须逐字节不变，改坏了 18 处既有 `approve` 断言不会全部变红（它们只覆盖自己那条路径）。
- `hooks/capability-gate:136-160` —— 门消费 evidence 的那段，`Test` 的消费分支是它的镜像。两者对 I1（`released` 最大 seq == `evidence` 行数）的实现必须一致，否则所有阶段永久拒绝。
- `skills/taskflow/references/runtime.md:61-75` —— store 的写者数量、「每阶段一次调用或一次声明」的规则写在这里；加第三个写者必须同步改这段，而没有任何断言会因为它没改而变红。

## Related Tasks

- `TF-20261024-b48e56`（inbox）—— 「没有工具时回落到模型自身能力」的措辞。本任务是它的上游：先有 `[Test]` 行，那句话才有落点。
- `TF-20261012-c66ad3`（inbox）—— 每版本重复记账。加第四个阶段会让「每版本 N 次」变成 N+1；本任务不改该机制。
- `TaskFlowDocs/achieved/2026-10-17-stage-capability-pairing/` —— `approve` 的 invoke pool 为什么必须比阶段记录更宽；本任务复用该结论，不改它。
- `TaskFlowDocs/achieved/2026-09-27-capability-pre-write-gate/` —— 门的出处。

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — purpose: 把「测试阶段没有载体」从直觉变成可测的需求与边界；outcome: succeeded; incorporated: R1–R6 与 A1–A8 的可测措辞，以及「不新增门」这条边界及其理由。
- [Spec] `agent-skills:api-and-interface-design` — purpose: 定 `unaided Test` 的输出契约与 `[Test]` 行文法；outcome: succeeded; incorporated: 三条契约（命令输出后缀携带 kind 与能力名、行文法与既有三种同构、`released` 第五字段由队列决定）、不变式 I1–I3，以及「破坏性变更要写进 Changed 并在失败消息里给补救命令」。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 拆成可独立验证的 Step 并排出依赖；outcome: succeeded; incorporated: 四步拆分（消费分支 / approve 门槛 / 断言与夹具 / 文档）与三个检查点。

## Preconditions

- [x] 适用仓库文档已读：`TaskFlowDocs/repository-docs/index.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`、`skills/taskflow/SKILL.md`、`references/artifacts.md`、`references/runtime.md`、`hooks/README.md`。无冲突，无需新建仓库文档。
- [x] 远程/PR 前置：单 remote `origin` = `hkwuks/TaskFlow`，base `main@6e31060`，分支 `chore/test-phase-capability` 从它创建；PR 模板 `.github/pull_request_template.md` 已读。
- [x] 无 personal rule（`TaskFlowDocs/repository-docs/personal.md` 不存在）。
- [x] 实测确认四个前提：概念类 `testing strategy` 已在 `concept_class_re` 内（`hooks/task:614`）；`unaided` 的 stage `case` 是唯一挡住 Test 的地方（`hooks/task:1082`）；`released` 只有两个写者（`hooks/capability-gate:160`、`hooks/task:1136`）；85 个已归档任务里 77 个跑过测试而 0 个写过 `[Test]` 行。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-24 23:33 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — `task unaided` 接受 Test 并在声明时消费证据队列

- Goal: R1、R2、R3。`hooks/task` 的 `unaided` 分支加上 `Test`，并让它在队列有未消费行时记 `kind=invoke`（取该行能力名），否则记 `kind=unaided`；两条路径都打印自己记下的 kind 与名字。PRD/Spec/Plan 的代码路径原样保留。
- Dependencies: 无。
- Files: `hooks/task`.
- Implementation checklist:
  - [x] `unaided_usage` 与 stage `case` 扩为 `PRD|Spec|Plan|Test`；错误消息同步。
  - [x] `Test` 走独立分支：计算 `consumed`（`released` 最大 seq）与 `total`（`evidence` 行数，文件读，不用管道），`total > consumed` 时取第 `consumed+1` 行原样拆出 kind 与能力名。
  - [x] 记 invoke 时**不**追加 evidence 行（第 `consumed+1` 行本已存在），只写 `vN|Test|consumed+1|invoke|<cap>`。
  - [x] 记 unaided 时先追加 `unaided|<considered>` 到 evidence，再写 `vN|Test|consumed+1|unaided|<considered>`（与现有 PRD/Spec/Plan 分支同序，守 I1）。
  - [x] 幂等键 `(version, stage)` 与门一致：已释放则打印 `(already released)` 并 exit 0，不消费新行。
  - [x] 输出后缀：`(recorded as unaided)` / `(consumed an invocation record: <cap>)`，只出现在 `Test` 上。
  - [x] 注释写清为什么只有 Test 走消费分支（测试无唯一首次写入点，门永远不会为它消费），以及 I1 为什么两种分支都满足。
- Acceptance: A2、A3、A4、A5。
- Verification: 在临时仓库里手工跑四种情形（有/无未消费行 × 首次/重复），`cat` 两个 store 对照；`bash -n hooks/task`。
- Rollback: `git checkout -- hooks/task`.
- Status: done

### Step 2 — `task approve` 无条件要求 `[Test]` 行

- Goal: R4。`require_stage` 增加 `Test`，对账逻辑复用，不新增代码路径。
- Dependencies: Step 1（没有它就没法产生 Test 的 release 记录，A1 的补救命令也就走不通）。
- Files: `hooks/task`.
- Implementation checklist:
  - [x] `require_stage Test` 加在 `require_stage Plan` 之后、`Spec` 条件之前 —— 顺序决定报错时先撞到哪一个。
  - [x] 缺 `[Test]` 时的失败消息沿用现有形状，并指明补救命令 `bash hooks/task unaided Test --considered 'testing strategy'`。
  - [x] `stages released by the gate: N invoked, M unaided` 的计数自然包含 Test，不改格式。
- Acceptance: A1。
- Verification: 缺行 → 拒绝且消息点名 `[Test]`；补上后通过。
- Rollback: `git checkout -- hooks/task`.
- Status: done

### Step 3 — `hooks/smoke-test` 断言 A1–A6，并修既有夹具

- Goal: R6。新增一段断言覆盖两个消费分支、幂等、词汇表拒绝与 approve 的三条拒绝路径；同时把既有 18 处 `approve` 夹具补上 `[Test]` 行与对应 release 记录，否则它们会因为新门槛全部变红——这是 A6 的实际检验。
- Dependencies: Step 1、Step 2。
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] 既有 approve 夹具：`ap_store` 与 `ap_large_store` 各补 `ap_release … v1 Test …`；两处 `set_skills_body` 调用点补 `[Test]` 行。
  - [x] 新断言段：A2（无未消费行 → unaided，打印类名）、A3（有未消费行 → invoke，打印能力名；且 `[Test] Unaided …` 在此记录下被拒）、A4（词汇表外类 exit 2 且两 store 无新行）、A5（重复声明不新增 evidence 行）、A1（缺行拒绝）。
  - [x] A6：既有 `stages released by the gate` 断言在补行后仍成立，计数不变。
  - [x] 变异验证：逐条改坏 → 套件红 → `cp` 还原 → `diff -q` 确认。
- Acceptance: A1–A6。
- Verification: `bash hooks/smoke-test`；`bash -n hooks/smoke-test`。
- Rollback: `git checkout -- hooks/smoke-test`.
- Status: done

### Step 4 — 四份文档同步与 CHANGELOG

- Goal: R5。`SKILL.md`、`artifacts.md`、`runtime.md`、`hooks/README.md` 写明 Test 是必需的第四个阶段、两种行形状、kind 由队列决定、以及 store 从两个写者变成三个。
- Dependencies: Step 1–3 定下实现，文档描述的是它。
- Files: `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, `skills/taskflow/references/runtime.md`, `hooks/README.md`, `CHANGELOG.md`.
- Implementation checklist:
  - [x] `SKILL.md:173-179` 阶段表的 Phase 6 行与 `:179`、`:181` 两段能力文字。
  - [x] `artifacts.md:98-99`（行形状）与 `:130`、`:132`（approve 说明）。
  - [x] `runtime.md:61-63`（store 写者）、`:72`（每阶段一次调用或一次声明）、`:233`（命令表用法串）。
  - [x] `hooks/README.md` 的 `unaided` 条目。
  - [x] `CHANGELOG.md`：`Added` 记 `[Test]` 阶段与命令接受 Test；`Changed` 记 approve 现在无条件要求它（破坏性，附补救命令）。
- Acceptance: A7。
- Verification: `grep -n 'Test'` 五处命中且语义一致。
- Rollback: `git checkout --` 五份文件。
- Status: done

## Checkpoints

- Step 1 后：手工四情形在本机跑通，两个 store 同步（`released` 最大 seq == `evidence` 行数）。
- Step 2 后：缺 `[Test]` 拒绝、补上通过，且既有 approve 断言该红的红。
- Step 3 后：`bash hooks/smoke-test` 全绿；变异逐条验证过。
- Step 4 后：`bash hooks/release-check .` 与 `git diff --check` 干净。

## Verification / Review

本机于 2026-10-24/25 在 `.worktrees/test-phase-capability`（`chore/test-phase-capability`，基线 `main@6e31060`）上跑：

| 命令 | 结果 |
| --- | --- |
| `bash hooks/smoke-test < /dev/null` | `ALL SMOKE PASSED`，exit 0，34.1s（连跑两次一致） |
| `sleep 250 \| bash hooks/smoke-test`（open stdin，永不投递） | `ALL SMOKE PASSED`，exit 0 —— 修掉 stdin 阻塞后 |
| `bash hooks/release-check .` | `STATUS: pass` |
| `git diff --check` | 干净 |
| `bash -n hooks/task hooks/smoke-test` | 通过 |

### 手工四情形（Step 1 的验收依据）

在临时仓库里逐个跑，`cat` 两个 store 对照：

| 情形 | 输出 | released 落行 |
| --- | --- | --- |
| 队列空 | `(recorded as unaided)` | `v1\|Test\|1\|unaided\|testing strategy` |
| 重复声明 | `(already released)` | 两个 store 逐字节不变 |
| 队列有一行 invoke（换 v2） | `(consumed an invocation record: some:test-engineer)` | `v2\|Test\|2\|invoke\|some:test-engineer`，evidence 行数不变（2） |
| 词汇表外的类 | exit 2 + 词汇表 | 两个 store 无写入 |

### 两个 store 恒等式 I1 的边界探针

`spec.md` 声明的不变式是「`released` 的最大 seq == `evidence` 行数」，门靠 `evidence > consumed` 判定可消费性，一旦不同步则**此后所有阶段永久拒绝**。三个边界用手工构造的状态验过：

| 构造的状态 | 加 I1 入口检查之前 | 现在 |
| --- | --- | --- |
| `released` 有 3 条、`evidence` 文件不存在 | 补写 1 行 evidence，得到 max seq 4 / lines 1 —— **恒等被破坏**；HEAD 上未改动的 `task` 对 `Spec` 做同样构造得到逐字相同结果，所以是既有缺陷 | 四个阶段一律拒绝并给出两个数字与恢复方式（exit 1），拒绝后两个 store 逐字节不变 |
| `evidence` 存在但 0 行、`released` 不存在 | 走 unaided 分支，max seq 1 / lines 1，恒等 | 不变：`consumed=0 == total=0`，检查不介入 |
| `evidence` 不存在、`released` 也不存在 | 同上 | 同上 |

第一行的缺陷原本判定为「超出本任务范围、只记 Follow-up」，依据是「修复要动既有三个阶段共用的代码」。用户追问后重新判断：**共用的那一段恰好就是唯一该修的地方**——检查放在 `Test` 分支之外、四个阶段之前，改的是 `hooks/task` 里本来就唯一的那个写者，没有引入新的分布面，也没有改任何既有输出。所以改成修复，并把「改坏它套件会不会红」补成 M7。

### 变异验证

逐条改坏 `hooks/task`、跑套件、再 `cp` 还原并由 `diff -q` 确认逐字节相同：

| # | 故意改坏 | 结果 |
| --- | --- | --- |
| M1 | 删掉 `require_stage Test` | `FAIL pooled approve did not report the released stages` |
| M1b | 保留要求但删掉拒绝消息里的补救命令 | `FAIL a Plan without a Test line did not name the stage and its remedy` |
| M2 | Test 永不消费队列（`if false`） | `FAIL an unconsumed invocation was not spent by the declaration` |
| M3 | 消费时同时追加一行 evidence（破坏 I1） | `FAIL release and evidence stores are out of step (2 vs 3)` |
| M4 | `Test` 从 stage `case` 里删掉（退回 R1 前） | `FAIL unaided Test` |
| M5 | 幂等键只按 version（不带 stage） | `FAIL gate gave deny for … expected allow` |
| M5b | 只让 `Test` 失去幂等 | `FAIL re-declaring an already-released Test stage did not report it` |
| M6 | invoke pool 改从 `evidence` 读 | `FAIL capability-mismatch message` |
| M7 | 删掉 I1 的入口检查（`consumed > total` 那道） | `FAIL Test was declared against a store already out of step` |

M5 咬住的是门那份断言而不是 Test 那份 —— 说明全仓库范围的幂等键改写会被既有断言先抓到，而 Test 单独的幂等需要 M5b 才能咬住。两条都留在表里，因为它们证明的是两件事。

M7 的断言要求拒绝消息点名两个数字，所以「拒绝但不说清」也会红；构造的是 `released` 到 seq 2、无 `evidence` 的 store，并且用 `Test` 与 `Spec` 两个阶段各跑一次 —— 两个阶段都不在 `released` 里，幂等分支答不上来，检查才真正被执行到。

### 一次断言缺陷，已修

新断言段最初在失败分支里**再跑一次被断言的命令**（`printf '%s\n' "$(tp_unaided …)"`）。这在幂等性被改坏时特别有害：第二次调用已经是 `(already released)`，于是失败信息报告的是第二次的输出，把读者引向「幂等没坏」的错误结论。M2 第一次跑就是这样：真正的失败是「没有消费队列」，打印出来的却是 `(already released)`。已改为每个断言只跑一次并捕获到 `tp_res`，失败时打印捕获的那一次。

### 一个真实的环境缺陷，已修（原判断是错的）

先前这一节写的是「套件需要 `< /dev/null`，停住时 `hooks/reopen` 在等输入」。**那个归因是错的**，本次重新定位后改掉：`session-start` 按契约从 stdin 读事件 JSON（`event_json="$(cat)"`），而套件里有两处把它当作「没有事件」来调用 —— `session-start emits a platform JSON shape` 那段与直跑 `run-hook.cmd` 那段 —— 都不喂事件，于是它继承了套件自己的 stdin。谁把套件跑起来，它就在等谁的输入。

复现与证据：

- 把套件的 stdin 接到一个永不投递的 fifo，套件停在 `== session-start emits a platform JSON shape ==` 之后不动（`timeout 12` 到点被杀）。
- 同一时刻 `ps -ef --forest` 显示阻塞进程链是 `smoke-test → smoke-test → session-start → cat`，不是 `reopen`。

修法是两处调用各加 `< /dev/null`（它们表达的是「没有事件」，不是「读调用者的终端」），并在调用点写明理由。验证：用同一条「永不投递的 open stdin」（`sleep 250 | bash hooks/smoke-test`）重跑，套件跑完并打印 `ALL SMOKE PASSED`。这是本任务顺手修掉的既有缺陷，记在 CHANGELOG 的 `Fixed`。

### bash 3.2 容器

`docker run --rm bash:3.2` 里把 Step 1 的四种情形重跑一遍：输出与 bash 5 逐字相同，含 I1 恒等（max=2 / lines=2）、词汇表拒绝（exit 2）与新增的 I1 入口检查（exit 1，且拒绝后两个 store 逐字节不变）。

镜像里没有 `git`（`apt-get install git` 也拉不到），所以用了一个 `/tmp/gitstub.sh` 顶上 `git -C <root> rev-parse --absolute-git-dir` —— 本项要验的是 shell 与 awk 的可移植性，不是 git 的行为。这一点要在读结论时记住：容器结果证明的是 `hooks/task` 的引用与算术在 bash 3.2.57 + busybox 下成立，不证明 git 版本差异。

## Change Log

- 2026-10-24 v1 — 建 PRD / Spec / Plan。用户四轮问答定下范围（只做测试阶段）、载体（`[Test]` 行 + approve 对账，不新增门）、必需性（总是必需）、消费范围（只对 Test 消费证据队列）。
- 2026-10-24 本次 `promote` 先按 small 建过、随即 `unpromote` 重建为 large：本任务要写 `spec.md` 并改 `approve` 对阶段的要求，改的是阶段契约本身，不是小任务。影响 `TaskFlowDocs/todo.md`。

- 2026-10-25 Step 1–4 完成。实现上唯一的新语义是 `unaided Test` 的队列消费；其余是加一个 stage 名与一条 `require_stage`。影响 `hooks/task`、`hooks/smoke-test`、四份文档、`CHANGELOG.md`。
- 2026-10-25 断言缺陷自查并修复：新段最初在失败分支里重跑被断言的命令，导致失败信息报告第二次运行的结果（M2 暴露）。改为只跑一次并捕获。影响 `hooks/smoke-test`。
- 2026-10-25 用户指出上一轮写的三件事里「2. 修复」「3. 是否需要修复」，据此把两件原本只记进 Follow-ups 的都做了：(a) I1 入口检查 —— 原先判定「修它超出范围」，用户要求修，于是加到 `unaided` 的 stage 分支之上，对四个阶段统一生效，并补 M7 变异与断言；(b) 套件 stdin 阻塞 —— 原先误判为 `reopen`，重新定位为 `session-start` 按契约读 stdin 而两处调用不喂事件，加 `< /dev/null` 并用 open stdin 重跑验证。影响 `hooks/task`、`hooks/smoke-test`、`runtime.md`、`CHANGELOG.md`。

## Follow-ups

- **`unaided` 这个命令名在 `Test` 上不再贴切** —— 它可能记下一次真实的调用。改名（如 `task declare`）是全仓库动作，单独立项。
- **阶段表里另外三个无载体阶段**（Research / Build / Complete）不在本任务范围，各自缺的东西不同。
- **每版本重复记账**（`TF-20261012-c66ad3`）在加第四个阶段后代价上升，本任务不改。
- 若将来定义出「什么是测试文件」的仓库约定，可以再考虑有没有可能给 Test 一道真门。
- **`capability-gate` 没有同样的入口检查** —— 门在 I1 已破时仍会按 `total > consumed` 判定，因而只是继续拒绝（不写、不扩大差距），行为上是安全的；但它不会指出原因。把同一条诊断放进门的拒绝消息，属于门那边的改动，单独立项。
- **store 的恢复只有「删掉重来」** —— `evidence` 丢行后无法重建，`released` 里那条记录对应的一次调用也就没有证据可查。若将来需要可修复的 store（例如在 `released` 里冗余存 `kind` 与能力名之外的行号映射），那是 store 格式的变更。

## Version History

- v1 — planning.
