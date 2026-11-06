---
name: ndd-setup
description: Inspect existing project instructions, skills and relevant agent settings, then propose a minimal NDD setup or update. Invoke explicitly with ndd-setup; apply only the exact changes the user approves.
argument-hint: "[--dry-run]"
disable-model-invocation: true
---

# ndd-setup

Connect this project to NDD without reorganizing the user's existing setup.
`--dry-run` performs inspection and preview only. Other options are unsupported
in this release (including the old experimental `--vendor`); explain the global
installation path instead of silently ignoring them.

This directory contains `VERSION` and `assets/{spec,plan,agents-block,principles}.md`.
The other three NDD skills are siblings. Use this loaded skill's actual location;
do not guess another installation if it differs. The format-2 project manifest
is documented in [references/project-state.md](references/project-state.md).
Read it when an existing manifest is found or before creating one.

## 1. Inspect without writing

- State the running agent and loaded kit version. Use the Git root when inside
  a repository; otherwise propose the current folder as project root. Report
  the root and existing local changes. Do not initialize Git or create a branch.
- Read applicable project/ancestor instructions, including overrides, scoped
  rules and relevant imports. Inspect root `AGENTS.md`, `CLAUDE.md`, optional
  `CLAUDE.local.md`, and nested instruction locations that affect the workflow.
- Read `.ndd-kit.json`, existing specs/templates and managed blocks. Check for
  malformed/duplicate markers, newer/incompatible manifests and local changes.
- Inventory skill/command names and metadata in project and relevant user
  directories. Read full bodies only for likely NDD collisions or conflicts.
  Detect both global and project NDD copies, other SDD tools, and disabled skills.
- Inspect known instruction files (`~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`)
  and relevant skill/instruction-loading settings, accounting for configured
  locations such as `CODEX_HOME` or `CLAUDE_CONFIG_DIR` where applicable. Do not
  assume the presence of a directory proves an agent or skill is usable.
- Do not recursively read agent state directories, auth files, `.env`, secrets,
  conversation history or unrelated skills. Never dump environment variables or
  whole configuration files. Report inaccessible/unknown settings as unverified.
- Infer existing test/build/lint commands from project docs/configuration, but
  do not execute them, load hooks, install dependencies or run project jobs.

Global files are read-only throughout setup. Do not change permissions, agent
settings, hooks, MCP connections or sandbox controls to make NDD work.

## 2. Propose the smallest integration

Preserve existing rules, formatting and file layout. NDD does not replace project
instructions or competing workflows. Classify findings as blocking conflicts,
optional improvements, or information. Don't make optional cleanup a prerequisite.

Default layout decisions:

| Existing instructions | Proposed change |
|---|---|
| Neither | Create `AGENTS.md` with the NDD block; for Claude create `CLAUDE.md` importing `@AGENTS.md`. |
| Only AGENTS | Add/update its NDD block; for Claude propose a small import file if needed. |
| Only CLAUDE | Preserve it and add NDD there; when enabling Codex, show the exact common rules proposed for a new `AGENTS.md`. Never silently omit important project rules or use an implicit "See CLAUDE.md" pointer. |
| Both | Preserve their separation. If an import already exposes the NDD block to both agents, reuse it; otherwise propose a short managed block in each. No automatic cross-import of the entire other file. |

Only prepare integration for agents the user selects; recommend both when the
project is intended to move between them. Machine detection is advisory, not a
reason to rewrite shared project choices. A project may target an agent that is
not installed on this machine; report its unverified local availability.

- Default specs directory: `specs`; preserve a previously configured directory.
  If that name already belongs to an unrelated workflow, propose a separate
  relative directory. Never overwrite or reinterpret existing feature folders.
- Render `assets/agents-block.md` with version and specs directory. Reuse existing
  project principles. `assets/principles.md` is only an optional source for
  missing commands; never insert unresolved placeholders or impose stack rules.
- Do not migrate user instructions, archive old commands or vendor skills as
  part of setup. Surface overlaps and let the user choose whether to use NDD.
- If required skills are absent, show the relevant installer command. Project
  setup itself must not install or modify global skills.
- For unsupported newer versions, stop affected operations. For 0.1 manifests,
  treat ownership as unverified and propose an explicit migration (see reference).

## 3. Show the reviewable result, then wait

Before any writes, show the root, versions/locations, findings, exact proposed
file operations, full text of new instruction blocks and a diff of existing files.
Include template and manifest changes. Explain which important existing rules
will or will not be shared between agents. Show blocking conflicts with concise
quotes and recommended resolutions; do not expose secrets in the report.

Collect necessary choices in one batch. Do not ask to approve a vague plan and
reveal the actual edits afterwards. An explicit approval of the displayed changes
is sufficient; don't ask again for those same edits. If `--dry-run`, stop here
without writing files, backups, timestamps or manifests.

## 4. Apply only the approved result

Re-read files before editing. If they changed since the preview, regenerate the
affected diff and obtain approval for the new result; don't overwrite concurrent
work. If instructions changed, reconcile them before continuing.

- Limit instruction edits to approved NDD marker blocks and explicitly approved
  additions. Preserve all unrelated text, encoding and line endings. If a tool
  cannot preserve these, show the additional changes before proceeding.
- Refuse malformed/duplicate markers or symlinked output files/parents until a
  concrete safe target is agreed. Never follow a project output link into global
  settings. Preserve local modifications even inside managed blocks/templates.
- For a file already tracked by Git with no pre-existing changes, its original
  is recoverable. Otherwise include a local backup outside agent skill discovery
  in the approved operations before replacement; never overwrite prior backups.
  Do not commit private backups or raw copies of global settings to the project.
- Create only approved templates, instruction additions and the format-2
  manifest. Do not change existing feature specs or plans during setup.
- Verify the written content against the approved preview. If interrupted or
  partially failed, report exact completed/pending operations and recovery paths.
  Do not claim success or revert unrelated work.

## 5. Verify and report

Check one managed block per intended file, correct imports/paths, no unresolved
placeholders, preserved surrounding instructions, and consistent manifest hashes.
Compare the final diff with the preview (or before/after content without Git).
Do not infer runtime skill discovery from files alone; say which agent checks
were actually observed and which remain unverified.

A repeat setup with unchanged inputs must produce no writes, no duplicate imports
and no timestamp-only changes. Updates require a new preview and approval. Finish
with changed files, verification, any unresolved conflicts and the next command:
`/ndd-spec <idea>` in Claude Code or `$ndd-spec <idea>` in Codex CLI/IDE. Never commit.
