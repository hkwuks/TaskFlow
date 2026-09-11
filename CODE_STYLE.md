# TaskFlow code style

## Markdown

- Use ATX headings and concise paragraphs.
- Keep one requirement or rule per bullet.
- Use repository-relative paths in documentation.
- Keep English and Chinese README behaviorally aligned.
- Put durable requirements in the Skill or repository document; keep task facts in the task directory.

## Shell

- Use `#!/usr/bin/env bash` and `set -euo pipefail`.
- Quote paths and variable expansions.
- Use exit `0` for pass, `2` for needs-user-input, and `3` for blocked workflow status.
- Keep checks read-only unless a script explicitly implements a named state transition.
- Never print credentials, tokens, or private URLs.

## Task artifacts

- Keep `prd.md`, `spec.md`, and `plan.md` version and state fields consistent.
- Use checklist items for implementation and record commands plus results under verification.
- Do not create duplicate sources of task facts.

## Simplicity and compatibility

- Reuse existing hooks and scripts before adding helpers.
- Prefer the smallest change that satisfies the approved Plan.
- Do not add compatibility code or dependencies without approval.
- Preserve user files, unrelated tasks, and existing history.
