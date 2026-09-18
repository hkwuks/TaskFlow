# Plan — Hook launcher exec bit
> Task version: v1
> Status: in_progress

No spec required — a file-mode change plus one assertion section.

## Reference Pointers

- `hooks/hooks.json` — the `command` value the harness executes verbatim;
  the reason the launcher needs the bit.
- `hooks/smoke-test` (final section) — the only place the harness's own
  invocation form is exercised.
- `obra/superpowers` `hooks/run-hook.cmd` at `100755` — the upstream pattern
  this launcher is modelled on.

## Related Tasks

- `TaskFlowDocs/achieved/2026-09-08-runtime-hooks/` — introduced the launcher.
- `TaskFlowDocs/achieved/2026-09-14-macos-hook-portability/` — the suite's
  portable-invocation conventions.

## Skills / Tools Used

`ponytail` (laziest sufficient fix: a mode, not a command rewrite) and
`claude-code-guide` for the hook execution contract and plugin-install
behaviour. Both were consulted before the first edit.

## Preconditions

- [x] Repository documents read; no priority conflict.
- [x] Remote / branch: `origin` = `hkwuks/TaskFlow`, base = `origin/main`
      (currently `ebd6b4f`), branch `fix/hook-launcher-exec-bit` in its own
      worktree from `04e830e`. The two differ by archived `readme-refresh`
      documents only, so this branch rebases cleanly.
- [x] This task adds no governance document.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-18 20:30 +0800
- Approved version: v1
- Approved scope: PRD / Plan v1 — exec bit on every `hooks/` script plus
  `tools/fixture-compare`, and one new smoke section asserting the harness's
  invocation form. User's words: "A，全修".

## Steps

### Step 1 — Record the hook scripts as executable

- Goal: A Unix plugin install can execute the launcher and every hook.
- Dependencies: none.
- Files: `hooks/*` (modes only), `tools/fixture-compare` (mode only).
- Implementation checklist:
  - [x] `git update-index --chmod=+x` on every non-JSON, non-Markdown file
        under `hooks/` and on `tools/fixture-compare`. `--chmod` writes the
        index directly, which is what matters here: this checkout sits on a
        drvfs mount with `core.filemode=false`, where a filesystem-level
        `chmod` is neither recorded nor reliable.
  - [x] Confirm no file content changed (`git diff --cached --stat` shows mode
        changes only).
- Acceptance: `100755` in the index for every affected file; byte-identical
  contents.
- Verification: `git ls-files -s` listing; `git diff --cached --summary`.
- Rollback: `git update-index --chmod=-x <path>` for each file.
- Status: done

### Step 2 — Assert the harness's invocation form in the suite

- Goal: The suite fails when the launcher cannot be run as the harness runs it.
- Dependencies: Step 1 (the section has to pass on the fixed tree).
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] Assert `hooks/run-hook.cmd` is `100755` **in the Git index**, read via
        `git ls-files -s`, whenever this checkout has one at `$HERE`; skip
        outside a Git checkout. The index is read rather than the filesystem
        because this host's mount reports every file executable, so a
        `test -x` check cannot see the real failure here.
  - [x] Execute the launcher as the harness does: bare path, no `bash` prefix,
        through `sh -c`, with `PATH` extended so the tree's own `bash` call
        resolves (the harness gives no guarantee that `bash` is on the hook's
        `PATH`), and assert the output carries `hookSpecificOutput`.
  - [x] Keep the section in the existing assert style; no harness added.
- Acceptance: The section passes on the fixed tree and fails when either the
  index mode or the on-disk mode is reverted.
- Verification: four runs, recorded below.
- Rollback: delete the section.
- Status: done

## Checkpoints

- Step 2 was written after Step 1 so the section's own pass is meaningful
  rather than a red test committed as evidence.

## Verification / Review

- `bash hooks/smoke-test` — `ALL SMOKE PASSED` (whole suite, worktree tree).
- Mutation 1 — index mode reverted with `git update-index --chmod=-x
  hooks/run-hook.cmd`: `FAIL run-hook.cmd is recorded as 100644, not 100755:
  it installs non-executable and every Unix hook fails with 'Permission
  denied'`. Restored to `100755`.
- Mutation 2 — a non-Git copy of the tree with `chmod 644
  hooks/run-hook.cmd`: `FAIL run-hook.cmd could not be executed directly:
  /bin/sh: 1: ...: Permission denied`.
- Control — the same copy left executable, and the worktree as committed:
  section `ok`, `ALL SMOKE PASSED`.
- `git diff --check` — clean. A mode-only diff has no text hunks by
  construction; the staging was also read back with `git diff --cached
  --summary` to confirm no content moved.
- Limitations: `hooks/smoke-test-windows.ps1` and the PowerShell/cmd lifecycle
  were not run here (no Windows host); the mode change cannot affect them
  because `cmd.exe` and PowerShell do not read the bit. `python3
  evals/runner.py` was not run — the eval runner does not load hooks, and this
  change moves no content.

## Change Log

- 2026-09-18 Step 1 — `git update-index --chmod=+x` on all 16 `hooks/`
  scripts and `tools/fixture-compare`; no content change.
- 2026-09-18 Step 2 — new final section in `hooks/smoke-test`, named for what
  it checks. Written to read the index first and only then attempt the
  execution, so the more specific diagnosis wins on this host.
- 2026-09-18 — task documents written after the fix was verified, not before;
  the work was direct user instruction ("A，全修") against a live failure, and
  the Todo item and this directory were created on the same branch before the
  commit.

## Follow-ups

- `tools/fixture-compare` non-idempotence: two runs of the unmodified suite
  differ in `release-check/.claude-plugin/marketplace.json`,
  `release-check/.codebuddy-plugin/marketplace.json`, and `todo-check/out`,
  each embedding a fresh Git SHA. Pre-existing, unrelated, unfixed.
- The installed plugin cache on this host (`~/.claude/plugins/cache/taskflow`)
  still holds a `644` launcher and will keep failing until the plugin is
  updated to a release carrying this fix.

## Version History

- v1 — planning.
