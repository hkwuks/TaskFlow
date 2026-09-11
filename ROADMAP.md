# TaskFlow roadmap

## Direction

TaskFlow is a repository-local workflow plugin for durable task requirements, design, approval, implementation, verification, and archival across Codex and Claude Code. The roadmap prioritizes reliable lifecycle records, low-noise host integration, and repository-governed development.

## Near-term priorities

1. Keep PRD/Spec/Plan lifecycle transitions explicit, recoverable, and easy to inspect.
2. Improve repository and fork readiness checks without silently mutating Git or remote state.
3. Maintain parity between Codex and Claude Code manifests and hooks.
4. Reduce token cost through bounded lifecycle commands while preserving traceability.
5. Expand focused smoke coverage for cross-platform hook behavior.

## Planning rules

- Priorities are directional, not dated commitments.
- Every implementation still requires a scoped TaskFlow task and approval.
- New integrations, hosted services, or provider-specific behavior require a separate approved task.
