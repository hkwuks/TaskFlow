# Spec — Adapt TaskFlow to the DeepSeek Harness (dsh) as a fourth host: ship a dsh plugin
> Task version: v1

## Objective and Success Criteria

Deliver a dsh **bundle package** at the repository root that, once installed into
a dsh profile, contributes TaskFlow's two existing artifacts — `skills/taskflow`
and the SessionStart hook — without the user editing any dsh YAML.

Success is measured in three layers, in increasing strength:

1. **Composition.** `dsh --profile <p> --dump-config` exits 0 and the composed
   tree names the TaskFlow row.
2. **Mount.** Booting the plugin raises a skill provider that lists exactly
   `taskflow`, and mounts the hook bridge with TaskFlow's config file.
3. **Seam.** dsh's own `parseHookOutput` reads `hooks/session-start`'s stdout as
   SessionStart context, under a matcher dsh's own matcher accepts.

A live model turn is explicitly not part of the measurement.

## Architecture Boundaries and Responsibilities

```text
dsh (harness)                     TaskFlow (this repository)
──────────────                    ──────────────────────────
profile package.json   ──names──► dsh.bundle.patch
app-boot               ──reads──► dsh/cordis.patch.yml   (inserts one row)
cordis loader          ──imports► dsh/index.js           (mounts two children)
ctx.loader.import      ──finds───► dsh-skill-filesystem   (dsh's own package)
                                   dsh-hooks-claude-code  (dsh's own package)
                                                │
                                                ├─► skills/taskflow   (existing)
                                                └─► hooks/hooks-dsh.json ─► hooks/session-start (existing)
```

TaskFlow owns: the package manifest, the patch layer, the plugin module, and the
Per-host hook wiring file. TaskFlow does **not** own the skill discovery
mechanism, the hook interception seams, or the hook config format — it borrows
dsh's own for each.

**Why the patch only inserts one row.** A patch's `baseUrl` is the *profile*
directory, so no patch can name the files of the package that carries it. All
path-dependent configuration therefore lives in `dsh/index.js`, which alone knows
its own location. The patch's remaining job — declaring the plugin to the loader —
is exactly what YAML is for.

**Why the plugin mounts dsh's own packages rather than shipping its own.** The
skill provider and the hook bridge are both first-party dsh packages present in
every installation's dependency closure. Re-implementing either inside TaskFlow
would duplicate dsh's frontmatter parsing, watching, matcher semantics, and codec
— and would drift from them.

## Project Structure / Affected Files

Added:

```text
package.json                       # repo root: name, type, exports, dsh.bundle.patch
dsh/index.js                       # the cordis plugin module
dsh/cordis.patch.yml               # the bundle patch layer (one insert)
hooks/hooks-dsh.json               # SessionStart wiring for dsh
```

Modified — host lists and per-host wiring:

```text
README.md                          # host list, install section, tree, comparison table
README.zh-CN.md                    # the same three places
hooks/README.md                    # wiring-file table and the per-host install notes
skills/taskflow/references/runtime.md   # the host wiring table
ROADMAP.md                         # the "parity between hosts" objective
```

Modified — release literals:

```text
RELEASE.md                         # the list of version-carrying files
hooks/release-check                # the literal set it compares
CHANGELOG.md                       # the new version section
hooks/smoke-test                   # the release-check fixture's file set
```

Untouched: every hook script, `skills/taskflow/SKILL.md`, the three existing host
manifest directories, and `hooks/hooks.json` / `hooks-codex.json` /
`hooks-codebuddy.json`.

## Interfaces, Data Flow, and Contracts

**`package.json` (root, new).** The repository has no root manifest today, so one
is introduced. Fields that matter:

- `"name": "dsh-taskflow"` — the name `dsh plugin add` records and the loader
  imports. Verified unclaimed on the public registry.
- `"type": "module"` and `"main": "dsh/index.js"` — how the loader reaches the
  plugin module. No `exports` map: dsh resolves the bundle by directory and reads
  the manifest as a file, so a map only adds a way to break the resolution.
- `"dsh": { "bundle": { "patch": "./dsh/cordis.patch.yml" } }` — the single
  self-activation marker `dsh plugin add` and `dsh --profile` both read.
- No `dependencies`. The two packages the plugin mounts are resolved through the
  profile, not through this package.
- `"version"` mirrors the Claude Code manifest's release number and carries no
  cachebuster, so a future publish stays possible.

**`dsh/cordis.patch.yml`.** One insert:

```yaml
- insert:
    - id: taskflow
      name: dsh-taskflow
```

**`dsh/index.js`.** Exports `name` (`taskflow`), `inject` (`['loader']`), and an
async `apply(ctx)` that:

1. derives the package root from `import.meta.url`;
2. `await ctx.loader.import('@deepseek-ai/dsh-skill-filesystem')` then
   `ctx.plugin(...)` with `providerName: 'taskflow'`, `includeDefaultRoots: false`,
   and `customSkillDirs: [<package>/skills]`;
3. `await ctx.loader.import('@deepseek-ai/dsh-hooks-claude-code')` then
   `ctx.plugin(...)` with `configPath: <package>/hooks/hooks-dsh.json` and
   `pluginRoot: <package root>`.

`ctx.loader.import` rather than a bare `import()` because the package is linked
out of tree: Node's resolver walks up from the package directory and never
reaches the profile, while the loader resolves from the profile directory where
the installation closure *is* reachable.

