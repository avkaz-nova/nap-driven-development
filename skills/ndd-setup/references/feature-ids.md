# Prefixes and feature identifiers

Task folders (features, bugs and other changes) use `PREFIX-NNN-feature-slug`, for example
`ak-001-fix-csv-export`. The full folder name is the spec's `id`; set its `owner`
to the confirmed prefix. Numbers start at `001` and advance separately for each
prefix. The prefix identifies a naming namespace, not an authenticated identity.

## Read only the applicable procedure

Only `ndd-setup` or an explicit prefix-setting request needs
[prefix setup and registration](prefix-setup.md). Other commands do not load it.
Read the saved prefix using `git config --local --no-includes --get-all ndd.prefix`.
Exit 1 with no value means unset; report other errors. A valid value is one
2–16 character lowercase ASCII alphanumeric string starting with a letter.
Multiple/invalid values are errors; only setup may change settings. An explicit
qualified task ID/path needs no personal prefix.
For an existing task, use Resolve below; read Create only for a new task.

## Create a feature

`ndd-spec` reads the saved prefix, or uses one explicitly confirmed for this
project in the current conversation. If neither exists, ask the user to run
`ndd-setup`; do not guess a prefix or save settings from the spec phase.

Choose the root using the [document location rules](project-state.md), defaulting
to `ndd-specs/` for new NDD work while retaining established `specs/` projects.
Inspect that root. Exclude the reserved `project/` context
folder from numbering and candidate selection. Choose one greater than the largest
visible number for that prefix (minimum three digits). Check the whole
`PREFIX-NNN` identifier, not just the proposed slug: `ak-001-one` and `ak-001-two`
must not be created as separate new tasks when either is already visible.
Recheck before creation and never overwrite another spec. Use the prefixed name
also for a new feature in an explicitly requested output directory. Do not rename
existing features or change their ids/owners when revising them.

Prefixes reduce collisions between teammates; they cannot reserve numbers across
unseen branches or clones. Two people using the same prefix, or one person working
in parallel, can still collide. Report visible duplicate identifiers. Resolving
an existing duplicate requires an explicitly approved rename and reference review;
never silently renumber tasks, merge their documents or choose one by slug order.

## Resolve a feature for plan/do

Read these rules before resolving an id. `project/` and its documents are not
feature candidates, including for an explicit path: use `ndd-init` for project
documents and choose a concrete task for plan/do/review. First select the root
using the [document location rules](project-state.md). Ambiguous roots require
an explicit root or path, including for latest-task selection in review.
Do not search unrelated roots.

1. A path to the required document, or an exact full folder name such as
   `ak-001-fix-csv-export`, selects that feature directly. No personal prefix is
   needed to work on a teammate's feature.
2. A qualified id such as `ak-001` selects matching prefixed feature folders.
   Require exactly one match; otherwise list candidates and ask for the full path.
3. A bare number such as `001` uses the current confirmed/saved prefix: for `ak`,
   resolve `ak-001`. With zero matches, report that result; do not fall back to
   another person's feature or an unprefixed legacy feature with the same number.
4. With no confirmed prefix, a bare number may resolve a single unprefixed legacy
   feature (`001-old-feature`) only when there are no prefixed matches for that
   number. Otherwise ask for a qualified id/path or setup. Do not infer the current
   user from whichever folder happens to match.

Validate saved settings on read, but only setup may change them. Report invalid
or ambiguous settings and allow an explicit feature id/path to avoid guessing.
Show the resolved feature path before planning or implementation. Preserve all
existing approval, spec-digest and task verification gates.
