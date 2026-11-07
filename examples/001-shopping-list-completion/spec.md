---
id: 001-shopping-list-completion
status: approved
owner: example
created: 2026-11-07
---

# Mark shopping list items as bought

This is an illustrative, reviewed specification; the example has not been implemented.

## Problem and users
People using a shopping list need to distinguish what is still needed from what
they have already bought, without deleting items they may want to reuse.

## Requirements
- R1: Each item has a bought checkbox, initially unchecked. Toggling it changes
  only that item's state; items with identical names remain independent.
- R2: Provide All, Needed and Bought filters. All is selected when the list opens.
  Needed shows unchecked items; Bought shows checked items. Preserve the existing
  item order within each filter.
- R3: Save bought state using the list's existing local storage. Reopening the
  list restores item states. Existing stored items without a bought field are
  treated as unchecked.
- R4: If saving a toggle fails, restore the item's previous state and show a
  visible error. Do not display a success message or lose other list data.

## Non-goals
- Shared lists, account synchronization or a new storage backend.
- Automatic deletion or reordering of bought items.

## Edge cases
- Empty lists and filters with no matching items.
- Two items with the same name but different identifiers.
- Existing stored items without the new field; a storage write failure.

## Acceptance criteria
- AC1 (R1): A new item is unchecked. Toggling it twice restores its original state;
  another item with the same name is unchanged.
- AC2 (R2): For items A, B and C in that order, with B bought, All shows A/B/C,
  Needed shows A/C and Bought shows B. Toggling A while Needed is selected leaves
  only C visible; switching to Bought shows A/B in their original order.
- AC3 (R2): An empty list or a filter with no matches shows an empty-state message
  and no item rows. Switching filters does not modify stored items.
- AC4 (R3): Reopening a saved list restores bought states and selects All.
  Loading stored items without a bought field succeeds and shows them unchecked.
- AC5 (R4): An injected storage failure leaves the toggled item in its previous
  state, preserves the other items and displays an error. A later successful retry
  saves the change and clears the error.

## Open questions
None.