`ctx.plugin` rather than `ctx.loader.create` because `create` needs a loader
fiber and fails on the plugin's own context.

**`hooks/hooks-dsh.json`.** The Claude Code shape the bridge parses, with two
differences from `hooks/hooks.json`:

- the matcher drops `fork` — dsh's `SessionStartSource` has no such value;
- the command sets `CLAUDE_PLUGIN_ROOT` in the hook process's environment.

That second point is the whole reason a separate file exists. `hooks/session-start`
selects its output shape by environment, emitting the nested
`hookSpecificOutput.additionalContext` only when `CLAUDE_PLUGIN_ROOT` is set. The
bridge substitutes that token inside the command *string* but does not export it,
so without the `VAR=value` prefix the hook takes its fallback branch and dsh's
codec discards the context. The prefix is `VAR=value bash script`, which the
bridge's `bash -c` seam honours.

## Invariants and Compatibility

- **No hook script gains a host branch.** The dsh wiring file adapts to the
  scripts, not the other way round. `hooks/session-start` is byte-identical.
- **No new runtime dependency for the repository's own tooling.** The root
  `package.json` declares none. The plugin's three imports (`node:url`, and the
  two packages dsh itself supplies) are satisfied by the dsh installation.
- **The existing three hosts are unaffected.** `hooks/hooks.json`,
  `hooks-codex.json`, and `hooks-codebuddy.json` are not edited; the dsh file is
  additive and read only by dsh.
- **Byte-for-byte hook behaviour is preserved**, which `bash hooks/smoke-test`
  and `tools/fixture-compare` continue to assert.
- **One writable surface per file.** The new files are read-only to the hooks:
  nothing outside `dsh/index.js` and `dsh/cordis.patch.yml` is loaded by dsh, and
  neither writes.

## Validation and Error Semantics

| Layer | Command | Pass |
|---|---|---|
| Composition | `dsh --profile <p> --dump-config` | exit 0, the TaskFlow row present |
| Mount | boot the profile; read the provider's `list()` | exactly `['taskflow']` |
| Seam (matcher) | dsh's `matchesMatcher` over the matcher and each dsh source | `startup`/`resume`/`clear`/`compact` match; nothing else |
| Seam (codec) | dsh's `parseHookOutput` over the hook's real stdout | the nested context is read back |
| Repository | `bash hooks/smoke-test`, `bash hooks/release-check .` | exit 0 |

Error semantics the plugin inherits rather than implements:

- A missing `hooks/hooks-dsh.json` makes the bridge log a warning and register no
  hooks; the agent still starts.
- A hook that fails to run is logged; the agent continues.
- A duplicate skill provider named `taskflow` throws at registration, naming the
  collision.

## Code and Test Constraints

- `dsh/index.js` is the repository's only JavaScript. It uses `node:` builtins
  and nothing else; no build step, no bundler, no TypeScript.
- Comments state why a choice was made where the reason is not in the code — the
  `ctx.loader.import` and `ctx.plugin` choices in particular. They do not restate
  what dsh does.
- No compatibility shim for older dsh versions. The plugin targets the
  installation it is installed into.
- Verification drives the **installed** dsh: its `--dump-config`, its
  `parseHookOutput`, its `matchesMatcher`. No dsh behaviour is re-implemented in
  a test.

## Design Decisions and Alternatives

**Chosen: a plugin module that mounts dsh's own packages.**

- *Alternative — a self-contained skill provider in `dsh/index.js`.* Rejected:
  duplicates dsh's frontmatter parsing and resource handling, and loses watching
  and cache invalidation. `dsh-skill-badge` shows the shape works, but only for a
  single hard-coded candidate; TaskFlow's skill has a `references/` directory and
  frontmatter that the filesystem provider already understands.
- *Alternative — enable the profile's disabled `skill-filesystem` row with
  `customSkillDirs`.* Rejected: it is a profile-directory path, so the bundle
  cannot ship it; the user would hand-write it, defeating self-wiring. Verified to
  work, so this remains the documented manual fallback.
- *Alternative — three `!!js` expressions in the patch, no plugin module.*
  Rejected: three copies of the same `createRequire` dance, uncommentable and
  unreviewable, to avoid fifteen lines of legible code.
- *Alternative — patch rows only, no code.* Impossible: `baseUrl` is the profile
  directory, so the patch cannot name its own package's files.

**Chosen: mount via `ctx.loader.import` + `ctx.plugin`.**

- *Alternative — `ctx.loader.create({id, name, config})`.* Rejected on evidence:
  fails with `cannot create effect on inactive context` from inside `apply`.
- *Alternative — a bare `import('@deepseek-ai/dsh-skill-filesystem')`.* Rejected
  on evidence: the package is linked out of tree, so Node's parent walk never
  reaches the profile.

**Chosen: a separate `hooks/hooks-dsh.json`.**

- *Alternative — reuse `hooks/hooks.json`.* Rejected: without the
  `CLAUDE_PLUGIN_ROOT` prefix the hook's output is silently discarded, and adding
  that prefix to the shared file would change what the other hosts run.
- *Alternative — teach `hooks/session-start` about dsh via an environment probe.*
  Rejected: it puts a host branch in the shared script and cannot distinguish dsh
  from a Claude Code installation that merely lacks the variable.

## Open Questions

None.
