<!--
  默认代码风格 — 源自 TaskFlow 自己的 CODE_STYLE.md 的通用部分。
  只保留了与语言无关、与具体项目无关的条目；TaskFlow 自己的产物约定没有带过来。
  这是你仓库里的文件：想怎么改都可以，TaskFlow 不会覆盖它。
-->

# Code style

## Markdown

- Use ATX headings (`##`), not underlined ones.
- Keep paragraphs short and one idea per bullet.
- Use repository-relative paths in documentation, so a reader can copy them into a command.
- If you keep a README in more than one language, keep them behaviourally aligned rather than word-for-word.

## Shell

- Use `#!/usr/bin/env bash` and `set -euo pipefail`.
- Quote paths and variable expansions. An unquoted path with a space is two arguments.
- Use exit `0` for success, `2` for "needs a human decision", and `3` for "blocked". A caller can then tell "it ran and passed" from "it could not run".
- Keep a check read-only unless the script explicitly implements a named state change.
- Never print credentials, tokens, or private URLs.

## Simplicity and compatibility

- Reuse what the repository already has before adding a helper.
- Prefer the smallest change that satisfies the requirement.
- Do not add compatibility code or a dependency without a decision that says why.
- Preserve unrelated files and existing history.
