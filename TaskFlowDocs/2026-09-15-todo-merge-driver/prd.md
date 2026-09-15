# Ship a Todo merge driver so parallel task branches merge cleanly
> Task version: v1
> Status: in_progress

## Goal

Give the plugin a strategy for the case where two task branches both record Todo
intake: a per-entry merge driver shipped with the plugin, installed into the
clone by a hook, so `TaskFlowDocs/todo.md` merges by Todo entry instead of by
line.

## Background / Confirmed Facts

- `TaskFlowDocs/todo.md` is a single append-only-in-practice file. Every task
  starts by adding an entry to it and every task completion updates one, so any
  two branches that both touch Todo conflict at merge time.
- Measured on this repository: merging two open task branches into `main`
  conflicted in `TaskFlowDocs/todo.md`, and the conflict was purely two adjacent
  appended entries — textually independent, semantically unrelated.
- `git`'s built-in `merge=union` is not the answer. Measured: with two entries
  appended at end of file it merged cleanly, but two entries inserted at the top
  interleaved and **dropped shared trailing lines**, silently removing `- Status`
  and `- Next action` fields from one entry. Losing a Status field is worse than
  a conflict, because nothing reports it.
- Hosted merge is not available as a fix. GitHub does not run custom merge
  drivers: drivers live in `.gitconfig`, which is not shipped with a repository,
  and GitHub merges server-side with libgit2 for exactly that reason
  (`isaacs/github#487`, still open; GitHub's own reply is that users who want
  alternate merge methods must merge locally). Measured: with `merge=foo` in
  `.gitattributes` and no driver configured, `git` falls back to an ordinary
  content conflict — so an unconfigured clone behaves exactly as it does today.
- The plugin cannot change a user's repository or hosting settings. Anything that
  depends on a ruleset, a branch-protection toggle, or a repository-level
  workflow is out of reach, which rules out "require branches to be up to date"
  as the strategy.
- The plugin *can* ship the driver script and *can* install the driver config,
  because `SessionStart` already runs in the user's clone and already performs
  repository-local setup (`TaskFlowDocs/repository-docs/index.md`).
- A custom driver that is only shipped but never installed silently degrades to
  today's conflict behavior, which is an acceptable failure mode but must be
  documented rather than left implicit.
- **Todo IDs collide across parallel branches.** Measured while creating this
  task's own sibling tasks: `task intake` allocates
  `TF-<date>-<max(existing)+1>`, computed from the branch's own copy of
  `todo.md`. Two branches cut from the same base on the same day therefore both
  allocate `TF-20260915-01` for different goals, and a merge driver that
  correctly keeps both entries produces a file with two entries sharing one ID.
  `todo_part` resolves an ID match by first hit, so every later command
  (`promote`, `state`, `progress`, `complete`) would operate on whichever entry
  sorts first — silently the wrong task. Merging text is not sufficient; the
  strategy has to make IDs unique across branches too.

## Requirements

- Ship a merge driver script that merges two versions of `todo.md` by `## ` entry,
  preserving the preamble and every entry's full field block.
- The driver resolves the two cases that actually occur: one side appended an
  entry the other does not have, and both sides added different entries. It must
  never silently drop a field, and it must not reorder entries that both sides
  agree on.
- Todo IDs must not collide across branches cut from the same base. Prefer making
  the ID itself collision-resistant at intake over repairing collisions at merge
  time: a repair that renumbers after promotion would break the ID a user has
  already been shown, while an ID derived deterministically from date + goal is
  stable on every branch that creates it. The numeric scheme stays as the
  fallback shape only if a deterministic suffix proves impractical.
- Ship a `.gitattributes` entry marking `TaskFlowDocs/todo.md` with that driver,
  and install the corresponding `merge.<driver>.driver` config from a hook so a
  fresh clone gets it without manual setup. The attribute belongs in the clone's
  `.git/info/attributes` rather than a tracked `.gitattributes`: it configures a
  tool only some clones have, and tracking it would put one user's choice into
  every other user's working tree.
- The install step is idempotent, repository-local (never `--global`), silent on
  success, and best-effort: it must not change the hook's exit code or context
  output.
- Document the strategy and its limits in the Skill and runtime reference: merge
  in a local clone, and expect a content conflict in the web UI.
- The driver must not attempt to merge entries both sides edited differently —
  that is a real conflict and must still surface as one.

## Acceptance Criteria

- With two branches each adding a Todo entry to `main`, `git merge` completes
  with no conflict and both entries present with all their fields.
- Two branches cut from the same base on the same day allocate **different** Todo
  IDs, and the merged file has no duplicate ID.
- A clone with no driver configured still gets an ordinary, resolvable conflict
  (no silent corruption, no error).
- Two branches that edit the same entry's `- Status:` differently still conflict.
- Re-running the install step twice leaves `git config --local` unchanged.
- `bash hooks/smoke-test` passes on all three CI runners.

## In Scope

- The merge driver script and its wiring (`.gitattributes` template shipped by the
  plugin, driver installation in `hooks/session-start` or a hook it calls).
- Todo ID allocation in `hooks/task` (the `intake` command), if the
  collision-resistant ID is adopted.
- `skills/taskflow/references/runtime.md`, `skills/taskflow/SKILL.md`, `README.md`,
  `README.zh-CN.md`.
- `hooks/smoke-test`.

## Out of Scope

- Any hosted-platform or branch-protection setting; the plugin cannot set those.
- Restructuring Todo into one file per entry. It removes the conflict by
  construction but changes the intake format, the artifact layout, seven hooks,
  and both reference documents, and it loses the single human-scannable list.
- Rewriting existing Todo history.

## Risks / Deferred Items

- The driver runs only when the user merges locally. A web-UI merge still
  conflicts; the documentation says so plainly.
- A driver script is executed by `git` on the user's machine. It must be a small,
  readable, POSIX-only script in the plugin, never a command fetched at runtime.
- If Todo's format ever changes, the driver is part of what must change with it;
  the smoke test pins the behavior so that drift fails loudly.

## Open Questions

- None blocking.

## Version History

- v1 — planning.