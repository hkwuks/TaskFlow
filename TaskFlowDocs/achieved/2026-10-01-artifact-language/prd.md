# Reconcile the artifact-language rule with capability-written documents: a phase
> Task version: v1
> Status: completed

## Goal

让「任务文档的正文用用户工作语言」这条约束，在正文由阶段能力起草时依然成立。

要求本身一直是对的，也没有过期——`87c30e5`（2026-09-15）引入时就是一句无作用域限定的白话要求。失效发生在两处后来加入的文本之间：`38adbbb`（2026-09-29）为 hook 解析边界收窄出显式名单时，顺手立了一条**骨架豁免**原则，而它的主语只写了 `hooks/task promote`；能力门 `d72c2b2`（2026-09-28）就位之后，「能力模板」成为同一意义上的骨架，于是被这条豁免一并放行。本次把那条原则的适用范围写成**来源无关**，并把语言随内容折入这件事说在折入指令所在处。

## Background / Confirmed Facts

### 要求本身：一句白话，无作用域限定

`87c30e5`（2026-09-15，「fix: require an approval before progress and completion」）随审批校验一同引入规则，原文是：

> Write `prd.md`, `spec.md`, `plan.md`, and `reference/` prose in the user's working language. Hooks parse task documents, so the lines they match stay English verbatim: …

它约束的是**目的文档**，与谁起草无关；这一层从来没有被写成「由谁写」。同一次提交引入了 `hooks/smoke-test` 的钉字符串段与 `CODE_STYLE.md` 的一句。commit message 给出的理由是 hooks 按文本解析：一个被译过的 `## Approval` 标题或 `- Status:` 行会让全部生命周期命令找不到它。

### 规则的现存陈述位置（三处）

- `skills/taskflow/SKILL.md:46` —— 一句话版本。
- `skills/taskflow/references/artifacts.md:15-31` —— 正式版本：`:17` 是规则本体，`:19-25` 是 hook 匹配的英文边界名单，`:27` 是骨架让步，`:29` 是 hook 写的字段值不翻译，`:31` 是不追溯既有文档。
- `CODE_STYLE.md:9` —— 「Write task-document prose in the user's working language; keep the lines hooks parse in English (see the Skill's artifact-language rule).」已是起草者中性的一句，指向 Skill 的规则，本次不动。

### 失效的文本级出口：以 promote 为主语的骨架豁免

`38adbbb`（2026-09-29，「docs: narrow the artifact-language rule to an explicit name list」，属 `2026-09-15-hook-integrity` v2）把原措辞里的「`## ` section headings」全英文换成显式名单，并新增了这句：

> `hooks/task promote` writes its own English scaffold into a new document, so headings arrive in English whatever the language — **that scaffold is not prose this rule governs**, and a scaffolded heading follows the rule only once you edit it.

加粗那半句立的是通则——**骨架本身不受本规则管**——而主语只写了 `hooks/task promote`。能力模板在同一个意义上就是骨架：它有英文标题，也有英文占位正文。照着占位写，语言就被锚定；而这句话刚好给了「骨架部分不归本规则管」的书面依据。这不是把规则推翻，是规则旁边多了一条被读宽了的豁免。

`d72c2b2`（2026-09-28，「feat: gate the first body write of prd/spec/plan on a real invocation」）让「调用能力」成为每个阶段常规的一步，于是这条豁免从「罕见」变成「每次都会经过」。

### 折入路径对语言沉默（四处）

- `SKILL.md:136` —— 「Review successful outputs before incorporating them; raw outputs are not authoritative.」
- `SKILL.md:152` —— 「Fold external requirements/design/planning output by kind: requirements → `prd.md`, design → `spec.md`, breakdown → `plan.md` Steps」。
- `artifacts.md:146` —— 「If a tool emits a default root-level artifact, move or rewrite its content into the current task destination before accepting it as authoritative.」
- `artifacts.md:150` —— 「Tool output is candidate material until the core-document owner reviews and merges it.」

四处都在讲「怎么折」，没有一处讲「折进来之后语言归谁」。折入是能力产物的必经一步，语言在这一步没有落脚点。

