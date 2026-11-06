---
status: approved
spec_digest: dc8c3f78e286d4a494aa1c9565594306e9a6f3f156d1b291f4274c1f1c874818
---

# Plan: CSV export

Spec: ./spec.md

Use the host platform's CSV writer on a read-only snapshot of visible tasks.
Keep serialization separate from saving. This illustrative plan claims no
implementation or passing checks; adapt checks to the host application's tooling.

## Tasks
- [ ] T1 (AC1, AC2): Add the serializer and round-trip/empty-input tests — verify: run the serializer tests with Unicode, comma, quote, multiline and empty fixtures.
- [ ] T2 (AC1, AC3): Connect the export action after T1 — verify: export a filtered view, read back values/order and compare task state before/after save and cancellation; run the host project's required final checks.

## Results
Not run; example only.
