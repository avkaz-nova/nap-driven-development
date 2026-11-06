# NDD — Nap-Driven Development

![Nap-Driven Development — a developer and cat nap while two robot assistants plan and code](docs/assets/nap-driven-development.png)

[![CI](https://github.com/avkaz/nap-driven-development/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/avkaz/nap-driven-development/actions/workflows/ci.yml)

NDD helps **Claude Code and Codex** implement changes that match your requirements.
It keeps the scope, tasks and verification results in your project, so you can
continue work across sessions or switch agents. Available on **Mac and Windows**.

Use it in an existing project, with its current structure, tools and rules.
NDD respects global, project and nested instructions, including `AGENTS.md` and
`CLAUDE.md`, and surfaces conflicts before proceeding with affected work.

```text
╭──────────╮   ╭──────────────╮   ╭──────────────╮   ╭───────────╮   ╭────────╮
│ Describe │ → │ Approve spec │ → │ Approve plan │ → │ Implement │ → │ Verify │
╰──────────╯   ╰──────────────╯   ╰──────────────╯   ╰───────────╯   ╰────────╯
```

**Example: export tasks to CSV.** The spec defines column order, correct quoting,
and empty-list behavior. The plan connects each requirement to implementation
tasks and checks. You approve both before the agent changes code, then review the
verification results. See the [example spec](examples/002-csv-export/spec.md) and
[plan](examples/002-csv-export/plan.md)—illustrative documents, not a completed demo.

[Download v0.5.0 (public preview)](https://github.com/avkaz/nap-driven-development/releases/tag/v0.5.0)
or install with Git below.

## Install

Install once on each computer. You need **Git** and **Claude Code or Codex**.

<details>
<summary><strong>Install for Mac</strong></summary>

Open **Terminal**.

**1. Download NDD:**

```bash
git clone https://github.com/avkaz/nap-driven-development.git
```

**2. Open the downloaded folder:**

```bash
cd nap-driven-development
```

**3. Installation options:**


<details>
<summary>Install for both agents</summary>

Optional preview:

```bash
bash ./install.sh --all --dry-run
```

Install:

```bash
bash ./install.sh --all
```

</details>

<details>
<summary>Install only for Codex</summary>

Optional preview:

```bash
bash ./install.sh --codex --dry-run
```

Install:

```bash
bash ./install.sh --codex
```

</details>

<details>
<summary>Install only for Claude Code</summary>

Optional preview:

```bash
bash ./install.sh --claude --dry-run
```

Install:

```bash
bash ./install.sh --claude
```

</details>

</details>

---

<details>
<summary><strong>Install for Windows</strong></summary>

Open **PowerShell**.

**1. Download NDD:**

```powershell
git clone https://github.com/avkaz/nap-driven-development.git
```

**2. Open the downloaded folder:**

```powershell
cd nap-driven-development
```

**3. Installation options:**


<details>
<summary>Install for both agents</summary>

Optional preview:

```powershell
powershell -NoProfile -File .\install.ps1 -All -DryRun
```

Install:

```powershell
powershell -NoProfile -File .\install.ps1 -All
```

</details>

<details>
<summary>Install only for Codex</summary>

Optional preview:

```powershell
powershell -NoProfile -File .\install.ps1 -Codex -DryRun
```

Install:

```powershell
powershell -NoProfile -File .\install.ps1 -Codex
```

</details>

<details>
<summary>Install only for Claude Code</summary>

Optional preview:

```powershell
powershell -NoProfile -File .\install.ps1 -Claude -DryRun
```

Install:

```powershell
powershell -NoProfile -File .\install.ps1 -Claude
```

</details>

If Windows blocks the script, see [Windows installation help](docs/installation.md#windows-execution-policy).

</details>

---

Restart your agent after installation.

[Custom installation folders and troubleshooting →](docs/installation.md)

<details>
<summary>No Git? Download a ZIP instead</summary>

1. Open the [v0.5.0 release](https://github.com/avkaz/nap-driven-development/releases/tag/v0.5.0) and download **ndd-kit-0.5.0.zip** from **Assets**.
2. Extract the ZIP and open Terminal or PowerShell in the extracted folder.
3. Run **step 3** from the Mac or Windows instructions above.

</details>

## Use

Run these commands in your agent's chat. Codex uses `$`; Claude Code uses `/`.

| Action | Codex | Claude Code |
|---|---|---|
| Check project and choose prefix | `$ndd-setup` | `/ndd-setup` |
| Describe a change | `$ndd-spec Fix CSV export` | `/ndd-spec Fix CSV export` |
| Plan an approved spec | `$ndd-plan 001` | `/ndd-plan 001` |
| Complete an approved plan | `$ndd-do 001` | `/ndd-do 001` |
| Execute only task T2 | `$ndd-do 001 T2` | `/ndd-do 001 T2` |
| Review the latest stage | `$ndd-review 001` | `/ndd-review 001` |
| Review a specific stage | `$ndd-review 001 plan` | `/ndd-review 001 plan` |
| Show command reference | `$ndd-help` | `/ndd-help` |

Approve the spec and plan in chat before proceeding. After showing a spec, the
agent offers **Approve spec and continue with Plan** for that feature. Selecting
it approves the spec and starts planning; the plan still needs its own approval.
Interactive choices depend on the host; a short chat reply also works.

`ndd-do 001` completes all remaining tasks and final verification.
`ndd-do 001 T2` runs only T2 and its checks, then stops. Unfinished prerequisites
are reported; a later `ndd-do 001` resumes the remaining work.

Review is optional. Use `spec`, `plan` or `code` to select a stage, for example
`ndd-review 001 spec` or `ndd-review 001 code`. Findings appear in chat, with an
option to save `review.md`. Review does not run tests or replace approval and
verification. `ndd-help` includes more examples and works before setup.

## Feature IDs and files

Setup confirms a personal prefix such as `ak` and saves it as local Git config
`ndd.prefix`. Then `001` means `ak-001`; use `iv-001` to select another prefix.
Numbers advance separately per prefix. Each clone needs its own setup.

```text
specs/
└── ak-001-fix-csv-export/
    ├── spec.md
    ├── plan.md
    └── review.md  (optional)
```

Specs contain a goal and acceptance criteria; plans contain tasks and checks.
Create them only for changes you choose. These are ordinary files you can commit
with your code. NDD preserves existing `AGENTS.md` / `CLAUDE.md` instructions and
does not commit, push or deploy automatically.

## Update

In your cloned NDD folder, download the latest changes:

```sh
git pull --ff-only
```

If you used a ZIP, download and extract a fresh copy instead of running `git pull`.


<details>
<summary><strong>Update for Mac</strong></summary>

<details>
<>
<summary>Update NDD for both agents</summary>

```bash
bash ./install.sh --all
```

</details>

<details>
<summary>Update NDD for Codex only</summary>

```bash
bash ./install.sh --codex
```

</details>

<details>
<summary>Update NDD for Claude Code only</summary>

```bash
bash ./install.sh --claude
```

</details>

</details>

---

<details>
<summary><strong>Update for Windows</strong></summary>

<details>
<summary>Update NDD for both agents</summary>

```powershell
powershell -NoProfile -File .\install.ps1 -All
```

</details>

<details>
<summary>Update NDD for Codex only</summary>

```powershell
powershell -NoProfile -File .\install.ps1 -Codex
```

</details>

<details>
<summary>Update NDD for Claude Code only</summary>

```powershell
powershell -NoProfile -File .\install.ps1 -Claude
```

</details>

</details>

---

If you installed to custom folders, use the same destination options again.

Restart the agent after updating. Existing project specs and plans stay unchanged.

## Uninstall

Run from the downloaded NDD folder using the latest installer. Choose one option
below. Optional previews show the planned actions without deleting anything.

Paths below use `~` for your home folder and assume the default installation
locations. If you used custom destinations or `CLAUDE_CONFIG_DIR`, use the same
settings when uninstalling; see [installation options](docs/installation.md).
If you set `NDD_STATE_DIR` for setup, use that same value for full uninstall.

**Removal is permanent:** local edits inside owned NDD skills and installation
backups are deleted too. Your project source, specs, plans, project instructions,
unrelated skills and other Git settings are preserved. The agent applications
and their enclosing `.agents` / `.claude` folders are not removed.

<details>
<summary>Uninstall NDD for Codex only</summary>

Removes:

- The six owned skill folders — `ndd-setup`, `ndd-spec`, `ndd-plan`, `ndd-do`,
  `ndd-help`, `ndd-review` —
  from `~/.agents/skills`.
- `~/.agents/skills.ndd-kit`, including installation receipts, backups and leftover
  staging files.

Keeps the Claude Code installation, the downloaded NDD source folder,
`~/.ndd/projects` and the `ndd.prefix` settings in your projects.

**Mac:**

Optional preview:

```bash
bash ./install.sh --codex --uninstall --dry-run
```

Uninstall:

```bash
bash ./install.sh --codex --uninstall
```

**Windows:**

Optional preview:

```powershell
powershell -NoProfile -File .\install.ps1 -Codex -Uninstall -DryRun
```

Uninstall:

```powershell
powershell -NoProfile -File .\install.ps1 -Codex -Uninstall
```

</details>

<details>
<summary>Uninstall NDD for Claude Code only</summary>

Removes:

- The six owned skill folders — `ndd-setup`, `ndd-spec`, `ndd-plan`, `ndd-do`,
  `ndd-help`, `ndd-review` —
  from `~/.claude/skills`.
- `~/.claude/skills.ndd-kit`, including installation receipts, backups and leftover
  staging files.

Keeps the Codex installation, the downloaded NDD source folder,
`~/.ndd/projects` and the `ndd.prefix` settings in your projects.

**Mac:**

Optional preview:

```bash
bash ./install.sh --claude --uninstall --dry-run
```

Uninstall:

```bash
bash ./install.sh --claude --uninstall
```

**Windows:**

Optional preview:

```powershell
powershell -NoProfile -File .\install.ps1 -Claude -Uninstall -DryRun
```

Uninstall:

```powershell
powershell -NoProfile -File .\install.ps1 -Claude -Uninstall
```

</details>

<details>
<summary>Uninstall NDD completely</summary>

Removes:

- The six owned NDD skill folders from both `~/.agents/skills` and
  `~/.claude/skills`, including local edits.
- Both installation metadata folders, `~/.agents/skills.ndd-kit` and
  `~/.claude/skills.ndd-kit`, including all receipts, backups and leftover staging files.
- The local Git config entry `ndd.prefix` in each project recorded in
  `~/.ndd/projects`, only when its value still matches the registered prefix.
  Other entries and global Git config are preserved.
- Successfully cleaned project records, then `~/.ndd/projects` if empty and
  `~/.ndd` if empty.
- The NDD source clone containing the running installer, only if it is a verified
  standalone clone of the official repository, is clean and has no unpublished
  work or linked worktrees.

**Project cleanup continues on errors.** If a project is missing, its prefix has
changed or its config cannot be updated, the installer warns, keeps that record
and moves on. These failures do not block removal of NDD skills or source.
An unreadable or locked registry is also skipped with a warning.

Only registered projects are checked; the installer does not search your disk.
Unresolved records can remain in `~/.ndd/projects` after uninstall.

**Source cleanup applies only to the clone running this installer.** Other clones
and downloads are not searched or removed. ZIP folders and modified or unverified
clones are kept with an explanation. Add `--keep-source` on Mac or `-KeepSource` on
Windows to preserve the source clone intentionally; project Git cleanup still runs.
See [source cleanup checks](docs/installation.md#source-clone-cleanup) for details.

**Mac:**

Optional preview:

```bash
bash ./install.sh --all --uninstall --dry-run
```

Uninstall:

```bash
bash ./install.sh --all --uninstall
```

**Windows:**

Optional preview:

```powershell
powershell -NoProfile -File .\install.ps1 -All -Uninstall -DryRun
```

Uninstall:

```powershell
powershell -NoProfile -File .\install.ps1 -All -Uninstall
```

</details>

## Learn more

- [Example spec](examples/002-csv-export/spec.md) and [plan](examples/002-csv-export/plan.md)
- [Project setup](docs/setup.md)
- [Workflow and approvals](docs/workflow.md)
- [Installation options and troubleshooting](docs/installation.md)
- [Development checks](docs/testing.md)

Inspired by [GitHub Spec Kit](https://github.com/github/spec-kit). [MIT license](LICENSE).
