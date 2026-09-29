# Plan — Hook integrity: unpolluted archives, unbypassable gates, user-language documents
> Task version: v2
> Status: checking

No spec required — three localized fixes in existing hooks plus a documentation rule.

## Spec Pointers

No spec required — 三个既有 hook 的局部修复加一条文档规则，无跨层契约；v2 只改规则文本与断言。

## Reference Pointers

- `hooks/version` — 已经被取代文档的写入路径；R1 加在其归档循环之前。
- `hooks/task` — `state` 分支里已有的批准校验就是 `complete` / `progress` 要复用的那套，理由与文案需一致。
- `hooks/smoke-test` — 断言风格、`digest` 助手、fixture 目录约定。
- `TaskFlowDocs/2026-09-15-no-python-hooks/old/v1/version.md` — 上一次归档污染的实际记录，R1 就是为了不再产生它。
- `old/v1/` — 本任务被取代的 v1 版本（PRD 全文）。
- v2：`hooks/task:214,222,295,378,394,401,508,647,829,837,907`、`hooks/version:113,141`、`hooks/reopen:23`、`hooks/todo-check:61`、`hooks/summarize-state:105,116,127`、`hooks/session-record:269,276,282` — 英文标题名单的每一个匹配点；`hooks/task:604-710` — `promote` 写出整个大纲的位置。

## Related Tasks

- `TaskFlowDocs/2026-09-15-no-python-hooks/`、`TaskFlowDocs/2026-09-15-todo-merge-driver/` — 待归档；本任务的 R2 决定它们能否通过 `complete`（两者 Approval 均为 `approved`，可通过）。
- `TaskFlowDocs/2026-09-15-macos-hook-portability/` — Approval 为 `requested` 而 Step 为 `done`；R2 落地后 `complete` 会（正确地）拦下它。

## Skills / Tools Used

- [PRD] Unaided — 需求边界由本轮对 `origin/main` @ `65ddd0a` 的 hook 实测（逐条 grep 匹配点）+ 三轮依赖排序提问确定；considered: requirements elicitation and framing。
- [Plan] Unaided — 分解为"改规则文本 / 扩 smoke 断言 / 补 CHANGELOG"三个可独立验证的步骤；considered: work breakdown and task decomposition。

## Preconditions

- [x] 适用仓库文档与个人规则已读；无优先级冲突。
- [x] 远程 / 分支：`origin` = `hkwuks/TaskFlow`，base = `origin/main`，本地分支 `fix/hook-integrity`，独立 worktree。PR 模板为 `.github/pull_request_template.md`。
- [x] 本任务不新建治理文档。
- [x] v2：v1 文档集已从 `TaskFlowDocs/achieved/2026-09-15-hook-integrity/` 取回活动区，v1 快照位于 `old/v1/`；本轮分支 `fix/artifact-language-heading-scope`，worktree `.worktrees/2026-09-15-hook-integrity`。
- [x] v2 实施中基线前移：起分支时的 `65ddd0a` 已被 `main`/`origin/main` 超过 8 个提交（v1.1.1 + capability-pre-write-gate 合并）。已 rebase 到 `477ced6`；`CHANGELOG.md` 冲突按用户决定两侧都保留（`## [Unreleased]` 在 `## [1.1.1]` 之上，排序遵循仓库惯例），并逐字节比对确认 `## [1.1.1]` 段与 `main` 一致。其余改动文件自动合并，全树无冲突标记。
- [x] v2：新基线新增写前能力门禁（`hooks/capability-gate` / `capability-evidence`）且 `task approve` 改为按门禁 release 记录核对阶段行。本任务两个阶段都确实未调用任何 capability，已用 `hooks/task unaided` 声明并由门禁生成 `released` 记录（见 Verification）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-29 19:33 +0800
- Approved version: v2
- Approved scope: PRD / Plan

## Steps

### Step 1 — 让 `hooks/version` 拒绝污染归档