### 观测证据

| 任务 | 是否走了阶段能力 | `prd.md` 正文语言 |
| --- | --- | --- |
| `achieved/2026-09-27-capability-pre-write-gate/` | 否 | 中文 |
| `achieved/2026-09-30-release-ci-test-policy/` | 是（`agent-skills:spec-driven-development` + `agent-skills:planning-and-task-breakdown`） | 英文 |

两篇都由同一个人、同一个仓库写出，差别只在「正文由谁起草」。

### 既有检查：钉字符串，不是正文语言校验

`hooks/smoke-test:1248-1272` 钉住规则文本本身：`^## Artifact language$`、`the lines they match stay English verbatim`、`in the user.s working language`（SKILL）、`user.s working language`（`CODE_STYLE.md`）、`are not rewritten for language`，并逐个钉住显式名单里的名字，同时**反向禁止**「\`## \` headings 全英文」这类已被替换的措辞。`:1274-1309` 是另一节，用真 fixture 验边界两侧：译一个名单外的标题不影响命令，译一个名单内的会被拒。

它验的是**规则文本还在不在**，不是**正文语言对不对**——后者机械上判定不了。正因为如此，规则一旦被旁边一句豁免读宽，这套检查不会有任何反应。

## Requirements

- **R1 —— 规则绑定目的文档，不绑定起草者。** `prd.md`、`spec.md`、`plan.md`、`reference/` 的正文一律用用户工作语言，与正文由 Agent 直接写、还是由某个能力起草后折入无关。
- **R2 —— 折入动作显式携带这条规则。** 能力输出按 kind 折入时，保留的是**结构**，重渲的是**语言**；这句话要落在折入指令本身所在的位置，而不是另起一段另说一遍。
- **R3 —— 骨架豁免改为来源无关。** 未被编辑的骨架标题可以留在它到达时的语言（`hooks/task promote` 的 scaffold 或能力模板皆然）；一旦被编辑，它服从 R1。骨架的来源不改变规则，且豁免的措辞要明确它**只管骨架自身的标题**，不管用它填出来的正文。
- **R4 —— 不新增机制。** 不新增 hook、不新增命令；不给正文语言做机械校验（做不到，只会误报）。检查只在既有 `hooks/smoke-test` 钉字符串段内扩展，不建第二套。
- **R5 —— 不追溯。** 既有文档（尤其 `TaskFlowDocs/achieved/`）不因语言重写。
- **R6 —— 边界名单不变。** hook 按文本匹配的那批英文行维持原样，本次不动其成员与含义。
- **R7 —— 新条款被钉住。** R2、R3 的新措辞要进入 `hooks/smoke-test` 既有那一节的钉字符串，使下一次收窄不能静默把它删掉。

## Acceptance Criteria

- **A1 —— SKILL.md 单读可判。** 只读 `SKILL.md:46` 那一段、手里拿着英文能力模板的 Agent，能据此判定正文该用什么语言。
- **A2 —— artifacts.md 单读可判。** 只读 `references/artifacts.md` § Artifact language 的 Agent，同样能判定；且能答出「骨架标题与其正文语言不同」时各自的归属。
- **A3 —— 折入点自带语言。** 折入指令所在处（`artifacts.md:146`）明确语言随内容一同折入，读者无需回到 § Artifact language 才知道。
- **A4 —— 豁免只有一份定义且来源无关。** 「未编辑的骨架标题可留原语言」由一处定义、对两种来源（promote scaffold、能力模板）共用一个表述；该表述明确它不覆盖骨架下方由你写的正文。
- **A5 —— 下游复核（观察性验收）。** 下一个调用阶段能力的任务，在归档前复核其 `prd.md`/`spec.md`/`plan.md` 的正文语言，结论记入该任务 `plan.md`；结论为「正文非用户工作语言」即视为本次修复未生效，需重开本任务。
- **A6 —— 改动面可核。** `git diff --stat` 只包含 `skills/taskflow/SKILL.md`、`skills/taskflow/references/artifacts.md`、`hooks/smoke-test`；`CODE_STYLE.md`、`evals/**`、`.github/**` 零改动。
- **A7 —— 边界名单零变化。** `artifacts.md` 第 19-25 行的英文行名单逐条不变（成员与语义都不变），且 `hooks/smoke-test:1263` 钉的那批名字继续匹配。
- **A8 —— 钉字符串真的钉得住。** 临时删掉新条款后，`hooks/smoke-test` 那一节必须**失败**并指出缺失项；恢复后通过。这条是本任务唯一可执行的检查，用来证明 A7 之外的钉不是空写。
- **A9 —— CI 为准。** 改动含 `hooks/smoke-test`，按 `CONTRIBUTING.md` § Checks 交给 CI `Hooks` 工作流的 `smoke` 任务（ubuntu / macos / windows）判定，不在本地重跑整个套件。

## In Scope

- `skills/taskflow/references/artifacts.md` —— § Artifact language：规则本体的措辞、骨架豁免改为来源无关、折入指令那一句（`:146`）的语言从句。
- `skills/taskflow/SKILL.md` —— 第 46 行那一段的措辞。
- `hooks/smoke-test` —— 既有「artifact language rule」那一节内新增钉字符串（R7）。

## Out of Scope

- 不新增 hook、命令或第二套检查机制（R4）；不给正文语言做机械校验。
- 不重写既有文档的语言，包含 `TaskFlowDocs/achieved/` 全部内容（R5）。
- 不改 `CODE_STYLE.md:9` —— 它已是起草者中性的一句，且被 `hooks/smoke-test:1255` 钉住。
- 不改 hook 匹配的英文行名单（R6），不改 `SKILL.md:152` 的 kind 路由。
- 不改第三方能力自身的 SKILL —— 它们在 Agent 配置目录下，且全局规则要求只改项目内的 `skills`。
- 不修本次执行中撞到的相邻缺陷（证据钩子与门的锚点不一致）：它已写入 PRD 的遗留项，另立待办。

## Risks / Deferred Items

- **风险：豁免句改宽反而更松。** 缓解：R3 明确豁免只管骨架自身标题，A4 要求同一句里点明它不覆盖正文。
- **风险：两处（`SKILL.md` 与 `artifacts.md`）措辞漂移。** 缓解：`SKILL.md` 维持「一句规则 + 指向 `artifacts.md`」的既有分工，`artifacts.md` 是唯一定义处；新增钉字符串只钉 `artifacts.md`。
- **风险：钉字符串是存在性检查，不是语义检查。** 它只能挡住「被删掉」，挡不住「被改写成语义相反的句子」。这是既有机制的固有上限，本次不试图抬高它；A5 的下游复核承担语义层面的发现责任。
- **遗留：能力若自带语言政策。** 若将来某个能力的 SKILL 明写「以英文回答」，R3 的豁免不足以覆盖这种冲突——记为待观察，出现时按用户变更处理。
- **遗留：正文语言仍无机械校验。** R4 的直接后果，由 A5 承担发现责任。
- **相邻缺陷（本任务不修）**：`capability-evidence` 用事件 `cwd` 定位证据库与活动任务（`hooks/capability-evidence:58-79`），`capability-gate` 用被写文件路径定位（`hooks/capability-gate:119`）。会话 cwd 不在任务工作树时，能力调用的证据不落盘，门随后拒绝写入——本次是靠把会话 cwd 切进工作树才走通正常流程。

## Open Questions

无。决策（只改文档措辞 + 钉字符串 / 骨架豁免改为来源无关 / 阅读式验收加一次下游复核 / `CODE_STYLE.md` 不动）已由用户在 2026-10-01 裁定。

## Version History

- v1 — planning. 修订一次：诊断由「规则写的是谁来写」（错，规则原文本就中立）改为按 commit 历史定位到 `38adbbb` 的骨架豁免；改动面由 2 文件改为 3 文件（加入 `hooks/smoke-test` 钉字符串）；验收由纯阅读式改为「钉字符串可失败 + CI 三平台」加一次下游复核。
