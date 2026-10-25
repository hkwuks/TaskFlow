# Plan — 本地文件由插件排除，不要求用户改 .gitignore

> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers

- `hooks/install-git-hygiene` —— 契约的权威实现（本任务从 `install-merge-driver` 改名而来）。既有三段（driver config → `info/attributes` → exit）的顺序与 `|| exit 0` 的停法必须保留，新增段接在末尾。
- `hooks/smoke-test:3268-3495` —— 既有的安装段（`install_root` 与 `non_git` 两个夹具）。新断言并进这一段，不另起平行段落；目录清单断言的失败消息会指出漏名的文件。
- `hooks/smoke-test:5273-5320` —— `doc_tree` 解析四份文档的目录树。改名后旧名会以「names files that do not exist」变红，这既是检出手段，也是 A5 的天然断言。
- `.gitignore:12-18` —— 我上一轮加的 `sessions.md` 规则与它的四行注释，本任务删除。

## Related Tasks

- `TF-20261025-24d06c`（inbox，**子任务**）—— 撤销 8 份已提交 `sessions.md` 的跟踪。依赖本任务先落地排除机制，否则 `git rm --cached` 之后它们立刻以未跟踪状态回到 `git status`。
- `related: TF-20261025-33b2c4` —— 「全局忽略会让已跟踪副本对 CI 隐形」。本任务的 A3 就是它的答案，实施后并入本任务结论。
- `TF-20261024-b48e56`（inbox）—— 同一批文档（`SKILL.md:179`、`artifacts.md:99/130`、`runtime.md:63`）的措辞改动，但改的是 Unaided 的表述，不是 local-only 的机制，两者不重叠。

## Skills / Tools Used

- [PRD] `agent-skills:spec-driven-development` — purpose: 把「local-only 写在文档里、没有任何机制」变成可测的需求与边界；outcome: succeeded; incorporated: R1–R6 与 A1–A8，以及「作用域必须等于 clone」这条边界及其理由。
- [Spec] `agent-skills:api-and-interface-design` — purpose: 定 hook 的退出语义、幂等契约与 `info/exclude` 的规则形状；outcome: succeeded; incorporated: 三种静默跳过的完整清单、逐行精确匹配、`**` 一条覆盖两处位置、失败即停、以及把改名当作破坏性变更写进 Changed。
- [Plan] `agent-skills:planning-and-task-breakdown` — purpose: 拆成可独立验证的 Step 并排出依赖；outcome: succeeded; incorporated: 四步拆分（hook / 调用点与仓库内旧名 / 文档 / 断言）与三个检查点。
- [Test] Unaided — no capability applied to this phase; considered: testing strategy

## Preconditions

- [x] 适用仓库文档已读：`CONTRIBUTING.md`、`CODE_STYLE.md`、`TaskFlowDocs/repository-docs/index.md`、`skills/taskflow/SKILL.md`、`references/artifacts.md`、`references/runtime.md`、`hooks/README.md`。无冲突。
- [x] 远程/PR 前置：单 remote `origin` = `hkwuks/TaskFlow`，base `main@0833dca`，分支 `chore/git-hygiene` 从它创建；PR 模板已读（上一个任务的同一份）。
- [x] 无 personal rule（`TaskFlowDocs/repository-docs/personal.md` 不存在）。
- [x] 四个实测前提见 `prd.md` 的 Background：`.gitignore` 的侥幸、8 份已提交副本、被跟踪文件不受 ignore 影响、`info/` 为 per-clone 且 worktree 共用。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-25 12:44 +0800
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — 改名并新增 `info/exclude` 写入

- Goal: R1、R2。`hooks/install-merge-driver` → `hooks/install-git-hygiene`，头注释改写，末尾接一段写两条规则。
- Dependencies: 无。
- Files: `hooks/install-merge-driver`（重命名）→ `hooks/install-git-hygiene`。
- Implementation checklist:
  - [x] `git mv hooks/install-merge-driver hooks/install-git-hygiene`。目录清单断言按文件名比对，`git mv` 后改名这一半立刻可验。
  - [x] 头注释改为三样写入；保留「repository-local and untracked」「best-effort」两句。
  - [x] `LOCAL_ONLY` 常量：`personal.md` 一行、`**/sessions.md` 一行。
  - [x] `git rev-parse --git-path info/exclude`，`case` 补绝对路径前缀（与 `info/attributes` 同形），`mkdir -p` 后写；已存在的行用 `grep -qxF --` 逐行跳过。
  - [x] 结尾 `exit 0` 保留；新增段失败走 `|| exit 0`，不继续后续（已是末段，语义上是「停下」）。
  - [x] 注释写清：为什么是 `info/exclude` 而不是 `.gitignore`（作用域 = clone），以及规则只对未跟踪文件生效。
- Acceptance: A1、A2、A4。
- Verification: 临时仓库手工跑三次（首次 / 二次 / 已有一行），`diff` 比对 `info/exclude`；`bash -n hooks/install-git-hygiene`。
- Rollback: `git mv hooks/install-git-hygiene hooks/install-merge-driver && git checkout -- hooks/`.
- Status: done

### Step 2 — 调用点与仓库内旧名清零