- Goal: 归档的一定是"被取代的那一版"，而不是被 v2 编辑覆盖后的工作区副本。
- Dependencies: 无。
- Files: `hooks/version`、`hooks/smoke-test`。
- Implementation checklist:
  - [x] 归档循环开始前，对每个要归档的文档判断：被 Git 跟踪（`git ls-files --error-unmatch`）且 `git diff --quiet` / `git diff --cached --quiet` 报告有改动 → 失败退出，不写任何文件。未被跟踪的文档不检查。
  - [x] 拒绝文案指明下一步：先提交被取代的版本，归档对象就是那次提交。
  - [x] 检查在**任何写入之前**（含 `mkdir -p old/vN`）完成，失败不得留下半个归档。
  - [x] smoke：被跟踪且有未提交改动时 `version` 失败、`old/v1` 不存在、根文档字节未变；提交后重跑成功。
- Acceptance: 污染场景被拒绝且无副作用；干净场景（含未跟踪 fixture 目录）行为与今天一致。
- Verification: `hooks/smoke-test` 新增段 "version refuses to archive uncommitted tracked documents"——真实 `git init` fixture 上：脏的被跟踪文档被拒、`old/v2` 不存在、根文档字节未变；提交后归档成功且内容等于该提交；未被跟踪的文档即使脏也照常归档。手工复验：干净任务上 `version v2` 成功，追加一行未提交内容后 `version v3` 被拒并打印 `prd.md has uncommitted changes; ...`。回归验证：把该 guard 从 `hooks/version` 摘掉，smoke 立刻红在 `FAIL version archived an uncommitted tracked document`。
- Rollback: 去掉该检查，恢复原写入顺序。
- Status: done

### Step 2 — 把语言规则的英文边界收窄为显式名单

- Goal: 规则读起来是一份"哪些名字必须英文"的名单，而不是"所有章节标题都必须英文"；未被 hook 匹配的标题归入正文散文，跟随用户语言。
- Dependencies: 无（与 Step 1 无交互）。
- Files: `skills/taskflow/references/artifacts.md`、`skills/taskflow/SKILL.md`、`hooks/smoke-test`、`CHANGELOG.md`。
- Implementation checklist:
  - [x] `artifacts.md` 的 `## Artifact language` 改写为显式名单：hook 按名字匹配的章节标题（`## Approval`、`## Skills / Tools Used`、`## Verification / Review`、`## Change Log`、`## Items`、`## Removed`、`## Active / Resumable`、`## Closed / Reference Only`）、条目标题（`### Step N — <name>`、`### SN — <Agent>`）、`## Approval` 的五个字段（`- Status:`、`- Approved by:`、`- Approved at:`、`- Approved version:`、`- Approved scope:`）、Todo 字段名、`> Task version:` / `> Status:` / `> Current Task version:` 等行、`- Status:` 行、`- [ ]` / `- [x]` 标记。
  - [x] 同一段落说明：未被匹配的章节标题（`## Requirements`、`## Checkpoints`、`## Follow-ups` 等）属于正文，跟随用户语言；并说明 `## ` 前缀仍被当作章节边界，翻译标题不影响边界识别。
  - [x] 规则明说 `hooks/task promote` 写出的英文骨架标题不受语言规则支配（R5）。
  - [x] `SKILL.md` 的对应句子同步收窄，删去"`## ` headings"这类整体表述。
  - [x] `hooks/smoke-test` 的语言规则段：把英文名字名单钉住，并新增行为断言——把 fixture 中一个未被匹配的标题（`## Checkpoints`）改成中文后，`task state` / `task step` / `task progress` 仍成功。
  - [x] `CHANGELOG.md` 加 `## [Unreleased]` 段记录该语言规则及其 v2 收窄（补 v1 缺失的变更记录）。
