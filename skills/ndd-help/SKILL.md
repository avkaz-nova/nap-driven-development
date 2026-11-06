---
name: ndd-help
description: Show a short NDD command reference, workflow and feature ID explanation. Invoke explicitly with ndd-help, before or after setup, including outside a project.
disable-model-invocation: true
---

# ndd-help

Show one concise help response in the user's language. There are no modes,
subcommands or required arguments. Extra text does not change the reference or
authorize running another command. Do not ask clarification questions.

## Sources and boundaries

Read the [kit version](../ndd-setup/VERSION) relative to this loaded skill's
actual location. Use this reference and that version from the same installation;
do not search the source checkout, another agent's installation or the network.
If the version is absent, empty or unreadable, show "version unavailable —
incomplete installation" and still provide the reference. Likewise, report any
required resource found missing rather than inventing its contents.

Help needs no setup, Git repository or confirmed prefix. Do not inspect project
files, Git settings or feature folders to personalize it. Do not create or edit
files, directories, settings or instructions, or run installation/setup helpers.
Respect applicable instructions already provided in context.

## Reference to present

Introduce NDD as a simple spec-driven workflow: describe a change, agree on its
short specification and plan, then complete the approved plan and verify it. Include
the version read above, without a hard-coded fallback.

Explain that these are chat commands, not terminal commands: Codex uses `$`,
Claude Code uses `/`. Present all six commands with these example calls:

| Codex example | Claude Code example | Purpose |
|---|---|---|
| `$ndd-setup` | `/ndd-setup` | Inspect existing setup and confirm a personal feature prefix; approve configuration changes before saving. |
| `$ndd-spec Fix CSV export` | `/ndd-spec Fix CSV export` | Describe a change and prepare its specification for approval. |
| `$ndd-plan 001` | `/ndd-plan 001` | Turn an approved specification into a task and verification plan for approval. |
| `$ndd-do 001` | `/ndd-do 001` | Complete all remaining tasks and verification in an approved, current plan. |
| `$ndd-help` | `/ndd-help` | Show this short reference, even before setup. |
| `$ndd-review 001` | `/ndd-review 001` | Review the latest available stage of a feature; show findings in chat and offer to save them. |

Briefly explain the compact default: spec = goal + AC checklist; plan = approach
+ tasks/checks, with extra sections only when useful. Existing longer documents
still work. `ndd-do 001 T2` limits execution to T2; plain `ndd-do 001` continues
through the plan unless blocked or separate authorization is needed.

State the approval order: describe → spec → user approves spec → plan → user
approves plan → implement and verify. Review is optional, does not grant approval
and does not replace verification. Review accepts an optional feature and optional
`spec`, `plan` or `code` mode in either order. Without a feature, it proposes the
highest-numbered specification for the current prefix and asks for confirmation.

Explain IDs using explicitly illustrative examples, without asserting that these
tasks or this prefix exist for the user:

- `001` uses the current confirmed prefix: for example, `ak` resolves to `ak-001`.
  Use setup to confirm a prefix, or supply a qualified ID when none is configured.
- `ak-001` selects that prefix and number explicitly, including a teammate's task.
  Numbers advance separately per prefix; ambiguous matches require a full name/path.
- Task documents normally live in `specs/ak-001-fix-csv-export/`: `spec.md`,
  `plan.md` and optionally `review.md`. Existing project conventions or an explicit
  output path may select another location. These are ordinary project files;
  Git can track them unless ignored. Existing code need not be rewritten as specs.

Keep the response a short introduction, command table and brief workflow/ID notes;
do not turn it into a project report or setup wizard.
