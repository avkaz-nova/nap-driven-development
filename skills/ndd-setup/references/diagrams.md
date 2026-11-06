# Diagrams and visual explanations

When a diagram helps explain architecture, a workflow, relationships or another
part of the task, use an editable Unicode text diagram with rounded boxes.
Apply this in chat responses, specifications, plans and other requested docs.
Use a different format when the user requests it. Do not add a diagram merely
to fill a section, or put implementation architecture into a behaviour-only spec.

- Put the diagram in a fenced `text` code block to preserve monospace alignment.
- Use `╭ ╮ ╰ ╯` for rounded corners, `─ │` for borders, and directional arrows
  such as `→ ▼ ◀`. Use `┬ ┴ ├` for connected branches and merges.
- Keep labels concise, connectors aligned and the diagram narrow enough to read
  comfortably in a note. Show branching, merging and return paths explicitly.
- Explain what the diagram means in the surrounding text. It supplements the
  requirements or explanation rather than replacing verifiable written criteria.

Adapt the topology and labels to the actual task. Example style:

```text
      ╭─────╮
      │  1  │◀────────────╮
      ╰──┬──╯             │
         ▼                │
      ╭─────╮             │
      │  2  │             │
      ╰──┬──╯             │
    ╭────┴────╮           │
    ▼         ▼           │
 ╭─────╮   ╭─────╮        │
 │  3  │   │  4  │        │
 ╰──┬──╯   ╰──┬──╯        │
    ╰────┬────╯           │
         ▼                │
      ╭─────╮             │
      │  5  │─────────────╯
      ╰─────╯
```
