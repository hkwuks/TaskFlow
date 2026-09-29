# Archived Version v1 — Plan — Hook integrity: unpolluted archives, unbypassable gates, user-language documents
> Task: 2026-09-15-hook-integrity
> Version: v1
> Status: superseded
> Archived: 2026-09-29 18:47 +0800
> Superseded by: v2
> Archive mode: file

## Change Summary

R4（文档语言规则）的英文边界被收窄：v1 把"章节标题"整体划入必须英文的一侧；v2 改为 hook **按精确名字匹配**的标题清单（`## Approval`、`## Skills / Tools Used`、`## Verification / Review`、`## Change Log`、`## Items`、`## Removed`、`## Active / Resumable`、`## Closed / Reference Only`、`### Step N — <name>`、`### SN — <Agent>`），其余章节标题归入正文散文、跟随用户语言。新增 R5（规则须说明 `promote` 写出的英文骨架不受此规则支配）、R6（smoke 钉住名单并新增"翻译非匹配标题后 hook 仍工作"的行为断言）、R7（`CHANGELOG.md` 补记录，补上 v1 落地时缺失的变更记录）。

Goal、R1–R3（`hooks/version` 拒绝污染归档、`complete` / `progress` 的批准门禁）与相应验收标准未变。v1 的归档污染 / 门禁缺口两项修复在 v2 中保持原样。

不产生可观察的行为变化：`hooks/task promote` 仍然把整个大纲写成英文，用户看到的标题依旧为英文；v2 的收益是规则准确且可检索。标题本地化被明确排除，记为 follow-up（语言声明放 `personal.md`、由 hook 执行）。

## Archived Materials
- prd.md

## Restore
Read the archived v1 core docs from a new temporary restore root. Do not overwrite the current task root.
