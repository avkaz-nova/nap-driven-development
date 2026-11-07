---
name: ndd-init
description: Discuss a new or existing project and create or revise optional project description, capabilities and rules in ndd-specs/project. Invoke with ndd-init; choose any document combination and approve the content before saving. Does not scaffold code or require setup.
argument-hint: "[project idea | requested documents or changes]"
disable-model-invocation: true
---

# ndd-init

Respect applicable global, project and nested instructions (`AGENTS.md`,
`CLAUDE.md` and scoped rules), following the host's instruction precedence.
If an unresolved conflict blocks the requested work, explain the specific
contradiction and pause the affected work; do not silently bypass or rewrite rules.

Help the user establish the project's purpose and direction. This is optional:
new and existing projects can use it at any time; ordinary tasks can use
`ndd-spec` without running init or creating project documents. Use the user's
language unless they choose another document language. No required arguments,
flags, Git repository, prefix or completed setup. Extra text describes the idea,
requested documents or changes; it is not a rigid subcommand syntax.

## Understand and propose

1. Identify the project root (Git root when available, otherwise the current
   folder), relevant local changes, existing instructions, README and project
   documents. For an existing project, inspect relevant entry points, structure,
   configuration and tests to understand its purpose and current capabilities.
   Summarize what the evidence establishes, distinguish inferred goals from
   confirmed decisions, and ask about material gaps or contradictions. Do not
   run application workflows or scan unrelated files to produce an overview.
   Follow [project context and overview rules](../ndd-setup/references/project-context.md)
   for location, scope, links and status updates. Preserve existing task paths.
   If a legacy manifest is present, use the
   [existing-project guidance](../ndd-setup/references/project-state.md) to resolve
   the established specs root without rewriting the manifest.
   Do not initialize Git, save a prefix, install dependencies or create code.
2. Reuse what is already known. For a new idea, ask what the user wants to build,
   for whom and what main problem it solves. Ask up to three material questions
   at a time, then clarify the first useful scope and known constraints as needed.
   Do not require a stack, complete roadmap or full questionnaire. For a request
   such as "only rules", discuss those rules without requiring a product spec.
3. Recommend the smallest useful document set and explain each file's purpose:
   - `spec.md`: purpose, users, main scenarios and current scope (or first working
     scope for a new idea); add known constraints and meaningful exclusions.
   - `features.md`: substantial descriptions of main product capabilities,
     intended stages, evidence-based status and links to task specs when present.
     A capability can have several feature, bug or other change specs. Ideas do
     not require task folders. Follow the shared reference's capability shape.
   - `rules.md`: only agreed project-wide conventions or constraints, such as
     interface/documentation language, stack or architecture boundaries. When
     rules already exist, propose relative links to their authoritative files
     with a short note about scope, rather than copying their contents. Verify
     each target and preserve scoped applicability. Only save these links if
     `rules.md` is selected and the displayed content is approved. Do not create
     a setup document, modify existing rule files or invent additional rules.
   Offer the recommended set, a smaller set or a changed selection using the
   host's choice UI when available, otherwise a short chat reply. Any nonempty
   combination is valid; no file is mandatory. Honor an already explicit choice
   without asking again. Declining all files leaves the project unchanged.

## Agree and save

Show concise drafts or a minimal revision of the selected documents, together.
Resolve material questions before asking to save. One explicit approval covers
the displayed set; selecting filenames alone does not approve their content.
Silence or a default choice does not authorize writes. Reuse approval already
given for that exact content; do not demand a separate confirmation per file.

Save only the approved files under `ndd-specs/project/` (or `project/` beside tasks
in the established alternative specs directory). Create directories only when
saving. Do not create empty files or copy task templates into this folder.
These are project documents, not an executable task: no feature ID, owner,
task approval frontmatter, plan or digest is required.

On repeat invocation, preserve current content, user notes, links and unselected
files. Re-read before saving and reconcile concurrent changes. Never silently
delete an unselected file or replace the whole folder. Refresh existing task
links/statuses in a selected `features.md` using evidence; show that refresh in
the proposed changes. If a project decision conflicts with existing task scope,
identify affected tasks for separate review; do not rewrite or approve their
specs/plans. Report failed writes and any partially saved set accurately.

Report the saved paths briefly. If useful, suggest a first or next task and
offer to continue to its specification. Only on the user's choice load the
sibling [ndd-spec skill](../ndd-spec/SKILL.md) for that task. Its prefix and
approval rules still apply; init does not create or approve tasks automatically.

When a diagram helps, use the
[rounded Unicode diagram style](../ndd-setup/references/diagrams.md).
