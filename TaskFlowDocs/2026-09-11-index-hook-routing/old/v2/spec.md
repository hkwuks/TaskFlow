# Spec — Index-driven repository document routing
> Task version: v2

## Objective and Success Criteria

Maintain one machine-readable Markdown catalog, then derive compact phase routing from it during SessionStart.

## Architecture Boundaries and Responsibilities

- `hooks/repository-docs-context`: synchronizes the catalog and prints routing context.
- `hooks/session-start`: composes task state and repository-document context into host JSON.
- `index.md`: routing/check record; source files remain policy authority.
- `SKILL.md`: defines when to read the index and routed sources without restating their rules.
- `run-hook.cmd`: provides the Windows boundary and invokes the same Bash implementation through Git for Windows.

## Project Structure / Affected Files

- `hooks/repository-docs-context`, `hooks/session-start`, `hooks/smoke-test`
- `TaskFlowDocs/repository-docs/index.md`
- `skills/taskflow/SKILL.md`, `skills/taskflow/references/artifacts.md`
- Hook documentation as needed
- `hooks/smoke-test-windows.ps1`

## Interfaces, Data Flow, and Contracts

`SessionStart -> repository-docs-context --sync -> index.md -> phase filter -> additionalContext`.

Windows follows `run-hook.cmd -> Git for Windows Bash -> session-start`; no hook logic is duplicated in PowerShell.

The table columns are `Class`, `Source path`, `Phases`, `Exists`, `Last checked`, and `Status`. Recognized conventional paths are synchronized automatically. Personal supplements are discovered under `repository-docs/personal/`.

## Invariants and Compatibility

- Source documents, core task documents, approval state, and Git metadata are never edited.
- No remote or hosting-provider operation occurs.
- Unknown candidate files are not silently promoted into binding policy.
- Paths containing spaces and non-ASCII characters survive the Windows launcher and JSON boundary.

## Validation and Error Semantics

- A write failure makes the helper fail and SessionStart report failure.
- Missing recognized sources remain catalog records with `missing` status.
- Unknown likely governance files are summarized as `needs-review` candidates.
- Missing Git for Windows Bash keeps the existing launcher behavior; installation documentation states that runtime dependency.

## Code and Test Constraints

- Reuse the repository's Bash-plus-Python hook pattern.
- Use atomic index writes and idempotent output.
- One focused smoke fixture covers synchronization, routing, and repeated execution.
- The Windows fixture invokes `run-hook.cmd session-start`, parses its JSON, checks routed paths and index contents, then repeats the call and compares hashes.

## Design Decisions and Alternatives

- Synchronize at SessionStart, not on every command, to avoid repeated writes and races.
- Inject paths/status, not full contents, to limit context and preserve authority boundaries.
- Use a fixed conventional-path registry; semantic classification of arbitrary documents is deferred.
- Reuse Git for Windows Bash instead of maintaining parallel Bash and PowerShell implementations.

## Open Questions

None.
