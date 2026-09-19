import { fileURLToPath } from 'node:url'

// This module's own location in the installed package. A patch's `baseUrl` is the
// *profile* directory, so `cordis.patch.yml` cannot name the files that ship
// beside it; a module inside the package is the only thing that can say where the
// package is. Everything below is derived from here for that reason.
const PACKAGE_ROOT = fileURLToPath(new URL('../', import.meta.url))

/** Skill root holding this repository's one skill. */
const SKILLS_DIR = fileURLToPath(new URL('../skills/', import.meta.url))

/** Claude Code-shaped hook config, read only by the dsh bridge below. */
const HOOKS_CONFIG = fileURLToPath(new URL('../hooks/hooks-dsh.json', import.meta.url))

/** Cordis plugin name. */
export const name = 'taskflow'

/** The loader that mounts the two contributions below. */
export const inject = ['loader']

/**
 * Mount TaskFlow's two contributions as loader entries.
 *
 * Both are dsh's own packages rather than implementations of our own: the
 * filesystem skill provider already owns frontmatter parsing, watching, and
 * catalog caching, and the Claude Code bridge already owns the matcher and the
 * output codec. Re-implementing either would duplicate dsh and then drift from it.
 *
 * `ctx.loader.import` rather than a bare `import()`: this package is linked into
 * the profile from outside it, so Node's parent walk from here never reaches the
 * profile's `node_modules`, where dsh's own packages are. The loader resolves
 * from the profile directory, so it finds them.
 *
 * `ctx.plugin` rather than `ctx.loader.create`: `create` needs a loader fiber and
 * fails on this plugin's own context with "cannot create effect on inactive
 * context".
 */
export async function apply(ctx) {
  const mount = async (specifier, config) => {
    ctx.plugin(await ctx.loader.import(specifier), config)
  }

  await mount('@deepseek-ai/dsh-skill-filesystem', {
    // A distinct provider name, so a collision names TaskFlow rather than
    // "filesystem". One instance per provider is what dsh's registry expects.
    providerName: 'taskflow',
    // Contribute this package's skills and nothing else: dsh's own
    // skill-filesystem row still serves the user's project and home roots, and a
    // skill appearing in both catalogs would be listed twice.
    includeDefaultRoots: false,
    customSkillDirs: [SKILLS_DIR]
  })

  await mount('@deepseek-ai/dsh-hooks-claude-code', {
    configPath: HOOKS_CONFIG,
    // Substituted into the hook command string; the bridge does not export it.
    pluginRoot: PACKAGE_ROOT
    // `projectDir` is left unset so hooks run in the session workspace, which is
    // what every other host does.
  })
}
