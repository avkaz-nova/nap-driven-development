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
| `--uninstall` | `-Uninstall` | Remove unchanged owned skills, retaining backups |
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
changed contents, extra files, or a changed link target blocks the operation.
Preview a deliberate replacement with `--replace --dry-run` / `-Replace -DryRun`.
Then use the same command without the dry-run option if that is your decision.
Replacement backs up even unowned files. Uninstall has no force/replace option.

Updates copy and verify each skill in a staging directory before replacing the
old one. All selected targets are preflighted and locked. A handled failure
restores replacements already made, including across both targets. User-created
empty directories also count as modifications. Permission bits are not part of
the content fingerprint.

Backups are under `<skills-directory>.ndd-kit/backups/<name>.<unique-id>/`, with
`skill` and `receipt` entries when an old installation existed. Backups are not
pruned automatically. Inspect and remove obsolete backup directories yourself
when you no longer need them; a backup may include your private custom instructions.

## Recover from an interruption

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

Uninstall leaves project specs and instructions intact. To disconnect a project,
review and remove only its NDD marker blocks, inserted imports and `.ndd-kit.json`.
Keep your feature documents and custom rules. Do not delete an entire instruction
file merely because setup once added a block to it.
