# Plan — Cut the mechanical overhead out of a release without adding any authority to it

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `RELEASE.md` — the release procedure this bounds.
- `hooks/release-check` — the read-only check extended here.
- `CONTRIBUTING.md` `## Checks` — where `hooks/smoke-test` is required.
- Task-level evidence for the corrected scope: `prd.md` `## Background / Confirmed
  Facts`, taken from `620c6a7`, `c3c536d`, `c1147ab`, and a live mutation run of
  `release-check`.

## Related Tasks

- `TF-20260919-c41f8a` — this task's Todo item.
- `TF-20260919-76e7fb` — delivered: a release no longer runs the TaskFlow flow.
  That change is why the v1.0.7 pin window's extra `plan.md` is historical.
- `TF-20260919-b7821b` — deferred, out of scope here.

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell/awk text
  processing, POSIX-portability references, and the repository's own hook
  conventions, all read directly.`

## Preconditions

- [x] Applicable repository documents and personal rules inspected;
  precedence/conflicts recorded. — `RELEASE.md`, `CONTRIBUTING.md`,
  `CODE_STYLE.md`, and `TaskFlowDocs/repository-docs/index.md` read.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-21
- Approved version: v1
- Approved scope: R1–R7; the corrected item (2) as a stating rule (R4), and the
  `TaskFlowDocs/` exemption in the pin-window rule (R5).

## Steps

### Step 1 — `hooks/release-version`, the one-call literal writer

- Goal: one command writes all eight mechanical literals in six files, and
  refuses before writing anything when it cannot.
- Dependencies: none.
- Files: `hooks/release-version` (new).
- Implementation checklist:
  - [x] Accept `<x.y.z> [root]`; validate the shape and that it is greater than
        the current `.claude-plugin/plugin.json` version.
  - [x] Require every target file to exist and `CHANGELOG.md` to already carry a
        `## [x.y.z]` section (R3). Refuse otherwise.
  - [x] Stage all rewrites in a temp dir under the same filesystem, then move
        them into place only after every check passed (R2).
  - [x] Write the four manifests, each README's **every** plugin-list sample
        line, and the Codex/CodeBuddy cachebuster date from the hook's `today`.
  - [x] Write nothing else: no tag, no push, no procedure step (R7).
- Acceptance: A and D.
- Verification: `bash hooks/release-check .` on a fixture prints `pass`; each
  refusal case diffed by digest.
- Rollback: delete `hooks/release-version`; no other file depends on it.
- Status: done

### Step 2 — `hooks/release-check`: every README literal, and the pin window

- Goal: close the two measured gaps — a stale second README literal passing, and
  a pin window carrying an unexplained change.
- Dependencies: Step 1 (its acceptance runs through this check).
- Files: `hooks/release-check`.
- Implementation checklist:
  - [x] Replace the `head -1` README reads with a loop over every match, and
        report each one (R6).  - [x] Add the pin-window rule: resolve `ref` to its commit, walk
        `tag..sha` with `git diff --name-only`, and fail with the paths named
        when anything other than the two marketplace catalogs or a
        `TaskFlowDocs/` path appears (R5).
  - [x] Keep every existing exit code and `STATUS:` line — CI and `RELEASE.md`
        read them.
- Acceptance: B and C.
- Verification: mutate each check in turn and confirm the suite fails.
- Rollback: `git checkout -- hooks/release-check`.
- Status: done

### Step 3 — `RELEASE.md` states the ordering, and names the new command

- Goal: the tagged commit carrying the release section becomes a stated rule.
- Dependencies: none.
- Files: `RELEASE.md`.
- Implementation checklist:
  - [x] State that the `CHANGELOG.md` section is written before the tag, and why
        (R4) — the tag is the immutable artifact, so what it points at has to be
        complete.
  - [x] Add `hooks/release-version` to the scope list and to the pre-tag steps.
  - [x] Leave the atomic-push step, the rollback section, and the
        "does not push tags or create GitHub Releases automatically" boundary
        untouched.
- Acceptance: the file reads as one consistent procedure.
- Verification: `git diff --check`; re-read the tag/pin steps for contradiction.
- Rollback: `git checkout -- RELEASE.md`.
- Status: done

### Step 4 — smoke assertions and the mutation pass

- Goal: each new check fails when it is reverted.
- Dependencies: Steps 1–3.
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] Assert A–D against a fixture, in the fixture style the release-check
        section already uses.
  - [x] Mutate one check at a time; record what each mutation made fail.
- Acceptance: E.
- Verification: `bash hooks/smoke-test` — ALL SMOKE PASSED.
- Rollback: `git checkout -- hooks/smoke-test`.
- Status: done

## Checkpoints

- After Step 2: run `bash hooks/release-check .` on the real repository and
  confirm it still prints `STATUS: pass`.

## Verification / Review

Run in this worktree on 2026-09-21, all four green:

- `bash hooks/smoke-test` — ALL SMOKE PASSED
- `bash hooks/release-check .` — `STATUS: pass` on the unmodified repository, and
  it reports all nine literal lines (four manifests, the CHANGELOG section, and
  both samples in each README)
- `bash hooks/repository-check .` — `needs-user-input`, for the expected reason:
  this branch's task directory is still untracked, and the check reports an
  uncommitted task artifact rather than a governance defect. It clears when the
  task documents are committed to this branch.
