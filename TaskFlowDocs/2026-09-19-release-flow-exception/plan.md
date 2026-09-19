# Plan — 发布不再走 TaskFlow 任务工作流

> Task version: v1
> Status: in_progress

No spec required — 规则文本的改写与一处断言替换，无跨层契约。

## Reference Pointers

- `RELEASE.md` —— 发布程序本身；本改动把它从「任务流程的一个用例」改为「独立程序」。
- `skills/taskflow/SKILL.md` 的 `## Applicability gate`、`skills/taskflow/references/artifacts.md` 的 `## Release task documents` —— 规则的两处权威落点。
- `TaskFlowDocs/todo.md` 的 `TF-20260919-76e7fb` 与 `TF-20260919-2877ca` —— 本任务的来源条目，两者既有的根因分析已逐条复核。
- `TaskFlowDocs/achieved/2026-09-17-release-v1-0-6/` —— 受旧规则影响的先例（141 行）。最后一份旧规则的产物 `TaskFlowDocs/2026-09-18-release-v1-0-7/`（116 行）已按用户 2026-09-19 的授权删除，见 Follow-ups。

## Related Tasks

- Related: `achieved/2026-09-13-revise-release-flow/`（确立直接打标签为默认路径）、`achieved/2026-09-15-release-friction/`（建立 `release-check` 与发布文档规则）。
- 本任务完成 `TF-20260919-2877ca`（规则放在哪才不会被跳过）——答案就是 `RELEASE.md` 自己。

## Skills / Tools Used

- **Unaided** —— 未调用外部能力。根因由仓库自身证据核对（`hooks/task promote` 的 `small|large` 分支、`CONTRIBUTING.md` 的分支硬规则、历史发布任务的文档行数）；断言由 `hooks/smoke-test` 自身执行；无外部资料、无 LLM 判定工具。

## Preconditions

- [x] Todo 条目 `TF-20260919-40eca2` 已 promote 为本任务。
- [x] 工作树与分支：`.worktrees/release-flow-exception` / `chore/release-flow-exception`，基于 `main`（`7dcff62`）。
- [x] `RELEASE.md`、`CONTRIBUTING.md`、`CODE_STYLE.md`、`skills/taskflow/SKILL.md`、`references/artifacts.md` 已读。
- [x] 消费者已核对：`hooks/release-check`、`hooks/repository-check`、`hooks/smoke-test`、`.github/workflows/hooks.yml` 中无一处要求「发布必须有任务文档」。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-19 10:23 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — 把发布边界写进六个规则落点

- Goal: 任何在执行发布时会被读到的规则文件，都不再把发布算作普通任务。
- Dependencies: 无。
- Files: `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`RELEASE.md`、`CONTRIBUTING.md`、`README.md`、`README.zh-CN.md`。
- Implementation checklist:
  - [x] `SKILL.md` 适用性门禁：移出 `release preparation`，写明例外、例外中的回口（显式 `$taskflow`、发布本身改插件），并把 frontmatter `description` 里的同一项一并去掉。
  - [x] `artifacts.md`：`## Release task documents` 改为「发布不使用任务文档」，记录 = CHANGELOG 段 + Release 正文，批准门禁随程序走。
  - [x] `RELEASE.md`：开头声明执行位置与不创建任务；`## Before release` 首句改为 `Open the release from the base checkout`；批准门禁写明在第 5 步推送之前；三处「record … in the release task」改为写进发布正文。
  - [x] `CONTRIBUTING.md`：`## TaskFlow workflow` 与 `## Working branches` 各加一句例外（不切分支的理由：发布打的正是它已验证的 base 提交）。
  - [x] 两份 README：适用性句与 `RELEASE.md` 指引各一行。
