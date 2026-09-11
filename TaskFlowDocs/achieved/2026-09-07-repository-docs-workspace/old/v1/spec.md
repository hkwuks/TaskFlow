# Spec — Repository documentation workspace
> Task version: v1

## Architecture

```text
TaskFlowDocs/repository-docs/
├── index.md                  # portable catalog and link status
├── README.md -> ../../README.md          # only when symlinks are supported
├── README.zh-CN.md -> ../../README.zh-CN.md # only when supported
└── standards/
    └── index.md
```

`index.md` always exists. A relative symbolic link is an optional convenience; it must point within the repository and its source must exist. If `core.symlinks` is false or the platform does not support links, the index lists the repository-relative source path instead.

## Document Discovery

Inspect repository-root and conventional documentation paths for `README*`, `CONTRIBUTING*`, `CODE_STYLE*`, `STYLEGUIDE*`, `RELEASING*`, `RELEASE*`, `ROADMAP*`, and `CODE_OF_CONDUCT*`. Index discovered files; list undiscovered classes as `not found`. Do not generate source files.

## Standards Contract

The standards entry point moves to `TaskFlowDocs/repository-docs/standards/index.md`. It remains repository-owned and is separate from task-specific `reference/` evidence.

## Safety

Do not follow links outside the repository, create links when source paths do not exist, overwrite source documents, or create text files that pretend to be symbolic links.
