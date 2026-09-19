# Adapt TaskFlow to the DeepSeek Harness (dsh) as a fourth host: ship a dsh plugin
> Task version: v1
> Status: completed

## Goal

Adapt TaskFlow to the DeepSeek Harness (dsh) as a fourth host: ship a dsh plugin bundle that self-wires the existing skill and hooks with no manual config

## Background / Confirmed Facts

Each fact below was established by running the installed dsh 0.1.5-rc.2, not by
reading documentation alone. Probe profiles and probe packages lived outside the
repository and were removed after use.

- **dsh has a first-party Claude Code hook bridge.** `@deepseek-ai/dsh-hooks-claude-code`
  ships inside the dsh installation closure and runs a Claude Code `hooks.json`
  on dsh's own interception seams (`agent/session-start`, `agent/pre-step`,
  `tools/pre-execute`, `tools/post-execute`, `agent/turn-stopping`). It is
  present but mounted by no shipped bundle.
- **The bridge parses only the nested context shape.** Its codec reads
  `hookSpecificOutput.additionalContext`, guarded by a matching
  `hookEventName`; a top-level `additionalContext` is discarded silently.
  `hooks/session-start` emits the nested shape only when `CLAUDE_PLUGIN_ROOT` is
  set in its environment.
- **The bridge does not export `CLAUDE_PLUGIN_ROOT`.** It substitutes
  `${CLAUDE_PLUGIN_ROOT}` inside the `command` string at config-parse time and
  exports only `CLAUDE_PROJECT_DIR`. Verified in `dsh-hooks-claude-code`'s
  `substituteCommand` and `runPoint`.
- **A patch's `baseUrl` is the profile directory, not the plugin's.** Measured
  with a `!!js` expression: `baseUrl` is `file:///home/hk/.dsh/profiles/<name>/`
  for bundle layers and for the user layer alike. A patch therefore cannot name
  its own package's files without help.
- **A plugin module can name them.** `fileURLToPath(new URL('../', import.meta.url))`
  resolves the installed package root from inside the module — the idiom
  `@deepseek-ai/dsh-skill-badge` uses for its assets.
- **`ctx.loader.import(name)` resolves from the profile directory.**
  `$DSH_HOME/profiles/node_modules` is an ancestor of every profile directory, so
  the installation's dependency closure (including the hook bridge and
  `dsh-skill-filesystem`) is reachable by bare name. A plain `import(name)` from
  the plugin's own file URL is **not** — the plugin is linked out of tree.
- **A plugin can mount its contributions from `apply()`.** Verified: inside a
  bundle plugin's `apply`, `await ctx.loader.import('@deepseek-ai/dsh-skill-filesystem')`
  followed by `ctx.plugin(mod, config)` raised a filesystem provider whose only
  listed skill was `taskflow`; the same shape mounted `dsh-hooks-claude-code`
  without error. `ctx.loader.create()` does **not** work there — it needs a
  loader fiber and fails with `cannot create effect on inactive context`.
- **dsh's `SessionStartSource` is `startup | resume | clear | compact`.** There is
  no `fork`.
- **The shell seam runs `bash -c <command>`.** A `VAR=value bash script` prefix in
  the command string therefore works.
- **`dsh plugin --profile <p> add <path>` links the package into the profile and
  appends it to `dsh.profile.bundles`** when its `package.json` declares
  `dsh.bundle.patch`. Verified end to end against a throwaway profile.

## Requirements

1. A dsh user installs TaskFlow with one command and gets the skill and the
   SessionStart hook with no hand-written profile YAML.
2. The skill is the repository's single `skills/taskflow`, discovered through
   dsh's own filesystem provider so frontmatter, `resourceBase`, and watching
   behave as dsh users expect.
3. SessionStart injects the same state summary every other host injects.
4. The existing three hosts and the hook scripts themselves are unchanged in
   behaviour. No host-specific branch is added to a hook script.
5. No language runtime beyond Node is added to the repository's own tooling; the
   hook scripts remain POSIX shell plus awk.

## Acceptance Criteria

- `dsh --profile <p> --dump-config` on an installed profile shows the TaskFlow
  row, composited at exit 0.
- A boot of that profile mounts a skill provider that lists exactly `taskflow`.
- `hooks/session-start`, run the way the bridge runs it, produces a
  `hookSpecificOutput.additionalContext` that dsh's own `parseHookOutput` reads
  back as SessionStart context.
- `bash hooks/smoke-test` passes.
- The release literals still agree under `bash hooks/release-check .`.

## In Scope

- Root `package.json` declaring `dsh.bundle.patch`.
- `dsh/index.js` — the plugin module.
- `dsh/cordis.patch.yml` — the bundle patch layer.
- `hooks/hooks-dsh.json` — the dsh wiring file.
- Host lists and per-host wiring tables in `README.md`, `README.zh-CN.md`,
  `hooks/README.md`, `skills/taskflow/references/runtime.md`, `ROADMAP.md`.
- The release-literal set: `RELEASE.md`, `hooks/release-check`,
  `CHANGELOG.md`, and the `hooks/smoke-test` release-check fixture.

## Out of Scope

- Publishing to npm, pushing, tagging, or opening a pull request.
- A live agent run against a real model. Verification stops at the composition
  layer (the composed tree) and the seam layer (dsh's own parser and matcher).
- Claude Code hook events with no TaskFlow hook today (`PreToolUse`,
  `PostToolUse`, `UserPromptSubmit`, `Stop`).
- Windows-specific wiring. dsh's own Windows story is unverified here.

## Risks / Deferred Items

- **No live run.** A mounted plugin that fails at the model seam — a bad
  `additionalContext`, a hook that times out — cannot be caught without an API
  call. The seam test exercises the parser directly to narrow the gap.
- **`ctx.loader.import` is an internal-ish API.** It is how dsh's own
  `loadProfileDirectory` mounts nested entries, so it is not private to the
  launcher, but it is not in a documented plugin-authoring surface either.
- **Duplicate skill provider names.** If a future dsh preset registers a provider
  named `taskflow`, `registerProvider` throws. The provider name is set
  explicitly so the collision would be visible and attributable.
- **The package name is unclaimed on npm**, so a future publish is possible but
  not done here.

## Open Questions

None.

## Version History

- v1 — planning.
