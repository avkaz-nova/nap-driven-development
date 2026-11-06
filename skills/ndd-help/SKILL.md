---
name: ndd-help
description: Return the fixed English NDD command reference, workflow and feature ID explanation. Invoke explicitly with ndd-help, before or after setup, including outside a project.
disable-model-invocation: true
---

# ndd-help

Respect applicable global, project and nested instructions (`AGENTS.md`,
`CLAUDE.md` and scoped rules), following the host's instruction precedence.
If an unresolved conflict blocks the requested work, explain the specific
contradiction and pause the affected work; do not silently bypass or rewrite rules.
For help, use instructions already in context; do not inspect the project.

Return the predefined reference verbatim, with only the version substituted:

1. Read [help text](assets/help.md) and [kit version](../ndd-setup/VERSION)
   relative to this loaded skill's location, preferably in one read operation.
2. Trim surrounding whitespace from the version. If it is absent, unreadable,
   or not a numeric `major.minor.patch`, use
   `version unavailable — incomplete installation` instead.
3. Replace `{{VERSION}}` in the help text with that value. Return the entire
   resulting text unchanged, without a preamble, summary, translation or code fence.

If the help text is missing or unreadable, report that resource error and stop;
do not reconstruct it. Do not search another installation or the network.

There are no modes, subcommands or required arguments. Extra text does not change
this reference or authorize another command. Do not ask questions, inspect the
project, run setup or change files/settings. The reference is intentionally fixed
English, regardless of the conversation language. Respect higher-priority
instructions; this skill does not change the host's reasoning settings.
