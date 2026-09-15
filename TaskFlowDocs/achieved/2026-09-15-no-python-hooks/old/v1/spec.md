# Spec — Run TaskFlow hooks without a Python interpreter
> Task version: v1

## Objective and Success Criteria

Every TaskFlow hook runs to identical effect with no Python interpreter available.
Success is defined as byte-identical output on the existing fixtures plus a smoke
suite that passes with no `python*` on `PATH` — not as "the tests still pass",
which would also be true of a subtly different implementation.

## Architecture Boundaries and Responsibilities

- A hook is a single POSIX shell script. No hook may delegate text processing to
  a language runtime.
- The portability floor is bash 3.2 with BSD userland, per the achieved
  `2026-09-14-macos-hook-portability` task. `awk` and `sed` are the extension
  points; they are the only structured-text tools a POSIX host guarantees.
- Git for Windows Bash is the Windows runtime. There is exactly one
  implementation of each hook, and it is the POSIX one.
- Removal is part of the change: `hooks/python-runtime` exists only to serve the
  dependency being removed, and it goes with it.

## Project Structure / Affected Files

```text
hooks/
├── archive                 # Python → awk
├── repository-docs-context # Python → awk
├── reopen                  # Python → awk
├── session-record          # Python → awk (heaviest structured edit)
├── session-start           # Python (event JSON field extraction) → sed/awk
├── summarize-state         # Python → awk
├── task                    # Python → awk (heaviest: 183 lines)
├── python-runtime          # DELETED
├── smoke-test              # python-runtime section → no-interpreter assertion
└── smoke-test-windows.ps1  # reference check only
```

## Interfaces, Data Flow, and Contracts

- Script names, arguments, stdout, stderr, and exit codes do not change. Callers
  (`hooks.json`, `hooks-codex.json`, the Skill) are untouched.
- The atomic write contract is preserved: write a temp file in the target's
  directory, then `mv` over the target. This is the existing idiom in
  `hooks/version` and it is what keeps a crash from truncating a task document.
- Byte-identical file writing: the Python implementation wrote with `newline=""`
  (no translation). The replacement must not introduce CRLF or strip a trailing
  newline, or Windows users get spurious diffs.
- The index-write lock (`index.md.lock`) and the relative-path traversal
  validation in `repository-docs-context` are behavior, not implementation
  detail: both must survive the rewrite.

## Invariants and Compatibility

- No `declare -A`, no `${var,,}`, no `mapfile`, no `readarray`, no bash-4
  substitution: all are absent from bash 3.2.
- No GNU-only `awk`/`sed`: no `gensub`, no `\b`/`\s` in `sed` patterns, no bare
  `sed -i` (BSD `sed` reads the next argument as a backup suffix).
- `set -euo pipefail` stays on in the entry scripts; the referenced-empty-array
  bug fixed by the macOS task must not be reintroduced.
- Output stays inside the documented context budget. Both hosts cap hook context,
  so a conversion must not expand what a hook prints.

## Validation and Error Semantics

- Each hook keeps its failure mode: a visible diagnostic on stderr and a nonzero
  exit where it had one, best-effort silence where it had that
  (`session-record` must still never change `session-start`'s exit code).
- Unparseable input still writes nothing and still reports on stderr. This is the
  property most likely to regress in a rewrite, so it is verified explicitly.

## Code and Test Constraints

- The smoke suite is the specification. Coverage is not reduced to make the
  rewrite pass; if an assertion is hard to satisfy, the implementation is wrong,
  not the assertion.
- One new assertion is added: the suite passes with no Python reachable.
- Verification is byte comparison against fixtures captured from the Python
  implementation before it is removed, not against freshly written expectations.

## Design Decisions and Alternatives

- **POSIX `awk`/`sed` over a native PowerShell implementation.** The rejected
  alternative was maintaining a second implementation for Windows. It costs a
  duplicate of every hook, a duplicate smoke suite, and a permanent
  two-place-edit rule, in exchange for supporting hosts without Git Bash — which
  the supported Windows path already requires.
- **Removing `python-runtime` rather than leaving it unused.** Keeping a
  validator for a dependency that no longer exists is the definition of dead
  weight, and its WindowsApps aliasing logic is exactly the class of environment
  failure this task removes.
- **`evals/runner.py` stays.** It is a repository-side harness, not shipped
  runtime, so it does not carry the compatibility risk that motivated the change.

## Open Questions

- None blocking.
