# Changelog

## Unreleased

## 0.6.0 — 2026-11-06 (public preview)

- Expand chat help with individual-task execution and spec/plan/code review examples.
- Offer spec approval with continuation to planning, using interactive choices
  where supported and short chat replies elsewhere. Keep plan approval separate.
- Shorten the README and move installation/removal details to the dedicated guide.
- Explicitly respect existing global, project and nested instructions in all six
  skills, surfacing conflicts before affected work proceeds.
- Remove terminal help launchers and PATH instructions; retain chat help and both
  installers. Updates remove previously installed launchers with the help skill.

## 0.5.0 — 2026-11-06 (public preview)

- Automatically replace all six installed NDD skills, including local edits,
  without requiring `--replace` / `-Replace`. Successful updates remove previous
  backups; temporary recovery copies remain available if rollback fails.
- Report backup cleanup failures with a nonzero exit status so incomplete updates
  cannot appear successful to scripts.
- Return a predefined English help reference in chat, with only the installed
  version substituted.
- Add a terminal `ndd-help` command for Bash and Windows using the same reference,
  without an agent, network access or project setup. Install/update/uninstall
  manage it with the help skill; installers print the directory to add to PATH.
- Verify exact help output, incomplete-installation errors, installed CLI behavior
  after source removal, packaging, replacement and backup cleanup.

## 0.4.0 — 2026-11-06 (public preview)

- Make new specs/plans compact by default: AC-only requirements, task-level
  coverage, optional sections and concise verification records. Existing R/AC
  documents remain supported without migration.
- Make `ndd-do <id>` complete the remaining approved plan; an explicit task id
  limits execution to that task. Preserve approvals, digest and verification gates.
- Reuse established context and unchanged passing checks to avoid repeated work;
  retain focused checks and required final verification.
- Add `ndd-help`: short command reference, installed version, workflow and IDs,
  available before setup and outside Git without writing project files.
- Add optional `ndd-review`: automatic stage selection or explicit spec/plan/code
  review, with confirmed latest-feature selection when no ID is given.
- Offer saving a review only after analysis; extend a unified checklist with stable
  finding IDs, preserved comments and evidence for fixed findings.
- Install and remove six skills for either agent; support upgrading a four-skill
  installation while retaining ownership, conflict and rollback protections.
- Add packaging/migration checks and manual agent acceptance scenarios.

## 0.3.0 — 2026-11-06 (public preview)

First public GitHub release. Automated installer and packaging checks cover macOS,
Ubuntu and both Windows PowerShell environments. End-to-end agent behavior still
needs manual validation; this release is marked as a pre-release.

- Release ZIPs normalize only known text formats and preserve images and unknown
  file types byte-for-byte, with regression coverage for the README banner.
- README adds a CI badge, a compact CSV example and a versioned download link.
- CI uses Node.js 24 actions and pins Ubuntu to 24.04.

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

## 0.2.0 — development milestone (not published)

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
