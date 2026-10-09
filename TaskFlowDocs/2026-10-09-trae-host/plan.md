# Plan — Adapt TaskFlow to Trae IDE as a fifth host

> Task version: v1
> Status: in_progress

No spec required — small, self-contained task.

## Reference Pointers

- `TaskFlowDocs/repository-docs/index.md` — routing record; routes this task to
  `README.md`, `CONTRIBUTING.md`, `CODE_STYLE.md`, `RELEASE.md`, `CHANGELOG.md`.
- `CONTRIBUTING.md` — branch/worktree rule (followed: `.worktrees/2026-10-09-trae-host`
  on `docs/trae-host`) and the landing rule (a task's documents land inside its own
  pull request).
- `skills/taskflow/references/runtime.md` — the host/harness hook contract this
  change extends; its own rule is that a host contract is written from a
  measurement, which this change must state it does not have.
- `TaskFlowDocs/achieved/2026-09-19-dsh-host/spec.md` — the precedent for adding a
  host: additive per-host wiring file, shared hook scripts untouched, release
  literals and smoke fixtures updated.
- `docs.trae.cn` (read 2026-10-09): `ide_skills`, `ide_automate-actions-with-hooks`,
  `ide_hook-configuration-reference` — Trae's skill directory, hook config format,
  event I/O, and the Claude Code config import switch.
- `mnemon-dev/mnemon` (`internal/memory/setup/trae.go`, `assets/trae/`) and
  `wanshuiyin/Auto-claude-code-research-in-sleep` (`docs/TRAE_ARIS_RUNBOOK_CN.md`) —
  how other tools ship to Trae: copy into `.trae/`; no plugin publish path exists.

## Related Tasks

- dsh host addition (achieved 2026-09-19) — the same shape, one host earlier.

## Skills / Tools Used

- **PRD (requirements elicitation and framing):** `sxng` — invoked for the Trae
  host research; documentation retrieval is what framed the gap this PRD states
  (no plugin mechanism, user-scoped `.trae/` only). Recorded by
  `capability-evidence` as `invoke|sxng` and spent by the gate on `prd.md`.
- **Plan (work breakdown and task decomposition):** `agent-skills:plan` — invoked
  to decompose the change into the ordered steps below; its vertical-slice and
  acceptance-criteria shape is what Steps 1–4 use.
- **Spec:** not applicable — no `spec.md` for this task (small, self-contained);
  record it with `hooks/task unaided Spec --considered 'architecture and design
  specification'` rather than leaving the stage unaccounted for.

## Preconditions

- On `docs/trae-host` in `.worktrees/2026-10-09-trae-host` (done).
- Todo item `TF-20261009-369e77` promoted and linked (done).
- No live Trae host available (accepted in the PRD: the wiring ships unmeasured and
  says so).

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-10-09
- Approved version: v1
- Approved scope: ship `hooks/hooks-trae.json` wiring SessionStart and the
  pre-write gate pair, plus the Trae install documentation and host-list
  bookkeeping; no `.trae-plugin/`, no committed `.trae/`, no gate script changes.

## Steps

### Step 1 — Ship the Trae wiring file

- Goal: a Trae user can point `.trae/hooks.json` at TaskFlow's hooks and get the
  same SessionStart context, and the same pre-write capability gate, that Claude
  Code gets.
- Dependencies: none.
- Files: `hooks/hooks-trae.json` (new).
- Implementation checklist:
  - [ ] Write `hooks/hooks-trae.json` in Trae's own schema: `version: 1`, then
        `SessionStart` (matcher `startup`), `PreToolUse` (matcher `Write|Edit`),
        and `PostToolUse` (matcher `Skill`, plus `mcp__.*`), each a hook group with
        one `type: "command"` hook, a `timeout`, and a command that sets
        `CLAUDE_PROJECT_DIR` and runs `hooks/run-hook.cmd <script>`.
  - [ ] Reuse `session-start`, `capability-gate`, and `capability-evidence`
        unchanged — the file wires events, and no hook script gains a host branch.
  - [ ] Keep the description line parallel to the other wiring files and name Trae
        as a host that writes this file as `.trae/hooks.json`.
- Acceptance: the file parses as JSON, carries no plugin-root variable, matches the
  gate's tool names, and each command produces the shape its consumer reads.
