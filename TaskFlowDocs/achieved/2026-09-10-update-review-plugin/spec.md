# Spec — Update and review TaskFlow plugin
> Task version: v1

## Objective and Success Criteria

Deliver one minimal patch that fixes the three reproduced defects, assigns an unambiguous cache version, and proves the published plugin works from its installed cache on Windows.

## Architecture Boundaries and Responsibilities

- `run-hook.cmd` selects a Windows-compatible Bash and delegates without changing Hook semantics.
- `summarize-state` derives Todo navigation from the documented fields.
- `archive` performs all non-mutating validation before its first move.
- `smoke-test` holds one regression check per non-trivial fix using temporary directories.
- Plugin manifests identify the installable release; Codex cache metadata identifies the exact Git revision.

## Project Structure / Affected Files

- `hooks/run-hook.cmd`
- `hooks/summarize-state`
- `hooks/archive`
- `hooks/smoke-test`
- `hooks/README.md` only where behavior text must change
- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`

No duplicate Skill/reference edits are needed unless implementation changes their existing contract.

## Interfaces, Data Flow, and Contracts

### Windows launcher

1. Keep current standard-location probes.
2. Derive Git's installation root from `where git` and probe its sibling `bin\\bash.exe` or `usr\\bin\\bash.exe`.
3. Use a PATH Bash only if it is not Windows' WSL launcher; otherwise exit without a Hook error, matching the existing no-compatible-Bash policy.

### Todo summary

Parse Markdown sections, read `- ID:`, `- Status:`, and `- Goal:` fields, and print non-done entries. The heading remains presentation, not identity.

### Archive

Before `mv`, require `todo.md` and verify it contains a `Task:` path for the active task. Preserve the existing post-move update and verification checks.

### Publication/install

Commit the approved plugin files, push `main`, refresh marketplace `taskflow`, run `codex plugin add taskflow@taskflow --json`, then use installed-state JSON, install metadata, hashes, and Windows Hook execution as final truth.

## Invariants and Compatibility

- No compatibility layer preserves invalid Todo-heading behavior; the documented ID field is authoritative.
- Existing `## T-...` entries still work when they also carry the required ID field.
- No move/delete occurs before archive preflight succeeds.
- No other plugin cache or marketplace is modified.
- `TaskFlowDocs/` remains untracked and unstaged.

## Validation and Error Semantics

- Missing compatible Git Bash: launcher exits silently, as currently documented.
- Missing Todo or task link: archive exits nonzero with the active directory unchanged.
- Marketplace/push/install failure: record the exact external failure and do not claim update completion.
- Cache mismatch after install: installed update is incomplete even if the version string looks correct.

## Code and Test Constraints

- Bash/batch/Python standard runtime only; no new dependency.
- Avoid blocking log-output techniques.
- Temporary regression fixtures must clean themselves up.
- Run Bash syntax checks, JSON parsing, smoke tests, Windows launcher test, focused archive failure test, diff checks, and installed-cache parity.

## Design Decisions and Alternatives

- Chosen: discover Git Bash relative to `git.exe`; this reuses the installed Git layout and fixes non-default drives.
- Rejected: invoke WSL Bash with path conversion; that adds a second runtime model and does not help Git-hook portability.
- Chosen: parse Todo ID fields; this matches the existing written contract.
- Rejected: require `## T-...` headings; headings are not specified as identifiers.
- Chosen: preflight archive inputs before move.
- Deferred: full rollback transactions for every lifecycle script; not required by the three reproduced failures.

## Open Questions

None.
