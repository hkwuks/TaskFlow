# Changelog

## [1.1.3] — 2026-10-01

### Fixed

- **`hooks/reopen` undoes what `hooks/archive` wrote into the Todo.** Reopening an archived task moved the directory back to the active root and stopped there, leaving the entry's `Task:` line pointing at `TaskFlowDocs/achieved/<task>/`. `hooks/task` locates an entry by the literal substring `TaskFlowDocs/<task>/`, which that spelling does not contain, so the first `state`, `get`, `progress`, or `complete` after a reopen failed with `Todo entry not found` — and the only way to continue was to hand-edit `todo.md`. Measured in a live session on 2026-10-01 and recorded there as `TF-20261001-da6047`. `reopen` now writes `Task:` back to the active root, `Status: promoted`, a reopen-specific `Next action`, and `Updated:`, and it carries the three guarantees `archive` has: a fail-closed preflight, a rollback, and a post-write verification. The ordering is part of the fix rather than an accident of it — every file-content change is made while the tree is still in its original layout, so the single `mv` is the last mutation and the rollback never has to put a file back into a directory that has already moved out from under it.

### Changed

- **The task-document language rule binds the document, not whoever drafts it.** A capability invoked for a phase supplies a shape to fill, and prose folded in from it is written in the user's working language exactly as prose written directly is; the language of a template is not a policy adopted along with it. The scaffold exemption now covers any skeleton rather than `hooks/task promote`'s alone, and states where it ends: an unedited scaffold heading may stay in the language it arrived in, and it follows the rule once edited. The boundary the hooks read is unchanged.
- **The landing rule is two independent questions, not one.** A task's documents — its PRD, Spec, and Plan, the verification record written into the Plan, and the archive — land on the task's branch inside that task's own pull request, whatever the author's push permission. Push permission routes only the bookkeeping that belongs to no task: a Todo entry edited on its own, a `reopen`, release execution, and documentation maintenance with no task behind it. The section previously stated one permission criterion with a list of covered classes beneath it, which read as covering every change; a task's documents could then be pushed to the base outside its pull request, and on 2026-10-01 that happened twice in a row — one Plan record had to be cherry-picked onto `main`, and two archives were pushed after their merges.
- **A task's pull request is opened as a draft, and marked ready only once its documents are in it.** The Plan record and the archive can only be written after the branch is pushed and CI has run, so a merge otherwise arrives before the documents do. A draft is a state GitHub enforces and a reader sees; a sentence in the body is only a request.
- **A task's landing claim is recorded in that pull request, not written back afterwards.** Because the verification record itself now lands inside the pull request, a fact that exists only once the merge has happened has no place in the task's documents — writing it back would be a task document pushed to the base outside its own pull request. Such a criterion is stated as a check, and the merge topology is the evidence.
- **CI is named the test authority.** `CONTRIBUTING.md` and `RELEASE.md` now say that the smoke matrix runs on three hosts for every pull request and every push to `main`, so what stays local is what CI does not run — the Skill validator and `git diff --check`. Both READMEs' description of the check policy follows.

### Compatibility

- **No hook gains an interpreter dependency.** The smoke job still installs no language runtime, and the four host manifests and the `hooks.json` wiring are unchanged.
- **`reopen`'s Todo rewrite touches only the entry it retrieves.** Entries left broken by an older `reopen` are not repaired retroactively — `hooks/task` still cannot find them, and the remedy for those is to correct the `Task:` path by hand once, as it was before this release.
- **The rule changes are statements, not mechanics.** The landing rule, the landing-claim rule, and the artifact-language rule live in `CONTRIBUTING.md`, `RELEASE.md`, and the Skill. They change what is written and where it is recorded; the pre-write gate, the evidence store, the escape hatch, and every hook's behaviour are untouched apart from `reopen`.
- **All four hosts see the same rule text and the same `reopen` fix**; no host-specific path changed.

### Verification

- `bash hooks/release-check .` — `STATUS: pass`.
- `quick_validate.py skills/taskflow` — `Skill is valid!`
- `git diff --check` — clean.
- `bash hooks/repository-check .` — exits `2` (`needs-user-input`) on the orphan `TaskFlowDocs/achieved/2026-09-10-repository-document-placement`, which no Todo `- Task:` line names. Recorded rather than repaired here: it is pre-existing, it was recorded the same way in 1.1.2, and repairing it is a bookkeeping change a release does not carry.
- `bash hooks/smoke-test` — **not run locally, and recorded as skipped**, per the CI-first policy this release records. The release commit's difference from `fdc4139` — the last commit on `main` before this release began, CI run `36880093919` on `main`, `success` — is the version literals and this section, which the suite does not exercise; the commit after it moves only the two marketplace catalogs. The suite ran on all three hosts for each change this release ships, while each was a pull request.
- The `reopen` fix was verified locally by extracting the reopen section of `hooks/smoke-test` and running it against an equivalent fixture, because the full suite aborts in its no-interpreter section on the Windows/MSYS host this was developed on. Swapping the pre-change `hooks/reopen` back in fails the first new assertion, so the assertions are not vacuous. The same assertions ran in the three-host matrix on PR #65 (run `36820873430`).

