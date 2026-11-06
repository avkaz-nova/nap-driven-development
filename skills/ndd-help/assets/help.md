NDD {{VERSION}} is a simple spec-driven workflow: describe a change, agree on a short specification and plan, then complete the approved plan and verify it.

These are chat commands, not terminal commands. Codex uses `$`; Claude Code uses `/`.

| Codex example | Claude Code example | Purpose |
|---|---|---|
| `$ndd-setup` | `/ndd-setup` | Inspect setup and confirm a personal feature prefix; approve configuration changes before saving. |
| `$ndd-spec Fix CSV export` | `/ndd-spec Fix CSV export` | Prepare a change specification for approval. |
| `$ndd-plan 001` | `/ndd-plan 001` | Turn an approved specification into a task and verification plan for approval. |
| `$ndd-do 001` | `/ndd-do 001` | Complete all remaining tasks and verification in an approved, current plan. |
| `$ndd-help` | `/ndd-help` | Show this reference, even before setup. |
| `$ndd-review 001` | `/ndd-review 001` | Review the latest available stage; show findings in chat and offer to save them. |

Workflow: describe → spec → user approves spec → plan → user approves plan → implement and verify.

Specs contain a goal and acceptance-criteria checklist; plans contain an approach and tasks/checks. Extra sections appear when useful, and existing longer documents still work.

Executing a plan (examples use Codex; use `/` instead of `$` in Claude Code):

| Example | What runs |
|---|---|
| `$ndd-do 001` | All remaining tasks in order, followed by final verification. |
| `$ndd-do 001 T2` | Only task T2 and its required checks; stops afterward. |
| `$ndd-do ak-001 T2` | Only T2 in the explicitly selected feature ak-001. |

`001` is the feature number; `T2` is a task ID from its `plan.md`. For a plan with T1, T2 and T3, if T1 is complete, `ndd-do 001` continues with T2 and T3. To do only T2, use `ndd-do 001 T2`; a later `ndd-do 001` resumes the remaining work. If T2 needs an unfinished T1, the agent reports that prerequisite instead of silently doing T1. Execution requires an approved, current plan and stops for blockers, scope changes or actions needing separate authorization.

Review is optional: it neither grants approval nor replaces verification.

| Example | What is reviewed |
|---|---|
| `$ndd-review 001` | The latest available stage: code, plan or spec. |
| `$ndd-review 001 spec` | The specification: clarity, contradictions and acceptance criteria. |
| `$ndd-review 001 plan` | The plan against the spec: coverage, tasks and verification. |
| `$ndd-review 001 code` | The implementation against the spec and plan. |
| `$ndd-review plan ak-001` | The same plan review with mode first and an explicit prefix. |
| `$ndd-review` | Proposes the highest-numbered specification for the current prefix and asks for confirmation. |

Review reports findings in chat without changing code or running tests, then offers to save `review.md`.

Illustrative IDs and file locations:

- `001` uses the confirmed prefix: for example, prefix `ak` resolves it to `ak-001`. Confirm a prefix through setup, or supply a qualified ID when none is configured.
- `ak-001` explicitly selects a prefix and number, including a teammate's task. Numbers advance separately per prefix; ambiguous matches require a full name/path.
- Documents normally live in `specs/ak-001-fix-csv-export/`: `spec.md`, `plan.md`, and optionally `review.md`. Project conventions or an explicit output path may choose another location. These are ordinary files Git can track unless ignored; existing code need not be rewritten as specs.
