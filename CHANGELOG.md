# Changelog

## [1.0.4] — 2026-09-13

### Added

- Current-task-first SessionStart context with explicit verbose mode.
- SessionStart event JSON routing using `cwd`, event filtering, and safe malformed-input diagnostics.
- Linux and Windows GitHub Actions coverage for TaskFlow hooks.

### Fixed

- Windows launcher forwarding for more than nine arguments, spaces, and Unicode values.
- Repository-document index path traversal validation, malformed-row preservation, and concurrent-write protection.
- Explicit Python 3 runtime discovery and Microsoft Store alias diagnostics.

### Compatibility

- Runtime behavior remains backward-compatible; hooks continue to use Git Bash on Windows and Python 3 for Markdown lifecycle operations.
- No migration or dependency installation is required for existing installations.

### Verification

- `bash hooks/smoke-test` — passed.
- Linux and Windows GitHub Actions matrix — passed.
- TaskFlow Skill validator — passed.
