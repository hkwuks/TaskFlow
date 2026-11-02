<!--
  默认仓库规则 — 源自 TaskFlow 自己的 CONTRIBUTING.md 的通用部分。
  不含 TaskFlow 自身的工作流（任务目录、worktree、归档到 achieved/ 等）。
  这是你仓库里的文件：想怎么改都可以，TaskFlow 不会覆盖它。
-->

# Contributing

## Before you start

- Work from a short-lived branch based on the intended base branch.
- For fork work, verify which repository receives the branch and which one receives the pull request; remote names alone are not evidence.
- Read `README.md` and whatever project rules your repository already has.

## Branches and commits

Use short-lived branches named `feature/<description>`, `fix/<description>`, `docs/<description>`, or `chore/<description>`.

Keep commits focused and use `<type>: <imperative description>` — for example, `fix: handle an empty search result`. Separate unrelated refactors and formatting changes into their own commits, so a later reader can tell a behaviour change from a tidy-up.

## Checks

Run the checks your project actually has before pushing, and let CI be the authority for anything it covers. Reproducing a full CI matrix locally spends the same time twice and still judges one host where CI judges several.

Two kinds of check stay local because CI cannot run them: those that only work on a particular machine, and those cheap enough that failing early is worth more than failing in CI.

## Pull requests

Describe the goal, the scope, the verification you ran and its results, and any known limitations. Do not include secrets.

**Open it as a draft, and mark it ready only once the change is complete.** A draft pull request still runs CI, so the matrix is not deferred by opening one; what it defers is the merge, and "do not merge yet" is then a state the platform enforces and a reader sees, rather than a sentence in the body.

```bash
gh pr create --draft --base <base> --title '<title>' --body-file <file>
gh pr ready <number>
```

If your repository has a pull request template, read it and fill in every field it asks for.
