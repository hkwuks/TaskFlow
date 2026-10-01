# Plan — Reconcile the artifact-language rule with capability-written documents: a phase
> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

无独立 `reference/`。判据全部来自仓库自身的规则文本与提交历史，已写入 `prd.md` 的 Confirmed Facts：

- `87c30e5`（2026-09-15）引入规则原文（无作用域限定）与 `hooks/smoke-test` 钉字符串段。
- `38adbbb`（2026-09-29）收窄为显式名单，并新增以 `hooks/task promote` 为主语的骨架豁免句。
- `d72c2b2`（2026-09-28）能力门就位，使调用能力成为阶段常规步骤。
- `achieved/2026-09-27-capability-pre-write-gate/` 与 `achieved/2026-09-30-release-ci-test-policy/` 的正文语言对比。

## Related Tasks

- Depends on: None
- Blocks: None
- Related: `TaskFlowDocs/achieved/2026-09-15-hook-integrity/`（`38adbbb` 所属任务，收窄规则的那次）；`TaskFlowDocs/achieved/2026-09-27-capability-pre-write-gate/`（阶段前置门，决定了本任务所处的调用流）；`TaskFlowDocs/achieved/2026-09-30-release-ci-test-policy/`（本次偏离的实例来源）

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — purpose: 用其六要素清单核对 PRD 是否把要求写成可观察验收而非待采纳的措辞；outcome: succeeded；incorporated: 采纳其「surface assumptions」要求，把未言明的前提落成 Risks 的三条遗留与一条相邻缺陷，并把 `## Open Questions` 保持为零。**修订说明**：v1 初稿的诊断（「规则写的是谁来写」）不正确，经用户指出后按 commit 历史重写——规则原文本就起草者中立，真正的出口是 `38adbbb` 引入的骨架豁免句被读宽。该修正来自用户，不由本次调用产生。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 用其依赖图与「先建地基」的顺序纪律决定改动先后与归属，并检查每步验收与验证是否成形；outcome: succeeded；incorporated: 定义处先于指针处、钉字符串再后（钉必须钉最终措辞），成为 Step 1 → 2 → 3 的顺序；「折入点自带语言」从句并入定义处所在的同一 Step，而不是另立一步。

## Preconditions

- [x] Worktree `.worktrees/artifact-language`，分支 `docs/artifact-language`，基于 `main` 的 `6424f12`；**且会话 cwd 已切入该工作树**。后者是前置条件而非细节：`capability-evidence` 按事件 `cwd` 定位证据库与活动任务（`hooks/capability-evidence:58-79`），会话停在主检出时阶段证据不落盘，门随后按被写文件路径拒绝写入（`hooks/capability-gate:119`）。
- [x] Applicable repository documents and personal rules inspected; precedence/conflicts recorded. 适用：`CONTRIBUTING.md`（Checks、§ Where the commit lands）、`CODE_STYLE.md`（第 9 行是本规则第三处陈述，本次不动）。不适用：`RELEASE.md`。`TaskFlowDocs/repository-docs/index.md` 已读，无冲突。
- [x] For remote/fork/PR work: remotes, target repository, base branch, local branch/base, freshness limits, and required checks recorded. `origin` = `hkwuks/TaskFlow`（非 fork），base `main`，本地分支自 `6424f12` 分出。改动含 Skill 措辞与 `hooks/smoke-test`，按 § Where the commit lands 属「措辞值得评审的文档」，走 PR；CI `Hooks` 三平台为准。
- [x] For PR creation/update: applicable template path, every required-field mapping, and template verification recorded. 模板 `.github/pull_request_template.md`，Step 4 逐项映射。
- [x] Missing governance drafts and explicit approvals recorded before they become binding. 无缺失治理文档。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-01 12:35 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — Generalize the exemption at its definition site

- Goal: 让 `artifacts.md` § Artifact language 成为唯一、来源无关的定义处——规则绑定目的文档；骨架豁免对 `hooks/task promote` 与能力模板共用一句，且明说它不覆盖用它填出来的正文。
- Dependencies: None
- Files: `skills/taskflow/references/artifacts.md`
- Implementation checklist:
  - [x] `:17` 规则本体的措辞带出「与起草者无关」一层（R1）。新句落在 `:19`。
  - [x] `:27` 豁免句的适用范围改为来源无关，并点明它只管骨架自身标题、不管正文（R3、A4）。改写后位于 `:29`。
  - [x] `:146` 折入指令补语言从句：折入的是结构，语言随内容一同重渲（R2、A3）。补后位于 `:145`。
  - [x] `:19-25` 英文行名单逐条不动（R6、A7）；`the lines they match stay English verbatim` 与 `are not rewritten for language` 两处被钉的字符串保持原样（名单段整体未进入 `git diff`）。
