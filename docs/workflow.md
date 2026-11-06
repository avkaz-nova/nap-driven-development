# Workflow contract

NDD uses `spec.md` and `plan.md` per feature. The spec describes agreed behaviour;
the plan describes implementation and stores progress and verification evidence.
No manifest, instruction-file changes or project template folder is required.
`ndd-spec` and `ndd-plan` use the standard templates bundled with `ndd-setup`.
Normal setup is an optional read-only readiness check. For older project locations,
see [existing-project guidance](../skills/ndd-setup/references/project-state.md).

| Operation | Required state | Result |
|---|---|---|
| Write/revise spec | User requests specification work | `draft` or `clarifying` |
| Approve spec | Explicit approval of current content, no material unknowns | `approved` |
| Create/revise plan | Spec `approved` or unchanged `in-progress` | Plan `draft`, current spec digest |
| Approve plan | Explicit approval of current approach/tasks | Plan `approved` |
| Implement | Spec `approved`/`in-progress`, approved current plan | Task evidence, spec `in-progress` |
| Complete | All tasks and all final AC/project checks verified | Spec `done` |

Chat approval is sufficient: the agent records it. Calling the next command alone
does not retroactively approve a draft. An implementation request that explicitly
approves the displayed plan can be recorded without another permission exchange.

## Change management

All behavioural content belongs in the Markdown body of the spec. The plan stores
`spec_digest`, computed by the helper shipped with `ndd-plan`. The helper excludes
YAML frontmatter, removes an initial UTF-8 BOM, normalizes CRLF to LF and removes
trailing blank lines, then hashes the body with one final LF. Lifecycle metadata
and host line endings don't invalidate the plan. Editorial body edits do; a brief
review is preferable to trying to infer semantic equality.

Changing requirements returns the spec to draft/clarifying. After approval,
re-plan affected work. Preserve valid completed tasks; reopen invalidated ones
with an explanation. Never reset all progress merely because the digest changed.
Legacy plans without status/digest metadata require review, not automatic approval.

A checksum catches stale documents, not malicious editing or falsified approval.
The user and agent still review the content. If the helper fails, implementation
stops instead of guessing or updating the stored digest to bypass the check.

If code disagrees with the spec, determine whether it is an implementation bug
or a requested behaviour change. Fix bugs against the agreed behaviour; do not
rewrite the spec just to match a bug. Behaviour changes require spec review.
Small implementation decisions within approved scope go in the plan's Decisions;
changes to the approach or scope require plan review.

## Verification and handoff

Every requirement and promised edge case has an AC. Each AC maps to a task and a
final check of the assembled feature. A check may be an automated test, a build,
a safe validation query or an explicit human observation. A task isn't complete
when its required checks are unavailable or failing.

Record commands/observations, results and limitations in the plan, without raw
private data. Keep later business hypotheses separate from release acceptance.
Before `done`, verify every AC, required project checks and the final diff.

One task per invocation is the default; the user can request several. A fresh
session is optional. Continue in the other agent by reading the same documents
and checking the same gates. Commit spec/plan updates with code when the user
chooses to commit; NDD itself does not authorize external actions.

## Diagrams

When useful for understanding behaviour, architecture or a workflow, use editable
Unicode text diagrams with rounded boxes and aligned arrows. Keep branching,
merging and return paths explicit. The four skills share the
[diagram style reference](../skills/ndd-setup/references/diagrams.md). User-requested
formats take precedence; a diagram is optional and does not replace written ACs.
