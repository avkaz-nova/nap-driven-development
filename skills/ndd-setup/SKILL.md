---
name: ndd-setup
description: Check whether the current project can use NDD without changing its instructions or copying templates. Invoke explicitly with ndd-setup; report readiness and conflicts, and get approval before any exceptional edit.
disable-model-invocation: true
---

# ndd-setup

Check readiness for the explicitly invoked NDD workflow. Normal setup is read-only:
no instruction blocks, imports, project templates, manifest or empty specs folder.
The first `ndd-spec` invocation creates the task documents when needed.
Invoke `ndd-setup` without flags.

This skill contains `VERSION` and the standard `assets/spec.md` and `assets/plan.md`.
The other three NDD skills are siblings. Use this loaded kit's actual location;
never silently combine resources from different installations. These installed
assets are the only templates: do not copy them into projects or select custom
project templates. If resources are missing, report the incomplete installation.

## Inspect

1. Identify the running agent, loaded kit version and project root (Git root when
   available, otherwise the current folder). Report relevant local changes.
   Do not initialize Git or create a branch.
2. Read applicable project/ancestor instructions and relevant scoped rules,
   overrides and imports. Read existing `AGENTS.md`/`CLAUDE.md` in place. Do not
   create or edit project or global instruction files simply to enable NDD.
3. Inventory relevant installed skills and command metadata, including duplicate
   NDD versions or other SDD tools. Read full bodies only to investigate a likely
   conflict. Inspect instruction/skill-loading settings and known user guidance
   in the configured agent homes. Directory presence alone does not prove that
   a skill loads. Report unavailable settings as unverified.
4. Inspect the project's documented test/build/lint commands without running
   jobs, hooks, migrations or installers. Do not scan auth caches, secrets,
   `.env`, conversation history or unrelated global files. Never dump environment
   variables or entire configuration files.
5. Check that the default output directory `specs/` does not belong to an unrelated
   workflow. Leave it absent until the first task. For an existing NDD project,
   read [existing-project guidance](references/project-state.md) if a legacy
   manifest, instruction block or copied template is found. Preserve those files.

## Resolve actual conflicts

Distinguish blocking contradictions from optional preferences. If the project's
rules allow the NDD workflow, nothing needs to be edited. An existing stack,
formatter, testing framework or another SDD tool is not automatically a conflict.
NDD must respect project rules; its installation does not override them.

Prefer a compatible way of working, such as an explicitly requested output path,
over editing shared instructions. Show any real contradiction with a concise
quote, its effect and a recommended resolution. Do not edit a project's rules,
permissions, global guidance, hooks or agent configuration to bypass it.

If the user chooses an instruction edit to resolve a genuine blocker, first show
the exact minimal diff and obtain approval. Re-read before applying it; ask again
only if the proposed result materially changed. Preserve unrelated text and local
work, verify the approved diff, and report the change. No general NDD block or
personal global reminder is required.

## Report

State:
- whether NDD is ready, blocked, or partially unverified;
- which installed templates and output location will be used;
- any actual conflict and unresolved checks;
- that a normal setup wrote no files;
- the next invocation: `/ndd-spec <idea>` or `$ndd-spec <idea>`.

A readiness report is not approval of a future spec or plan. Skills perform the
workflow when explicitly invoked; normal coding requests need not use NDD.
Repeated setup should remain a read-only check. Never commit or install globally.

When a diagram helps explain a conflict or workflow, use the
[rounded Unicode diagram style](references/diagrams.md). Skip diagrams that add no value.