- Acceptance: 六个文件中不再出现「发布创建一个任务」的表述；`grep -rn 'release task'` 在 `skills/`、`hooks/`、根文档中无命中。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout -- <file>` 逐个还原；本改动无外部可见影响，未打标签、未推送。
- Status: done

### Step 2 — 用 smoke-test 锁住新边界

- Goal: 任一句规则被改回旧形态时，测试立刻失败并指出文件。
- Dependencies: Step 1（断言锁的是 Step 1 写下的文本）。
- Files: `hooks/smoke-test`。
- Implementation checklist:
  - [x] 替换原「release task documents point at the procedure」一节（它锁的是旧规则，改完必然失败）为「a release runs RELEASE.md instead of the task workflow」。
  - [x] 五条断言分别覆盖 `artifacts.md`、`SKILL.md`、`CONTRIBUTING.md`、`RELEASE.md`，其中批准门禁一条单独锁住「门禁没被删掉」。
  - [x] 断言路径用 `$repo`（该节已有的仓库根变量），不新引入变量。
  - [x] 变异验证一次一个：改坏 `RELEASE.md` 的关键句 → 该节报 `FAIL RELEASE.md does not exclude the task path`；还原后 `ALL SMOKE PASSED`。
- Acceptance: `bash hooks/smoke-test` → `ALL SMOKE PASSED`；变异后该节失败。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout -- hooks/smoke-test`。
- Status: done

### Step 3 — 回写来源条目并收尾

- Goal: 两个来源 Todo 条目的状态与本任务的结论一致，不留下互相矛盾的说法。
- Dependencies: Step 1、Step 2。
- Files: `TaskFlowDocs/todo.md`。
- Implementation checklist:
  - [x] `TF-20260919-40eca2` 的 Notes 已记录用户确认的四个选择与本条改动落点。
  - [x] `TF-20260919-76e7fb` 与 `TF-20260919-2877ca` 的 `Next action` 与 Notes 已回写为「由本任务交付」，并指明落点。
  - [x] `TF-20260919-40eca2` 的 `Status` 随 `task state` 推进为 `in_progress`。
- Acceptance: `bash hooks/task get <id>` 三条目的状态与结论一致。
- Verification: 见 `## Verification / Review`。
- Rollback: 条目状态按原值改回。
- Status: done

### Step 4 — 让授权删除不再被 todo-merge-audit 判为丢失

- Goal: 本任务删除 Todo 条目后，CI 的 `todo-merge-audit` 把「按授权删除」与「merge 静默丢条目」判成同一件事并报 `needs-user-input`。让删除自证，同时不削弱对真实丢失的检查。
- Dependencies: Step 1（删除动作来自 Step 1 的范围）。
- Files: `hooks/task`、`hooks/todo-check`、`hooks/smoke-test`。
- Implementation checklist:
  - [x] `hooks/task remove <todo-id> <reason>`：写入 `## Removed` 记录后再删条目；已 promote 的条目拒绝删除（否则任务目录变孤儿），未知 ID 与空理由也拒绝。
  - [x] `hooks/todo-check` 增加 `removed_at`：`## Removed` 段里锚定行首的 ID 从「丢失」集合中扣除；无记录时行为完全不变。
  - [x] `hooks/smoke-test` 新增一节，覆盖记录落点、条目消失（计数与标题两条）、兄弟条目与文件头存活、第二次删除不新开段、promoted 拒绝、未知 ID/空理由拒绝。
  - [x] 回归验证：一个真实 drop 的 merge fixture 仍旧 `FAIL`（`TF-X present in … but missing from …`），而记录过的删除放行。
- Acceptance: `bash hooks/smoke-test` → `ALL SMOKE PASSED`；真实 drop fixture 仍报 `needs-user-input`；本分支的 `todo-check` 区间审计为 `pass`。
- Verification: 见 `## Verification / Review`。
- Rollback: `git checkout -- hooks/task hooks/todo-check hooks/smoke-test`。
- Status: done

## Checkpoints

- Step 1 后：`grep -rn 'release task'` 无命中。
- Step 2 后：`bash hooks/smoke-test` → `ALL SMOKE PASSED`，且变异验证失败过一次。
- Step 3 后：三个 Todo 条目的 `Status` / `Task` / `Next action` 互相一致。

