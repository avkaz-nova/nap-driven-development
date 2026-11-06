# Workflow and approvals

Each feature has two files: `spec.md` describes the agreed behaviour;
`plan.md` contains implementation tasks, progress and verification results.

| Step | What happens |
|---|---|
| `ndd-spec <idea>` | Write or revise the spec and resolve open questions |
| Approve the spec | Confirm the current requirements in chat |
| `ndd-plan <id>` | Create a technical plan with tasks and checks |
| Approve the plan | Confirm the current approach and task scope in chat |
| `ndd-do <id>` | Implement and verify the next task; repeat to continue |

Use `/` before commands in Claude Code and `$` in Codex. A short id such as `001`
uses your [setup prefix](setup.md#your-prefix); a qualified id or full path selects
an explicit feature.

The agent records your approval in the documents. Calling the next command alone
does not approve a draft. An explicit “approve this plan and implement it” can
cover both actions without another confirmation.

## When requirements change

The plan stores a checksum of the spec body. If that body changes, implementation
stops for review and an updated plan. Status changes and line-ending differences
do not invalidate it; edits to the body do, including wording changes.

Changed requirements need spec approval again. Revise the affected tasks while
keeping completed work and evidence that remain valid. Changes to the approach
or scope need plan approval; small implementation decisions within approved scope
can be recorded in the plan.

If the code violates the agreed spec, fix the bug. Do not change the spec simply
to make it match the bug.

## Verification and continuing work

Each acceptance criterion needs a task and a final check. Checks can be tests,
builds or a recorded manual observation, depending on the change. Failed or missing
checks leave the task incomplete. The feature is marked `done` only after all
acceptance criteria, required project checks and the final diff are verified.

`ndd-do` handles one task by default; you can request several. Continue in another
session or agent using the same spec, plan and recorded results. No fresh session
is required. Commit, push, deployment and production actions need separate authorization.

See the [CSV export example](../examples/002-csv-export/spec.md) and its
[plan](../examples/002-csv-export/plan.md).