- Acceptance: `artifacts.md` 不再出现"`## ` headings"这类整体表述；名单每一条都能在 hooks 里找到匹配点或生成点；翻译 `## Checkpoints` 后 `task` 解析命令仍成功；`promote` 的新建骨架仍为英文。
- Verification:
  - **本机无法跑完整套件**：`bash hooks/smoke-test` 在 "hooks run with no interpreter available" 段中止（`FAIL session-record failed without an interpreter`，MSYS 无法运行 symlink 出来的二进制，`error while loading shared libraries: ?`）。该段与本次改动无关（1.1.1 的 Known limitations 也记录同一点），所以判据是 **CI（ubuntu / macos-latest / windows）**，由 PR 的运行结果裁定。
  - 语言规则两段（`== artifact language rule is documented…` 与新增的 `== a heading the language rule leaves as prose…`）在 rebase 后**逐字从 `hooks/smoke-test` 抽出单独运行，两段均 `ok`**。
  - 判别力（证明断言不是摆设）：把 fixture 的 `## Verification / Review` 翻成 `## 验证 / 审查` 后，`task progress` 的核验行 `named-heading-must-not-land` **不再落入** Plan —— 即该名字确实是承重的；而把未被匹配的 `## Checkpoints` 翻成 `## 检查点` 后 `task state` 与 `task progress` 都正常，核验行 `prose-heading-ok` 正常落入。断言写成"没有落入"而非"命令失败"，这样将来把静默丢弃改成显式报错也不会让本条回归。
  - 实测中发现并修掉自己的一个错误：fixture 根目录必须先 `mkdir -p`，否则 `task intake` 报 `root not found`（单独运行该段时才暴露）。
  - 阶段记录（新契约）：`task unaided PRD --considered 'requirements elicitation and framing'`、`task unaided Plan --considered 'work breakdown and task decomposition'` 各写一条 evidence；再按宿主的方式对 `prd.md` / `plan.md` 各发一次合成 `PreToolUse` 事件让 `hooks/capability-gate` 释放阶段，得到 `released` 两行 `v2|PRD|…|unaided|…`、`v2|Plan|…|unaided|…`。复跑 `task approve` 通过并打印 `stages released by the gate: 0 invoked, 2 unaided` —— 将来本任务再需批准不会 fail closed。（副作用：`- Approved at:` 被这次复跑刷新为 `2026-09-29 19:33 +0800`，批准依据未变。）
- Rollback: `git revert` 本步的规则文本与 smoke 断言，恢复 v1 的笼统表述（`old/v1/prd.md` 记录 v1 措辞）。
- Status: done

## Checkpoints

- Step 1 完成后：先在一个被跟踪且有未提交改动的真实任务上手工验证拒绝路径，再动 Step 2。
- Step 2 完成后：在 `macos-hook-portability` 上确认 `complete` 被拦（预期行为），不动它的文档。
- v2 Step 2 完成后：本机**无法**跑完整 `bash hooks/smoke-test`——它在"无解释器"段中止（MSYS 无法运行 symlink 出来的二进制，`error while loading shared libraries: ?`），而基线在**同一处**同样失败（1.1.1 的 Known limitations 也记录同一点），因此不是本步回归。判据改为：语言段逐字抽出单独运行须 `ok`，完整套件交给 CI（ubuntu / macos-latest / windows）裁定。

## Verification / Review

- 三个缺陷各有"复现 → 修复 → 断言"的完整证据链，断言全部用真实 `git` 行为而非脚本调用模拟。
- 逐个验证每个新断言会在对应缺陷回归时失败（临时回退一行代码确认变红），避免"断言写得刚好通过"。
- v2 的判据是"名单与实测匹配点一致"，不是"文本看起来更窄"：名单每条都要指到具体的 hook 行号；翻译标题的行为断言必须在把 `## Verification / Review` 也翻译时变红。

## Pre-PR checks and template mapping

PR：**#59** — https://github.com/hkwuks/TaskFlow/pull/59（head `fix/artifact-language-heading-scope` → base `main`）。分支已推送并设置 upstream。

`CONTRIBUTING.md` 的三项检查与 `.github/pull_request_template.md` 的逐字段映射（模板路径已读：`.github/pull_request_template.md`）。

| 检查 | 结果 |
| --- | --- |
| `bash hooks/smoke-test` | **不可用（本机）**：在 "hooks run with no interpreter available" 段中止，MSYS 无法运行 symlink 出来的二进制（`error while loading shared libraries: ?`）；基线在同一处同样失败，1.1.1 的 Known limitations 亦记录同一点。语言规则两段已逐字抽出单独运行并 `ok`。完整套件交给 CI（ubuntu / macos-latest / windows）裁定。 |
| `python3 …/quick_validate.py skills/taskflow` | **通过** —— `Skill is valid!`。注意必须 `PYTHONUTF8=1`：本机 locale 为 GBK，直接运行会以 `UnicodeDecodeError: 'gbk' codec can't decode byte 0x94` 失败；这是宿主 locale 问题，不是 Skill 问题。另外本机 `python3` 解析到 WindowsApps 的 redirector 桩（`python3 -c "print(...)"` 无输出却 exit 0），必须用 `python3.12`。 |
| `git diff --check` | **干净**（`477ced6..HEAD` 无空白错误） |

