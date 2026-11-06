# Changelog

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
