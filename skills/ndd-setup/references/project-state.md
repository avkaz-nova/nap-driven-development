# Existing projects and output locations

New NDD projects need no manifest, instruction block or project-local template.
The default document location is `specs/PREFIX-NNN-feature-slug/{spec,plan}.md`, created
only when a specification is requested. All skills use the installed kit's
`ndd-setup/assets` templates; the generated feature documents are independent of
the templates afterwards. Updating NDD does not rewrite those documents.
The confirmed personal prefix is a local Git setting, not a tracked project file;
see [prefixes and feature identifiers](feature-ids.md).

## Projects created by 0.1 or 0.2

An existing `.ndd-kit.json` can be read for output-location compatibility:
- Version 0.1 (no format field) used `specs/`.
- Format 2 has a `specs_dir` field. Honor that relative directory when safe.
- For unknown/newer formats, report the uncertainty and ask for an explicit
  feature path instead of guessing, downgrading or overwriting the manifest.

Do not create or update manifests, their version fields, managed hashes or agents
lists. Legacy `managed` entries do not authorize edits. Paths must stay inside
the project and must not traverse links into other locations. A supplied feature
path takes precedence over a manifest's default after these checks.

Existing `specs/_templates`, NDD instruction blocks and CLAUDE imports remain
untouched. Report that they are no longer needed for NDD itself. Do not remove
an import that may also load the team's own rules. Any cleanup is a separate,
explicitly approved change, never an automatic setup/update/uninstall action.
If an old block mandates project templates, flag the contradiction; propose its
minimal removal/update only after approval rather than silently ignoring it.

Old feature plans lacking approval/digest metadata require review through
`ndd-plan` before implementation. Preserve their completed work; setup must not
bulk-approve or rewrite specs/plans.

Existing unprefixed feature folders from any earlier NDD installation keep their
names and ids. Prefix selection does not migrate or rename them. Use their full
folder name/path when a short number would be ambiguous.

## Other output locations

If `specs/` already serves another purpose or project rules require a different
location, ask the user to name a project-relative feature path. No configuration
file is necessary: later commands can receive that spec/plan path explicitly.
When a short id is ambiguous, ask for the path rather than choosing a folder.
Do not recursively search unrelated projects or global directories for a match.

## Removal

Machine uninstall only removes installed skills and their installation state.
It does not scan or change projects, including legacy templates/manifests/blocks,
feature documents, source code or Git settings. The downloaded source checkout
is also preserved; it is not part of the installed copy.
