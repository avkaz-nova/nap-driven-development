# Project setup

Run `/ndd-setup` in Claude Code or `$ndd-setup` in Codex, inside your project.
It checks project rules, installed skills and available verification commands,
then confirms a personal prefix for feature names.

## What setup changes

After you confirm a prefix, setup saves `ndd.prefix` in the repository's local
Git config and records the project and value in `~/.ndd/projects`. Both agents
share these settings. Neither is committed or pushed.

Setup creates no tracked project files, instruction blocks, templates or empty
specs folders. Existing `AGENTS.md` and `CLAUDE.md` stay unchanged unless you
approve a specific fix for a real conflict. Project checks are inspected, not run.

Repeat setup reuses a valid saved prefix. If its registry record is missing,
setup adds it; unchanged settings and records are left alone. A save or registration
failure is reported rather than treated as successful setup.

## Your prefix

Setup suggests a prefix from your Git author name, or asks you to supply one.
Use 2–16 lowercase letters or digits, starting with a letter, such as `ak`.
Choose different prefixes for teammates.

With `ak`, new features are named `ak-001-feature`, `ak-002-feature`, and so on.
`ndd-plan 001` and `ndd-do 001` select your feature; `ndd-plan iv-001` explicitly
selects another prefix. You can also give the full feature path. Ambiguous matches
require clarification.

A new clone needs setup again; you can use the same personal prefix. Changing
it affects future features and does not rename existing documents.

## Without Git

Installing the skills does not require a project repository or create Git config.
When setup runs outside a Git repository, it offers a prefix for the current
conversation only. It does not initialize Git, create a config file or register
that session-only choice. An unreadable existing config is reported as an error.

## Task documents

The first `ndd-spec` creates `specs/PREFIX-NNN-feature/spec.md`; `ndd-plan` adds
`plan.md` beside it. Templates come from the installed skills. Updating NDD does
not rewrite existing documents.

If your project uses another location, provide an explicit feature path.
Setup reports actual conflicts with project rules and suggests a resolution;
it does not replace those rules or change permissions to make NDD work.

Next: [workflow and approvals](workflow.md).
