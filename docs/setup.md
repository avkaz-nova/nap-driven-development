# Setup contract

`ndd-setup` checks whether the current project can use the installed NDD skills
and confirms a personal feature prefix. Inspection is read-only. The only normal
write is saving that prefix in local Git config after the user's confirmation.
The first requested specification creates its feature directory; setup creates
no tracked initialization files.

## Inspection

Read applicable project and ancestor instructions, relevant overrides/imports,
project and user skill metadata, instruction-loading settings and test/build/lint
definitions. Inspect full skill bodies only for a likely conflict. Missing access
is reported as unverified. Do not read credentials, `.env`, auth caches or history,
or execute project jobs and hooks merely to inspect them.

Existing `AGENTS.md` and `CLAUDE.md` remain unchanged, both project and personal.
Do not create a missing instruction file, add an import, copy project templates,
write `.ndd-kit.json`, or create an empty specs folder. Skills contain the workflow;
project instructions continue to define the team's working rules.

## Personal prefix

Read the repository-local `ndd.prefix`. When absent, suggest a short prefix from
`git config user.name`, explain that it separates teammates' feature numbers, and
let the user accept or supply another value. Validate it and save only the explicit
choice. A valid saved choice is reused without repeated confirmation or writes.
The shared [prefix and identifier rules](../skills/ndd-setup/references/feature-ids.md)
define validation, missing Git identity, collisions and command resolution.

For a confirmed `ak`, Git adds this section to its existing local config:

```ini
[ndd]
    prefix = ak
```

No separate `ndd.prefix` file is created. The setting is shared by both agents in
this clone (and its linked worktrees), stays out of commits, and is not pushed.
On another computer or clone, setup asks again; recommend using the same prefix.
No global Git settings or author identity are changed. Without Git, offer a
session-only choice; do not initialize a repository or create a fallback file.

New tasks use `ak-001-feature`, `ak-002-feature`, and so on. A teammate with `iv`
has a separate sequence. `ndd-plan 001` and `ndd-do 001` use the current prefix;
`ndd-plan iv-001` selects a teammate's task explicitly. Existing feature names
remain unchanged. Changing a prefix affects future tasks, not existing documents.

Prefixes reduce collisions, but do not reserve ids across unseen branches or
clones. Choose different prefixes for teammates. If duplicate ids become visible,
ask for an exact path; any rename is a separate approved change.

## Real contradictions

Report only actual blockers, separately from optional suggestions. Existing stack
choices, formatting preferences or another SDD framework are not automatically
conflicts. Prefer a compatible output path or verification command over editing
team instructions. If the user chooses an instruction edit to resolve a blocker,
show its exact minimal diff, obtain approval, preserve unrelated work and verify
the result.

Do not change permissions, hooks, sandbox policy or other agent settings to force
NDD to work. A readiness report does not approve any future spec or plan.

## Templates and documents

Standard templates stay in the installed kit at `ndd-setup/assets/spec.md` and
`plan.md`. No custom project-template selection is provided. Future documents use
the currently installed templates; existing feature documents are not rewritten
when the kit is updated. The default output is `specs/PREFIX-NNN-feature-slug/`.

A new project's first NDD task adds only `spec.md`, then `plan.md`. It does not
convert existing application code into specifications. If the default path is
unavailable, explicitly supply a feature path; subsequent commands can use that
path without introducing another settings file.

## Older projects

Read [existing-project guidance](../skills/ndd-setup/references/project-state.md)
when encountering legacy manifests, templates or instruction blocks. Honor safe
legacy output locations, but preserve these files and do not use their templates.
If an old instruction explicitly demands the old workflow, surface that conflict
and propose a minimal approved resolution. Cleanup of legacy project files is a
separate request; machine uninstall never performs it.

Invoke `ndd-setup` without flags. Team members install the same kit release. A
repeat setup with an unchanged prefix is read-only, with no timestamp or version-file churn.

## Limits

The operating agent follows the skill instructions. They are not filesystem
access controls and cannot prove that inaccessible corporate settings were checked.
Keep normal agent permissions and exercise the [manual scenarios](testing.md)
before declaring end-to-end agent compatibility. When a diagram adds clarity,
use the bundled rounded Unicode style rather than adding mandatory diagrams.
