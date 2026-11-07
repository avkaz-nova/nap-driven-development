---
name: ndd-plan
description: Create or revise a technical plan and verifiable tasks for an approved NDD specification. Invoke explicitly with ndd-plan; this phase does not implement code.
argument-hint: "<feature id | path to spec.md>"
disable-model-invocation: true
---

# ndd-plan

Respect applicable global, project and nested instructions (`AGENTS.md`,
`CLAUDE.md` and scoped rules), following the host's instruction precedence.
If an unresolved conflict blocks the requested work, explain the specific
contradiction and pause the affected work; do not silently bypass or rewrite rules.

Edit the task's `plan.md` and relevant links/statuses in an existing project
capability overview. Read applicable project instructions and the
feature's spec. No manifest or copied project templates are required. If legacy
NDD files exist, follow the [existing-project guidance](../ndd-setup/references/project-state.md).
Resolve the feature with the shared
[prefix and identifier rules](../ndd-setup/references/feature-ids.md): `001` uses
the current user's confirmed prefix; `ak-001` or a full folder name/path selects
an explicit feature. Report the resolved path; never guess between matches.
Follow the [project context and overview rules](../ndd-setup/references/project-context.md)
for optional context, document language and synchronization. Use the project's
existing tools. Without a chosen document language, use the user's language.

1. Require spec status `approved` or `in-progress`, and no unresolved
   `[NEEDS CLARIFICATION]`. `in-progress` supports revising an implementation
   plan without resetting the agreed behaviour. A changed spec must be approved
   again through `ndd-spec`. A done feature needs an explicitly approved revision.
2. Reuse the spec-phase findings, then inspect affected implementation, tests
   and configuration needed for concrete tasks. Recheck uncertain or changed
   assumptions; do not repeat a broad project scan. Do not run unfamiliar jobs,
   migrations or verification commands before checking their external effects.
3. Use `../ndd-setup/assets/plan.md` relative to this loaded skill's directory.
   Do not select project templates or copy a template folder into the project.
   If that bundled asset is missing, report an incomplete installation and stop.
   Create/revise the plan from it. For ordinary tasks aim for 100–250 words or
   fewer, expanding only for concrete complexity or risk. Respect project rules.
   Use a short approach and an execution checklist. Mention files/contracts in
   tasks instead of duplicating them in a components section. Include risks,
   rollback or decisions only when there is something material to explain.
4. Write ordered tasks with stable T ids, each referencing the AC ids it covers
   and a concrete verification command or observation. Include prerequisites
   only when ordering is insufficient. Keep related implementation and tests
   together; do not split trivial steps into separate tasks. Existing R/AC
   documents remain supported without migration or renumbering.
5. Ensure every AC has a task and a way to verify the assembled feature. Put
   this coverage in the tasks; do not add a duplicate coverage table. Add a final
   integration check only where task checks are insufficient. Include required
   project checks and distinguish release acceptance from later measurements.
6. Compute `spec_digest` using this skill's read-only helper:
   - macOS/Linux: `bash <this-skill>/scripts/spec-digest.sh <spec-path>`
   - Windows: `powershell -NoProfile -File <this-skill>/scripts/spec-digest.ps1 -Path <spec-path>`
   Quote paths. Use `pwsh` if that is the installed PowerShell. Stop on failure;
   never make up a checksum. The helpers hash the Markdown body as UTF-8/LF,
   ignoring BOM, frontmatter and trailing blank lines, with one final LF.
7. Set the plan `status: draft`, synchronize the relevant existing overview entry,
   and show the short plan once (or changed parts),
   without repeating it in a summary, and ask for review. On explicit approval of
   this version, set `status: approved`.
   A chat approval is enough; the agent records it and refreshes the overview
   progress after checking plan currency. A draft plan never means ready.
   Next: `ndd-do <feature id>`.

If an existing plan is revised, preserve completed tasks and verification
history that remain valid. Reopen affected tasks and explain why. A changed
approach or task scope requires new approval; a small implementation adjustment
within approved scope can be recorded later in Decisions by `ndd-do`.

If the spec is incomplete or contradictory, report the proposed correction and
stop. Do not edit the spec or rewrite requirements to fit an implementation.

When a diagram clarifies architecture, dependencies or execution flow, use the
[rounded Unicode diagram style](../ndd-setup/references/diagrams.md).
