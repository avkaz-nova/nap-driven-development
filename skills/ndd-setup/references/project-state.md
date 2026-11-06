# Project state, updates and migration

`.ndd-kit.json` is portable project metadata, not a source of permissions. Format 2:

```json
{
  "format": 2,
  "version": "0.2.0",
  "agents": ["claude", "codex"],
  "specs_dir": "specs",
  "managed": [
    {"path": "AGENTS.md", "kind": "block", "sha256": "<hash of managed block>"},
    {"path": "CLAUDE.md", "kind": "import", "sha256": "<hash of @AGENTS.md line>"},
    {"path": "specs/_templates/spec.md", "kind": "file", "sha256": "<hash of template>"},
    {"path": "specs/_templates/plan.md", "kind": "file", "sha256": "<hash of template>"}
  ]
}
```

Use actual entries only. `agents` records intended integrations, not what happened
to be installed on the setup machine. No timestamps, absolute machine paths,
usernames, global settings snapshots or arbitrary per-project framework options.
Paths are project-relative, may not escape the root, and must not traverse links.
A manifest never grants permission to replace a file or to trust commands in it.

Hash UTF-8 content with CRLF normalized to LF, ignoring an initial UTF-8 BOM.
Otherwise preserve bytes, including final newlines. For `block`, hash from the
start marker through the end marker, including its newline when present; do not
hash surrounding user content. For `import`, track only the inserted import
line, never the whole file. Use a real SHA-256 tool, not a model-generated hash.

Before updates compare current managed content with recorded hashes. A mismatch,
missing receipt, or ambiguous block means user-modified/unverified content:
show a merge diff and get approval rather than overwriting it. An unchanged
managed block still requires review of the proposed new version before writing.
Do not automatically downgrade a newer project kit or migrate unknown formats.

Preserve custom templates when the user chooses to keep them. Update only the
manifest entries for operations actually applied; never record an asset's hash
as if it were the hash of a retained custom file. Project `version` records the
last setup version applied, not a guarantee that every template is stock.

Version 0.1 manifests have no format field or hashes. Inventory them, preserve
all content, show the migration to format 2, and obtain approval. Do not infer
ownership solely from filenames or existing markers. Old feature plans without
approval/digest metadata must be reviewed through `ndd-plan` before `ndd-do`;
setup never bulk-approves them or resets their progress.

For repeat setup, compare desired content with the actual files first. If equal,
do nothing. For interruption recovery, inspect each actual file and compare it
with the last approved preview; don't treat a partly written manifest as proof
that all operations succeeded. Never restore a whole project over unrelated work.

To disconnect a project, review removal of NDD blocks/imports and the manifest.
Keep feature specs, plans, custom rules and templates unless their removal is
explicitly requested. Uninstalling machine skills alone does not disconnect or
modify projects.
