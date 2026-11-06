NDD {{VERSION}} is a simple spec-driven workflow: describe a change, agree on a short specification and plan, then complete the approved plan and verify it.

These are chat commands, not terminal commands. Codex uses `$`; Claude Code uses `/`. The terminal command `ndd-help` prints this same reference without AI.

| Codex example | Claude Code example | Purpose |
|---|---|---|
| `$ndd-setup` | `/ndd-setup` | Inspect setup and confirm a personal feature prefix; approve configuration changes before saving. |
| `$ndd-spec Fix CSV export` | `/ndd-spec Fix CSV export` | Prepare a change specification for approval. |
| `$ndd-plan 001` | `/ndd-plan 001` | Turn an approved specification into a task and verification plan for approval. |
| `$ndd-do 001` | `/ndd-do 001` | Complete all remaining tasks and verification in an approved, current plan. |
| `$ndd-help` | `/ndd-help` | Show this reference, even before setup. |
| `$ndd-review 001` | `/ndd-review 001` | Review the latest available stage; show findings in chat and offer to save them. |

Workflow: describe → spec → user approves spec → plan → user approves plan → implement and verify.

Specs contain a goal and acceptance-criteria checklist; plans contain an approach and tasks/checks. Extra sections appear when useful, and existing longer documents still work. `ndd-do 001 T2` limits execution to T2; `ndd-do 001` continues through the plan unless blocked or separate authorization is needed.

Review is optional: it neither grants approval nor replaces verification. It accepts an optional feature and optional `spec`, `plan`, or `code` mode in either order. Without a feature, it proposes the highest-numbered specification for the current prefix and asks for confirmation.

Illustrative IDs and file locations:

- `001` uses the confirmed prefix: for example, prefix `ak` resolves it to `ak-001`. Confirm a prefix through setup, or supply a qualified ID when none is configured.
- `ak-001` explicitly selects a prefix and number, including a teammate's task. Numbers advance separately per prefix; ambiguous matches require a full name/path.
- Documents normally live in `specs/ak-001-fix-csv-export/`: `spec.md`, `plan.md`, and optionally `review.md`. Project conventions or an explicit output path may choose another location. These are ordinary files Git can track unless ignored; existing code need not be rewritten as specs.
