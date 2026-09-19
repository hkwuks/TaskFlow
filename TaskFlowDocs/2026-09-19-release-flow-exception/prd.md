# 发布不再走 TaskFlow 任务工作流
> Task version: v1
> Status: in_progress

## Goal

发布直接在 base 检出上执行 `RELEASE.md`，不创建 Todo 条目、任务目录、分支、PRD 或 Plan；一次发布的唯一记录是它的 `CHANGELOG.md` 段落与 GitHub Release 正文。把这条边界写进 Agent 在发布时真正会读到的每一处规则，并用 `hooks/smoke-test` 锁住它，使下一个版本不再重走一遍通用任务流程。

## Background / Confirmed Facts

- **根因（`TF-20260919-76e7fb` 已记，本次逐条核对确认，非推测）**：
  1. `hooks/task promote <todo-id> <task-id> <small|large>` 只有两个尺寸选项，没有发布形态，于是每个发布任务都被生成成通用七节 PRD 骨架（Goal / Background / Requirements / Acceptance / In Scope / Out of Scope / Risks / Open Questions），而 `skills/taskflow/references/artifacts.md` 的「Release task documents」规则要求记录决策与结果、不重述程序——生成的骨架与规则直接冲突，每次都靠人手削。重量趋势即证据：v1.0.4 77 行 → v1.0.5 101 → v1.0.6 141 → v1.0.7 116。
  2. `CONTRIBUTING.md` 的「一个任务一个短生命周期分支」没有给发布留例外，而 `RELEASE.md` 的默认路径是直接从 `main` 打标签。两条规则冲突时默认读到的是 `CONTRIBUTING.md`，于是 2026-09-19 的发布自加了 `chore/release-v1-0-7`。
  3. 规则是渐进披露的：`RELEASE.md` 与 `artifacts.md` 都写着正确答案，但发布的最初几步不会去读 `artifacts.md`——规则存在不等于规则生效。
- **用户决定（2026-09-19，已逐项确认）**：发布彻底不走 TaskFlow（不创建任务目录与 Todo 条目）；记录形态取「只在 `CHANGELOG.md` 段落 + GitHub Release 正文」；写入方式取「纯文档规则、Agent 手写」；分支取「豁免」；批准门禁改为「用户授权先行，再执行不可逆动作」。
- **用户当场追问并确认**：发布不切分支。
- 现行机制事实：`hooks/release-check` 只比较版本字面量与 marketplace pin，不读任务文档；`hooks/repository-check` 认「`prd.md` 或 `plan.md` 存在」即为任务目录，两者都不因本改动需要调整。CI 的 `release` 作业只跑 `release-check`。

## Requirements

- R1: `skills/taskflow/SKILL.md` 的适用性门禁不再把发布列为自动适用，并写清例外边界：发布不创建任务文档；`$taskflow` 显式调用，或发布本身要改插件，仍是普通开发任务。
- R2: `RELEASE.md` 自身声明它直接在 base 检出执行、不创建任务、不写 PRD/Spec/Plan，并保留不可逆动作（打标签、推 pin、建 Release）之前的批准门禁。
- R3: `CONTRIBUTING.md` 的 `## TaskFlow workflow` 与 `## Working branches` 各留发布例外，后者说明理由是「发布打的正是它在 base 检出的那个已验证提交」。
- R4: `references/artifacts.md` 的发布节改为「发布不使用任务文档」，不再要求 `prd.md` / `plan.md`。
- R5: 两份 README 的适用性句与 `RELEASE.md` 指引与规则同步。
- R6: `hooks/smoke-test` 用断言锁住新边界，并替换掉锁旧规则的那一节。

## Acceptance Criteria

- 仓库中不再存在旧规则的文本：`release task`、`Create a release TaskFlow task`、`record … in the release task`。
- `bash hooks/smoke-test` → `ALL SMOKE PASSED`。
- 变异验证：把新断言对应的任一句文本改坏，该节 `FAIL` 并给出具体文件名。
- `bash hooks/repository-check .` → `pass`；`bash hooks/release-check .` → `pass`（版本字面量未动）；`git diff --check` clean。

## In Scope

- 六个规则文件的改写与一处 smoke-test 断言的替换（文件清单见 Plan 的 Step）。
- 结论回写到 `TF-20260919-76e7fb` 与 `TF-20260919-2877ca`（后者是「规则放哪才不会被跳过」，本改动即其答案）。

## Out of Scope

- 不给 `hooks/task` 增加发布子命令——用户明确选择纯文档规则。
- 不改任何 hook 的行为；本改动只动文档与断言。
- 不重写 `achieved/` 里的历史发布任务文档（用户已明确：压缩历史）。
- `TF-20260918-985164`（v1.0.7 发布任务）的处置另议，不在本任务内。

## Risks / Deferred Items

- 风险：同一规则出现在六个文件里，措辞容易漂移。缓解 = `hooks/smoke-test` 对五个文件各留一条断言，改坏即失败。
- 遗留：`skills/taskflow/SKILL.md` 的 frontmatter description 仍列着 `release preparation`，与新的适用性门禁不一致；属于发布通道的一部分，本任务内一并修。

## Open Questions

- 无。四个方向性选择均已由用户当场确认。

## Version History

- v1 — planning.