- `git diff --check` — clean

Mutated once per check, each restored after:

| Mutation | Suite result |
|---|---|
| `readme_versions` restricted to the first match, as the old code did | `FAIL stale second README sample accepted` |
| the pin-window rule's guard forced false | `FAIL a stray file in the pin window was accepted` |
| `release-version`'s "exactly one version key" relaxed to "at least one" | `FAIL a manifest with two version keys was rewritten` |
| `release-version`'s CHANGELOG-section precondition removed | `FAIL release-version ran without a CHANGELOG section` |
| `release-version`'s already-at-target refusal removed | `FAIL a file already at the target version was overwritten silently` |

## Change Log

- 2026-09-21 — item (2) of the Todo entry is corrected to a stating rule; the
  measurement is in `prd.md`. Item (1) was an undercount, not a defect: eight
  literals in six files. Item (3)'s window rule gains a `TaskFlowDocs/` exemption.

## Follow-ups

- `TF-20260919-b7821b` — `hooks/version`'s Approval block shape. Still open.

## Version History

- v1 — planning.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-09-19 用户指定三条一起做，作为本条**（依据是 v1.0.8 的实测产物，不是设想）。
- **2026-09-21 已 promote，三条经实测修正为**：(1) 机械字面量不是 6 处而是 **8 处 / 6 个文件**（4 个 manifest + 两份 README 各两处 `Version:` 示例），`hooks/release-version` 一次写掉；(2) **tag 缺正文不是真的**——实测 v1.0.7 (`c3c536d`) 与 v1.0.8 (`620c6a7`) 的 CHANGELOG 段落**都在被 tag 的 commit 里**，tag 注释是 tag 对象上的第二份正文，不替代第一份；真正缺的只是 `RELEASE.md` 没写下「段落先于 tag」这条顺序规则，改为补规则（R4）；(3) 新增两条已实测的检查——`release-check` 对每份 README **只用 head -1 比第一处**，把 `README.md:261` 改成 1.0.7 仍报 pass；以及 tag→pin 窗口内除 marketplace 两文件与 `TaskFlowDocs/` 外任何改动均应判红。用户已裁定：第 (2) 条只补规则、窗口豁免 `TaskFlowDocs/`。
  **三条内容**：
  (1) **`hooks/release-version <x.y.z>`（只做格值写入）**——当前一次发布要手改 **7 个文件**（`620c6a7` 的 stat）：4 个 manifest 的 `version`、两份 README 的插件列表示例、`CHANGELOG.md` 新段落。**前六处是格值**（4 个 manifest + 2 处 README 示例输出，`README.md:207,261`、`README.zh-CN.md:173,226`），完全可以一条命令写掉；**第七处是散文，留给 Agent**。Codex/CodeBuddy 的 cachebuster 形如 `1.0.8+codex.20260919`，日期用 hook 已有的 `today`。**必须一次调用写完，不要做成 preflight + write 两次**——一次调用就先检查后写，失败不留半成品。
  (2) **把 CHANGELOG 段落搬进 base tree 的 release commit，让 tag 不可变**。现状（`RELEASE.md:86-92` + 实测 `620c6a7`）：**release notes 活在 tag 指向的 commit 之后的第二个 commit 里**，所以 `git tag -a` 只能把正文写进 tag，**tag 本身缺发布正文**；后来补写正文是重写 tag 对象，而 tag 是 claude 的 `sha` pin 引用的东西，重写需要「显式 owner 授权 + 记录理由」（`RELEASE.md:126`，且改的是 `620c6a7`/`2a89e2` 那类 commit）。把 CHANGELOG 段落移进 release commit 之后：tag 指向的 commit 自带发布正文，下一个 tag 可以带正文且先于 pin 创建、此后不再改。`RELEASE.md` 的步骤顺序要同步（正文写入在打标签之前），并记录为什么。
  (3) **让过期的发布记录在 CI 里失败**：给 `hooks/release-check` 加一条——**tag 指向的 commit 之后、被 pin 的 commit 之前**，只允许存在 marketplace 的 `ref`/`sha` 字面量差异；一旦出现别的差异（CHANGELOG 段落、README、manifest 版本、代码），就退出非零。v1.0.8 顺带发现：`README.md:261` 的 `claude plugin list` 示例还停在 1.0.8，而发布前的文档版本是 1.0.9——这条同时就是防这个的。
  **三条的公共红线（不是可选项）**：新增的工具**不得做判断**。`RELEASE.md` 的批准门禁是「用户先批准，写入是转录」；格值写入与记录校验都是转录，所以可以做；**「允许发布」必须永远留在人手里**，任何一条都不得演变成自动发布或自动批准。另：`RELEASE.md:122` 明确「不做自动 tag / 自动 GitHub Release」，三条都不得触碰这条边界。
  **边界已核**：Hook 的 JSON 目前只有 `SessionStart`（`hooks/hooks.json`），三条都不需要新增 hook 事件，也都不需要 `hooks/task` / `hooks/archive` 的现有事务。`hooks/release-check` 已被 `hooks/smoke-test:1172-1231` 覆盖（漂移、坏 pin、cachebuster、缺 manifest），新增的检查要按同法补断言。相关：`TF-20260919-76e7fb`（发布不走 TaskFlow，已交付）、`TF-20260919-b7821b`（`hooks/version` 的 Approval 形状）。
