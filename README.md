# NDD — Nap-Driven Development

![Nap-Driven Development — a developer and cat nap while two robot assistants plan and code](docs/assets/nap-driven-development.png)

[![CI](https://github.com/avkaz/nap-driven-development/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/avkaz/nap-driven-development/actions/workflows/ci.yml)

NDD helps **Claude Code and Codex** implement changes that match your requirements.
It keeps the scope, tasks and verification results in your project, so you can
continue work across sessions or switch agents. Available on **Mac and Windows**.

Use NDD in new or existing projects. Optional project documents capture goals,
capabilities and links to existing rules while preserving your structure and tools.
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

[Download the current source ZIP](https://github.com/avkaz/nap-driven-development/archive/refs/heads/main.zip)
or install with Git below.

## Install

Install once on each computer. You need **Git** and **Claude Code or Codex**.
Install, update and uninstall commands run from the downloaded **NDD folder**.
Run NDD chat commands inside the project you are working on.

The commands below save NDD in `nap-driven-development` in your home folder,
so you can return to it from any terminal location. If you already downloaded
NDD elsewhere, use that folder's full path instead; you do not need another clone.
[Finding your NDD folder →](docs/installation.md#find-your-ndd-folder)

<details>
<summary><strong>Install for Mac</strong></summary>

Open **Terminal**.

**1. Download NDD:**

```bash
git clone https://github.com/avkaz/nap-driven-development.git "$HOME/nap-driven-development"
```

**2. Open NDD from any folder:**

```bash
cd "$HOME/nap-driven-development"
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
git clone https://github.com/avkaz/nap-driven-development.git "$env:USERPROFILE\nap-driven-development"
```

**2. Open NDD from any folder:**

```powershell
Set-Location -LiteralPath "$env:USERPROFILE\nap-driven-development"
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

1. Download the [current source ZIP](https://github.com/avkaz/nap-driven-development/archive/refs/heads/main.zip).
2. Extract the ZIP and open Terminal or PowerShell in the extracted folder.
3. Run **step 3** from the Mac or Windows instructions above.

</details>

## Use

Run these commands in your agent's chat. Codex uses `$`; Claude Code uses `/`.

| Action | Codex | Claude Code |
|---|---|---|
| Check project and choose prefix | `$ndd-setup` | `/ndd-setup` |
| Optional, any project: capture goals, capabilities and rules | `$ndd-init` | `/ndd-init` |
| Describe a change | `$ndd-spec Fix CSV export` | `/ndd-spec Fix CSV export` |
| Plan an approved spec | `$ndd-plan 001` | `/ndd-plan 001` |
| Complete an approved plan | `$ndd-do 001` | `/ndd-do 001` |
| Execute only task T2 | `$ndd-do 001 T2` | `/ndd-do 001 T2` |
| Review the latest stage | `$ndd-review 001` | `/ndd-review 001` |
| Review a specific stage | `$ndd-review 001 plan` | `/ndd-review 001 plan` |
| Show command reference | `$ndd-help` | `/ndd-help` |

Workflow: setup → init (optional, any project) → spec → approve → plan → approve → do + verify.

Start with `ndd-setup`. Optionally use `ndd-init` in a new or existing project
to capture its goals and main capabilities. For an existing project, the agent
studies relevant docs and code, summarizes its understanding and asks about gaps.
Existing rules can be linked from `ndd-specs/project/rules.md` without duplicating them.
Choose and approve only the documents you need, or skip init and use `ndd-spec`
for the next change. Init is never required to use NDD.
[Project initialization and progress →](docs/init.md)

Approve each task spec and plan in chat before proceeding. After showing a spec, the
agent offers **Approve spec and continue with Plan** for that feature. Selecting
it approves the spec and starts planning; the plan still needs its own approval.
Interactive choices depend on the host; a short chat reply also works.

`ndd-do 001` completes all remaining tasks and final verification.
`ndd-do 001 T2` runs only T2 and its checks, then stops. Unfinished prerequisites
are reported; a later `ndd-do 001` resumes the remaining work.

Review is optional. Use `spec`, `plan` or `code` to select a stage, for example
`ndd-review 001 spec` or `ndd-review 001 code`. Findings appear in chat, with an
option to save `review.md`. Review does not run tests or replace approval and
verification. `ndd-help` shows a compact command reference and works before setup.

## Feature IDs and files

Setup confirms a personal prefix such as `ak` and saves it as local Git config
`ndd.prefix`. Then `001` means `ak-001`; use `iv-001` to select another prefix.
Numbers advance separately per prefix. Each clone needs its own setup.

New NDD projects use `ndd-specs/` by default. Existing NDD documents in `specs/`
or a configured location stay there; no automatic move is performed. An unrelated
`specs/` folder is left untouched. If both roots contain NDD work, choose the root
or provide a full task path.

```text
ndd-specs/
├── project/             (optional; choose any files)
│   ├── spec.md          (purpose and scope)
│   ├── features.md      (main capabilities, stages and task links)
│   └── rules.md         (agreed project conventions)
└── ak-001-fix-csv-export/
    ├── spec.md
    ├── plan.md
    └── review.md        (optional)
```

Task specs contain a goal and acceptance criteria; plans contain tasks and checks.
Create them only for changes you choose. These are ordinary files you can commit
with your code.

Spec, plan and do use optional project context and refresh relevant task links and
progress in an existing capability overview. Review reports stale entries without
editing them. This happens during commands, not through a background watcher.
One completed task does not automatically complete an entire capability.
NDD preserves existing `AGENTS.md` / `CLAUDE.md` instructions and
does not commit, push or deploy automatically.

## Update

Open your NDD folder, pull the current source, then reinstall for your chosen
agents. Use your actual path if you downloaded NDD somewhere else. If you used a
ZIP, download and extract a fresh copy and skip `git pull`.


<details>
<summary><strong>Update for Mac</strong></summary>

Open NDD from any folder:

```bash
cd "$HOME/nap-driven-development"
```

After the folder opens successfully, download the changes:

```bash
git pull --ff-only
```

After a successful pull, choose one install command below.

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

Open NDD from any folder:

```powershell
Set-Location -LiteralPath "$env:USERPROFILE\nap-driven-development"
```

After the folder opens successfully, download the changes:

```powershell
git pull --ff-only
```

After a successful pull, choose one install command below.

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

Open your downloaded NDD folder, then choose **one** removal command below.
If you downloaded NDD elsewhere, use its actual path in the first command.

<details>
<summary><strong>Uninstall for Mac</strong></summary>

**1. Open the NDD folder:**

```bash
cd "$HOME/nap-driven-development"
```

**2. After the folder opens successfully, choose one option:**

Remove NDD for Claude Code only:

```bash
bash ./install.sh --claude --uninstall
```

Remove NDD for Codex only:

```bash
bash ./install.sh --codex --uninstall
```

Remove NDD completely:

```bash
bash ./install.sh --all --uninstall
```

</details>

<details>
<summary><strong>Uninstall for Windows</strong></summary>

**1. Open the NDD folder:**

```powershell
Set-Location -LiteralPath "$env:USERPROFILE\nap-driven-development"
```

**2. After the folder opens successfully, choose one option:**

Remove NDD for Claude Code only:

```powershell
powershell -NoProfile -File .\install.ps1 -Claude -Uninstall
```

Remove NDD for Codex only:

```powershell
powershell -NoProfile -File .\install.ps1 -Codex -Uninstall
```

Remove NDD completely:

```powershell
powershell -NoProfile -File .\install.ps1 -All -Uninstall
```

</details>

Add `--dry-run` / `-DryRun` to a removal command to preview.

Removal deletes the selected NDD skills, including local edits, and their install
metadata. Your project code, specs and unrelated skills remain. Full removal also
cleans registered NDD prefixes and may delete the verified clean source clone;
add `--keep-source` / `-KeepSource` to keep it. Reuse any custom destination or
`NDD_STATE_DIR` settings from installation/setup.
[Removal details and troubleshooting →](docs/installation.md#uninstall)

## Learn more

- [Example spec](examples/002-csv-export/spec.md) and [plan](examples/002-csv-export/plan.md)
- [Project setup](docs/setup.md)
- [Optional project context](docs/init.md)
- [Workflow and approvals](docs/workflow.md)
- [Installation options and troubleshooting](docs/installation.md)
- [Development checks](docs/testing.md)

Inspired by [GitHub Spec Kit](https://github.com/github/spec-kit). [MIT license](LICENSE).
