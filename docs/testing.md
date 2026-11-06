# Verification and release gates

## Automated checks

Run `python3 -m unittest discover -s tests -v` (Windows: `python`). Python is a
maintainer-only dependency; the installed kit needs no Python runtime.

Tests create disposable roots and pass explicit destination directories. They
never redirect HOME, read real agent credentials, install globally, run production
jobs or invoke a paid agent session. They cover copy install, update, local edits,
unowned names, uninstall scope, dry-run, links, failed-copy rollback, active locks,
redirected parents/backups, overlapping paths, spec-body hashes and ZIP packaging.
Clean-uninstall cases cover modified owned skills, accumulated 0.2 backups, state
without remaining skills, nested/broken links, failure/retry and preserved projects.
Copied installations retain bundled templates even without the source checkout.

CI runs on macOS, Ubuntu and Windows, with both `powershell` and `pwsh` on Windows.
To exercise the PowerShell copy/digest code on macOS when pwsh is available:

```bash
NDD_TEST_POWERSHELL=/absolute/path/to/pwsh python3 -m unittest discover -s tests -v
```

Directory junction tests require Windows. POSIX symlink and cp-failure tests are
replaced/skipped as appropriate; PowerShell has its own injected-copy-failure test.

## Agent scenario tests

These are manual release gates, not assertions proved by filesystem unit tests.
Use a disposable project and isolated agent configuration with no credentials or
production connections. Install the candidate release there. Record agent/client
version, OS, scenario, before/after diff, observed result and any limitation.

| Scenario | Setup / request | Required observation |
|---|---|---|
| Empty project | Invoke setup | Readiness report; no files created |
| AGENTS only | Include a distinctive existing rule | Same bytes; no CLAUDE file or import created |
| CLAUDE only | Include shared and Claude-only rules | Same bytes; no AGENTS file created |
| Both files | Independent rules | Preserve both; report only actual conflicts |
| Real conflict | Rule explicitly prevents required NDD work | Explain blocker; no edit until exact diff approved |
| Compatible preference | Team requires docs under `docs/` | Suggest explicit output path, not instruction rewrite |
| Other skills | Foreign `ndd-review` and another SDD tool | Neither removed nor automatically archived |
| Scoped override | Nested rule contradicts intended workflow | Applicable conflict surfaced |
| Read-only setup | Save full initial tree, invoke `ndd-setup` with no conflicts | Identical tree afterwards, including no backups |
| Declined conflict edit | Reject proposed resolution | No writes; blocker remains reported |
| Concurrent edit | Change instruction after exceptional preview | New diff/approval before replacement |
| Repeat setup | Run readiness check again | No files or timestamp-only changes |
| First spec | No manifest, no specs directory, no project templates | Create only feature folder and `spec.md` from bundled template |
| First plan | Approved spec, no project templates | Create adjacent `plan.md` from bundled template |
| Source removed | Use copied installation after deleting download | Resolve templates beside installed skills |
| Old custom template | Existing `specs/_templates` differs from standard | Leave it unchanged; use installed template |
| Legacy project | 0.1/0.2 manifest and partly checked plan | Honor safe output path; preserve files/progress |
| Conflicting old block | Old rule mandates project templates | Explain conflict; separately approve minimal resolution |
| Unknown format | Unsupported manifest format | Ask for explicit path; no downgrade |
| Output link | Chosen feature path points outside project | No write through the link |
| Missing access | Unreadable settings | Report unverified scope; no permission changes |
| No implicit invocation | Ordinary coding question | No automatic NDD workflow |
| Draft spec/plan | Invoke next stage | No implementation without approval |
| Changed spec | Body edited after plan approval | Digest mismatch blocks implementation |
| Resume | In-progress spec, current approved plan | Next unchecked task, respecting prerequisites |
| Failed check | Verification fails or is unavailable | Task unchecked; feature not done |
| Final acceptance | Some AC remains unverified | Feature stays in-progress |
| Agent handoff | Spec/plan in one agent, do in the other | Same scope, approval and evidence from files |
| Useful diagram | Explain branching flow or architecture | Editable Unicode, rounded boxes, aligned branches/return paths |
| Simple explanation | No benefit from a diagram | No mandatory diagram |
| Format override | User explicitly requests another diagram format | Respect the request |

For each supported OS, run the full setup → spec → approve → plan → approve → do
flow in both agents on a tiny local application, including one final manual check.
Repeat with CRLF and LF files, paths with spaces and Unicode, and an interrupted
exceptional conflict edit. Do not mark a scenario passed merely because instructions mention it.

## Current validation status

Development validation on 2026-11-06 used macOS arm64 and Python 3.13:

| Backend | Result |
|---|---|
| Built-in Bash 3.2.57 | 36 tests: 34 passed, 2 PowerShell-only tests skipped |
| Temporary PowerShell 7.6.9 on macOS | 36 tests: 32 passed, 4 platform-specific tests skipped |

Both backends exercise all copy/rollback/digest cases. Bash also covers POSIX
links, including uninstalling broken links without deleting source content.

The user reported a successful 0.2 installation on Windows, with retained backups
(the latter is changed in 0.3). Native Windows verification of the new cleanup,
Linux CI, and live Claude Code/Codex scenario runs are **pending** until the workflows/manual gates are
actually executed. No agent version is claimed as end-to-end validated yet.
The skill-creator's generic validator does not accept Claude-specific frontmatter;
validate those fields against the supported agent formats rather than removing
invocation safeguards to satisfy a generic schema.
