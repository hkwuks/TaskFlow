# Plan — Adapt TaskFlow to the DeepSeek Harness (dsh) as a fourth host: ship a dsh plugin
> Task version: v1
> Status: in_progress

## Spec Pointers

- `spec.md`

## Reference Pointers

- `TaskFlowDocs/2026-09-19-dsh-host/prd.md` — the confirmed facts this plan builds on.

## Related Tasks

None.

## Skills / Tools Used

- **Skill (taskflow)** — the workflow itself: Todo intake, promote, PRD/Spec/Plan, this approval gate.
- **Explore subagents (2, during planning)** — surveyed dsh's skill-provider registry and its lifecycle extension points before anything was designed. Their findings set the scope of what dsh could support.
- **Direct execution against the installed dsh** — every fact in the PRD's "Background / Confirmed Facts" came from a probe against `dsh 0.1.5-rc.2` in a throwaway profile, not from reading documentation.
- **Unaided** — the composition search, the `baseUrl` measurement, and the mount-API comparison were each a single scripted probe; no capability beyond Bash was used to establish them.

## Preconditions

- dsh 0.1.5-rc.2 installed and resolvable on `PATH` (`dsh --version` → `0.1.5-rc.2`).
- Working on `feature/dsh-host` in the worktree `.worktrees/dsh-host`.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-19 19:29 +08:00
- Approved version: v1
- Approved scope: PRD / Spec / Plan

## Steps

### Step 1 — Ship the dsh bundle and verify it at the composition and seam layers

- Goal: A dsh user installs TaskFlow with one command and gets the skill and the
  SessionStart hook, with no hand-written profile YAML.
- Dependencies: none; this is the whole task.
- Files:
  - add `package.json` (repo root)
  - add `dsh/index.js`
  - add `dsh/cordis.patch.yml`
  - add `hooks/hooks-dsh.json`
  - edit `README.md`, `README.zh-CN.md`, `hooks/README.md`,
    `skills/taskflow/references/runtime.md`, `ROADMAP.md`
  - edit `RELEASE.md`, `hooks/release-check`, `CHANGELOG.md`, `hooks/smoke-test`
- Implementation checklist:
  - [x] Root `package.json`: `dsh-taskflow`, `type: module`, `main`,
        `exports`, `files`, `dsh.bundle.patch`; no `dependencies`.
  - [x] `dsh/cordis.patch.yml`: one insert of the `taskflow` row.
  - [x] `dsh/index.js`: `name` / `inject` / `apply`, mounting
        `dsh-skill-filesystem` and `dsh-hooks-claude-code` via
        `ctx.loader.import` + `ctx.plugin`, with both paths derived from
        `import.meta.url`.
  - [x] `hooks/hooks-dsh.json`: the bridge's config shape, matcher without
        `fork`, command carrying a `CLAUDE_PLUGIN_ROOT` prefix.
  - [x] Docs: add dsh to every host list and per-host wiring table.
  - [x] Release literals: add the root manifest to the set `release-check`
        compares, to `RELEASE.md`, to the `smoke-test` release fixture, and
        write the `CHANGELOG.md` entry.
  - [x] Run the verification below.
- Acceptance: the five checks in "Verification" pass.
- Verification:
  1. `dsh --profile <throwaway> --dump-config` → exit 0 and the TaskFlow row.
  2. Boot that profile; the mounted provider's `list()` returns exactly
     `taskflow`.
  3. dsh's own `matchesMatcher` accepts the matcher for each of
     `startup|resume|clear|compact` and rejects a non-source.
  4. dsh's own `parseHookOutput` reads the hook's real stdout back as
     SessionStart context.
  5. `bash hooks/smoke-test` and `bash hooks/release-check .` → exit 0.
- Rollback: `git checkout .worktrees/dsh-host` for the edits and delete the four
  added files. Nothing outside the worktree was touched; the throwaway dsh
  profile used for verification is removed at the end of the step.
- Status: done

## Checkpoints

- After Step 1's checklist but before verification: the four added files exist
  and `node --check`-style import of `dsh/index.js` succeeds.

## Verification / Review

- 2026-09-19 Step 1: 1. dsh --profile tfadd --dump-config -> exit 0, row 'taskflow / dsh-taskflow' present. 2. Booting that profile with an independent observer plugin listed exactly ['taskflow|taskflow|custom']. 3. dsh's own matchesMatcher accepted startup|resume|clear|compact, rejected fork|end|(empty). 4. dsh's own parseHookOutput read the hook's real stdout as 397 chars of SessionStart context; two negative controls (wrong event name; env prefix removed) both lost the context. 5. bash hooks/smoke-test -> ALL SMOKE PASSED; bash hooks/release-check . -> STATUS: pass; bash hooks/repository-check . -> needs-user-input (uncommitted task dir, expected).

Recorded in Step 1. Note explicitly what is **not** covered: no live model turn,
so a failure that only appears at the model seam is out of reach of this
verification. The seam test narrows that gap by driving dsh's real parser.

## Change Log

- v1 — the task as approved.

## Follow-ups

- Windows verification of the dsh host, which is untested here.
- A live end-to-end run against a real model, which needs an API call and was
  excluded by the approved scope.

## Version History

- v1 — approved.