### Known limitations

- **The landing rule's draft boundary is a convention, not a mechanism.** No CI job fails if a pull request is merged before its documents are in it; the draft state is what makes it visible.
- **The landing-claim rule is prose only.** No hook refuses a Plan that promises to write a result back after the merge; the rule is read, not enforced.
- **Entries broken by an older `reopen` are not repaired retroactively.** `hooks/task` still cannot find an entry whose `Task:` path points at `achieved/`.
- Unchanged from 1.1.2: `Agent` and `mcp__.*` matching is inferred from the tool-call lifecycle rather than measured; a leading UTF-8 BOM makes both gate hooks no-op; `Bash` can still write the evidence store and `reference/index.md` is not gated; the newer hooks are recorded `100644`.
- Pre-existing: `bash hooks/repository-check .` still reports the orphan `TaskFlowDocs/achieved/2026-09-10-repository-document-placement/`; it does so on 1.1.2 as well.

## [1.1.2] — 2026-09-30

### Changed

- **The task-document language rule names its English lines instead of naming every section heading.** `skills/taskflow/references/artifacts.md` and `skills/taskflow/SKILL.md` no longer put all `## ` section headings on the machine side of the boundary. The English list is now the section headings and entry headings `hooks/` matches by exact text (`## Approval`, `## Skills / Tools Used`, `## Verification / Review`, `## Change Log`, `## Items`, `## Removed`, `## Active / Resumable`, `## Closed / Reference Only`, `### Step N`, `### SN`), the `## Approval` fields, Todo field names, and the `> Task version:` / `> Status:` / `> Current Task version:` / `- Status:` lines and `- [ ]` / `- [x]` markers. A section heading outside that list is prose and follows the user's working language; translating one is safe because the hooks read the `## ` prefix as the section boundary and never the words after it. `hooks/task promote` still writes its own English scaffold, so a newly created document's headings arrive in English regardless.

- **The repository-document index no longer records whether a personal rule exists.** `TaskFlowDocs/repository-docs/index.md` is committed while `TaskFlowDocs/repository-docs/personal.md` is not, so the `personal-rule` row and the `Status: present` / `Status: not present` line made the tracked index permanently modified on any clone that had a personal rule — the uncommitted-but-tracked state that makes the next checkout refuse to move, the same class `57d507a` fixed for the check date. The row is now unconditional and reads `Exists: local` instead of the filesystem, and presence is reported by the `- Local personal rules …` session route line, so the committed index is byte-identical with and without a personal rule. `SKILL.md` and `references/artifacts.md` describe the split.

### Fixed

