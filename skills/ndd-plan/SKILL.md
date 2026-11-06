---
name: ndd-plan
description: Create or revise a technical plan and verifiable tasks for an approved NDD specification. Invoke explicitly with ndd-plan; this phase does not implement code.
argument-hint: "<feature id | path to spec.md>"
disable-model-invocation: true
---

# ndd-plan

Edit only the feature's `plan.md`. Read applicable project instructions and the
feature's spec. No manifest or copied project templates are required. If legacy
NDD files exist, follow the [existing-project guidance](../ndd-setup/references/project-state.md).
Resolve the feature with the shared
[prefix and identifier rules](../ndd-setup/references/feature-ids.md): `001` uses
the current user's confirmed prefix; `ak-001` or a full folder name/path selects
an explicit feature. Report the resolved path; never guess between matches.
Use the user's language and the project's existing tools.

1. Require spec status `approved` or `in-progress`, and no unresolved
   `[NEEDS CLARIFICATION]`. `in-progress` supports revising an implementation
   plan without resetting the agreed behaviour. A changed spec must be approved
   again through `ndd-spec`. A done feature needs an explicitly approved revision.
2. Explore affected code, tests and configuration. Do not run unfamiliar jobs,
   migrations or verification commands before checking their external effects.
3. Use `../ndd-setup/assets/plan.md` relative to this loaded skill's directory.
   Do not select project templates or copy a template folder into the project.
   If that bundled asset is missing, report an incomplete installation and stop.
   Create/revise the plan from it. Describe the approach,
   affected components, relevant interfaces, risks and rollback; omit sections
   that add no value. Respect existing architecture and project rules.
4. Write ordered tasks with stable ids. Each names its R/AC coverage and a
   concrete verification step supported on the project's operating systems.
   Include prerequisites when order alone is insufficient; do not use `[P]`.
   A task should be a small, coherent change. Tests precede or accompany code
   where useful; docs/config changes can use other meaningful checks.
5. Map every AC to tasks and a final verification method. Include integration,
   error paths and any acceptance needing human observation. Distinguish
   deferred business measurements from checks required before completion.
6. Compute `spec_digest` using this skill's read-only helper:
   - macOS/Linux: `bash <this-skill>/scripts/spec-digest.sh <spec-path>`
   - Windows: `powershell -NoProfile -File <this-skill>/scripts/spec-digest.ps1 -Path <spec-path>`
   Quote paths. Use `pwsh` if that is the installed PowerShell. Stop on failure;
   never make up a checksum. The helpers hash the Markdown body as UTF-8/LF,
   ignoring BOM, frontmatter and trailing blank lines, with one final LF.
7. Set the plan `status: draft`, show the approach, tasks and risks, and ask for
   review. On explicit approval of this version, set `status: approved`.
   A chat approval is enough; the agent records it. Next: `ndd-do <feature id>`.

If an existing plan is revised, preserve completed tasks and verification
history that remain valid. Reopen affected tasks and explain why. A changed
approach or task scope requires new approval; a small implementation adjustment
within approved scope can be recorded later in Decisions by `ndd-do`.

If the spec is incomplete or contradictory, report the proposed correction and
stop. Do not edit the spec or rewrite requirements to fit an implementation.

When a diagram clarifies architecture, dependencies or execution flow, use the
[rounded Unicode diagram style](../ndd-setup/references/diagrams.md).
