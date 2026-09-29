# 修复 TaskFlow hooks 的四处遗留缺陷
> Task version: v1
> Status: completed

## Goal

修掉归档任务 `TaskFlowDocs/achieved/2026-09-15-hook-integrity/plan.md` 的 `## Follow-ups` 记录的四处 hook 缺陷，每处配一条有判别力的 smoke 断言。

## Background / Confirmed Facts

四条都在当前 base（`main` @ `f5ce0a4`）上复读过，行号即当前行号。

- **标题截断切断多字节字符**：`hooks/task:205` 用 `title = substr(t, 1, 80)` 生成 Todo 条目标题，而 `hooks/task:11-12` 设了 `LC_ALL=C`，awk 在字节语义下按字节切。上次会话实测：非 ASCII 的 goal 在受跟踪的 `todo.md` 里写出非法 UTF-8（`od -c` 末尾为孤立的 `e6`），当时只手工修正了那一条条目。
- **写入写死的 Owner**：`hooks/task:251` 把 `- Owner: Codex` 作为字面量写进每个新条目。全仓库只有这一处出现 `Owner`——没有任何 hook 读它，`skills/taskflow/references/artifacts.md:24` 的 Todo 字段名单里也没有它。于是任何宿主下新建的条目都记成 Codex。
- **核验行静默丢弃**：`hooks/task:292-306` 只在 `line[i] == "## Verification / Review"` 命中时才插入核验行；找不到该标题时既不写也不报错，`progress` 照常打印 `progress OK` 并以 0 退出。标题被翻译或写错时，核验记录就这样消失。
- **路由记录泄漏本地态**：`hooks/repository-docs-context:78-81` 依据未跟踪的 `TaskFlowDocs/repository-docs/personal.md` 决定是否加一行 `personal-rule`，`:256-260` 再依据同一文件渲染 `Status: present / not present`。而 `index.md` 是受跟踪文件（`git ls-files` 命中，`.gitignore` 用 `!` 显式放行），`personal.md` 被 `.gitignore` 整目录忽略。因此有 personal 规则的 clone 上，SessionStart 会把受跟踪的 `index.md` 永久改脏。

两条支撑事实：

- **同类先例**：`57d507a` 用同一手法修掉过一次"每日 dirty"——把 `date` 写进渲染的那一列删掉。本次第 4 条是同一类问题的另一个来源。
- **原子性已有保证**：`hooks/task` 的写路径统一走 `run_awk_to`（`hooks/task:442-457`），awk 写临时文件后 `mv`，awk 非零退出即删临时文件并返回 1。所以 awk 内 `die()` 不会留下半个核验行，fail closed 不需要额外机制。
- **宿主探测已有先例**：`hooks/session-record:82-93` 已经在做宿主身份判定（`AI_AGENT`、`CLAUDECODE` / `CLAUDE_CODE_SESSION_ID`、`CODEX_HOME` / `CODEX_SANDBOX`），产出 `Claude` / `Codex` / 空。

## Requirements

- R1 标题截断只在完整字符边界收边：任何 goal 生成的 `todo.md` 标题都必须是有效 UTF-8；纯 ASCII goal 的结果与改动前逐字节一致，80 字节的上限本身不变。
- R2 `intake` 写入的 `- Owner:` 反映运行它的宿主 agent，判定与 `hooks/session-record:82-93` 一致；无法识别时写 `Unknown`，任何情况下都不再写死 `Codex`。
- R3 `progress` 带 verification 参数而 Plan 里没有 `## Verification / Review` 时 fail closed：命令非零退出、Plan 文件字节不变，不再静默返回成功。
- R4 `index.md` 只承载受跟踪事实：`personal-rule` 行恒定存在，且它的每一列都不随本地 `personal.md` 的有无变化；同一仓库在有/无 `personal.md` 两种状态下渲染出的 `index.md` 字节相同。
- R5 personal rule 的当前存在性由 `repository-docs-context` 的 stdout 路由行按本地实际报出——文件在才有那一行，文件不在就没有。personal 内容不进入仓库。
- R6 四处缺陷各有一条 smoke 断言，且断言有判别力：把修复回退掉会变红。
- R7 修复记入 `CHANGELOG.md` 的 `## [Unreleased]` —— 这四条都不在 1.1.1 里，没有 Release 段落可挂。
- R8 文档与代码一致：`skills/taskflow/SKILL.md:79` 与 `skills/taskflow/references/artifacts.md:11` 关于"index 记录 personal-rule 存在性"的措辞按 R4/R5 改写。

## Design Decisions