| 模板字段 | 取值 |
| --- | --- |
| Summary | 把 artifact-language 规则的英文边界从"所有 `## ` 章节标题"收窄为 hook 精确匹配的显式名单；非匹配标题归入正文、跟随用户语言；并补上 v1 从未记录的 CHANGELOG 条目 |
| Task: | `TaskFlowDocs/2026-09-15-hook-integrity/`（v2；v1 归档于 `old/v1/`） |
| Scope | `skills/taskflow/references/artifacts.md`、`skills/taskflow/SKILL.md`、`hooks/smoke-test`、`CHANGELOG.md`，以及本任务 PRD / Plan（含 `old/v1/`、`todo.md` 条目）。**不改任何 hook 行为** |
| Base branch | `main` |
| Target repository | `https://github.com/hkwuks/TaskFlow`（`origin`；无凭据） |
| Verification 四项 | `smoke-test` 不可用并已在 Plan 记录原因；`git diff --check` 干净；`quick_validate.py` 通过；结果全部记录于本 Plan |
| Review boundaries 四项 | 无密钥或不可读远端载荷；未改无关任务或用户文件（取回的是本任务自己的归档目录）；远程 / 基线假设已在上表逐条写明；已知限制与 follow-up 见本节与 `## Follow-ups` |

- [x] Remote/base 假设：`origin` = `hkwuks/TaskFlow`，base = `main`（`477ced6`）。未新增或改写任何 remote。
- [x] 未推送、未创建 PR 之前不得声称 CI 结果。

## Change Log

- 2026-09-29 reopen — retrieved achieved task `2026-09-15-hook-integrity` for new work; re-approval required before core changes (`hooks/reopen` 的规范行；本次用 `git mv` 完成同一移动以保留 Git 重命名追踪)
- 2026-09-15 Step 1 实现 —— `hooks/version` 增加受跟踪文档的未提交改动检查（`git ls-files --error-unmatch` + 两次 `git diff --quiet`），放在 `mkdir -p old/vN` 之前；smoke 新增真实仓库 fixture 段。
- 2026-09-15 Step 1 验证时误在真实任务上跑了 `version 2026-09-15-no-python-hooks v3`：该任务在本 worktree 内已被跟踪且干净，guard 正确地放行，于是产生了 `old/v2/` 并把三个文档推到 v3。已用 `git checkout` 与删除未跟踪目录完整回退，`git status` 确认无残留。教训与 R1 的设计一致：guard 只能拦住"脏工作区"，拦不住"在错误的分支/worktree 里对干净文档执行正确的命令"。
- 2026-09-29 任务取回并升为 v2 —— 用户指出 v1 的语言规则把"章节标题"整体划为英文，而实测只有少数标题被 hook 按名字匹配；同时用户质疑该规则"只在 CODE_STYLE 里"，实测它由提交 `87c30e5` 落在 `artifacts.md` / `SKILL.md` / `CODE_STYLE.md` 三处、且该提交 message 与 `CHANGELOG.md` 均未提及语言。取回自 `achieved/`，v1 归档于 `old/v1/`；顺带修掉 v1 文档早于 stage gate 的两处形态（`## Skills / Tools Used (Optional)` → `## Skills / Tools Used`，补 `[PRD]` / `[Plan]` 行），否则 `task approve` 会 fail-closed。
- 2026-09-29 v2 范围决策 —— 用户确认：只收窄规则，不做标题本地化（`promote` 写出整个大纲，收窄规则本身不产生可观察行为变化，收益是规则准确 + 可检索）；标题本地化方案（语言声明放 `personal.md`、由 hook 读并写出对应语言标题）记为 follow-up，需要时先改"不引入语言探测"这条排除项。
- 2026-09-29 Step 2 实施 —— `artifacts.md` 的 `## Artifact language` 改为显式名单（含"名单即边界、翻译非匹配标题安全、`promote` 骨架为英文"三条说明），`SKILL.md` 对应句子同步收窄，`hooks/smoke-test` 的语言段扩为名单 pin + 反向检查（不得再出现"`## ` headings"整体表述）+ 新增行为段，`CHANGELOG.md` 加 `## [Unreleased]`（含 v1 缺失记录的追溯说明）。
- 2026-09-29 Step 2 实施中发现并在本次修掉：新 smoke 段的 fixture 缺 `mkdir -p`，`task intake` 以 `root not found` 失败；该错误只在把该段单独运行时可暴露。
- 2026-09-29 基线前移与冲突决策 —— 起分支的 `65ddd0a` 已被 `main` 超过 8 个提交。rebase 到 `477ced6` 时 `CHANGELOG.md` 冲突（`main` 在同一锚点加了 `## [1.1.1]`）。**用户决定：两侧都保留**，`## [Unreleased]` 置于 `## [1.1.1]` 之上。已逐字节确认 `## [1.1.1]` 段与 `main` 一致、全树无冲突标记，其余文件自动合并。
- 2026-09-29 新契约对齐 —— `main` 新增写前能力门禁，且 `task approve` 改为按门禁 release 记录核对阶段行。本任务两个阶段确为 Unaided，已声明并让门禁生成 `released` 记录；`task approve` 复跑通过（`0 invoked, 2 unaided`），并把 `- Approved at:` 刷新为 `2026-09-29 19:33 +0800`。批准依据未变，无需重新取得批准。
- 2026-09-29 进入 checking 并开 PR —— 本机三项 pre-PR 检查结果：`smoke-test` 不可用（既有 MSYS 段），`quick_validate.py` 通过（需 `PYTHONUTF8=1`），`git diff --check` 干净。分支已推送，开 **PR #59**。`repository-check` 仍报两项既有项：`Base: ambiguous`（推分支后应消失）与 orphan `achieved/2026-09-10-repository-document-placement`（1.1.1 亦记录为 pre-existing）。任务尚未完成：待 CI 三平台与用户验收。