- **The task-document language rule is now recorded in the changelog.** It shipped inside `fix: require an approval before progress and completion` with no changelog entry and no mention of language in that commit message, so neither `git log -S"working language"` nor this file could find it. Recorded here retroactively rather than rewriting that commit's history.
- **A Todo title is cut on a character boundary instead of mid-byte.** `hooks/task intake` derived the entry heading with `substr(goal, 1, 80)` while the same script sets `LC_ALL=C`, where awk counts bytes, so a goal whose 80th byte fell inside a UTF-8 sequence wrote an invalid byte into the tracked `TaskFlowDocs/todo.md`. The 80-byte cap stays — it is what keeps the ID digest and the index bytes host-independent — and the cut now backs off to the last whole character, leaving a pure-ASCII goal byte-for-byte unchanged.
- **`hooks/task intake` records the host that ran it as the Todo owner.** The entry template wrote `- Owner: Codex` as a literal, so an entry created on Claude Code, CodeBuddy, or dsh claimed Codex. It now applies the detection `hooks/session-record` already uses and writes `Claude`, `Codex`, or `Unknown`.
- **`hooks/task progress` fails instead of dropping a verification line.** When the Plan carried no `## Verification / Review` — a translated or mistyped heading — the line was written nowhere and the command still printed `progress OK` and exited 0, so the verification was silently gone. It now exits nonzero and, because the write path is a temp file that is discarded on failure, leaves the Plan byte-identical.
- **The pre-write gate no longer fails open on Windows paths.** Claude Code delivers `tool_input.file_path` with backslashes there (claude-code #83877, #64432), and the gate extracted the task directory with `${file_path%/*}` — which finds no separator in a backslash path. The task directory came out as the whole path, the not-a-task-document guard fired, and every stage write was allowed with no output at all. Measured on 1.1.1: one document denied with forward slashes and allowed with backslashes, in the same repository. Nothing reported that the gate had stopped, and because the gate is the only writer of `released`, that record was never created on Windows either — so `task approve` failed with "was never released by the pre-write gate" for every task there, while naming the one command that could not fix it. The path and the event `cwd` are now normalized at entry, before any path test, and the Windows suite feeds the backslash form the host actually sends; it fed forward slashes before, which is how this shipped behind a green job.
- **The gate's regression fixtures escape backslashes for JSON.** The first version of the new assertion fed a raw backslash into the hand-written event, putting `\c` and `\r` in it — not escapes JSON defines. The parser rejected the whole event, the hook exited 0, and the write was allowed: the fixture reproduced the defect instead of detecting it. Escaping now happens where the host does it, in the JSON layer.

### Compatibility

- **Nothing else about the gate moves.** The evidence store and its format, the escape hatch, the `hooks.json` wiring, and the manifest shape are unchanged; the fix is one normalization at the gate's entry and one more on the event `cwd` it joins a relative path onto. No host gains a runtime dependency.
- **A task blocked at `approve` on Windows needs no repair beyond installing this release.** With the gate actually running, the stage is released the next time the document is written, or declared with `hooks/task unaided <stage> --considered "<concept class>"`. Plans approved before this release are not re-validated.
- **Claude Code only, unchanged from 1.1.1.** Codex, CodeBuddy, and dsh carry no gate.

### Verification

- `bash hooks/smoke-test` — the gate section asserts that both spellings of one file get one verdict: unreleased denied twice, released allowed twice, and a non-task path and an `achieved/**` path still no-ops, each case fed once as written and once with every separator flipped. The backslash `cwd` plus relative-path form is driven separately, since `cwd` is joined and normalized with the path. The new assertions were run against the un-normalized gate first and are red there (the backslash case is allowed), then green against the fix.
- `bash hooks/release-check .` — `STATUS: pass`.
- `quick_validate.py skills/taskflow` — Skill is valid!
- `git diff --check` — clean.
- The Windows suite drives the gate and the escape hatch through `run-hook.cmd` on a repository path containing a space and Chinese characters, now feeding the native backslash `file_path` and a backslash `cwd`.
- **The full suite cannot run on the Windows/MSYS host this was developed on** — it aborts in the no-interpreter section, and the unmodified base fails in the same place. `smoke (macos-latest)` adjudicates the bash 3.2 + BSD userland floor and `smoke (windows-latest)` the Windows behaviour; both passed on PR #61 (run 36700345485).

### Known limitations

- **1.1.1 still fails open on Windows; this release is what fixes it.** The defect was found in a live session rather than by the suite, because a repository edit does not reach an installed plugin until a release and reinstall. Verifying the installed 1.1.2 in a real session — a `prd.md` written through the host's own backslash path must be denied — is the remaining step, tracked as `TF-20260929-3fc4b8`.
- Unchanged from 1.1.1: `Agent` and `mcp__.*` matching is inferred from the tool-call lifecycle rather than measured; a leading UTF-8 BOM makes both hooks no-op; `Bash` can still write the evidence store and `reference/index.md` is not gated; the newer hooks are recorded `100644`.
- Pre-existing: `bash hooks/repository-check .` still reports the orphan `TaskFlowDocs/achieved/2026-09-10-repository-document-placement/`; it does so on the previous release too.

## [1.1.1] — 2026-09-28

### Added

- **A pre-write gate on `prd.md` / `spec.md` / `plan.md`.** The stage record added in 1.1.0 was shape-only: `Unaided — …` and a real invocation are the same text, so an overlooked phase could not be told from a compliant one, and the ordering it asked for — invoke before the first body write — was checked by nothing. On Claude Code a `PostToolUse` hook now appends one `kind|capability` line per real `Skill`, agent, or MCP call to `<absolute-git-dir>/taskflow/evidence`, and a `PreToolUse` hook refuses the first body write of a stage document in an active task directory until that stage can be released against one. Nothing is read out of the document, so no wording passes the gate. The store lives in the git directory: per worktree, invisible to `git status`, left alone by `version`, and unaffected by compaction or a changed session id. One invocation is spent by one stage, so writing `prd.md` and then `spec.md` needs two.
- `hooks/task unaided <PRD|Spec|Plan> --considered "<concept class>"` — declares a phase that ran without a capability and releases its stage. It is the single place a concept class is validated, and a class outside the phase vocabulary exits `2` with the vocabulary printed.

### Changed

- **`hooks/task approve` reconciles the stage record instead of pattern-matching it.** Each required stage line is checked against the release the gate wrote: an invoke line must name the capability that really was invoked, an `Unaided` line must carry the class that really was recorded, and a stage with no release fails closed before any Approval field is written. It prints how many stages were released by an invocation and how many unaided, so a task that declared every phase unaided is visible rather than silent. The large-task concept-class branch and the "invoke line is empty" branch are deleted — the store already guarantees both, and a concept class is validated only at the command that can write one.
- **The stage record moved out of `plan.md`.** `## Skills / Tools Used` is a report of what happened, reconciled at approve, rather than a declaration written before the document. `SKILL.md` and `references/artifacts.md` no longer ask for a stage line before the first body write; `references/runtime.md` documents the gate, its event wiring, and that it was measured against Claude Code 2.1.282.

### Compatibility

- **In-flight tasks are affected.** A task whose documents were written before this release has no release record for any stage, so `approve` fails closed for it and names the escape hatch. Declare each stage with `hooks/task unaided <stage> --considered "<concept class>"`, or re-run the phase with a capability invoked. Already-approved Plans are not re-validated.
- **Claude Code only.** `hooks-codex.json`, `hooks-codebuddy.json`, and `hooks-dsh.json` are untouched and carry no gate. A host without a tool-call hook runs the same flow unchanged — the gate is an enforcement, not a step.
- **The installation procedure is unchanged.** The same six files carry the version literal, the marketplace entry still names a tag and the commit it resolves to, and no host gains a runtime dependency. What changed is the wiring: on Claude Code the plugin now also registers a capture on `PostToolUse` and a gate on `PreToolUse`. The gate may only deny, never approve, and it never writes a core document. Both hooks are complete no-ops outside an active task directory, which they must be: hooks installed in `~/.claude/settings.json` are machine-global and fire in every concurrent session and unrelated repository.

### Verification

- `bash hooks/smoke-test` — new sections cover `json-field` (including a spoofing attempt through `Skill`'s free-form `args`), the capture hook's boundaries, the gate's allow/deny matrix and per-stage freshness, and approve's reconciliation. The rewritten approve section is proven to have teeth by running it against the pre-change hook, where it fails on exactly the new assertion. The no-interpreter section now drives both new hooks, and the Windows suite drives the gate and the escape hatch through `run-hook.cmd` on a repository path containing a space and Chinese characters. The CI matrix is green on all three platforms (PR #57, run 36438913953).
- `bash hooks/release-check .` — `STATUS: pass`.
- `quick_validate.py skills/taskflow` — Skill is valid!
- `git diff --check` — clean.
- The exact `command` strings in `hooks/hooks.json` were executed with synthetic events (deny → record → allow), so the wiring is covered and not only the scripts.
- **The full suite cannot run on the Windows/MSYS host this was developed on**: it aborts in the no-interpreter section, and the unmodified base fails in the same place. `smoke (macos-latest)` is therefore what adjudicates the bash 3.2 + BSD userland floor, and it passed. End-to-end behaviour in a live session is verified by the recipe in the task Plan after this release, because a repository edit does not reach an installed plugin until a release and reinstall.

### Known limitations

- **`Agent` and `mcp__.*` matching is inferred, not measured.** The hook contract was probed against Claude Code 2.1.282 for `Skill` (it fires both events and carries `tool_input.skill`); that the other two reach `PostToolUse` the same way follows from the same lifecycle. The wiring is executed, but the host's matcher behaviour is not observable from the repository.
- **A leading UTF-8 BOM makes both hooks no-op** (fail-open). Measured to come from PowerShell piping a string into a native command, not from a host event, and `session-start` shares the same parser — so stripping it is a repo-wide decision rather than a local fix.
- **`Bash` can still write the evidence store.** v1 refuses a direct `Write`/`Edit` to it as a discipline-level guard; closing the `Bash` path would need signing, deliberately out of scope. `reference/index.md` is not gated either — v1 covers the three stage documents.
- The three new hooks are recorded in Git as `100644`, not `100755` like most of `hooks/`. Nothing executes them directly — `run-hook.cmd` calls `bash <script>` — so the release is unaffected, and `hooks/release-version` is already `100644`. Normalizing the modes is a follow-up.
- Pre-existing: `bash hooks/repository-check .` still reports the orphan `TaskFlowDocs/achieved/2026-09-10-repository-document-placement/`; it does so on the previous release too.

## [1.1.0] — 2026-09-24

### Added

- **Personal rules live in a single `TaskFlowDocs/repository-docs/personal.md` (PR #55).** Each rule is its own section with its own `Scope`. `hooks/repository-docs-context` catalogs only that file as `personal-rule` and never merges it into `Read authoritative sources:`. Sibling `*.md` files beside `index.md` are not personal rules. The index `## Personal rules` section always names `personal.md`, states origin (local-only, never committed) and purpose (cannot override repository documents), and marks the file present or not present. Skill, artifacts, and both READMEs describe appending a section rather than creating a new sibling file.
- **Stage-gated capability records on PRD / Spec / Plan (PR #56).** Invoke a matching capability **when each document starts** (not after a draft) and append a stage-tagged line to the Plan’s `## Skills / Tools Used`: `[PRD]`, `[Spec]`, or `[Plan]`. `hooks/task approve` requires `[PRD]`+`[Plan]` always and `[Spec]` when `spec.md` exists; a missing or invalid stage fails closed before Approval is written, naming the stage. Validation is shape-only — any capability id, no product allowlist. Large-task Unaided stages must put a phase-table concept class in `considered:`. Skill and artifacts document the pre-write rule and foreign-output fold by kind (requirements → `prd.md`, design → `spec.md`, breakdown → `plan.md` Steps).

### Fixed

- Smoke fixtures for the stage gate pass multiline Skills bodies through the environment so BSD awk on macOS does not reject newlines in `-v` values (macos-latest CI).

### Compatibility

- **Personal.md is additive for empty catalogs.** Repositories with no personal rules only see richer standing prose in the index. Any existing sibling personal `*.md` files stop being cataloged; move their content into `personal.md` sections (local-only; never committed).
- **`task approve` now rejects Plans whose Skills section is empty or missing a required stage.** Existing already-approved Plans are not re-validated. Plans awaiting a first approve must carry stage-tagged lines (or are blocked until they do).
- **No runtime or installation change.** Hook floor (POSIX shell + awk), plugin wiring, and host manifest shape are unchanged from 1.0.9.

### Known limitations

- Temporal order (invoke truly before the first byte of `prd.md`) is Skill discipline plus the stage record, not a filesystem watcher.
- Stage lines can still be tokenized at approve time.
- `bash hooks/repository-check .` may still exit `2` for the pre-existing orphan `TaskFlowDocs/achieved/2026-09-10-repository-document-placement/` (no Todo entry in history).

## [1.0.9] — 2026-09-23

### Added

- `hooks/task approve <task-id> [approver]` — records an approval the user has already given into the Plan's five-field `## Approval` block (Status, approver defaulting to `user`, `date '+%Y-%m-%d %H:%M %z'`, plan Task version, and `PRD / Spec / Plan` scope from the core documents that exist). It only transcribes; it never invents consent, is not gated by `require_approval`, and leaves `> Status:`, Todo, and Git alone. The Skill now points at this command after the user approves; hand-editing the five lines is the fallback when the hook is unavailable.
- `hooks/repository-check` reports **orphan task directories**: every `TaskFlowDocs/<id>/` and `TaskFlowDocs/achieved/<id>/` that has `prd.md` or `plan.md` but no backticked `- Task:` line in `todo.md`. Orphans set `needs` (exit 2). The report is read-only — it never deletes or rewrites. Uncommitted-artifact lines stay needs-neutral.
- `hooks/release-version X.Y.Z` — writes the four host manifests and every README `plugin list` sample in one call after the `CHANGELOG.md` section exists; it never tags or pushes. Release overhead work landed in PR #47.

### Fixed

- **`task complete` / `hooks/archive` is fail-safe.** `complete` runs every preflight (including archive's own preconditions) before any `docstatus` write, and rolls both documents back to their prior `> Status:` if archive fails — no more half-archived tasks with `completed` docs beside an active directory. On success `archive` prints the exact `git add` lines for the moved paths and states that the commit belongs on the **current** branch (the task worktree branch), still without invoking Git. The Todo rewrite remains limited to Status / Task / Next action (PR #51).
- **`hooks/merge-todo` treats `## Removed` as a deletion.** A tombstone now matches its live entry by the first whitespace token of `- ID:`, deletion wins over a lone live copy, and dual-changed Removed sections union by ID instead of conflicting. `hooks/todo-check`'s `ids_at` uses the same token so an authorized removal is not a false drop (PR #50).
- `hooks/task intake` inserts at the top of `## Items` (skipping blanks and the template comment), else before `## Removed`, else EOF — not always at end of file, which could land a new entry inside `## Removed` (PR #48).
- `hooks/task get` prints every non-blank line of an entry body, so indented Notes continuations are no longer silently dropped (PR #49).
- `hooks/version` reset always emits the same five-line Approval block `hooks/task` promote writes, in order, and **inserts** a missing `- Status:` instead of refusing. The Skill's human record snippet now includes `- Status: approved` (PR #52).
- **Windows worktree detection.** `hooks/task` reads Git's absolute git dir (`--absolute-git-dir`), so a drive-letter path (`D:/…`) is no longer treated as relative to the repository root and worktrees are no longer judged to be the base tree (PR #45).
- `hooks/repository-docs` reads the catalog index by header name rather than by column count (PR #46).

### Compatibility

- **No runtime or installation change.** The hook set floor (POSIX shell + awk), the plugin wiring, and the host manifests' shape are unchanged from 1.0.8; updating needs no migration and no dependency installation.
- **`task approve` is a new subcommand**, not a gate change. `require_approval` still greps `- Status: approved`, `- Approved version:`, and a non-`pending` approver; existing Plans keep working.
- **Orphan reporting can turn a previously `pass` `repository-check` into exit 2** when a directory has no Todo reference. That is intentional (a lost record is actionable). This repository's tree carries one known historical orphan under `achieved/` until a human records the missing Todo entry — see Known limitations.
- **A release is two commits by construction.** The marketplace pin names a commit that cannot exist before the tag does; Claude Code verifies the pin as `sha_pin_mismatch` on mismatch and clones by the pinned commit, not the tag.

### Known limitations

- `bash hooks/repository-check .` on this repository may exit `2` solely because of `TaskFlowDocs/achieved/2026-09-10-repository-document-placement/`, which never had a Todo entry in history. Fixing that is a data decision (extra Todo line or deliberate acceptance), not a code defect of this release.
- Reverse direction (a Todo `Task:` pointing at a missing directory) is not asserted in this release; it was measured empty when the orphan check was designed and is deferred.

### Verification

- `bash hooks/smoke-test` — `ALL SMOKE PASSED` on the release working tree (2026-09-23).
- `bash hooks/release-check .` — `STATUS: pass` before the tag/pin step (version literals aligned; marketplace still names `v1.0.8` until the atomic pin push). Re-run after the pin is required by `RELEASE.md` step 6.
- `bash hooks/repository-check .` — `STATUS: needs-user-input` (exit 2) solely because of the known orphan `TaskFlowDocs/achieved/2026-09-10-repository-document-placement/` (see Known limitations). Not claimed as a pass.
- `python3 /home/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/taskflow` — Skill is valid.
- `git diff --check` — clean.

## [1.0.8] — 2026-09-19

### Added

- **DeepSeek Harness (dsh) support.** The repository root is now a dsh plugin package (`package.json` with `dsh.bundle.patch`), so `dsh plugin --profile <name> add dsh-taskflow` installs the skill and the SessionStart hook with no hand-written profile YAML. `dsh/index.js` mounts `@deepseek-ai/dsh-skill-filesystem` over the repository's own `skills/` and `@deepseek-ai/dsh-hooks-claude-code` over `hooks/hooks-dsh.json`, both of dsh's own packages rather than copies of them. The new wiring file sets `CLAUDE_PLUGIN_ROOT` on the command line because dsh's bridge substitutes that variable inside the command string but does not export it, and `hooks/session-start` chooses its output shape from the environment — without the prefix the hook's context is discarded silently. `hooks/release-check` now compares the dsh bundle manifest's version with the other three, and `hooks/smoke-test` runs the dsh wiring command the way dsh runs it.
- `hooks/task remove <todo-id> <reason>` — records the ID in a `## Removed` section and deletes the entry in the same write, so the intent is stated before the entry disappears. An entry whose `Task:` is not `Not promoted.` is refused, because deleting it would leave its task directory with no Todo record; unknown IDs and empty reasons are refused before anything is written.

### Fixed

- **`todo-merge-audit` failed on an authorized deletion.** `hooks/todo-check` reports any `- ID:` a merge commit's parent held and the result does not, which is exactly the failure it exists to catch — so it could not tell an authorized removal from a merge that lost an entry, and the release-workflow change tripped it on a deletion the owner had approved. `hooks/todo-check` now subtracts the IDs a commit records in `## Removed`, and behaves exactly as before when no record is present.
- `hooks/task remove` wrote its `## Removed` section between the header and the status flow, where it displaced the preamble a reader starts from. It now lands below the preamble. Found by running the command against the live `todo.md` rather than a fixture: the fixture had no preamble to expose it.

### Compatibility

- **A release no longer goes through TaskFlow.** `RELEASE.md` is the whole procedure and runs directly on the base checkout: no Todo item, no task directory, no branch, and no PRD, Spec, or Plan — the task workflow plans work that does not exist yet, and a release ships what is already merged. Its record is this `CHANGELOG.md` section and the GitHub Release body, and the approval gate moves with the procedure: the release owner approves the release commit before `RELEASE.md`'s step 5 pushes. A release that also changes the plugin is ordinary development work and still takes the full path. Nothing about installation changes.
- **dsh is the fourth host, and it installs outside the marketplaces.** `dsh plugin --profile <name> add dsh-taskflow` reads `dsh.bundle.patch` from the package manifest; there is no dsh catalog, so the two marketplace pins do not describe it. `hooks/release-check` compares its version with the other three manifests, and it carries no cachebuster because dsh installs through pnpm rather than a host-side plugin cache.
- **No change to the hook set or the other three hosts.** `hooks/session-start` is byte-identical, and `hooks/hooks.json`, `hooks-codex.json`, and `hooks-codebuddy.json` are untouched. The dsh wiring adapts to the shared script rather than the reverse.
- **A release is two commits by construction.** The marketplace pin names a commit that cannot exist before the tag does, so the pin lands as a second commit after the tag. Claude Code verifies the pin at install time and refuses a mismatch as `sha_pin_mismatch`; it clones by the pinned commit rather than by the tag, which is what keeps an installation on the reviewed release if the tag is ever moved.

### Verification

- `bash hooks/smoke-test` — passed on Ubuntu, macOS, and Windows GitHub Actions runners.
- `bash hooks/release-check .` — passed, over four manifests.
- `python3 evals/runner.py` — passed.
- TaskFlow Skill validator — passed.
- The dsh host was verified against an installed dsh 0.1.5-rc.2 at three layers: `dsh --profile <name> --dump-config` composited the TaskFlow row at exit 0; booting that profile listed exactly one skill, `taskflow`, from the provider the plugin registers; and dsh's own `matchesMatcher` and `parseHookOutput` accepted the shipped hook's matcher and read its real stdout back as SessionStart context, with negative controls. A live model turn and Windows were not exercised for this host.

## [1.0.7] — 2026-09-19

### Added

- `hooks/task next <todo-id> <next-action> [notes]` — writes a Todo entry's `- Next action:` and `- Updated:` in one call, and appends `notes` at the end of the entry's Notes block. The fields it writes are templated from state the Agent already has, so writing them by hand only bought a full read of `TaskFlowDocs/todo.md` to change two lines. Missing fields are added rather than failing the write, matching `hooks/archive`.
- `hooks/task get <todo-id>` — prints one entry's field lines verbatim, so confirming an entry's state no longer means reading every entry. It is the read half of the same trade `task next` makes on the write side.
- `hooks/repository-check` — a read-only readiness summary: missing baseline governance documents and ambiguous branch/remote information are reported as `needs-user-input`, and any task artifact left uncommitted in the checkout is named. Opt-in; it is not attached to automatic hooks.
- A conflict rule in `skills/taskflow/SKILL.md`: when a merge or rebase the Agent runs hits a conflict, stop and put both sides in front of the user, who decides what to keep; the decision is recorded in the task `plan.md` before continuing. An automatic merge needs no action, and a conflict on a pull request merged in a hosting web UI is explicitly outside the rule.

### Fixed

- **The Claude Code SessionStart hook failed on every Unix installation.** `hooks/hooks.json` invokes `hooks/run-hook.cmd` as a bare path, but the file was recorded in Git without its executable bit, so the host failed each session with `Permission denied` (exit 126) — a configured hook that could not run, and no plugin feature behind it. `hooks/*` and `tools/fixture-compare` now carry the executable bit in the index. **This is the reason to update from 1.0.6.**
- `README.zh-CN.md` said the release check compares "two plugin manifests" where `hooks/release-check` compares three. The count had been corrected once before, and a later conflict resolution reverted it — two sides that both read as valid Chinese, differing only in the number.
- The awk program in `hooks/task` could be broken by an apostrophe in a comment: macOS ships bash 3.2, whose parser rejects that shape inside a heredoc that is itself inside a command substitution, and it reports the failure against the end of the substitution rather than the comment.

### Compatibility

- **No runtime or installation change.** The hook set, the plugin wiring, and the POSIX-shell-plus-awk floor are unchanged from 1.0.6; updating an existing installation needs no migration and no dependency installation.
- **`task next` and `task get` are additions, not changes.** They are new explicit subcommands; the existing `intake` / `promote` / `state` / `progress` / `complete` lifecycle is unchanged, and a task that never calls them behaves exactly as before.
- **The conflict rule hands control back to the user.** On a conflict you decide which side to keep, so a merge that hits one stops and waits. Only merges the Agent runs are covered; a pull request resolved in a hosting web UI is not.
- **A release is two commits by construction.** The marketplace pin names a commit that cannot exist before the tag does, so the pin lands as a second commit after the tag. Claude Code verifies the pin at install time and refuses a mismatch as `sha_pin_mismatch`; it clones by the pinned commit rather than by the tag, which is what keeps an installation on the reviewed release if the tag is ever moved.

### Verification

- `bash hooks/smoke-test` — passed on Ubuntu, macOS, and Windows GitHub Actions runners.
- `bash hooks/release-check .` — passed.
- `python3 evals/runner.py` — passed.
- TaskFlow Skill validator — passed.

## [1.0.6] — 2026-09-17

### Added

- CodeBuddy as a third host: `.codebuddy-plugin/plugin.json` and `.codebuddy-plugin/marketplace.json`, installable through the CodeBuddy Code CLI (`codebuddy plugin marketplace add` then `codebuddy plugin install`), and `hooks/hooks-codebuddy.json` wiring `SessionStart` through `${CODEBUDDY_PLUGIN_ROOT}`. The CodeBuddy IDE client does not implement these commands, so the plugin is exercised through the CLI.
- `hooks/todo-check` — reports a Todo entry a merge dropped, by comparing every `- ID:` a merge commit's parents held against the result. A hosted-platform merge runs server-side where the merge driver cannot go, so the check runs after the fact; its range form audits every merge in a push, and the `todo-merge-audit` CI job runs it on every push to `main` and on every pull request.
- `hooks/release-check` — compares the version literals a release has to move (both plugin manifests, the newest `CHANGELOG.md` section, the `claude plugin list` sample in each README) and confirms each marketplace `ref` resolves to the commit its `sha` names. The `release` CI job runs it on every change, so a README sample or CHANGELOG section left on the previous version is caught at the commit that left it rather than at the next release.
- `RELEASE.md` records why a release is two commits, and its validation checklist now carries `hooks/release-check` in place of the inline Python manifest dump.

### Fixed

- `hooks/release-check` reads each catalog's pin from inside its `source` object instead of scanning the whole file, so a second entry carrying `ref`/`sha` can no longer displace the value being checked, and it validates the `X.Y.Z` shape of all three manifests rather than only the one without a cachebuster suffix.
- `hooks/archive` clears the Todo item's `Next action` to `None — completed and archived.` instead of leaving the pre-completion action in place. `promote` writes an action that is only true before completion, so every archived entry claimed outstanding work; the archive transaction now asserts the field was cleared.

### Compatibility

- **No runtime or installation change.** The runtime floor, the hook set, and the plugin wiring are unchanged from 1.0.5; updating an existing installation needs no migration or dependency installation.
- **CodeBuddy is CLI-only.** The CodeBuddy IDE client does not implement `plugin` subcommands, so the plugin is installed and validated through the CodeBuddy Code CLI.
- **A release is two commits by construction.** The marketplace pin names a commit that cannot exist before the tag does, so the pin lands as a second commit after the tag. Claude Code verifies the pin at install time and refuses a mismatch as `sha_pin_mismatch`; it clones by the pinned commit rather than by the tag, which is what keeps an installation on the reviewed release if the tag is ever moved.
- This is the first release that carries `hooks/release-check` and the archive `Next action` rule, so it is the first release either one governs.

### Verification

- `bash hooks/smoke-test` — passed on Ubuntu, macOS, and Windows GitHub Actions runners.
- `bash hooks/release-check .` — passed.
- `python3 evals/runner.py` — passed.
- TaskFlow Skill validator — passed.

## [1.0.5] — 2026-09-15

### Added

- A Git merge driver for `TaskFlowDocs/todo.md`, installed into the clone by `SessionStart`, so two task branches merge Todo by entry instead of by line.
- Deterministic Todo IDs derived from the goal (`TF-<yyyymmdd>-<6 hex>`), replacing the `TF-<date>-<max+1>` counter that made two branches cut from one base allocate the same ID.
- Session ids recorded in the selected task's `sessions.md`, and the macOS CI runner added to the hooks matrix.
- `CONTRIBUTING.md` working-branch rules and repository-documents guidance for personal rules.

### Fixed

- **Hooks no longer need a Python interpreter at all.** `hooks/python-runtime` and `TASKFLOW_PYTHON` are gone; every hook is POSIX shell with `awk` and `sed` at the bash 3.2 + BSD userland level.
- macOS portability: `sed`/`grep` patterns that relied on GNU-only `\|` and `\{n\}` no longer fail silently or vacuously, and the hooks parse under the bash 3.2 that macOS ships.
- `hooks/version` no longer archives a tracked document that has uncommitted changes, which had made `old/vN/` record the text that replaced the version instead of the version itself.
- `task progress` and `task complete` now require the same recorded approval as `task state in_progress`; previously an unapproved task could be completed step by step and archived.
- Windows launcher argument forwarding, and the repository-document index path and concurrency protections carried over from 1.0.4.

### Compatibility

- **The runtime floor dropped.** No interpreter needs to be located, validated, or version-matched; a missing, shimmed, or wrong-major-version Python is no longer a failure mode. Windows still requires Git for Windows Bash, and there is still exactly one implementation of each hook.
- **Todo IDs change shape for new entries.** Existing entries keep their numeric suffix; only new intake uses the derived six-hex-digit form.
- **The Todo merge driver applies to local merges only.** A pull request merged in a hosting web UI runs server-side and does not run a custom driver, so that path still produces an ordinary content conflict. `skills/taskflow/references/runtime.md` states this.
- Updating an existing installation needs no migration or dependency installation.

### Verification

- `bash hooks/smoke-test` — passed on Ubuntu, macOS, and Windows GitHub Actions runners.
- `python3 evals/runner.py` — passed.
- TaskFlow Skill validator — passed.
- Every hook parses under a real `bash:3.2` container.

## [1.0.4] — 2026-09-13

### Added

- Current-task-first SessionStart context with explicit verbose mode.
- SessionStart event JSON routing using `cwd`, event filtering, and safe malformed-input diagnostics.
- Linux and Windows GitHub Actions coverage for TaskFlow hooks.

### Fixed

- Windows launcher forwarding for more than nine arguments, spaces, and Unicode values.
- Repository-document index path traversal validation, malformed-row preservation, and concurrent-write protection.
- Explicit Python 3 runtime discovery and Microsoft Store alias diagnostics.

### Compatibility

- Runtime behavior remains backward-compatible; hooks continue to use Git Bash on Windows and Python 3 for Markdown lifecycle operations.
- No migration or dependency installation is required for existing installations.

### Verification

- `bash hooks/smoke-test` — passed.
- Linux and Windows GitHub Actions matrix — passed.
- TaskFlow Skill validator — passed.
