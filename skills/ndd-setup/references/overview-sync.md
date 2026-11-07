# Capability overview and synchronization

## Describe capabilities

Keep `features.md` readable Markdown, not a second task database. For each main
capability use a stable heading/anchor, a short but substantive description of
user behaviour and boundaries, an intended stage (for example MVP or Later),
and status. Stage expresses product priority, not workflow progress. Add task
links only when specs exist. A useful entry looks like this:

```markdown
## CSV export

Users can export the filtered records with selected columns. The first working
scope supports CSV; scheduled exports are outside that scope.

- Stage: MVP
- Status: planned
- Tasks:
  - [ak-001-csv-export](../ak-001-csv-export/spec.md) — spec approved
  - [ak-003-fix-quotes](../ak-003-fix-quotes/spec.md) — draft
```

Adapt headings and prose to the chosen document language. Preserve existing
names, structure and stages. Do not require a capability ID or a new template.
Not every bug or maintenance task belongs to a main capability.

## Synchronize during task work

`ndd-spec`, `ndd-plan` and `ndd-do` may update only the relevant task links and
derived progress/status notes in an existing `project/features.md`, in addition
to their usual writes. This small update is part of those commands; it does not
need another approval prompt. It never authorizes changes to product scope,
stages, rules, task approvals or other tasks. `ndd-review` is read-only: report
stale overview entries, do not synchronize them. Init shows updates for approval
with its selected document drafts.

After creating/revising a task spec or recording a lifecycle/plan approval change,
refresh its existing overview entry. Link a new spec to an explicitly selected
or unambiguously matching capability. Preserve existing links and user notes;
do not create duplicates. If association is uncertain, ask while continuing
independent task work; leave the overview unchanged until resolved. An unrelated
bug need not be forced into the overview. Do not create a new capability or an
overview file without the user's requested project-document change.

Read the current linked spec and, when present, plan before deriving progress:

| Task evidence | Task progress label |
|---|---|
| Spec `clarifying` / `draft` | clarifying / draft |
| Spec approved, plan absent or draft (without a stale digest) | spec approved; planning needed |
| Spec approved, current approved plan | ready |
| Spec `in-progress`, current approved plan | in progress |
| Spec `done`, current plan and recorded completion/verification | done |
| Missing link target, stale plan, incomplete completion evidence or contradiction | needs review; explain why |

An absent plan is normal before planning, not a broken link. A draft plan is
not ready. A reopened spec takes precedence over its old plan. A stale plan
cannot be ready/in progress; check its digest with the installed helper when
using it to derive readiness. Missing tools mean readiness is unverified.
If implementation is blocked or checks fail, retain the underlying lifecycle
and add the concrete blocker; do not invent a new task frontmatter status.

Capability status is a summary of its described scope, not simply the latest
task's status: `idea` for proposed capabilities without implementation evidence,
`planned` once work is specified,
`in progress` when partially implemented or actively worked on, and `done` only
when the entire described scope is covered by completed, verified work. All
linked tasks being done is insufficient if part of the capability is unspecified
or unverified. For an open bug affecting a completed capability, retain the
completion history and show the current limitation/open fix; do not call it
fully done while a known defect violates its described scope. Use `needs review`
when the evidence cannot establish the current state, rather than guessing.

For an existing capability with no NDD task specs, record the observed behaviour
and its source (for example, an inspected entry point or project document), with
`existing; verification not recorded` when appropriate. Missing NDD specs do not
make existing functionality an idea. Inspection alone does not prove completion;
do not invent task links, approvals or passing checks to fill the overview.

Refresh only affected entries, inspecting their other linked tasks when needed
for the aggregate. Re-read before writing, preserve concurrent edits, and avoid
rewriting unchanged entries. If an overview update fails, keep valid task work,
report the unsynchronized overview and do not claim it was updated. These files
are refreshed by command invocations, not a background watcher; manual/external
changes can leave them stale until inspected.
