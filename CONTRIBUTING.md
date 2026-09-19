# Contributing to TaskFlow

## Before you start

- Work from a short-lived feature, fix, docs, or chore branch based on the intended base branch.
- For fork work, verify the target repository and base branch; remote names alone are not evidence.
- Read `README.md`, `TaskFlowDocs/repository-docs/index.md`, and applicable TaskFlow task documents.
- Run `bash hooks/repository-check .` for governance, fork, or pull-request work.

## TaskFlow workflow

Non-trivial changes require a Todo item, `prd.md`, `spec.md` when large, and `plan.md`. Do not implement until the Plan records user approval. Record verification and follow-ups in the Plan. Archive completed tasks under `TaskFlowDocs/achieved/` only after acceptance.

**A release is the exception.** It runs `RELEASE.md` directly, on the base checkout: no Todo item, no task directory, no PRD or Plan. `RELEASE.md` carries the approval gate a Plan's `## Approval` block otherwise provides.

## Working branches

Never implement in the base working tree. One task, one short-lived branch, created before the first edit — and before the first task document, which is written in the planning phase. A release is the one exception: it takes no branch, because it tags the base commit it already verified:

```bash
git worktree add .worktrees/<slug> -b <type>/<slug> <base>
cd .worktrees/<slug>
```

- Name the branch for its TaskFlow task, using the prefixes below.
- One task, one working tree — not only when several tasks run at once. What needs isolating is not just the code: a task's PRD, Plan, and its `todo.md` entry are written before implementation starts, and a task that writes them in the base checkout leaves them on whatever branch happened to be checked out.
- `.worktrees/` is ignored, so the working trees themselves never show up as changes.
- Keep a task's documents and its code on the same branch so the Plan, the diff, and the verification stay together.
- `hooks/task promote` refuses to run outside a task working tree, and `hooks/task intake` warns when it has written `todo.md` in a shared one.
- Confirm where you are before editing. `git branch --show-current` shows the branch; `bash hooks/repository-check .` reports the local branch and warns with `Base: ambiguous` when no upstream is set.
- Run `bash hooks/smoke-test` on the branch whose files changed, not on another checkout.

`skills/taskflow/SKILL.md` states the same rule where the phases are defined.

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
