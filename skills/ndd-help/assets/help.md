NDD: describe a change, approve its spec and plan, then implement and verify.
These are chat commands: `$` in Codex, `/` in Claude Code.

| Codex | Claude Code | Purpose |
|---|---|---|
| `$ndd-setup` | `/ndd-setup` | Check readiness and confirm your task prefix. |
| `$ndd-init` | `/ndd-init` | Optional, for a new project: agree on purpose, main capabilities and/or rules. |
| `$ndd-spec Fix CSV export` | `/ndd-spec Fix CSV export` | Write a feature, bug or change spec for approval. |
| `$ndd-plan 001` | `/ndd-plan 001` | Prepare an implementation plan for approval. |
| `$ndd-do 001` | `/ndd-do 001` | Complete all remaining tasks and verification in an approved plan. |
| `$ndd-review 001` | `/ndd-review 001` | Optional review of the latest available stage: spec, plan or code. |
| `$ndd-help` | `/ndd-help` | Show this reference. |

Workflow: setup → init (optional, new project only) → spec → approve → plan → approve → do + verify.
For an existing project, skip init.

Common variations (use `/` instead of `$` in Claude Code):

| Example | Meaning |
|---|---|
| `$ndd-init Build a workout tracker` | Start from an idea; choose any project documents before saving. |
| `$ndd-init only rules` or `$ndd-init only features` | Choose just rules or the capability overview. |
| `$ndd-spec specs/ak-001-export/spec.md` | Revise an existing spec. |
| `$ndd-do 001 T2` | Run only T2 and its checks, then stop. Required unfinished tasks are reported. |
| `$ndd-do ak-001 T2` | Select the task with an explicit prefix. |
| `$ndd-review 001 spec`, `$ndd-review 001 plan`, `$ndd-review 001 code` | Choose the review stage. |
| `$ndd-review plan ak-001` | Put the stage first and use an explicit prefix. |
| `$ndd-review` or `$ndd-review plan` | Propose the highest-numbered task for your prefix and ask before reviewing. |

`001` uses your confirmed prefix (for example, `ak-001`); `T2` is a task in `plan.md`.
Plan, do and review also accept a task document path. Later `ndd-do 001` resumes unfinished work.
Review does not approve or implement changes; saving `review.md` is optional.

Task documents live in `specs/<task>/`; optional project documents in `specs/project/`.
