# NDD — Nap-Driven Development

NDD is a lightweight spec-driven workflow for **Claude Code and Codex**, on **Mac
and Windows**. It turns an idea or bug report into a clear specification, a practical
plan, and small implementation tasks with checks for the result.

You review the spec and plan before coding begins. Both stay with your project,
so you can pick up the work in a new session or continue with another agent.
Start with one task — there is no need to document your entire codebase or replace
your team's existing rules.

```text
╭──────────╮   ╭──────────────╮   ╭──────────────╮   ╭───────────╮   ╭────────╮
│ Describe │ → │ Approve spec │ → │ Approve plan │ → │ Implement │ → │ Verify │
╰──────────╯   ╰──────────────╯   ╰──────────────╯   ╰───────────╯   ╰────────╯
```

## Install

Install once on each computer. You need **Git** and **Claude Code or Codex**.
Expand your operating system's instructions below. Complete steps 1 and 2, then choose one option
in step 3. Run each command separately; optional previews make no changes.

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

Choose one option below.

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

Choose one option below.

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

Restart your agent after installation. `--all` / `-All` installs NDD skills for
both agents; it does not install the agents themselves.
[Custom installation folders and troubleshooting →](docs/installation.md)

<details>
<summary>No Git? Download a ZIP instead</summary>

1. On the [repository page](https://github.com/avkaz/nap-driven-development), choose **Code → Download ZIP**.
2. Extract the ZIP and open Terminal or PowerShell in the extracted folder.
3. Run **step 3** from the Mac or Windows instructions above.

</details>

## Use it in your project

Open your existing project in Claude Code or Codex. Enter these commands **in the
agent's chat**, not in the terminal. In Codex, you can also select the skill from
the skill picker.

| Step | Claude Code | Codex |
|---|---|---|
| Check project and choose prefix | `/ndd-setup` | `$ndd-setup` |
| Describe a task | `/ndd-spec Fix CSV export` | `$ndd-spec Fix CSV export` |
| Review the spec | Say “I approve this spec” when ready | Same |
| Create a plan | `/ndd-plan 001` | `$ndd-plan 001` |
| Review the plan | Say “I approve this plan” when ready | Same |
| Implement the next task | `/ndd-do 001` | `$ndd-do 001` |

Setup suggests a personal prefix from your Git name, such as `ak`. Accept it or
choose your own. After your confirmation, it saves `ndd.prefix` in the existing
local Git config — no separate project file, and nothing to commit. A new clone
needs its own setup; use the same prefix on your other computer.
Setup also records the project and prefix in `~/.ndd/projects`, shared by Claude
and Codex, so full uninstall can remove the recorded Git setting later.

`ndd-plan 001` then means your `ak-001` feature. To select a teammate's feature,
use its prefix, e.g. `ndd-plan iv-001`. Repeat `ndd-do` to continue through the plan.
Choose different prefixes within the team; ambiguous matches always need clarification.

**Setup preserves your project instructions.** It checks readiness and reports conflicts.
Editing existing `AGENTS.md` / `CLAUDE.md` requires your approval of a specific fix.

You write specs only for the tasks you choose. No need to document the whole
existing project. Templates stay with the installed skills; task documents live here:

```text
your-project/
└── specs/
    └── ak-001-fix-csv-export/
        ├── spec.md
        └── plan.md
```

These are ordinary project files: commit them with the code if you want to share
them. NDD does not commit or push anything automatically.

## Update

In your cloned NDD folder, download the latest changes:

```sh
git pull --ff-only
```

If you used a ZIP, download and extract a fresh copy instead of running `git pull`.

Then choose your operating system and the agents you want to update.
Run the selected command from the updated NDD folder.

<details>
<summary><strong>Update for Mac</strong></summary>

<details>
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

- The four owned skill folders — `ndd-setup`, `ndd-spec`, `ndd-plan`, `ndd-do` —
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

- The four owned skill folders — `ndd-setup`, `ndd-spec`, `ndd-plan`, `ndd-do` —
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

- The four owned NDD skill folders from both `~/.agents/skills` and
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