- Acceptance: A2、A3、A4、A7
- Verification: 只读该节即可判定（A2）；`:19-25` 与改动前逐条比对不变（A7）；`git diff --stat` 只列本文件。
- Rollback: `git checkout -- skills/taskflow/references/artifacts.md`
- Status: done

### Step 2 — Point the Skill's one-liner at the tightened rule

- Goal: `SKILL.md:46` 的一句话版本跟上，使只读 `SKILL.md` 的 Agent 也能判定（A1），且不复述边界名单。
- Dependencies: Step 1（先有定义，再有指针）
- Files: `skills/taskflow/SKILL.md`
- Implementation checklist:
  - [x] `:46` 补「与起草者无关」一层；维持「一句规则 + 指向 `artifacts.md`」的既有分工，不复制名单、不新增段落。
  - [x] 保留被 `hooks/smoke-test:1254` 钉住的 `in the user's working language` 字面。
- Acceptance: A1、A6
- Verification: 只读该段即可判定（A1）；与 `artifacts.md` 交叉核对，无二义、无重复定义（A4）。
- Rollback: `git checkout -- skills/taskflow/SKILL.md`
- Status: done

### Step 3 — Pin the new clauses in the existing smoke-test section

- Goal: 让 R2、R3 的新措辞进入 `hooks/smoke-test` 既有的「artifact language rule」那一节，下一次收窄不能静默删掉它（R7）。
- Dependencies: Step 1、Step 2（钉的是最终措辞）
- Files: `hooks/smoke-test`
- Implementation checklist:
  - [x] 在 `:1248-1272` 那一节内新增针对新措辞的钉字符串，沿用该节既有的写法（`grep -q -F` + 失败即 `exit 1` 并指明缺失项）。实为 4 条 clause 钉在 `artifacts.md`、1 条钉在 `SKILL.md`，并附一段说明为何必须钉住。
  - [x] 不新增独立小节、不新建第二套检查；不改已钉的名字列表、不改反向禁止那一对。
- Acceptance: A8
- Verification: 临时删掉被钉条款 → 该节**失败**并指出缺失项；恢复后通过。这条同时证明新钉不是空写（A8）。
- Rollback: `git checkout -- hooks/smoke-test`
- Status: done

### Step 4 — Verify, then land by pull request

- Goal: 按 A1–A9 完成验收，并按仓库落地规则以 PR 提交。
- Dependencies: Step 1、2、3
- Files: 无（验收与提交；PR body 依据 `.github/pull_request_template.md`）
- Implementation checklist:
  - [x] 逐条核对 A1–A9，结论写入 `## Verification / Review`。
  - [x] `git diff --stat` 复核改动面；`CODE_STYLE.md`、`evals/**`、`.github/**` 零改动（A6）——字面偏差已记入 Verification。
  - [x] 两条本地静态检查（`CONTRIBUTING.md` § Checks）：`git diff --check`；`quick_validate.py skills/taskflow`（本机 `python3` 为 Store stub，以 `python` 代之，并需 `PYTHONUTF8=1`，见 Verification）。
  - [ ] 推分支、开 PR、按模板逐项填字段；smoke 套件整体不在本地重跑，判定以 CI `Hooks` 三平台为准（A9）。
  - [x] A5 的下游复核义务写入 `## Follow-ups`，并在 `TaskFlowDocs/todo.md` 另立相邻缺陷的待办（`TF-20261001-efbc51`）。
- Acceptance: A1–A9 全部满足；CI `Hooks` 三平台通过。
- Verification: CI run URL 记入本 Plan；PR 模板字段逐项映射。
- Rollback: 丢弃分支即可，`main` 未受影响。
- Status: in_progress

## Checkpoints

- [x] Step 1 后：`artifacts.md` 单读可判，且英文行名单与两处被钉字符串逐条未变。
- [x] Step 2 后：两文件交叉核对无重复定义、无悬空指针。
- [x] Step 3 后：删条款能令该节失败，恢复后通过。
- [ ] Step 4 后：A1–A9 逐条有结论，CI `Hooks` 通过，PR 已开且模板字段完整。

## Verification / Review

