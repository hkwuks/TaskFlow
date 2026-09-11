# Spec — Repository document environment behavior
> Task version: v2

## State and Flow

```text
triage / PR / release / roadmap task
  → inspect repository-docs catalog
  → refresh discovery when absent or stale
  → select documents applicable to task phase
  → record selected documents in task plan
  → source document changes
      → refresh catalog; re-plan if a changed rule affects approved work
```

## Catalog Contract

`TaskFlowDocs/repository-docs/index.md` is derived navigation, not authority. Each entry records document class, repository-relative source path, workspace access mode (`symlink` or `index`), existence, and last checked date. Source files remain authoritative.

## Selection Rules

- Code work: code style and contributing guidance.
- Commit or PR work: contributing, commit rules, PR templates, CODEOWNERS, branch/CI rules.
- Design/API/UX work: design standards, architecture guidance, README when it defines public behavior.
- Release work: release and changelog guidance.
- Roadmap or product-scope work: roadmap and README.

## Refresh Rules

Refresh before non-trivial work if the catalog is missing, an entry is stale, or the task phase needs a class not cataloged. Refresh after a relevant source change. Source discovery must not create missing source documents. If a recognized document is missing and the task needs its rules, use the standards-bootstrap workflow only for repository-owned rules, not for generic project prose.

## Safety

Only allow relative paths inside the repository. Never copy source contents, create fake links, or overwrite source documents. A link is optional; the index mode must be functionally sufficient.
