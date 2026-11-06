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
| `--replace` | `-Replace` | Accepted for compatibility; replacement is automatic |
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

## Terminal help command

The `ndd-help` skill includes a terminal command in its `scripts` directory:
`ndd-help` for Bash and `ndd-help.cmd` for Windows. It prints the same predefined
English Markdown reference used by the chat skill and reads VERSION from the
adjacent `ndd-setup` installation. No Python, agent or network is needed.
Missing or invalid version data produces an incomplete-installation notice with
the reference; missing/unreadable help text produces an error and nonzero exit.
Arguments are ignored, just as with the chat help skill.

Installers copy these files with the skill and print the directory to add to PATH.
They do not edit shell profiles or persistent environment variables. Choose one
installed agent's help directory; if you remove that agent later, switch to the
remaining agent's directory.

For the default Codex installation on Mac, enable the command in the current shell:

```bash
export PATH="$HOME/.agents/skills/ndd-help/scripts:$PATH"
ndd-help
```

To keep it available in future zsh sessions, add that export line once to
`~/.zshrc` (or use your shell's normal startup file). For Claude Code, substitute
`$HOME/.claude/skills/ndd-help/scripts`, respecting `CLAUDE_CONFIG_DIR` if set.

On Windows, enable the default Codex command in the current PowerShell session:

```powershell
$env:Path = "$HOME\.agents\skills\ndd-help\scripts;" + $env:Path
ndd-help
```

For future sessions, add the full directory printed by the installer to your user
Path via **Environment Variables**, then open a new terminal. The `.cmd` launcher
uses Windows PowerShell with a process-only execution-policy bypass for the
bundled read-only helper; it does not change persistent execution policy.
PowerShell 7 can also run `scripts/print-help.ps1` directly.

Custom installations work the same way; always use the installed path printed by
the installer. Copy installations keep working after the downloaded source folder
is removed. Link installations require the source folder to remain available.
Uninstall removes the command with its skill, without editing your PATH.

## Windows execution policy

If Windows blocks a script you have inspected, use this process-only override
with your chosen target (`-Codex`, `-Claude` or `-All`):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -All
```

This does not change persistent policy. On a managed computer, follow your
organization's installation policy.

## Replacing existing skills

Install and update automatically replace all six NDD skill directories at the
selected destinations, including local edits and existing directories without
receipts. Unrelated skills and project files are preserved. Use `--dry-run` /
`-DryRun` to preview. The old `--replace` / `-Replace` option is no longer needed.

Receipts live beside the skills directory in `<skills-directory>.ndd-kit`.
Successful installs retain no backups and delete backups left by earlier versions.
Previous skills and receipts are held temporarily under `backups/` only to restore
them if installation fails. Failed recovery retains these files for manual repair.
Uninstall deletes all installation state; an existing skill without valid ownership
information still blocks uninstall.

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
