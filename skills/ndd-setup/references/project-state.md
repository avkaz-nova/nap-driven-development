# Existing projects and output locations

New NDD projects need no manifest, instruction block or project-local template.
The default document location is `ndd-specs/PREFIX-NNN-feature-slug/{spec,plan}.md`, created
only when a task specification is requested. Optional `project/` documents live
beside task folders; follow [project context rules](project-context.md). Task specs
and plans use the installed kit's `ndd-setup/assets` templates; generated task documents are independent of
the templates afterwards. Updating NDD does not rewrite those documents.
The confirmed personal prefix is a local Git setting, not a tracked project file;
see [prefixes and feature identifiers](feature-ids.md).

## Choose the document root

Use the same root for setup, init, spec, plan, do and review:

1. Honor an explicit safe document path or root selected by the user, and the
   project's applicable location instructions. An explicit existing task path
   selects its containing root for related project context; it does not move files.
2. Otherwise honor an existing legacy manifest's location as described below.
3. Without a selected location, inspect `ndd-specs/` and `specs/` only enough to
   identify existing NDD work. Use task metadata/content and NDD context already
   established by the user or project instructions; a folder name, `spec.md` or
   `project/` alone is not evidence of NDD ownership. Preserve recognizable
   legacy NDD tasks even when they lack current approval metadata.
   If exactly one root contains established NDD work, keep using it, including
   `specs/`. Existing project context alone can establish a root when its NDD
   purpose is clear. If both contain NDD work or ownership is uncertain, ask for
   the root or full task path before creating documents or resolving short IDs.
4. With no existing NDD root, use `ndd-specs/`. An unrelated `specs/` is left
   untouched and does not block this choice. If `ndd-specs/` itself is occupied
   by unrelated content, ask for another project-relative location.

Report the selected root and reuse it within the task. Number and resolve tasks
only in that root; do not merge roots or fall back to the other after a missing
ID. Init's `project/` folder and overview updates use the same root as the task.
Do not create a manifest or remember a root in new configuration. Existing
documents, IDs, links and templates remain in place; renaming or moving them
requires a separate explicit request.

## Existing NDD files

An existing `.ndd-kit.json` can be read for output-location compatibility:
- A manifest without a format field uses `specs/`.
- Format 2 has a `specs_dir` field. Honor that relative directory when safe.
- For unknown formats, report the uncertainty and ask for an explicit
  feature path instead of guessing, downgrading or overwriting the manifest.

Do not create or update manifests, their metadata, managed hashes or agents
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

If `ndd-specs/` already serves another purpose or project rules require a different
location, ask the user to name a project-relative feature path. No configuration
file is necessary: later commands can receive that spec/plan path explicitly.
When a short id is ambiguous, ask for the path rather than choosing a folder.
Do not recursively search unrelated projects or global directories for a match.

## Removal

Machine uninstall removes installed skills and their installation state. With
both agents selected, it also removes the verified clean NDD clone containing
the installer, unless `--keep-source` / `-KeepSource` is requested. Unverified or
modified clones are kept with an explanation; other downloads are not searched.
Full uninstall first clears registered, unchanged local `ndd.prefix` values
using `~/.ndd/projects`; unresolved records are retained with warnings and do not
stop removal. It does not
scan the machine or change legacy templates, manifests, blocks, feature documents,
source code, or other Git settings. Single-agent uninstall preserves the shared registry.
