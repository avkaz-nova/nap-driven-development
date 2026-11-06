# Setup contract

`ndd-setup` is an agent-guided integration, not a global configuration manager.
Its phases are inspection, exact preview, approval, application and verification.

## What is inspected

Project/ancestor instructions and applicable overrides; project and user skills
and command metadata; existing NDD state; relevant skill/instruction-loading
settings; existing test/build/lint definitions. Full skill bodies are read only
when needed to understand a conflict. Inaccessible settings are marked unverified.

Setup does not scan credentials, `.env`, auth caches or conversation history.
It does not execute project jobs or hooks to discover what they do. Global files
remain read-only. An unreadable corporate setting cannot be assumed absent.

## Minimal integration

New projects can share `AGENTS.md` through an `@AGENTS.md` import in `CLAUDE.md`.
Existing independent instructions keep their layout, rules and formatting; short
NDD blocks can be added to both when necessary. If a common rule would not reach
one of the selected agents, setup shows that gap and the exact proposed addition.

No automatic migration, old-command archiving, permission changes, stack rules
or removal of another SDD framework. Blocking contradictions need a resolution;
optional cleanups do not prevent adopting NDD. Project integrations can include
an agent not installed on the current machine.

## Approval and preservation

Before writing, show file operations, exact added text and diffs. Approval applies
to those changes. If files change after preview, obtain approval for the changed
result. Dry-run creates no backup, manifest, directory or timestamp.

Managed blocks do not make user modifications disposable. Changed templates and
blocks need a merge decision. Output paths cannot traverse links outside the
project. Malformed or duplicate markers need an explicit repair proposal.

For pre-existing uncommitted/untracked content, include a recoverable local backup
in the approved operations before replacing it. Do not commit private backups or
global configuration snapshots. Check the final result against the approved diff.

## Updates and portability

The [format-2 manifest](../skills/ndd-setup/references/project-state.md) records only
portable project choices and managed content hashes. Repeated unchanged setup is
a no-op. Setup preserves feature specs/plans and never upgrades them in bulk.

Global skill updates do not edit projects. A newer incompatible project format
must not be downgraded by an older setup. Old 0.1 manifests require an explicit,
reviewed adoption; no assumptions of ownership from filenames alone.

`--vendor` from 0.1 was experimental and is not available in 0.2. Team members
install the same release globally. Vendoring may return after duplicate-skill
resolution is tested in both agents.

## Limits

The operating agent performs the edits. These instructions are not filesystem
access controls and do not prove that all undiscoverable organization settings
were checked. Test the scenarios in [testing.md](testing.md) in each supported
agent before claiming a release is validated. Keep the agent's normal permissions.