## Follow-ups

- 待归档的 no-python-hooks / todo-merge-driver 正文保持英文（用户决定），不追溯。
- 标题本地化（若将来要做）：语言声明放 `TaskFlowDocs/repository-docs/personal.md`，由 hook 读它并写出非匹配标题的对应语言；`promote` 骨架中 hook 匹配的标题仍保持英文。与 PRD 的"不引入语言探测/i18n 机制"排除项冲突，重开时必须先修订该排除项（材料性变更，需重新批准）。
- 仓库级问题（不在本任务范围）：`hooks/repository-docs-context` 的 SessionStart 同步会在主检出上改写受跟踪的 `TaskFlowDocs/repository-docs/index.md`（`## Personal rules` 段），使工作区常驻未提交改动；与提交 `57d507a` 修掉的"每日 dirty"是同一类问题。
- 仓库级问题（不在本任务范围，本轮编辑 todo.md 时实测）：`hooks/task:204` 的 `title = substr(t, 1, 80)` 在字节语义的 awk（BSD awk / mawk，即本仓库 runtime.md 规定的底线）上会**切断多字节字符**，于是非 ASCII 的 goal 在受跟踪的 `todo.md` 里写出非法 UTF-8 标题（实测 `od -c` 末尾为 `... 347 224 250 346 \n`，一个不成对的 `e6`）。本次只手工修正了本任务条目的标题，未改 hook。
- 仓库级问题（不在本任务范围）：`hooks/task:251` 的 intake 模板把 `- Owner: Codex` 写死，任何宿主下新建的 Todo 条目都会记成 Codex；本任务条目已手工改为 `Claude`。
- 仓库级问题（不在本任务范围，做 Step 2 的行为断言时实测）：`hooks/task:295` 找不到 `## Verification / Review` 时**不报错也不记录**——`progress` 会静默丢掉那条核验行并照常返回成功。这正是把该标题列进英文名单的理由，但"静默丢弃"比"显式失败"差：标题被翻译或写错时没有任何提示。建议后续让缺失该段时 fail closed。本次的断言写成"核验行没有落入"，与将来改成显式报错不冲突。

## Version History

- v1 — planning。
- v2 — 收窄语言规则的英文边界为显式名单；补 `CHANGELOG.md` 记录。取回自 `TaskFlowDocs/achieved/2026-09-15-hook-integrity/`。
