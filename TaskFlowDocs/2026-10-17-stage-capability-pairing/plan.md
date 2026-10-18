# Plan — Pair a release to the capability its phase reported, not to whatever record queue position handed it

> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md` — 本次唯一行为改动的契约（approve 对账的判据域）、I1–I8 不变量、D1–D4 决定与替代方案。

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — 适用的仓库文档与阶段。
- `CONTRIBUTING.md:18` / `:20-32` — 「Never implement in the base working tree」与分支前缀。
- `CODE_STYLE.md` — shell 退出码约定（`0` 通过 / `2` 需用户输入 / `3` 工作流阻塞）与 POSIX 下限。
- `.github/pull_request_template.md` — phase `pr` 的适用文档；Step 3 逐字段映射。
- `hooks/capability-gate:126-157` — 释放的选择算法（`consumed`、`next`、`awk 'NR == n'`）与两条注释；本次只改注释，不改行为。
- `hooks/capability-evidence:13-17` — 「does not know which phase is running」这一自述；本条缺陷的上游。
- `skills/taskflow/references/artifacts.md:127-129` — `## Skills / Tools Used` 被定为「a report of what happened」以及 approve 的现有对账描述。
- `TaskFlowDocs/achieved/2026-09-27-capability-pre-write-gate/` — 门的原始 PRD（R3「谓词是工具类别不是产品清单」、R11「记录的家从 plan.md 移到证据存储」）；本条是它的一个记账层缺口，不是它的要求被推翻。

## Related Tasks

- Parent: None.
- Children: None.
- Depends on: None.
- Blocks: None.
- Related:
  - `TF-20261012-c66ad3`（inbox）— 同一记账层的另一个面。本次**更正它的 goal 与 Notes**（证伪「版本提升是死路」），但**不改它描述的机制**。
  - `TF-20261009-8abbd6`（inbox）— 能力表示层（让阶段选择不必是工具调用的产物）。相邻但不同的面。
  - `2026-10-11-gate-host-coverage`（done）— `unaided` 自写 release 行的来源；本次不改该路径。
  - `2026-09-27-capability-pre-write-gate`（done）— 门的来源文档。

## Skills / Tools Used

- [PRD] Unaided — no capability applied to this phase; considered: requirements elicitation, divergent exploration
- [Spec] `mcp__exa__web_search_exa` — purpose: 查供给链溯源体系（in-toto link / SLSA provenance）如何把产物绑定到授权它的证据，以判断「按队列位点配对」是不是已知的反模式；outcome: 拿到三处一手规范（in-toto link 的 `name` 是步骤标识、`materials`/`products` 用**名字**做键；SLSA v0.1 的 `recipe.definedInMaterial` 用**索引**指材料，规范自己留了 TODO「What if there is more than one material?」）；incorporated: 只用于确认「按位点配对会丢失归因，且这不是本仓库的发明」，不作为本次修法的依据——用户已裁定修判据域而不是改存储格式（Spec D1）。
- [Plan] `general-purpose` — purpose: 对一个已定的修法做对抗性检查（枚举放宽后可能被冒领的路径、定位会被打破的既有断言、给出可用的变异编辑、定位待改行号）；outcome: 回报了 9 条可能的冒领路径与两处待改行号；其中**两条经我独立复现后成立并折入本 Plan**——(a) 既有断言 `smoke-test:1187` 的文案必须同步（不改编译即全量红，已实测）；(b) 池取自 `released` 而非 `evidence`，因此**未被任何阶段释放的名字不在池中**（反直觉的收紧，已实测并记为 I9）；另**否掉了它的一处措辞**：「事后调用可回头背书更早的阶段」在本实现下**不成立**（那样调用留下的记录仍在队列里未释放），故未采信；incorporated: 见 PRD Risks ①②、Spec I9/I10、本 Plan Step 1/2 的清单。
  - [Plan] Step 3 的对抗性检查由 `general-purpose` 那次调用完成；它**没有**产出独立结论以外的东西，也不构成本阶段的第二次调用——本阶段只调了它一次。

