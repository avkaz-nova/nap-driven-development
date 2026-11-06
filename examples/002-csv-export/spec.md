---
id: 002-csv-export
status: approved
owner: example
created: 2026-11-06
---

# Export a task list to CSV

Let users open their visible task list in a spreadsheet without copying rows.
This is an illustrative specification, not a completed implementation.

## Acceptance criteria
- AC1: Export visible tasks in displayed order as UTF-8 CSV with `title,status`
  columns. A CSV reader reconstructs exact values for Unicode titles and fields
  containing commas, quotes or line breaks.
- AC2: An empty view produces the header only, with no data rows.
- AC3: Task data and displayed order stay unchanged after export or save cancellation.

## Out of scope
Import, scheduling, additional columns and spreadsheet styling.
