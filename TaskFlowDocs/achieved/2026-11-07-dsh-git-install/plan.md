# Plan — dsh 走 Git 安装路径
> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `README.md:278-311`、`README.zh-CN.md:245-274` — dsh 安装段（主改点）。
- `hooks/README.md:97` — 快速安装块里的 dsh 行。
- `skills/taskflow/references/runtime.md:26-29` — 各宿主安装命令的汇总段。
- `dsh/index.js:7-13` — 运行时从包根解析 `../skills/` 与 `../hooks/hooks-dsh.json`，决定 `files` 白名单必须包含什么。
- `dsh/cordis.patch.yml` — 自激活层，声明 `dsh.bundle.patch` 的语义。
- `RELEASE.md` 第 3–4 步 — tag 与 commit pin 的产生位置，sha 从这里取。

## Related Tasks

- 无。

## Skills / Tools Used

- [PRD] Unaided — 依据为官方文档查证结论（Todo 已记录）+ 本仓库实测体积；considered: requirements elicitation
- [Plan] Unaided — 单步文档 + 一处清单修改；considered: work breakdown
- [Test] Unaided — 复用既有 smoke 断言模式；considered: testing strategy

## Preconditions

- 本 worktree 在 `feature/dsh-git-install` 分支上。
- 环境无 dsh CLI，真实安装无法本机验证（会在 Plan 的验证节与 PR 中如实记录）。

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-11-07 20:28 +0800
- Approved version: v1
- Approved scope: PRD / Plan

## Steps

### Step 1 — files 白名单

- Goal: 给 `package.json` 加 `files`，让打包只含运行时需要的三处入口。
- Dependencies: 无
- Files:
  - `package.json`
- Implementation checklist:
  - [x] 加 `files` 数组：`dsh/`、`hooks/`、`skills/`、`README.md`、`LICENSE`。
  - [x] 确认 `main`（`dsh/index.js`）与 `dsh.bundle.patch`（`./dsh/cordis.patch.yml`）都落在白名单内。
- Acceptance: 白名单覆盖 `dsh/index.js` 引用的两个同级目录。
- Verification: 逐条比对 `dsh/index.js:7-13` 的路径来源。
- Rollback: `git checkout -- package.json`
- Status: done

### Step 2 — 三个文档站点改为 Git 主路径

- Goal: 把首选命令改成 `github:hkwuks/TaskFlow#<sha>`，说明 sha 来源与升级方式。
- Dependencies: 无
- Files:
  - `README.md`
  - `README.zh-CN.md`
  - `hooks/README.md`
  - `skills/taskflow/references/runtime.md`
- Implementation checklist:
  - [x] 四处的 dsh 段改主路径为 Git + sha，本地目录降为次要选项。
  - [x] 说明 sha 从 release tag 取（`git rev-parse vX.Y.Z^{commit}`）。
  - [x] 保留 `dsh plugin --profile <name> update` 作为升级方式。
- Acceptance: PRD 的全部验收标准，中英一致。
- Verification: 读回四处核对；`bash hooks/smoke-test`。
- Rollback: `git checkout -- README.md README.zh-CN.md hooks/README.md skills/taskflow/references/runtime.md`
- Status: done

### Step 3 — smoke 断言

- Goal: pin 住 `files` 白名单与三个文档的主路径，防止后续漂移。
- Dependencies: Steps 1, 2
- Files:
  - `hooks/smoke-test`
- Implementation checklist:
  - [x] 断言 `package.json` 的 `files` 含 `dsh`、`hooks`、`skills`，且不含 `TaskFlowDocs`、`evals`、`tools`（落在 `release-check`，见验证节）。
  - [x] 断言 `hooks/README.md` 与 `runtime.md` 含 `github:hkwuks/TaskFlow#` 的 dsh 命令。
- Acceptance: 变异验证能捕获回退。
- Verification: 删除任一条目后断言变红。
- Rollback: `git checkout -- hooks/smoke-test`
- Status: done

## Checkpoints

- Steps 1–2 后跑一次 smoke 再写断言。

## Verification / Review

**改了什么**

| 文件 | 改动 |
| --- | --- |
| `package.json` | 新增 `files` 白名单：`dsh/`、`hooks/`、`skills/`、`README.md`、`LICENSE` |
| `README.md` / `README.zh-CN.md` | dsh 段改为以 `github:hkwuks/TaskFlow#<sha>` 为主路径；说明 sha 从 release tag 取；本地检出降为开发用次要选项；说明两条路径都不执行构建 |
| `hooks/README.md` | 快速安装块里的 dsh 行改为 Git + sha |
| `skills/taskflow/references/runtime.md` | 宿主安装命令汇总段的 dsh 部分 |
| `hooks/release-check` | 新增 `files` 白名单检查 |
| `hooks/smoke-test` | 新增 dsh 安装断言；四个 `package.json` 夹具补上 `files` |

**两处判断，都不是原计划写的**

