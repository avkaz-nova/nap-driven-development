# Installation options and troubleshooting

Start with the [installation, update and uninstall commands](../README.md#install).
This page covers custom locations and problems you may encounter. Project
registration uses Git 2.31 or newer.

## Options and locations

| Bash | PowerShell | Meaning |
|---|---|---|
| `--codex` | `-Codex` | Install for Codex |
| `--claude` | `-Claude` | Install for Claude Code |
| `--all` | `-All` | Select both agents |
| `--dry-run` | `-DryRun` | Preview without changes |
| `--replace` | `-Replace` | Back up and replace conflicting or modified skills |
| `--uninstall` | `-Uninstall` | Remove NDD for the selected agents |
| `--keep-source` | `-KeepSource` | Keep the source clone during uninstall |
| `--link` | `-Link` | Link skills to this checkout for development |
| `--codex-dir PATH` | `-CodexDir PATH` | Select a custom Codex skills directory |
| `--claude-dir PATH` | `-ClaudeDir PATH` | Select a custom Claude skills directory |

Defaults are `~/.agents/skills` for Codex and `~/.claude/skills` for Claude Code.
`CLAUDE_CONFIG_DIR` changes the Claude configuration root. `CODEX_HOME` helps
agent detection but does not change the Codex skills destination.

Custom paths must be actual directories your agent loads. Use the same paths
for updates and uninstall. For redirected parent folders, pass the real path;
the installer refuses to follow parent symlinks or junctions.

Link mode loads skills directly from the checkout, so pulling changes updates
what the agent uses immediately. Keep that checkout in place. Normal installation
copies the skills and works without the downloaded folder.

## Windows execution policy

If Windows blocks a script you have inspected, use this process-only override
with your chosen target (`-Codex`, `-Claude` or `-All`):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -All
```

This does not change persistent policy. On a managed computer, follow your
organization's installation policy.

## Modified skills and backups

An install or update stops if an existing skill is modified or cannot be identified
as owned by NDD. To replace it deliberately, add `--replace` / `-Replace` to your
install command; add the dry-run option first to preview.

Receipts and backups live beside the skills directory in
`<skills-directory>.ndd-kit`. Backups are under `backups/`, with the saved `skill`
and, when present, its `receipt`. Updates keep these backups. Uninstall deletes
them along with the owned skills, including local edits, without making a new backup.
An existing skill without valid ownership information blocks uninstall.

## Interrupted installation or removal

1. Make sure no installer is still running.
2. Inspect the reported paths and backups. For an interrupted update, restore the
   affected skill and its matching receipt if needed; preserve any newer edits.
3. Remove a stale `lock` in `<skills-directory>.ndd-kit` only after confirming
   no installer is active. Keep staging files until recovery is complete.
4. Preview again, then retry. On Windows, close processes holding files in a
   source clone that could not be removed.

## Source clone cleanup

Full uninstall can delete only the clone containing the running installer.
It must be a standalone clone of `avkaz/nap-driven-development`, with Git available,
no local changes (including untracked or ignored files), no linked worktrees and
no unpublished history, stashes or reflog entries. The check uses local
remote-tracking refs; it does not fetch. Hidden index changes also prevent cleanup.

ZIP folders, forks and clones that fail these checks are kept with a reason.
Other downloads are never searched. Use `--keep-source` / `-KeepSource` to keep
the clone intentionally. Preview shows the source path and proposed action.

## Project registry

Setup records each project's location and saved prefix in `~/.ndd/projects`.
Full uninstall removes only the registered local `ndd.prefix` value when it still
matches. Failed or inaccessible entries are kept with a warning, and removal
continues. Single-agent uninstall keeps the registry and project settings.

Successful records are removed, followed by the registry folders if empty.
Moved projects need setup again; stale records may need manual cleanup.
`NDD_STATE_DIR` overrides `~/.ndd`; use the same value for setup and uninstall.
