# Changelog

## 0.3.0 — unreleased

- Setup records project/common-Git-directory, key and prefix in `~/.ndd/projects`.
  Full uninstall clears registered, unchanged local prefixes before removing NDD;
  unresolved records are kept with warnings while removal continues. Single-agent uninstall preserves
  the shared registry. Dry-run previews cleanup without writes.

- Setup checks readiness without creating instruction blocks, imports, manifests,
  project templates or empty specs directories.
- Setup proposes a personal prefix and saves the confirmed choice in local Git
  config. New feature ids use `PREFIX-NNN-slug`; bare numbers use the current
  prefix. Existing ids are preserved and ambiguous matches require clarification.
- README groups optional install/removal previews with their respective actions,
  with one command per copyable block.
- Removed the redundant setup dry-run option; installer dry-run remains available.
- Spec and plan use only bundled templates; legacy project files are preserved.
- Uninstall permanently removes owned skills (including edits), receipts, staging
  files and all old backups. With both agents selected, it also removes the verified
  clean official NDD clone containing the installer. Local work, unpublished history,
  linked worktrees and unverified sources are retained; `--keep-source` / `-KeepSource`
  explicitly preserves the clone. Your project files remain untouched.
- Shared rounded Unicode diagram guidance for all four skills.
- Regression coverage for clean removal, old leftover state, nested links, dry-run
  and interrupted deletion. Install/update backup and rollback are unchanged.

## 0.2.0 — unreleased

- Safe installers for the four named skills: ownership receipts, full-target
  preflight, dry-run, explicit replacement, backups, locks and rollback.
- Matching Bash/PowerShell options, custom target paths, and development links.
- Explicit invocation policies for Claude Code and Codex.
- Setup now previews exact edits, preserves existing instruction layouts, detects
  conflicts and user modifications, and uses a portable format-2 manifest.
- Approved plan state and cross-platform spec-body digests block stale execution.
- Practical verification, optional fresh sessions, recorded final AC checks and
  preserved task history on re-planning.
- Corrected recommendation example and a small CSV export example.
- Isolated regression tests, cross-platform CI and deterministic ZIP packaging.
- Removed experimental setup vendoring from this release; no automatic command
  archiving or instruction-file migration.

## 0.1.0 — 2026-11-06

- Initial release.
- Skills: `ndd-setup`, `ndd-spec`, `ndd-plan`, `ndd-do` (Agent Skills format; Claude Code and Codex).
- Templates: `spec.md` (EARS requirements, AC traceability, Data & metrics), `plan.md` (tasks with verify steps, coverage, decisions log).
- Installers: `install.sh`, `install.ps1` (copy or link, auto-detect, uninstall).
