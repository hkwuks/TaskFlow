# Repository standards

This file is the entry point for repository-owned rules that apply alongside TaskFlow. Keep it short; link only the standards that exist and apply.

## Applicability

| Standard | File | Applies when |
| --- | --- | --- |
| Code | `code.md` | Editing or reviewing source code |
| Commits | `commits.md` | Creating commits, branches, or release notes |
| Design | `design.md` | Making architecture, UX, or API decisions |
| Development process | `development.md` | Planning, testing, review, or delivery |

Repositories may add more rows with narrower scope. An absent or unlinked file is not an error until that category applies to the current task. When it applies, TaskFlow guides the user to define the file or explicitly waive the category before implementation.

## Bootstrap questions

Ask at most three questions per turn, in dependency order, and recommend an answer for each. Default order: development process, code, commits/PR, design. Ask only categories relevant to the current task. After confirmation, create only the selected files; do not create empty placeholders. A waiver is recorded here and in the task `plan.md`.

Every standards file must contain: `Scope`, `Rules`, `Verification`, and `Exceptions / Change control`. `commits.md` must also contain `Commit format` and `PR checks`.

## Precedence

Apply applicable local standards before generic TaskFlow advice, except for safety requirements and explicit user instructions. If two rules conflict, stop and surface the conflict.

## Remote PR rules

When work targets a pull request or Git remote, inspect the configured remote and available repository-host guidance (for example contribution guides, PR templates, CODEOWNERS, branch/CI rules, and host metadata). Treat discovered rules as candidates until reviewed. Record the source, date, and incorporated conclusion here or in a linked note; never copy secrets, tokens, private data, or opaque payloads.

```yaml
remote_sync:
  status: not-run
  sources: []
  last_synced: null
```

If the remote is unavailable or permissions are insufficient, record `unavailable` and continue without claiming synchronization completed.
