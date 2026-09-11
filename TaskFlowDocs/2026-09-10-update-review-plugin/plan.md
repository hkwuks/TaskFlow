# Plan — Update and review TaskFlow plugin
> Task version: v1
> Status: completed

## Spec Pointers

- `spec.md` — launcher selection, Todo parsing, archive preflight, versioning, and installation contracts.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md`
- `hooks/README.md`
- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`

## Related Tasks

- `TaskFlowDocs/achieved/2026-09-10-repository-document-placement/` — completed documentation placement change already on `origin/main`.

## Skills / Tools Used (Optional)

- `taskflow` — purpose: govern requirements, approval, execution, verification, and archive; incorporated: this v1 contract.
- `agent-skills:code-review-and-quality` — purpose: evidence-led multi-axis review; incorporated: three reproduced required findings.
- `agent-skills:git-workflow-and-versioning` — purpose: keep publication atomic and scoped; incorporated: exclude `TaskFlowDocs/`, verify staged diff before commit.
- `ponytail` — purpose: minimize repair scope; incorporated: three direct fixes and focused tests, no broad rewrite.
- `context-mode` — purpose: inspect repository, plugin cache, and scripts efficiently; incorporated: installed revision, cache differences, and call-path evidence.

## Preconditions

- [x] Current date, Windows version, project path, Git state, and absence of CodeGraph confirmed.
- [x] Installed TaskFlow source, enabled state, version, revision, and cache path confirmed.
- [x] Three findings reproduced or verified against the real invocation path.
- [x] User authorized fixes, version bump, scoped commit/push, and TaskFlow-only reinstall/update.
- [x] User approves Task version v1 execution contract.

## Approval

- Status: approved
- Requested: 2026-09-10
- Approved: 2026-09-10 by user
- Scope: PRD and Spec v1 in this directory.

## Steps

### Step 1 — Fix confirmed Hook defects
- Goal: Correct Windows launch, Todo discovery, and archive preflight at their shared sources.
- Dependencies: v1 approval.
- Files: `hooks/run-hook.cmd`, `hooks/summarize-state`, `hooks/archive`, `hooks/README.md` if needed.
- Implementation checklist:
  - [x] Select compatible Git Bash on non-default drives and reject WSL Bash fallback.
  - [x] Parse Todo identity from required ID fields.
  - [x] Validate Todo and matching task link before archive move.
- Acceptance: Each reproduced failure is eliminated without changing unrelated behavior.
- Verification: Focused Windows and temporary-directory reproductions.
- Rollback: Revert only Step 1 files.
- Status: done

