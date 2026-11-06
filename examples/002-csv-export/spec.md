---
id: 002-csv-export
status: approved
owner: example
created: 2026-11-06
---

# Export a task list to CSV

This is an illustrative reviewed specification, not a completed implementation.

## Problem and users
A user wants to open their task list in a spreadsheet without copying each row.

## Requirements
- R1: Export the currently visible tasks, in displayed order, with columns
  `title,status`. Use UTF-8 CSV; quote commas, quotes and line breaks correctly.
- R2: Exporting an empty view produces the header only.
- R3: Export must not change tasks or their order in the application.

## Non-goals
Import, background scheduling, additional columns and spreadsheet styling.

## Edge cases
Empty view, Unicode titles, commas, double quotes and multiline titles.

## Acceptance criteria
- AC1 (R1): A CSV reader reconstructs the exact visible titles and statuses in
  order, including Unicode, comma, quote and multiline fixtures.
- AC2 (R2): An empty view produces a CSV with `title,status` and no data rows.
- AC3 (R3): Task data and displayed order are unchanged after successful export
  and after the user cancels saving the file.

## Open questions
None.
