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
- If a local `bash hooks/smoke-test` is warranted, run it in the worktree whose files changed, not in another checkout — the suite reads the tree it is run from.

`skills/taskflow/SKILL.md` states the same rule where the phases are defined.

### Where the commit lands

Everything above is about **isolation** — keeping a task's work off whatever branch happened to be checked out. This section is the other half: which commits go straight to the target branch, and which go through a pull request.

It routes **bookkeeping**, and only bookkeeping:

- **Todo entries** — intake, promotion, status, next action, removal.
- **A task's status and archive** — moving `TaskFlowDocs/<task>/` to `achieved/`, and the status lines that move with it.
- **Release execution** — the release commit and the catalog pin, as `RELEASE.md` describes.

None of those has anything to review, so each goes straight to the target branch when the author can push it, and to a pull request when they cannot. From a task worktree that means pushing the branch's commits to the base — the branch there is a work surface, not a proposal.

**Everything else keeps its pull request.** Code, hooks, the Skill, and any document whose wording is worth reviewing do not become direct pushes because the author happens to have permission. If you are unsure which side a change falls on, it is a pull request.

Whether you can push is a checkable fact, not a job title — the target branch's protection rules, and the author's role on the repository:

```bash
gh api repos/<owner>/<repo> --jq .permissions
gh api repos/<owner>/<repo>/branches/<base>/protection
```

An unprotected branch plus a role carrying `push` is the direct path. A protected branch, a read-only role, or a fork you cannot write to is a pull request. Neither answer is permanent — protection and roles are configuration — so check rather than remember, and do not infer it from who someone is.

This does not relax the rule above. A worktree isolates a task's work; this decides where that work's commits go, and the isolation rule is unchanged.

## Branches and commits

Use short-lived branches named `feature/<description>`, `fix/<description>`, `docs/<description>`, or `chore/<description>`. Keep commits focused and use `<type>: <imperative description>` (for example, `docs: clarify fork workflow`). Separate unrelated refactors and formatting changes.

## Checks

CI is the test authority. The `Hooks` workflow runs the full matrix — the smoke
suite on `ubuntu-latest`, `macos-latest`, and `windows-latest`, plus
`hooks/release-check`, the Todo merge audit, and the evals — for every pull
request and every push to `main`. Push the branch and read the verdict there
rather than reproducing the matrix locally: a local run spends time and resources
CI has already spent, and it adjudicates one host where CI adjudicates three.

Run something locally only when CI cannot cover it — the host-specific, such as
the Windows suite on a Windows machine, and the pre-push, where failing early is
worth more than failing in CI. Two checks no CI job runs, so they stay local for
every change:

```bash
python3 <skill-creator>/scripts/quick_validate.py skills/taskflow   # <skill-creator> is wherever that checkout lives
git diff --check
```

**A surface CI does not exercise is added to CI in the same change** — not left
to a local run, and not shipped unverified. The smoke matrix exists because the
hooks have to work on three hosts; a new hook, a new host, or a changed plugin
surface belongs in it before it belongs in a pull request. When adding it in that
change is not possible, say so in the TaskFlow Plan and run it locally until it
is. A preference for CI is never a reason for something to go unverified, and CI
that has fallen behind the surface it is supposed to cover is not an authority —
keep it current, and keep it running on the hosts it declares.

Release-time checks are their own list, in `RELEASE.md`, which states which of
them CI covers and which it cannot.

Record unavailable checks and their limitations in the TaskFlow Plan. Do not claim checks or synchronization that did not occur.

## Pull requests

Read `.github/pull_request_template.md` before creating or updating a PR. Complete every required field and record its mapping in the TaskFlow Plan. Describe the goal, scope, TaskFlow task path, verification commands and results, remote/base assumptions, and known limitations. Do not include secrets or opaque remote payloads.