1. **`files` 的断言落在 `release-check` 而不是 `hooks/smoke-test`。** 我先写在 smoke 里，跑出 `FAIL smoke for package.json: expected true, got 'false'` —— `tools/workflow-affected` 把 `package.json` 归入 `release` 类而非 `smoke` 类。一条断言若只在「改动不涉及该文件」时运行，就是从不运行的检查。改到 `release-check` 后归属正确，那里本来就读这个文件。

2. **`hooks/README.md` 与 `runtime.md` 留在 smoke。** 两者都在 `hooks/*` / `skills/*` 路径下，确实触发 smoke。两个根 README 不断言——它们归 `release` 类，同理。

**测试夹具**

新检查让四个既有 `package.json` 夹具变得不合规。补的是夹具而非放宽检查：那些夹具声称「一致的版本应当被接受」，而一个缺 `files` 的 manifest 现在不属于一致发布。补的是契约，不是为了让检查通过。

**验证**

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| 合规 manifest | 临时仓库，`files` 齐全 | `STATUS: pass` |
| 缺 `skills/` | 同上，`files: ["dsh/","hooks/"]` | `files whitelist does not keep skills/`，`needs-user-input` |
| 多 `TaskFlowDocs/` | 同上，`files` 含 `TaskFlowDocs/` | `files whitelist ships TaskFlowDocs/`，`needs-user-input` |
| `bash hooks/release-check .` | 本仓库 | `STATUS: pass` |
| `bash hooks/smoke-test` | 全量 | `ALL SMOKE PASSED` |
| `git diff --check` | | 通过 |

三次变异各自命中不同的消息，说明三个方向（保留、拒绝多出、拒绝遗漏）都在起作用。

**未验证的**

真实 dsh 安装没有本机执行——环境无 dsh CLI。文档改动基于官方文档（见 PRD 的 External Facts）与仓库内 `dsh/index.js` 的路径解析，属「文档化但未实测」，PR 里如实标注。

## Change Log

- v1 — 初始计划。
- v1 — 同日后记：`files` 断言从 smoke 移到 `release-check`，因为分类器不把 `package.json` 发给 smoke 任务；四个夹具补上 `files`。

## Follow-ups

- 真实 dsh 安装未实测。环境有 dsh CLI 时补一次端到端验证。

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-11-04 查证结论（官方文档 + 本仓库实测）**。
  **先纠正一个前提**：dsh **没有**「官方发布通道」。官方文档 `deepseek-harness.github.io/.../develop/basic/publish` 原话是 *"Publishing to a registry is not required — users can install straight from a git host"*。`dsh plugin --profile <name> <args>` **转发给 pnpm**，所以它认的是 pnpm 能解析的任何来源：npm registry、`github:owner/repo#<sha>`、本地目录、`pnpm pack` 出来的 tarball。没有审核、没有入驻、没有「上架」这个动作。
  社区目录 `dsh.pub` 是第三方（非 DeepSeek 官方），流程是开提交页 → 生成 `submissions/*.json` → 提 PR → 自动检查通过即合并，并明说 *"Listing is not a human review, security audit, or official DeepSeek endorsement"*。
  **用户 2026-11-04 裁定：走 Git 路线。**
  **为什么 Git 路线对 TaskFlow 特别便宜**：`dsh/index.js` 是纯 ESM，没有任何构建步骤，所以官方文档里那个「git 安装的 build-script catch」（需要 `prepare` 脚本 + 用户手动 allowlist `allowBuilds`）**完全不适用**。用户可以一条命令装，不需要授权执行任何代码：
  ```
  dsh plugin --profile web add github:hkwuks/TaskFlow#<40位sha>
  ```
  **要做的事**：
  1. **`package.json` 加 `files` 白名单**（唯一的硬缺口）。`npm pack --dry-run` 实测：当前会打包 **417 个文件、3.8 MB**，含 `.github/workflows/`、`CHANGELOG.md`(169KB)、`CONTRIBUTING.md`、`evals/`、`tools/`、`TaskFlowDocs/`。dsh 只需要 `dsh/`、`hooks/`、`skills/`。虽然 Git 安装不走 npm 的 files 字段（pnpm 从 git 拉的是整个仓库），但 tarball 路径和将来上 npm 都需要它，且它是 `npm pack` 体积的唯一控制点。
  2. **README 的 dsh 段改成以 Git 路径为主**。现状把 `dsh plugin --profile web add dsh-taskflow` 写在第一位，而该包 `npm view dsh-taskflow` 返回 **404**——名字空着，没发布过。文档描述了一个装不上的命令。
  3. **记录 commit pin**。官方文档要求 git 安装钉 40 位 sha（`github:you/plugin#<sha>`），"so a later push cannot silently change what runs"。TaskFlow 每次发版都有 tag，`git rev-parse vX.Y.Z^{commit}` 就是该钉的值——这与 `RELEASE.md` 第 4 步已经在做的 marketplace pin 是同一个值，可以复用而不是新增一套。
  **不做的**：不发 npm、不进 dsh.pub 目录。理由是 Git 路径零成本、可撤销，且 TaskFlow 没有构建产物需要分发。等确有用户要求再上 npm。
