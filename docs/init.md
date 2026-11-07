# Start with a project idea

Start with `ndd-setup` to check readiness and choose your task prefix. For a new
project, optionally use `$ndd-init` in Codex or `/ndd-init` in Claude Code to
discuss its purpose, main capabilities and/or rules. For an existing project,
skip init and use `ndd-spec` → `ndd-plan` → `ndd-do` for the next change.

Workflow: setup → init (optional, new project only) → spec → approve → plan → approve → do + verify.

Init itself does not require Git or a saved prefix. Repeat it when you explicitly
want to revise the project documents you previously created.

Examples (use `/` in Claude Code):

```text
$ndd-init
$ndd-init I want to build a workout tracker
$ndd-init Only project rules: English interface and Russian documentation
$ndd-init Add a capability overview using our existing project description
```

These are ordinary requests, not flags or required modes.

## Conversation and document choice

The agent first reads existing project context and asks what you want to build,
for whom and what main problem it solves. It asks only material follow-ups,
up to three at a time, without requiring a full roadmap or stack selection.
For a rules-only request, it discusses rules without demanding a product spec.

After the discussion it recommends the smallest useful selection:

| Optional file | Content |
|---|---|
| `specs/project/spec.md` | Purpose, users, main scenarios, first working scope and known constraints. |
| `specs/project/features.md` | Detailed main capabilities, intended stages, current status and links to concrete tasks. |
| `specs/project/rules.md` | Agreed conventions such as interface/documentation language or technical boundaries. |

Choose any combination, or none. If you already selected the files in your
request, the agent does not ask you to choose again. No empty placeholders are
created. Each capability can link to several feature, bug or maintenance specs;
an idea does not need a task spec yet, and an unrelated bug needs no capability.

The agent shows the selected drafts together. One approval saves the displayed
set. Selecting filenames alone does not approve their content. On repeat init,
it proposes changes while preserving unselected files, user notes and task links.
Material changes to product direction or rules are reviewed, not inferred from
a task update. No code, Git initialization, prefix setting or task plan is created.

## Location and ongoing work

The `project/` folder sits beside numbered task folders, not above a `features/`
directory. An established alternative specs root uses the same sibling layout.
Existing task paths are preserved. Project documents have no feature number,
task approval metadata or implementation plan.

```text
specs/
├── project/
│   ├── spec.md
│   ├── features.md
│   └── rules.md
├── ak-001-record-workout/
│   ├── spec.md
│   └── plan.md
└── ak-002-fix-duration/
    ├── spec.md
    └── plan.md
```

After saving, the agent can suggest a first or next task and offer to prepare
its specification. Your choice starts `ndd-spec`; the usual prefix, spec and
plan approvals still apply. Project-document approval never approves code work.

Spec, plan and do read existing project context and refresh relevant links and
progress in an existing `features.md` as part of the command. They do not create
missing project documents or rewrite your purpose, stage assignments or rules.
Review reads this context and reports stale entries without editing them.
Setup does not synchronize progress, and help does not inspect the project.

A capability entry can include a description followed by:

```markdown
- Stage: MVP
- Status: in progress
- Tasks:
  - [ak-001-record-workout](../ak-001-record-workout/spec.md) — in progress
  - [ak-002-fix-duration](../ak-002-fix-duration/spec.md) — draft
```

Stages such as MVP/Later express priorities; task progress reflects actual spec
and plan state. Draft specs, spec approval, readiness, implementation and verified
completion are distinct. A stale plan or missing evidence is marked for review;
one completed task never completes an entire capability. Known bugs affecting
its scope remain visible. Unclear task associations are resolved with you rather
than guessed. Failed overview writes are reported without discarding valid work.

Synchronization happens when commands run, not in the background. Manual changes
may leave the overview stale until the relevant entries are checked. Init can
refresh the selected overview across its existing links and show the proposed
update for approval.

Project rules complement existing `AGENTS.md`/`CLAUDE.md` instructions within the
host's precedence; contradictions are surfaced. Documentation language and
interface language are separate choices. Fixed help remains English.
