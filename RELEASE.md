# Release process

This is the manual, auditable release checklist for TaskFlow. Do not create a tag, GitHub Release, or package publication until the release owner approves the release commit.

**This procedure is executed directly, on the base checkout.** A release does not create a TaskFlow task or a `todo.md` item, does not take a branch or a working tree, and does not write a PRD, Spec, or Plan — the repository's task workflow plans work that does not exist yet, and a release ships what is already merged. A release that also changes the plugin is development work; do that part under TaskFlow first, then release what merged. The record of a release is its `CHANGELOG.md` section and its GitHub Release body, both written below.

The approval gate comes with the procedure instead of with a Plan's `## Approval` block: the release owner approves the release commit before step 5 pushes, and that approval is what the release notes and the catalog pin stand on. Never push a tag or open a GitHub Release that the owner has not approved.

## Release scope

TaskFlow ships as a repository plugin for Claude Code, Codex CLI, CodeBuddy, and dsh. Keep these artifacts aligned:

- `.codex-plugin/plugin.json` — Codex manifest and development cachebuster;
- `.claude-plugin/plugin.json` — Claude Code manifest version;
- `.codebuddy-plugin/plugin.json` — CodeBuddy manifest and development cachebuster;
- `package.json` — the dsh bundle manifest (its `dsh.bundle.patch` is what makes the repository root installable as a dsh plugin);
- `.claude-plugin/marketplace.json` and `.codebuddy-plugin/marketplace.json` — catalog entries pinned to the stable release tag and full commit SHA;
- `skills/taskflow/` and `hooks/` — plugin contents;
- README, governance documents, and release notes.

Six of those files carry a version literal, eight in all: the four manifests, and
the two `plugin list` samples in each README. Seven of the eight are transcription
of one approved version string, so `hooks/release-version` writes them in a single
call:

```bash
bash hooks/release-version X.Y.Z
```

It checks before it writes, so a refusal leaves every file untouched, and it
refuses until the `CHANGELOG.md` section exists — see the ordering rule under
Release notes. It never creates a tag, pushes, or publishes anything; the two
manual steps below stay manual.

## Before release