三阶段都不是空话：`unaided` 由 `hooks/task unaided` 落成记录，另两次调用的记录也真实产生于本工作树。本课的 `released` 三行与上面对应关系一致（`v1|PRD|1|unaided|…` / `v1|Spec|2|invoke|mcp__exa__web_search_exa` / `v1|Plan|3|invoke|general-purpose`）。

## Preconditions

- [x] 适用的仓库文档与个人规则已检查、优先级/冲突已记录。`repository-docs/index.md` 路由 `CONTRIBUTING.md`（design,code,commit,pr,release）、`CODE_STYLE.md`（code,review）、`RELEASE.md`（release）、`.github/pull_request_template.md`（pr）。无仓库文档规范 approve 的判据，无冲突。本 clone 无个人规则（`personal.md` 不存在）。
- [x] 远程/fork/PR 工作：`origin` = `hkwuks/TaskFlow`，base = `main`，本分支 `fix/stage-capability-pairing` 从 `447eea4` 起（`origin/main` = `447eea4`）。Step 3 在任何推送前复核。
- [x] PR 模板：`.github/pull_request_template.md` 为 phase `pr` 的适用文档；Step 3 逐字段映射并记录模板路径与验证。
- [x] 缺失治理草案与显式批准：不适用——本任务不创建任何缺失的治理文档。
- [x] 核心文档单一写者：Primary Agent（Claude）。分支 `fix/stage-capability-pairing`，worktree `.worktrees/2026-10-17-stage-capability-pairing`。
- [x] 既有用户裁定已记录：D1（放宽判据域，不改存储格式）、D2（接受溢出，文档写明不归因）、以及任务范围含 `c66ad3` 的更正——均为用户 2026-10-12 / 2026-10-17 裁定，见 Spec 的 Design Decisions 与 `## Open Questions`。
- [x] 隔离先于第一份文档：worktree 与分支在任何 `TaskFlowDocs/2026-10-17-stage-capability-pairing/` 文件之前创建；`promote` 在该工作树内运行。
- [x] 缺陷已在本仓库第一手复现（非仅读码）：同一 `released` 下，如实写法被拒、调序写法通过。见 PRD「复现」。
- [x] **本任务自己的账本恰好没有踩中这个缺陷，原因值得记下**：本工作树的 `released` 是 `v1|PRD|1|unaided|requirements elicitation`、`v1|Spec|2|invoke|mcp__exa__web_search_exa`、`v1|Plan|3|invoke|general-purpose`。三行的归因**都是真的**，因为 `unaided PRD` 是在写任何文档正文之前先执行的，队列顺序于是与阶段顺序一致。缺陷只在「先写 `plan.md`／一个阶段调多次」时显形——本条正是靠这一点说明它不是理论问题：同一份 `## Skills / Tools Used`（据实书写）会在另一个写作顺序下被判为错。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-18 00:23 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 把 invoke 一行的判据域从「本阶段那条记录」放宽到「本版本记录过的调用」

