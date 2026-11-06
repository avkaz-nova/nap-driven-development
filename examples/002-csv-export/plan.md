---
status: approved
spec_digest: a9988029ab05ecfae477f11a7091c92afad010d46cc932c8318e6bd9bf7c8220
---

# Plan: CSV export

Spec: ./spec.md

Illustrative approved plan for a host application. No code or passing tests are
claimed. Adapt verification commands to that application's existing tooling.

## Approach
Use the platform's existing CSV writer on a read-only snapshot of visible tasks.
Keep serialization separate from the save action so fixtures can cover escaping
and empty input. Avoid a dependency if the stack already provides CSV support.

## Affected components and contracts
The task list's export action and its CSV serializer. Output columns are exactly
`title,status`; no changes to stored task records.

## Tasks
- [ ] T1 (R1, R2, AC1, AC2): serializer and round-trip/empty-input tests — verify: run the host project's serializer test target on all listed fixtures.
- [ ] T2 (R1, R3, AC1, AC3): connect the export action using current view order — verify: UI/integration test for filtered ordering and unchanged tasks on save/cancel.

## Acceptance coverage
| AC | Tasks | Final verification |
|---|---|---|
| AC1 | T1, T2 | Export the fixture view; read the file back and compare values/order |
| AC2 | T1 | Export an empty view and confirm only the header is present |
| AC3 | T2 | Compare task state and view order before/after save and cancellation |

## Verification results
None yet. Also run the host project's required final checks before marking done.

## Decisions
None yet.
