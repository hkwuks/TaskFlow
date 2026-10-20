# Plan — 证据锚点：让拒绝点名记录真正的落点

> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md` — 诊断查找的契约、文案形状与不变量（I1–I6）。

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — 适用的仓库文档与阶段。
- `CONTRIBUTING.md:16-33` — 分支/worktree 隔离；本任务从 `52fc3e4` 起在 `.worktrees/2026-10-11-evidence-anchor`。
- `skills/taskflow/references/runtime.md` 的 four properties — 第一条「per worktree (one task, one worktree)」是本轮保留的不变量（PRD B4）。
- `hooks/capability-gate:102-124`（gate 的定位链）、`hooks/capability-evidence:60-67`（evidence 的定位链）— 两个锚点的代码位置（PRD B1）。
- `hooks/capability-gate:133-139` — `released` 的全局 seq 语义，这是「真统一」被排除的成本依据（PRD B5）。
- `skills/taskflow/SKILL.md:122-131`、`:256`(Phase 5) — 文档侧两半的落点。
- `TaskFlowDocs/achieved/2026-09-10-audit-hook-opportunities/reference/hook-audit.md:81` — `UserPromptSubmit` 的否决记录（相邻任务的约束，本条不下探）。

## Related Tasks

- Parent: None.
- Children: None.
- Depends on: None.
- Blocks: None.
- Related: 本条吸收 `TF-20261008-84a0ce`（文档侧那半）。`TF-20261009-8abbd6`、`TF-20261009-cc463b` — 「已发生调研的入账」由它们承担；本条只让失配可诊断，正是为那条留出干净的后续（PRD 的 Out of Scope）。`TF-20261010-82ec77`、`TF-20261010-taskflow-first-order` — 入口层同族，已归档。

## Skills / Tools Used

- [PRD] Unaided — no capability applied to this phase; considered: requirements elicitation and framing
- [Spec] Unaided — no capability applied to this phase; considered: architecture and design specification
- [Plan] Unaided — no capability applied to this phase; considered: work breakdown and task decomposition

三阶段都用 `hooks/task unaided` 声明。本阶段的工作是读本仓库自己的两个 hook 与既有 smoke 夹具、并在一次性夹具里复现锚点错配；三个设计决定（锚点方案 / 搬移层级 / 钉住方式）已由用户裁定，没有外部能力可补充这些文档未承载的信息。

## Preconditions

- [x] 适用的仓库文档与个人规则已检查、优先级/冲突已记录。`repository-docs/index.md` 路由 `CONTRIBUTING.md`（design,code,commit,pr,release）与 `CODE_STYLE.md`（code,review）；无仓库文档规范证据库的锚点。本 clone 无个人规则。
- [x] 远程/fork/PR 工作：`origin` = `hkwuks/TaskFlow`，base = `main`，本分支从 `52fc3e4` 起。Step 3 在任何推送前复核。
- [x] PR 模板：`.github/pull_request_template.md` 为 phase `pr` 的适用文档；Step 3 逐字段映射并记录模板路径与验证。
- [x] 缺失治理草案与显式批准：不适用——本任务不创建任何缺失的治理文档。
- [x] 核心文档单一写者：Primary Agent（Claude）。分支 `fix/evidence-anchor`，worktree `.worktrees/2026-10-11-evidence-anchor`。
- [x] 既有用户裁定已记录：见 PRD 的 Open Questions。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-11 10:21 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 让 gate 在拒绝前查明记录落在了哪个工作树

- Goal: R1–R4 落在 `hooks/capability-gate`：即将 deny 时做一次只读的同级 worktree 查找，命中则把落点写进拒绝信息；不改变任何放行路径。
- Dependencies: None.
- Files: `hooks/capability-gate`。
- Implementation checklist:
  - [x] R1：实现改为从 `--absolute-git-dir` 反推 common dir（`spec.md` 的 Implementation Note 说明了为什么不用 `--git-common-dir`：它在 worktree 里返回相对路径，而归一化需要知道基准目录；`--path-format=absolute` 会抬高 Git 版本下限）。按 `spec.md` 的枚举契约 glob `<common>/taskflow/evidence` 与 `<common>/worktrees/*/taskflow/evidence`，排除本库自身。
  - [x] R1：命中（存在且行数 > 0）则拼出诊断句，含该库路径、它所属的 worktree、记录数，以及两侧各自是什么。
  - [x] R2：诊断结果**只进文案**，绝不参与放行判定。
  - [x] R3：文案给出可执行下一步——`git branch --show-current` + `pwd` 自查，然后「在本工作树重跑调用」或「把工作搬进来」并指向 `SKILL.md`。
  - [x] R4：只在即将 deny 的两条路径上执行；无 git / 无 common dir / 无同级 / glob 无匹配 / 记录为 0 行，一律静默降级到现有文案；所有 `git` 调用带 `2>/dev/null` 且接受失败。
  - [x] I4：文案不含双引号与反斜杠（路径先 `tr '\134' '/'`）；保留既有断言要求的 `[<STAGE>]`、概念类别、`task unaided <STAGE> --considered`。
  - [x] I5：只用 `git`、内建 glob、`case`、`printf`。
- Acceptance: PRD A1–A3（A1 由 Step 2 的夹具裁决）。
- Verification: 用 PRD B2 的一次性夹具手跑四种形态（失配 / 同树 / 无记录 / 无 git）；`bash -n` 与 bash 3.2 解析。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

### Step 2 — 用 main+worktree 夹具把它钉住

- Goal: A1/A2/A3 由断言而不是靠人记着。
- Dependencies: Step 1.
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 新增独立一节：夹具为主检出 + `git worktree add` 出的 linked worktree，两个树各有自己的任务目录（沿用 `cg_root` 的命名风格，但自建、自清理）。
  - [x] A1 正向：`capability-evidence` 带基础检出 `cwd` 写下记录；gate 检查 worktree 内任务的 `prd.md` → deny，且文案含记录真实所在的库路径。
  - [x] A2 反向：在 worktree 里正常记录 → 同树放行，不回归。
  - [x] A3（变异验证，不在断言内）：去掉查找 → A1 红。
  - [x] 夹具 git 操作带 `-c user.email/-c user.name`；末尾 `rm -rf`；不依赖前一节的 `$tmp` 状态。
  - [x] 遵守 bash 3.2 陷阱：heredoc 里的撇号、`cmd && { ...; }`。
- Acceptance: PRD A1、A2、A5。
- Verification: `bash hooks/smoke-test` 全量；变异验证一次一个，做完确认工作树干净。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

### Step 3 — 文档侧：把「搬进去」写成可执行步骤

- Goal: R5–R7 落在 `SKILL.md`，并由断言钉住。
- Dependencies: None（与 Step 1/2 无文件重叠）。
- Files: `skills/taskflow/SKILL.md`、`hooks/smoke-test`（A4 的断言可并入 Step 2 的新节或就近加在既有 Skill 断言区）。
- Implementation checklist:
  - [x] R5：「Isolate before the first document」补搬移步骤 `git stash push -u` / `git stash pop`，并说明未修改的已跟踪文件不需要搬。
  - [x] R6：同段补「确认自己在哪个工作树」的可检查动作，以及基础检出脏状态的含义。
  - [x] R7：Phase 5 的 `then move the work there` 改为指向该步骤。
  - [x] A4：断言钉住三条命令与 Phase 5 的指向措辞。
  - [x] 新段落使用**用户工作语言**（这是散文不是机器读取的行）。
- Acceptance: PRD A4。
- Verification: `bash hooks/smoke-test`；变异——删掉 `git stash pop` 一行 → A4 红。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

### Step 4 — 全量验证与收尾

- Goal: 确认没有打破既有断言与无解释器不变量，并留下可复核的记录。
- Dependencies: Step 1, Step 2, Step 3.
- Files: 本任务 `plan.md`（验证记录）、`skills/taskflow/references/runtime.md`（A6）、`TaskFlowDocs/todo.md`（状态）。
- Implementation checklist:
  - [x] A6：`references/runtime.md` 的 four properties 增补一条（拒绝会点名记录的真实落点；库仍按工作树分离），正文补一句 gate 描述。
  - [x] `bash hooks/smoke-test` 全量；确认 no-interpreter 一节仍通过（A5）。
  - [x] `git diff --check`。
  - [x] `bash hooks/release-check .`。
  - [x] `quick_validate.py skills/taskflow`（`/home/hk/miniconda3/envs/torch/bin/python`）。
  - [x] `bash -n` 与 `docker run --rm -v "$PWD:/w" -w /w bash:3.2 bash -c 'bash -n …'`。
  - [x] 在 `## Verification / Review` 记录每条命令与结果，区分既有/新引入/环境失败，并记录三个方向的变异验证。
  - [x] 读 `.github/pull_request_template.md`，逐字段映射并记录模板路径与验证结果。
  - [x] 推送后记录 CI 三 host 矩阵结果（含 run 链接）。
- Acceptance: PRD A6。
- Verification: 上述命令输出逐条记录在 `## Verification / Review`。
- Rollback: revert 承载本 Step 的 commit。
- Status: done

## Checkpoints

- CP1（Step 1 后）：四种形态手跑结果与 PRD B2 的复现一致；放行路径零改动（`git diff` 只增不移动既有权重逻辑）。
- CP2（Step 2 后）：失配被点名、同树不回归；变异各触发一次；no-interpreter 一节未被新代码破坏。
- CP3（Step 3 后）：文档步骤可照抄执行；断言钉住三条命令。
- CP4（Step 4 收尾）：全套命令通过、验证记录与 PR 模板映射写入本文件、CI 绿。

## Verification / Review

逐条记录命令与结果。区分：**既有失败**（改动前就存在）/ **新引入失败** / **环境失败**。

| 检查 | 结果 | 分类 |
| --- | --- | --- |
| `bash hooks/smoke-test`（全量） | exit 0，`ALL SMOKE PASSED`，68 个 `ok` 节；新增两节各自 `ok` | 通过 |
| **变异验证 1**：`stray=""`（关掉诊断查找） | `FAIL the denial does not say the records are elsewhere` | 断言有效（A1 被咬住） |
| **变异验证 2**：删掉 `SKILL.md` 的 `git stash pop` 行 | `FAIL the move procedure does not land the work in the worktree` | 断言有效（A4 被咬住） |
| 恢复两处后重跑全量 | `ALL SMOKE PASSED`，`git status` 仅本轮 4 个文件 + 任务目录 | 通过 |
| 失配的两个方向（断言内，各自独立夹具） | 方向一：记录在基础检出、检查 worktree 文档 → 拒绝且点名基础检出库；方向二：镜像 → 拒绝且点名 linked worktree | 通过（PRD A1） |
| 同树不回归（断言内） | worktree 与基础检出各自在自己的库里放行自己树内的文档 | 通过（PRD A2） |
| 空库降级（断言内） | 无任何记录时不出现「another working tree」那句，文案回到原状 | 通过（R4） |
| 无解释器不变量 | no-interpreter 一节仍通过；诊断只用 `git`、内建 glob、`case`、`printf` | 通过（PRD R8、I5） |
| `bash -n hooks/capability-gate`、`hooks/smoke-test` | 无输出 | 通过 |
| `docker run --rm -v "$PWD:/w" -w /w bash:3.2 bash -c 'bash -n …'` | 两个文件都 `bash 3.2 OK` | 通过 |
| `git diff --check` | `CLEAN` | 通过 |
| `bash hooks/release-check .` | `STATUS: pass` | 通过 |
| `quick_validate.py skills/taskflow` | `Skill is valid!`，用 `/home/hk/miniconda3/envs/torch/bin/python` | 通过 |

### 实现期修正（两处，均由实测咬出）

1. **common dir 的来源改了。** `spec.md` 第一稿写 `git rev-parse --git-common-dir`。实测（git 2.43）：基础检出返回 `.git`（相对），linked worktree 返回 `/abs/repo/.git`（绝对）——归一化时无从判断基准。改用 `--path-format=absolute` 需 git ≥ 2.31，而这个 hook 在别人机器上运行，不该抬高下限；最终从**已经绝对化的** `--absolute-git-dir` 反推。已写入 `spec.md` 的 Implementation Note。
2. **`own` 的取值错了。** 第一版把 `git_dir` 直接当作 `own` 比较，而实际路径是 `$git_dir/taskflow/evidence`——于是本库永不被排除，诊断在最该触发的场景里静默。是断言先红（`FAIL the worktree document was released by the base checkout's record` 之后的一连串）咬出来的。

### 断言自身的一次修正

新增节的第一版把两个方向放在**同一个夹具**上，而两者要求「另一棵树的库为空」这一互斥状态：先记录 base 再测方向一，base 的记录会让 worktree 的文档真的被放行，断言就以错误理由变红。改成**每个方向一个夹具**（`wk` 与 `wk2`），并在节内注明为什么不能合并。这条过程留在本节，因为「一个夹具同时问两个互斥的问题」是同类断言最容易重犯的错。

**CI 结果**（`Hooks` workflow）：[run 38107432916](https://github.com/hkwuks/TaskFlow/actions/runs/38107432916)，commit `3bc7a34` — **success**，三 host 矩阵 + `release` / `evals` / `todo-merge-audit` 全部通过。

### PR 模板映射（`.github/pull_request_template.md`，phase `pr` 的适用文档）

模板路径已核对（25 行、4 节）。每个字段的映射：

| 模板字段 | 落点 | 状态 |
| --- | --- | --- |
| Summary | PR [#78](https://github.com/hkwuks/TaskFlow/pull/78) 正文首节——两个锚点的实测复现、gate 的诊断、以及库边界不变 | 已完成 |
| TaskFlow traceability: Task | `TaskFlowDocs/achieved/2026-10-11-evidence-anchor/` | 已确定 |
| TaskFlow traceability: Scope | PRD 的 In Scope：`hooks/capability-gate`、`hooks/smoke-test`、`SKILL.md`、`references/runtime.md`、本任务文档 | 已确定 |
| TaskFlow traceability: Base branch | `main`（`origin` = `hkwuks/TaskFlow`），本分支从 `52fc3e4` 起 | 已验证 |
| TaskFlow traceability: Target repository | `hkwuks/TaskFlow`，凭据不写入 | 已验证 |
| Verification: Hooks workflow pass | [run 38107432916](https://github.com/hkwuks/TaskFlow/actions/runs/38107432916)，commit `3bc7a34`，全绿；已写入 PR 正文 | 已完成 |
| Verification: `git diff --check` | 见上表：`CLEAN` | 已记录 |
| Verification: Skill/plugin validation | `quick_validate` `Skill is valid!`、`release-check` `STATUS: pass` | 已记录 |
| Verification: Results recorded in the Plan | 本节 | 已完成 |
| Review boundaries（4 条） | 无凭据写入；`git status` 仅本轮 4 个文件 + 任务目录；`origin`/`main` 已核对；见 `## Follow-ups` | 已完成 |

## Change Log

- 2026-10-11 work revision — 任务由 `TF-20261001-efbc51` promote 创建（吸收 `TF-20261008-84a0ce`）；用户裁定三个设计决定（保持库边界 + 失配可诊断 / 只补文档步骤 / 新增 main+worktree 夹具节），写入 PRD 的 Open Questions 与 `spec.md` 的 Design Decisions；affects `prd.md`, `spec.md`, `plan.md`, `TaskFlowDocs/todo.md`。

## Follow-ups

- 同名任务目录下的跨库放行仍未修（PRD Risks 第一条）：基础检出库里的一条记录能放行 worktree 里的同名任务文档。修它需要「记录带工作树归属」，属被排除的「真统一」。
- 诊断查找按默认布局（`<common>/worktrees/*`）枚举；`--separate-git-dir` 等非默认布局静默降级。
- 搬移步骤是 prose：`git stash push -u` 在基础检出有 staged 改动时的行为由 Git 定义，本任务不重新定义它。
- 本任务落地后需一次发布才惠及已安装用户。

## Version History

- v1 — 规划中，等待用户批准。

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- 2026-10-10 用户裁定：本条吸收 TF-20261008-84a0ce（主检出的工作怎么进 worktree）。两条是同一失败模式「干活的落点不是以为的落点」的两半——efbc51 是 hook 侧（事件 cwd 与文件路径两个锚点不一致，记录静默落空），84a0ce 是文档侧（SKILL.md 只写「move the work there」而不给可执行步骤，也不警告隔离外的脏状态）；合并后一个任务同时改 hook 与 SKILL.md，且 84a0ce 不必等 efbc51 的锚点语义定下来才能写步骤。
