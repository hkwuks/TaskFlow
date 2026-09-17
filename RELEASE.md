# Release process

This is the manual, auditable release checklist for TaskFlow. Do not create a tag, GitHub Release, or package publication until the release owner approves the release commit.

## Release scope

TaskFlow ships as a repository plugin for Codex and Claude Code. Keep these artifacts aligned:

- `.codex-plugin/plugin.json` — Codex manifest and development cachebuster;
- `.claude-plugin/plugin.json` — Claude Code manifest version;
- `.codebuddy-plugin/plugin.json` — CodeBuddy manifest and development cachebuster;
- `.claude-plugin/marketplace.json` and `.codebuddy-plugin/marketplace.json` — catalog entries pinned to the stable release tag and full commit SHA;
- `skills/taskflow/` and `hooks/` — plugin contents;
- README, governance documents, and release notes.

## Before release

Create a release TaskFlow task and confirm:

- target repository and base branch;
- clean working tree and approved release scope;
- intended changes are merged into the intended base (`main` by default);
- applicable `CONTRIBUTING.md`, `CODE_STYLE.md`, `ROADMAP.md`, and PR template are read;
- the version follows the approved repository decision.

The default path is a direct tag from the verified base commit; a `release/vX.Y.Z` branch and Release PR are optional when release-only documentation needs separate review or the owner requests a release candidate.

## Validation checklist

Run and record applicable results:

```bash
bash hooks/repository-check .
bash hooks/release-check .
bash hooks/smoke-test
python3 /home/hk/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/taskflow
git diff --check
```

`hooks/release-check` compares the version literals a release has to move — both
plugin manifests, the newest `CHANGELOG.md` section, and the `claude plugin list`
sample in each README — and confirms each marketplace `ref` resolves to the
commit its `sha` names. It exits `2` on a mismatch and `3` when a manifest is
missing.

Do not claim an unavailable check passed; record limitations in the release task.

## Release notes

Include the version and date, user-visible changes, migration or installation impact, known limitations, verification results, the release commit (and Release PR when used), and the TaskFlow task link. Do not include secrets or unverified claims.

## Tag and GitHub Release

After the release scope is merged to the intended base (or the optional Release PR is merged):

1. Check out the exact merged base commit and confirm a clean working tree.
2. Verify manifest versions and release notes again.
3. Create an annotated tag such as `vX.Y.Z`.
4. Push the tag only after explicit release-owner approval.
5. Create the GitHub Release from that tag with the approved notes.
6. Update both marketplace entries on `main` so each Git source uses the release tag as `ref` and the exact tagged commit as `sha`; then run `bash hooks/release-check .` and validate it with Claude Code, Codex, and CodeBuddy tooling before publishing the catalog change.
7. Record the tag, release URL, commit, marketplace pin, and checks in the release task.

Steps 3–6 make a release two commits, by construction: the tag cannot be created
before the release commit exists on the base, and the pinned `sha` cannot be
written before the tag exists. Claude Code verifies the pin at install time and
refuses a mismatch as `sha_pin_mismatch`, and it clones by the pinned commit
rather than by the tag, so the pin is what keeps an installation on the reviewed
release if the tag is ever moved. The second commit is the pin, not a mistake.

The marketplace catalog itself remains on `main` so refreshes can discover the latest stable entry. The plugin source must not point at moving `main`; local-directory marketplace registration remains the development path.

### Optional Release PR path

Use `release/vX.Y.Z` when the release needs an isolated documentation review, a release candidate, or an explicit PR approval. Merge that PR before applying the same tag and GitHub Release steps above.

TaskFlow does not push tags or create GitHub Releases automatically.

## Rollback

Stop distribution, record the affected tag/commit and impact, and prefer a corrective patch release. Deleting or moving a remote tag requires explicit owner authorization and a documented reason. Never rewrite shared branch history as a rollback.

## Known limitations

- The generic plugin validator may reject the existing Codex manifest `hooks` field even when Codex installation and TaskFlow smoke tests pass; record the discrepancy rather than deleting the hook declaration.
- `hooks/repository-check` is opt-in and does not mutate Git remotes or enforce release permissions.
- Release automation, package registries, signing, and provenance attestations are not configured by this document.