- Goal: `approve` 对 invoke 形状的 stage 行，要求其点名**本版本 `released` 中任一 `kind == invoke` 行的能力**；该阶段自己的记录仍必须存在（I1），`kind` 相符仍必须成立（I2），Unaided 一侧一字不改（I3）。
- Dependencies: None.
- Files: `hooks/task`。
- Implementation checklist:
  - [x] R1：新增一次 `awk` 求值得到**池**——`awk -F'|' -v v="$approved_version" '$1 == v && $4 == "invoke" { print $5 }' "$cap_released"`。值与既有做法一致，走位置参数给 `awk -v` 只传版本号（版本号形如 `v[0-9]+`，无反斜杠风险）；能力名不经 `awk -v`（I7）。
  - [x] R1：判据改为对池逐行匹配，**用 `while IFS= read -r` + 单引号 heredoc**，不得用 `<<<`、`$'…'`、`<(…)`（Code and Test Constraints 明列）。`case "$line" in *"$c"*)` 而非 `grep -qF`：空池下 `case` 不匹配任何行、不需要 `|| true` 兜 `set -e`。
  - [x] R1：`require_stage` 的 `local` 行（`hooks/task:1117`）补上 `cap_pool`、`cap_hit`、`c` 三个局部名。
  - [x] R1/I10：池为空（文件不存在、或只有 `unaided` 行）时 `cap_hit` 保持 0 → 拒；该赋值放在已有 `[ -f "$cap_released" ]` 之外但 `awk` 只读已由 I1 保证存在的路径——实测：本版本只有 `unaided` 行时 `awk` 正常输出空、`while` 体一次不执行、`cap_hit` 为 0、`fail` 分支命中；文件不存在的情形由 I1 的检查先拦下，`awk` 不会读到不存在的文件。
  - [x] R2(a)：本版本一条 invoke 行都没有、或 bullet 与池中所有名字都不匹配 → 仍 `fail`，消息点名阶段与「本版本被调用过」这一要求。
  - [x] R2(b)：本版本该能力只以 `unaided` 出现时池中不含它；`kind` 判据保持在放宽之前（`[ "$kind" = "invoke" ]` 一行不动）。
  - [x] R3：Unaided 分支（`hooks/task:1134-1142`，含 `considered:` 与类名逐字相等）**一字未改**，逐字节核对（`git diff` 该分支零行）。
  - [x] R4：`hooks/capability-gate` 与 `hooks/task` 的 `unaided` 分支均不改行为；本 Step 未动 `hooks/capability-gate`。
  - [x] R5：段首注释（`hooks/task` approve 处）写明「账本按不止一个阶段数消费记录，记录的阶段归属取决于文档写作顺序，所以对账的判据域是版本而不是阶段」。连同「两侧有意不同强度」「池取自 `released` 而非 `evidence`」一并写明。
  - [x] R7：只用 `awk`/`grep`/`printf`；无 `declare -A`、`mapfile`、GNU-only `sed -i`、`grep -P`、进程替换。
- Acceptance: PRD A1、A2、A3。
- Verification: 已跑。`bash -n hooks/task` 通过；`docker run --rm -v "$PWD":/w -w /w bash:3.2 bash -n hooks/task` 通过；完整套件 `ALL SMOKE PASSED`。见 `## Verification / Review`。
- Rollback: revert 本 Step 的 commit。
- Status: done

### Step 2 — 断言钉住两面，并改写被取代的那一条

