# NDD — Nap-Driven Development

A simple spec-driven workflow for **Claude Code and Codex**, on **Mac and Windows**.
Describe a task → approve the spec → approve the plan → let the agent implement it.

## Install

Install once on each computer. You need **Git** and **Claude Code or Codex**.
Click your operating system below. Run each command separately, in order.

<details>
<summary><strong>Mac — show installation</strong></summary>

Open **Terminal**.

**1. Download NDD:**

```bash
git clone https://github.com/avkaz/nap-driven-development.git
```

**2. Open the downloaded folder:**

```bash
cd nap-driven-development
```

**3. Install the skills for both agents:**

```bash
bash ./install.sh --all
```

</details>

<details>
<summary><strong>Windows — show installation</strong></summary>

Open **PowerShell**.

**1. Download NDD:**

```powershell
git clone https://github.com/avkaz/nap-driven-development.git
```

**2. Open the downloaded folder:**

```powershell
cd nap-driven-development
```

**3. Install the skills for both agents:**

```powershell
powershell -NoProfile -File .\install.ps1 -All
```

If Windows blocks the script, see [Windows installation help](docs/installation.md#windows-execution-policy).

</details>

Restart your agent after installation. `--all` / `-All` installs NDD skills for
both agents; it does not install the agents themselves.
[Install for just one agent or choose another folder →](docs/installation.md)

<details>
<summary>No Git? Download a ZIP instead</summary>

1. On the [repository page](https://github.com/avkaz/nap-driven-development), choose **Code → Download ZIP**.
2. Extract the ZIP and open Terminal or PowerShell in the extracted folder.
3. Run **step 3** from the Mac or Windows instructions above.

For a specific published version, use [Releases](https://github.com/avkaz/nap-driven-development/releases).

</details>

## Use it in your project

Open your existing project in Claude Code or Codex. Enter these commands **in the
agent's chat**, not in the terminal. In Codex, you can also select the skill from
the skill picker.

| Step | Claude Code | Codex |
|---|---|---|
| Check the project | `/ndd-setup` | `$ndd-setup` |
| Describe a task | `/ndd-spec Fix CSV export` | `$ndd-spec Fix CSV export` |
| Review the spec | Say “I approve this spec” when ready | Same |
| Create a plan | `/ndd-plan 001` | `$ndd-plan 001` |
| Review the plan | Say “I approve this plan” when ready | Same |
| Implement the next task | `/ndd-do 001` | `$ndd-do 001` |

Replace `001` with your feature's number. Repeat `ndd-do` to continue through the plan.

**Setup normally changes nothing.** It checks readiness and reports conflicts.
Editing existing `AGENTS.md` / `CLAUDE.md` requires your approval of a specific fix.

You write specs only for the tasks you choose. No need to document the whole
existing project. Templates stay with the installed skills; task documents live here:

```text
your-project/
└── specs/
    └── 001-fix-csv-export/
        ├── spec.md
        └── plan.md
```

These are ordinary project files: commit them with the code if you want to share
them. NDD does not commit or push anything automatically.

## What does dry run mean?

**“Show what would happen, without changing anything.”** It is optional.
You do not need it before installing or using NDD.

Add `--dry-run` on Mac or `-DryRun` on Windows to the installer command to preview
an install or removal. Project setup uses plain `ndd-setup`, without flags.

<details>
<summary>Show an installation preview</summary>

Run from the downloaded NDD folder. These commands **do not install** anything.

**Mac:**

```bash
bash ./install.sh --all --dry-run
```

**Windows:**

```powershell
powershell -NoProfile -File .\install.ps1 -All -DryRun
```

To actually install, use step 3 in the installation instructions.

</details>

## Update or uninstall

<details>
<summary>Update NDD</summary>

In your cloned NDD folder, download the latest changes:

```sh
git pull --ff-only
```

Then rerun **step 3** for your operating system and restart the agent.
If you used a ZIP, download and extract a fresh copy instead, then run step 3.
Existing project specs and plans stay unchanged.

</details>

<details>
<summary>Uninstall NDD</summary>

Run from the downloaded NDD folder. Use version **0.3.0 or newer** to remove old backups too.

**This deletes installed NDD skills, their local edits and all installation backups.**
Project files, unrelated skills and the downloaded NDD folder are preserved.

**Mac:**

```bash
bash ./install.sh --all --uninstall
```

**Windows:**

```powershell
powershell -NoProfile -File .\install.ps1 -All -Uninstall
```

To preview removal first, add `--dry-run` / `-DryRun` to the uninstall command.

</details>

## Learn more

- [Example spec](examples/002-csv-export/spec.md) and [plan](examples/002-csv-export/plan.md)
- [Setup and existing projects](docs/setup.md)
- [Workflow and approvals](docs/workflow.md)
- [Installation options and troubleshooting](docs/installation.md)
- [Tests and verification status](docs/testing.md) · [Building releases](docs/releasing.md)

Inspired by [GitHub Spec Kit](https://github.com/github/spec-kit). [MIT license](LICENSE).