- Verification: exercised by Step 4's smoke section; the gate and evidence scripts
  are unchanged, so `bash hooks/smoke-test`'s existing gate assertions still cover
  their behaviour.
- Rollback: delete the file; nothing else references it.
- Status: done

### Step 2 — Document the install in the three host-facing documents

- Goal: a Trae user has the exact commands, and prefers Trae's own hooks file over
  importing the Claude Code one.
- Dependencies: Step 1 (the file the commands reference must exist).
- Files: `hooks/README.md`, `README.md`, `README.zh-CN.md`.
- Implementation checklist:
  - [x] `hooks/README.md`: tree listing, one-JSON-per-host list, and a "Trae manual
            install" block beside the Codex/CodeBuddy manual-install blocks — skill
            copy into `.trae/skills/taskflow`, `.trae/hooks.json` from the shipped
            file, and the re-copy-after-update caveat.
  - [x] `hooks/README.md`: why there is no `trae plugin …` command, and Trae's
            "导入 CLAUDE 中的 Hooks 配置" switch named as the alternative with its
            opt-in caveat.
  - [x] `README.md`: an "Install with Trae" section in the same shape as the other
            per-host sections, plus the plugin/description line and the project map.
  - [x] `README.zh-CN.md`: the same three places, in Chinese.
- Acceptance: the commands run as written on a clean checkout (skill copy and hooks
  file both land), and the copy-after-update caveat is present.
- Verification: run the install commands in a scratch directory and confirm
  `.trae/skills/taskflow/SKILL.md` and `.trae/hooks.json` exist; then run the
  documented hook command by hand.
- Rollback: revert the three documents.
- Status: done

### Step 3 — Add Trae to every host list, and record the caveat

- Goal: no file claims TaskFlow supports exactly four hosts, and the unmeasured
  status is readable at the place the wiring is described.
- Dependencies: Step 1.
- Files: `ROADMAP.md`, `skills/taskflow/SKILL.md`, `package.json`,
  `skills/taskflow/references/runtime.md`.
- Implementation checklist:
  - [x] `ROADMAP.md`: direction sentence and host-parity priority.
  - [x] `skills/taskflow/SKILL.md`: the host/harness hooks sentence.
  - [x] `package.json`: `description`. Also `RELEASE.md`'s release-scope opening
            and a note that Trae carries no version literal to bump.
  - [x] `runtime.md`: Trae row in the "Supported hosts" table, a Trae column in the
            event map (SessionStart → `hookSpecificOutput.additionalContext`;
            the gate wired, unlike Codex/CodeBuddy/dsh; no launcher needed but
            `bash` spelled explicitly), the install note in the paragraph that lists
            per-host install commands, the folder-layout entry, and move the gate's
            "Claude Code only" sentence to name Claude Code and Trae.
  - [x] `runtime.md`: "Trae specifics" subsection beside "CodeBuddy specifics", stating: the `.trae/` file locations, `source` is always
            `startup`, `CLAUDE_PROJECT_DIR`/`TRAE_PROJECT_DIR` are injected but no
            plugin-root variable is, that Trae reads Claude Code hook configs behind
            an opt-in switch, and — separately and plainly — that none of it has run
            on a live host, naming the read date and the one thing the tester must
            check first (`PreToolUse`/`PostToolUse` field names reaching the gate and
            the evidence recorder).
- Acceptance: `grep -ri trae` shows Trae wherever the other hosts are enumerated;
  the caveat is in the same subsection as the claims it qualifies.
- Verification: `grep -rn "CodeBuddy" --include='*.md' .` and check every hit has a
  Trae counterpart or a stated reason it does not.
- Rollback: revert the four files.
- Status: done

### Step 4 — Pin the wiring with one smoke section

- Goal: deleting the file, dropping the repository-root variable, or losing an
  event's expected output shape fails the suite.
