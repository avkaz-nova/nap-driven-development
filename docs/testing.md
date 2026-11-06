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
| Empty Git project | Invoke setup and accept a prefix | Only local Git prefix saved; no tracked files created |
| Proposed prefix | Set Git author name to Alexey Kazakov; no prefix yet | Explain proposed prefix and local storage; wait for acceptance/custom choice |
| Custom prefix | Supply a valid alternative | Save that value only; read it back; no extra approval loop |
| Invalid prefix | Supply spaces, punctuation, a path or multiple saved values | Explain invalid value; no silent coercion or overwrite |
| Declined prefix | Decline the suggestion without choosing another | No config/files written; explain that new features need a confirmed prefix |
| Missing Git identity | No author name configured | Ask for prefix; do not invent identity or read email/credentials |
| No Git repository | Invoke setup | Offer session-only prefix; no Git initialization or fallback file |
| Prefix save failure | Local config is not writable | Report unsaved choice; do not claim persistence |
| Other computer | Fresh clone of a project with prefixed specs | Confirm own prefix again; do not infer ownership from a matching folder |
| AGENTS only | Include a distinctive existing rule | Same bytes; no CLAUDE file or import created |
| CLAUDE only | Include shared and Claude-only rules | Same bytes; no AGENTS file created |
| Both files | Independent rules | Preserve both; report only actual conflicts |
| Real conflict | Rule explicitly prevents required NDD work | Explain blocker; no edit until exact diff approved |
| Compatible preference | Team requires docs under `docs/` | Suggest explicit output path, not instruction rewrite |
| Other skills | Foreign `ndd-review` and another SDD tool | Neither removed nor automatically archived |
| Scoped override | Nested rule contradicts intended workflow | Applicable conflict surfaced |
| Read-only repeat | Valid saved prefix; save full initial tree, invoke setup with no conflicts | Identical tree/config afterwards, including no backups |
| Declined conflict edit | Saved prefix; reject proposed resolution | No writes; blocker remains reported |
| Concurrent edit | Change instruction after exceptional preview | New diff/approval before replacement |
| Repeat setup | Saved prefix; Git author name changed | Reuse prefix without prompting or rewriting config |
| First spec | Confirmed prefix, no manifest/specs/templates | Create only prefixed feature folder and `spec.md` from bundled template |
| Missing prefix for new spec | No saved or session-confirmed choice | Ask for setup; no guessed prefix, settings write or partial spec |
| Prefix-local numbering | `ak-001` and `iv-009` already exist | Next ak feature is `ak-002`; id equals folder, owner equals prefix |
| Short id | Saved `ak`; both `ak-001` and `iv-001` exist | `plan/do 001` resolve ak; explicit `iv-001` resolves iv |
| Missing own id | Saved `ak`; only `iv-001` or legacy `001` exists | Bare `001` does not silently choose either; request explicit id/path |
| Colliding branches | Two `ak-001-*` folders become visible | Ask for exact path; no automatic rename/merge or arbitrary selection |
| Prefix change | User approves a new prefix | Change local setting only; existing feature names, ids and owners preserved |
| Legacy short id | No prefix; one unprefixed `001` and no prefixed matches | Resolve old feature without migration or new settings |
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

A disposable Git repository on macOS was also used to check the prefix commands:
only the local `[ndd]` section was added, a fresh process read the saved value,
and global config, project files and Git status stayed unchanged. A second
repository had no local prefix. This checks Git storage, not the agent's prefix
prompting, numbering or resolution behaviour; those scenario runs remain pending.

The user reported a successful 0.2 installation on Windows, with retained backups
(the latter is changed in 0.3). Native Windows verification of the new cleanup,
Linux CI, and live Claude Code/Codex scenario runs are **pending** until the workflows/manual gates are
actually executed. No agent version is claimed as end-to-end validated yet.
The skill-creator's generic validator does not accept Claude-specific frontmatter;
validate those fields against the supported agent formats rather than removing
invocation safeguards to satisfy a generic schema.
