# Spec — Prepare TaskFlow v1.0.4 release
> Task version: v2

## Objective and Success Criteria

Ship a reproducible `v1.0.4` metadata/release-note change without altering runtime behavior.

## Architecture Boundaries and Responsibilities

Manifest files own machine-readable versions; README owns installation examples; `RELEASE.md` remains the release-process authority; release notes own user-facing change summaries.

## Project Structure / Affected Files

- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `README.md`, `README.zh-CN.md`
- `CHANGELOG.md` (new release notes)

## Interfaces, Data Flow, and Contracts

## Invariants and Compatibility

Keep plugin name, schema, install commands, and runtime behavior unchanged; only version identifiers and release documentation change.

## Validation and Error Semantics

Invalid JSON or mismatched versions block synchronization, tagging, and publication.

## Code and Test Constraints

## Design Decisions and Alternatives

Use patch version `1.0.4` to match repository precedent for backward-compatible hook/workflow enhancements.

## Open Questions