### Step 2 — Add regression checks and bump versions
- Goal: Leave runnable checks and a unique install-cache identity.
- Dependencies: Step 1.
- Files: `hooks/smoke-test`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`.
- Implementation checklist:
  - [x] Add one focused assertion per fix.
  - [x] Set Claude version to `1.0.1` and Codex version to `1.0.1+codex.<timestamp>`.
  - [x] Validate JSON and shell syntax.
- Acceptance: New checks fail against the old behavior and pass against the fix; manifests are coherent.
- Verification: Smoke test, focused commands, JSON parsing, Bash syntax checks.
- Rollback: Revert Step 2 files and restore previous versions.
- Status: done

### Step 3 — Review, commit, and push scoped plugin files
- Goal: Publish exactly the approved fix set to `origin/main`.
- Dependencies: Steps 1–2 pass verification.
- Files: Only approved plugin files; explicitly exclude `TaskFlowDocs/`.
- Implementation checklist:
  - [x] Review working and staged diffs for correctness, security, simplicity, and scope.
  - [x] Stage only approved plugin files and verify staged file list/content.
  - [x] Commit with repository convention and push `main`.
- Acceptance: `origin/main` contains the scoped commit and TaskFlow artifacts remain untracked.
- Verification: Staged diff, commit file list, remote branch revision.
- Rollback: Before push, amend/recreate scoped commit; after push, use a new revert commit only with user authorization.
- Status: done

### Step 4 — Refresh and verify installed TaskFlow
- Goal: Make Codex use the pushed release and prove installed behavior.
- Dependencies: Step 3 remote success.
- Files: User-level TaskFlow marketplace/cache managed by Codex CLI.
- Implementation checklist:
  - [x] Upgrade only marketplace `taskflow`.
  - [x] Reinstall/update only `taskflow@taskflow`.
  - [x] Verify installed/enabled version and install revision.
  - [x] Verify maintained cache files match the pushed revision.
  - [x] Execute the installed Windows SessionStart Hook path.
- Acceptance: Installed TaskFlow reports the new version/revision and all parity/behavior checks pass.
- Verification: `codex plugin list --json`, install metadata, hashes, Windows Hook output.
- Rollback: Reinstall prior published revision/version only if current installation becomes unusable and recovery is necessary.
- Status: done

## Checkpoints

- After Step 2: all local regressions pass before publication.
- After Step 3: remote revision and scoped file set are confirmed.
- After Step 4: installed cache matches the remote commit and Hook executes successfully.

## Verification / Review

- Bash syntax checks passed for all Hook scripts.
- `hooks/smoke-test`: `ALL SMOKE PASSED`, including field-based Todo parsing, Windows Git Bash discovery, and archive preflight preservation.
- Real Windows launcher returned exit 0 and valid JSON containing `TF-20260910-02`.
- Missing-Todo and missing-task-link archive cases both returned nonzero with `active=true` and `achieved=false`.
- All plugin and Hook JSON files parsed; versions are Claude `1.0.1` and Codex `1.0.1+codex.20260910154748`.
- `git diff --check` passed; review found no credential material or new blocking issue.
- Implementation deviation: Windows testing exposed a `python3` WindowsApps shim that exits 49; the same root runtime path affected summarize/archive/reopen, so those scripts now verify `python3` and minimally fall back to `python`.
- User committed and pushed the approved eight-file change as `5c196dadf1130573c0998d0ee88c62778306f6e0`; local HEAD, `origin/main`, and remote `main` match, and post-commit regressions pass.
- External blocker: the execution environment rejected `codex.cmd plugin marketplace upgrade taskflow --json` twice, including after explicit user authorization; no marketplace or cache mutation occurred.
- User completed the two blocked Codex CLI operations locally. `codex plugin list --json` reports TaskFlow `1.0.1+codex.20260910154748` installed and enabled.
- Marketplace HEAD, cache install metadata, local HEAD, `origin/main`, and remote `main` all identify revision `5c196dadf1130573c0998d0ee88c62778306f6e0`.
- Installed Windows SessionStart Hook returned exit 0, valid JSON, and the current Todo item.
- Cache parity passed: 27 files were raw-byte identical; `LICENSE` differed only by CRLF versus LF checkout representation, with identical Git-normalized object hash `0ad25db4bd1d86c452db3f9602ccdbe172438f52` and no text diff.

## Change Log

- 2026-09-10 v1 planning — recorded three confirmed review findings and authorized update/publication scope.
- 2026-09-10 v1 approval — user approved implementation and publication of PRD/Spec v1.
- 2026-09-10 v1 implementation — fixed Git Bash selection, Todo field parsing, archive preflight, and Python shim handling; added focused regressions and bumped versions.
- 2026-09-10 v1 publication — user committed and pushed scoped changes as `5c196da`; installation refresh is blocked by execution-environment review.
- 2026-09-10 v1 installation — user refreshed and reinstalled TaskFlow; installed version, revision, cache parity, and Windows Hook verification passed.

## Follow-ups

- Reassess other lifecycle scripts for stronger rollback semantics only if a separate reproduced failure warrants it.

## Version History

- v1 — Approved, implemented, published, installed, verified, and completed.
