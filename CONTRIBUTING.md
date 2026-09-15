# Contributing to TaskFlow

## Before you start

- Work from a short-lived feature, fix, docs, or chore branch based on the intended base branch.
- For fork work, verify the target repository and base branch; remote names alone are not evidence.
- Read `README.md`, `TaskFlowDocs/repository-docs/index.md`, and applicable TaskFlow task documents.
- Run `bash hooks/repository-check .` for governance, fork, or pull-request work.

## TaskFlow workflow

Non-trivial changes require a Todo item, `prd.md`, `spec.md` when large, and `plan.md`. Do not implement until the Plan records user approval. Record verification and follow-ups in the Plan. Archive completed tasks under `TaskFlowDocs/achieved/` only after acceptance.

## Working branches

Never implement in the base working tree. One task, one short-lived branch, created before the first edit:

```bash
git switch -c fix/<description> <base-branch>
```

- Name the branch for its TaskFlow task, using the prefixes below.
- Keep a task's documents and its code on the same branch so the Plan, the diff, and the verification stay together.
- Confirm where you are before editing. `git branch --show-current` shows the branch; `bash hooks/repository-check .` reports the local branch and warns with `Base: ambiguous` when no upstream is set.
- Run `bash hooks/smoke-test` on the branch whose files changed, not on another checkout.

Agents working several tasks at once isolate each one in its own working tree; `skills/taskflow/SKILL.md` states that rule.

## Branches and commits

Use short-lived branches named `feature/<description>`, `fix/<description>`, `docs/<description>`, or `chore/<description>`. Keep commits focused and use `<type>: <imperative description>` (for example, `docs: clarify fork workflow`). Separate unrelated refactors and formatting changes.

## Checks

Before opening a pull request, run:

```bash
bash hooks/smoke-test
python3 /home/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/taskflow
git diff --check
```

Record unavailable checks and their limitations in the TaskFlow Plan. Do not claim checks or synchronization that did not occur.

## Pull requests

Read `.github/pull_request_template.md` before creating or updating a PR. Complete every required field and record its mapping in the TaskFlow Plan. Describe the goal, scope, TaskFlow task path, verification commands and results, remote/base assumptions, and known limitations. Do not include secrets or opaque remote payloads.