- Goal: 让 R1 与 R2 由检查而不是靠人记着；把因判据域改变而失效的既有断言按新语义改写，并在节注释里写明这是有意的行为变更。
- Dependencies: Step 1.
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] R6：新增夹具——同一版本两条 invoke 记录（PRD 记 `some:requirements-skill`，Plan 记 `other:breakdown-tool`），bullet 按**该版本实际释放后的归属**书写，其中 `[PRD]` 点名的是 Plan 释放掉的名字 → 必须 `approve OK`。**这条在改前的实现上必红**，即变异方向一。落点：`hooks/smoke-test:1201-1218`（`ap_release v1 Spec 3 invoke later:plan-skill` + `[PRD] later:plan-skill`）。取 `Spec` 而非 `Plan` 作池里那条：本夹具里 `Plan` 自己的记录是 `unaided`，把池记录挂到 `Plan` 会让 `Plan` 的 `kind` 判据先红（已实测），而 `Spec` 在本夹具里不是必需阶段（无 `spec.md`），因此它能在池里而不与任何阶段自己的记录冲突。
  - [x] R6：新增夹具——bullet 点名池里没有的能力 → 必须被拒，且消息含阶段名与 `(some:requirements-skill)`（即该阶段记录里那个名字）。落点：`:1230-1237`（`never:invoked`）。
  - [x] R6/I9：新增夹具——**只在 `evidence` 里、尚未被任何阶段释放**的名字不能背书 bullet（池取自 `released` 而非 `evidence`）。落点：`:1222-1228`（`printf 'invoke|queued:never-released\n' >> evidence` 后仍被拒）。这条钉住实测 ① 的强度边界，防止实现日后漂移成读 `evidence`。
  - [x] R2(b)：新增断言——把 Plan 的记录改为 `unaided`，bullet 仍以 invoke 形状写它 → 拒，消息仍是既有 kind 不符文案。落点：`:1191-1198`（既有 `kind-mismatch` 断言，保留未改）。
  - [x] **改写既有断言（`smoke-test:1187`）：消息文案由 `does not name the recorded capability (…)` 变为 `does not name a capability invoked in this Task version (…)`。** 已实测：不改这一条，全量套件在该节 `FAIL capability-mismatch message` 退出 1（该夹具本身仍**应当**被拒——它是「点名池里没有的名字」这一面，语义没变，变的只是文案）。节注释同步写明这是有意的行为变更。**这条是本 Step 唯一必须改的既有期望。**
  - [x] A4：Unaided 一族的既有断言（缺 `considered:`、类名不符、三阶段全通过计数行 `0 invoked, 3 unaided`）全部保留、不改期望，全量套件中全绿。
  - [x] 变异方向一/二（本合同一件事）：把判据改回「等于本阶段那条记录的名字」（heredoc 里 `$cap_pool` → `$capability`）→ 新夹具在 `FAIL approve refused a stage naming a capability this version released` 处红，退出 1。**已跑。**
  - [x] 变异方向三（对抗性检查给的「静默失效」编辑）：把池匹配的 pattern 置空（`case "$line" in *""*）`，空 pattern 匹配任意行）→ 既有 `smoke-test:1187` 在 `FAIL capability-mismatch message` 处红（实际落在 `:1188` 的 `grep -q '…(some:requirements-skill)'`，被静默放行），退出 1。这条证明本体断言仍咬得住放宽后的代码。**已跑。**
  - [x] 附加的第三条变异（不在原清单，本次补上）：把池判据也贴到 Unaided 分支（两侧「统一」）→ 在 `FAIL approve refused a stage naming a capability this version released` 处红，被拒理由是 `stage [Plan] reports a different considered class than the recorded one (work breakdown)`，退出 1。这一条实测证明了 I3 确实是可被咬住的约束，而不只是注释里的说法。
  - [x] 新断言只用既有 POSIX 工具；无撇号嵌在 `$( )` 的 heredoc 中；bash 3.2 解析通过。
- Acceptance: PRD A2、A3、A4、A5。
- Verification: `bash hooks/smoke-test </dev/null` → `ALL SMOKE PASSED`，退出 0，73 节 `ok`。**实测口径**：`git checkout 447eea4 -- hooks/task hooks/smoke-test`（本任务之前的实现）在同一棵树上也是 73 节 `ok`、`ALL SMOKE PASSED` —— 新断言写在既有节内、不新增节，所以节数不变是对的；改动前的草稿里写的「72 节」是预演副本上的旧计数，已按实测更正。反向对照：只回退 `hooks/smoke-test` 而保留新 `hooks/task` → `ok=28` 后在该节红，证明新夹具确实咬在新实现上。三个变异方向各红一次（详见上），恢复后全绿。逐条记录见 `## Verification / Review`。
- Rollback: revert 本 Step 的 commit。
- Status: done

### Step 3 — 文档写明账本不按阶段归因，更正 c66ad3，全量验证与收尾

