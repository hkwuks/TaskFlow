# Release process

This is the manual, auditable release checklist for TaskFlow. Do not create a tag, GitHub Release, or package publication until the release owner approves the release commit.

## Release scope

TaskFlow ships as a repository plugin for Codex and Claude Code. Keep these artifacts aligned:

- `.codex-plugin/plugin.json` — Codex manifest and development cachebuster;
- `.claude-plugin/plugin.json` — Claude Code manifest version;
- `skills/taskflow/` and `hooks/` — plugin contents;
- README, governance documents, and release notes.

## Before release

Create a release TaskFlow task and a short-lived branch from the intended base. Confirm:

- target repository and base branch;
- clean working tree and approved release scope;
- intended changes are merged into the release branch;
- applicable `CONTRIBUTING.md`, `CODE_STYLE.md`, `ROADMAP.md`, and PR template are read;
- the version follows the approved repository decision.

The release PR must be merged before tagging. Use a branch such as `release/vX.Y.Z` for a release candidate.

## Validation checklist

Run and record applicable results:

```bash
bash hooks/repository-check .
bash hooks/smoke-test
python3 /home/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/taskflow
git diff --check
```

Verify both manifests report the intended version:

```bash
python3 - <<'PY'
import json
for path in ('.codex-plugin/plugin.json', '.claude-plugin/plugin.json'):
    with open(path, encoding='utf-8') as handle:
        data = json.load(handle)
    print(path, data['name'], data['version'])
PY
```

Do not claim an unavailable check passed; record limitations in the release task.

## Release notes

Include the version and date, user-visible changes, migration or installation impact, known limitations, verification results, the release PR, and the TaskFlow task link. Do not include secrets or unverified claims.

## Tag and GitHub Release

After the release PR is merged:

1. Check out the merged base commit and confirm a clean working tree.
2. Verify manifest versions and release notes again.
3. Create an annotated tag such as `v1.0.3`.
4. Push the tag only after explicit release-owner approval.
5. Create the GitHub Release from that tag with the approved notes.
6. Record the tag, release URL, commit, and checks in the release task.

TaskFlow does not push tags or create GitHub Releases automatically.

## Rollback

Stop distribution, record the affected tag/commit and impact, and prefer a corrective patch release. Deleting or moving a remote tag requires explicit owner authorization and a documented reason. Never rewrite shared branch history as a rollback.

## Known limitations

- The generic plugin validator may reject the existing Codex manifest `hooks` field even when Codex installation and TaskFlow smoke tests pass; record the discrepancy rather than deleting the hook declaration.
- `hooks/repository-check` is opt-in and does not mutate Git remotes or enforce release permissions.
- Release automation, package registries, signing, and provenance attestations are not configured by this document.