- **D1 一个任务、四个步骤**（用户裁定）：四处同出归档 Plan 的 Follow-ups，各自只有几行，第 4 处涉及的是措辞与断言而非独立交付物。
- **D2 Owner 按宿主探测**（用户裁定）：沿用 `session-record` 的既有判定，得到 `Claude` / `Codex` / `Unknown`，保留字段槽位而去掉假值。
- **D3 `index.md` 里保留 personal.md，但只作为路由位置**（用户原话："index.md 中可以写 personal.md，但是 personal 不进入仓库，这样 TaskFlow 框架可以知道有 personal，但不给仓库泄露 personal"）。落实为：表格里那一行恒定出现（`Exists` 列固定 `local`，不再读文件系统），说明性 prose 也稳定；"这个 clone 现在有没有 personal 规则"改由 stdout 路由行报出，因此 TaskFlow 框架每一轮都能知道存在性，而受跟踪文件不承载任何本地事实。
- **D4 不抽公共宿主探测脚本**：`session-record` 的判定只有 12 行，抽 `hooks/agent-id` 会把改动扩散到一个当前正常的 hook 并波及 `runtime.md` 的目录清单。本次在 `hooks/task` 内镜像同一判定，重复本身记为 follow-up。

## Acceptance Criteria

- AC1 `intake` 一个超过 80 字节的中文 goal 后，`todo.md` 中该条目标题行是有效 UTF-8（无孤立前导/续接字节）；同一个 ASCII goal 产出的标题与改动前逐字节相同。
- AC2 在 Claude Code 会话里 `intake` 得到的新条目 `- Owner: Claude`（而不是 `Codex`）；判定在无法识别宿主的环境下退化为 `Unknown`。
- AC3 把 Plan 里的 `## Verification / Review` 改名后，`progress <task> 1 done "<text>"` 非零退出，且 `plan.md` 字节不变。
- AC4 同一仓库分别在"有 `personal.md`"与"删掉 `personal.md`"两种状态下跑 `repository-docs-context`：两次的 `index.md` 字节相同，且都含 `| personal-rule | \`TaskFlowDocs/repository-docs/personal.md\` | all | local | local-only |`；stdout 的 `- Local personal rules …` 行只在文件存在时出现。
- AC5 受影响的 smoke 段落全部通过；本机跑不了整卷时，逐字抽出对应段落单独运行并记录结果，整卷以 CI 为准。

## In Scope

- `hooks/task`（R1、R2、R3）
- `hooks/repository-docs-context`（R4、R5）
- `hooks/smoke-test`（R6，含第 4 处现有断言的改写）
- `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`（R8）
- `CHANGELOG.md`（R7）
- `TaskFlowDocs/repository-docs/index.md`（渲染结果的正常变更：恒定的 personal-rule 行）
- 本任务的 `prd.md` / `plan.md` / `todo.md` 条目

## Out of Scope

- 不改 80 字节的标题上限，也不改标题的其他语义（如截断处的词边界）。
- 不动 `hooks/session-record` 的现有探测逻辑，不新增共享脚本（见 D4）。
- 不追溯修正 `todo.md` 里既有的 `- Owner: Codex` 条目——历史条目不是本次交付物。
- 不处理"标题本地化"（语言声明放 `personal.md`、由 hook 执行），它需要先修订 v1 批准的排除项，是独立的实质性变更。
- 不改 `index.md` 的跟踪状态：`.gitignore` 里"重新纳入 routing record"的决定保持不变。

## Risks / Deferred Items

- **本机 smoke 受限**：`bash hooks/smoke-test` 在 `hooks run with no interpreter available` 段中止（MSYS 无法运行 symlink 出来的二进制：`error while loading shared libraries: ?`），基线在同一处同样失败。受影响的段落逐字抽出单独运行，整卷以 CI 为准。
- **跨 awk 实现**：字符边界判定在字节语义 awk（gawk/mawk/BSD awk 配 `LC_ALL=C`）下按预期收边；在 UTF-8 感知的 awk 下 `substr` 本来就按字符切，该判定退化为空操作。两个方向都不会产生非法 UTF-8。
- **Owner 判定与 `session-record` 重复**（D4 的代价）：新增宿主时需要改两处。记为 follow-up。
- **`hooks/task:295` 之外的同族静默**：本次只让核验行 fail closed；`## Change Log` 等其它段若也被改名，行为不变。不在本次范围。

## Open Questions

无。D1/D2/D3 三处设计决定已由用户裁定，D4 是 D2 的实现细节。

## Version History

- v1 — planning.