- Dependencies: Step 1.
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] A section modeled on the dsh one: read the four commands out of
        `hooks-trae.json`, require each to name `<TASKFLOW_ROOT>`, substitute the
        checkout, and run each with `CLAUDE_PROJECT_DIR` set.
  - [x] SessionStart's output carries `hookSpecificOutput` and a matching
        `hookEventName`.
  - [x] The wired event/matcher set is asserted, so an edit cannot silently drop the
        gate: `SessionStart`/`startup`, `PreToolUse`/`Write|Edit`,
        `PostToolUse`/`Skill`, `PostToolUse`/`mcp__.*`, and the command count.
  - [x] The gate's PreToolUse fixture runs through the Trae-resolved command and must
        deny; a recorded `Skill` invocation must then release it.
  - [x] Mutations checked one at a time in this worktree: file deleted → names it;
        `CLAUDE_PLUGIN_ROOT` prefix stripped → names it; `PreToolUse` entry dropped →
        names it; an `mcp__.*` matcher changed → names it.
- Acceptance: the section prints `ok` on the unmodified tree and fails on each
  mutation.
- Verification: `bash hooks/smoke-test` from the task worktree exits 0; then apply
  each mutation in a scratch copy and confirm the failure message names it.
- Rollback: remove the section.
- Status: done

## Checkpoints

- After Step 2: run the documented Trae install end to end in a scratch directory,
  including the hook command by hand. This is the only check that exercises the
  instructions a user will follow, so it gates Step 3.
- After Step 4: `bash hooks/smoke-test`, `bash hooks/release-check .`, and
  `git diff --check` all clean, then read the diff once for host-list completeness.

## Verification / Review

| What | Command | Result |
| --- | --- | --- |
| Smoke suite | `bash smoke-test` from `hooks/` | `ALL SMOKE PASSED`, including the new Trae section |
| Release literals | `bash hooks/release-check .` | `STATUS: pass` |
| Trae wiring section, mutated | file deleted; `CLAUDE_PLUGIN_ROOT` prefix stripped; `PreToolUse` entry dropped; `mcp__.*` matcher changed | each failed with a message naming the mutation — run one at a time, file restored from a copy between runs |
| Documented install | the `hooks/README.md` commands, in a scratch git project | `.trae/skills/taskflow/SKILL.md` + `.trae/hooks.json` created; `events: SessionStart, PreToolUse, PostToolUse` |
| Documented install, hooks run | each of the four commands run against that project with `CLAUDE_PROJECT_DIR`/`TRAE_PROJECT_DIR` set, as Trae would | SessionStart emitted the nested `hookSpecificOutput.additionalContext`; the gate denied `prd.md`; a `Skill` PostToolUse recorded `invoke|trae:probe`; the next gate call released |
| Whitespace | `git diff --check` | clean |
| JSON | `python3 -c "json.load(...)"` over `hooks/hooks-trae.json` | parses |
| Host lists | `grep -rn "CodeBuddy"` over the tree | every enumeration now names Trae; `CHANGELOG.md` and `TaskFlowDocs/achieved/**` left untouched as historical records |
| CI | the `Hooks` workflow on the pushed branch | **not run** — no push from this session |

## Change Log

- 2026-10-09 — Trae wired to SessionStart **and** the pre-write gate pair, on the
  user's decision. The gate was originally deferred as unmeasurable; the user's
  reading is that Trae's documented `PreToolUse`/`PostToolUse` shapes carry it, so
  the initial scope was raised before implementation.
- 2026-10-09 — `hooks-trae.json`'s SessionStart command must set
  `CLAUDE_PLUGIN_ROOT` itself: Trae injects `CLAUDE_PROJECT_DIR` and no plugin
  root, and that variable alone selects the nested context field. Found by running
  the wiring, not by reading the docs — the first version produced a top-level
  `additionalContext` that Trae would have discarded silently.
- 2026-10-09 — the smoke section reads commands out of the JSON, so it strips the
  JSON `\"` escaping; without that, every command failed with `not found` on a path
  that exists.

## Follow-ups

- Run `hooks-trae.json` on a machine with Trae (the user has one) and either correct
  the file or replace the runtime caveat with the measurement. Check the gate and
  the recorder first: a denial that never fires and an evidence line that never
  records are both silent by design, and `tool_input`'s field names on Trae are the
  one documented-for-Claude-Code detail the gate depends on.
- The Windows command spelling (`& '<path>\hooks\run-hook.cmd'`, and the
  `$env:CLAUDE_PLUGIN_ROOT=…;` prefix) is PowerShell knowledge, not Trae knowledge.
  It is written in `hooks/README.md` but never executed; a Windows Trae machine
  would settle it.

## Version History

- v1 — planning.