Open the release from the base checkout and confirm:

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
python3 <skill-creator>/scripts/quick_validate.py skills/taskflow   # <skill-creator> is wherever that checkout lives
git diff --check
```

`hooks/release-check` compares the version literals a release has to move — the
three host manifests, the dsh bundle manifest, the newest `CHANGELOG.md` section,
and **every** `plugin list` sample in each README, not just the first one — and
confirms each marketplace `ref` resolves to the commit its `sha` names. It also
fails when the range from the tagged commit to the commit that recorded the pin
contains a change outside the two marketplace catalogs (paths under
`TaskFlowDocs/` are exempt), because such a change would ship under the pin
without being in the release commit the tag names. It exits `2` on a mismatch and
`3` when a manifest is missing.

The dsh bundle manifest carries no cachebuster. dsh installs the package through
pnpm rather than through a host-side plugin cache, so there is no stale-copy
failure for a suffix to defeat; bump its `version` with the others.

Do not claim an unavailable check passed; record limitations in the release notes.

## Release notes

The release notes are the record: the `CHANGELOG.md` section and the GitHub Release body carry it, and no other document is written for the release.

Include the version and date, user-visible changes, migration or installation impact, known limitations, verification results, and the release commit (and Release PR when used). Do not include secrets or unverified claims.

**The `CHANGELOG.md` section is written before the tag.** The tag is the immutable
artifact — it is what the marketplace `sha` pins, and moving it needs explicit
owner authorization — so the commit it names has to be the complete release on its
own. Writing the section afterwards would put the release record in a commit the
tag does not name, leaving the tagged tree describing a release whose notes it
does not carry. `hooks/release-version` enforces the order by refusing to run
until the section exists.

## Tag, catalog pin, and GitHub Release

After the release scope is merged to the intended base (or the optional Release PR is merged):

1. Check out the exact merged base commit and confirm a clean working tree.
2. Verify manifest versions and release notes again — the `CHANGELOG.md` section
   must already be in this commit, because the tag names it.
3. Create an annotated tag such as `vX.Y.Z` on that commit.
4. Update both marketplace entries so each Git source uses the release tag as `ref`
   and the exact tagged commit as `sha`, then commit that edit locally. It carries
   only those four literals — `ref` is the tag name and `sha` is
   `git rev-parse <tag>^{commit}` — so there is nothing in it to review.
5. Push the pin commit and the tag together, in one atomic push, after explicit
   release-owner approval:

   ```bash
   git push --atomic origin main refs/tags/vX.Y.Z
   ```

   The pin commit must carry nothing else, and the push must carry no other refs.
6. Run `bash hooks/release-check .` again on the pushed `main`, and create the
   GitHub Release from the tag with the approved notes. Validate the catalog
   entry with Claude Code, Codex, and CodeBuddy tooling.
7. Record the result in the release notes: the tag, the release URL, the commit, and the two marketplace pins.

Steps 3–4 make a release two commits, by construction: the tag cannot be created
before the release commit exists on the base, and the pinned `sha` cannot be
written before the tag exists. Claude Code verifies the pin at install time and
refuses a mismatch as `sha_pin_mismatch`, and it clones by the pinned commit
rather than by the tag, so the pin is what keeps an installation on the reviewed
release if the tag is ever moved. The second commit is the pin, not a mistake.

Two commits, but not two pushes. The tag has to exist before the pin is
readable, and the pin has to be readable before the tag is useful; pushing them
apart leaves an interval where the catalog names a tag that is either missing
or stale, and a refresh landing in that interval installs the previous release.
`--atomic` makes both refs visible at once, so the interval does not exist.

This step is a direct push rather than a pull request on purpose. It moves two
things at once: an immutable tag, and the catalog record naming it. The record
is mechanically derived, so there is nothing to review, and its correctness is
enforced rather than reviewed — `git merge-base --is-ancestor` for the tag, and
`bash hooks/release-check .` for the `ref`/`sha` pair. A pull request here would
only reintroduce the interval it is meant to close, for a four-line diff whose
content the tag already determined. The release metadata commit is a different
matter: it carries prose, so it takes the Release PR path above.

If the remote rejects an atomic push, fall back to pushing the tag first and
updating the catalog after, exactly as this document required before the
atomic form existed, and record the resulting interval in the release notes. Do
not work around the rejection by putting other files into the atomic push: that
would make one unreviewable push out of the release metadata and an irreversible
tag.

The marketplace catalog itself remains on `main` so refreshes can discover the latest stable entry. The plugin source must not point at moving `main`; local-directory marketplace registration remains the development path.

### Optional Release PR path

Use `release/vX.Y.Z` when the release needs an isolated documentation review, a release candidate, or an explicit PR approval. Merge that PR before applying the same tag and GitHub Release steps above.

TaskFlow does not push tags or create GitHub Releases automatically.

## Rollback

Stop distribution, record the affected tag/commit and impact, and prefer a corrective patch release. Deleting or moving a remote tag requires explicit owner authorization and a documented reason. Never rewrite shared branch history as a rollback.

A wrong catalog record is corrected like any other catalog change — a new
commit with the right `ref`/`sha`, verified by `bash hooks/release-check .` —
and does not touch the tag. Only a wrong *tag* needs the authorization above,
because the tag is the part installations are pinned to.

## Known limitations

- The generic plugin validator may reject the existing Codex manifest `hooks` field even when Codex installation and TaskFlow smoke tests pass; record the discrepancy rather than deleting the hook declaration.
- `hooks/repository-check` is opt-in and does not mutate Git remotes or enforce release permissions.
- Release automation, package registries, signing, and provenance attestations are not configured by this document.
