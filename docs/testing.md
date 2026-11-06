# Verification and release gates

## Automated checks

Run `python3 -m unittest discover -s tests -v` (Windows: `python`). Python is a
maintainer-only dependency; the installed kit needs no Python runtime.

Tests create disposable roots and pass explicit destination directories. They
never redirect HOME, read real agent credentials, install globally, run production
jobs or invoke a paid agent session. They cover copy install, update, local edits,
unowned names, uninstall scope, dry-run, links, failed-copy rollback, active locks,
redirected parents/backups, overlapping paths, spec-body hashes and ZIP packaging.

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
| Empty project | Invoke setup | Exact preview first; no writes until approval |
| AGENTS only | Add a distinctive existing rule | Rule preserved; minimal Claude import proposed |
| CLAUDE only | Include shared and Claude-only rules | Codex additions shown explicitly; no silent migration |
| Both files | Different independent rules | Preserve both layouts; report actual conflicts |
| Existing imports | CLAUDE already imports AGENTS | No duplicate NDD block or import |
| Other skills | Add a foreign `ndd-review` and another SDD tool | Neither removed nor automatically archived |
| Scoped override | Nested/override rule contradicts the intended workflow | Applicable conflict surfaced, not ignored |
| Dry-run | Save the full initial tree, invoke `--dry-run` | Identical tree afterwards, including no backups |
| Declined preview | Reject all changes | No files written |
| Partial approval | Approve only specified operations | Only those operations applied; blockers reported |
| Concurrent edit | Change a file after preview | New diff and approval before replacement |
| Repeat setup | Run again after successful setup | No content or timestamp-only changes |
| Custom template | Edit a managed template/block | Merge decision before replacement |
| Broken markers | Duplicate/unclosed NDD markers | Explicit repair proposal, no guessed edit |
| Output link | Instruction file links outside project | No write through the link |
| Legacy project | 0.1 manifest and partially checked plan | Reviewed migration; preserve progress |
| Newer format | Unsupported manifest format | No downgrade or destructive migration |
| No Git | Ordinary folder | Proposed root; no implicit git init |
| Missing access | Unreadable global instructions/settings | Report unverified scope, no permission weakening |
| No implicit invocation | Ask an ordinary coding question | NDD explicit-only skills do not activate themselves |
| Draft spec | Invoke plan | No implementation or plan from unapproved requirements |
| Draft plan | Invoke do | No implementation; request plan review |
| Changed spec | Edit body after plan approval | Digest mismatch blocks implementation |
| Resume | Spec in-progress, approved matching plan | Resume next unchecked task |
| Prerequisites | Ask for a later task | Block unmet prerequisites without guessing |
| Failed verification | Make task check fail | Keep task unchecked and feature not done |
| Final acceptance | Task checks pass but one AC is unverified | Feature stays in-progress |
| Agent handoff | Spec/plan in one agent, do in the other | Same scope and approvals read from files |

For each supported OS, run the full setup → spec → approve → plan → approve → do
flow in both agents on a tiny local application, including one final manual check.
Repeat with CRLF and LF files, paths with spaces and Unicode, and an interrupted
setup. Do not mark a scenario passed merely because instructions mention it.

## Current validation status

Development validation on 2026-11-06 used macOS arm64 and Python 3.13:

| Backend | Result |
|---|---|
| Built-in Bash 3.2.57 | 26 passed, 1 PowerShell-only test skipped |
| Temporary PowerShell 7.6.9 on macOS | 24 passed, 3 platform/backend-specific tests skipped |

Both backends exercise all copy/rollback/digest cases. Bash also covers POSIX
links, including uninstalling broken links without deleting source content.

Native Windows PowerShell 5.1/7 (including junctions), Linux CI, and live Claude
Code/Codex scenario runs are **pending** until the workflows/manual gates are
actually executed. No agent version is claimed as end-to-end validated yet.
The skill-creator's generic validator does not accept Claude-specific frontmatter;
validate those fields against the supported agent formats rather than removing
invocation safeguards to satisfy a generic schema.
