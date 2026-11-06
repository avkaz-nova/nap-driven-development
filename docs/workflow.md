# Workflow and approvals

Each feature has two core files: `spec.md` describes the agreed behaviour;
`plan.md` contains implementation tasks, progress and verification results.

| Step | What happens |
|---|---|
| `ndd-spec <idea>` | Write or revise the spec and resolve open questions |
| Approve the spec | Confirm the current requirements in chat |
| `ndd-plan <id>` | Create a technical plan with tasks and checks |
| Approve the plan | Confirm the current approach and task scope in chat |
| `ndd-do <id>` | Complete all remaining approved tasks and verification |
| `ndd-help` | Show commands, version and ID rules, with no setup required |
| `ndd-review [feature] [mode]` | Optional review of spec, plan or implementation |

Use `/` before commands in Claude Code and `$` in Codex. A short id such as `001`
uses your [setup prefix](setup.md#your-prefix); a qualified id or full path selects
an explicit feature.

The agent records your approval in the documents. Calling the next command alone
does not approve a draft. An explicit “approve this plan and implement it” can
cover both actions without another confirmation.

## Compact documents

For an ordinary task, the spec is a goal plus an AC checklist, usually 150–300
words or fewer. Criteria include observable behaviour and relevant edge/failure
cases; there is no separate repeated requirements list. Add exclusions or open
questions only when needed.

The plan is a short approach plus tasks and checks, usually 100–250 words or fewer.
Each task names its AC coverage and verification, so no separate coverage table is
needed. Risks, rollback and decisions appear only when material. These are length
guidelines, not quotas: complex changes can need more detail. Existing R/AC specs
and longer plans remain valid without conversion or renumbering.

Spec creation inspects current behaviour; planning explores implementation details.
Implementation reuses those findings and rechecks changed files and assumptions.
Each document is shown once for approval, without a duplicate summary.

## Optional review

Use `ndd-review 001` to review the latest available stage of that feature. An
explicit `spec`, `plan` or `code` mode overrides detection and can come before or
after the feature. Without an ID, review proposes the highest number for your
confirmed prefix and waits for your confirmation; it does not select by date.

Review reads relevant files without editing them or running tests/builds. It
reports findings and limitations in chat, including stale plan checksums or
missing approvals, without changing them. It can review drafts and completed work.

Afterward choose whether to save `review.md` beside the feature's spec/plan.
For an existing report, choose replace, extend or do not save. Extend maintains
one checklist with stable finding IDs, preserves comments and adds new problems
without duplicates. Verified corrections become `[x] F1 — fixed` with date and
evidence; unchecked or out-of-scope findings are not silently closed. A changed
file requires a fresh choice before saving. No answer means no write.

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

`ndd-do 001` completes all remaining tasks in order and final verification.
`ndd-do 001 T2` limits execution to T2; unfinished prerequisites are reported,
not silently implemented. A completed task alone is not a reason to pause.
Stop for a blocker, scope change, stale approval/checksum or an action requiring
separate authorization. Continue in another session or agent using the same spec, plan and recorded results. No fresh session
is required. Commit, push, deployment and production actions need separate authorization.

Use focused checks during implementation, then required final project checks.
Reuse passing results only while relevant code, configuration, dependencies and
inputs are unchanged; rerun affected checks after changes. Record concise results
instead of repeating execution logs. A final response states changes, verification
and unresolved issues.

See the compact [CSV export example](../examples/002-csv-export/spec.md) and its
[plan](../examples/002-csv-export/plan.md).