- Goal: R1 的另一半。`session-start` 调新名字；仓库树里不再出现旧文件名。
- Dependencies: Step 1（文件得先存在）。
- Files: `hooks/session-start`, `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [x] `hooks/session-start:172` 的调用与上方三行注释改为新名字，注释补一句它也排除本地文件。
  - [x] `grep -rn 'install-merge-driver'` 确认只剩文档（Step 3 处理）与 `achieved/` 历史（不改）。
  - [x] `README.md` / `README.zh-CN.md` 的目录树改名并同步说明列（这两处是仓库根文档，不是 hooks 目录清单，但目录树会误导）。
- Acceptance: A5（代码侧）。
- Verification: `grep -rn 'install-merge-driver' -- . ':!TaskFlowDocs/achieved'`；`bash -n hooks/session-start`。
- Rollback: `git checkout -- hooks/session-start README.md README.zh-CN.md`.
- Status: done

### Step 3 — 五份文档同步，撤掉 `.gitignore` 那一条

- Goal: R3、R4。写清机制、作用域、退化路径；规则只剩一个出处。
- Dependencies: Step 1、2 定下实现。
- Files: `hooks/README.md`, `skills/taskflow/references/runtime.md`, `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`, `.gitignore`, `CHANGELOG.md`.
- Implementation checklist:
  - [x] `hooks/README.md`：目录树行、`install-*` 条目改名并说明三样写入、Scope 段（`:257-264`）扩写。
  - [x] `runtime.md:255` 的 wiring 段与 `:300` 的目录树。
  - [x] `SKILL.md:93`、`:122` 与 `artifacts.md:7`、`:13` 的 local-only 句补「由插件排除」「没跑过 hook 要手动跑一次」。
  - [x] `.gitignore` 的 `sessions.md` 规则保留，注释改写为「它管克隆本仓库的人，插件管用户自己的项目」这一分工（用户追问后改的，见 Change Log）。`repository-docs/*` 那三行不动。
  - [x] `CHANGELOG.md`：`Changed` 记 hook 改名（破坏性，给新名字）；`Added` 记两个本地文件被自动排除。
- Acceptance: A6、A7。
- Verification: `grep -rn 'install-merge-driver'` 只剩 `achieved/` 与 CHANGELOG 的改名记录；`git diff --check`。
- Rollback: `git checkout --` 六份文件。
- Status: done

### Step 4 — 断言改写与新增

- Goal: R5。既有安装段改名并补 A1–A4，另加「旧名不存在」这一条。
- Dependencies: Step 1–3。
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] `:3275`、`:3379`、`:3462`、`:3475`、`:3488`、`:3624` 六处 `install-merge-driver` 改成新名。
  - [x] `install_root` 夹具里补：两条规则在 `info/exclude` 中各出现一次；二次运行 `info/exclude` 逐字节不变；`git check-ignore -q` 对 `TaskFlowDocs/x/sessions.md` 与 `repository-docs/personal.md` 命中。
  - [x] 已跟踪副本不被忽略：`git add -f` 一份 `sessions.md` 提交后再改，`git status --porcelain` 仍见它，`git check-ignore` 返回未命中。
  - [x] `non_git` 夹具补 `info/exclude` 不存在。
  - [x] 仓库内不再出现旧文件名（`grep -r`，排除 `achieved/`）。
  - [x] 变异验证：逐条改坏 → 套件红 → `cp` 还原 → `diff -q`。
- Acceptance: A1–A5。
- Verification: `bash hooks/smoke-test < /dev/null`；`bash -n hooks/smoke-test`。
- Rollback: `git checkout -- hooks/smoke-test`.
- Status: done

## Checkpoints

- Step 1 后：临时仓库里两条规则生效，二次运行 `info/exclude` 逐字节不变。
- Step 2 后：`grep` 旧名只在文档与 `achieved/` 里。
- Step 3 后：`.gitignore` 无 `sessions.md`；`git diff --check` 干净。
- Step 4 后：`bash hooks/smoke-test` 全绿；变异逐条验证过。

## Verification / Review

- 2026-10-25 Step 4: block added and passing; mutations caught; .gitignore rule restored as a scoped complement

- 2026-10-25 Step 3: five docs, .gitignore reverted to repository-only rules, CHANGELOG Added+Changed

- 2026-10-25 Step 2: session-start and both README trees call the new name

- 2026-10-25 Step 1: scratch repo: rules written, idempotent byte-identical, tracked copy still visible, non-git silent

待实现后填写。

## Change Log

- 2026-10-25 v1 — 建 PRD / Spec / Plan。用户三轮问答定下载体（扩展并改名 `install-merge-driver` → `install-git-hygiene`）、子任务切分（8 份已提交副本留给 `TF-20261025-24d06c`）、无 hook 的兜底（文档写一句，不加代码）。
- 2026-10-25 用户追问「我写到 git 屏蔽文件也没有什么错呀」，据此把 R3 从「删掉 `.gitignore` 那一条」改成「保留并写明分工」。理由成立：两条规则作用域不同——`.gitignore` 跟着仓库走，管刚克隆还没跑 hook 的树；`info/exclude` 跟着 clone 走，管用户自己的项目。前者正是我把它删掉后留下的缺口。影响 `prd.md`、`spec.md`、`.gitignore`。

## Follow-ups

- **`TF-20261025-24d06c`** 是子任务，不是本任务的 Follow-up 条目，但本任务不完成它，仓库就仍然带着 8 份陈旧会话索引。
- **没有卸载路径**：删掉 `info/exclude` 的两行就是卸载；不提供命令，也不打算提供。

## Version History

- v1 — planning.
