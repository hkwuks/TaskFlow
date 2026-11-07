# dsh 走 Git 安装路径
> Task version: v1
> Status: in_progress

## Goal

让 dsh 的安装文档描述一条**能装上的命令**：以 `dsh plugin --profile <name> add github:hkwuks/TaskFlow#<sha>` 为主路径，加 `package.json` 的 `files` 白名单控制打包体积，并说明 sha 从哪里来。

## Background / Confirmed Facts

**当前文档描述的命令装不上**：`README.md:286`、`README.zh-CN.md:251`、`hooks/README.md:97` 都把 `dsh plugin --profile web add dsh-taskflow` 写在第一位。该包从未发布到 npm —— Todo 记录 `npm view dsh-taskflow` 返回 404。读者按文档第一条命令执行会失败。

**dsh 没有「官方发布通道」**：官方文档原话 *"Publishing to a registry is not required — users can install straight from a git host"*。`dsh plugin --profile <name> <args>` 转发给 pnpm，所以它认 pnpm 能解析的任何来源：npm registry、`github:owner/repo#<sha>`、本地目录、tarball。

**Git 路径对 TaskFlow 特别便宜**：`dsh/index.js` 是纯 ESM，无构建步骤，所以官方文档里 git 安装的「build-script catch」（需 `prepare` 脚本 + 用户手动 allowlist `allowBuilds`）完全不适用。一条命令装好，不需要用户授权执行任何代码。

**`files` 白名单是硬缺口（本次实测）**：仓库总计 5.3 MB，其中 `TaskFlowDocs/` 3.3 MB、`CHANGELOG.md` 176 KB。dsh 实际需要的只有三处：

```
dsh/    4.0K
hooks/  884K
skills/ 164K
```

Git 安装走 pnpm 拉整个仓库，不经 npm 的 `files` 字段；但 tarball 路径、以及将来真上 npm 时，`files` 是唯一控制点。加上它不改变 Git 安装行为，纯粹是让「打包」这件事有正确答案。

**sha 从哪来**：`RELEASE.md` 第 3–4 步已经产生它 —— tag 与 marketplace pin 用的是同一个 commit。`git rev-parse vX.Y.Z^{commit}` 就是该钉的值，不需要新增一套。

## Requirements

1. `package.json` 加 `files` 白名单：`dsh/`、`hooks/`、`skills/`，以及 dsh 运行所需的根文件。
2. 三个文档站点的 dsh 段改为以 Git 路径为主，本地目录为次。
3. 说明 sha 必须钉 40 位，以及它从哪里取（release tag），并说明 `dsh plugin --profile web update` 仍是升级方式。
4. 不描述任何需要用户执行构建脚本的路径。

## Acceptance Criteria

- `package.json` 含 `files` 数组，内容覆盖 `dsh/`、`hooks/`、`skills/`，且不含 `TaskFlowDocs/`、`evals/`、`tools/`。
- `README.md`、`README.zh-CN.md`、`hooks/README.md` 的首选 dsh 命令是 `github:hkwuks/TaskFlow#<sha>` 形式。
- 三处都说明了 sha 的来源（release tag）与升级方式。
- 中英文行为一致。
- `bash hooks/smoke-test` 通过；`git diff --check` 通过。

## External Facts

- Depends on external facts: yes
- Source: https://deepseek-harness.github.io/dsh/develop/basic/publish
- What it settled: dsh 发布不要求 registry，可从 git host 直接安装；`dsh plugin` 转发 pnpm；git 安装的 build-script catch 只适用于有 `prepare` 脚本的包。

## In Scope

- `package.json` — 新增 `files`。
- `README.md`、`README.zh-CN.md` — dsh 安装段。
- `hooks/README.md` — 快速安装块里的 dsh 行。
- `skills/taskflow/references/runtime.md` — 安装命令那一段的 dsh 部分。

## Out of Scope

- 不发布到 npm，不提交 dsh.pub 社区目录：Git 路径零成本、可撤销，等确有需求再说。
- 不改 `dsh/index.js` 或 `dsh/cordis.patch.yml`：安装路径变化不涉及运行时。
- 不加 `prepare`/`postinstall` 脚本：那正是官方文档警告的、会逼用户 allowlist 执行代码的东西，对纯 ESM 包完全不需要。

## Risks / Deferred Items

- 风险：`files` 白名单漏掉 dsh 运行必需的文件，导致 npm 安装路径坏掉。缓解：白名单按 `package.json` 的 `main`（`dsh/index.js`）与 `dsh.bundle.patch`（`./dsh/cordis.patch.yml`）两个入口反推，两者都在 `dsh/` 内；`hooks/` 与 `skills/` 是运行时读取的目录。补一条 smoke 断言，pin 住这三个目录都在 `files` 里。
- 遗留：真实 dsh 安装未在本机验证（环境无 dsh CLI）。文档改动基于官方文档与仓库事实，属于「文档化但未实测」，需在 Known limitations 里说明。

## Open Questions

无。
