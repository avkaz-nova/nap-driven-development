---
name: ndd-spec
description: Create or revise an NDD feature specification describing expected behaviour and acceptance criteria. Invoke explicitly with ndd-spec; this phase does not implement code.
argument-hint: "<feature idea | path to spec.md> [output path in the request]"
disable-model-invocation: true
---

# ndd-spec

Create or revise `specs/PREFIX-NNN-feature-slug/spec.md`, or an explicitly requested
project-relative feature path. Until the user chooses to continue to planning,
this phase may edit only that specification and create its containing folder.
Read applicable project instructions in place; preserve unrelated work. Use the
user's language. No project manifest is required.
If a legacy manifest exists, follow the [existing-project guidance](../ndd-setup/references/project-state.md).

1. Resolve the project and feature using the shared
   [prefix and identifier rules](../ndd-setup/references/feature-ids.md).
   For a new feature, require a confirmed prefix, choose its next unused number,
   and set the spec's `id` to the full folder name and `owner` to the prefix.
   Only setup may save prefix settings. Keep output inside
   the project and do not write through links. If `specs/` belongs to another
   workflow, ask for an explicit feature path. If the input is an
   existing spec, keep its id, owner and created date. Use the standard template at
   `../ndd-setup/assets/spec.md`, relative to this loaded skill's directory.
   Never look for or copy templates in the project. If the bundled template is
   missing, report an incomplete NDD installation and stop before writing.
   Setup is a readiness check, not a required on-disk initialization marker.
2. Inspect only enough relevant code/interfaces to establish current behaviour
   and scope; leave implementation exploration to planning. Reuse reliable
   context already gathered rather than scanning the project again. Ask only
   questions affecting scope, observable behaviour or acceptance, at most three
   at a time. Do not repeat answered questions.
3. Write a compact spec using the bundled template. For ordinary tasks aim for
   150–300 words or fewer; this is a ceiling guideline, not a minimum or hard cap.
   Expand only for concrete complexity or risk, never to fill sections.
   - Goal: problem and expected outcome in 1–3 sentences.
   - Acceptance criteria: stable AC ids describing observable behaviour, important
     edge cases and failure paths. These are the requirements; do not repeat them
     in separate requirements or edge-case lists.
   - Out of scope: include only meaningful exclusions.
   - Questions: include only unresolved material questions, marked
     `[NEEDS CLARIFICATION]`; otherwise omit the section.
   Keep implementation choices in the plan. Required API names, formats and
   compatibility belong in the criteria when they affect observable behaviour.
   Existing specs with R ids and separate sections remain supported: preserve
   their structure and identifiers when revising; do not migrate merely for brevity.
4. Check ambiguity, contradictions, missing boundary cases and AC coverage.
   Use `clarifying` if material questions remain, otherwise `draft`.
5. Show the short spec once (or the changed parts when revising), without a
   duplicate summary, and ask for review. When ready for approval, offer
   "Approve spec and continue with Plan <id>", "Approve spec only", and
   "Request changes". Substitute the resolved qualified ID (e.g. `ak-001`),
   or the project-relative spec path when needed to avoid ambiguity. Use the
   host's interactive choice tool when available and allowed in the current mode;
   otherwise offer the choices in chat. Do not invent clickable Markdown links
   or require the user to type a skill command.
   Only an explicit response approves this version; a displayed/default choice
   or silence does not. Record `status: approved` after approval. If the user
   selects approve-and-continue, load the sibling [ndd-plan skill](../ndd-plan/SKILL.md)
   and follow it for that same feature in this conversation. This choice explicitly
   requests planning; the resulting plan still needs separate approval before
   implementation. Approval alone does not start planning: offer
   "Continue with Plan <id>" after an approve-only response and wait for selection,
   then perform the same handoff to `ndd-plan`.
   For a clarifying spec, resolve questions first without offering approval or
   continuation. A clear chat response is sufficient; do not require YAML edits.

When changing an existing approved/in-progress/done spec, return it to draft
(or clarifying), retain history/progress in the existing plan, and explain that
its tasks and approval must be reviewed again. Do not edit the plan here.
The plan's `spec_digest` will detect a changed Markdown body. All behavioural
requirements belong in that body, never only in frontmatter.

Editorial body changes also invalidate the digest; confirm and re-plan briefly
rather than silently bypassing the check. A lifecycle status change alone does
not invalidate it. The manual alternative is `ndd-plan <feature id>`.

When a diagram clarifies users, scenarios or behaviour, use the
[rounded Unicode diagram style](../ndd-setup/references/diagrams.md).