- **A1 —— 达成（阅读式）。** 只读 `SKILL.md:46`：段中新增「The rule binds the document, not its drafter: a capability invoked for a phase supplies a shape to fill, and prose folded in from it is written in the user's working language like any other.」持有英文能力模板的读者据此可判。
- **A2 —— 达成（阅读式）。** 只读 § Artifact language：`artifacts.md:19` 正面写出规则绑定目的文档；`:29` 写出骨架下方的正文「is yours, and it is in the user's working language however the words around it are phrased」。骨架标题与骨架下方正文的归属分列两处，可分别作答。
- **A3 —— 达成。** 折入指令 `artifacts.md:145` 末句：「Rewriting it covers the language as well as the structure: what folds in is the shape, and the prose is rewritten in the user's working language rather than carried over from whoever produced the draft.」读者无需回到 § Artifact language。
- **A4 —— 达成。** 豁免只有 `artifacts.md:29` 一处定义，主语来源无关（「`hooks/task promote` writes one into every new document, and a capability invoked for a phase brings its own」），并以「That exemption ends at the headings.」划出上限。
- **A5 —— 未到执行时点。** 观察性验收，义务已写入 `## Follow-ups`，由下一个调用阶段能力的任务承担。
- **A6 —— 达成，但字面有一处必须点明。** `git diff --stat` 为四个文件：`hooks/smoke-test`(+10)、`skills/taskflow/SKILL.md`(+1/−1)、`skills/taskflow/references/artifacts.md`(+6/−2)、`TaskFlowDocs/todo.md`(+8/−3)。第四个是本任务自己的 Todo 条目，本仓库每个任务提交都带着它（`7d7a60d`、`cb4423e` 各带 15 行 `todo.md` 改动），A6 第一句漏列了它——判据写窄，非改动越界，本任务不对 A6 作事后改字。A6 明列的排除项 `CODE_STYLE.md`、`evals/**`、`.github/**` **零改动**，逐条成立；任务目录 `TaskFlowDocs/2026-10-01-artifact-language/` 为新增未跟踪文件。
- **A7 —— 达成。** `artifacts.md` 的英文行名单整段未进入 `git diff`；`hooks/smoke-test` 原已钉的 14 个名字与 `^## Approval$`、`^- Status:`、`> Task version:`、`### Step ` 四个 token 全部继续匹配；两条反向禁止（`` `## ` section headings ``、`` `## ` headings ``）未被触发。
- **A8 —— 达成。** 新增的 5 条钉字符串逐条命中原条款；把 `That exemption ends at the headings` 从副本里删去后该钉不再匹配，即被删时该节会 `exit 1` 并打印 `FAIL artifact language rule does not pin: …`。
- **A9 —— 见下。** 本地不重跑 smoke 套件；判定以 CI `Hooks` 工作流三平台结论为准。
  - CI run: 待推分支后填写。

**未在本地重跑、且如实记为「未跑」的检查**：`bash hooks/smoke-test` 整段在本机 Windows + MSYS 上跑不完（无解释器章节因软链启动的二进制找不到 DLL 而中止，未修改的 `origin/main` 在同一处同样失败），故按 `CONTRIBUTING.md` § Checks 交给 CI。上面 A7/A8 是我手工执行该节**等价 grep** 的结果，不是套件运行结果，两者不得混读。

**本地静态检查**：`git diff --check` 干净；`python …/quick_validate.py skills/taskflow` 首次以本机默认 `gbk` 编码读取时抛 `UnicodeDecodeError`（宿主环境问题，与本次改动无关），加 `PYTHONUTF8=1` 后输出 `Skill is valid!`。

## Change Log

- 2026-10-01 v1 — 建立 v1：三项决策落为 R1–R7、A1–A9 与四个 Step；`affects` `prd.md`、`plan.md`。
- 2026-10-01 v1 — 用户指出诊断有误（规则原文本就起草者中立，不存在「按谁写限定」），据提交历史重写诊断并调整范围：改动面 2 → 3 文件（加入 `hooks/smoke-test` 钉字符串），验收由纯阅读式改为「钉字符串可失败 + CI 三平台」加一次下游复核；`CODE_STYLE.md` 明确不动。`affects` `prd.md`、`plan.md`。
- 2026-10-01 v1 — Step 1–3 实现完成并逐条验收 A1–A9：`artifacts.md` 规则本体 / 骨架豁免 / 折入点从句，`SKILL.md:46` 指针，`hooks/smoke-test` 新增 5 条钉字符串；A6 的字面偏差（任务自带 `todo.md` 未列入）如实记入 Verification 而非事后改字；相邻缺陷另立 `TF-20261001-efbc51`。`affects` `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`hooks/smoke-test`

## Follow-ups

- A5：下一个调用阶段能力的任务，在归档前复核其 `prd.md`/`spec.md`/`plan.md` 的正文语言，结论记入该任务 `plan.md`；结论为「正文非用户工作语言」即视为本次修复未生效。
- 相邻缺陷（本任务不修，另立待办）：`capability-evidence` 用事件 `cwd` 定位证据库与活动任务，`capability-gate` 用被写文件路径定位；会话 cwd 不在任务工作树时，阶段证据不落盘、门拒绝写入。修法待定。

## Version History

- v1 — planning.
