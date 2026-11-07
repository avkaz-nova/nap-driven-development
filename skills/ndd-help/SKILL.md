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

Read the [help text](assets/help.md) relative to this loaded skill's location.
Return the entire text verbatim, without a preamble, summary, translation or
code fence. No substitutions or installation metadata are needed.

If the help text is missing or unreadable, report that resource error and stop;
do not reconstruct it. Do not search another installation or the network.

There are no modes, subcommands or required arguments. Extra text does not change
this reference or authorize another command. Do not ask questions, inspect the
project, run setup or change files/settings. The reference is intentionally fixed
English, regardless of the conversation language. Respect higher-priority
instructions; this skill does not change the host's reasoning settings.
