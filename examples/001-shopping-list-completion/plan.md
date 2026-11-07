---
status: approved
spec_digest: a7788a1ba7ffc38180ae6fa28c24f39e8bf6e5504542fad6897e6273f4395679
---

# Plan: Shopping list completion

Spec: ./spec.md

Illustrative approved plan. Commands name tests that would be added to a host
project; they are not runnable tests supplied by this kit. No task is complete.

## Approach
Add a bought flag to the existing item model, defaulting missing values to false
when loading stored lists. Update items by their existing stable identifiers.
Keep filters as view state and derive visible rows without changing item order.
Save toggles through the existing storage boundary; on failure restore the prior
state and display an error that clears after a successful retry.

## Affected components and contracts
- Shopping item model and local-storage loading/saving.
- List rows, bought checkboxes, filter controls and empty/error messages.
- Existing identifiers and stored item fields remain unchanged.

## Risks and rollback
- Filtering must not overwrite the stored list with only visible items.
- Keep the new field optional when reading existing data. If the UI change is
  reverted, preserve item names, identifiers and order in storage.

## Tasks
- [ ] T1 (R1, R3, AC1, AC4): add bought state and backward-compatible loading — verify: `python -m pytest tests/test_shopping_storage.py`
- [ ] T2 (R1, R2, AC1, AC2, AC3): implement checkbox toggling and ordered filter views — verify: `python -m pytest tests/test_shopping_list.py`
- [ ] T3 (R4, AC5): restore state on save failures and support retry — verify: `python -m pytest tests/test_shopping_save_errors.py`
- [ ] T4 (R1–R4, AC1, AC2, AC3, AC4, AC5): verify the complete list flow, including reopening and failures — verify: `python -m pytest tests/test_shopping_flow.py`

## Acceptance coverage
| AC | Tasks | Final verification |
|---|---|---|
| AC1 | T1, T2, T4 | New item, repeated toggle and duplicate-name fixtures |
| AC2 | T2, T4 | Ordered rows before and after toggling within a filter |
| AC3 | T2, T4 | Empty views with unchanged underlying list data |
| AC4 | T1, T4 | Reopen saved data and load items without the bought field |
| AC5 | T3, T4 | Injected write failure followed by a successful retry |

## Verification results
None yet. The host project's required checks and UI review remain outstanding.

## Decisions
None yet.
