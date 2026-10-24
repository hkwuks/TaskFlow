# 让 hooks 文档与 hooks 目录保持同步

> Task version: v1
> Status: completed

## Goal

`hooks/smoke-test` 为 `SKILL.md` 和 `references/artifacts.md` 钉了一大串条款，却没有任何断言看管真正描述 `hooks/` 本身的那两份文档——`skills/taskflow/references/runtime.md` 和 `hooks/README.md`。两者都是目录的散文清单，所以加一个 hook、改名、删一个，它们都会静默过期。本次把这种漂移变成失败断言，并补上本条目吸收进来的那半：版本跃迁的廉价断言。

## Background / Confirmed Facts

- `hooks/` 下有 22 个无后缀脚本、5 个 hook JSON 文件，外加 `README.md`。`hooks/README.md` 的树形代码块就是清单，`runtime.md` 的表格点名各个命令。
- **今天实测到的漂移（2026-10-24）：** README 树里没有 `repository-check`；`runtime.md` 既没提 `release-version` 也没提 `repository-check`。而 `skills/taskflow/SKILL.md:331` 点名了 `repository-check`，`RELEASE.md` 两个都点名了——知识是存在的，只是不在读者被路由到的那份文档里。
- 反方向是干净的：`SKILL.md` 与 `references/*.md` 里提到的每个 `hooks/<名字>` 都能对应到真实文件，前提是把 `run-hook.cmd`、`smoke-test-windows.ps1` 的 `.md`/`.ps1` 后缀剥掉。
- 被吸收的条目 `TF-20261008-4d37b2` 提了两件事。第一件是「在 `SKILL.md` 的更新点旁边点名 `hooks/version`」——这条**已经是事实**：`SKILL.md:112`、`:255`、`:282`、`:286` 与 `runtime.md:236` 都写了命令名或跃迁规则。第二件是可测且今天成立：83 个 achieved 任务，根版本之下的每一版都有对应的 `old/vN`，缺口为 0。
- `release-version` 与 `repository-check` 不是 hook 接线，也不是生命周期命令，它们是发布流程的命令，权威描述在 `RELEASE.md`。这正是当初没写进 `runtime.md` 的原因——但 `runtime.md` 同时也是 `SKILL.md` 路由「`hooks/` 布局」去的那份文件，所以顺着这条路走的读者根本不知道它们存在。

## Requirements

1. `hooks/README.md` 的树里包含 `hooks/` 的每一个文件，且不含不存在的文件。
2. `runtime.md` 点名每个具有生命周期或宿主角色的 hook；对发布流程命令，说明它们记录在别处，而不是留成空白。
3. `hooks/smoke-test` 在这两份文档与目录发生漂移时失败，**双向**：文件没被写进文档、文档点名了不存在的文件。
4. `hooks/smoke-test` 在 achieved 任务的根 Task 版本与 `old/vN/` 之间出现缺口时失败。
5. 断言要廉价：不联网、不造夹具仓库、不遍历每个 achieved 文档的正文。

## Acceptance Criteria

- 修复后 `bash hooks/smoke-test` 通过，新增的小节各自打印 `ok`。
- 从 README 树里删掉一行、或新增一个 hook 文件却不写进文档，都会让套件失败，且失败消息点名那个文件。（评审时用变异验证，不作为口头声明留下。）
- 版本缺口断言：在 `plan.md` 写 `v3` 却只有 `old/v1` 的夹具任务上失败；在 `v3` + `old/v1` + `old/v2` 上通过。
- 套件跑完后，两份文档与 `ls hooks/` 一致：没有 hook 未被提及，没有提及无法落地。

## In Scope

- `hooks/README.md`——树里补 `repository-check`；写清楚树覆盖什么、不覆盖什么。
- `skills/taskflow/references/runtime.md`——加一行或一小段，覆盖 `release-version`、`repository-check`，并指向 `RELEASE.md`。
- `hooks/smoke-test`——一节做文档与目录的双向核对，一节做版本与 `old/` 的缺口检查。
- `CHANGELOG.md`——一条 `Unreleased` 记录。

## Out of Scope

- 重写 `RELEASE.md`。它已经把两个发布命令写对了。
- 从 `hooks/` 生成这两份文档。生成器需要被维护，而本条目关心的是漂移，断言已经覆盖。
- 断言两份文档的**散文**。只查名字；描述过期仍然属于文档评审，不是测试。
- `hooks/smoke-test-windows.ps1`。

## Risks / Deferred Items

- **名字检查是下限，不是条目的全部野心。** `TF-20261008-a4454d` 的标题写的是「保持同步」，而表格里出现一个文件名，描述仍可能写错。断言抓住常见情况（新增/改名/删除 hook），README 的「一个文件一行」形态让描述在评审时可见。不做语义检查。
- **README 树是按形状解析的。** 断言读取 ` ```text ` 代码块并剥掉框线前缀，所以重新排版树会让解析失败而不是让事实失败。失败消息会说明是哪份文档解析不了，修起来一目了然。
- **版本缺口检查会读每个 achieved `plan.md` 的第一行版本。** 今天 83 个文件，每个一次 `sed`——实测远低于一秒。若 achieved 任务涨到上千，改成只查本次 diff 触及的任务；在那之前不做。

## Open Questions

没有阻塞项。
