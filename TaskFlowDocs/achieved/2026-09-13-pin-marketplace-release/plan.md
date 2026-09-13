# Plan — Pin stable marketplace installs to released revisions

- Task version: v1
- Status: completed

## Repository documents

- `TaskFlowDocs/repository-docs/index.md` — read first; routes this change to repository and release rules.
- `CONTRIBUTING.md` — use a short-lived `chore/` branch and focused commit.
- `CODE_STYLE.md` — keep Markdown concise and bilingual behavior aligned.
- `RELEASE.md` — direct-tag release remains authoritative.
- `README.md` and `README.zh-CN.md` — installation guidance must remain aligned.

## Skills / Tools Used

- `taskflow` — recorded Todo-first intake, approval, scope, and verification.
- `openai-docs` — confirmed Codex Git marketplace entries support `ref` and `sha` selectors.
- `sxng` — located and checked Anthropic's official marketplace source/version rules.
- `git-workflow-and-versioning` — selected a short-lived branch and immutable release pin.

## Approval

- Approved by: user
- Approved at: 2026-09-13 22:49 +08:00
- Approved version: v1
- Approved scope: fixed `v1.0.4` tag plus commit SHA, retained local development path, direct short-lived branch implementation without a new release

No spec required — this is a bounded marketplace metadata and documentation correction with no runtime contract change.

## Steps

### Step 1 — Pin the shared marketplace entry

- Goal: Make stable remote installs resolve to the immutable v1.0.4 commit.
- Dependencies: published tag and commit identity verified.
- Files: `.claude-plugin/marketplace.json`.
- Implementation checklist:
  - [x] Replace the relative source with the cross-host Git URL source.
  - [x] Set both `ref` and the full `sha`.
- Acceptance: both host schemas accept the entry and it targets the repository root.
- Verification: JSON parse, repository checks, and host validators where available.
- Rollback: revert the marketplace entry to `./`.
- Status: done

### Step 2 — Document stable and local channels

- Goal: Keep future releases pinned without removing local development installs.
- Dependencies: Step 1.
- Files: `README.md`, `README.zh-CN.md`, `RELEASE.md`.
- Implementation checklist:
  - [x] Explain that remote stable installs follow the release pin advertised by the catalog on `main`.
  - [x] Retain local-directory development commands.
  - [x] Add the tag-plus-SHA catalog update to the release checklist.
- Acceptance: English, Chinese, and release guidance agree.
- Verification: focused text review and `git diff --check`.
- Rollback: revert the documentation changes with the metadata change.
- Status: done

### Step 3 — Verify and close

- Goal: Prove the focused change and archive its records.
- Dependencies: Steps 1–2.
- Files: task records and Todo.
- Implementation checklist:
  - [x] Run repository and smoke checks.
  - [x] Validate the skill and JSON manifests.
  - [x] Review the final diff for unrelated files or secrets.
  - [x] Archive the completed task and update Todo.
- Acceptance: all applicable checks pass or limitations are explicitly recorded.
- Verification: commands and results recorded below.
- Rollback: leave the task active and record the blocker.
- Status: done

## Verification

- JSON parsing for both manifests and the shared marketplace — passed.
- `git rev-list -n 1 v1.0.4` matched the marketplace `sha` `2691453a40955a6f7353c3326dd44c58638f6608`.
- `claude plugin validate .` — passed.
- `codex plugin list --json` — passed and resolved TaskFlow as Git source `v1.0.4` plus the full pinned SHA.
- `bash hooks/repository-check .` — passed; expected working-tree change notice only.
- `bash hooks/smoke-test` — all smoke checks passed in a writable environment.
- Skill quick validator — passed.
- `git diff --check` — passed.
- Scope review excluded unrelated untracked `test.md` and preserved the pre-existing repository-index auto-sync change in a stash.

## Risks and rollback

- If either host rejects the shared `url` source shape, do not publish; retain the relative source and split host catalogs only after explicit approval.
- A bad pin prevents new stable installs; rollback is a focused revert on `main`, without changing the published tag.

## Change Log

- 2026-09-13 — User approved pinning stable distribution to `v1.0.4` plus its full commit SHA while retaining local development installs; agreed this small change does not require a worktree or a new plugin release.