- Goal: 让 R5 落到读者会去的地方；把 `c66ad3` 那条站不住的判断改正；确认没有打破既有断言与无解释器不变量。
- Dependencies: Step 1, Step 2.
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`hooks/README.md`、`README.md`、`hooks/capability-gate`（注释）、`TaskFlowDocs/todo.md`、本任务 `plan.md`。
- Implementation checklist:
  - [ ] R5：`SKILL.md:177` 的「an invoke line must name the capability that really was invoked」「one invocation is spent by one stage」改为版本域说法，并点明「记录的阶段归属取决于文档写作顺序」。
  - [ ] R5：`references/artifacts.md:127` 的「one invocation is spent by one stage」与 `:129` 的对账描述同步；保留「report of what happened」这一定性（放宽**是**为了让它成真）。
  - [ ] R5：`hooks/README.md:197-201` 的 store 段补上「哪个阶段拿到哪条记录由写作顺序决定」。
  - [ ] R5：`README.md:124` 的「refused until a capability really was invoked for that stage」同样按版本域改写（门的判据从来不是「该阶段调用过」，写清了才不会让读者据此推断归因）。
  - [ ] R5：`hooks/capability-gate` 队列消费处与 `hooks/task` 的 approve 注释各补一句（只改注释，行为不动）。
  - [ ] 更正 `TF-20261012-c66ad3`：goal 改为「版本提升需重走 N 次能力声明或调用（N = 所需阶段数）；按门的已扣减计数算，仅无门宿主需要真调用」；Notes 记下本次实测（34/34 耗尽、零工具调用、`unaided` 三阶段、`approve OK`）与哪一句站不住；状态留 `inbox`、优先级 `normal`。
  - [ ] R6：`smoke-test` 里钉住旧措辞的断言（`is a report of what happened` 等）核对是否需要同步；若改写措辞则一并更新。
  - [ ] `bash hooks/smoke-test </dev/null` 全量；`git diff --check`；`bash hooks/release-check .`；`quick_validate.py skills/taskflow`；`bash -n`；`docker run bash:3.2` 解析。
  - [ ] 读 `.github/pull_request_template.md`，逐字段映射并记录模板路径与验证结果。
  - [ ] 在 `## Verification / Review` 记录每条命令与结果，含两个方向的变异验证。
  - [ ] 推送后按 `CONTRIBUTING.md:43` 把 landing claim 写进 PR 正文（不写回本文件）。
- Acceptance: PRD A5、A6、A7。
- Verification: 上述命令输出逐条记录在 `## Verification / Review`。
- Rollback: revert 承载本 Step 的 commit。
- Status: pending

## Checkpoints

- CP1（Step 1 后）：如实错配的夹具从「被拒」变为「通过」；本版本未记录的能力名仍被拒；Unaided 一侧逐字节未变。
- CP2（Step 2 后）：两个变异方向各红一次；Unaided 一族的既有断言全绿；`no interpreter` 一节未被新代码破坏。
- CP3（Step 3 收尾）：文档如实陈述账本不归因；`c66ad3` 的 goal 与实测一致；全套命令通过、验证记录与 PR 模板映射写入本文件、CI 绿。

## Verification / Review

记录格式：逐条命令与结果。区分 **既有失败** / **新引入失败** / **环境失败**。待实现后填写。

## Change Log

- 2026-10-17 work revision — 任务由 `TF-20261012-c79e31` promote 创建；用户裁定 D1（放宽判据域）、D2（接受溢出并写入文档）与范围含 `c66ad3` 更正；affects `prd.md`, `spec.md`, `plan.md`, `TaskFlowDocs/todo.md`。

## Follow-ups

- 若日后要让「哪个阶段用了哪个能力」成为真的，只能让门或证据钩子知道阶段（例如按「自上次释放以来的记录」成组释放）。那会改 `released` 的行格式，需另立条目（Spec D4 已否于本次）。
- `TF-20261012-c66ad3` 剩下成立的那一半（版本提升重走 N 次声明）仍留在 inbox；若日后要消除重复劳动，方向是让 release 记录按 (version, stage) 复用上一版本的 `kind` 与能力名，而不是改 `seq`。
- 溢出在当前契约下不可观测（多出的记录静默归给下一个阶段）。若实测因此产生误导，考虑让门在释放时把「本次消费的那条记录与剩余条数」写进拒绝路径的诊断，而不是改存储。

## Version History

- v1 — planning，等待用户批准。
