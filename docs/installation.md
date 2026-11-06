# Installation, updates and recovery

Run the installer from a downloaded release or checkout. It has no download,
telemetry, package-installation or project-setup side effects.

| Bash | PowerShell | Meaning |
|---|---|---|
| `--claude` | `-Claude` | Select Claude Code |
| `--codex` | `-Codex` | Select Codex |
| `--all` | `-All` | Select both |
| `--dry-run` | `-DryRun` | Inspect and print without writing |
| `--replace` | `-Replace` | Back up and replace conflicting/modified skills |
| `--uninstall` | `-Uninstall` | Permanently remove owned skills and all NDD install state |
| `--link` | `-Link` | Development symlinks/junctions into this checkout |
| `--claude-dir /absolute/path` | `-ClaudeDir C:\absolute\path` | Select an explicit Claude skills directory |
| `--codex-dir /absolute/path` | `-CodexDir C:\absolute\path` | Select an explicit Codex skills directory |

Custom paths must be the actual directories the agent loads. NDD does not change
agent configuration to make an arbitrary path discoverable. For redirected
parent directories, select the real destination path explicitly; the installer
refuses to follow parent symlinks/junctions. Individual installed skills may be
links made by `--link` / `-Link`.

`CLAUDE_CONFIG_DIR`, when set, changes the default Claude destination. `CODEX_HOME`
is a detection hint for the Codex configuration directory, not a replacement for
its documented user skills directory `~/.agents/skills`.

## Windows execution policy

If an inspected local script is blocked on your own machine, you can run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -All
```

This option applies to this PowerShell process, not machine policy. NDD never
changes persistent execution policy. Do not use it to circumvent organization
policy; use the supported installation process on managed devices.

## Ownership and replacement

The installer manages exactly `ndd-setup`, `ndd-spec`, `ndd-plan`, `ndd-do`.
Receipts live in `<skills-directory>.ndd-kit/<name>.receipt`, next to (not inside)
the directory scanned for skills. Each receipt records format, version, mode,
source path and content fingerprint. Receipts are local machine state, never
project configuration, and should not be copied between machines.

A matching name or NDD marker is not proof of ownership. A skill with no receipt,
changed contents, extra files, or a changed link target blocks an install/update.
For uninstall, a valid ownership receipt is sufficient even when skill contents
were edited: removal is the explicitly requested action.
Preview a deliberate replacement with `--replace --dry-run` / `-Replace -DryRun`.
Then use the same command without the dry-run option if that is your decision.
Replacement backs up even unowned files. Uninstall has no force/replace option;
missing/invalid ownership for an existing skill blocks deletion before changes.

Updates copy and verify each skill in a staging directory before replacing the
old one. All selected targets are preflighted and locked. A handled failure
restores replacements already made, including across both targets. User-created
empty directories also count as modifications. Permission bits are not part of
the content fingerprint.

Backups are under `<skills-directory>.ndd-kit/backups/<name>.<unique-id>/`, with
`skill` and `receipt` entries when an old installation existed. Install/update
retains them for recovery. Uninstall deletes ALL this NDD state, including older
backups, and creates no new backup. Inspect/save anything you want to keep before
requesting uninstall; a backup may contain your custom instructions.

## Recover from an interrupted install/update

A process kill, power loss or filesystem failure can interrupt any installer.
Do not assume rollback completed if the process never printed its final result.

1. Ensure no installer is still running. Inspect the reported destination,
   backup directory and any `stage.*` directories.
2. Move any partial new skill aside. Restore that skill's backed-up `skill` to
   its original name and its `receipt` to the corresponding receipt path.
   Do this only for affected NDD names, preserving any subsequent user edits.
3. After recovery and only when no install is active, remove the stale `lock`
   entry (a directory for Bash, a file for PowerShell).
4. Run a dry-run again. Do not delete staging files until you have confirmed
   which copies contain the content you want to retain.

Old backups are retained after successful automatic rollback as well. Never
blindly copy a whole backup folder over unrelated global skills.

## Link mode and removal

Link mode keeps this checkout as the source. A `git pull` immediately changes
what agents load, without a separate installation review. Use it for developing
NDD; use a copied release for routine work. Moving/deleting the checkout leaves
broken links; uninstall recognizes its own links and removes only those links.
PowerShell uses Windows junctions, not administrator-only symbolic links.

## Clean uninstall

Uninstall preflights every selected target, then permanently deletes its four
owned skills and all contents of `<skills-directory>.ndd-kit`: receipts, backups,
leftover staging files and the metadata directory itself. Existing backups are
removed even if no installed skills remain. Local edits inside owned skills are
also removed. A dry-run performs none of these deletions.

Nested symlinks/junctions are removed as links, including in old backups; their
targets are not traversed. An active/stale lock blocks concurrent removal. After
an interrupted uninstall, ensure no installer is running before removing a stale
lock, fix the reported error and retry. Removal has no backup or rollback; it
must never report success after a failed delete.

NDD never searches for or removes project documents, source code or project
settings. It also preserves the downloaded source checkout and unrelated skills.
For a new 0.3 project there is nothing to disconnect beyond keeping your spec/plan
files. Legacy manifests, templates, blocks and imports also remain in projects;
removing them requires a separate explicit request and review of shared rules.