## Verification / Review

Step 1–2 实施于 2026-09-19；Step 3 于 10:23 批准后完成。全部命令在本任务 worktree（`chore/release-flow-exception`）内执行。

| 检查 | 命令 | 实际输出 |
| --- | --- | --- |
| smoke | `bash hooks/smoke-test` | `ALL SMOKE PASSED`，`grep -c FAIL` = 0 |
| 变异验证 | 改坏 `RELEASE.md` 关键句后重跑 | `FAIL RELEASE.md does not exclude the task path`（还原后转为 `ALL SMOKE PASSED`） |
| 仓库就绪 | `bash hooks/repository-check .` | `needs-user-input` —— 只因为改动未提交（它在报「这个检出的未提交任务产物」），非缺陷；提交后即 `pass` |
| 版本一致性 | `bash hooks/release-check .` | `STATUS: pass`（字面量未动） |
| evals | `python3 evals/runner.py` | `PASS (6 evals)` |
| Skill 校验 | `python3 <skill-creator>/scripts/quick_validate.py skills/taskflow` | `Skill is valid!` |
| 空白 | `git diff --check` | clean |

Step 4 的验证（同一 worktree，2026-09-19 追加）：

| 检查 | 命令 | 实际输出 |
| --- | --- | --- |
| `task remove` 行为 | 临时 fixture 连删两条 + 边界 | 记录落 `## Removed`、条目与其标题消失、兄弟条目与文件头存活、二次删除不新开段；promoted 条目、未知 ID、空理由均被拒并保持文件不变 |
| `todo-check` 回归 | 一个真实 drop 的 merge fixture | 仍报 `TF-X present in … but missing from …` / `needs-user-input`（exit 2），未被新逻辑放过 |
| `todo-check` 放行 | 同一 merge fixture 加 `## Removed` 记录 | `Records 1 authorized deletion(s)` → `STATUS: pass` |
| 本分支区间审计 | `bash hooks/todo-check . "7dcff62..HEAD"` | `Merge commits in range: 0` → `pass`（本分支无 merge） |
| smoke | `bash hooks/smoke-test` | `ALL SMOKE PASSED`（新增一节；首次运行时 fixture 缺 `cc` 条目与断言过宽，均已修正） |

**未跑**：无。

## Change Log

- 2026-09-19 v1 — 规则改写与断言替换；affects `SKILL.md`、`references/artifacts.md`、`RELEASE.md`、`CONTRIBUTING.md`、两份 `README`、`hooks/smoke-test`。
- 2026-09-19 v1 — 用户当场确认「发布不切分支」，`CONTRIBUTING.md` 的例外句据此补上理由。
- 2026-09-19 v1 — 用户批准 Plan（`+0800`，Approval 块已记录）；`task state` 推进为 `in_progress`；来源条目回写完成。
- 2026-09-19 v1 — Step 4：CI 的 `todo-merge-audit` 在 PR #42 报 `TF-20260918-985164 present in … but missing from …`。这是 Step 2 的删除触发的**误报**，不是缺陷——检查无法区分「授权删除」与「merge 丢失」。按用户决定给删除留痕：`hooks/task remove` 先写 `## Removed` 再删，`hooks/todo-check` 认这段记录。修改了 `hooks/task`、`hooks/todo-check`、`hooks/smoke-test`。

## Follow-ups

- 2026-09-19 用户复核 —— 本条记录的处置：`TaskFlowDocs/2026-09-18-release-v1-0-7/` 与其 Todo 条目 `TF-20260918-985164` 已删除（用户明确授权）。删掉之后，代码仓库里不再存在「发布任务文档」这一产物，本任务的规则因此有了实物佐证：规则、断言与先例三者一致。v1.0.7 自身的发布事实仍在 Git 历史、`v1.0.7` 标签、`CHANGELOG.md` 与 GitHub Release 里——正是本规则规定的记录形态。修改了 `skills/taskflow/references/artifacts.md` 的一处 Reference Pointer。

## Version History

- v1 — planning.
